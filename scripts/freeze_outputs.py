#!/usr/bin/env python3
"""Freeze the S0-S2 outputs that later stages read (plan v4, Phase 0; docs/plan_v4_S4_S7.md).

Writes tests/frozen/s0_s2_outputs.json: the SHA-256 of every file S3-S7 read from S0-S2 for the frozen designs, taken
at the reviewed state (tag s0s3-reviewed). tests/test_s4s5.py fails if any of them changes, so work on S3-S7 cannot
alter the reviewed S0-S2 results by accident. A deliberate change to S0-S2 is a logged decision: re-run this script
and say why in the progress log.

Frozen per design: each stage's top-level JSON (IR, reports, budgets, constraints, hierarchy, sensitivities), S0's
LVS reference netlists (ref/) and testbenches (tb/), and S2's per-layer parasitics (outputs/S2/pdk/*.json).

usage (repo root, inside layout-s0s3): python3 scripts/freeze_outputs.py [--check]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO = next(p for p in Path(__file__).resolve().parents if (p / "src").is_dir())
MANIFEST = REPO / "tests" / "frozen" / "s0_s2_outputs.json"
DESIGNS = ("example_ota_5t", "loadbench_miller")
SKIP_SUFFIXES = (".raw", ".ext")       # git-ignored simulator and extraction scratch


def frozen_files() -> list:
    files = sorted((REPO / "outputs" / "S2" / "pdk").glob("*.json"))
    for d in DESIGNS:
        for st in ("S0", "S1", "S2"):
            files += sorted((REPO / "outputs" / st / d).glob("*.json"))
        for sub in ("ref", "tb"):
            files += sorted(p for p in (REPO / "outputs" / "S0" / d / sub).rglob("*")
                            if p.is_file() and p.suffix not in SKIP_SUFFIXES)
    return files


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def changed(manifest: dict) -> list:
    """Paths whose bytes differ from the manifest, or that are missing."""
    return [rel for rel, h in manifest["sha256"].items()
            if not (REPO / rel).is_file() or sha256(REPO / rel) != h]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="compare with the manifest instead of writing it")
    a = ap.parse_args(argv)
    if a.check:
        bad = changed(json.loads(MANIFEST.read_text()))
        print("\n".join(bad) if bad else "S0-S2 outputs unchanged")
        return 1 if bad else 0
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    m = {"note": "SHA-256 of the S0-S2 files later stages read, at tag s0s3-reviewed (scripts/freeze_outputs.py)",
         "designs": list(DESIGNS),
         "sha256": {p.relative_to(REPO).as_posix(): sha256(p) for p in frozen_files()}}
    MANIFEST.write_text(json.dumps(m, indent=1) + "\n")
    print(f"{MANIFEST.relative_to(REPO)}: {len(m['sha256'])} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
