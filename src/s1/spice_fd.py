"""S1 step 3 — ground truth: finite differences on the transistor-level testbench.

A capacitor Cpar is added inside the DUT subcircuit (to ground = the DUT's VSS, or between two
nets), the unmodified AC testbench is re-run, and the slope (M(delta) - M(0)) / delta is taken
for two step sizes. Agreement between the two step sizes shows how linear the response is.
"""
from __future__ import annotations

import re
from pathlib import Path

from src.common.tools import run_ngspice


def deck_with_cap(s0_ac_deck: Path, dut: str, a: str, b: str | None, c_ff: float, gnd: str = "VSS") -> str:
    txt = s0_ac_deck.read_text()
    pat = re.compile(rf"^(\.subckt\s+{re.escape(dut)}\b[^\n]*\n)", re.M)
    if not pat.search(txt):
        raise RuntimeError(f"DUT {dut} not found in {s0_ac_deck}")
    line = f"Cpar_s1 {a} {b or gnd} {c_ff}f\n"
    return pat.sub(lambda m: m.group(1) + line, txt, count=1)


def run_fd(s0_dir: Path, dut: str, cases: list, deltas_ff: list, work: Path) -> dict:
    """cases: [(label, a, b_or_None)] using DUT-internal net names."""
    ac = s0_dir / "tb" / "diso_amp_AC.spice"
    base = run_ngspice(ac, work / "base")["meas"]
    out = {"base": base, "cases": {}}
    for label, a, b in cases:
        res = {}
        for dl in deltas_ff:
            deck = work / f"fd_{label.replace('~', '_')}_{dl:g}f.spice"
            deck.write_text(deck_with_cap(ac, dut, a, b, dl))
            m = run_ngspice(deck, work)["meas"]
            res[f"{dl:g}fF"] = {"meas": m, "slope_per_fF": {k: (None if m.get(k) is None or base.get(k) is None
                                                               else (m[k] - base[k]) / dl)
                                                            for k in ("gain_db", "gbw_mhz", "pm_deg")}}
        out["cases"][label] = res
    return out
