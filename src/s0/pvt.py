#!/usr/bin/env python3
"""S0 extension (plan v2): the design across PVT corners and under device mismatch, before any layout.

  PVT : 5 process corners (tt ff ss fs sf) x VDD (nominal, -10 %, +10 %) x temperature (-40, 27, 85 C)
        = 45 points; the S0 AC and OP testbenches (and NOISE when a noise spec exists) at every point.
  MC  : N runs of the tt_mm library section (mismatch only, sky130 AGAUSS models), one seed per run:
        offset of the unity-gain follower (the OP bench closes the loop at DC, or is turned into a
        follower) and the AC specs.
Margins per point feed S2 (one budget constraint per spec and point, plan v2); points where the sized
circuit already misses a spec are reported: no layout budget exists there.

usage (inside layout-s0s3):  python3 -m src.s0.pvt inputs/<design>/package.yaml [--mc 200] [--workers 4]
Outputs: outputs/S0/<design>/pvt.json, mc.json, plots/pvt_*.png; gates G0.9 (PVT) and G0.10 (MC) are
added to s0_report.json as information (pass = None).
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import statistics
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.common.tools import REPO, bench, rel, run_ngspice_text, write_json
from src.s0.ingest import load_package

CORNERS = ("tt", "ff", "ss", "fs", "sf")
VDD_FACTORS = (0.9, 1.0, 1.1)
TEMPS = (-40, 27, 85)


def with_conditions(txt: str, corner: str, vdd: float | None, temp: float | None, seed: int | None = None) -> str:
    txt = re.sub(r"(sky130\.lib\.spice)\s+\w+", rf"\1 {corner}", txt, count=1)
    if vdd is not None:
        txt = re.sub(r"(^\.param .*?\bVDD_V=)([^\s]+)", rf"\g<1>{vdd:g}", txt, count=1, flags=re.M)
    if temp is not None:
        txt = re.sub(r"^\.temp .*$", f".temp {temp:g}", txt, count=1, flags=re.M)
    if seed is not None:
        txt = re.sub(r"^(\.lib .*sky130\.lib\.spice.*)$", rf"\1\n.option seed={seed}", txt, count=1, flags=re.M)
    return txt


def follower(op_txt: str) -> str:
    """OP bench as a unity-gain follower (already one when it closes the loop at DC through a choke)."""
    if re.search(r"^L\S*\s+OUT\S*\s+IN[NP]\s", op_txt, re.M | re.I):
        return op_txt
    out, n = re.subn(r"^Vinn\s+INN\s+0\s+.*$", "Vinn INN OUT 0", op_txt, count=1, flags=re.M | re.I)
    if n != 1:
        raise RuntimeError("no way to make a follower of the OP bench")
    return out


def margin_of(meas: dict, specs: dict) -> dict:
    out = {}
    for k, lim in specs.items():
        v = meas.get(k)
        if v is None:
            continue
        out[k] = (v - lim["min"]) if "min" in lim else (lim["max"] - v)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package")
    ap.add_argument("--mc", type=int, default=None, help="Monte Carlo runs (default: package key mc_runs, else 200)")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args(argv)
    pkg = load_package(REPO / a.package)
    design = pkg["design"]
    s0 = REPO / "outputs" / "S0" / design
    tb = s0 / "tb"
    ir = json.loads((s0 / "circuit_ir.json").read_text())
    specs = ir["specs"]
    vdd0 = float(ir["conditions"].get("VDD_V", 1.8))
    kinds = ["AC", "OP"] + (["NOISE"] if "vnoise_nv_rthz" in specs else [])
    decks = {k: bench(tb, k).read_text() for k in kinds}
    work = s0 / "pvt_work"

    jobs = []
    for c, fv, t in itertools.product(CORNERS, VDD_FACTORS, TEMPS):
        pid = f"{c}_v{fv:g}_t{t:g}"
        for k in kinds:
            jobs.append(("pvt", pid, k, with_conditions(decks[k], c, vdd0 * fv, t), work / "pvt" / pid / k,
                         {"corner": c, "vdd": vdd0 * fv, "temp": t}))
    n_mc = a.mc if a.mc is not None else int(pkg.get("mc_runs", 200))
    fol = follower(decks["OP"])
    for i in range(n_mc):
        seed = 1000 + i
        jobs.append(("mc", f"mc{i:03d}", "OP", with_conditions(fol, "tt_mm", None, None, seed), work / "mc" / f"{i:03d}" / "OP",
                     {"seed": seed}))
        jobs.append(("mc", f"mc{i:03d}", "AC", with_conditions(decks["AC"], "tt_mm", None, None, seed),
                     work / "mc" / f"{i:03d}" / "AC", {"seed": seed}))

    def one(j):
        grp, pid, k, txt, wd, cond = j
        r = run_ngspice_text(txt, wd, k.lower(), cache=False)
        return grp, pid, k, cond, (r["meas"] if r["rc"] == 0 else None)

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        res = list(ex.map(one, jobs))

    points: dict = {}
    mc: dict = {}
    for grp, pid, k, cond, meas in res:
        tgt = points if grp == "pvt" else mc
        rec = tgt.setdefault(pid, {**cond, "meas": {}, "failed": []})
        if meas is None:
            rec["failed"].append(k)
        else:
            rec["meas"].update(meas)
    for pid, rec in points.items():
        rec["margin"] = margin_of(rec["meas"], specs)
        rec["meets_all"] = not rec["failed"] and all(rec["margin"].get(k, -1) >= 0 for k in specs)
    worst = {}
    for k in specs:
        vals = [(r["margin"][k], pid) for pid, r in points.items() if k in r["margin"]]
        if vals:
            m, pid = min(vals)
            worst[k] = {"margin": m, "point": pid, "nominal_margin": ir["margins"].get(k, {}).get("margin")}
    write_json(s0 / "pvt.json", {"design": design, "corners": CORNERS, "vdd_factors": VDD_FACTORS, "temps": TEMPS,
                                 "specs": specs, "points": points, "worst_margin": worst,
                                 "n_meeting_all_specs": sum(1 for r in points.values() if r["meets_all"])})
    # Monte Carlo summary
    sig = "vout_v"
    offs = [r["meas"].get(sig) for r in mc.values() if r["meas"].get(sig) is not None]
    vcm = float(ir["conditions"].get("VCM_V", 0.9))
    diff_out = bench(tb, "AC").name.startswith("dido")
    offset_v = [o if diff_out else (o - vcm) for o in offs]   # follower: v(OUT) - VCM, or v(OUTP) - v(OUTN)
    summ = {}
    for k in ("gain_db", "gbw_mhz", "pm_deg"):
        v = [r["meas"].get(k) for r in mc.values() if r["meas"].get(k) is not None]
        if len(v) > 1:
            summ[k] = {"mean": statistics.fmean(v), "std": statistics.stdev(v), "min": min(v), "max": max(v), "n": len(v)}
    if len(offset_v) > 1:
        summ["offset_v"] = {"mean": statistics.fmean(offset_v), "std": statistics.stdev(offset_v),
                            "min": min(offset_v), "max": max(offset_v), "n": len(offset_v),
                            "definition": "follower output - VCM (single-ended) or v(OUTP) - v(OUTN) (differential)"}
    write_json(s0 / "mc.json", {"design": design, "runs": n_mc, "library_section": "tt_mm (mismatch only)",
                                "summary": summ, "runs_detail": mc})
    # plots
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        (s0 / "plots").mkdir(exist_ok=True)
        ks = [k for k in ("gain_db", "gbw_mhz", "pm_deg") if k in specs]
        fig, axs = plt.subplots(1, len(ks), figsize=(5 * len(ks), 4))
        axs = axs if len(ks) > 1 else [axs]
        for ax, k in zip(axs, ks):
            for ci, c in enumerate(CORNERS):
                xs, ys = [], []
                for pid, r in points.items():
                    if r["corner"] == c and k in r["meas"]:
                        xs.append(ci + 0.08 * (TEMPS.index(r["temp"]) - 1) + 0.03 * (VDD_FACTORS.index(round(r["vdd"] / vdd0, 3)) - 1))
                        ys.append(r["meas"][k])
                ax.scatter(xs, ys, s=14)
            lim = specs[k].get("min", specs[k].get("max"))
            ax.axhline(lim, color="#E45756", lw=1, label="spec")
            ax.set_xticks(range(len(CORNERS))); ax.set_xticklabels(CORNERS); ax.set_title(k); ax.legend(fontsize=7)
        fig.suptitle(f"{design}: 45 PVT points (VDD +-10 %, -40/27/85 C), pre-layout")
        fig.tight_layout(); fig.savefig(s0 / "plots" / "pvt_specs.png", dpi=110); plt.close(fig)
    except Exception as e:  # evidence, not a gate
        print("plot error:", e)
    rep_f = s0 / "s0_report.json"
    rep = json.loads(rep_f.read_text())
    rep["gates"]["G0.9_pvt (info)"] = {"pass": None, "points": len(points),
                                       "meeting_all_specs": sum(1 for r in points.values() if r["meets_all"]),
                                       "worst_margin": worst, "failed_runs": sorted(p for p, r in points.items() if r["failed"]),
                                       "detail": rel(s0 / "pvt.json")}
    rep["gates"]["G0.10_mismatch_mc (info)"] = {"pass": None, "runs": n_mc, "summary": summ, "detail": rel(s0 / "mc.json")}
    write_json(rep_f, rep)
    print(f"PVT: {sum(1 for r in points.values() if r['meets_all'])}/{len(points)} points meet every spec; worst {worst}")
    print(f"MC ({n_mc} runs): {json.dumps({k: {kk: round(vv, 6) for kk, vv in v.items() if isinstance(vv, float)} for k, v in summ.items()})}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
