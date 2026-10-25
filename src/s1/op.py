"""S1 step 1 — DC operating point of every transistor from ngspice (BSIM4 instance parameters).

The OP deck is the S0-patched OP testbench (same conditions, same DUT text) with its .control
block replaced by `op` and one `echo` per device parameter. Instance path in the testbench:
x1 (dut_amp) -> xdut (DUT) -> x<dev> (PDK subckt) -> m<model> (BSIM4 device).
"""
from __future__ import annotations

import re
from pathlib import Path

from src.common.tools import run_ngspice

ESSENTIAL = ["id", "vgs", "vds", "vbs", "vth", "vdsat", "gm", "gds", "gmbs",
             "cgg", "cgd", "cgs", "cgb", "cdg", "cdd", "cds", "cdb", "csg", "csd", "css", "csb",
             "cbg", "cbd", "cbs", "cbb", "capbd", "capbs"]
OPTIONAL = ["cgso", "cgdo", "cgbo", "weff", "leff"]   # reported if the model exposes them
PARAMS = ESSENTIAL + OPTIONAL


def inst_path(dev: str, model: str, top: str = "x1.xdut") -> str:
    return f"m.{top}.{dev.lower()}.m{model.lower()}"


def op_deck(s0_op_deck: Path, devices: list) -> str:
    txt = s0_op_deck.read_text()
    lines = ["set numdgt=12", "op"]
    for d in devices:
        ip = inst_path(d["name"], d["model"])
        for p in PARAMS:
            lines.append(f"let s1v = @{ip}[{p}]")
            lines.append(f"echo OPV {d['name']} {p} $&s1v")
    lines.append("let s1i = i(vsup)")
    lines.append("echo OPI isup $&s1i")
    lines.append("quit 0")
    ctrl = ".control\n" + "\n".join(lines) + "\n.endc"
    out, n = re.subn(r"\.control.*?\.endc", lambda _: ctrl, txt, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError("OP deck has no .control block")
    return out


def run(s0_dir: Path, ir: dict, work: Path) -> dict:
    deck = work / "op_extract.spice"
    work.mkdir(parents=True, exist_ok=True)
    deck.write_text(op_deck(s0_dir / "tb" / "diso_amp_OP.spice", ir["devices"]))
    r = run_ngspice(deck, work)
    log = (work / "op_extract.log").read_text()
    vals: dict = {}
    for m in re.finditer(r"^OPV (\S+) (\S+) (\S+)", log, re.M):
        try:
            vals.setdefault(m.group(1), {})[m.group(2)] = float(m.group(3))
        except ValueError:
            vals.setdefault(m.group(1), {})[m.group(2)] = None
    isup = re.search(r"^OPI isup (\S+)", log, re.M)
    names = [d["name"] for d in ir["devices"]]
    missing = [(d, p) for d in names for p in ESSENTIAL if vals.get(d, {}).get(p) is None]
    missing_opt = [(d, p) for d in names for p in OPTIONAL if vals.get(d, {}).get(p) is None]
    return {"rc": r["rc"], "log": r["log"], "devices": vals,
            "isup_A": abs(float(isup.group(1))) if isup else None,
            "missing": missing, "missing_optional": missing_opt}


def cap_convention(dev: dict) -> dict:
    """ngspice BSIM4 reports the intrinsic matrix as C_ij = dQ_i/dV_j. Charge conservation then
    makes every row and every column sum to zero. Check it (evidence for the linear model)."""
    rows = {i: sum(dev[f"c{i}{j}"] for j in "gdsb") for i in "gdsb"}
    cols = {j: sum(dev[f"c{i}{j}"] for i in "gdsb") for j in "gdsb"}
    scale = max(abs(dev["cgg"]), 1e-30)
    worst = max(abs(v) for v in list(rows.values()) + list(cols.values())) / scale
    return {"row_sums_F": rows, "col_sums_F": cols, "worst_rel_to_cgg": worst,
            "derivative_convention": worst < 1e-3}


def saturation(dev: dict, polarity: str) -> dict:
    vds, vdsat = dev["vds"], dev["vdsat"]
    margin = (abs(vds) - abs(vdsat))
    return {"vds": vds, "vdsat": vdsat, "vds_minus_vdsat_V": margin, "saturated": margin > 0}
