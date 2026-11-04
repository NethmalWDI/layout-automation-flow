"""S7 — post-layout evaluation in the flow's own benches (plan v4, Phase 5).

For each routed layout of S5 (budget-aware, and the area-only baseline for H5), S6's netlists replace the DUT in S0's
AC, OP and NOISE benches (the wrapper of scripts/reference_layout.py):
  * drawn devices only (the LVS netlist: the devices with their drawn diffusion, no wiring),
  * C-only PEX (every capacitance), and
  * R+C PEX (extresist: wire and via resistance as well); the post-layout result is this one;
and the schematic runs in the same bench (with the same 1 Tohm shunts) as the reference.
An internal source the layout view removed (e.g. V1 on VBIAS) is put back in the wrapper from the IR.

Checks (PREREG amendment of 2026-11-03):
  G7.1 every spec met post-layout (nominal);
  G7.2 the margin each spec loses, schematic -> post-layout, at most eta x margin x (1 + TOL_USE);
  G7.3 (info) G2.0's prediction against that loss as a fraction of the margin (PREREG: within 25 %);
  G7.4 (info) PVT points: not run here.
The budget-aware layout is gated; the area-only one is reported for H5. Device saturation (S2's sat_* checks) is not
evaluated here: the flat extraction renames the devices, so S3's per-finger probes do not apply.

usage (inside layout-s0s3): python3 -m src.s7.run inputs/<d>/package.yaml   (or ./flow run <d> --stage S7)
Writes outputs/S7/<d>/: sim/<rule>/<view>/<kind>/, metrics.json, s7_report.json.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.common.hygiene import fresh_output_dir, gate_exit, new_run_id
from src.common.tolerance import TOL_USE
from src.common.tools import REPO, bench, provenance, run_ngspice_text, write_json
from src.s0.ingest import load_package
from src.s5 import route as R
from src.s6.run import node_net

RULES = ("budget_aware", "area_only")
KINDS = ("AC", "OP", "NOISE")
VIEWS = ("drawn", "pex_c", "pex_rc")
BIG_DECK = 20_000_000   # characters: a deck this large runs with --big-workers (default 1) after the others


def shunted(txt: str) -> str:
    """1 Tohm shunts: extracted metal touching only capacitors has no DC path (as in scripts/reference_layout.py;
    the schematic gets them too, so the runs differ only in the DUT)."""
    return re.sub(r"^(\.lib .*)$", r"\1\n.option rshunt=1e12", txt, count=1, flags=re.M)


def bench_ports(bench_txt: str) -> tuple[list, dict]:
    """The bench wrapper's ports, and {DUT port: wrapper node} from its 'XDUT <nodes> <cell>' line and that cell's
    .subckt line (the 5T: VDD -> VDD, ...; LOADBench: in1 -> INN, in2 -> INP, out -> OUTP, sourceNmos -> VSS,
    sourcePmos -> VDD)."""
    m = re.search(r"^\.subckt dut_amp\s+(.*?)$\s*^XDUT\s+(.*?)$", bench_txt, re.M)
    wrapper, xdut = m.group(1).split(), m.group(2).split()
    sub = re.search(rf"^\.subckt\s+{re.escape(xdut[-1])}\s+(.*?)$", bench_txt, re.M)
    if not sub:                         # the DUT cell is not in the bench: its ports are taken by name
        return wrapper, {w: w for w in wrapper}
    return wrapper, dict(zip(sub.group(1).split(), xdut[:-1]))


def wrapped(bench_txt: str, netlist: str, cell: str, ir: dict, nmap: dict, nets: set, inv: dict) -> str:
    """The bench with its DUT replaced by the extracted cell. Ports map to the wrapper's nodes as the bench's own DUT
    line maps the schematic's (a layout-view name through its IR name); an inner net exposed by flattening goes to
    its own node; a removed internal source (V or I) is put back on its port."""
    joined = re.sub(r"\n\+", " ", netlist)
    ports = re.search(rf"^\.subckt\s+{re.escape(cell)}_flat\s+(.*?)$", joined, re.M).group(1).split()
    wrapper, pmap = bench_ports(bench_txt)
    # Only the first port of each name (the top cell's label) is a circuit node. Every other port, a repeated name
    # (VDD twice: the top label and a block track's) or a unit's own D/G/S/B in the R+C netlist, is a point inside
    # the resistor network: it gets its own node, never the bench's, which would short the wiring between them.
    # The bench's own wrapper may hold more than the DUT: iadc_ota's ideal CMFB (Bcmfb) drives the DUT's cmc through
    # the wrapper node cmc_w. Those elements are kept, and a port goes to its wrapper node also when that node is
    # inside the wrapper (flow record row 100: they were dropped, so iadc's layout views ran with the CMFB open; the
    # other designs' wrappers hold only the DUT line, so nothing changes for them).
    body = re.search(r"^\.subckt dut_amp\s.*?$(.*?)^\.ends", bench_txt, re.S | re.M)
    extra = [ln for ln in (body.group(1).splitlines() if body else []) if ln.strip() and not ln.startswith("XDUT")]
    known = set(wrapper) | set(pmap.values())
    first, nodes = {}, []
    for i, p in enumerate(ports):
        base = re.split(r"[./]", p)[-1]
        if base not in first:
            node = pmap.get(base) or pmap.get(inv.get(base, base))
            first[base] = node if node in known else f"N_{re.sub(r'[^A-Za-z0-9_]', '_', base)}"
            nodes.append(first[base])
        else:
            nodes.append(f"N{i}_{re.sub(r'[^A-Za-z0-9_]', '_', base)}")
    lines = [f"XDUT {' '.join(nodes)} {cell}_flat"] + extra
    for s in ir.get("internal_sources", []):
        if "removed in layout view" in (s.get("layout_handling") or ""):
            p, n = nmap.get(s["p"], s["p"]), nmap.get(s["n"], s["n"])
            kind = s.get("kind", "V")
            lines.append(f"{kind}{s['name']}_layout {first.get(p, p)} {first.get(n, n)} {s['dc']}")
    for x in ir.get("passives", []):   # an off-chip element S0 removed from the layout view (ttsky25a_fd's 12 kohm
        if "removed in the layout view" in ((x.get("layout_binding") or {}).get("status") or ""):   # Rgm_ext; Phase 8)
            a, b = nmap.get(x["a"], x["a"]), nmap.get(x["b"], x["b"])
            lines.append(f"{x['kind']}{x['name']}_layout {first.get(a, a)} {first.get(b, b)} {x['value']}")
    sub = ".subckt dut_amp " + " ".join(wrapper) + "\n" + "\n".join(lines) + "\n.ends"
    txt = re.sub(r"^\.subckt dut_amp .*?^\.ends\s*$", lambda _: sub, shunted(bench_txt), count=1, flags=re.S | re.M)
    body = netlist.replace(".end\n", "")
    return txt.replace("\n.end\n", "\n" + body + "\n.end\n") if "\n.end\n" in txt else txt + body


def mim_cancelled(netlist: str, mims: dict) -> str | None:
    """The post-layout netlist with each MIM capacitor's plate-to-plate coupling, as S6 extracted it from the capacitor
    block alone (G6.5), cancelled by negative capacitors across the device's own terminals; None if not possible.
    A capacitor drawn as several units (ttsky25a_fd: 5 per Miller capacitor) gives several device lines: each line
    goes to the capacitor whose top and bottom nets its terminals name (after a flattened block prefix such as
    'XC1__A_0.'), and the coupling is split evenly over that capacitor's lines. With one MIM capacitor, every MIM line
    is its own (an R+C netlist names sub-nodes). A line no capacitor claims: None (plan v4 Phase 8)."""
    lines = netlist.splitlines()
    models = {m["model"] for m in mims.values()}
    base = lambda n: n.rsplit(".", 1)[-1]                   # noqa: E731
    owner = {}
    for i, ln in enumerate(lines):
        t = ln.split()
        if len(t) > 3 and t[0][:1] in "Xx" and t[3] in models:
            hit = [c for c, m in mims.items() if t[3] == m["model"] and len(mims) == 1 or
                   {base(t[1]), base(t[2])} == {m.get("top"), m.get("bottom")}]
            if len(hit) != 1:
                return None
            owner[i] = hit[0]
    count = {c: list(owner.values()).count(c) for c in mims}
    out, n = [], 0
    for i, ln in enumerate(lines):
        out.append(ln)
        c = owner.get(i)
        if c is not None and mims[c]["plate_coupling_fF"] > 0:
            t = ln.split()
            v = mims[c]["plate_coupling_fF"] if count[c] == 1 else round(mims[c]["plate_coupling_fF"] / count[c], 6)
            out.append(f"Cmimself{n} {t[1]} {t[2]} -{v}f")
            n += 1
    return "\n".join(out) + "\n" if n else None


def run_view(job):
    txt, work, kind = job
    r = run_ngspice_text(txt, work, kind.lower(), cache=False, timeout=1800)
    return {"meas": r["meas"], "rc": r["rc"], "warnings": r.get("numerical_warnings", [])}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--big-workers", type=int, default=1)
    a = ap.parse_args(argv)
    pkg = load_package(REPO / a.package)
    design = pkg["design"]
    s0, s2, s6 = (REPO / "outputs" / s / design for s in ("S0", "S2", "S6"))
    out = REPO / "outputs" / "S7" / design
    ir = json.loads((s0 / "circuit_ir.json").read_text())
    ref_spice = (s0 / "ref" / f"{design}_layout.spice").read_text()
    nmap = R.net_map(ir, ref_spice)
    inv = {v: k for k, v in nmap.items() if v != k}
    nets = {n["name"] for n in ir["nets"]} | {p["name"] for p in ir["ports"]}
    s6p = json.loads((s6 / "parasitics_vs_budgets.json").read_text())
    s2r = json.loads((s2 / "s2_report.json").read_text())
    eta = s2r["eta"]
    g20 = (s2r["gates"].get("G2.0_expected_layout_use (info)") or {}).get("checks", {})
    tb = s0 / "tb"
    cell = f"{design}_routed"
    fresh_output_dir(out)
    jobs, keys = [], []
    for kind in KINDS:
        jobs.append((shunted(bench(tb, kind).read_text()), out / "sim" / "schematic" / kind, kind))
        keys.append(("schematic", None, kind))
    for r in RULES:
        nl = s6p["layouts"][r]["netlists"]
        for view, key in (("drawn", "lvs"), ("pex_c", "pex_c"), ("pex_rc", "pex_rc")):
            if not nl.get(key):
                continue
            net = (REPO / nl[key]).read_text()
            for kind in KINDS:
                jobs.append((wrapped(bench(tb, kind).read_text(), net, cell, ir, nmap, nets, inv),
                             out / "sim" / r / view / kind, kind))
                keys.append((r, view, kind))
    # the post-layout view: R+C, or C-only where S6 did no R+C extraction (layout.yaml rc_extraction: false; plan v4
    # Phase 8, ttsky25a_fd). The key post_layout_rc keeps its name; post_layout_view says which view it is
    # Only the design's own option chooses C-only (review of plan v4 Phase 8): a missing R+C netlist otherwise stays
    # missing, and G7.1 fails on it
    from src.s4.run import layout_options
    post_view = "pex_rc" if layout_options(design).get("rc_extraction", True) else "pex_c"
    mim_view = f"{post_view}_mim_cancelled"
    mims = s6p.get("mim_self") or {}
    if mims:   # G7.5 (info): the post-layout AC with the capacitor's own plate coupling cancelled (S6's G6.5)
        for r in RULES:
            nl = s6p["layouts"][r]["netlists"].get(post_view)
            fixed = mim_cancelled((REPO / nl).read_text(), mims) if nl else None
            if fixed:
                jobs.append((wrapped(bench(tb, "AC").read_text(), fixed, cell, ir, nmap, nets, inv),
                             out / "sim" / r / mim_view / "AC", "AC"))
                keys.append((r, mim_view, "AC"))
    # a large deck (LOADBench's R+C netlist: 315 000 resistors, 79 MB) runs on its own: four at once ran the container
    # (5 GB) out of memory and the kernel killed the AC runs (flow record row 76)
    # an identical deck (both rules chose the same placement, as on LOADBench) is simulated once; its other folders get
    # a note naming the folder that holds the run
    first_of = {}
    for i, j in enumerate(jobs):
        first_of.setdefault(j[0], i)
    dup = {i: first_of[j[0]] for i, j in enumerate(jobs) if first_of[j[0]] != i}
    big = [i for i, j in enumerate(jobs) if len(j[0]) > BIG_DECK and i not in dup]
    small = [i for i in range(len(jobs)) if i not in big and i not in dup]
    runs = [None] * len(jobs)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        for i, r in zip(small, ex.map(run_view, [jobs[i] for i in small])):
            runs[i] = r
    with ThreadPoolExecutor(max_workers=a.big_workers) as ex:
        for i, r in zip(big, ex.map(run_view, [jobs[i] for i in big])):
            runs[i] = r
    for i, k in dup.items():
        runs[i] = runs[k]
        jobs[i][1].mkdir(parents=True, exist_ok=True)
        (jobs[i][1] / "SAME_DECK.txt").write_text(f"identical deck; simulated once in {jobs[k][1].relative_to(REPO)}\n")
    meas, failed = {}, []
    for (r, view, kind), res in zip(keys, runs):
        meas.setdefault(r, {}).setdefault(view or "schematic", {}).update(res["meas"] or {})
        if res["rc"] != 0 or res["warnings"]:
            failed.append({"layout": r, "view": view, "kind": kind, "rc": res["rc"], "warnings": res["warnings"][:3]})
    sch = meas["schematic"]["schematic"]
    margins = ir["margins"]
    metrics = {}
    missing = {}
    for r in RULES:
        post = meas.get(r, {}).get(post_view) or {}
        rows = {}
        for k, mg in margins.items():
            if post.get(k) is None or sch.get(k) is None:
                missing.setdefault(r, []).append(k)        # a spec with no measurement fails G7.1, never passes
                continue
            lost = (sch[k] - post[k]) if mg["kind"] == "min" else (post[k] - sch[k])
            allowed = eta * mg["margin"]
            pred = (g20.get(k) or {}).get("fraction_of_margin")
            frac = lost / mg["margin"] if mg["margin"] else None
            rows[k] = {"schematic": sch[k], "drawn": meas[r].get("drawn", {}).get(k), "pex_c": meas[r].get("pex_c", {}).get(k),
                       "post_layout_rc": post[k], "limit": mg["limit"], "kind": mg["kind"], "margin": mg["margin"],
                       "meets_spec": post[k] >= mg["limit"] if mg["kind"] == "min" else post[k] <= mg["limit"],
                       "lost": round(lost, 6), "use_of_allowed": round(lost / allowed, 4) if allowed else None,
                       "within_allowed": lost <= allowed * (1 + TOL_USE),
                       "lost_frac_of_margin": None if frac is None else round(frac, 5),
                       "G2.0_predicted_frac": pred,
                       "G2.0_rel_error": None if (pred in (None, 0) or frac is None) else round((frac - pred) / pred, 4)}
        metrics[r] = rows
    metrics_mim = {}
    for r in RULES:
        cm = meas.get(r, {}).get(mim_view) or {}
        rows = {}
        for k in ("gain_db", "gbw_mhz", "pm_deg"):
            mg = margins.get(k)
            if mg is None or cm.get(k) is None or sch.get(k) is None:
                continue
            lost = (sch[k] - cm[k]) if mg["kind"] == "min" else (cm[k] - sch[k])
            allowed = eta * mg["margin"]
            rows[k] = {"value": cm[k], "lost": round(lost, 6), "use_of_allowed": round(lost / allowed, 4) if allowed else None,
                       "within_allowed": lost <= allowed * (1 + TOL_USE)}
        if rows:
            metrics_mim[r] = rows
    ident = {"run_id": new_run_id(), "design": design, "s6_run_id": s6p.get("run_id"), "eta": eta, "TOL_USE": TOL_USE,
             "post_layout_view": post_view}
    write_json(out / "metrics.json", {**ident, "views": meas, "metrics": metrics, "failed_runs": failed,
                                      "not_evaluated": "device saturation (S2's sat_* checks); PVT points"})
    ba = metrics["budget_aware"]
    s6r = json.loads((s6 / "s6_report.json").read_text())
    g62 = s6r["gates"]["G6.2_parasitics_within_budgets"]["pass"]
    gates = {
        "G7.1_specs_met_post_layout": {"pass": bool(ba) and all(x["meets_spec"] for x in ba.values()) and
                                       not missing.get("budget_aware") and
                                       not [f for f in failed if f["view"] != mim_view],
                                       "missing_measurements": missing,
                                       "detail": {k: [x["post_layout_rc"], x["limit"], x["meets_spec"]] for k, x in ba.items()},
                                       "failed_runs": failed},
        "G7.2_loss_within_eta_margin": {"pass": bool(ba) and not missing.get("budget_aware") and
                                        all(x["within_allowed"] for x in ba.values()),
                                        "detail": {k: x["use_of_allowed"] for k, x in ba.items()}},
        "G7.3_G2.0_prediction (info)": {"pass": None, "detail": {k: [x["lost_frac_of_margin"], x["G2.0_predicted_frac"],
                                                                    x["G2.0_rel_error"]] for k, x in ba.items()},
                                        "note": "[post-layout loss / margin, G2.0's predicted share, relative error]; PREREG: within 25 %"},
        "G7.4_pvt (info)": {"pass": None, "note": "PVT points are not simulated post-layout here"},
        "G7.5_mim_self_coupling_cancelled (info)": {
            "pass": None, "capacitors": mims, "detail": metrics_mim,
            "budget_aware_within_eta": (all(x["within_allowed"] for x in metrics_mim["budget_aware"].values())
                                        if metrics_mim.get("budget_aware") else None),
            "view": mim_view,
            "note": "the post-layout AC run (R+C, or C-only without R+C extraction) with each MIM capacitor's own "
                    "plate-to-plate coupling cancelled (S6 G6.5: very likely counted twice by Magic's sky130 rules); "
                    "G7.1 and G7.2 keep Magic's netlist"},
        "H4 (info)": {"pass": None, "G6.2": g62,
                      "G7.1_and_G7.2": bool(ba) and all(x["meets_spec"] and x["within_allowed"] for x in ba.values()),
                      "note": "H4 holds if G6.2 passing implies G7.1 and G7.2 passing"},
        "H5 (info)": {"pass": None,
                      "use_of_allowed": {r: {k: x["use_of_allowed"] for k, x in metrics[r].items()} for r in RULES}},
    }
    prov = provenance([s6 / "parasitics_vs_budgets.json", s0 / "circuit_ir.json", s2 / "s2_report.json", REPO / a.package])
    report = {**ident, "gates": gates, "all_pass": all(g.get("pass") in (True, None) for g in gates.values()),
              "provenance": prov}
    write_json(out / "s7_report.json", report)
    for r in RULES:
        print(f"== {r}")
        for k, x in metrics[r].items():
            print(f"   {k:16s} sch={x['schematic']:.5g} drawn={x['drawn']} pexC={x['pex_c']} pexRC={x['post_layout_rc']:.5g} "
                  f"lim={x['limit']} meets={x['meets_spec']} use={x['use_of_allowed']} G2.0={x['G2.0_predicted_frac']} "
                  f"actual={x['lost_frac_of_margin']}")
    print("failed runs:", failed)
    for k, g in gates.items():
        print(f"{k:34s} {g.get('pass')}")
    return gate_exit(report["all_pass"])


if __name__ == "__main__":
    sys.exit(main())
