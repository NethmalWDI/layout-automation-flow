#!/usr/bin/env python3
"""S0 — ingest and freeze a design package, bind devices to SKY130 Magic PCells.

usage (inside layout-s0s3, from /foss/designs):
    python3 -m src.s0.ingest inputs/example_ota_5t/package.yaml [--skip-sim]

Outputs (outputs/S0/<design>/):
    circuit_ir.json      canonical description (devices, nets, ports, hierarchy, specs, margins)
    device_map.json      device -> exact PDK PCell call (magic::gencell sky130::<model>)
    pdk_config.yaml      PDK, tool versions, decks, unit conventions
    ref/<d>_full.spice   the circuit as simulated (bias sources kept)
    ref/<d>_layout.spice the circuit as laid out / LVS reference (bias sources -> ports)
    tb/                  re-run testbenches and logs
    s0_report.json       every gate with pass/fail and evidence
Nothing here edits an input file. Missing upstream items are reported, never invented.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

import yaml

from src.common import spice
from src.common.tools import (REPO, PDK_ROOT, provenance, rel, run_netgen_compare, run_ngspice,
                              sha256, write_json)

ALLOWED_MODELS = ["sky130_fd_pr__nfet_01v8", "sky130_fd_pr__pfet_01v8",
                  "sky130_fd_pr__nfet_01v8_lvt", "sky130_fd_pr__pfet_01v8_lvt"]
ROLE_BY_IFACE = {"INP": "input", "INN": "input", "OUTP": "output", "OUTN": "output",
                 "VDD": "supply", "VSS": "ground"}
TB_TOL = {"default_rel": 1e-3}  # same netlist, same tools -> results must reproduce to 0.1 %


def load_package(path: Path) -> dict:
    pkg = yaml.safe_load(path.read_text())
    if "inherit" in pkg:
        base = load_package(REPO / pkg["inherit"])
        base.update({k: v for k, v in pkg.items() if k != "inherit"})
        pkg = base
    pkg["_package_file"] = str(path)
    return pkg


def p(pkg_rel: str | None) -> Path | None:
    return (REPO / pkg_rel) if pkg_rel else None


# ---------------------------------------------------------------- hierarchy via name map
def map_hierarchy(pkg: dict, nl: spice.Netlist) -> tuple[list, list, dict]:
    """Return (blocks, findings, name_map). Blocks come from the upstream primitives.json
    through the explicit name map; terminal-by-terminal consistency is checked."""
    up = pkg.get("upstream") or {}
    if not up.get("primitives") or not up.get("name_map"):
        return [], [{"level": "missing", "msg": "no upstream hierarchy/name map provided"}], {}
    prim = json.loads(p(up["primitives"]).read_text())
    nmap = yaml.safe_load(p(up["name_map"]).read_text())
    up_nl = spice.parse(p(up["netlist"]))
    up_dev = {m.name: m for m in up_nl.mosfets}
    tgt_dev = {m.name: m for m in nl.mosfets}
    dmap, nmap_n = nmap["devices"], nmap["nets"]
    findings, blocks = [], []
    for inst in prim["instances"]:
        devs = []
        for _, up_name in inst["transistors"].items():
            t = dmap.get(up_name)
            if t is None:
                findings.append({"level": "manual", "msg": f"upstream {up_name} ({inst['subckt']}) has no target device"})
                continue
            if t not in tgt_dev:
                findings.append({"level": "error", "msg": f"name map points {up_name} -> {t}, not in netlist"})
                continue
            u, g = up_dev[up_name], tgt_dev[t]
            if u.polarity != g.polarity:
                findings.append({"level": "error", "msg": f"{up_name}->{t}: polarity {u.polarity} vs {g.polarity}"})
            for term in "dgsb":
                un = u.terminals[term]
                expect = nmap_n.get(un, "__unmapped__")
                got = g.terminals[term]
                if expect is None or expect == "__unmapped__":
                    findings.append({"level": "manual", "msg": f"{up_name}.{term} on upstream net {un} (unmapped); target {t}.{term} on {got}"})
                elif expect != got:
                    findings.append({"level": "error", "msg": f"{up_name}.{term}: upstream {un} -> {expect}, but target {t}.{term} is on {got}"})
            devs.append(t)
        blocks.append({"name": inst["subckt"], "category": inst["category"], "primitive": inst["primitive"],
                       "devices": devs, "source": "name_map" if len(devs) == len(inst["transistors"]) else "name_map+manual",
                       "upstream_instance": inst["instance"]})
    for note in nmap.get("manual", []):
        findings.append({"level": "assumption", "msg": note})
    covered = {d for b in blocks for d in b["devices"]}
    for m in nl.mosfets:
        if m.name not in covered:
            findings.append({"level": "error", "msg": f"target device {m.name} belongs to no block"})
    return blocks, findings, nmap


# ---------------------------------------------------------------- specs and margins
def specs_and_margins(cfg: dict, achieved: dict, units: dict) -> tuple[dict, dict]:
    specs, margins = cfg.get("specs", {}), {}
    for k, lim in specs.items():
        if k not in achieved or achieved[k] is None:
            margins[k] = {"status": "not_evaluated", "reason": "no achieved value"}
            continue
        a = achieved[k]
        if "min" in lim:
            margins[k] = {"kind": "min", "limit": lim["min"], "achieved": a, "margin": a - lim["min"], "units": units.get(k)}
        elif "max" in lim:
            margins[k] = {"kind": "max", "limit": lim["max"], "achieved": a, "margin": lim["max"] - a, "units": units.get(k)}
        margins[k]["meets"] = margins[k]["margin"] >= 0
    return specs, margins


# ---------------------------------------------------------------- writers
def fmt(x: float) -> str:
    return f"{x:.6g}"


def write_full(nl: spice.Netlist, name: str) -> str:
    """The circuit exactly as simulated: every original parameter kept, bias sources kept."""
    lines = [f".subckt {name} " + " ".join(nl.ports)]
    for m in nl.mosfets:
        lines.append(spice.mos_line(m.name, m.terminals, m.model, m.params))
    for s in nl.sources:
        lines.append(f"{s.name} {s.p} {s.n} {s.value}")
    for c in nl.passives:
        lines.append(f"{c.name} {c.a} {c.b} {c.value}")
    lines.append(f".ends {name}")
    return "\n".join(lines) + "\n"


def write_layout(nl: spice.Netlist, name: str, bias: dict) -> tuple[str, list]:
    """The circuit as laid out: ideal bias sources removed, their node exposed as a port (µm units)."""
    ren = {}
    for s in nl.sources:
        if s.name in bias:
            ren[s.p] = bias[s.name]
    ports = list(nl.ports) + [v for v in bias.values()]
    lines = [f".subckt {name} " + " ".join(ports)]
    for m in nl.mosfets:
        t = {k: ren.get(v, v) for k, v in m.terminals.items()}
        prm = {"L": fmt(m.num("L")), "W": fmt(m.num("W")), "nf": int(m.num("NF", 1))}
        mult = int(m.num("MULT", m.params.get("M", 1)))
        if mult != 1:
            prm["m"] = mult
        lines.append(spice.mos_line(m.name, t, m.model, prm))
    unhandled = [s.name for s in nl.sources if s.name not in bias]
    lines.append(f".ends {name}")
    return "\n".join(lines) + "\n", unhandled


def wrap_original(src: Path, dst: Path, name: str) -> None:
    """xschem writes the top subckt header commented ('**.subckt'); make a plain subckt copy for netgen."""
    out = []
    for ln in src.read_text().splitlines():
        if re.match(r"^\*\*\.subckt\b", ln):
            ln = ln[2:]
        elif re.match(r"^\*\*\.ends\b", ln):
            ln = ln[2:]
        elif ln.strip().lower() == ".end":
            continue
        out.append(ln)
    dst.write_text("\n".join(out) + "\n")


# ---------------------------------------------------------------- testbenches
def patched_deck(tb: Path, dut_name: str, dut_text: str, cond: dict) -> str:
    txt = tb.read_text()
    blk = re.compile(rf"^\.subckt\s+{re.escape(dut_name)}\b.*?^\.ends\b[^\n]*\n", re.S | re.M)
    if not blk.search(txt):
        raise RuntimeError(f"{tb.name}: DUT subckt {dut_name} not found")
    txt = blk.sub(lambda _: dut_text, txt, count=1)
    params = " ".join(f"{k}={v}" for k, v in cond.items() if k not in ("temp", "corner"))
    txt, n = re.subn(r"^\.param .*$", f".param {params}", txt, count=1, flags=re.M)
    if n != 1:
        raise RuntimeError(f"{tb.name}: no .param line to set conditions")
    if "temp" in cond:
        txt = re.sub(r"^\.temp .*$", f".temp {cond['temp']}", txt, count=1, flags=re.M)
    if "corner" in cond:
        txt = re.sub(r"(sky130\.lib\.spice)\s+\w+", rf"\1 {cond['corner']}", txt, count=1)
    return txt


# ---------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("package")
    ap.add_argument("--skip-sim", action="store_true", help="skip testbench re-run (for quick checks)")
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)

    pkg_path = (REPO / a.package) if not Path(a.package).is_absolute() else Path(a.package)
    pkg = load_package(pkg_path)
    design = pkg["design"]
    out = Path(a.out) if a.out else REPO / "outputs" / "S0" / design
    (out / "ref").mkdir(parents=True, exist_ok=True)
    gates, notes = {}, []

    # --- netlist
    nl_path = p(pkg["netlist"])
    nl = spice.parse(nl_path)
    errs = spice.validate(nl, ALLOWED_MODELS)
    gates["G0.1_inventory"] = {"pass": len(nl.mosfets) > 0 and not any("model" in e for e in errs),
                               "mosfets": len(nl.mosfets), "sources": len(nl.sources), "passives": len(nl.passives)}
    gates["G0.2_validation"] = {"pass": not errs, "errors": errs}

    # --- freeze check against hashes recorded at copy time
    recorded = {}
    sha_file = REPO / "circuits" / "SOURCE_SHA256.txt"
    if sha_file.exists():
        for ln in sha_file.read_text().splitlines():
            h, f = ln.split(maxsplit=1)
            recorded[f.strip()] = h
    checked = []
    for key in ("netlist", "config", "achieved"):
        if pkg.get(key):
            f = rel(p(pkg[key])).replace("circuits/", "", 1)
            checked.append({"file": pkg[key], "recorded": recorded.get(f), "now": sha256(p(pkg[key])),
                            "match": recorded.get(f) == sha256(p(pkg[key]))})
    gates["G0.3_hash_freeze"] = {"pass": all(c["match"] for c in checked), "files": checked}

    # --- specs, conditions, achieved
    cfg = yaml.safe_load(p(pkg["config"]).read_text())
    cond = dict(cfg.get("conditions", {}))
    cond.update(pkg.get("conditions_override") or {})
    ach_raw = json.loads(p(pkg["achieved"]).read_text()) if pkg.get("achieved") else {}
    achieved = {k: v for grp in ach_raw.get("measurements", {}).values() for k, v in grp.items()}
    units = ach_raw.get("units", {})

    # --- ports and roles
    iface = cfg.get("interface", {}).get("ports", {})
    port_roles = []
    for prt in nl.ports:
        std = next((k for k, v in iface.items() if v == prt), prt)
        port_roles.append({"name": prt, "role": ROLE_BY_IFACE.get(std, "unknown"),
                           "direction": nl.port_dirs.get(prt, "unknown"), "testbench_port": std})
    bias = pkg.get("bias_sources") or {}
    for s_name, port in bias.items():
        port_roles.append({"name": port, "role": "bias", "direction": "input",
                           "testbench_port": None, "note": f"node of internal source {s_name}, exposed for layout"})

    # --- hierarchy through the name map
    blocks, findings, _nmap = map_hierarchy(pkg, nl)
    gates["G0.4_name_map"] = {"pass": not any(f["level"] == "error" for f in findings), "findings": findings}

    # --- reference netlists
    full_name, lay_name = design, design
    full_txt = write_full(nl, full_name)
    lay_txt, unhandled = write_layout(nl, lay_name, bias)
    (out / "ref" / f"{design}_full.spice").write_text(full_txt)
    (out / "ref" / f"{design}_layout.spice").write_text(lay_txt)
    if unhandled:
        notes.append(f"sources kept inside the layout view (not declared as bias): {unhandled}")

    # --- round trip: IR-written netlist vs the original, in netgen
    wrapped = out / "ref" / "original_wrapped.spice"
    wrap_original(nl_path, wrapped, nl.name)
    gates["G0.5_round_trip_lvs"] = run_netgen_compare(out / "ref" / f"{design}_full.spice", full_name,
                                                      wrapped, nl.name, out / "ref" / "round_trip_lvs.txt")

    # --- testbench re-run with the IR-written DUT
    tb_results = {}
    if not a.skip_sim:
        dut_name = pkg["dut_subckt_in_testbench"]
        dut_text = write_full(nl, dut_name)
        for tb_rel in pkg.get("testbenches", []):
            tb = p(tb_rel)
            deck = out / "tb" / tb.name
            deck.parent.mkdir(parents=True, exist_ok=True)
            deck.write_text(patched_deck(tb, dut_name, dut_text, cond))
            tb_results[tb.stem] = run_ngspice(deck, out / "tb")
    measured = {k: v for r in tb_results.values() for k, v in r["meas"].items()}

    # --- achieved specs: upstream values, or generated (stress variants)
    ach_source = "upstream measurements.json"
    if pkg.get("specs_from_achieved"):
        achieved, ach_source = dict(measured), "generated by this S0 run (conditions_override)"
        specs = copy.deepcopy(cfg.get("specs", {}))
        for k, rule in pkg["specs_from_achieved"].items():
            if k in achieved and achieved[k] is not None:
                v = achieved[k]
                if "min_delta" in rule:
                    specs[k] = {"min": round(v + rule["min_delta"], 4)}
                if "min_factor" in rule:
                    specs[k] = {"min": round(v * rule["min_factor"], 4)}
        cfg = {**cfg, "specs": specs}
        notes.append("ASSUMPTION: stress-variant specs derived from its own achieved values "
                     f"by {pkg['specs_from_achieved']}; this is a test case, not a design target")
        gates["G0.6_testbench_reproduction"] = {"pass": all(r["rc"] == 0 for r in tb_results.values()) and bool(measured),
                                                "note": "no upstream values to compare (stress variant)",
                                                "measured": measured}
    elif not a.skip_sim:
        cmp = {}
        for k, ref in achieved.items():
            got = measured.get(k)
            ok = got is not None and abs(got - ref) <= TB_TOL["default_rel"] * max(abs(ref), 1e-12)
            cmp[k] = {"upstream": ref, "rerun": got, "ok": ok}
        gates["G0.6_testbench_reproduction"] = {"pass": all(c["ok"] for c in cmp.values()) and
                                                all(r["rc"] == 0 for r in tb_results.values()),
                                                "tolerance_rel": TB_TOL["default_rel"], "compare": cmp}
    else:
        gates["G0.6_testbench_reproduction"] = {"pass": None, "note": "skipped (--skip-sim)"}

    specs, margins = specs_and_margins(cfg, achieved, units)

    # --- device map: exact PCell calls
    devmap = []
    for m in nl.mosfets:
        W, L, nf = m.num("W"), m.num("L"), int(m.num("NF", 1))
        mult = int(m.num("MULT", m.params.get("M", 1)))
        ad_chk = None
        if nf == 1 and "AD" in m.params:
            ad_chk = abs(float(m.params["AD"]) - 0.29 * W) < 1e-6 * max(W, 1)
        devmap.append({
            "device": m.name, "polarity": m.polarity, "model": m.model,
            "netlist": {"W_um": W, "L_um": L, "nf": nf, "m": mult, "W_total_um": W * mult},
            "pcell": {"generator": "magic::gencell", "cell": f"sky130::{m.model}",
                      "params": {"w": W / nf, "l": L, "nf": nf, "m": mult},
                      "options": "defaults until S3 decides (guard, topc/botc, diffcov/polycov, via coverage)"},
            "conventions": {"netlist_W": "total width of one instance (xschem sky130); PCell w = W/nf per finger",
                            "ad_equals_0.29W_nf1": ad_chk},
        })

    # --- circuit IR
    nets = nl.nets()
    ir = {
        "schema": "circuit_ir/v1", "design": design, "description": pkg.get("description", ""),
        "subckt": nl.name,
        "ports": port_roles,
        "nets": [{"name": n, "kind": "port" if n in nl.ports else "internal",
                  "connections": [{"element": e, "terminal": t} for e, t in c]} for n, c in sorted(nets.items())],
        "devices": [{"name": m.name, "type": m.polarity, "model": m.model, "terminals": m.terminals,
                     "W_um": m.num("W"), "L_um": m.num("L"), "nf": int(m.num("NF", 1)),
                     "m": int(m.num("MULT", m.params.get("M", 1))),
                     "extra_params": {k: v for k, v in m.params.items() if k not in ("W", "L", "NF", "MULT", "M")},
                     "source_line": m.line_no} for m in nl.mosfets],
        "internal_sources": [{"name": s.name, "p": s.p, "n": s.n, "value": s.value,
                              "layout_handling": f"removed in layout view; node exposed as port {bias[s.name]}"
                              if s.name in bias else "kept"} for s in nl.sources],
        "hierarchy": {"blocks": blocks, "source": "upstream 5t-ota primitives through name map",
                      "findings": findings},
        "conditions": cond, "specs": specs, "achieved": achieved, "achieved_source": ach_source,
        "units": units, "margins": margins,
        "pending_inputs": {
            "operating_point": pkg.get("operating_point") or "not provided (S1 generates it with ngspice .op)",
            "variation_ranges": pkg.get("variation_ranges") or "not provided (awaiting PSO range format)",
            "nodal_analysis": (pkg.get("upstream") or {}).get("equations") or "not provided",
            "net_symbol_map": "not provided by upstream (requested); S1 derives it from the level-0 netlist",
        },
        "notes": notes,
    }
    inputs = [nl_path, p(pkg["config"]), p(pkg.get("achieved")), pkg_path] + \
             [p(x) for x in (pkg.get("upstream") or {}).values() if isinstance(x, str)] + \
             [p(x) for x in pkg.get("testbenches", [])]
    prov = provenance(inputs)
    ir["provenance"] = prov
    write_json(out / "circuit_ir.json", ir)
    write_json(out / "device_map.json", {"schema": "device_map/v1", "design": design, "devices": devmap,
                                          "provenance": prov})

    # --- PDK / tool configuration
    tv = {}
    tv_file = REPO / "runs" / "env" / "tool_versions.txt"
    if tv_file.exists():
        for ln in tv_file.read_text().splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                tv[k.strip()] = v.strip()
    pdkcfg = {
        "pdk": "sky130A", "pdk_root": PDK_ROOT, "tool_versions": tv,
        "decks": {"magicrc": f"{PDK_ROOT}/sky130A/libs.tech/magic/sky130A.magicrc",
                  "netgen_setup": f"{PDK_ROOT}/sky130A/libs.tech/netgen/sky130A_setup.tcl",
                  "klayout_lyp": f"{PDK_ROOT}/sky130A/libs.tech/klayout/tech/sky130A.lyp",
                  "spice_lib": f"{PDK_ROOT}/sky130A/libs.tech/combined/sky130.lib.spice"},
        "conventions": {"length_unit": "um (combined lib sets .option scale=1e-6)",
                        "W": "total width per instance; PCell w is per finger",
                        "corner": cond.get("corner"), "temp_C": cond.get("temp")},
        "device_generator": "Magic open_pdks sky130 PCells (canonical); see docs/04_device_generation.md",
    }
    (out / "pdk_config.yaml").write_text(yaml.safe_dump(pdkcfg, sort_keys=False))

    report = {"design": design, "package": rel(pkg_path), "gates": gates, "notes": notes,
              "testbenches": tb_results, "all_pass": all(g.get("pass") in (True, None) for g in gates.values()),
              "provenance": prov}
    write_json(out / "s0_report.json", report)
    for k, g in gates.items():
        print(f"{k:30s} {'PASS' if g.get('pass') else ('SKIP' if g.get('pass') is None else 'FAIL')}")
    print("S0", "PASS" if report["all_pass"] else "FAIL", "->", rel(out))
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
