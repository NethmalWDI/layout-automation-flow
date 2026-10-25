"""Thin wrappers around the EDA tools inside the layout-s0s3 container, plus provenance helpers."""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PDK_ROOT = os.environ.get("PDK_ROOT", "/foss/pdks")
TOOL_ENV = {
    **os.environ,
    "PATH": "/foss/tools/bin:/foss/tools/sak:/foss/tools/klayout:" + os.environ.get("PATH", ""),
    "PDK_ROOT": PDK_ROOT,
    "PDK": "sky130A",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rel(path: Path) -> str:
    try:
        return str(Path(path).resolve().relative_to(REPO))
    except ValueError:
        return str(path)


def git_commit() -> str:
    try:
        return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True,
                              text=True, timeout=20).stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def provenance(inputs: list, extra: dict | None = None) -> dict:
    return {
        "created": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "inputs": [{"path": rel(p), "sha256": sha256(p)} for p in inputs if p and Path(p).exists()],
        **(extra or {}),
    }


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")


def run_ngspice(deck: Path, workdir: Path, timeout: int = 600) -> dict:
    """Run ngspice in batch mode; return {'rc', 'meas': {key: float}, 'log'}."""
    workdir.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["ngspice", "-b", str(deck)], cwd=workdir, env=TOOL_ENV,
                       capture_output=True, text=True, timeout=timeout)
    log = r.stdout + r.stderr
    (workdir / (deck.stem + ".log")).write_text(log)
    meas = {}
    for m in re.finditer(r"^MEAS\s+(\w+)\s+(\S+)", log, re.M):
        try:
            meas[m.group(1)] = float(m.group(2))
        except ValueError:
            meas[m.group(1)] = None
    return {"rc": r.returncode, "meas": meas, "log": rel(workdir / (deck.stem + ".log"))}


def run_netgen_compare(a: Path, a_cell: str, b: Path, b_cell: str, report: Path, timeout: int = 300) -> dict:
    """Netgen LVS between two netlists; the result is read from the report text, not the exit code."""
    setup = Path(PDK_ROOT) / "sky130A/libs.tech/netgen/sky130A_setup.tcl"
    report.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["netgen", "-batch", "lvs", f"{a} {a_cell}", f"{b} {b_cell}", str(setup), str(report)],
                       cwd=report.parent, env=TOOL_ENV, capture_output=True, text=True, timeout=timeout)
    (report.parent / (report.stem + ".netgen.log")).write_text(r.stdout + r.stderr)
    txt = report.read_text() if report.exists() else ""
    unique = "Circuits match uniquely" in txt
    prop_err = bool(re.search(r"property errors|Property errors", txt))
    pins_bad = "failed pin matching" in txt
    return {"match_uniquely": unique, "property_errors": prop_err, "pin_mismatch": pins_bad,
            "pass": unique and not prop_err and not pins_bad, "report": rel(report)}
