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


def bench(tb_dir: Path, kind: str) -> Path:
    """The testbench of one analysis (AC, OP, NOISE) in a folder: '<prefix>_<KIND>.spice', prefix
    diso_amp (single-ended output) or dido_amp (differential output). Exactly one per kind."""
    hits = sorted(Path(tb_dir).glob(f"*_{kind.upper()}.spice"))
    if len(hits) != 1:
        raise FileNotFoundError(f"expected one *_{kind.upper()}.spice in {tb_dir}, found {[h.name for h in hits]}")
    return hits[0]


def differential_output(tb_dir: Path) -> bool:
    return bench(tb_dir, "AC").name.startswith("dido")


def out_expr(tb_dir: Path) -> str:
    """The signal output as an ngspice expression in the testbench (node names of the bench)."""
    return "v(OUTP,OUTN)" if differential_output(tb_dir) else "v(OUT)"


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


def parse_meas(log: str) -> dict:
    meas = {}
    for m in re.finditer(r"^MEAS\s+(\w+)\s+(\S+)", log, re.M):
        try:
            meas[m.group(1)] = float(m.group(2))
        except ValueError:
            meas[m.group(1)] = None
    return meas


NUMERIC_TROUBLE = ("singular matrix", "gmin stepping failed", "source stepping failed", "timestep too small",
                   "no convergence")


def numerical_warnings(log: str) -> list:
    """Lines that mean the operating point may not be trustworthy (floating nodes, failed homotopy)."""
    return [ln.strip() for ln in log.splitlines() if any(t in ln.lower() for t in NUMERIC_TROUBLE)][:10]


def run_ngspice(deck: Path, workdir: Path, timeout: int = 600) -> dict:
    """Run ngspice in batch mode; return {'rc', 'meas': {key: float}, 'log', 'numerical_warnings'}."""
    workdir.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["ngspice", "-b", str(deck)], cwd=workdir, env=TOOL_ENV,
                       capture_output=True, text=True, timeout=timeout)
    log = r.stdout + r.stderr
    (workdir / (deck.stem + ".log")).write_text(log)
    (workdir / (deck.stem + ".rc")).write_text(str(r.returncode))
    return {"rc": r.returncode, "meas": parse_meas(log), "log": rel(workdir / (deck.stem + ".log")),
            "numerical_warnings": numerical_warnings(log)}


def run_ngspice_text(txt: str, workdir: Path, name: str, cache: bool = True, timeout: int = 600) -> dict:
    """Write <name>.spice and run it, unless the identical deck already ran successfully in this folder
    (same text, log present, exit code 0): then its log is re-read. Re-runs of a stage only simulate
    what changed."""
    workdir.mkdir(parents=True, exist_ok=True)
    deck, log, rc = workdir / f"{name}.spice", workdir / f"{name}.log", workdir / f"{name}.rc"
    if cache and deck.exists() and log.exists() and rc.exists() and rc.read_text().strip() == "0" \
            and deck.read_text() == txt:
        txt_log = log.read_text()
        return {"rc": 0, "meas": parse_meas(txt_log), "log": rel(log), "cached": True,
                "numerical_warnings": numerical_warnings(txt_log)}
    deck.write_text(txt)
    return run_ngspice(deck, workdir, timeout)


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
