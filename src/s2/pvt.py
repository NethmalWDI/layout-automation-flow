"""S2 extension (plan v2): budget constraints at every PVT point, not only at the nominal one.

For each PVT point of S0 (outputs/S0/<design>/pvt.json) where the sized circuit meets a spec, the margin
there and the rates there define one more constraint per spec:  sum_k a_ik(p) x_k <= eta * m_i(p).
  * operating point at p: the S0 OP bench with p's corner, VDD and temperature (one ngspice run);
  * capacitance rates at p: the exact linear model at that operating point (linear.FastModel, a +-1 fF
    central difference with root finding at the unity-gain frequency);
  * resistance rates at p: S2's nominal rate (SPICE-based where S1 measured it) scaled by the ratio of the
    linear model's rate at p to its nominal rate (the bias-shift part is assumed to scale the same way:
    ASSUMPTION), or the linear rate at p when the nominal linear rate is zero.
Points where the circuit already misses a spec before layout give no constraint for that spec (no budget
can exist there) and are reported. Gain, GBW and PM only (noise and DC headroom stay nominal).
"""
from __future__ import annotations

import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.common.tools import bench, run_ngspice_text
from src.s0.pvt import with_conditions
from src.s1 import linear, op as opmod
from src.s2 import budgets as B

SPECS_PVT = ("gain_db", "gbw_mhz", "pm_deg")


def corner_ops(s0: Path, ir: dict, points: dict, work: Path, workers: int = 4) -> dict:
    src = bench(s0 / "tb", "OP")
    txt0 = src.read_text()
    jobs = []
    for pid, p in points.items():
        d = work / pid
        d.mkdir(parents=True, exist_ok=True)
        f = d / "op_src.spice"
        f.write_text(with_conditions(txt0, p["corner"], p["vdd"], p["temp"]))
        jobs.append((pid, opmod.op_deck(f, ir["devices"], passives=ir.get("passives")), d))

    def one(j):
        pid, txt, d = j
        r = run_ngspice_text(txt, d, "op", cache=False)
        vals: dict = {}
        log = (d / "op.log").read_text() if (d / "op.log").exists() else ""
        for m in re.finditer(r"^OPV (\S+) (\S+) (\S+)", log, re.M):
            try:
                vals.setdefault(m.group(1), {})[m.group(2)] = float(m.group(3))
            except ValueError:
                pass
        pas = {}
        for c in ir.get("passives", []):
            m_ = re.search(rf"^OPP {re.escape(c['name'])} (\S+)", log, re.M)
            if m_:
                try:
                    pas[c["name"]] = opmod.passive_value(c, float(m_.group(1)))
                except ValueError:
                    pass
        ok = r["rc"] == 0 and all(dd["name"] in vals and all(vals[dd["name"]].get(k) is not None for k in opmod.ESSENTIAL)
                                  for dd in ir["devices"])
        return pid, ({"devices": vals, "passives": pas} if ok else None)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        return dict(ex.map(one, jobs))


def constraints(ir: dict, s0: Path, elements: list, nominal_rates: dict, eta: float, drive: dict, work: Path,
                workers: int = 4) -> dict:
    pv = json.loads((s0 / "pvt.json").read_text())
    pts = pv["points"]
    ops = corner_ops(s0, ir, pts, work, workers)
    kinds = {k: v["kind"] for k, v in ir["margins"].items()}
    lm0 = linear.LinearModel(ir, json.loads((s0.parent.parent / "S1" / ir["design"] / "operating_point.json")
                                            .read_text())["devices"], drive=drive)
    fm0 = linear.FastModel(lm0)
    lin_nom_r = {}
    for e in elements:
        if e["kind"] == "terminal_resistance":
            mem = [m.split(".") for m in e["targets"]]
            p_ = fm0.delta_lm(linear.LinearModel(ir, lm0_op(s0, ir), drive=drive, extra_r=[(d, t, 5.0) for d, t in mem]))
            m_ = fm0.delta_lm(linear.LinearModel(ir, lm0_op(s0, ir), drive=drive, extra_r=[(d, t, -5.0) for d, t in mem]))
            lin_nom_r[e["id"]] = {k: None if p_[k] is None or m_[k] is None else (p_[k] - m_[k]) / 10.0 for k in p_}
    out, skipped, failed = [], {}, []

    def per_point(pid):
        import copy
        p = pts[pid]
        opj = ops.get(pid)
        if opj is None or "AC" in p.get("failed", []):   # a failed NOISE run alone does not drop the point
            return pid, None
        op_p = opj["devices"]
        ir_p = opmod.apply_passives(copy.deepcopy(ir), opj)   # PDK resistor/capacitor values at this point
        fm = linear.FastModel(linear.LinearModel(ir_p, op_p, drive=drive))
        rates = {}
        for e in elements:
            if e["kind"] == "terminal_resistance":
                mem = [m.split(".") for m in e["targets"]]
                p_ = fm.delta_lm(linear.LinearModel(ir_p, op_p, drive=drive, extra_r=[(d, t, 5.0) for d, t in mem]))
                m_ = fm.delta_lm(linear.LinearModel(ir_p, op_p, drive=drive, extra_r=[(d, t, -5.0) for d, t in mem]))
                lin = {k: None if p_[k] is None or m_[k] is None else (p_[k] - m_[k]) / 10.0 for k in p_}
                r = {}
                for k in SPECS_PVT:
                    ln, l0 = lin.get(k), lin_nom_r[e["id"]].get(k)
                    nom_used = nominal_rates[e["id"]].get(k, 0.0)
                    if ln is None:
                        r[k] = None
                        continue
                    # additive rule (review item 9): the nominal rate S2 uses (SPICE-based where S1 measured it)
                    # plus the change of the linear-model rate from nominal to this point
                    hk = lambda v: B.harmful_rate(kinds.get(k, "min"), v)  # noqa: E731
                    r[k] = max(0.0, nom_used + hk(ln) - hk(l0 if l0 is not None else 0.0))
                rates[e["id"]] = r
            else:
                a_, b_ = (e["targets"] + [None])[:2]
                rc = fm.rates_c(a_, b_)
                rates[e["id"]] = {k: (None if rc.get(k) is None else B.harmful_rate(kinds.get(k, "min"), rc[k]))
                                  for k in SPECS_PVT}
        return pid, {"rates": rates, "fast_base": fm.base}

    with ThreadPoolExecutor(max_workers=workers) as ex:
        res = dict(ex.map(per_point, sorted(pts)))
    for pid, r in res.items():
        if r is None:
            failed.append(pid)
            continue
        for k in SPECS_PVT:
            if k not in ir["margins"]:
                continue
            m = pts[pid]["margin"].get(k)
            if m is None or m <= 0:
                skipped.setdefault(pid, []).append(k)
                continue
            if any(r["rates"][e["id"]].get(k) is None for e in elements):
                # no rate (e.g. no unity-gain crossing in the linear model): never a vacuous constraint (item 8)
                skipped.setdefault(pid, []).append(f"{k} (no linear-model rate)")
                continue
            out.append({"id": f"{k}@{pid}", "spec": k, "point": pid, "b": eta * m, "margin": m,
                        "units": ir["margins"][k].get("units"),
                        "a": {e["id"]: r["rates"][e["id"]].get(k, 0.0) for e in elements}})
    return {"constraints": out, "skipped_spec_not_met": skipped, "op_failed": failed,
            "points": len(pts), "linear_at_points": {pid: r["fast_base"] for pid, r in res.items() if r}}


_OP_CACHE: dict = {}


def lm0_op(s0: Path, ir: dict) -> dict:
    key = str(s0)
    if key not in _OP_CACHE:
        _OP_CACHE[key] = json.loads((s0.parent.parent / "S1" / ir["design"] / "operating_point.json").read_text())["devices"]
    return _OP_CACHE[key]
