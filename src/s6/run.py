"""S6 — extraction of the routed layouts and their parasitics against S2's budgets (plan v4, Phase 5).

For each routed layout of S5 (the budget-aware one, and the area-only baseline for H5):
  * Magic extracts the flattened top cell twice, with the code of scripts/reference_layout.py: a capacitance-only
    netlist (every capacitance, cthresh 0) and an R+C netlist (extresist, tolerance 100). S7 simulates both;
  * LVS of the flat extraction against S5's top-level reference (G6.1);
  * every capacitance is assigned: to a net's capacitance when its other side is an AC ground of S2 (supply, ground,
    bias AC ground, the nodes of an internal voltage source), to a coupling when both sides are signal nets;
  * G6.2: every budgeted net capacitance and coupling of S2 against its budget, from the extraction; every budgeted
    terminal resistance against its budget as S3's access R plus S5's top-level wire and via R (the block's own
    stubs and tracks are not in this sum: their effect is in S7's R+C simulation).
Node names: a flattened block net is '<block>_0.<net>'; a ring is '<body>_body'; a port has the layout view's name.

usage (inside layout-s0s3): python3 -m src.s6.run inputs/<d>/package.yaml   (or ./flow run <d> --stage S6)
Writes outputs/S6/<d>/: <rule>/ (netlists, logs), parasitics_vs_budgets.json, s6_report.json.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from src.common.hygiene import fresh_output_dir, gate_exit, new_run_id
from src.common.tools import REPO, provenance, rel, write_json
from src.s0.ingest import load_package
from src.s5 import route as R

sys.path.insert(0, str(REPO / "scripts"))
import reference_layout as RL  # noqa: E402

RULES = ("budget_aware", "area_only")
UNIT = {"a": 1e-3, "f": 1.0, "p": 1e3, "n": 1e6, "u": 1e9, "": 1e15}    # to fF
EXT_TOL = 0.05     # the C-only netlist's total may be this much below the .ext's (G6.4)


def ac_grounds(ir: dict) -> set:
    """S2's AC grounds (src/s2/run.py): supply, ground and bias AC ground ports, and both nodes of every internal
    voltage source."""
    return {p["name"] for p in ir["ports"] if p["role"] in ("supply", "ground", "bias_ac_ground")} | \
        {x for s in ir.get("internal_sources", []) if s.get("kind", "V") == "V" for x in (s["p"], s["n"])}


def node_net(node: str, nets: set, inv: dict) -> str | None:
    """The IR net of an extracted node: the part after the last '.' or '/', a layout-view name mapped back
    (VBIAS -> net2), a ring '<body>_body' to its body net; None for an unnamed node."""
    base = re.split(r"[./]", node)[-1]
    if base.endswith("_body"):
        base = base[: -len("_body")]
    base = inv.get(base, base)
    return base if base in nets else None


def capacitances(pex: Path, nets: set, inv: dict, gnd: set) -> dict:
    """{'net': {net: fF to AC ground}, 'coupling': {'a~b': fF}, 'unassigned': [...]} from a C-only netlist."""
    txt = re.sub(r"\n\+", " ", pex.read_text())
    out = {"net": {}, "coupling": {}, "unassigned": [], "n_caps": 0}
    for m in re.finditer(r"^C\S*\s+(\S+)\s+(\S+)\s+([0-9.eE+-]+)([afpnu]?)\b", txt, re.M):
        a, b = m.group(1), m.group(2)
        v = float(m.group(3)) * UNIT[m.group(4)]          # Magic writes e.g. 1.68612f; a bare number is farads
        out["n_caps"] += 1
        na, nb = node_net(a, nets, inv), node_net(b, nets, inv)
        if na is None or nb is None:
            out["unassigned"].append([a, b, round(v, 6)])
            continue
        if na == nb:
            continue
        ga, gb = na in gnd, nb in gnd
        if ga and gb:
            continue
        if ga or gb:
            n = nb if ga else na
            out["net"][n] = out["net"].get(n, 0.0) + v
        else:
            k = "~".join(sorted((na, nb)))
            out["coupling"][k] = out["coupling"].get(k, 0.0) + v
    out["net"] = {k: round(v, 4) for k, v in out["net"].items()}
    out["coupling"] = {k: round(v, 4) for k, v in out["coupling"].items()}
    return out


def ext_capacitances(ext: Path, nets: set, inv: dict, gnd: set) -> dict:
    """A cross-check of the C-only netlist against Magic's .ext of the flat cell (plan v4 Phase 6, flow record row 71).
    On LOADBench the netlist lacks the capacitance to ground of the nets that are transistor gates (FirstStageYout1,
    outFirstStage, ibias, in1, in2): its total is 8.9 % below the .ext's. Nodes are joined through the .ext's 'equiv'
    records; a 'node' record's capacitance is counted to the substrate (a ground net here), 'cap' records are
    couplings; values are in aF in the .ext. This reading puts all of a node's capacitance on the substrate, where
    Magic charges the part over an n-well to that well (the 5T's net3: 4.3 fF to VDD in the netlist), so per net it is
    an approximation; the totals ('total_fF') are exact and are what the check compares."""
    txt = ext.read_text()
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in re.findall(r'^equiv "([^"]+)" "([^"]+)"', txt, re.M):
        parent[find(a)] = find(b)
    names = {}
    for n in set(parent) | set(re.findall(r'^(?:node|substrate|port) "([^"]+)"', txt, re.M)):
        names.setdefault(find(n), []).append(n)
    net_of = {}
    for g, ms in names.items():
        found = sorted({x for x in (node_net(m, nets, inv) for m in ms) if x})
        net_of[g] = found[0] if len(found) == 1 else None
        if len(found) > 1:
            net_of[g] = "|".join(found)            # two nets in one group: a short; reported, never assigned
    sub = re.search(r'^substrate "([^"]+)"', txt, re.M)
    sub_net = net_of.get(find(sub.group(1))) if sub else None
    out = {"net": {}, "coupling": {}, "unassigned": [], "n_caps": 0, "substrate_net": sub_net,
           "substrate_is_ground": sub_net in gnd}

    def add(a, b, v):
        out["n_caps"] += 1
        na, nb = net_of.get(find(a)), net_of.get(find(b))
        if na is None or nb is None or "|" in na or "|" in nb:
            out["unassigned"].append([a, b, round(v, 6)])
            return
        if na == nb or (na in gnd and nb in gnd):
            return
        if na in gnd or nb in gnd:
            n = nb if na in gnd else na
            out["net"][n] = out["net"].get(n, 0.0) + v
        else:
            k = "~".join(sorted((na, nb)))
            out["coupling"][k] = out["coupling"].get(k, 0.0) + v
    for name, c in re.findall(r'^node "([^"]+)" \S+ (\S+)', txt, re.M):
        if float(c) > 0 and sub:
            add(name, sub.group(1), float(c) / 1000)
    for a, b, c in re.findall(r'^cap "([^"]+)" "([^"]+)" (\S+)', txt, re.M):
        add(a, b, float(c) / 1000)
    out["net"] = {k: round(v, 4) for k, v in out["net"].items()}
    out["coupling"] = {k: round(v, 4) for k, v in out["coupling"].items()}
    out["total_fF"] = round(sum(float(c) for c in re.findall(r'^node "[^"]+" \S+ (\S+)', txt, re.M)) / 1000 +
                            sum(float(c) for c in re.findall(r'^cap "[^"]+" "[^"]+" (\S+)', txt, re.M)) / 1000, 3)
    return out


def netlist_total(pex: Path) -> float:
    """Every capacitance in a C-only netlist, in fF."""
    txt = re.sub(r"\n\+", " ", pex.read_text())
    return round(sum(float(m.group(1)) * UNIT[m.group(2)] for m in
                     re.finditer(r"^C\S*\s+\S+\s+\S+\s+([0-9.eE+-]+)([afpnu]?)\b", txt, re.M)), 3)


def mim_self(s4: Path, out: Path) -> dict:
    """G6.5 (info; plan v4 Phase 7): each MIM capacitor block of S4 extracted alone, the same way as the layout.
    Magic's sky130 rules charge metal4 over metal3 everywhere (defaultoverlap allm4/allm3, 84 aF/um2), also where the
    top plate (capm, at metal4's potential) lies between them and the device model already counts the capacitance;
    so the coupling it reports between the two plates of a lone capacitor is, very likely, counted twice. S7 runs a
    view with it cancelled (G7.5). The bottom plate's capacitance to the substrate is real and stays."""
    f = s4 / "blocks.json"
    res = {}
    for b in (json.loads(f.read_text())["blocks"] if f.exists() else []):
        if b.get("kind") != "mim_cap":
            continue
        v = next(v for v in b["variants"] if v.get("ok"))
        top, bot = b["binding"]["top"], b["binding"]["bottom"]
        d = out / "mim_self" / b["name"]
        d.mkdir(parents=True, exist_ok=True)
        ex = RL.extract((REPO / v["build"]["gds"]).resolve(), v["cell"], d)
        txt = re.sub(r"\n\+", " ", ex["pex"].read_text())
        plates, sub = 0.0, 0.0
        for m in re.finditer(r"^C\S*\s+(\S+)\s+(\S+)\s+([0-9.eE+-]+)([afpnu]?)\b", txt, re.M):
            ends, val = {m.group(1), m.group(2)}, float(m.group(3)) * UNIT[m.group(4)]
            if ends == {top, bot}:
                plates += val
            elif bot in ends:
                sub += val
        res[b["name"]] = {"top": top, "bottom": bot, "plate_coupling_fF": round(plates, 4),
                          "bottom_to_substrate_fF": round(sub, 4), "netlist": rel(ex["pex"]),
                          "model": b["binding"]["model"], "params": b["binding"]["params"]}
    return res


def kpex_cross_check(gds: Path, cell: str, ref_top: Path, design: str, out: Path, magic_caps: dict, nets: set,
                     inv: dict, gnd: set) -> dict:
    """G6.3 (info): KLayout-PEX (kpex, 2.5D engine, sky130A) on the same layout. kpex runs KLayout's own LVS first; a
    net it cannot match is written unnamed ('$6'), so only the nets both tools name are compared (the substrate,
    'sky130_gnd', counts as ground)."""
    import subprocess
    from src.common.tools import TOOL_ENV
    out.mkdir(parents=True, exist_ok=True)
    ref = out / "ref_named.spice"
    ref.write_text(re.sub(rf"^(\.(?:subckt|ends))\s+{re.escape(design)}\b", rf"\1 {cell}", ref_top.read_text(), flags=re.M))
    r = subprocess.run(["kpex", "extract", "--pdk", "sky130A", "--gds", str(gds), "--cell", cell, "--schematic", str(ref),
                        "--2.5D", "--out_dir", str(out)], env=TOOL_ENV, capture_output=True, text=True, timeout=1800)
    (out / "kpex_run.log").write_text(r.stdout + r.stderr)
    f = next(iter(sorted(out.rglob("*_k25d_pex_netlist.spice"))), None)
    if f is None:
        return {"ran": False, "log": rel(out / "kpex_run.log")}
    k = capacitances(f, nets | {"sky130_gnd"}, inv, gnd | {"sky130_gnd"})
    named = sorted(set(k["net"]) & set(magic_caps["net"]))
    cpl = sorted(set(k["coupling"]) & set(magic_caps["coupling"]))
    tot_k = sum(k["net"].values()) + sum(k["coupling"].values()) + sum(x[2] for x in k["unassigned"])
    tot_m = sum(magic_caps["net"].values()) + sum(magic_caps["coupling"].values())
    return {"ran": True, "netlist": rel(f), "kpex_lvs_matched": "Netlists don't match" not in (r.stdout + r.stderr),
            "unnamed_nets": sorted({n.lstrip("\\") for a, b, _ in k["unassigned"] for n in (a, b) if n.lstrip("\\").startswith("$")}),
            "net_fF": {n: {"magic": magic_caps["net"][n], "kpex": k["net"][n]} for n in named},
            "coupling_fF": {c: {"magic": magic_caps["coupling"][c], "kpex": k["coupling"][c]} for c in cpl},
            "total_fF": {"magic": round(tot_m, 3), "kpex": round(tot_k, 3)}}


def flat_lvs(report: Path) -> dict:
    """The flat extraction's LVS. Flattening makes every inner label a port, so a block net (e.g.
    '<block>_0.net1') can appear as a layout port where the layout view has an internal net. Accepted only when Netgen
    matches the netlists uniquely and every row of its pin tables either pairs one name with itself or is such an
    inner net (same name after the block prefix). Netgen cuts each column at 43 characters, so a cut name is compared
    as a prefix (review of plan v4 Phase 7: a cut row was skipped before)."""
    txt = report.read_text() if report.exists() else ""
    unique = "match uniquely" in txt and "property errors" not in txt.lower()
    odd, other, inner = [], [], 0

    def same(a, b, cut):
        return a == b or (cut and (a.startswith(b) or b.startswith(a)))
    for block in re.split(r"^Subcircuit pins:\s*$", txt, flags=re.M)[1:]:
        for ln in block.splitlines()[1:]:
            if ln.startswith(("-", "Circuit ")) or "|" not in ln:
                if ln.strip() and not ln.startswith(("-", "Circuit ")):
                    break                                   # past the table
                continue
            left, right = (x.strip() for x in ln.split("|", 1))
            cut = len(ln.split("|", 1)[0]) >= 43 and not ln.split("|", 1)[0].endswith(" ")
            if left.startswith("(no pin"):
                other.append(ln.strip())                    # a reference port the layout lacks
                continue
            base = re.split(r"[./]", left)[-1]
            if right.startswith("(no pin, node is "):
                name = right[len("(no pin, node is "):]
                cut_r = not name.endswith(")")
                inner += 1
                if not same(base, name.rstrip(")"), cut or cut_r):
                    odd.append([left, name])
            elif not same(left, right, cut or len(right) >= 42):
                odd.append([left, right])                   # two different pins paired
    return {"match": bool(unique and not odd and not other), "inner_nets_as_ports": inner,
            "other_pin_errors": odd + other, "report": rel(report)}


def against_budgets(caps: dict, budgets: dict, s5_rules: dict, s3_dec: dict, ir: dict, ext_net: dict | None = None) -> dict:
    """Every budgeted element against its S2 budget. A net's capacitance to ground is the larger of the C-only
    netlist's and the .ext's (ext_net, G6.4's reading): the netlist leaves out the gate nets' (row 75), the .ext
    reading charges a node's capacitance over an n-well to the substrate; so the value never understates (review of
    plan v4 Phase 7)."""
    ext_net = ext_net or {}
    rows, devs = [], {d["name"]: d for d in ir["devices"]}
    types = {d: t for t, v in s3_dec.items() for d in v["devices"]}
    for e in budgets["elements"]:
        if e.get("budget") is None:
            continue
        if e["kind"] == "net_capacitance":
            nl, ex = caps["net"].get(e["id"], 0.0), ext_net.get(e["id"], 0.0)
            val, src = max(nl, ex), ("extracted (C-only netlist)" if nl >= ex else
                                     f"extracted (.ext; the C-only netlist has {round(nl, 4)} fF)")
        elif e["kind"] == "coupling":
            val, src = caps["coupling"].get("~".join(sorted(e["id"].split("~"))), 0.0), "extracted"
        elif e["kind"] == "terminal_resistance":
            dn, term = e["id"].split("+")[0], e["id"].rsplit(".", 1)[1]
            dn = dn.split(".")[0]
            acc = s3_dec[types[dn]]["access_resistance_ohm"][term]
            route = ((s5_rules.get("max_series_R") or {}).get(e["id"]) or {}).get("route_ohm", 0.0)
            val, src = acc + route, "S3 access R + S5 top-level wires and vias"
        else:
            continue
        rows.append({"id": e["id"], "kind": e["kind"], "units": e.get("units"), "value": round(val, 4),
                     "budget": round(e["budget"], 4), "use": round(val / e["budget"], 4) if e["budget"] else None,
                     "ok": val <= e["budget"] * (1 + 1e-9), "source": src})
    budgeted = {r["id"] for r in rows if r["kind"] == "coupling"}
    extra = {k: v for k, v in caps["coupling"].items()
             if k not in {"~".join(sorted(b.split("~"))) for b in budgeted}}
    return {"rows": rows, "violations": [r["id"] for r in rows if not r["ok"]], "unbudgeted_couplings_fF": extra}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package")
    ap.add_argument("--rc-tol", type=float, default=100.0)
    a = ap.parse_args(argv)
    pkg = load_package(REPO / a.package)
    design = pkg["design"]
    s0, s2, s3, s5 = (REPO / "outputs" / s / design for s in ("S0", "S2", "S3", "S5"))
    out = REPO / "outputs" / "S6" / design
    ir = json.loads((s0 / "circuit_ir.json").read_text())
    ref_spice = (s0 / "ref" / f"{design}_layout.spice").read_text()
    nmap = R.net_map(ir, ref_spice)
    inv = {v: k for k, v in nmap.items() if v != k}
    nets = {n["name"] for n in ir["nets"]} | {p["name"] for p in ir["ports"]}
    gnd = ac_grounds(ir)
    budgets = json.loads((s2 / "budgets.json").read_text())
    s3_dec = json.loads((s3 / "device_decisions.json").read_text())["decisions"]
    s5_rep = json.loads((s5 / "s5_report.json").read_text())
    fresh_output_dir(out)
    out.mkdir(parents=True, exist_ok=True)
    cell = f"{design}_routed"
    res = {}
    same = (s5_rep["gates"].get("G5.5_area_vs_area_only (info)") or {}).get("same_placement")
    for r in RULES:
        gds = s5 / f"routed_{r}" / f"{cell}.gds"
        d = out / r
        d.mkdir(parents=True, exist_ok=True)
        if r == "area_only" and same:
            # both rules chose one placement (LOADBench), routed by one router: extracted once, so the two layouts
            # are not told apart by extresist's run-to-run variation, and S7 simulates their decks once
            (d / "SAME_LAYOUT.txt").write_text("S5 chose the same placement for both rules; see ../budget_aware/\n")
            res[r] = {**res["budget_aware"], "same_as": "budget_aware"}
            continue
        ex = RL.extract(gds.resolve(), cell, d)
        rc = RL.extract_rc(gds.resolve(), cell, d, a.rc_tol)
        RL.lvs(ex["lvs"], cell, s5 / f"routed_{r}" / "ref_top.spice", design, d)
        lv = flat_lvs(d / "lvs_report.txt")
        caps = capacitances(ex["pex"], nets, inv, gnd)
        ce = ext_capacitances(d / f"{cell}_flat.ext", nets, inv, gnd)
        tot_nl = netlist_total(ex["pex"])
        ext_check = {"netlist_total_fF": tot_nl, "ext_total_fF": ce["total_fF"],
                     "netlist_short_of_ext": round(1 - tot_nl / ce["total_fF"], 4) if ce["total_fF"] else None,
                     "complete": tot_nl >= ce["total_fF"] * (1 - EXT_TOL), "tolerance": EXT_TOL,
                     "substrate_net": ce["substrate_net"], "ext_net_fF_approx": ce["net"],
                     "nets_without_ground_C_in_netlist": sorted(n for n, v in ce["net"].items()
                                                                if v > 1.0 and caps["net"].get(n, 0.0) == 0.0),
                     "nets_short_in_netlist": {n: [caps["net"].get(n, 0.0), v] for n, v in ce["net"].items()
                                               if v - caps["net"].get(n, 0.0) > max(1.0, 0.05 * v)}}
        cmp_ = against_budgets(caps, budgets, s5_rep["gates"]["G5.4_route_rules"]["detail"][r] or {}, s3_dec, ir,
                               ce["net"])
        n_r = len(re.findall(r"^R", rc.read_text(), re.M)) if rc.exists() else None
        kx = kpex_cross_check(gds.resolve(), cell, s5 / f"routed_{r}" / "ref_top.spice", design, d / "kpex", caps,
                              nets, inv, gnd)
        res[r] = {"netlists": {"lvs": rel(ex["lvs"]), "pex_c": rel(ex["pex"]), "pex_rc": rel(rc) if rc.exists() else None},
                  "lvs": lv, "n_caps": caps["n_caps"], "n_resistors_rc": n_r, "unassigned_caps": caps["unassigned"],
                  "net_fF": caps["net"], "coupling_fF": caps["coupling"], "c_only_vs_ext": ext_check,
                  "budgets": cmp_, "kpex": kx}
    ident = {"run_id": new_run_id(), "design": design, "s5_run_id": s5_rep.get("run_id"),
             "ac_grounds": sorted(gnd)}
    mims = mim_self(REPO / "outputs" / "S4" / design, out)
    for x in res.values():
        corr = []
        for row in x["budgets"]["rows"]:
            for m in mims.values():
                if row["kind"] == "coupling" and set(row["id"].split("~")) == {m["top"], m["bottom"]}:
                    val = row["value"] - m["plate_coupling_fF"]
                    corr.append({"id": row["id"], "value": round(val, 4), "budget": row["budget"],
                                 "use": round(val / row["budget"], 4), "ok": val <= row["budget"]})
        x["mim_corrected_rows"] = corr
    write_json(out / "parasitics_vs_budgets.json", {**ident, "mim_self": mims, "layouts": res})
    ba = res["budget_aware"]
    gates = {
        "G6.1_extracted_and_LVS": {"pass": all(x["lvs"]["match"] and x["netlists"]["pex_rc"] and not x["unassigned_caps"]
                                               for x in res.values()),
                                   "detail": {r: {"lvs": x["lvs"]["match"], "caps": x["n_caps"], "rc_resistors": x["n_resistors_rc"],
                                                  "unassigned_caps": len(x["unassigned_caps"])} for r, x in res.items()}},
        "G6.2_parasitics_within_budgets": {
            "pass": not ba["budgets"]["violations"], "violations": ba["budgets"]["violations"],
            "worst": sorted(((x["use"], x["id"]) for x in ba["budgets"]["rows"]), reverse=True)[:5],
            "area_only_violations (H5)": res["area_only"]["budgets"]["violations"],
            "note": "the budget-aware layout is gated; the area-only baseline is reported for H5"},
        "G6.4_c_only_netlist_complete (info)": {
            "pass": None, "detail": {r: x["c_only_vs_ext"] for r, x in res.items()},
            "note": "Magic's C-only netlist against its own .ext (totals): ext2spice leaves out the capacitance to ground "
                    "of nets that are transistor gates (flow record row 71); G6.2 reads the netlist, so a net listed "
                    "under nets_without_ground_C_in_netlist reads low there. S7's R+C netlist carries it"},
        "G6.5_mim_self_coupling (info)": {
            "pass": None, "capacitors": mims, "budget_aware_rows_less_it": ba.get("mim_corrected_rows", []),
            "note": "a MIM capacitor block extracted alone: the plate-to-plate coupling Magic adds on top of the "
                    "device (metal4 over metal3 across the top plate) is very likely counted twice; S7's G7.5 "
                    "simulates the layout with it cancelled. G6.2 keeps Magic's number"},
        "G6.3_kpex_cross_check (info)": {"pass": None, "detail": {r: x["kpex"] for r, x in res.items()},
                                         "note": "kpex 2.5D against Magic on the nets both name; kpex leaves a net it "
                                                 "cannot match in its own LVS unnamed"},
    }
    prov = provenance([s5 / "s5_report.json", s2 / "budgets.json", s0 / "circuit_ir.json", REPO / a.package])
    report = {**ident, "gates": gates, "all_pass": all(g.get("pass") in (True, None) for g in gates.values()),
              "provenance": prov}
    write_json(out / "s6_report.json", report)
    for r, x in res.items():
        print(f"== {r}: lvs={x['lvs']['match']} caps={x['n_caps']} rc_R={x['n_resistors_rc']} unassigned={len(x['unassigned_caps'])}")
        for row in x["budgets"]["rows"]:
            print(f"   {row['id']:16s} {row['kind']:20s} {row['value']:10.3f} / {row['budget']:10.3f} {row['units'] or '':4s} "
                  f"use={row['use']} {'ok' if row['ok'] else 'OVER'}")
        print("   unbudgeted couplings:", x["budgets"]["unbudgeted_couplings_fF"])
    for k, g in gates.items():
        print(f"{k:34s} {g.get('pass')}")
    return gate_exit(report["all_pass"])


if __name__ == "__main__":
    sys.exit(main())
