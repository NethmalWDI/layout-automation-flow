"""S1 step 3 — ground truth: finite differences on the transistor-level testbench.

A capacitor Cpar is added inside the DUT subcircuit (to ground = the DUT's VSS, or between two
nets), the unmodified AC testbench is re-run, and the slope (M(delta) - M(0)) / delta is taken
for two step sizes. Agreement between the two step sizes shows how linear the response is.
"""
from __future__ import annotations

import re
from pathlib import Path

from src.common.tools import run_ngspice, run_ngspice_text


def deck_with_cap(s0_ac_deck: Path, dut: str, a: str, b: str | None, c_ff: float, gnd: str = "VSS") -> str:
    txt = s0_ac_deck.read_text()
    pat = re.compile(rf"^(\.subckt\s+{re.escape(dut)}\b[^\n]*\n)", re.M)
    if not pat.search(txt):
        raise RuntimeError(f"DUT {dut} not found in {s0_ac_deck}")
    line = f"Cpar_s1 {a} {b or gnd} {c_ff}f\n"
    return pat.sub(lambda m: m.group(1) + line, txt, count=1)


def run_fd(s0_dir: Path, dut: str, cases: list, deltas_ff: list, work: Path, workers: int = 4,
           gnd: str = "VSS") -> dict:
    """cases: [(label, a, b_or_None)] using DUT-internal net names. Independent runs, thread pool;
    each run has its own folder (ngspice writes rawspice.raw into its cwd)."""
    from concurrent.futures import ThreadPoolExecutor
    ac = s0_dir / "tb" / "diso_amp_AC.spice"
    jobs = [("base", None, ac.read_text(), work / "base")]
    for label, a, b in cases:
        for dl in deltas_ff:
            jobs.append((label, dl, deck_with_cap(ac, dut, a, b, dl, gnd), work / f"{label.replace('~', '_')}_{dl:g}f"))

    def one(job):
        _, _, txt, wd = job
        r = run_ngspice_text(txt, wd, "ac")
        if r["rc"] != 0 or r.get("numerical_warnings"):
            raise RuntimeError(f"ngspice run in {wd} failed or reported numerical trouble")
        return r["meas"]

    with ThreadPoolExecutor(max_workers=workers) as ex:
        res = list(ex.map(one, jobs))
    base = res[0]
    out = {"base": base, "cases": {}}
    for (label, dl, _, _), m in zip(jobs[1:], res[1:]):
        out["cases"].setdefault(label, {})[f"{dl:g}fF"] = {
            "meas": m, "slope_per_fF": {k: (None if m.get(k) is None or base.get(k) is None else (m[k] - base[k]) / dl)
                                        for k in ("gain_db", "gbw_mhz", "pm_deg")}}
    return out
