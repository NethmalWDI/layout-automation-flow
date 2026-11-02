#!/usr/bin/env python3
"""S1 add-on (Plan v3 Phase A step 10, row 49): LOADBench's hand model with the NMOS-mirror pole-zero doublet.

circuits/loadbench_miller/upstream/equations.predicted.json (hash-frozen, never edited) is the PREDICTED textbook
two-stage Miller model; its 'assumes' says "first-stage mirror pole-zero doublet neglected". On this design the
doublet's pole (~33 MHz) sits next to the unity-gain frequency (~25 MHz), and it is the whole 17 deg gap between
the hand PM and SPICE in G1.5.

This module writes a PATCHED COPY (derived input) to inputs/<design>/upstream_patched/ -- nothing in circuits/:
  P1 'mirror doublet': half of the first stage's signal passes through the mirror node,
       Gm(s) = gm1/2 * (1 + 1/(1 + s*tau_m)) = gm1 * (1 + s*tau_m/2) / (1 + s*tau_m),
       tau_m = C_m / g_m,  g_m = gm_N1 + gds_N1 + gds_P7 (equal to the S1 linear model's conductance at the node),
       C_m = the S1 linear model's capacitance at the node (diagonal of C), written as C4_<diode device> + the
       rest, so that the node's sensitivity can be taken symbolically (C4 of the diode device is on no other node).
       Pole 1/tau_m, zero 2/tau_m; Gm(0) = gm1, so the DC gain is the original's.
It is labelled PREDICTED (patched, post hoc): it was written after this circuit's 17 deg gap was seen, so it has to
be judged on other designs as well. G1.5 (the unpatched file) stays as it is, reported and not gated.

The copy is evaluated by the same evaluator as the original (src/s1/symbolic.py) and checked against
  (a) the exact rational H(s) of the same model (two poles, the RHP zero, the doublet; no closed-form shortcuts),
  (b) transistor-level SPICE: the S0 achieved values and the S1 SPICE finite differences at the output and the
      mirror node.

usage (inside layout-s0s3): python3 -m src.s1.symbolic_patch_miller inputs/<design>/package.yaml
outputs: inputs/<design>/upstream_patched/<equations stem>.P1.json (regenerated)
         outputs/S1/<design>/symbolic_patch_check.json, outputs/S1/<design>/plots/symbolic_patch.png
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
import yaml

from src.common.tools import REPO, sha256, write_json
from src.s0.ingest import load_package
from src.s1 import linear, op as opmod, symbolic
from src.s1.run import ac_drive
from src.s1.symbolic_patch import COMMON_REFS, fd_slopes

LABEL = "PREDICTED (patched, post hoc)"
# the mirror of LOADBench's SimpleTwoStageOpAmp (upstream names; identity name map): the input device P7 feeds the
# diode-connected N1 on the mirror node, which N4 mirrors onto the first-stage output (P6's drain)
ROLES = {"mirror_net": "FirstStageYout1", "diode": "XDiodeTransistorNmos1", "mirror_out": "XNormalTransistorNmos4",
         "input_mirror_side": "XNormalTransistorPmos7", "input_direct": "XNormalTransistorPmos6", "out_net": "out"}
REFS = ["P. E. Allen, D. R. Holberg, CMOS Analog Circuit Design, 3rd ed., sec. 6.2: two-stage op amp, the mirror "
        "pole of the first stage with a left-half-plane zero at twice its frequency"] + COMMON_REFS


def build_patched(orig: dict, orig_rel: str, c_rest: float) -> dict:
    """The patched copy P1. c_rest: the S1 linear model's capacitance at the mirror node minus the OP value of
    C4_<diode device> (F); the original performance block is kept under 'performance_original'."""
    doc = copy.deepcopy(orig)
    perf0 = orig["performance"]
    perf = copy.deepcopy(perf0)
    d, p7 = ROLES["diode"], ROLES["input_mirror_side"]
    # the evaluator resolves terms in order, each in those before it: 'wu' moves to the end
    terms = {k: v for k, v in perf0["terms"].items() if k != "wu"}
    terms["wu0"] = perf0["terms"]["wu"]                  # the original estimate (dominant pole only)
    terms["g_m"] = f"G1_{d} + 1/R1_{d} + 1/R1_{p7}"
    terms["C_m"] = f"C4_{d} + {c_rest!r}"
    terms["tau_m"] = "C_m/g_m"
    terms["tau_z"] = "tau_m/2"
    # |H| = 1 with the dominant pole and the doublet: (wu0/w)^2 (1 + w^2 tau_z^2)/(1 + w^2 tau_m^2) = 1, a quadratic
    # in w^2 (the form of the 5T patch, src/s1/symbolic_patch.py)
    terms["wu"] = ("sqrt((-(1 - wu0**2*tau_z**2) + sqrt((1 - wu0**2*tau_z**2)**2 + 4*tau_m**2*wu0**2))"
                   "/(2*tau_m**2))")
    perf["terms"] = terms
    perf["pm_deg"] = ("180 - 180*(atan(wu*A0*Cc/gm1) + atan(wu/wp2) + atan(wu/wz) + atan(wu*tau_m) "
                      "- atan(wu*tau_z))/pi")
    perf["transfer_function"] = {"v(out) per vd": {
        "form": "H(s) = Gm(s)*(gm2 - s*Cc)*R1o*R2o / (1 + s*(R1o*(C1n + Cc) + R2o*(C2n + Cc) + gm2*R1o*R2o*Cc) "
                "+ s**2*R1o*R2o*(C1n*C2n + Cc*(C1n + C2n))), Gm(s) = gm1*(1 + s*tau_z)/(1 + s*tau_m)",
        "poles_rad_s": ["the two roots of the quadratic denominator", "-1/tau_m"],
        "zeros_rad_s": ["gm2/Cc (right half plane)", "-1/tau_z = -2/tau_m"]}}
    doc["provenance"] = LABEL
    doc["performance_original"] = perf0
    doc["performance"] = perf
    doc["patch"] = {
        "variant": "P1",
        "status": f"{LABEL}: textbook terms added by this repository after seeing this circuit's PM gap (G1.5, "
                  "17 deg); derived input, regenerated by src/s1/symbolic_patch_miller.py from the S1 outputs",
        "based_on": {"file": orig_rel, "sha256": sha256(REPO / orig_rel)},
        "reason": ("the original 'assumes' neglects the first-stage mirror pole-zero doublet; on this design the "
                   "mirror pole sits next to the unity-gain frequency"),
        "changes": [
            f"Gm(s) = gm1/2*(1 + 1/(1 + s*tau_m)): the half of the signal from {p7} passes through the mirror node "
            f"{ROLES['mirror_net']}; tau_m = C_m/g_m, g_m = gm + gds of {d} + gds of {p7}",
            f"C_m: the S1 linear model's capacitance at {ROLES['mirror_net']} (diagonal of C), written as C4_{d} "
            f"+ {c_rest:.6g} F so that the node's sensitivity can be taken symbolically",
            "wu: magnitude condition with the doublet solved exactly (quadratic in w^2) from the original wu0",
            "pm_deg: adds atan(wu*tau_m) - atan(wu*tau_z) to the original phase lag",
        ],
        "assumptions": [
            f"matched input pair: the mirrored half uses the file's gm1 (G1 of {ROLES['input_direct']}); "
            f"{p7}'s gm differs by the amount recorded in symbolic_patch_check.json",
            f"matched mirror: {ROLES['mirror_out']} copies {d}'s current 1:1, so Gm(0) = gm1 as in the original",
            "the mirror node's other nodes are AC ground for its time constant (C from the diagonal of C)",
        ],
        "references": REFS,
    }
    return doc


def term_values(perf: dict, l0: dict, CL: float) -> dict:
    """Numeric value of every performance term (the terms are defined each in those before it)."""
    loc = {k: sp.Symbol(k) for k in set(l0) | set(perf["terms"]) | {"CL"}}
    loc.update({"pi": sp.pi, "Abs": sp.Abs, "log": sp.log, "atan": sp.atan, "sqrt": sp.sqrt})
    num = {loc[k]: v for k, v in l0.items()}
    num[loc["CL"]] = CL
    out = {}
    for k, v in perf["terms"].items():
        out[k] = float(sp.N(sp.sympify(v, locals=loc).xreplace({**num, **{loc[j]: x for j, x in out.items()}})))
    return out


def exact(t: dict, tau_m: float | None) -> dict:
    """GBW and PM of the model's full rational H(s), no closed-form approximation (tau_m None: no doublet)."""
    P = np.polynomial.polynomial
    R1, R2, g1, g2, Cc, C1, C2 = (t[k] for k in ("R1o", "R2o", "gm1", "gm2", "Cc", "C1n", "C2n"))
    num = P.polymul([g2, -Cc], [g1 * R1 * R2])
    den = [1.0, R1 * (C1 + Cc) + R2 * (C2 + Cc) + g2 * R1 * R2 * Cc, R1 * R2 * (C1 * C2 + Cc * (C1 + C2))]
    if tau_m:
        num, den = P.polymul(num, [1.0, tau_m / 2]), P.polymul(den, [1.0, tau_m])
    H = lambda w: P.polyval(1j * w, num) / P.polyval(1j * w, den)    # noqa: E731
    lo, hi = 1e3, 1e13
    if abs(H(lo)) <= 1:
        return {"gbw_mhz": None, "pm_deg": None}
    for _ in range(200):
        m = math.sqrt(lo * hi)
        lo, hi = (m, hi) if abs(H(m)) > 1 else (lo, m)
    ph = np.degrees(np.unwrap(np.angle(H(np.logspace(0, math.log10(lo), 4000)))))
    return {"gbw_mhz": lo / 2e6 / math.pi, "pm_deg": float(180 + ph[-1] - linear.pm_reference(ph[0]))}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("packages", nargs="+")
    a = ap.parse_args(argv)
    summary = {}
    for pk in a.packages:
        pkg = load_package(REPO / pk)
        design = pkg["design"]
        up = pkg["upstream"]
        orig_rel = up["equations"]
        nm_path = REPO / up["name_map"]
        nm = yaml.safe_load(nm_path.read_text())
        orig = json.loads((REPO / orig_rel).read_text())
        s0, s1 = REPO / "outputs" / "S0" / design, REPO / "outputs" / "S1" / design
        ir = json.loads((s0 / "circuit_ir.json").read_text())
        op_json = json.loads((s1 / "operating_point.json").read_text())
        opmod.apply_passives(ir, op_json)
        op = op_json["devices"]
        CL = linear.parse_si(ir["conditions"]["CL_F"])
        # the mirror node in the S1 linear model (the same model as S1's G1.2)
        lm = linear.LinearModel(ir, op, drive=ac_drive(s0, ir, pkg.get("ac_drive")))
        net, d, p7 = nm["nets"][ROLES["mirror_net"]], nm["devices"][ROLES["diode"]], nm["devices"][ROLES["input_mirror_side"]]
        i = lm.idx[net]
        c_lin, g_lin = float(lm.C[i, i]), float(lm.G[i, i])
        l0 = symbolic.level0_values(op, nm, ir.get("passives"))
        c4 = l0[f"C4_{ROLES['diode']}"]
        g_m = op[d]["gm"] + op[d]["gds"] + op[p7]["gds"]
        pdir = REPO / "inputs" / design / "upstream_patched"
        pdir.mkdir(parents=True, exist_ok=True)
        files = {"original": REPO / orig_rel, "P1": pdir / f"{Path(orig_rel).stem}.P1.json"}
        patched = build_patched(orig, orig_rel, c_lin - c4)
        files["P1"].write_text(json.dumps(patched, indent=1) + "\n")
        ach = json.loads((s1 / "symbolic_check.json").read_text())["spice"]
        res = {}
        for name, f in files.items():
            r = symbolic.evaluate(f, nm_path, op, CL, extra_sens={net: f"C4_{ROLES['diode']}"},
                                  passives=ir.get("passives"))
            res[name] = {"file": str(f.relative_to(REPO)), "predicted": r["predicted"],
                         "error_vs_spice": {k: r["predicted"][k] - ach[k] for k in r["predicted"]},
                         "per_fF": {nm["nets"][ROLES["out_net"]]: r["d_dCL_per_fF"], net: r["d_dsymbol_per_fF"][net]["per_fF"]},
                         "unresolved_symbols": r["unresolved_symbols"]}
        t1 = term_values(patched["performance"], l0, CL)
        checks = {"original_exact_rational": exact(t1, None), "P1_exact_rational": exact(t1, t1["tau_m"])}
        on_node = [f"C{k}_{ROLES[r]}" for r, ks in (("diode", "214"), ("mirror_out", "213"), ("input_mirror_side", "43"))
                   for k in ks]       # the file's level-0 capacitances that touch the mirror node
        mirror = {"net": net, "C_linear_model_F": c_lin, "C_level0_sum_F_for_comparison": sum(l0[k] for k in on_node),
                  "g_S": g_m, "g_linear_model_S": g_lin, "tau_m_s": t1["tau_m"],
                  "pole_mhz": 1 / (2 * math.pi * t1["tau_m"]) / 1e6, "zero_mhz": 2 / (2 * math.pi * t1["tau_m"]) / 1e6,
                  "gm_input_pair_S": {ROLES["input_direct"]: op[nm["devices"][ROLES["input_direct"]]]["gm"], p7: op[p7]["gm"]}}
        fd = {nm["nets"][ROLES["out_net"]]: fd_slopes(s1, nm["nets"][ROLES["out_net"]]), net: fd_slopes(s1, net)}
        doc = {"design": design, "label": LABEL, "spice": ach, "CL_F": CL, "models": res, "exact_checks": checks,
               "mirror_node": mirror, "spice_fd_per_fF": fd,
               "reading": ("'original' = the PREDICTED textbook file (G1.5); P1 adds the NMOS-mirror pole-zero doublet, "
                           "PREDICTED (patched, post hoc). error_vs_spice = prediction - transistor-level SPICE. "
                           "exact_checks: the same models solved without the closed-form approximations. The mirror "
                           "node's C is the S1 linear model's; the sum of the file's level-0 symbols on that node is "
                           "given for comparison only.")}
        write_json(s1 / "symbolic_patch_check.json", doc)
        summary[design] = {k: {"pred": res[k]["predicted"], "err": res[k]["error_vs_spice"]} for k in res}
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            (s1 / "plots").mkdir(exist_ok=True)
            fig, ax = plt.subplots(1, 2, figsize=(8, 3.4))
            labels = ["PREDICTED\noriginal", "P1 (post hoc)\n+mirror doublet", "SPICE"]
            for j, (k, unit) in enumerate((("pm_deg", "PM (deg)"), ("gbw_mhz", "GBW (MHz)"))):
                vals = [res["original"]["predicted"][k], res["P1"]["predicted"][k], ach[k]]
                bars = ax[j].bar(labels, vals, color=["#9aa5b1", "#5b8def", "#2e7d32"])
                for b, x in zip(bars, vals):
                    ax[j].text(b.get_x() + b.get_width() / 2, x, f"{x:.1f}", ha="center", va="bottom", fontsize=8)
                ax[j].set_ylabel(unit)
                ax[j].set_ylim(0, max(vals) * 1.15)
                ax[j].tick_params(axis="x", labelsize=8)
            fig.suptitle(f"{design}: hand model vs SPICE (CL = {CL * 1e15:.0f} fF)", fontsize=10)
            fig.tight_layout()
            fig.savefig(s1 / "plots" / "symbolic_patch.png", dpi=120)
            plt.close(fig)
        except Exception as e:  # evidence only
            print("plot error:", e, file=sys.stderr)
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
