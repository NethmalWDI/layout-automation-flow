"""S1 step 1 — DC operating point of every transistor from ngspice (BSIM4 instance parameters).

The OP deck is the S0-patched OP testbench (same conditions, same DUT text) with its .control
block replaced by `op` and one `echo` per device parameter. Instance path in the testbench:
x1 (dut_amp) -> xdut (DUT) -> x<dev> (PDK subckt) -> m<model> (BSIM4 device).
"""
from __future__ import annotations

import re
from pathlib import Path

from src.common.tools import bench, run_ngspice

ESSENTIAL = ["id", "vgs", "vds", "vbs", "vth", "vdsat", "gm", "gds", "gmbs",
             "cgg", "cgd", "cgs", "cgb", "cdg", "cdd", "cds", "cdb", "csg", "csd", "css", "csb",
             "cbg", "cbd", "cbs", "cbb", "capbd", "capbs", "cgso", "cgdo", "cgbo"]
OPTIONAL = ["weff", "leff"]   # reported if the model exposes them
PARAMS = ESSENTIAL + OPTIONAL


# PDK passives: (element letter, inner element of the model subckt, instance parameter)
PASSIVE_INNER = {"sky130_fd_pr__cap_mim_m3_1": ("c", "c1", "capacitance"),
                 "sky130_fd_pr__cap_mim_m3_2": ("c", "c1", "capacitance"),
                 "sky130_fd_pr__res_generic_po": ("r", "rsky130_fd_pr__res_generic_po", "resistance")}


def inst_path(dev: str, model: str, top: str = "x1.xdut") -> str:
    return f"m.{top}.{dev.lower()}.m{model.lower()}"


def op_deck(s0_op_deck: Path, devices: list, paths: dict | None = None, passives: list | None = None) -> str:
    """paths: optional {device: instance path} for devices that are not plain PDK instances (S3 puts an
    extracted device cell in their place; one finger is then probed)."""
    txt = s0_op_deck.read_text()
    lines = ["set numdgt=12", "op"]
    for d in devices:
        ip = (paths or {}).get(d["name"]) or inst_path(d["name"], d["model"])
        for p in PARAMS:  # one vector per value: a failed read cannot leave a previous value behind
            v = f"s1_{d['name'].lower()}_{p}"
            lines.append(f"let {v} = @{ip}[{p}]")
            lines.append(f"echo OPV {d['name']} {p} $&{v}")
    for c in passives or []:
        if c.get("model", "ideal") == "ideal":
            continue
        if c["model"] not in PASSIVE_INNER:
            raise RuntimeError(f"no simulator path known for PDK passive model {c['model']}")
        letter, inner, prm = PASSIVE_INNER[c["model"]]
        v = f"s1p_{c['name'].lower()}"
        lines.append(f"let {v} = @{letter}.x1.xdut.{c['name'].lower()}.{inner}[{prm}]")
        lines.append(f"echo OPP {c['name']} $&{v}")
    lines.append("let s1i = i(vsup)")     # supply source and output node names of the diso testbenches
    lines.append("echo OPI isup $&s1i")
    # signal output at DC: v(OUT) (diso benches) or v(OUTP) - v(OUTN) (dido benches)
    if re.search(r"^x1\s+\S+\s+\S+\s+OUTN\s", txt, re.M | re.I):
        lines.append("let s1o = v(OUTP) - v(OUTN)")
        lines.append("let s1cm = (v(OUTP) + v(OUTN)) / 2")
        lines.append("echo OPI voutcm $&s1cm")
    else:
        lines.append("let s1o = v(OUT)")
    lines.append("echo OPI vout $&s1o")
    lines.append("quit 0")
    ctrl = ".control\n" + "\n".join(lines) + "\n.endc"
    out, n = re.subn(r"\.control.*?\.endc", lambda _: ctrl, txt, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError("OP deck has no .control block")
    return out


def run(s0_dir: Path, ir: dict, work: Path) -> dict:
    deck = work / "op_extract.spice"
    work.mkdir(parents=True, exist_ok=True)
    deck.write_text(op_deck(bench(s0_dir / "tb", "OP"), ir["devices"], passives=ir.get("passives")))
    r = run_ngspice(deck, work)
    log = (work / "op_extract.log").read_text()
    vals: dict = {}
    for m in re.finditer(r"^OPV (\S+) (\S+) (\S+)", log, re.M):
        try:
            vals.setdefault(m.group(1), {})[m.group(2)] = float(m.group(3))
        except ValueError:
            vals.setdefault(m.group(1), {})[m.group(2)] = None
    pas = {}
    for c in ir.get("passives", []):
        m_ = re.search(rf"^OPP {re.escape(c['name'])} (\S+)", log, re.M)
        if m_:
            mult = float(c.get("params", {}).get("M", 1))   # ngspice instance multiplier of the PDK subckt
            try:
                pas[c["name"]] = float(m_.group(1)) * mult
            except ValueError:
                pas[c["name"]] = None
    isup = re.search(r"^OPI isup (\S+)", log, re.M)
    errors = [ln for ln in log.splitlines() if re.search(r"error|no such vector|not found", ln, re.I)]
    names = [d["name"] for d in ir["devices"]]
    missing = [(d, p) for d in names for p in ESSENTIAL if vals.get(d, {}).get(p) is None]
    missing_opt = [(d, p) for d in names for p in OPTIONAL if vals.get(d, {}).get(p) is None]
    return {"rc": r["rc"], "log": r["log"], "devices": vals, "passives": pas,
            "isup_A": abs(float(isup.group(1))) if isup else None,
            "missing": missing, "missing_optional": missing_opt, "log_errors": errors[:20],
            "numerical_warnings": r.get("numerical_warnings", [])}


def apply_passives(ir: dict, op_json: dict) -> dict:
    """Give the IR's PDK passives the value S1 read from the simulator (operating_point.json)."""
    vals = op_json.get("passives") or {}
    for c in ir.get("passives", []):
        if c.get("model", "ideal") != "ideal" and vals.get(c["name"]) is not None:
            c["value"] = vals[c["name"]]
    return ir


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
