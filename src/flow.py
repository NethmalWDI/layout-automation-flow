#!/usr/bin/env python3
"""One entry point for the whole flow: run designs stage by stage, show their status, test them.

Run inside the EDA image (the launchers ./flow and flow.ps1 do that for you):

  python3 -m src.flow list                                   designs found in inputs/
  python3 -m src.flow run <design>|all [--stage S0..S3|all] [--from S1] [--workers 4] [--strict]
  python3 -m src.flow status <design>|all                    gate table from the stage reports
  python3 -m src.flow test [--stage S0..S3] [--design d] [--rerun]   unit tests + golden comparison
  python3 -m src.flow snapshot <design> [--stage Sx]         (maintainers) write tests/golden/<design>/<stage>.json

A stage reads only the outputs of the stages before it (outputs/<stage>/<design>/). Exit status of a
stage: PASS (all gates pass), FAIL (a gate failed; the stage still produced its report, e.g. S3 flags a
device type), ERROR (no fresh report: the stage crashed). The run stops on ERROR, and on FAIL only with
--strict. A summary is written to outputs/flow/<design>/flow_summary.json and every command's log to
runs/logs/flow/<design>/.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
import time
from pathlib import Path

import yaml

from src.common.tools import REPO

STAGES = ["S0", "S1", "S2", "S3"]
PY = sys.executable


def designs() -> list[str]:
    out = []
    for p in sorted((REPO / "inputs").glob("*/package.yaml")):
        if p.parent.name.startswith("_"):
            continue
        out.append(p.parent.name)
    return out


def package(design: str) -> Path:
    p = REPO / "inputs" / design / "package.yaml"
    if not p.exists():
        sys.exit(f"no package for design '{design}': expected {p.relative_to(REPO)}")
    return p


def report_path(stage: str, design: str) -> Path:
    return REPO / "outputs" / stage / design / f"{stage.lower()}_report.json"


def pkg_yaml(design: str) -> dict:
    return yaml.safe_load(package(design).read_text())


VARIANT_ARGS = {   # v1: the flow before the plan-v2 updates (ablation / "before"); v2: current
    "v1": {"S0": ["--no-pvt"], "S2": ["--alloc", "v1", "--no-pvt", "--no-baselines"], "S3": ["--rules", "v1", "--mode", "A-free"]},
    "v2": {"S0": [], "S2": [], "S3": []},
}


def steps(stage: str, design: str, a) -> list[tuple[str, list[str]]]:
    """The commands that make up one stage, in order: (label, argv)."""
    pkg = str(package(design).relative_to(REPO))
    w = ["--workers", str(a.workers)]
    var = VARIANT_ARGS[getattr(a, "variant", "v2") or "v2"]
    if stage == "S0":
        s = [("ingest", [PY, "-m", "src.s0.ingest", pkg]),
             ("pcell_binding", [PY, "-m", "src.s0.pcell_binding", f"outputs/S0/{design}", "--workers", str(a.workers)])]
        if not getattr(a, "no_pvt", False) and "--no-pvt" not in var["S0"]:
            s.append(("pvt", [PY, "-m", "src.s0.pvt", pkg] + w))
        return s
    if stage == "S1":
        s = [("run", [PY, "-m", "src.s1.run", pkg] + (["--no-fd"] if a.skip_fd else []))]
        if "symbolic_patch" in (pkg_yaml(design).get("s1_extras") or []):
            s.append(("symbolic_patch", [PY, "-m", "src.s1.symbolic_patch", pkg]))
        return s
    if stage == "S2":
        s = []
        if not (REPO / "outputs" / "S2" / "pdk" / "parasitics.json").exists():
            s.append(("pdk_parasitics", [PY, "-m", "src.s2.pdk_parasitics"]))
        # S2's expected need uses the default device cells of the S3 library (built before S2)
        s.append(("cells", [PY, "-m", "src.s3.run", pkg, "--cells-only"] + w))
        s.append(("run", [PY, "-m", "src.s2.run", pkg] + w + var["S2"]))
        return s
    if stage == "S3":
        return [("run", [PY, "-m", "src.s3.run", pkg] + w + var["S3"])]
    raise ValueError(stage)


def gates_of(report: dict) -> dict:
    out = {}
    for k, v in (report.get("gates") or {}).items():
        out[k] = v.get("pass") if isinstance(v, dict) else v
    return out


def run_stage(stage: str, design: str, a) -> dict:
    logdir = REPO / "runs" / "logs" / "flow" / design
    logdir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    rec = {"stage": stage, "steps": [], "started": dt.datetime.now().isoformat(timespec="seconds")}
    for label, cmd in steps(stage, design, a):
        log = logdir / f"{stage}_{label}.log"
        ts = time.time()
        with log.open("w") as fh:
            fh.write("$ " + " ".join(cmd) + "\n")
            fh.flush()
            r = subprocess.run(cmd, cwd=REPO, stdout=fh, stderr=subprocess.STDOUT)
        rec["steps"].append({"step": label, "rc": r.returncode, "seconds": round(time.time() - ts, 1),
                             "log": str(log.relative_to(REPO))})
        print(f"  {stage}/{label:15s} rc={r.returncode}  {time.time() - ts:7.1f} s  log: {log.relative_to(REPO)}")
    rp = report_path(stage, design)
    fresh = rp.exists() and rp.stat().st_mtime >= t0 - 1
    if not fresh:
        rec["status"] = "ERROR"
        rec["reason"] = f"no fresh report at {rp.relative_to(REPO)}"
    else:
        rep = json.loads(rp.read_text())
        g = gates_of(rep)
        rec["gates"] = g
        failed = [k for k, v in g.items() if v is False]
        rec["status"] = "PASS" if not failed else "FAIL"
        rec["failed_gates"] = failed
    rec["seconds"] = round(time.time() - t0, 1)
    return rec


def cmd_run(a) -> int:
    targets = designs() if a.design == "all" else [a.design]
    order = STAGES if a.stage in (None, "all") else [a.stage]
    if a.from_stage:
        order = STAGES[STAGES.index(a.from_stage):]
    worst = 0
    for d in targets:
        print(f"== {d}")
        summ_f = REPO / "outputs" / "flow" / d / "flow_summary.json"
        summ = json.loads(summ_f.read_text()) if summ_f.exists() else {"design": d, "stages": {}}
        for st in order:
            rec = run_stage(st, d, a)
            summ["stages"][st] = rec
            msg = rec["status"] + (f"  failed: {rec['failed_gates']}" if rec.get("failed_gates") else "") \
                + (f"  ({rec['reason']})" if rec.get("reason") else "")
            print(f"  {st}: {msg}")
            summ_f.parent.mkdir(parents=True, exist_ok=True)
            summ_f.write_text(json.dumps(summ, indent=1) + "\n")
            if rec["status"] == "ERROR":
                worst = max(worst, 2)
                break
            if rec["status"] == "FAIL":
                worst = max(worst, 1)
                if a.strict:
                    break
    return worst


def cmd_status(a) -> int:
    targets = designs() if a.design == "all" else [a.design]
    for d in targets:
        print(f"== {d}")
        for st in STAGES:
            rp = report_path(st, d)
            if not rp.exists():
                print(f"  {st}: not run")
                continue
            g = gates_of(json.loads(rp.read_text()))
            failed = [k for k, v in g.items() if v is False]
            when = dt.datetime.fromtimestamp(rp.stat().st_mtime).isoformat(timespec="minutes")
            print(f"  {st}: {'PASS' if not failed else 'FAIL'}  ({len(g)} gates, {when})" +
                  (f"  failed: {failed}" if failed else ""))
    return 0


def cmd_list(a) -> int:
    for d in designs():
        pk = pkg_yaml(d)
        print(f"{d:24s} {(pk.get('description') or '').strip().splitlines()[0][:90] if pk.get('description') else ''}")
    return 0


def cmd_test(a) -> int:
    from src import golden
    rc = 0
    if not a.golden_only:
        print("== unit tests")
        rc = subprocess.run([PY, "-m", "pytest", "-q", "tests", "-p", "no:cacheprovider"], cwd=REPO).returncode
    stages = STAGES if a.stage in (None, "all") else [a.stage]
    targets = golden.designs_with_snapshots() if a.design in (None, "all") else [a.design]
    for d in targets:
        for st in stages:
            snap = golden.snapshot_path(d, st)
            if not snap.exists():
                continue
            if a.rerun:
                print(f"== re-running {st} for {d}")
                rec = run_stage(st, d, a)
                if rec["status"] == "ERROR":
                    print(f"  ERROR: {rec.get('reason')}")
                    rc = rc or 2
                    continue
            diffs = golden.compare(d, st)
            print(f"== golden {d} {st}: {'OK' if not diffs else f'{len(diffs)} differences'}")
            for x in diffs[:20]:
                print("   ", x)
            if diffs:
                rc = rc or 1
    return rc


def cmd_snapshot(a) -> int:
    from src import golden
    for st in (STAGES if a.stage in (None, "all") else [a.stage]):
        if report_path(st, a.design).exists():
            p = golden.write_snapshot(a.design, st)
            print("wrote", p.relative_to(REPO))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("design")
    r.add_argument("--stage", choices=STAGES + ["all"])
    r.add_argument("--from", dest="from_stage", choices=STAGES)
    r.add_argument("--workers", type=int, default=4)
    r.add_argument("--skip-fd", action="store_true", help="S1 without the transistor-level cross-check")
    r.add_argument("--strict", action="store_true", help="stop at the first stage with a failed gate")
    r.add_argument("--no-pvt", action="store_true", help="S0 without the PVT corners and Monte Carlo step")
    r.add_argument("--variant", choices=["v2", "v1"], default="v2",
                   help="v1 reproduces the flow before the plan-v2 updates (ablation, 'before')")
    s = sub.add_parser("status")
    s.add_argument("design", nargs="?", default="all")
    sub.add_parser("list")
    t = sub.add_parser("test")
    t.add_argument("--stage", choices=STAGES + ["all"])
    t.add_argument("--design")
    t.add_argument("--rerun", action="store_true", help="re-run the stage before comparing with the golden snapshot")
    t.add_argument("--golden-only", action="store_true")
    t.add_argument("--workers", type=int, default=4)
    t.add_argument("--skip-fd", action="store_true")
    t.add_argument("--no-pvt", action="store_true")
    t.add_argument("--variant", choices=["v2", "v1"], default="v2")
    n = sub.add_parser("snapshot")
    n.add_argument("design")
    n.add_argument("--stage", choices=STAGES + ["all"])
    a = ap.parse_args(argv)
    return {"run": cmd_run, "status": cmd_status, "list": cmd_list, "test": cmd_test, "snapshot": cmd_snapshot}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
