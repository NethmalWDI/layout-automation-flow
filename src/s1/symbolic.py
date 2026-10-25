"""S1 step 4 — evaluate the upstream (stage-1) symbolic hierarchy with real operating-point values.

The upstream equations (5t-ota_differential_equations.json) express level-2 amplifier elements in
level-1 primitive elements, and those in level-0 transistor elements (C1..C5, G1, R1 of
mosfet-ssm). Level-0 values come from this OP through the S0 name map:
  C1 = gate-bulk, C2 = gate-source, C3 = gate-drain, C4 = drain-bulk, C5 = source-bulk  (intrinsic
  magnitude + overlap/junction), G1 = gm, G2 = gmbs, R1 = 1/gds.
The closed-form gain/GBW/PM are then compared with SPICE, and d(spec)/d(CL) is taken symbolically.
Known upstream limitations (stage-1 README) are expected to show up here: tail treated as a virtual
ground, and no Ioutn->Ioutp coupling in the level-2 template (mirror pole missing -> PM optimistic,
zero sensitivity to the mirror node).
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp
import yaml


def level0_values(op: dict, name_map: dict) -> dict:
    vals = {}
    for up, tgt in name_map["devices"].items():
        if tgt is None or tgt not in op:
            continue
        o = op[tgt]
        vals.update({
            f"C1_{up}": abs(o["cgb"]) + o["cgbo"],
            f"C2_{up}": abs(o["cgs"]) + o["cgso"],
            f"C3_{up}": abs(o["cgd"]) + o["cgdo"],
            f"C4_{up}": o["capbd"] + abs(o["cbd"]),
            f"C5_{up}": o["capbs"] + abs(o["cbs"]),
            f"G1_{up}": o["gm"], f"G2_{up}": o["gmbs"], f"R1_{up}": 1.0 / o["gds"],
        })
    return vals


def collect_values(node: dict, acc: dict) -> None:
    for k, v in node.items():
        if isinstance(v, dict):
            if "values" in v and isinstance(v["values"], dict):
                for sym, expr in v["values"].items():
                    if expr is not None and sym != expr:
                        acc[sym] = expr
            collect_values(v, acc)


def evaluate(eq_path: Path, name_map_path: Path, op: dict, CL: float) -> dict:
    eq = json.loads(Path(eq_path).read_text())
    nm = yaml.safe_load(Path(name_map_path).read_text())
    defs: dict = {}
    collect_values(eq, defs)
    perf = eq["performance"]
    sy = {k: sp.Symbol(k) for k in set(defs) | set(level0_values(op, nm))}
    sy["CL"] = sp.Symbol("CL")
    loc = {**sy, "oo": sp.oo, "pi": sp.pi, "Abs": sp.Abs, "log": sp.log, "atan": sp.atan, "sqrt": sp.sqrt}
    exprs = {k: sp.sympify(v, locals=loc) for k, v in defs.items()}

    def down(e, depth=0):
        for _ in range(6):  # three levels; a few passes resolve everything
            e2 = e.xreplace({sy[k]: exprs[k] for k in exprs if sy.get(k) is not None and sy[k] in e.free_symbols})
            if e2 == e:
                break
            e = e2
        return e

    terms = {k: sp.sympify(v, locals=loc) for k, v in perf["terms"].items()}
    A0 = down(terms["A0"])
    wgbw = down(terms["wgbw"])
    kft = down(terms["kft"])
    wu = wgbw * sp.sqrt((1 - 1 / A0 ** 2) / (1 - kft ** 2))
    gain_db = 20 * sp.log(sp.Abs(A0)) / sp.log(10)
    gbw_mhz = wu / (2e6 * sp.pi)
    pm = down(sp.sympify(perf["pm_deg"], locals={**loc, "wu": sp.Symbol("wu")}))
    pm = pm.xreplace({sp.Symbol("wu"): wu})
    num = {sy[k]: v for k, v in level0_values(op, nm).items() if k in sy}
    num[sy["CL"]] = CL
    res, sens = {}, {}
    for name, e in (("gain_db", gain_db), ("gbw_mhz", gbw_mhz), ("pm_deg", pm)):
        res[name] = float(sp.N(e.xreplace(num)))
        sens[name] = float(sp.N(sp.diff(e, sy["CL"]).xreplace(num))) * 1e-15  # per fF
    missing = sorted(str(s) for e in (gain_db, gbw_mhz, pm) for s in e.free_symbols if s not in num)
    return {"predicted": res, "d_dCL_per_fF": sens, "unresolved_symbols": sorted(set(missing)),
            "level0_values": {k: v for k, v in level0_values(op, nm).items()},
            "expressions_level2": {k: str(v) for k, v in perf["terms"].items()},
            "note": ("Output-node capacitance enters as CL. The mirror node (net0 upstream = net3 here) has no "
                     "element in the level-2 performance expressions, so its symbolic sensitivity is 0 by "
                     "construction (upstream limitation).")}
