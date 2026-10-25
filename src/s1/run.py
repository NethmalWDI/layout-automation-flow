#!/usr/bin/env python3
"""S1 — electrical intent: which node moves which spec, by how much, and why.

usage (inside layout-s0s3):  python3 -m src.s1.run inputs/example_ota_5t/package.yaml [--no-fd]

Inputs : outputs/S0/<design>/{circuit_ir.json, tb/*.spice}, upstream equations + name map (package)
Outputs: outputs/S1/<design>/
  operating_point.json   per-device OP (gm, gds, gmbs, caps, Id, Vds, Vdsat, region)
  linear_model.json      exact small-signal model check vs SPICE (gain, GBW, PM)
  symbolic_check.json    upstream hierarchical equations evaluated with this OP, vs SPICE
  sensitivity.json       per net / net pair: d(spec)/dC [per fF] from the linear model, the
                         symbolic model (where it has a symbol) and transistor-level SPICE;
                         plus 'fF that would consume the whole margin'
  node_classes.json      dominant / non-dominant pole nodes, high-Z, mirror, tail, bias, supply
  currents.json          device and per-net branch currents (input to EM width rules in S2)
  intent.json            matching groups and ranked critical nets with evidence
  plots/*.png            Bode (linear model vs SPICE) and sensitivity comparison
  s1_report.json         gates G1.x with evidence
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

from src.common.tools import REPO, provenance, rel, run_ngspice, write_json
from src.s0.ingest import load_package
from src.s1 import linear, op as opmod, resistance, spice_fd, symbolic

TOL = {"gain_db": 0.2, "gbw_rel": 0.03, "pm_deg": 2.0}      # linear model vs SPICE (G1.2)
SENS_TOL_REL = 0.20                                         # linear vs SPICE slope (G1.3 a)
PRED_TOL_MARGIN = 0.05                                      # prediction error at +20 fF / margin (G1.3 b)


def spice_bode(s0: Path, work: Path) -> tuple:
    """Re-run the S0 AC deck with a wrdata of v(OUT) to get the transistor-level Bode curve."""
    txt = (s0 / "tb" / "diso_amp_AC.spice").read_text()
    if "  write\n" not in txt:
        raise RuntimeError("AC deck has no '  write' line to anchor wrdata")
    txt = txt.replace("  write\n", "  wrdata bode_spice.txt v(OUT)\n  write\n", 1)
    work.mkdir(parents=True, exist_ok=True)
    deck = work / "bode_ac.spice"
    deck.write_text(txt)
    run_ngspice(deck, work)
    d = np.loadtxt(work / "bode_spice.txt")
    return d[:, 0], d[:, 1] + 1j * d[:, 2]


def ac_drive(s0: Path, ir: dict) -> dict:
    """AC stimulus of each DUT input, read from the AC testbench (V<name> <node> 0 ... ac <value>)."""
    txt = (s0 / "tb" / "diso_amp_AC.spice").read_text()
    tb = {}
    for m in re.finditer(r"^V\S*\s+(\S+)\s+(0|gnd)\s+.*?\bac\s+([-+0-9.eE]+)", txt, re.M | re.I):
        tb[m.group(1)] = float(m.group(3))
    drive = {p["name"]: tb[p["testbench_port"]] for p in ir["ports"]
             if p["role"] == "input" and p.get("testbench_port") in tb}
    if len(drive) != len([p for p in ir["ports"] if p["role"] == "input"]):
        raise RuntimeError(f"could not read the AC drive of every input from the AC deck: {drive}")
    return drive


def classify_nodes(ir: dict, lm: linear.LinearModel) -> dict:
    R = lm.dc_node_resistance()
    C = lm.node_capacitance()
    tau = {n: R[n] * C[n] for n in R}
    order = sorted(tau, key=tau.get, reverse=True)
    roles = {p["name"]: p["role"] for p in ir["ports"]}
    diode = {d["terminals"]["d"] for d in ir["devices"] if d["terminals"]["d"] == d["terminals"]["g"]}
    tails = {}
    for d in ir["devices"]:
        tails.setdefault(d["terminals"]["s"], []).append(d["name"])
    rmax = max(R.values())
    out = {}
    for n in ir["nets"]:
        name = n["name"]
        tags = []
        if roles.get(name) in ("supply", "ground"):
            tags.append(roles[name])
        if roles.get(name) == "input":
            tags.append("signal_input")
        if roles.get(name) == "output":
            tags.append("signal_output")
        if any(s["p"] == name for s in ir.get("internal_sources", [])):
            tags.append("bias (ideal source in the testbench: AC ground, ASSUMPTION)")
        if name in diode:
            tags.append("mirror_node (diode-connected)")
        if name in tails and len(tails[name]) >= 2 and roles.get(name) is None:
            tags.append("source_coupled (tail)")
        rec = {"tags": tags}
        if name in tau:
            rec.update({"R_dc_ohm": R[name], "C_node_F": C[name], "tau_s": tau[name],
                        "pole_estimate_Hz": 1 / (2 * math.pi * tau[name]) if tau[name] > 0 else None,
                        "high_impedance": R[name] >= 0.1 * rmax})
            rank = order.index(name)
            rec["pole_rank"] = rank + 1
            if rank == 0:
                tags.append("dominant_pole")
            elif rank == 1:
                tags.append("non_dominant_pole")
        out[name] = rec
    return {"nodes": out, "method": "open-circuit time constants R_dc*C_node from the linear model; "
                                     "structural tags from topology"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package")
    ap.add_argument("--no-fd", action="store_true", help="skip transistor-level finite differences")
    a = ap.parse_args(argv)
    pkg = load_package(REPO / a.package)
    design = pkg["design"]
    s0 = REPO / "outputs" / "S0" / design
    out = REPO / "outputs" / "S1" / design
    work = out / "work"
    (out / "plots").mkdir(parents=True, exist_ok=True)
    ir = json.loads((s0 / "circuit_ir.json").read_text())
    gates = {}

    # 1. operating point
    opr = opmod.run(s0, ir, work / "op")
    sat = {d["name"]: opmod.saturation(opr["devices"][d["name"]], d["type"]) for d in ir["devices"]}
    isup_ach = ir["achieved"].get("isup_ua")
    isup_ok = isup_ach is None or abs(opr["isup_A"] * 1e6 - isup_ach) <= 0.01 * isup_ach
    conv = {} if opr["missing"] else {d: opmod.cap_convention(v) for d, v in opr["devices"].items()}
    conv_ok = bool(conv) and all(c["derivative_convention"] for c in conv.values())
    gates["G1.1_operating_point"] = {"pass": opr["rc"] == 0 and not opr["missing"] and all(s["saturated"] for s in sat.values())
                                     and isup_ok and conv_ok and not opr["numerical_warnings"],
                                     "numerical_warnings": opr["numerical_warnings"],
                                     "saturation": sat, "isup_uA": opr["isup_A"] * 1e6, "isup_achieved_uA": isup_ach,
                                     "missing_params": opr["missing"], "missing_optional_params": opr["missing_optional"],
                                     "charge_conservation_worst_rel": max((c["worst_rel_to_cgg"] for c in conv.values()), default=None)}
    write_json(out / "operating_point.json", {"devices": opr["devices"], "saturation": sat, "isup_A": opr["isup_A"],
                                              "cap_matrix_check": conv, "log": opr["log"], "conditions": ir["conditions"],
                                              "convention": "BSIM4 instance values from ngspice; intrinsic C_ij = dQ_i/dV_j "
                                                            "(rows/cols sum to 0); overlap cgso/cgdo/cgbo and junction "
                                                            "capbd/capbs are separate, positive"})
    op = opr["devices"]

    # 2. linear model vs SPICE (stimulus read from the AC testbench itself)
    drive = ac_drive(s0, ir)
    lm = linear.LinearModel(ir, op, drive=drive)
    H = lm.response(linear.FREQ)
    m_lin = linear.metrics(H)
    ach = ir["achieved"]
    dl = {"gain_db": m_lin["gain_db"] - ach["gain_db"], "gbw_rel": m_lin["gbw_mhz"] / ach["gbw_mhz"] - 1,
          "pm_deg": m_lin["pm_deg"] - ach["pm_deg"]}
    lin_ok = abs(dl["gain_db"]) <= TOL["gain_db"] and abs(dl["gbw_rel"]) <= TOL["gbw_rel"] and abs(dl["pm_deg"]) <= TOL["pm_deg"]
    gates["G1.2_linear_model_vs_spice"] = {"pass": lin_ok, "linear": m_lin, "spice": {k: ach[k] for k in m_lin},
                                           "delta": dl, "tolerance": TOL}
    write_json(out / "linear_model.json", {"metrics": m_lin, "spice": {k: ach[k] for k in m_lin}, "delta": dl,
                                           "unknown_nodes": lm.unknown, "driven": lm.drive, "ac_ground": sorted(lm.ground)})
    try:
        fs, Hs = spice_bode(s0, work / "bode")
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
        ax[0].semilogx(fs, 20 * np.log10(abs(Hs)), label="transistor-level SPICE", lw=2)
        ax[0].semilogx(linear.FREQ, 20 * np.log10(abs(H)), "--", label="linear model (this S1)", lw=1.5)
        ax[1].semilogx(fs, np.degrees(np.unwrap(np.angle(Hs))), lw=2)
        ax[1].semilogx(linear.FREQ, np.degrees(np.unwrap(np.angle(H))), "--", lw=1.5)
        ax[0].set_ylabel("|H| (dB)"); ax[1].set_ylabel("phase (deg)"); ax[1].set_xlabel("frequency (Hz)")
        ax[0].axhline(0, color="grey", lw=0.5); ax[0].legend(); ax[0].grid(True, which="both", alpha=0.3); ax[1].grid(True, which="both", alpha=0.3)
        ax[0].set_title(f"{design}: open-loop response")
        fig.tight_layout(); fig.savefig(out / "plots" / "bode_linear_vs_spice.png", dpi=110); plt.close(fig)
    except Exception as e:  # plots are evidence, not a gate
        gates["G1.2_linear_model_vs_spice"]["plot_error"] = str(e)

    # 3. sensitivities: linear model (all nets and signal pairs)
    solved = lm.unknown
    signal = [n for n in solved] + list(lm.drive)
    pairs = [(x, y) for x, y in itertools.combinations(signal, 2) if x in solved or y in solved]
    sl = linear.sensitivities(ir, op, solved, pairs, drive=drive)
    # 4. symbolic (upstream) check
    up = pkg.get("upstream") or {}
    sym = None
    if up.get("equations") and up.get("name_map"):
        CL = linear.parse_si(ir["conditions"]["CL_F"])
        sym = symbolic.evaluate(REPO / up["equations"], REPO / up["name_map"], op, CL)
        sym["spice"] = {k: ach[k] for k in sym["predicted"]}
        sym["delta"] = {k: sym["predicted"][k] - ach[k] for k in sym["predicted"]}
        write_json(out / "symbolic_check.json", sym)
    # 5. transistor-level finite differences for the solved nets and the top coupling pairs
    fd = None
    if not a.no_fd:
        cases = [(n, n, None) for n in solved]
        def consume(p):  # fF of coupling that alone consumes the tightest margin (first order)
            s = sl["per_fF"][f"{p[0]}~{p[1]}"]
            v = [ir["margins"][k]["margin"] / -s[k] for k in ("gain_db", "gbw_mhz", "pm_deg")
                 if s[k] is not None and s[k] < 0 and k in ir["margins"]]
            return min(v) if v else math.inf
        top_pairs = sorted(pairs, key=consume)[:3]
        cases += [(f"{x}~{y}", x, y) for x, y in top_pairs]
        fd = spice_fd.run_fd(s0, ir["subckt"], cases, [5.0, 20.0], work / "fd",
                             gnd=next(p_["name"] for p_ in ir["ports"] if p_["role"] == "ground"))
    # assemble sensitivity table
    margins = ir["margins"]
    table = {}
    for label, s in sl["per_fF"].items():
        row = {}
        for k in ("gain_db", "gbw_mhz", "pm_deg"):
            lin_s = s[k]
            r = {"linear_per_fF": lin_s}
            if sym and label == ir["ports"][[p["role"] for p in ir["ports"]].index("output")]["name"]:
                r["symbolic_per_fF"] = sym["d_dCL_per_fF"][k]
            elif sym and label in solved:
                r["symbolic_per_fF"] = 0.0
                r["symbolic_note"] = "no element for this node in the level-2 performance expressions"
            if fd and label in fd["cases"]:
                r["spice_per_fF"] = {dd: v["slope_per_fF"][k] for dd, v in fd["cases"][label].items()}
            mg = margins.get(k, {}).get("margin")
            if lin_s and mg is not None and lin_s < 0:
                r["fF_to_consume_margin"] = mg / -lin_s
            row[k] = r
        table[label] = row
    # G1.3: linear vs SPICE agreement where the effect is measurable.
    # (a) derivative check: the linear model gives dM/dC at C=0; SPICE slopes at 5 and 20 fF are
    #     extrapolated to zero step (Richardson, slope linear in step): s0 = (4*s5 - s20)/3.
    # (b) prediction check, used when the derivative is small: the error of the first-order
    #     prediction at +20 fF, as a fraction of the spec margin (what S2 budgeting depends on).
    # Pass = (a) within SENS_TOL_REL with the same sign, or (b) within PRED_TOL_MARGIN.
    checks = []
    if fd:
        for label, res in fd["cases"].items():
            for k in ("gain_db", "gbw_mhz", "pm_deg"):
                s5 = res["5fF"]["slope_per_fF"][k]; s20 = res["20fF"]["slope_per_fF"][k]
                lin_s = table[label][k]["linear_per_fF"]
                meas_floor = {"gain_db": 1e-4, "gbw_mhz": 1e-3 * ach["gbw_mhz"] / 20, "pm_deg": 1e-3}[k]
                if s20 is None or abs(s20) * 20 < 20 * meas_floor:
                    checks.append({"case": label, "spec": k, "status": "below_resolution", "spice_20fF": s20, "linear": lin_s})
                    continue
                s0x = (4 * s5 - s20) / 3 if s5 is not None else s20
                rel_x = abs(lin_s - s0x) / abs(s0x) if (lin_s is not None and s0x) else None
                ok_a = lin_s is not None and np.sign(lin_s) == np.sign(s0x) and rel_x is not None and rel_x <= SENS_TOL_REL
                mg = margins.get(k, {}).get("margin")
                pred = abs(lin_s - s20) * 20 / mg if (lin_s is not None and mg) else None
                ok_b = pred is not None and pred <= PRED_TOL_MARGIN
                checks.append({"case": label, "spec": k, "linear": lin_s, "spice_5fF": s5, "spice_20fF": s20,
                               "spice_extrapolated_0": s0x, "rel_err_vs_extrapolated": rel_x,
                               "rel_err_vs_20fF": abs(lin_s - s20) / abs(s20),
                               "step_consistency": (abs(s5 - s20) / abs(s20) if s5 is not None else None),
                               "pred_err_at_20fF_frac_of_margin": pred,
                               "criterion": "a_derivative" if ok_a else ("b_prediction" if ok_b else None),
                               "pass": bool(ok_a or ok_b)})
    judged = [c for c in checks if "pass" in c]
    gates["G1.3_sensitivity_vs_spice"] = {"pass": (all(c["pass"] for c in judged) and bool(judged)) if fd else None,
                                          "tolerance_rel": SENS_TOL_REL, "tolerance_pred_frac_margin": PRED_TOL_MARGIN,
                                          "checks": checks}
    write_json(out / "sensitivity.json", {"units": "spec units per fF of added capacitance",
                                          "base_linear": sl["base"], "margins": margins, "table": table,
                                          "spice_fd": fd, "symbolic_available": sym is not None})
    # plot: sensitivity comparison (per spec, per case). Gain at 1 Hz does not depend on any
    # capacitance (all its sensitivities are 0), so only GBW and PM are drawn.
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        labels = [c[0] for c in (cases if fd else [(n, n, None) for n in solved])]
        ext = {(c["case"], c["spec"]): c.get("spice_extrapolated_0") for c in checks}
        fig, axs = plt.subplots(1, 2, figsize=(13, 4.4))
        for ax, k in zip(axs, ("gbw_mhz", "pm_deg")):
            x = np.arange(len(labels)); w = 0.2
            lin_v = [table[l][k]["linear_per_fF"] or 0 for l in labels]
            sp0 = [ext.get((l, k)) if ext.get((l, k)) is not None else
                   ((table[l][k].get("spice_per_fF") or {}).get("20fF") or 0) for l in labels]
            sp20 = [(table[l][k].get("spice_per_fF") or {}).get("20fF") or 0 for l in labels]
            sy_v = [table[l][k].get("symbolic_per_fF") for l in labels]
            ax.bar(x - 1.5 * w, lin_v, w, label="linear model (dM/dC at 0)")
            ax.bar(x - 0.5 * w, sp0, w, label="SPICE, slope extrapolated to 0 (5 & 20 fF)")
            ax.bar(x + 0.5 * w, sp20, w, label="SPICE, secant slope at +20 fF")
            ax.bar(x + 1.5 * w, [0 if v is None else v for v in sy_v], w, label="upstream symbolic (0 = no term)")
            ax.set_xticks(x); ax.set_xticklabels(labels, rotation=25, ha="right")
            ax.set_title(f"{design}: d({k})/dC  [{'MHz' if k == 'gbw_mhz' else 'deg'} per fF]")
            ax.axhline(0, color="grey", lw=0.5); ax.grid(True, axis="y", alpha=0.3)
        axs[0].legend(fontsize=7.5)
        fig.tight_layout(); fig.savefig(out / "plots" / "sensitivity_comparison.png", dpi=110); plt.close(fig)
    except Exception as e:
        gates["G1.3_sensitivity_vs_spice"]["plot_error"] = str(e)

    # 6. node classes, currents, intent
    nc = classify_nodes(ir, lm)
    write_json(out / "node_classes.json", nc)
    currents = {"devices": {d["name"]: {"id_A": op[d["name"]]["id"], "type": d["type"]} for d in ir["devices"]}, "nets": {}}
    for d in ir["devices"]:
        for t in ("d", "s"):
            currents["nets"].setdefault(d["terminals"][t], []).append({"device": d["name"], "terminal": t, "abs_id_A": abs(op[d["name"]]["id"])})
    roles_ = {p_["name"]: p_["role"] for p_ in ir["ports"]}
    for n, lst in currents["nets"].items():
        tot = sum(x["abs_id_A"] for x in lst)
        # a supply/ground net feeds every connected branch from outside; an internal net carries half the
        # sum of its branch currents (what enters leaves, KCL)
        trunk = tot if roles_.get(n) in ("supply", "ground") else tot / 2
        currents["nets"][n] = {"connections": lst, "max_branch_A": max(x["abs_id_A"] for x in lst),
                               "trunk_A": trunk, "trunk_rule": "sum (supply/ground)" if trunk == tot else "sum/2 (internal)"}
    write_json(out / "currents.json", currents)
    devs = {d["name"]: d for d in ir["devices"]}
    matching = []
    for b in ir["hierarchy"]["blocks"]:
        if len(b["devices"]) >= 2:
            sizes = {(devs[x]["W_um"], devs[x]["L_um"], devs[x]["nf"], devs[x]["m"]) for x in b["devices"]}
            kind = "diff_pair" if "differential" in b["primitive"] else ("mirror" if "mirror" in b["primitive"] else b["category"])
            gm = [op[x]["gm"] for x in b["devices"]]
            matching.append({"devices": b["devices"], "kind": kind, "equal_size": len(sizes) == 1,
                             "purpose": {"diff_pair": "input offset, CMRR, symmetric loading of net3/OUTP",
                                         "mirror": "current-copy accuracy (systematic offset, gain)"}.get(kind, ""),
                             "evidence": [f"hierarchy block {b['name']} ({b['source']})", f"sizes {sorted(sizes)}",
                                          f"gm spread {max(gm)/min(gm)-1:.2%}"]})
    crit, pairs_r = [], []
    for label, row in table.items():
        worst = min((v.get("fF_to_consume_margin", math.inf), k) for k, v in row.items())
        rec = {"most_limiting_spec": worst[1] if worst[0] < math.inf else None,
               "fF_to_consume_margin": worst[0] if worst[0] < math.inf else None,
               "per_fF": {k: row[k]["linear_per_fF"] for k in row}}
        if "~" in label:
            pairs_r.append({"pair": label, **rec})
        else:
            crit.append({"net": label, **rec, "classes": nc["nodes"].get(label, {}).get("tags", [])})
    key = lambda c: c["fF_to_consume_margin"] if c["fF_to_consume_margin"] is not None else math.inf  # noqa: E731
    crit.sort(key=key)
    pairs_r.sort(key=key)
    for lst in (crit, pairs_r):
        for i, c in enumerate(lst):
            c["rank"] = i + 1
    intent = {"design": design, "matching": matching, "critical_nets": crit, "coupling_pairs_ranked": pairs_r,
              "ranking": "ascending capacitance (fF, to ground for nets, between the two nets for pairs) that would "
                         "alone consume the margin of the most limiting spec, first-order (linear model)"}
    gates["G1.4_matching_groups"] = {"pass": bool(matching) and all(m["equal_size"] for m in matching),
                                     "groups": [{k: m[k] for k in ("devices", "kind", "equal_size")} for m in matching]}
    gates["G1.5_symbolic_vs_spice (reported, not gated)"] = {"pass": None, **({"predicted": sym["predicted"], "spice": sym["spice"],
                                                              "delta": sym["delta"]} if sym else {"note": "no upstream equations"})}
    # 7. series resistance at device terminals (wiring + PCell access).
    # Matched devices (diff pair, mirror) are wired symmetrically (S2 hard rule), so the resistance of a
    # matched terminal is a pair variable: the same R on both members ('XM1+XM2.s'). Its asymmetric part
    # is a different mechanism (systematic offset); it is measured separately below with one-sided
    # resistors and reported as offset per ohm, not mixed into the AC budgets.
    groups = []
    in_match = {}
    for m in matching:
        if m["equal_size"] and len(m["devices"]) == 2:
            for d_ in m["devices"]:
                in_match[d_] = m["devices"]
    seen = set()
    for d in ir["devices"]:
        if d["name"] in seen:
            continue
        mem = in_match.get(d["name"], [d["name"]])
        seen.update(mem)
        for t in ("d", "g", "s"):
            groups.append(("+".join(mem) + f".{t}", [(x, t) for x in mem]))
    slr = linear.sensitivities_r(ir, op, groups, drive=drive)
    kinds = {k: v.get("kind") for k, v in margins.items()}

    def rate(spec, slope):  # margin consumed per unit of the parasitic (only the harmful direction counts)
        if slope is None:
            return 0.0
        return max(0.0, -slope) if kinds.get(spec, "min") == "min" else max(0.0, slope)

    R_VALUES = [20.0, 100.0]
    fdr = slr_spice = fd1 = None
    single = [(f"{d['name']}.{t}", [(d["name"], t)]) for d in ir["devices"] for t in ("d", "g", "s")
              if d["name"] in in_match]
    if not a.no_fd:
        fdr = resistance.dc_and_ac(s0, ir, groups, groups, R_VALUES, work / "fd_r")
        slr_spice = resistance.slopes(fdr, R_VALUES)
        fd1 = resistance.offset_follower(s0, ir, single, [5.0, 20.0], work / "fd_offset")
    base_sat = fdr["base"]["op"]["vds_minus_vdsat_V"] if fdr else {d: sat[d]["vds_minus_vdsat_V"] for d in sat}
    a_dc = 10 ** (ach["gain_db"] / 20)
    rtable, rchecks = {}, []
    for gid, members in groups:
        row = {"members": [f"{d}.{t}" for d, t in members], "linear_per_ohm": slr["per_ohm"][gid]}
        sp = (slr_spice or {}).get(gid, {})
        for kind, name in (("ac", "spice_ac"), ("noise", "spice_noise"), ("op", "spice_dc")):
            if kind in sp:
                row[name] = sp[kind]
        # Rates used downstream: transistor-level SPICE (it contains the bias shift I*R moves the operating
        # point by, which a small-signal model at a fixed operating point cannot see); the linear model is
        # kept to tell the two mechanisms apart. Without SPICE (--no-fd) the linear model is used.
        ac0 = (sp.get("ac") or {}).get("extrapolated_0") or {}
        per = {k: (ac0.get(k) if ac0.get(k) is not None else v) for k, v in slr["per_ohm"][gid].items()}
        nz = (sp.get("noise") or {}).get("extrapolated_0") or {}
        if nz.get("vnoise_nv_rthz") is not None:
            per["vnoise_nv_rthz"] = nz["vnoise_nv_rthz"]
        row["per_ohm_used"] = per
        row["rate_source"] = "spice (extrapolated to 0 from 20 and 100 ohm)" if ac0 else "linear model"
        cons = {k: margins[k]["margin"] / rate(k, v) for k, v in per.items() if k in margins and rate(k, v) > 0}
        dc = {}
        for dd, m0 in base_sat.items():
            s_ = ((sp.get("op") or {}).get("extrapolated_0") or {}).get(f"sat_{dd}")
            if s_ is not None and s_ < 0:
                dc[f"sat_{dd}"] = {"slope_V_per_ohm": s_, "margin_V": m0, "ohm_to_consume": m0 / -s_}
                cons[f"sat_{dd}"] = m0 / -s_
        row["dc_saturation"] = dc
        row["ohm_to_consume_margin"] = min(cons.values()) if cons else None
        row["most_limiting"] = min(cons, key=cons.get) if cons else None
        rtable[gid] = row
        if "ac" in sp:  # G1.6: SPICE slopes consistent over 20..100 ohm; linear model agreement classifies
            for k in ("gbw_mhz", "pm_deg", "gain_db"):
                lin_s = slr["per_ohm"][gid][k]
                x0 = (sp["ac"]["extrapolated_0"] or {}).get(k)
                s20 = sp["ac"]["per_ohm"]["20ohm"].get(k)
                s100 = sp["ac"]["per_ohm"]["100ohm"].get(k)
                floor = {"gain_db": 1e-5, "gbw_mhz": 1e-5 * ach["gbw_mhz"], "pm_deg": 1e-4}[k]
                if x0 is None or abs(x0) < floor:
                    rchecks.append({"case": gid, "spec": k, "status": "below_resolution", "spice_extrapolated_0": x0,
                                    "linear": lin_s})
                    continue
                mg = margins.get(k, {}).get("margin")
                pred = abs(x0 - s100) * 100 / mg if mg else None          # first-order prediction at 100 ohm
                step = abs(s100 - s20) / max(abs(s20), abs(s100))
                lin_agree = (lin_s * x0 > 0) and abs(lin_s - x0) / abs(x0) <= SENS_TOL_REL
                # independent test of the model and of the mechanism: re-solve the linear model at the
                # operating point SPICE finds WITH the resistor (100 ohm) and compare the change
                c100 = fdr["cases"][gid]["100ohm"]
                opR = (c100.get("op") or {}).get("params") or {}
                sh = None
                if all(dd in opR and all(p_ in opR[dd] and opR[dd][p_] is not None for p_ in opmod.ESSENTIAL)
                       for dd in op):
                    mR = linear.evaluate(ir, opR, extra_r=[(d_, t_, 100.0) for d_, t_ in members], drive=drive)
                    d_lin = (mR[k] - m_lin[k]) if mR[k] is not None else None
                    d_sp = (c100["ac"][k] - fdr["base"]["ac"][k]) if c100.get("ac", {}).get(k) is not None else None
                    ok_sh = d_lin is not None and d_sp is not None and (
                        abs(d_lin - d_sp) <= SENS_TOL_REL * abs(d_sp) or
                        (mg and abs(d_lin - d_sp) <= PRED_TOL_MARGIN * mg))
                    sh = {"linear_at_shifted_op_change": d_lin, "spice_change": d_sp, "agree": bool(ok_sh)}
                rchecks.append({"case": gid, "spec": k, "spice_20ohm": s20, "spice_100ohm": s100,
                                "spice_extrapolated_0": x0, "step_consistency": step,
                                "pred_err_at_100ohm_frac_of_margin": pred, "linear": lin_s,
                                "linear_agrees": lin_agree, "shifted_op_check": sh,
                                "mechanism": ("small-signal" if lin_agree else
                                              ("bias shift (DC operating point), confirmed" if sh and sh["agree"]
                                               else "unexplained")),
                                "pass": bool((step <= SENS_TOL_REL or (pred is not None and pred <= PRED_TOL_MARGIN))
                                             and (lin_agree or (sh is not None and sh["agree"])))})
    offset = {}
    for tid_, sl_ in ((fd1 or {}).get("terminals") or {}).items():
        s5, s20_ = sl_.get("5ohm"), sl_.get("20ohm")
        if s5 is None:
            continue
        # follower: the output tracks the input, so dV(OUT)/dR is the input-referred offset per ohm
        offset[tid_] = {"offset_uV_per_ohm_5ohm": s5 * 1e6, "offset_uV_per_ohm_20ohm": None if s20_ is None else s20_ * 1e6,
                        "ohm_per_mV_offset": (1e-3 / abs(s5)) if s5 else None}
    judged_r = [c for c in rchecks if "pass" in c]
    gates["G1.6_resistance_sensitivity_vs_spice"] = {
        "pass": (all(c["pass"] for c in judged_r) and bool(judged_r)) if fdr else None,
        "checks": rchecks, "values_ohm": R_VALUES,
        "note": "matched terminals varied symmetrically. Pass = SPICE slopes consistent between 20 and 100 ohm "
                "(or first-order prediction within 5 % of the margin at 100 ohm) AND the linear model explains "
                "the change: either directly (small-signal) or when re-solved at the operating point SPICE finds "
                "with the resistor inserted (bias shift)."}
    write_json(out / "sensitivity_r.json", {
        "units": "spec units per ohm of series resistance between device terminal(s) and the net",
        "groups": rtable, "base_spice": fdr["base"] if fdr else None, "margins": margins,
        "dc_saturation_margin_V": base_sat,
        "mismatch_offset": {"terminals": offset, "follower_base_vout_V": (fd1 or {}).get("base_vout_V"),
                            "method": "one-sided resistor (5 and 20 ohm) on one member of a matched pair, OTA in "
                                      "unity-gain feedback (Vinn tied to OUT): dV(OUT)/dR = systematic input offset",
                            "note": "no offset spec in the design package: reported per ohm, budget not evaluated"}})
    crit_t = sorted([{"group": k, "ohm_to_consume_margin": v["ohm_to_consume_margin"], "most_limiting": v["most_limiting"]}
                     for k, v in rtable.items()], key=lambda r: r["ohm_to_consume_margin"] or math.inf)
    for i, c in enumerate(crit_t):
        c["rank"] = i + 1
    intent["critical_terminals"] = crit_t
    intent["ranking_terminals"] = ("ascending series resistance (ohm, applied to every member of the group) that "
                                   "would alone consume the margin of the most limiting spec, incl. DC headroom")
    write_json(out / "intent.json", intent)

    prov = provenance([s0 / "circuit_ir.json", REPO / a.package] + ([REPO / up["equations"], REPO / up["name_map"]] if sym else []))
    report = {"design": design, "gates": gates, "all_pass": all(g.get("pass") in (True, None) for g in gates.values()),
              "provenance": prov}
    write_json(out / "s1_report.json", report)
    for k, g in gates.items():
        print(f"{k:45s} {'PASS' if g.get('pass') else ('INFO' if g.get('pass') is None else 'FAIL')}")
    print("S1", "PASS" if report["all_pass"] else "FAIL", "->", rel(out))
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
