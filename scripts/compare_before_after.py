#!/usr/bin/env python3
"""Before/after record of the flow on every design (plan v2, item 4).

  snap <design> <tag>     keep the key results of the current outputs/S0..S3/<design> in
                          outputs/compare/<design>/<tag>.json (gates, specs, budgets, decisions)
  report                  docs/before_after.md: one table per design, every tag side by side

Run inside the EDA image from the repository root.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "outputs" / "compare"


def _j(p: Path):
    return json.loads(p.read_text()) if p.exists() else None


def g20_by_part(b: dict) -> dict:
    """G2.0's expected use of each spec margin, split by where the expected need comes from: capacitance of the
    routes (cap_wiring), capacitance inside the device cells (cap_cells), route resistance (r_wiring) and the
    cells' access resistance (r_access). The rates are recovered from budgets.json (margin_used / budget; S2
    keeps only harmful, i.e. positive, rates); 'residual' is G2.0's recorded total minus the sum of the parts."""
    out: dict = {}
    for e in b.get("elements", []):
        bud = e.get("budget")
        if not bud:
            continue
        wp = e.get("w_parts") or {}
        cap = e.get("kind") != "terminal_resistance"
        for c, used in (e.get("margin_used") or {}).items():
            if c.startswith("sat_") or "@" in c:
                continue
            o = out.setdefault(c, {"cap_wiring": 0.0, "cap_cells": 0.0, "r_wiring": 0.0, "r_access": 0.0})
            rate = used / bud
            o["cap_wiring" if cap else "r_wiring"] += rate * float(wp.get("wiring", 0) or 0)
            o["cap_cells" if cap else "r_access"] += rate * float(wp.get("device_cells", 0) or 0)
    for c, o in out.items():
        tot = sum(o.values())
        elu = (b.get("expected_layout_use") or {}).get(c) or {}
        o.update({"total": tot, "margin": elu.get("margin"),
                  "residual": None if elu.get("use_at_expected_need") is None else elu["use_at_expected_need"] - tot})
    return out


def budget_over_need(b: dict, bl: dict | None) -> dict | None:
    """How much room each budget rule leaves the layout: budget / expected need over the budgeted elements
    (geometric mean, median, minimum). A rule can be safe and feasible yet leave no room (every budget = need)."""
    if not bl:
        return None
    import math
    need = {e["id"]: float(e["w"]) for e in b.get("elements", []) if float(e.get("w") or 0) > 0}
    out = {}
    for m, v in (bl.get("methods") or {}).items():
        x = v.get("budgets") or {}
        r = sorted(x[i] / need[i] for i in x if i in need and x[i] is not None)
        if r:
            out[m] = {"geomean": math.exp(sum(math.log(max(t, 1e-12)) for t in r) / len(r)),
                      "median": r[len(r) // 2], "min": r[0], "n": len(r)}
    return out


def snap(design: str, tag: str) -> Path:
    rec: dict = {"design": design, "tag": tag}
    # a report older than the start of a stage that ended in ERROR in the last flow run is stale: that run
    # crashed there (or stopped before this stage), so the file is from an earlier run (review B, item 10)
    summ = _j(REPO / "outputs" / "flow" / design / "flow_summary.json") or {"stages": {}}
    order_ = ("S0", "S1", "S2", "S3")
    errs = [(order_.index(k), dt.datetime.fromisoformat(v["started"]).timestamp()) for k, v in summ["stages"].items()
            if k in order_ and v.get("status") == "ERROR" and v.get("started")]
    err_idx, err_start = min(errs) if errs else (None, None)
    for i_st, st in enumerate(order_):
        f_ = REPO / "outputs" / st / design / f"{st.lower()}_report.json"
        rep = _j(f_)
        if rep is None:
            rec[st] = None
            continue
        if err_start is not None and i_st >= err_idx and f_.stat().st_mtime < err_start:
            rec[st] = {"stale": True, "gates": {}, "failed": ["stale report (the last flow run ended in ERROR before it)"]}
            continue
        g = {k: (v.get("pass") if isinstance(v, dict) else v) for k, v in rep["gates"].items()}
        rec[st] = {"gates": g, "failed": sorted(k for k, v in g.items() if v is False)}
    s1 = REPO / "outputs" / "S1" / design
    lm = _j(s1 / "linear_model.json")
    fresh = lambda st: rec.get(st) and not rec[st].get("stale")  # noqa: E731
    if lm and fresh("S1"):        # S1 may have crashed after writing its linear model
        rec["S1"]["linear_vs_spice"] = lm["delta"]
    sy = _j(s1 / "symbolic_check.json")
    if sy and fresh("S1"):
        rec["S1"]["symbolic_vs_spice"] = sy.get("delta")
    s2 = REPO / "outputs" / "S2" / design
    b = _j(s2 / "budgets.json")
    rep2 = _j(s2 / "s2_report.json")
    if b and rep2 and fresh("S2"):
        g = rep2["gates"]
        el = [e for e in b["elements"] if e.get("budget") is not None]
        rec["S2"].update({
            "eta": b.get("eta"), "alloc": b.get("alloc", "v1"),
            "expected_use_fraction": {k: v["fraction_of_margin"] for k, v in (g.get("G2.0_expected_layout_use (info)") or {}).get("checks", {}).items()
                                      if not k.startswith("sat_") and "@" not in k},
            "t_round1": (g.get("G2.3_allocation") or {}).get("t_round1"),
            "n_budgeted": len(el),
            "starved": sum(1 for e in el if e["budget"] < e["w"] * (1 - 1e-9)),
            "min_ratio_to_need": min((e["budget"] / e["w"] for e in el), default=None),
            "verify": {r["check"]: r.get("spice_use_frac_of_margin") for r in (g.get("G2.5_spice_budget_verification") or {}).get("rows", [])},
            "floors": g.get("G2.7_library_floors_feasible"),
            "baselines": (g.get("G2.8_baselines (info)") or {}).get("scores"),
            "pvt": {k: v for k, v in (g.get("G2.9_pvt_constraints (info)") or {}).items() if k != "skipped_spec_not_met_before_layout"},
            "g20_by_part": g20_by_part(b),
            "baseline_budget_over_need": budget_over_need(b, _j(s2 / "baselines.json")),
        })
    s3 = REPO / "outputs" / "S3" / design
    d = _j(s3 / "device_decisions.json")
    if d and fresh("S3"):
        dec = d["decisions"]
        rec["S3"].update({
            "mode": d.get("mode", "A-free"), "rules": d.get("rules", "v1"),
            "types": {t: {"option": x["chosen"]["id"], "area_um2": x["area_um2"], "relaxed": x["relaxed"],
                          "devices": len(x["devices"])} for t, x in dec.items()},
            "total_device_area_um2": sum(x["area_um2"] * len(x["devices"]) for x in dec.values()),
            "relaxed": sorted(t for t, x in dec.items() if x["relaxed"]),
            "final": {k: v for k, v in d["final_in_circuit"].items() if isinstance(v, (int, float))},
            "by_mode": {m: {"total_area_um2": v["total_area_um2"], "relaxed": v["relaxed"],
                            "fingers_outside_sized_bin": v["fingers_outside_sized_bin"]}
                        for m, v in (d.get("by_mode") or {}).items()},
        })
    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / design / f"{tag}.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(rec, indent=1) + "\n")
    return f


def _fmt(v):
    if v is None:
        return "–"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, float):
        return f"{v:.3g}"
    if isinstance(v, (list, tuple)):
        return ", ".join(map(str, v)) if v else "none"
    return str(v)


def hand_layout_rows(design: str, recs: dict) -> list:
    """G2.0's prediction (before any layout) against what a hand-drawn layout's wiring actually costs:
    drawn devices -> PEX in scripts/reference_layout.py, capacitance only, and R+C when an extresist run exists.
    Only the bench's own conditions are compared (the S0 margins are defined there)."""
    rd = REPO / "outputs" / "reference_layout" / design
    nom = _j(rd / "reference_layout.json")
    g = {t: (recs[t].get("S2") or {}).get("g20_by_part") for t in ("before", "after") if t in recs}  # G2.0 does not depend on eta
    g = {t: v for t, v in g.items() if v}
    if not nom or not g:
        return []
    rcs = [(f, _j(f)) for f in sorted(rd.glob("reference_layout*.json"), key=lambda f: f.stat().st_mtime)]
    rcs = [(f, r) for f, r in rcs if r and r.get("post_layout_rc") and r.get("compare") is not None]

    def warns(r):
        return sorted({w for k, v in ((r or {}).get("runs") or {}).items() if k.startswith("pex_rc")
                       for w in v.get("numerical_warnings", [])})
    clean = [(f, r) for f, r in rcs if not warns(r)]       # the newest clean R+C run, else the newest one
    rc_f, rc = (clean or rcs)[-1] if rcs else (None, None)
    rc_warn = warns(rc)
    out = ["Hand-drawn layout against G2.0 (bench conditions). G2.0 is S2's estimate, before any layout, of the "
           "spec lost to a compact layout's parasitics, split into route capacitance / capacitance inside the device "
           "cells / resistance (routes + cell access). The hand layout's loss is its drawn devices -> extracted "
           "netlist; the capacitance-only extraction can only be compared with the capacitance parts.", "",
           "| spec | margin | " + " | ".join(f"G2.0 {t}: C routes / C cells / R" for t in g)
           + " | hand layout, C only | hand layout, R+C |", "|---|---|" + "---|" * len(g) + "---|---|"]
    for k in ("gain_db", "gbw_mhz", "pm_deg"):
        mg = ((nom.get("compare") or {}).get(k) or {}).get("margin")
        cells = []
        for t, v in g.items():
            p = v.get(k)
            f3 = lambda v: "0" if abs(v) < 1e-9 else f"{v:.3g}"  # noqa: E731
            cells.append("–" if not p else f"{f3(p['cap_wiring'])} / {f3(p['cap_cells'])} / {f3(p['r_wiring'] + p['r_access'])}")
        c_only = (nom.get("lost_to_parasitics") or {}).get(k)
        rcv = ((rc or {}).get("lost_to_parasitics_rc") or {}).get(k)
        out.append(f"| {k} | {_fmt(mg)} | " + " | ".join(cells) + f" | {_fmt(c_only)} | "
                   + (_fmt(rcv) + (" (run warnings)" if rc_warn else "") if rc else "not run") + " |")
    out.append("")
    if rc:
        out += [f"R+C run: `{rc_f.relative_to(REPO)}`" + (f"; ngspice warnings: {', '.join(rc_warn)}. Gmin stepping "
                "failed in this run's operating point, so its R+C numbers are not trusted." if rc_warn else "."), ""]
    return out


def report() -> Path:
    lines = ["# Before / after (plan v2)", "",
             "Generated by `scripts/compare_before_after.py report` from `outputs/compare/`. 'before' is the flow as",
             "it was (v1: allocation without floors and without the R19 fix, S3 rules v1, A-free options, nominal",
             "only), run after the generality fixes that let it ingest the new circuits; 'after' is v2;",
             "'after_nopvt' is v2 with nominal constraints only in S2 (ablation of the PVT constraints, G2.9);",
             "'after_eta0.9' is v2's S2 at eta = 0.9 (PREREG's headline eta; S3 not re-run).", ""]
    for dd in sorted(p for p in OUT.glob("*") if p.is_dir()):
        order = {"before": 0, "after": 1}          # then ablations (after_*) by name
        tags = sorted(dd.glob("*.json"), key=lambda f: (order.get(f.stem, 2), f.stem))
        recs = {t.stem: json.loads(t.read_text()) for t in tags}
        if not recs:
            continue
        lines += [f"## {dd.name}", "", "| | " + " | ".join(recs) + " |", "|---|" + "---|" * len(recs)]

        def row(label, fn):
            vals = []
            for r in recs.values():
                try:
                    vals.append(_fmt(fn(r)))
                except Exception:
                    vals.append("–")
            lines.append(f"| {label} | " + " | ".join(vals) + " |")
        for st in ("S0", "S1", "S2", "S3"):
            row(f"{st} failed gates", lambda r, st=st: (r[st] or {}).get("failed") if r.get(st) else "not run")
        row("S1 linear − SPICE (gain dB, GBW rel, PM °)", lambda r: [round(v, 4) for v in r["S1"]["linear_vs_spice"].values()])
        row("S1 symbolic − SPICE (gain, GBW MHz, PM)", lambda r: [round(v, 3) for v in r["S1"]["symbolic_vs_spice"].values()])
        row("S2 eta / alloc", lambda r: f"{r['S2']['eta']} / {r['S2']['alloc']}")
        row("S2 expected layout use (fraction of margin)", lambda r: {k: round(v, 3) for k, v in r["S2"]["expected_use_fraction"].items()})
        row("S2 round-1 t (budget / need)", lambda r: r["S2"]["t_round1"])
        row("S2 budgeted / starved (budget < need)", lambda r: f"{r['S2']['n_budgeted']} / {r['S2']['starved']}")
        row("S2 SPICE use at budget (fraction of margin)", lambda r: {k: round(v, 3) for k, v in r["S2"]["verify"].items()
                                                                       if v is not None and not k.startswith("sat_")})
        row("S2 library floors feasible", lambda r: (r["S2"]["floors"] or {}).get("pass"))
        row("S2 PVT constraints added", lambda r: r["S2"]["pvt"].get("constraints_added"))
        row("S3 mode / rules", lambda r: f"{r['S3']['mode']} / {r['S3']['rules']}")
        row("S3 relaxed types", lambda r: r["S3"]["relaxed"])
        row("S3 total device area (µm²)", lambda r: r["S3"]["total_device_area_um2"])
        row("S3 final gain / GBW / PM", lambda r: [round(r["S3"]["final"].get(k, float("nan")), 3) for k in ("gain_db", "gbw_mhz", "pm_deg")])
        lines.append("")
        main = "after" if "after" in recs else list(recs)[-1]
        last = recs[main]
        bl = (last.get("S2") or {}).get("baselines")
        if bl:
            lines += [f"Budget rules on the same sensitivities ({main}):", "",
                      "| rule | worst use / allowed (1st order) | worst use / allowed (SPICE) | specs violated (SPICE) | failed SPICE runs | starved | below floor | budget/need: min / geomean | outcome |",
                      "|---|---|---|---|---|---|---|---|---|"]
            room = (last.get("S2") or {}).get("baseline_budget_over_need") or {}
            for m, sc in bl.items():
                gm = (room.get(m) or {}).get("geomean")
                lines.append(f"| {m} | {_fmt(sc.get('worst_use_of_allowed'))} | {_fmt(sc.get('spice_worst_use_of_allowed'))} | "
                             f"{_fmt(sc.get('spice_specs_violated'))} | {len(sc.get('spice_failed_runs') or [])}/{_fmt(sc.get('spice_checks'))} | "
                             f"{len(sc.get('starved', []))}/{sc.get('n_elements')} | "
                             f"{len(sc.get('below_floor', []))} | {_fmt(sc.get('min_ratio_to_need'))} / {_fmt(gm)} | {_fmt(sc.get('outcome'))} |")
            lines.append("")
        bm = (last.get("S3") or {}).get("by_mode")
        if bm:
            lines += [f"S3 option modes ({main}):", "", "| mode | total area (µm²) | relaxed types | fingers outside the sized W bin |",
                      "|---|---|---|---|"]
            for m, v in bm.items():
                lines.append(f"| {m} | {_fmt(v['total_area_um2'])} | {_fmt(v['relaxed'])} | {_fmt(v['fingers_outside_sized_bin'])} |")
            lines.append("")
        lines += hand_layout_rows(dd.name, recs)
    f = REPO / "docs" / "before_after.md"
    f.write_text("\n".join(lines) + "\n")
    return f


if __name__ == "__main__":
    if sys.argv[1] == "snap":
        print(snap(sys.argv[2], sys.argv[3]))
    elif sys.argv[1] == "report":
        print(report())
