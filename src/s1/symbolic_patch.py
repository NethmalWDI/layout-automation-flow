#!/usr/bin/env python3
"""S1 add-on — the 'pole drop-out' study: the upstream level-2 template has no mirror pole.

The upstream file circuits/5t-ota/source/5t-ota_differential_equations.json (READ-ONLY, never edited)
builds the level-2 amplifier X1 with elements for the mirror node Ioutn (= net0 upstream, net3 here):
R1_X1 (its resistance), C2_X1 (its capacitance to ground), C5_X1 (its capacitance to Vinn), but its
performance template has no element that carries the signal from Ioutn to the output: the mirror
coupling Ioutn -> Ioutp (G12_X1_X1) is listed under 'missing', and only its DC effect is folded into
G2_X1. So the mirror node never creates a pole: PM and GBW come out optimistic and the node's
sensitivity is 0 by construction.

This module writes PATCHED COPIES (derived inputs) next to the name map, with textbook equations added:
  P1 'mirror doublet' (only symbols the file already defines):
       Gm(s) = G2_X1_X2 + (G2_X1 - G2_X1_X2) / (1 + s*tau_m),   tau_m = R1_X1*(C2_X1 + C5_X1)
       = the classic 5T-OTA mirror pole at 1/tau_m with its zero at ~2/tau_m (pole-zero doublet).
  P2 'mirror doublet + transcapacitance':
       in addition gm(s) = gm - s*Cm for the input device and the mirror output device, with
       Cm = Cdg - Cgd ~= (2/5)*Cgs in saturation (quasi-static charge model, 40/60 charge partition),
       written with the level-0 symbol C2 (gate-source) that the file already has.
Each copy is evaluated by the same evaluator as the original (src/s1/symbolic.py) and checked against
  (a) the exact rational H(s) of the same patched model (validates the closed-form wu and PM),
  (b) the same model with Cm taken from the OP (|cdg| - |cgd|) instead of (2/5)*Cgs (approximation error),
  (c) transistor-level SPICE: S0 achieved values and the S1 SPICE finite differences (CL, net3).

usage (inside layout-s0s3): python3 -m src.s1.symbolic_patch inputs/<design>/package.yaml [...]
outputs: <name_map dir>/upstream_patched/5t-ota_differential_equations.{P1,P2}.json (regenerated)
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
from src.s1 import linear, symbolic

ORIGINAL_TERMS = ("A0", "wgbw", "kft")
COMMON_REFS = [
    "B. Razavi, Design of Analog CMOS Integrated Circuits, 2nd ed., ch. 5/10: five-transistor OTA, mirror "
    "pole gm3/C_mirror with a zero at twice its frequency",
    "W. Sansen, Analog Design Essentials, ch. 5 (OTA with current-mirror load: pole-zero doublet)",
]
CM_REFS = [
    "Y. Tsividis, C. McAndrew, Operation and Modeling of the MOS Transistor, 3rd ed., ch. 8: quasi-static "
    "small-signal model, transcapacitance Cm = Cdg - Cgd = (4/15) Cox W L = (2/5) Cgs in saturation",
]

# --- the textbook terms, in the file's own symbols ----------------------------------------------------
TAU_M = "R1_X1*(C2_X1 + C5_X1)"
CM_IN = "2*C2_XM3/5"      # input device (upstream XM3 = Vinp side; XM4 takes XM3's values)
CM_P = "2*C2_XM2/5"       # mirror output device (upstream XM2)


def build_patched(orig: dict, variant: str, orig_rel: str) -> dict:
    """Return a patched copy of the upstream equations. variant 'P1' or 'P2'. The original performance
    block is kept under 'performance_original'; the level trees are untouched."""
    assert variant in ("P1", "P2")
    doc = copy.deepcopy(orig)
    perf0 = orig["performance"]
    perf = copy.deepcopy(perf0)
    cm = variant == "P2"
    terms = {k: perf0["terms"][k] for k in ORIGINAL_TERMS}
    terms["wu0"] = perf0["terms"]["wu"]                  # the original estimate (one pole + feedthrough)
    terms["tau_m"] = TAU_M
    terms["Cm_in"] = CM_IN if cm else "0"
    terms["Cm_p"] = CM_P if cm else "0"
    terms["tau_z"] = "(tau_m - Cm_p*R1_X1)/(1 + G12_X1_X1*R1_X1)"
    # |H| = 1 with one dominant pole and the doublet: (wu0/w)^2 (1 + w^2 tau_z^2)/(1 + w^2 tau_m^2) = 1,
    # a quadratic in w^2 -> exact for that magnitude model
    terms["wu_d"] = ("sqrt((-(1 - wu0**2*tau_z**2) + sqrt((1 - wu0**2*tau_z**2)**2 + 4*tau_m**2*wu0**2))"
                     "/(2*tau_m**2))")
    terms["wu"] = "wu_d*sqrt(1 + (wu_d*Cm_in/G1_X1_X2)**2)" if cm else "wu_d"
    perf["terms"] = terms
    pm = ("180 - 180*(atan(C6_X1*wu/G2_X1) + atan(R2_X1*wu*(C4_X1 + C6_X1 + CL)) + atan(wu*tau_m) "
          "- atan(wu*tau_z)" + (" + atan(wu*Cm_in/G1_X1_X2)" if cm else "") + ")/pi")
    perf["pm_deg"] = pm
    gm_d = "(G2_X1_X2 - s*Cm_in)"
    gm_n = "(G1_X1_X2 - s*Cm_in)"
    gm_m = "(G12_X1_X1 - s*Cm_p)"
    perf["transfer_function"] = {"v(Voutp) per vd": {
        "form": (f"H(s) = (R2_X1/2)*(Gm(s) - s*C6_X1)/(1 + s*R2_X1*(C4_X1 + C6_X1 + CL)), "
                 f"Gm(s) = {gm_d} + {gm_n}*{gm_m}*R1_X1/(1 + s*tau_m)"),
        "poles_rad_s": ["-1/(R2_X1*(C4_X1 + C6_X1 + CL))", "-1/tau_m"],
        "zeros_rad_s_estimate": ["-1/tau_z", "G2_X1/C6_X1"] + (["G1_X1_X2/Cm_in"] if cm else []),
        "note": "poles exact (the denominator factors); zeros are the usual far-apart estimates"}}
    doc["performance_original"] = perf0
    doc["performance"] = perf
    doc["patch"] = {
        "variant": variant,
        "status": "ASSUMPTION / derived input: textbook equations added by this repository, not by upstream",
        "based_on": {"file": orig_rel, "sha256": sha256(REPO / orig_rel)},
        "reason": ("upstream 'missing': the Ioutn -> Ioutp coupling (G12_X1_X1) of the mirror is not in the "
                   "level-2 template, only its DC value inside G2_X1; the mirror node then has no pole."),
        "changes": [
            "Gm(s): the mirrored half of G2_X1 passes through the mirror node: pole 1/tau_m, "
            "tau_m = R1_X1*(C2_X1 + C5_X1) (elements the file already builds for Ioutn); zero at 1/tau_z",
            "wu: magnitude condition with the doublet solved exactly (quadratic in w^2) starting from the "
            "original estimate wu0",
            "pm_deg: adds atan(wu*tau_m) - atan(wu*tau_z) to the original phase lag",
        ] + ([
            "gm(s) = gm - s*Cm for the input pair and the mirror output device (transcapacitance), "
            "Cm ~= (2/5)*C2 (C2 = level-0 gate-source capacitance); adds the RHP-zero lag "
            "atan(wu*Cm_in/G1_X1_X2) and moves the doublet zero (tau_z)",
        ] if cm else []),
        "assumptions": [
            "matched pair: G1_X1_X2 = G2_X1_X2 (true for this template: both are G1_XM3)",
            "nodes far apart: Vinn/Vinp are ideal sources, the tail is an AC ground (upstream assumption)",
        ] + (["Cm = (2/5)*Cgs is the long-channel saturation value; it is checked against the OP's "
              "|cdg| - |cgd| in symbolic_patch_check.json"] if cm else []),
        "references": COMMON_REFS + (CM_REFS if cm else []),
    }
    return doc


# --- numeric check: the exact rational H(s) of the patched model --------------------------------------
L2_NAMES = ["R1_X1", "R2_X1", "C2_X1", "C4_X1", "C5_X1", "C6_X1", "G2_X1", "G1_X1_X2", "G2_X1_X2",
            "G12_X1_X1", "C2_XM3", "C2_XM2"]


def level_values(eq: dict, nm: dict, op: dict, names: list) -> dict:
    defs: dict = {}
    symbolic.collect_values(eq, defs)
    l0 = symbolic.level0_values(op, nm)
    sy = {k: sp.Symbol(k) for k in set(defs) | set(l0)}
    loc = {**sy, "oo": sp.oo}
    ex = {k: sp.sympify(v, locals=loc) for k, v in defs.items()}
    out = {}
    for k in names:
        e = sp.Symbol(k)
        for _ in range(8):
            e2 = e.xreplace({sy[j]: ex[j] for j in ex if sy[j] in e.free_symbols})
            if e2 == e:
                break
            e = e2
        out[k] = float(e.xreplace({sy[j]: v for j, v in l0.items()}))
    return out


def exact(v: dict, CL: float, cm_in: float, cm_p: float) -> dict:
    """GBW and PM of H(s) = (R2/2)(Gm(s) - s C6)/(1 + s R2 Cout), Gm as in build_patched (exact rational)."""
    P = np.polynomial.polynomial
    tm = v["R1_X1"] * (v["C2_X1"] + v["C5_X1"])
    g_d, g_n, g_m = [v["G2_X1_X2"], -cm_in], [v["G1_X1_X2"], -cm_in], [v["G12_X1_X1"], -cm_p]
    num = P.polyadd(P.polymul(g_d, [1, tm]), P.polymul(P.polymul(g_n, g_m), [v["R1_X1"]]))
    num = P.polysub(num, P.polymul([0, v["C6_X1"]], [1, tm])) * v["R2_X1"] / 2
    den = P.polymul([1, tm], [1, v["R2_X1"] * (v["C4_X1"] + v["C6_X1"] + CL)])
    H = lambda w: P.polyval(1j * w, num) / P.polyval(1j * w, den)
    lo, hi = 1e3, 1e13
    if abs(H(lo)) <= 1:
        return {"gbw_mhz": None, "pm_deg": None}
    for _ in range(200):
        m = math.sqrt(lo * hi)
        lo, hi = (m, hi) if abs(H(m)) > 1 else (lo, m)
    w = np.logspace(0, math.log10(lo), 4000)
    ph = np.unwrap(np.angle(H(w)))
    return {"gbw_mhz": lo / 2e6 / math.pi, "pm_deg": 180 - math.degrees(ph[0] - ph[-1]),
            "mirror_pole_mhz": 1 / (2 * math.pi * tm) / 1e6 if tm > 0 else None}


def fd_slopes(s1_dir: Path, case: str) -> dict | None:
    """S1 SPICE finite-difference slope (5 fF step) for a node, per fF."""
    f = s1_dir / "sensitivity.json"
    if not f.exists():
        return None
    fd = json.loads(f.read_text()).get("spice_fd") or {}
    c = (fd.get("cases") or {}).get(case) or {}
    return (c.get("5fF") or {}).get("slope_per_fF")


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
        pdir = nm_path.parent / "upstream_patched"
        pdir.mkdir(parents=True, exist_ok=True)
        files = {"original": REPO / orig_rel}
        for v in ("P1", "P2"):
            f = pdir / f"{Path(orig_rel).stem}.{v}.json"
            f.write_text(json.dumps(build_patched(orig, v, orig_rel), indent=1) + "\n")
            files[v] = f
        s1 = REPO / "outputs" / "S1" / design
        op = json.loads((s1 / "operating_point.json").read_text())["devices"]
        ir = json.loads((REPO / "outputs" / "S0" / design / "circuit_ir.json").read_text())
        CL = linear.parse_si(ir["conditions"]["CL_F"])
        ach = json.loads((s1 / "symbolic_check.json").read_text())["spice"]
        # mirror node (upstream net0 = target net3): C4_XM1 is a grounded cap only on that node
        mirror_net = nm["nets"].get("net0")
        out_net = nm["nets"].get("Voutp")
        res = {}
        for name, f in files.items():
            r = symbolic.evaluate(f, nm_path, op, CL, extra_sens={mirror_net: "C4_XM1"})
            res[name] = {"file": str(f.relative_to(REPO)), "predicted": r["predicted"],
                         "error_vs_spice": {k: r["predicted"][k] - ach[k] for k in r["predicted"]},
                         "per_fF": {out_net: r["d_dCL_per_fF"], mirror_net: r["d_dsymbol_per_fF"][mirror_net]["per_fF"]},
                         "unresolved_symbols": r["unresolved_symbols"]}
        v = level_values(orig, nm, op, L2_NAMES)
        dev_in, dev_p = nm["devices"]["XM3"], nm["devices"]["XM2"]
        cm_op = {"in": abs(op[dev_in]["cdg"]) - abs(op[dev_in]["cgd"]),
                 "p": abs(op[dev_p]["cdg"]) - abs(op[dev_p]["cgd"])}
        cm_25 = {"in": 0.4 * v["C2_XM3"], "p": 0.4 * v["C2_XM2"]}
        checks = {
            "P1_exact_rational": exact(v, CL, 0.0, 0.0),
            "P2_exact_rational": exact(v, CL, cm_25["in"], cm_25["p"]),
            "P2_exact_rational_Cm_from_OP": exact(v, CL, cm_op["in"], cm_op["p"]),
        }
        fd = {out_net: fd_slopes(s1, out_net), mirror_net: fd_slopes(s1, mirror_net)}
        doc = {"design": design, "spice": ach, "CL_F": CL, "models": res, "exact_checks": checks,
               "Cm_F": {"two_fifths_Cgs": cm_25, "from_op_cdg_minus_cgd": cm_op},
               "level2_values": v, "spice_fd_per_fF": fd,
               "reading": ("'original' = upstream template; P1 adds the mirror pole-zero doublet; P2 also adds the "
                           "transcapacitance. error_vs_spice = prediction - transistor-level SPICE. exact_checks: "
                           "the patched model solved without the closed-form approximations.")}
        write_json(s1 / "symbolic_patch_check.json", doc)
        summary[design] = {k: {"pred": res[k]["predicted"], "err": res[k]["error_vs_spice"]} for k in res}
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            (s1 / "plots").mkdir(exist_ok=True)
            fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
            labels = ["upstream\noriginal", "P1\n+mirror doublet", "P2\n+transcap.", "SPICE"]
            for i, (k, unit) in enumerate((("pm_deg", "PM (deg)"), ("gbw_mhz", "GBW (MHz)"))):
                vals = [res["original"]["predicted"][k], res["P1"]["predicted"][k], res["P2"]["predicted"][k], ach[k]]
                bars = ax[i].bar(labels, vals, color=["#9aa5b1", "#5b8def", "#2f6fdb", "#2e7d32"])
                for b, x in zip(bars, vals):
                    ax[i].text(b.get_x() + b.get_width() / 2, x, f"{x:.1f}", ha="center", va="bottom", fontsize=8)
                ax[i].set_ylabel(unit)
                ax[i].set_ylim(0, max(vals) * 1.15)
                ax[i].tick_params(axis="x", labelsize=8)
            fig.suptitle(f"{design}: symbolic model vs SPICE (CL = {CL * 1e15:.0f} fF)", fontsize=10)
            fig.tight_layout()
            fig.savefig(s1 / "plots" / "symbolic_patch.png", dpi=120)
            plt.close(fig)
        except Exception as e:  # evidence only
            print("plot error:", e, file=sys.stderr)
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
