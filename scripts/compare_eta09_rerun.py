#!/usr/bin/env python3
"""S2 at eta 0.9: a design's first run against its re-run with the PC awake (plan v2; written by Claude Code,
2026-10-27, Imasha's decision).

The first eta 0.9 runs of example_ota_5t and loadbench_miller ran while Windows had the PC in Modern Standby. A
SPICE check slowed past its 180 s limit counts as a failed run: that marks a budget rule's outcome "unverified" and
can hide a violation. Their logs were removed when the 'after' outputs were put back. The re-run
(scripts/plan_v2_eta09_rerun.sh) keeps its S2 folder and records whether the container's clock jumped during it.

usage (inside the container, repo root):
  python3 scripts/compare_eta09_rerun.py <design> [<design> ...] [--first after_eta0.9] [--rerun after_eta0.9_rerun]
                                         [--json outputs/posthoc/eta09_rerun/compare.json]
Reads  outputs/compare/<design>/<first>.json and <rerun>.json (snapshots), and the re-run's kept S2 folder and
       clock record in outputs/posthoc/eta09_rerun/<design>/ (S2/, clock.json), when they exist
Writes the --json file; prints one table per design.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RERUN = REPO / "outputs" / "posthoc" / "eta09_rerun"
RULE_KEYS = ("outcome", "spice_failed_runs", "spice_worst_use_of_allowed", "spice_specs_violated",
             "worst_use_of_allowed")


def _j(p: Path):
    return json.loads(p.read_text()) if p.exists() else None


def timed_out(s2_dir: Path) -> list:
    """the re-run's SPICE runs that ended in the ngspice timeout (common.tools.run_ngspice writes 'TIMEOUT after')"""
    out = []
    for f in sorted(s2_dir.rglob("*.log")):
        try:
            if "TIMEOUT after" in f.read_text(errors="replace")[-200:]:
                out.append(str(f.relative_to(s2_dir)))
        except OSError:
            pass
    return out


def compare(design: str, first: str, rerun: str) -> dict:
    a = _j(REPO / "outputs" / "compare" / design / f"{first}.json")
    b = _j(REPO / "outputs" / "compare" / design / f"{rerun}.json")
    if not a or not b or not a.get("S2") or not b.get("S2"):
        return {"design": design, "error": f"snapshot {first} or {rerun}, or its S2 part, is missing"}
    sa, sb = a["S2"], b["S2"]
    s2 = {k: {"first": sa.get(k), "rerun": sb.get(k)} for k in ("failed", "eta", "t_round1", "starved", "n_budgeted")}
    s2["floors_pass"] = {"first": (sa.get("floors") or {}).get("pass"), "rerun": (sb.get("floors") or {}).get("pass")}
    va, vb = sa.get("verify") or {}, sb.get("verify") or {}
    dv = [abs(vb[k] - va[k]) for k in va if isinstance(va[k], (int, float)) and isinstance(vb.get(k), (int, float))]
    s2["verify_max_abs_change"] = max(dv, default=None)
    rules = {}
    for m in dict.fromkeys(list(sa.get("baselines") or {}) + list(sb.get("baselines") or {})):
        ra, rb = (sa.get("baselines") or {}).get(m) or {}, (sb.get("baselines") or {}).get(m) or {}
        rules[m] = {k: {"first": ra.get(k), "rerun": rb.get(k)} for k in RULE_KEYS}
    same = s2["failed"]["first"] == s2["failed"]["rerun"] and all(
        r["outcome"]["first"] == r["outcome"]["rerun"]
        and len(r["spice_failed_runs"]["first"] or []) == len(r["spice_failed_runs"]["rerun"] or [])
        for r in rules.values())
    d = RERUN / design
    return {"design": design, "first": first, "rerun": rerun, "s2": s2, "rules": rules,
            "same_gates_outcomes_and_failed_run_counts": same,
            "rerun_timed_out_runs": timed_out(d / "S2") if (d / "S2").exists() else None,
            "rerun_clock": _j(d / "clock.json")}


def _f(v):
    if isinstance(v, float):
        return f"{v:.3g}"
    if isinstance(v, list):
        return str(len(v))
    return "–" if v is None else str(v)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("designs", nargs="+")
    ap.add_argument("--first", default="after_eta0.9")
    ap.add_argument("--rerun", default="after_eta0.9_rerun")
    ap.add_argument("--json", default=str((RERUN / "compare.json").relative_to(REPO)))
    a = ap.parse_args(argv)
    res = {d: compare(d, a.first, a.rerun) for d in a.designs}
    out = REPO / a.json
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"created": dt.datetime.now().isoformat(timespec="seconds"), "designs": res},
                              indent=1) + "\n")
    for d, r in res.items():
        if r.get("error"):
            print(f"== {d}: {r['error']}")
            continue
        s2, ck, to = r["s2"], r["rerun_clock"] or {}, r["rerun_timed_out_runs"]
        print(f"== {d} ({r['first']} -> {r['rerun']}): same gates, outcomes and failed-run counts: "
              f"{'yes' if r['same_gates_outcomes_and_failed_run_counts'] else 'NO'}; re-run timed-out SPICE runs: "
              f"{'not kept' if to is None else len(to)}; re-run clock jump: {_f(ck.get('jump_s'))} s")
        print("   S2 " + "; ".join(f"{k} {_f(v['first'])} -> {_f(v['rerun'])}" for k, v in s2.items()
                                    if isinstance(v, dict)) + f"; verify max change {_f(s2['verify_max_abs_change'])}")
        print("   | rule | outcome | failed SPICE runs | SPICE worst use / allowed | specs violated (SPICE) |")
        for m, x in r["rules"].items():
            print(f"   | {m} | {_f(x['outcome']['first'])} -> {_f(x['outcome']['rerun'])} | "
                  f"{_f(x['spice_failed_runs']['first'])} -> {_f(x['spice_failed_runs']['rerun'])} | "
                  f"{_f(x['spice_worst_use_of_allowed']['first'])} -> {_f(x['spice_worst_use_of_allowed']['rerun'])} | "
                  f"{_f(x['spice_specs_violated']['first'])} -> {_f(x['spice_specs_violated']['rerun'])} |")
    print(out.relative_to(REPO))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
