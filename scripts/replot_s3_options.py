#!/usr/bin/env python3
"""Redraw outputs/S3/<design>/plots/option_space.png from the run's saved files (S0's circuit_ir.json, S3's
option_table.json and device_decisions.json), with the same function the S3 run uses. Nothing is simulated and
no other output changes, so a committed run keeps its results and ids.

usage (inside layout-s0s3, repo root): python3 scripts/replot_s3_options.py [design ...]
default designs: example_ota_5t loadbench_miller
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = next(p for p in Path(__file__).resolve().parents if (p / "src").is_dir())
sys.path.insert(0, str(REPO))

from src.s3 import options as O  # noqa: E402
from src.s3.run import plot_option_space  # noqa: E402


def replot(design: str) -> Path:
    s3 = REPO / "outputs" / "S3" / design
    ir = json.loads((REPO / "outputs" / "S0" / design / "circuit_ir.json").read_text())
    table = json.loads((s3 / "option_table.json").read_text())["options"]
    dd = json.loads((s3 / "device_decisions.json").read_text())
    out = s3 / "plots" / "option_space.png"
    plot_option_space(out, table, O.device_types(ir), dd["decisions"], dd["mode"])
    return out


def main(argv=None) -> int:
    for d in (argv if argv is not None else sys.argv[1:]) or ["example_ota_5t", "loadbench_miller"]:
        print(replot(d))
    return 0


if __name__ == "__main__":
    sys.exit(main())
