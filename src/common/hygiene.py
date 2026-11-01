"""Run hygiene shared by the stages (Plan v3 Phase A, step 2; flow record 7.1, rows 40 and 43).

Exit codes of a stage's main:
  EXIT_PASS       0  every gate passed
  EXIT_GATE_FAIL  3  the stage finished and wrote its report, but a gate failed
  any other code     an error: Python itself exits with 1 on an uncaught exception
In plan v2 a gate FAIL and a crash both exited with 1, so a crashed run could be taken for a finished one.

A run of S2 or S3 carries a run_id (ISO time + 8 hex characters) in every JSON it writes, and starts from a clean
output folder: the files of the run before are moved to `<folder>.prev/`, never mixed with the new ones.
"""
from __future__ import annotations

import datetime as dt
import secrets
import shutil
from pathlib import Path

EXIT_PASS = 0
EXIT_GATE_FAIL = 3


def gate_exit(all_pass: bool) -> int:
    """The exit code of a stage that finished: PASS or gate FAIL."""
    return EXIT_PASS if all_pass else EXIT_GATE_FAIL


def new_run_id() -> str:
    """ISO time to the second plus 8 hex characters, e.g. 2026-11-01T16:30:05-3fa9c2d1."""
    return f"{dt.datetime.now().isoformat(timespec='seconds')}-{secrets.token_hex(4)}"


def fresh_output_dir(out: Path, keep: tuple = ()) -> Path | None:
    """Move what an earlier run left in `out` to `<out>.prev/` (an earlier .prev is replaced), so the new run
    starts from an empty folder. Entries named in `keep` (caches that are reused on purpose) stay in place.
    Returns the .prev folder, or None when `out` did not exist."""
    prev = out.with_name(out.name + ".prev")
    if not out.exists():
        out.mkdir(parents=True)
        return None
    if prev.exists():
        shutil.rmtree(prev)
    if not keep:
        out.rename(prev)
        out.mkdir()
        return prev
    prev.mkdir()
    for p in list(out.iterdir()):
        if p.name not in keep:
            p.rename(prev / p.name)
    return prev
