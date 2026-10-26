#!/usr/bin/env python3
"""S3 — device design: PCell options per transistor, chosen against the S2 budgets, signed off.

usage (inside layout-s0s3):  python3 -m src.s3.run inputs/<design>/package.yaml [--workers 4]

Inputs : outputs/S0/<design>/circuit_ir.json + tb/, outputs/S1/<design>/intent.json,
         outputs/S2/<design>/budgets.json, outputs/S2/pdk/parasitics.json
Outputs: outputs/S3/<design>/
  option_table.json     every option of every device type: DRC/LVS, area, extraction, access R,
                        in-circuit specs and margin use
  device_decisions.json chosen option per device type, with the evidence for the choice
  cells/<cell>/...      GDS, PNG, DRC/LVS/PEX runs of every option
  plots/*.png, s3_report.json (gates G3.1-G3.5)
Option cells are design independent and cached in outputs/S3/_cells (same type + option = same cell).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.common import pcell
from src.common.tools import REPO, provenance, rel, write_json
from src.s0.ingest import load_package
from src.s3 import evaluate as E, options as O, wbins

F_DEVICE = 0.5   # ASSUMPTION: half of each terminal-R budget (S2) is for the PCell, half for routing (S5)
TOL = 0.01       # consumption tolerance: 1 % of the margin (simulation resolution)
AREA_TIE = 0.02  # options within 2 % of the smallest feasible area are compared on slack


def consumption(base: dict, now: dict, margins: dict) -> dict:
    out = {}
    for k, m in margins.items():
        if k in base and k in now and base[k] is not None and now[k] is not None:
            out[k] = (base[k] - now[k]) if m["kind"] == "min" else (now[k] - base[k])
    for d, v in (now.get("sat_V") or {}).items():
        if d in (base.get("sat_V") or {}):
            out[f"sat_{d}"] = base["sat_V"][d] - v
    return out


def model_change(base: dict, rec: dict, t: dict) -> dict:
    """How far the chosen cell changes the transistor itself, cell only (no access R): drain current and gm
    of the whole device (one probed finger x nf) relative to the sized netlist device. A multi-finger option
    puts each finger in another SKY130 W bin, so this is a re-sizing effect for the sizing stage to know."""
    nf = rec["option"]["nf"]
    now = (rec.get("in_circuit_cell_only") or {}).get("op_params") or {}
    b0 = base.get("op_params") or {}
    out = {}
    for d in t["devices"]:
        if d in now and d in b0 and b0[d].get("id") and now[d].get("id") is not None:
            out[d] = {"id_rel": abs(now[d]["id"]) * nf / abs(b0[d]["id"]) - 1,
                      "gm_rel": (now[d]["gm"] * nf / b0[d]["gm"] - 1) if b0[d].get("gm") else None,
                      "vth_shift_V": (abs(now[d]["vth"]) - abs(b0[d]["vth"])) if now[d].get("vth") is not None else None}
    return {"per_device": out, "note": "cell only, vs the sized netlist device; nf > 1 changes the SKY130 W bin"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--cells-only", action="store_true", help="only build/measure the option cells (cache)")
    ap.add_argument("--mode", choices=list(O.MODES), default="A-bin",
                    help="option mode of the main decision (all modes are reported)")
    ap.add_argument("--build-mode", choices=list(O.MODES), default=None,
                    help="options to build: default the package key s3_build_mode, else A-free")
    ap.add_argument("--rules", choices=["v2", "v1"], default="v2",
                    help="v2: a cell may always use the library's lowest access R of its terminal (R19 b)")
    a = ap.parse_args(argv)
    pkg = load_package(REPO / a.package)
    design = pkg["design"]
    s0, s1, s2 = (REPO / "outputs" / s / design for s in ("S0", "S1", "S2"))
    out = REPO / "outputs" / "S3" / design
    cells_dir = REPO / "outputs" / "S3" / "_cells"
    (out / "plots").mkdir(parents=True, exist_ok=True)
    ir = json.loads((s0 / "circuit_ir.json").read_text())
    rules = json.loads((REPO / "outputs" / "S2" / "pdk" / "parasitics.json").read_text())["rules"]
    margins = dict(ir["margins"])
    gates = {}

    # 1. option table: build and measure every option of every device type (parallel, cached by cell)
    types = O.device_types(ir)
    build_mode = a.build_mode or pkg.get("s3_build_mode") or "A-free"
    jobs = [(tid, t, opt) for tid, t in types.items() for opt in O.grid(t["W"], wide=(a.rules == "v2"))
            if O.in_mode(t, opt, build_mode)]

    def build(job):
        tid, t, opt = job
        cache = cells_dir / f"{tid}__{opt['id']}" / "record.json"
        if cache.exists():
            return json.loads(cache.read_text())
        try:
            rec = O.build_one(t, tid, opt, cells_dir, rules, cross_check=(opt["id"] == O.default_option_id()))
        except Exception as e:  # recorded, never silently dropped
            rec = {"type": tid, "option": opt, "cell": f"{tid}__{opt['id']}", "ok": False, "error": repr(e)}
        write_json(cache, rec)
        return rec

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        table = list(ex.map(build, jobs))
    # geometry and access resistance are re-derived from the GDS on every run (cheap), so a change of the
    # resistance model never leaves stale cached values
    from src.s3 import strap as S
    for r in table:
        if r.get("ok"):
            gds = REPO / r["gds"]
            pl = S.plan(gds, r["option"]["outer"])
            r["geometry"] = O.geometry(gds, pl)
            r["access_resistance_ohm"] = O.access_resistance(types[r["type"]], r["option"], r["geometry"], rules)
            # keep the cache in step, so that S2's floors read the same values (review item 5)
            cf = cells_dir / r["cell"] / "record.json"
            if cf.exists():
                cr = json.loads(cf.read_text())
                if cr.get("access_resistance_ohm") != r["access_resistance_ohm"] or cr.get("geometry") != r["geometry"]:
                    cr["access_resistance_ohm"], cr["geometry"] = r["access_resistance_ohm"], r["geometry"]
                    write_json(cf, cr)
    bad = [r["cell"] for r in table if not r.get("ok")]
    gates["G3.4_option_table_complete"] = {"pass": len(table) == len(jobs), "options": len(table),
                                           "not_signed_off": bad, "build_mode": build_mode}
    if a.cells_only:
        print(f"option cells: {len(table)} built, {len(bad)} not signed off: {bad}")
        return 0
    budgets = json.loads((s2 / "budgets.json").read_text())

    # 2. allowances, in S2's own terms: S2's expected need of every element is split into the default device
    #    cells' part (measured) and the wiring part; the cells get the same fraction of each budget.
    #    R: every terminal of an option must satisfy R_access <= (cell fraction) * (S2 ohm budget of its group);
    #       the rest of the ohm budget is handed to S5.
    #    Cell: the cell's own effect (extracted cell without access R, vs. the S0 netlist device: its
    #       capacitances and any change of the device model itself) may use, of every capacitance budget, the
    #       fraction its default cell contributes to that element's expected need, plus its share of the
    #       margin S2 left unallocated; only harmful changes count.
    # margin S2 left unallocated inside eta*margin (non-binding checks): shared equally by the device types
    # (ASSUMPTION), usable for any cell effect, including a changed device model (nf > 1 moves a SKY130 device
    # into another W bin, which changes Vth, gm and flicker noise, not only parasitics)
    used_by = {}
    for e in budgets["elements"]:
        for k, v in (e.get("margin_used") or {}).items():
            used_by[k] = used_by.get(k, 0.0) + v
    slack = {c["id"]: max(0.0, c["b"] - used_by.get(c["id"], 0.0)) for c in budgets["constraints"]}
    slack_share = {k: v / max(1, len(types)) for k, v in slack.items()}
    r_budget, allow_c, allow_r = {}, {}, {}
    for tid, t in types.items():
        rb, ac_, ar_ = {}, {}, {}
        for e in budgets["elements"]:
            if e.get("budget") is None:
                continue
            parts = e.get("w_parts") or {}
            if e["kind"] == "terminal_resistance":
                mem = [m for m in e["targets"] if m.split(".")[0] in t["devices"]]
                if mem:
                    # the cell's share of the budget = its share of the expected need S2 allocated by
                    # (measured default-cell access R / need); F_DEVICE only if S2 had no split
                    frac = parts["device_cells"] / e["w"] if parts.get("device_cells") is not None else F_DEVICE
                    rb[mem[0].split(".")[1]] = {"group": e["id"], "budget_ohm": e["budget"], "cell_fraction": frac}
                    for k, v in e["margin_used"].items():
                        ar_[k] = ar_.get(k, 0.0) + frac * v
            else:
                by_dev = parts.get("device_cells_by_device") or {}
                frac = sum(v for d_, v in by_dev.items() if d_ in t["devices"]) / e["w"] if e["w"] else 0.0
                if frac > 0:
                    for k, v in e["margin_used"].items():
                        ac_[k] = ac_.get(k, 0.0) + frac * v
        for k, v in slack_share.items():
            ac_[k] = ac_.get(k, 0.0) + v
        r_budget[tid], allow_c[tid], allow_r[tid] = rb, ac_, ar_

    # 3. in-circuit evaluation of each signed-off option's cell (no access R): its capacitance effect
    sim = [("baseline", k, txt, wd) for k, txt, wd in E.scenario_jobs(s0, ir, {}, out / "sim" / "baseline")]
    for r in table:
        if r.get("ok"):
            repl = {d: (r, None) for d in types[r["type"]]["devices"]}
            sim += [(r["cell"], k, txt, wd) for k, txt, wd in E.scenario_jobs(s0, ir, repl, out / "sim" / r["cell"])]
    res = E.collect(E.run_jobs(sim, a.workers))
    base = res["baseline"]
    if base.get("failed"):
        raise RuntimeError(f"baseline simulation failed: {base['failed']}")
    need = [k for k in margins if k in base] + ["sat_V"]

    def mg_of(k):
        return margins[k]["margin"] if k in margins else base["sat_V"].get(k[4:])

    r_floor = {}
    for r in table:
        if r.get("ok") and O.in_mode(types[r["type"]], r["option"], a.mode):   # options the main mode may use
            for term in "dgs":
                v = r["access_resistance_ohm"][term]
                key_ = (r["type"], term)
                r_floor[key_] = min(r_floor.get(key_, v), v)
    for r in table:
        if not r.get("ok"):
            continue
        now = res.get(r["cell"], {"failed": ["missing"]})
        r["in_circuit_cell_only"] = now
        if now.get("failed") or any(k not in now for k in need):
            r["feasible"], r["min_slack"] = False, None
            r["budget_check"] = {"simulation": "failed or incomplete"}
            continue
        signed = consumption(base, now, margins)
        harm = {k: max(0.0, v) for k, v in signed.items()}
        al = allow_c[r["type"]]
        cc = {k: {"used_harmful": u, "signed": signed[k], "allowed": al.get(k, 0.0),
                  "ok": u <= al.get(k, 0.0) + TOL * (mg_of(k) or 0),
                  "slack_frac_of_margin": (al.get(k, 0.0) + TOL * (mg_of(k) or 0) - u) / mg_of(k) if mg_of(k) else None}
              for k, u in harm.items()}
        rc_ = {}
        for term, rbv in r_budget[r["type"]].items():
            lim_ = rbv["cell_fraction"] * rbv["budget_ohm"]
            if a.rules == "v2":   # R19 b: the cheapest cell of the library always fits, if the budget allows it
                lim_ = min(rbv["budget_ohm"], max(lim_, r_floor.get((r["type"], term), 0.0)))
            ra = r["access_resistance_ohm"][term]
            rc_[term] = {"group": rbv["group"], "R_access_ohm": ra, "allowed_ohm": lim_, "ok": ra <= lim_,
                         "remaining_for_routing_ohm": rbv["budget_ohm"] - ra,
                         "slack_frac": (lim_ - ra) / lim_ if lim_ else None}
        r["budget_check"] = {"capacitance": cc, "resistance": rc_}
        r["margin_use_cell_only"] = signed
        r["feasible"] = all(c["ok"] for c in cc.values()) and all(c["ok"] for c in rc_.values())
        sl = [c["slack_frac_of_margin"] for c in cc.values() if c["slack_frac_of_margin"] is not None] + \
             [c["slack_frac"] for c in rc_.values() if c["slack_frac"] is not None]
        r["min_slack"] = min(sl) if sl else None

    # 4. choose per type: smallest feasible area; near-ties (2 %) by largest slack -- for every option mode
    def choose(mode: str) -> dict:
        decisions = {}
        for tid, t in types.items():
            if mode == "RoT":
                cand = [r for r in table if r["type"] == tid and r.get("ok") and r.get("min_slack") is not None
                        and r["option"]["id"] == O.rule_of_thumb_id(t)]
            else:
                cand = [r for r in table if r["type"] == tid and r.get("ok") and r.get("min_slack") is not None
                        and O.in_mode(t, r["option"], mode)]
            if not cand:
                decisions[tid] = None
                continue
            feas = [r for r in cand if r["feasible"]]
            relaxed = not feas
            pool = feas or cand
            if relaxed:
                dflt_ = next((r for r in pool if r["option"]["id"] == O.default_option_id()), None)
                pick = dflt_ or max(pool, key=lambda r: r["min_slack"])
                why = ("no option met the allowance: the default PCell (the device exactly as sized) is kept and the "
                       "type is flagged (relaxation); see budget_check for what does not fit")
            else:
                amin = min(r["geometry"]["area_um2"] for r in pool)
                near = [r for r in pool if r["geometry"]["area_um2"] <= amin * (1 + AREA_TIE)]
                pick = max(near, key=lambda r: r["min_slack"])
                why = (f"smallest area among the {len(feas)} of {len(cand)} options that stay within the allowance "
                       f"({len(near)} within {AREA_TIE:.0%} of it; largest slack among those)")
            dflt = next((r for r in table if r["type"] == tid and r.get("ok") and r.get("min_slack") is not None
                         and r["option"]["id"] == O.default_option_id()), None)
            decisions[tid] = {
                "devices": t["devices"], "model": t["model"], "W_um": t["W"], "L_um": t["L"],
                "chosen": pick["option"], "cell": pick["cell"], "gds": pick["gds"], "png": pick.get("png"),
                "reason": why, "relaxed": relaxed, "area_um2": pick["geometry"]["area_um2"],
                "bbox_um": pick["geometry"]["bbox_um"],
                "access_resistance_ohm": {k: pick["access_resistance_ohm"][k] for k in "dgs"},
                "budget_check": pick["budget_check"], "allowance_capacitance": allow_c[tid],
                "allowance_resistance_margin": allow_r[tid],
                "pex": {k: pick["pex"][k] for k in ("n_devices", "n_caps", "sum_caps_F")},
                "drc": pick["drc"], "lvs": pick["lvs"],
                "device_model_change": model_change(base, pick, t),
                "finger_in_sized_bin": wbins.same_bin(t["model"], t["W"], t["L"], t["W"] / pick["option"]["nf"]),
                "vs_default": None if not dflt else {
                    "default_cell": dflt["cell"], "default_area_um2": dflt["geometry"]["area_um2"],
                    "default_feasible": dflt.get("feasible"), "default_budget_check": dflt.get("budget_check"),
                    "default_access_resistance_ohm": {k: dflt["access_resistance_ohm"][k] for k in "dgs"},
                    "magic_extresist_cross_check": dflt.get("magic_extresist")},
                "n_options": len(cand), "n_feasible": len(feas)}
        return decisions

    by_mode = {m_: choose(m_) for m_ in ("B", "A-bin", "A-free", "RoT")}
    decisions = by_mode[a.mode]
    if any(v is None for v in decisions.values()):
        raise RuntimeError(f"mode {a.mode}: no built option for {[k for k, v in decisions.items() if v is None]}")
    mode_summary = {}
    for m_, dd in by_mode.items():
        ok_ = {k: v for k, v in dd.items() if v is not None}
        mode_summary[m_] = {"complete": len(ok_) == len(dd), "total_area_um2": sum(v["area_um2"] * len(v["devices"]) for v in ok_.values()),
                            "relaxed": sorted(k for k, v in ok_.items() if v["relaxed"]),
                            "fingers_outside_sized_bin": sorted(k for k, v in ok_.items() if not v["finger_in_sized_bin"]),
                            "chosen": {k: v["chosen"]["id"] for k, v in ok_.items()},
                            "missing": sorted(k for k, v in dd.items() if v is None)}
    gates["G3.7_modes (info)"] = {"pass": None, "main_mode": a.mode, "summary": mode_summary,
                                  "w_bins": wbins.table(sorted({t["model"] for t in types.values()})),
                                  "note": "the sky130 subcircuits pass W, not W/nf, to BSIM4; an nf-finger layout is "
                                          "extracted as fingers of W/nf, simulated in the bin of W/nf"}

    # 5. every chosen option at once, cells AND access resistance
    repl = {}
    for tid, dcs in decisions.items():
        rec = next(r for r in table if r["cell"] == dcs["cell"])
        for d in dcs["devices"]:
            repl[d] = (rec, rec["access_resistance_ohm"])
    final = E.collect(E.run_jobs([("final", k, txt, wd) for k, txt, wd in
                                  E.scenario_jobs(s0, ir, repl, out / "sim" / "_final")], a.workers))["final"]
    ok_runs = not final.get("failed") and all(k in final for k in need)
    fin_use = consumption(base, final, margins) if ok_runs else {}
    lim = {k: v["limit"] for k, v in margins.items()}
    spec_ok = {k: (final[k] >= lim[k] if margins[k]["kind"] == "min" else final[k] <= lim[k])
               for k in margins if k in final}
    tot_allow = {}
    for d_ in (allow_c, allow_r):
        for al in d_.values():
            for k, v in al.items():
                tot_allow[k] = tot_allow.get(k, 0.0) + v
    within = {k: max(0.0, u) <= tot_allow.get(k, 0.0) + TOL * (mg_of(k) or 0) for k, u in fin_use.items()}
    sat_ok = ok_runs and all(v > 0 for v in final["sat_V"].values())
    gates["G3.3_all_chosen_devices_in_circuit"] = {
        "pass": bool(ok_runs and all(spec_ok.values()) and sat_ok and all(within.values())),
        "specs": {k: final.get(k) for k in margins}, "meets": spec_ok, "saturated": final.get("sat_V"),
        "margin_use_signed": fin_use, "allowance_total": tot_allow, "within_allowance_harmful": within,
        "failed_runs": final.get("failed")}
    gates["G3.1_chosen_DRC"] = {"pass": all(d["drc"]["pass"] for d in decisions.values()),
                                "detail": {k: d["drc"] for k, d in decisions.items()}}
    gates["G3.2_chosen_LVS_W_L_nf"] = {"pass": all(d["lvs"]["pass"] for d in decisions.values()),
                                       "detail": {k: d["lvs"] for k, d in decisions.items()}}
    gates["G3.5_no_relaxation"] = {"pass": not any(d["relaxed"] for d in decisions.values()),
                                   "relaxed": [k for k, d in decisions.items() if d["relaxed"]]}
    allow = {"cell_margin": allow_c, "resistance_margin": allow_r, "resistance_ohm_budget": r_budget,
             "unallocated_slack_from_S2": slack, "slack_share_per_type": slack_share}

    # the sky130 model cards must not model gate resistance themselves (otherwise R_g would count twice)
    import re as _re
    from src.common.tools import PDK_ROOT
    rgm = {}
    for t in types.values():
        f = Path(PDK_ROOT) / "sky130A/libs.ref/sky130_fd_pr/spice" / f"{t['model']}__tt.pm3.spice"
        vals = sorted(set(_re.findall(r"rgatemod\s*=\s*([0-9.]+)", f.read_text()))) if f.exists() else None
        rgm[t["model"]] = {"file": str(f), "rgatemod_values": vals}
    gates["G3.6_model_has_no_gate_resistance"] = {
        "pass": all(v["rgatemod_values"] and all(float(x) == 0 for x in v["rgatemod_values"]) for v in rgm.values()),
        "detail": rgm}
    slim = []
    for r in table:
        slim.append({k: r.get(k) for k in ("type", "cell", "option", "ok", "gds", "png", "drc", "lvs", "geometry",
                                           "access_resistance_ohm", "pex", "in_circuit_cell_only", "margin_use_cell_only",
                                           "budget_check", "feasible", "min_slack", "magic_extresist", "strap", "error")})
    write_json(out / "option_table.json", {"design": design, "f_device": F_DEVICE, "tolerance": TOL,
                                           "baseline_S0": base, "allowance": allow, "options": slim})
    write_json(out / "device_decisions.json", {"design": design, "mode": a.mode, "rules": a.rules,
                                               "decisions": decisions, "final_in_circuit": final,
                                               "by_mode": mode_summary,
                                               "f_device_note": "ASSUMPTION: share of each terminal-R budget given to the PCell"})
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axs = plt.subplots(1, len(types), figsize=(5.2 * len(types), 4.3))
        axs = axs if len(types) > 1 else [axs]
        for ax, (tid, t) in zip(axs, types.items()):
            rs = [r for r in table if r["type"] == tid and r.get("min_slack") is not None]
            for feas, col in ((True, "#54A24B"), (False, "#E45756")):
                xs = [r["geometry"]["area_um2"] for r in rs if r["feasible"] == feas]
                ys = [r["min_slack"] for r in rs if r["feasible"] == feas]
                ax.scatter(xs, ys, c=col, s=26, label="within allowance" if feas else "over allowance")
            ch = next(r for r in table if r["cell"] == decisions[tid]["cell"])
            ax.scatter([ch["geometry"]["area_um2"]], [ch["min_slack"]], s=160, facecolors="none", edgecolors="k",
                       label=f"chosen: {ch['option']['id']}")
            ax.axhline(0, color="grey", lw=0.6)
            ax.set_xlabel("cell area (um^2)"); ax.set_ylabel("worst slack (fraction of margin)")
            ax.set_title(f"{tid}\n({', '.join(t['devices'])})", fontsize=9); ax.legend(fontsize=7)
        fig.tight_layout(); fig.savefig(out / "plots" / "option_space.png", dpi=110); plt.close(fig)
    except Exception as e:
        gates["G3.4_option_table_complete"]["plot_error"] = str(e)

    prov = provenance([s0 / "circuit_ir.json", s2 / "budgets.json", REPO / "outputs" / "S2" / "pdk" / "parasitics.json",
                       REPO / a.package])
    report = {"design": design, "gates": gates, "all_pass": all(g.get("pass") in (True, None) for g in gates.values()),
              "provenance": prov}
    write_json(out / "s3_report.json", report)
    for k in sorted(gates):
        print(f"{k:40s} {'PASS' if gates[k].get('pass') else 'FAIL'}")
    for tid, d in decisions.items():
        print(f"  {tid:28s} -> {d['chosen']['id']:24s} area {d['area_um2']:.1f} um2  R(d,g,s)="
              f"{', '.join(f'{d['access_resistance_ohm'][k]:.1f}' for k in 'dgs')} ohm")
    print("S3", "PASS" if report["all_pass"] else "FAIL", "->", rel(out))
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
