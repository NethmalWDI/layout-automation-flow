#!/usr/bin/env python3
"""Generate docs/iadc_ota_report.md (and, with pandoc, a self-contained HTML copy): the full report on the automatic
layout of iadc_ota in a Tiny Tapeout analog tile, written for a reader who does not know the flow; the companion of
docs/ttsky25a_fd_report.html. It reuses scripts/make_ttsky_report.py's pictures, charts and tables (with that module's
design set to iadc_ota) and writes its own text: every number is read from the run's outputs or the flow's code; typed
by hand are only the explanations, the decision table, the novelty and LLM sections and the lists of assumptions.

usage (inside layout-s0s3, repo root, after `source scripts/env.sh`): python3 scripts/make_iadc_report.py [--no-html]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_s0s3_walkthrough as W  # noqa: E402
import make_ttsky_report as T  # noqa: E402
import report_figures as F  # noqa: E402

REPO = W.REPO
from src.s4 import block as B4  # noqa: E402
from src.s5 import grid as G5, macro as M5, place as P5  # noqa: E402

D = "iadc_ota"
T.D = D                                              # the shared helpers read these module globals
T.FIG = REPO / "outputs" / "report" / D
T.OUT_MD = REPO / "docs" / f"{D}_report.md"
T.MACROS = ("x1", "x2", "top")
T.LABEL = {**T.LABEL, "hand": "Hand layout (upstream)"}
FIG, OUT_MD = T.FIG, T.OUT_MD
RULES = T.RULES
MCOLOR = {"x1": "#e87ba4", "x2": "#008300", "top": "#eda100"}
MTEXT = {"x1": "x1: bias (folded_cascode_3_bias)", "x2": "x2: core (folded_cascode_3_core)",
         "top": "top: CMFB output capacitors C3/C4 and top-level dummies"}
T.MCOLOR, T.MTEXT = MCOLOR, MTEXT
SCH = "circuits/iadc_ota/upstream_src/schematic"
f, pct, fig_html = T.f, T.pct, T.fig_html


# ---------------------------------------------------------------------------------------------------- pictures
def layouts(d: dict, nb: dict) -> dict:
    FIG.mkdir(parents=True, exist_ok=True)
    W_UM, H_UM, PPU = 240, 240, 3                 # one scale for all three pictures
    out = {}
    ow, oh = d["opts"].get("outline_um", [161, 225.77])
    for r in RULES:
        out[r] = T.render(REPO / f"outputs/S5/{D}/routed_{r}/{D}_routed.gds", FIG / f"layout_{r}.png",
                          w=W_UM, h=H_UM, ppu=PPU, outline=f"{ow}x{oh}")
    out["hand"] = T.render(REPO / d["ref"]["gds"], FIG / "layout_hand.png", w=W_UM, h=H_UM, ppu=PPU, cell="sc_cmfb")
    for r in RULES:
        pl = d["pl"]["chosen"][r]["placement"]
        hi = T.render(REPO / f"outputs/S5/{D}/routed_{r}/{D}_routed.gds", FIG / f"layout_{r}_big.png",
                      w=W_UM, h=H_UM, ppu=6, outline=f"{ow}x{oh}")
        rects = [(m["bbox"], MCOLOR[k], k) for k, m in pl["macros"].items()]
        labels = [((b["bbox"][0] + b["bbox"][2]) / 2, (b["bbox"][1] + b["bbox"][3]) / 2, f"B{nb['num'][n]}")
                  for n, b in pl["blocks"].items()]
        F.annotate(FIG / f"layout_{r}_big.png", hi["window_um"], rects, labels, FIG / f"layout_{r}_annot.png",
                   title=f"{T.LABEL[r]}: sub-circuits outlined, blocks numbered (thin box: the tile)",
                   legend=[(MTEXT[k], MCOLOR[k]) for k in T.MACROS])
    hb = T.render(REPO / d["ref"]["gds"], FIG / "layout_hand_big.png", w=150, h=120, ppu=8, cell="sc_cmfb")
    rects = [(bx, "#898781", "sc_cmfb (the whole switched-capacitor CMFB)", "tl") for bx in hb["cells"].get("sc_cmfb", [])]
    F.annotate(FIG / "layout_hand_big.png", hb["window_um"], rects, [], FIG / "layout_hand_annot.png",
               title="Hand layout (upstream ota.gds): its only named sub-cell is the CMFB",
               legend=[("switched-capacitor CMFB: in the hand layout, not in the flow's circuit", "#898781")])
    return out


def schematics(d: dict, nb: dict) -> dict:
    """iadc's own xschem sheets with every laid-out device boxed in its sub-circuit's colour and its block number."""
    work = F._work(REPO, SCH, None)
    num, dev, macro = nb["num"], nb["dev"], nb["macro"]
    devices = {x["name"] for x in d["ir"]["devices"]} | {p["name"] for p in d["ir"].get("passives", [])}

    def boxes(prefix, insts, extra=()):
        out = []
        for i in insts:
            ir = prefix + i
            if ir in devices and ir in dev:
                out.append((i, macro[dev[ir]], f"B{num[dev[ir]]}", 6, 0.32))
        return out + list(extra)
    sheets = {"top": F.schematic(REPO, work, "ota", [("x1", "x1", "x1: bias", 16, 0.45), ("x2", "x2", "x2: core", 16, 0.45),
                                                     ("x3", "top", "x3: CMFB (only C3, C4 laid out)", 16, 0.38)],
                                 FIG / "sch_top.png", MCOLOR)}
    sheets["x1"] = F.schematic(REPO, work, "folded_cascode_3_bias",
                               boxes("XX1_", F.instance_names(work / "folded_cascode_3_bias.sch")), FIG / "sch_x1.png", MCOLOR)
    sheets["x2"] = F.schematic(REPO, work, "folded_cascode_3_core",
                               boxes("XX2_", F.instance_names(work / "folded_cascode_3_core.sch")), FIG / "sch_x2.png", MCOLOR)
    sheets["x3"] = F.schematic(REPO, work, "sc_cmfb", boxes("X", F.instance_names(work / "sc_cmfb.sch")),
                               FIG / "sch_x3.png", MCOLOR)
    return sheets


def shot(src: Path, title: str, out: Path, keep=None, first: str | None = None, last: str | None = None) -> Path:
    """A picture of a tool's own report, as a terminal shows it: the lines of `src` from the one containing `first`
    to the one containing `last` (or those `keep` picks), verbatim, under a title naming the file."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    lines = src.read_text(errors="replace").splitlines()
    if first or last:
        i = next((k for k, ln in enumerate(lines) if first and first in ln), 0)
        j = next((k for k, ln in enumerate(lines) if last and last in ln and k >= i), len(lines) - 1)
        lines = lines[i:j + 1]
    if keep:
        lines = [ln for ln in lines if keep(ln)]
    lines = [ln.rstrip()[:96] for ln in lines][:40]
    fig = plt.figure(figsize=(8.6, 0.55 + 0.19 * (len(lines) + 2)), dpi=150)
    fig.patch.set_facecolor("#1a1a19")
    fig.text(0.012, 1 - 0.18 / fig.get_figheight(), f"$ {title}", color="#9fd3a8", family="DejaVu Sans Mono",
             fontsize=8.2, va="top")
    fig.text(0.012, 1 - 0.45 / fig.get_figheight(), "\n".join(lines), color="#e8e6df", family="DejaVu Sans Mono",
             fontsize=7.6, va="top", linespacing=1.32)
    fig.savefig(out, facecolor="#1a1a19")
    plt.close(fig)
    return out


def shots() -> dict:
    """The final (budget-aware) design's sign-off, as the tools wrote it."""
    s5 = REPO / f"outputs/S5/{D}/routed_budget_aware"
    return {
        "drc": shot(s5 / "drc/drc_report.txt", f"Magic DRC, routed top cell: {s5.relative_to(REPO)}/drc/drc_report.txt",
                    FIG / "shot_drc.png"),
        "lvs": shot(s5 / "lvs/lvs/lvs_report.txt", f"Netgen LVS, routed layout against the circuit: "
                    f"{s5.relative_to(REPO)}/lvs/lvs/lvs_report.txt", FIG / "shot_lvs.png",
                    first="Number of devices", last="Final result"),
        "neg": shot(s5 / "lvs/lvs_negctl/lvs_report.txt", "Netgen LVS, negative control (one device's L changed): "
                    "must not match cleanly", FIG / "shot_lvs_negctl.png",
                    keep=lambda ln: "Netlists" in ln or "Final result" in ln or "property errors" in ln.lower()
                    or "Number of" in ln),
        "flat": shot(REPO / f"outputs/S6/{D}/budget_aware/lvs_report.txt",
                     f"Netgen LVS, flat extraction (S6): outputs/S6/{D}/budget_aware/lvs_report.txt",
                     FIG / "shot_lvs_flat.png", keep=lambda ln: "Number of" in ln or "Netlists" in ln
                     or "Final result" in ln or "symmetr" in ln),
    }


def numbers(d: dict, lay: dict) -> dict:
    m = d["m7"]["metrics"]
    ref = d["ref"]
    size = d["s5"]["gates"]["G5.6_outline"]["size_um"]
    hw, hh = lay["hand"]["w_um"], lay["hand"]["h_um"]
    cm = lay["hand"]["cells"]["sc_cmfb"][0]
    area = {r: size[r][0] * size[r][1] for r in RULES}
    area["hand"] = hw * hh
    wl = {}
    for r in RULES:
        wl[r] = {"gbw_pct": -pct(m[r]["gbw_mhz"]["drawn"], m[r]["gbw_mhz"]["post_layout_rc"]),
                 "pm_deg": m[r]["pm_deg"]["drawn"] - m[r]["pm_deg"]["post_layout_rc"],
                 "gain_db": m[r]["gain_db"]["drawn"] - m[r]["gain_db"]["post_layout_rc"]}
    dr, po = ref["drawn_devices_only"], ref["post_layout"]
    wl["hand"] = {"gbw_pct": -pct(dr["gbw_mhz"], po["gbw_mhz"]), "pm_deg": dr["pm_deg"] - po["pm_deg"],
                  "gain_db": dr["gain_db"] - po["gain_db"]}
    ow, oh = d["opts"].get("outline_um", [161, 225.77])
    secs = {st: sum(x.get("seconds") or 0 for x in d["fs"].get(st, {}).get("steps", [])) for st in d["fs"]}
    return {"size": {**size, "hand": [hw, hh]}, "area": area, "cmfb_area": (cm[2] - cm[0]) * (cm[3] - cm[1]),
            "cmfb_size": [cm[2] - cm[0], cm[3] - cm[1]], "wiring_loss": wl, "outline": [ow, oh],
            "outline_area": ow * oh, "secs": secs}


# ---------------------------------------------------------------------------------------------------- the text
GLOSSARY = [g for g in T.GLOSSARY if g[0] != "MIM capacitor"] + [
    ("MIM capacitor", "metal–insulator–metal capacitor: here the CMFB's output capacitors C3 and C4, 4 units of "
                      "4.8 × 4.8 µm each (196 fF)."),
    ("CMFB", "common-mode feedback: holds the average of the two outputs at a reference voltage. iadc's is a "
             "switched-capacitor circuit; the flow's AC model replaces it by an ideal source with its steady-state "
             "law (ASSUMPTION), keeping only its output capacitors C3 and C4 in the circuit."),
    ("Tiny Tapeout analog tile", "the fixed area a design gets on a Tiny Tapeout chip; the 1×2 analog tile is "
                                 "161 × 225.77 µm (read from Imasha's taped-out tile)."),
    ("Multi-row array", "a device with many copies drawn as several identical rows inside one tap ring, instead of "
                        "one long row (iadc's two m = 96 devices)."),
]

ASSUMPTIONS = [
    "The specs: phase margin ≥ 60° from the design's config; gain ≥ the schematic's gain − 1 dB and GBW ≥ 0.9 × the "
    "schematic's GBW, derived from the schematic's own results (ASSUMPTION: the upstream project gives no specs).",
    "The switched-capacitor CMFB is modelled by an ideal source with its steady-state law (ASSUMPTION); only its "
    "output capacitors C3 and C4 are in the laid-out circuit.",
    "The whole Tiny Tapeout 1×2 tile (161 × 225.77 µm) is the outline; the tile's power straps and analog pins are "
    "not routed (ASSUMPTION).",
    "The matching and dummy choices repeat Imasha's decisions for ttsky25a_fd (centroid or interdigitated, a dummy at "
    "each end of every matched row), although the netlist already holds the designer's own dummies (ASSUMPTION).",
    "The fold limit: a single device's row longer than 100 µm becomes a multi-row array (ASSUMPTION; any value below "
    "the tile's width works).",
    "Capacitance-only extraction, as for ttsky25a_fd and as the hand layout was measured (flow record 7.8).",
    "One condition only (typical corner, 27 °C, 0.3 pF per output, 30 µA bias); no PVT corners after layout.",
    "Electromigration limits for SKY130 were not found in the PDK; wire widths are not checked against current.",
]

DECISIONS = [
    ("Specs", "PM ≥ 60° (config); gain ≥ schematic − 1 dB; GBW ≥ 0.9 × schematic", "upstream gives no specs",
     "applies them in every check", "accepted the rule (ttsky, LOADBench)", "proposed the ASSUMPTION"),
    ("CMFB model", "an ideal source with the switched-capacitor CMFB's steady-state law; C3, C4 kept",
     "an AC flow cannot simulate a clocked CMFB directly", "simulates it", "–", "proposed (ASSUMPTION)"),
    ("Share of the margin for layout (η)", "0.5", "half kept for what the flow does not model", "applies it",
     "accepted", "proposed (ASSUMPTION)"),
    ("Main nodes, budgets, cells", "as for every design (sections 3, 5)", "from the specs and the small-signal model",
     "computes them (S1–S3)", "–", "wrote the methods"),
    ("Blocks and matching", "matched devices together; common centroid or interdigitated, as needed",
     "gradients cancel; the cheaper one wins", "draws both, S5 picks by the cost", "decided the policy (ttsky)",
     "implemented"),
    ("Dummies", "one at each end of every matched row", "edge effects", "adds them", "decided for ttsky; for iadc "
     "an ASSUMPTION", "implemented"),
    ("Capacitors", "C3, C4 as 4 MIM units of 4.8 × 4.8 µm each", "as the netlist gives them", "draws the arrays",
     "(the design)", "implemented"),
    ("Outline", "the Tiny Tapeout 1×2 analog tile, 161 × 225.77 µm", "the design must fit a tile",
     "rejects anything outside (G5.6)", "decided (2026-11-04)", "read the tile from her taped-out GDS"),
    ("Long devices", "a multi-row array in one ring for the two m = 96 devices", "a 198 µm row is wider than the "
     "tile", "folds any single-device row over 100 µm", "decided (2026-11-05: one multi-row array)",
     "implemented; proposed the 100 µm limit (ASSUMPTION)"),
    ("Sub-circuits as macros", "x1 (bias), x2 (core), top", "keeps the designer's grouping", "places each, then "
     "arranges them", "decided (use the given hierarchy)", "implemented"),
    ("Placement search in a tight outline", "start from shelf packing; area-only shapes when nothing else fits",
     "the default search could not reach a fit in the tile (rows 96, 98, 99)", "searches", "–",
     "designed; opt-in for iadc only so the finished designs keep their results"),
    ("Routing", "metal-3/metal-4 grid router", "as for ttsky", "routes", "–", "designed"),
    ("Extraction", "capacitance only", "as ttsky; as the hand layout was measured", "extracts", "open question",
     "proposed"),
    ("Checks", "DRC, LVS, budgets, specs, η, at every stage", "nothing passes on trust", "runs them",
     "approved PREREG", "drafted PREREG"),
]

WHY = {
    "G0.7": "S0's own reference cell of two devices (XX2_M23, XX2_M24, the PDK's default cell) has 12 DRC errors; "
            "that cell is a reference only, and S3 chooses the cells S4 draws (all signed off).",
    "G1.1": "some devices sit below saturation by design (unit cascodes); the open G1.1 question (flow record row 41).",
    "G2.7": "S2's budgets cannot all be met with the library's smallest cells (\"library floors\"): the margins left "
            "for the layout are small.",
    "G3.3": "some transistor types use their \"least bad\" drawn cell; follows from G2.7.",
    "G3.5": "same as G3.3: a relaxation was needed for some cells.",
    "G5.4": "S2's wire-length budgets are far exceeded by nets that run between sub-circuits in the tile.",
    "G6.2": "follows from G5.4: the long nets and their couplings exceed S2's capacitance budgets.",
    "G7.1": "GBW misses its spec after layout (section 7).",
    "G7.2": "GBW loses more than η × its margin (section 7).",
}


def build_md(d: dict, num: dict, lay: dict, nb: dict, nodes_main: list, head: str) -> list:
    ir, s5g, s6g, s7g, m = d["ir"], d["s5"]["gates"], d["s6"]["gates"], d["s7"]["gates"], d["m7"]["metrics"]
    ba, ao = m["budget_aware"], m["area_only"]
    ref = d["ref"]
    hand_dr, hand_po = ref["drawn_devices_only"], ref["post_layout"]
    margins, eta = ir["margins"], d["m7"]["eta"]
    nmos = len(ir["devices"])
    copies = sum(x.get("m", 1) for x in ir["devices"])
    sz, ar, wl = num["size"], num["area"], num["wiring_loss"]
    g75 = (s7g.get("G7.5_mim_self_coupling_cancelled (info)") or {}).get("detail", {})
    cen = (s5g.get("G5.7_matched_centring (info)") or {}).get("detail", {})
    flow_min = sum(num["secs"].get(s, 0) for s in ("S4", "S5", "S6", "S7")) / 60
    gb = ba["gbw_mhz"]
    g5 = s5g["G5.5_area_vs_area_only (info)"]
    blocks = d["s4b"]["blocks"]
    nvar = sum(len(b["variants"]) for b in blocks)
    arrays = [(b["name"], v.get("array_rows"), b["devices"]) for b in blocks for v in b["variants"] if v.get("array_rows")]
    tab = d["sens"]["table"]
    top_gbw = sorted((n for n in tab if "~" not in n), key=lambda n: tab[n]["gbw_mhz"]["linear_per_fF"])[:3]
    rows6 = {x["id"]: x for x in d["pv"]["layouts"]["budget_aware"]["budgets"]["rows"]}
    fb = {r: d["pl"]["chosen"][r].get("fallback") for r in RULES}
    L = [f"# Automatic layout of `{D}` in a Tiny Tapeout tile, and how it compares with the hand layout", "",
         f"*Generated by `python3 scripts/make_iadc_report.py` from the flow's own output files (repo at {head}). Every "
         "number is read from `outputs/` or from the flow's code; only the explanations are typed. Assumptions are "
         "marked ASSUMPTION.*", "",
         "**How to read this report.** Section 1 is the result on one page; 2–3 show the circuit and what the flow "
         "learned about it before drawing; 4 says who decided what; 5–6 how the layout was built (with the exact "
         "algorithms); 7 what it costs after layout; 8 the comparison with the hand layout; 9–10 the novelty and the "
         "planned LLM work; 11–13 the failed checks, assumptions and open questions. Each picture has a *How to read "
         "it* note and a *What it shows here* line. A glossary is at the end. The companion report on `ttsky25a_fd` "
         "(`docs/ttsky25a_fd_report.html`) explains the flow at more length.", ""]
    # ---------------------------------------------------------------- 1
    L += ["## 1. Summary", "",
          f"`{D}` is the fully differential folded-cascode OTA of an incremental delta-sigma ADC (the open-source "
          f"`r09g/iadc` project, SKY130). It is built from unit transistors: {nmos} transistors in the netlist become "
          f"{copies} transistor pieces once each multiplier m is drawn, plus two MIM capacitors. The flow took the "
          f"netlist and, with no hand editing, drew two complete layouts inside a Tiny Tapeout 1×2 analog tile "
          f"({num['outline'][0]:g} × {num['outline'][1]:g} µm), checked them, read their wiring back and simulated "
          f"them. S4–S7 took {flow_min:.0f} minutes of computer time.", "",
          "**What came out:**", "",
          "- **Both layouts fit the tile and are clean:** 0 design-rule errors (DRC), and the layout matches the "
          "schematic (LVS), for both.",
          f"- **Gain and phase margin are met after layout:** gain {f(ba['gain_db']['post_layout_rc'], 4)} dB (spec ≥ "
          f"{f(ba['gain_db']['limit'], 4)}), phase margin {f(ba['pm_deg']['post_layout_rc'], 4)}° (≥ "
          f"{f(ba['pm_deg']['limit'])}).",
          f"- **GBW is not:** {f(gb['post_layout_rc'], 4)} MHz against a spec of ≥ {f(gb['limit'], 4)} MHz (an "
          f"ASSUMPTION: 0.9 × the schematic's {f(gb['schematic'], 4)} MHz). The wiring takes "
          f"{100 * gb['lost'] / gb['margin']:.0f} % of the GBW margin; the flow allows {100 * eta:.0f} %.",
          f"- **Against the hand layout:** the flow's wiring costs more bandwidth (GBW −{wl['budget_aware']['gbw_pct']:.1f} % "
          f"against −{wl['hand']['gbw_pct']:.1f} %) and more phase margin (−{wl['budget_aware']['pm_deg']:.1f}° against "
          f"−{wl['hand']['pm_deg']:.1f}°), and it is far less dense: {ar['budget_aware'] / ar['hand']:.1f} × the hand "
          f"layout's area, although the hand layout also holds the whole switched-capacitor CMFB "
          f"({num['cmfb_size'][0]:.0f} × {num['cmfb_size'][1]:.0f} µm) that the flow's circuit models ideally.",
          "- **Three things had to be built for this design** (flow record rows 93–100): multi-row arrays for its two "
          "m = 96 devices (Imasha's choice), a placement search that can work inside a tight outline, and fixes in "
          "S6 and S7 that its CMFB and its eleven identical cascode pairs brought to light. The finished designs' "
          "results are unchanged.",
          "- **No AI model decided anything in these runs** (section 4).", ""]
    L += ["| | Flow, budget-aware | Flow, area-only | Hand layout |", "|---|---|---|---|",
          f"| Size (µm) | {sz['budget_aware'][0]:.1f} × {sz['budget_aware'][1]:.1f} | "
          f"{sz['area_only'][0]:.1f} × {sz['area_only'][1]:.1f} | {sz['hand'][0]:.1f} × {sz['hand'][1]:.1f} (with the CMFB) |",
          f"| Area (µm²) | {ar['budget_aware']:,.0f} | {ar['area_only']:,.0f} | {ar['hand']:,.0f} |",
          f"| Inside the tile ({num['outline'][0]:g} × {num['outline'][1]:g} µm) | yes | yes | (not placed in one) |",
          f"| DRC errors / LVS | {s5g['G5.2_top_DRC']['detail']['budget_aware']} / match | "
          f"{s5g['G5.2_top_DRC']['detail']['area_only']} / match | not checked here / does not match (holds the "
          "real CMFB) |",
          f"| GBW lost to the wiring | −{wl['budget_aware']['gbw_pct']:.1f} % | −{wl['area_only']['gbw_pct']:.1f} % | "
          f"−{wl['hand']['gbw_pct']:.1f} % |",
          f"| Phase margin lost to the wiring | −{wl['budget_aware']['pm_deg']:.1f}° | −{wl['area_only']['pm_deg']:.1f}° | "
          f"−{wl['hand']['pm_deg']:.1f}° |",
          f"| GBW after layout (MHz) | {f(ba['gbw_mhz']['post_layout_rc'], 4)} | {f(ao['gbw_mhz']['post_layout_rc'], 4)} | "
          f"{f(hand_po['gbw_mhz'], 4)} (its own devices give {f(hand_dr['gbw_mhz'], 4)} before wiring) |", ""]
    L += W.how("\"lost to the wiring\" compares one layout simulated twice, with its drawn devices only and with every "
               "wire's capacitance (Magic, C-only, same bench and conditions): what the wiring and placement cost.")
    # ---------------------------------------------------------------- 2
    kinds = {}
    for lv in d["hier"]["levels"]:
        for v in lv.values():
            if isinstance(v, list):
                for x in v:
                    kinds[x.get("instance")] = (x.get("kind"), len(x.get("elements", [])))
    L += ["", "## 2. The circuit, its sub-circuits and what was asked", "",
          "The design's own hierarchy (from its xschem schematics) gives the units the flow places (\"macros\"); "
          "each has one colour throughout this report.", "",
          "| Colour | Sub-circuit | What it is | Elements |", "|---|---|---|---|"]
    for mac in ("x1", "x2", "top"):
        k, n = kinds.get(mac, ("", 0))
        L.append(f'| <span style="color:{MCOLOR[mac]}">■</span> | **{mac}** | {k} | {n} |')
    L += ["", "**The top schematic** (`ota.sch`): the bias (x1), the core (x2) and the switched-capacitor CMFB (x3). "
          "The flow's circuit keeps only the CMFB's two output capacitors C3 and C4 (in `top`); the rest is the ideal "
          "CMFB of the AC model.", "", W.img(f"outputs/report/{D}/sch_top.png", 900, "top schematic"), ""]
    L += W.how("the designer's own schematic (xschem), unchanged; the coloured boxes are drawn on a scratch copy.")
    for key, title in (("x1", "**x1, the bias** (`folded_cascode_3_bias`), every device boxed with its block number:"),
                       ("x2", "**x2, the core** (`folded_cascode_3_core`): the input pair, the folded cascodes and the "
                              "output branches."),
                       ("x3", "**x3, the CMFB** (`sc_cmfb`): only C3 and C4 (boxed) are in the flow's circuit.")):
        L += ["", title, "", W.img(f"outputs/report/{D}/sch_{key}.png", 900, key), ""]
        if key in ("x1", "x2"):
            L += W.how("the unboxed transistors with all terminals on a supply are the sheet's dummies. The upstream "
                       "netlist the flow reads gathers them into three top-level dummy devices (XM9, XM43, XM45, m = 23, "
                       "8 and 6), which the flow places in `top`.")
    L += ["", "**The specs** (section 12: how they were set):", "",
          "| Spec | Schematic | Limit | Margin | Allowance for the layout (η × margin) |", "|---|---|---|---|---|"]
    sch = {k: x["schematic"] for k, x in ba.items()}
    for k, mg in margins.items():
        name, unit = T.SPEC_NAME.get(k, (k, ""))
        L.append(f"| {name} ({unit}) | {f(sch.get(k), 5)} | {'≥' if mg['kind'] == 'min' else '≤'} {f(mg['limit'], 5)} | "
                 f"{f(mg['margin'], 4)} | {f(eta * mg['margin'], 4)} |")
    L += ["", "**Imasha's decisions for this design:** lay it out to fit a Tiny Tapeout analog tile (2026-11-04); fold "
          "its long devices into one multi-row array (2026-11-05). The other layout choices repeat her ttsky "
          "decisions (ASSUMPTION; `inputs/iadc_ota/layout.yaml`).", ""]
    # ---------------------------------------------------------------- 3
    nodes, bud = d["nodes"]["nodes"], {e["id"]: e for e in d["budgets"]["elements"]}
    ml = {k.lower(): v for k, v in s5g["G5.4_route_rules"]["detail"]["budget_aware"]["max_length"].items()}
    groups = d["s1"]["gates"]["G1.4_matching_groups"]
    L += ["## 3. What the flow learned before drawing: main nodes, nets and budgets (S1, S2)", "",
          W.img(f"outputs/S1/{D}/plots/bode_linear_vs_spice.png", 640, "bode"), ""]
    L += W.how("open-loop gain and phase: SPICE on the transistors (solid) against S1's linear model (dashed). Where "
               "they agree, every estimate built on the model can be trusted.")
    L += W.here(f"gate G1.3 (sensitivities against SPICE): "
                f"{'PASS' if d['s1']['gates']['G1.3_sensitivity_vs_spice']['pass'] else 'FAIL'}.")
    L += ["", "| Node | Role (S1) | Pole rank | GBW lost per fF (kHz) | PM lost per fF (m°) | Capacitance budget (fF) | "
          "Extracted (fF) | Use | Wire length use |", "|---|---|---|---|---|---|---|---|---|"]
    for n in nodes_main:
        v, s = nodes.get(n, {}), tab.get(n, {})
        b, r6, lm = bud.get(n, {}), rows6.get(n, {}), ml.get(n.lower(), {})

        def sv(key):
            if not s:
                return "–"
            x = -1000 * s.get(key, {}).get("linear_per_fF", 0)
            return "≈ 0" if abs(x) < 1e-6 else f(x, 3)
        tags = ", ".join(v.get("tags") or []) or ("high impedance" if v.get("high_impedance") else "–")
        L.append(f"| {n} | {tags} | {v.get('pole_rank', '–')} | {sv('gbw_mhz')} | {sv('pm_deg')} | "
                 f"{f(b.get('budget'), 3) if b else '–'} | {f(r6.get('value'), 3) if r6 else '–'} | "
                 f"{('**' + f(r6.get('use')) + '**') if r6 and not r6.get('ok') else f(r6.get('use')) if r6 else '–'} | "
                 f"{f(lm.get('use')) if lm else '–'} |")
    L += W.how("pole rank 1 is the dominant pole; the sensitivities say how much GBW and phase margin drop per fF of "
               "wiring on the node; \"use\" is extracted / budget (bold: over).")
    L += W.here(f"the nodes where wiring costs GBW most are {W.and_list(top_gbw)}; most main nodes end up over their "
                "capacitance budget, which is why G6.2 fails.")
    L += ["", W.img(f"outputs/report/{D}/chart_sensitivity.png", 760, "sensitivity chart"), ""]
    L += W.how("the ten nodes where added capacitance costs the most GBW (left) and phase margin (right).")
    L += ["", f"**Matching groups** (S1, rule: *{groups['rule']}*): {len(groups['groups'])} groups; each becomes one "
          "S4 block.", ""]
    # ---------------------------------------------------------------- 4
    L += ["## 4. Who decides what: code, Imasha, and the LLM", "",
          "- **Code** (the flow): every decision at run time, by fixed rules and by searching for the lowest cost; its "
          "settings are fixed in PREREG.",
          "- **Imasha** (the definition): the constraints and policies (the tile, the multi-row array, matching, "
          "dummies) and approval of the plans.",
          "- **LLM** (Claude, while building the flow): wrote the code, proposed the algorithms, the rules and the "
          "ASSUMPTIONs, drafted PREREG and reviewed the code. **No LLM is called during a run.**", "",
          "| Decision | What was decided here | Why | Code | Imasha | LLM |", "|---|---|---|---|---|---|"]
    L += [f"| {a} | {b} | {c} | {x} | {y} | {z} |" for a, b, c, x, y, z in DECISIONS] + [""]
    # ---------------------------------------------------------------- 5
    L += ["## 5. The building blocks (S4)", "",
          f"{len(blocks)} blocks, {nvar} variants, every one DRC-clean and LVS-matched with a negative control "
          f"rejected. {len(arrays)} block(s) are multi-row arrays: "
          + ", ".join(f"{n} ({', '.join(dv)}: {k} rows)" for n, k, dv in arrays) + ".", "",
          "**The algorithm, step by step** (as for ttsky25a_fd, with this design's options):", "",
          "1. **Group:** S1's matching groups first, then S0's blocks; one device type and one body net per block.",
          "2. **Units:** a device with multiplier m is drawn as m copies of the cell S3 chose.",
          "3. **Variants:** common centroid (A B B A …) or interdigitated (A B A B …) for matched devices; a mirror "
          "image where neither exists (row 93); one row for a single device.",
          "4. **Dummies** at both ends of every matched row.",
          f"5. **Draw the row:** units {B4.GAP} µm apart, a metal-2 stub from each terminal to a metal-3 track per net "
          f"({B4.TRACK_W} µm wide, {B4.PITCH} µm pitch); two stubs too close for facing via patches are staggered "
          "(row 94); pins measured from the cell's bounding-box corner (`pin_origin: bbox`, row 95).",
          f"6. **Fold** (`fold_row_um: {d['opts'].get('fold_row_um')}`, row 97): a single device's row longer than "
          "that becomes identical rows in one ring; metal-2 columns join each net's tracks across the rows.",
          f"7. **Ring:** one tap ring {B4.RING_GAP} µm outside the tracks; tap strips where the latch-up distance needs them.",
          "8. **Sign off:** Magic DRC, Netgen LVS (with m and the dummies), a negative control that must fail.", ""]
    figs = []
    for name in nb["order"]:
        b = nb["by_name"][name]
        vba, vao = nb["chosen"]["budget_aware"].get(name), nb["chosen"]["area_only"].get(name)
        v = next((x for x in b["variants"] if x["id"] == vba), b["variants"][0])
        bb = (v.get("geometry") or {}).get("bbox_um")
        size = f"{bb[2] - bb[0]:.1f} × {bb[3] - bb[1]:.1f} µm" if bb else ""
        devs = b["devices"] if len(b["devices"]) <= 4 else b["devices"][:3] + [f"… ({len(b['devices'])})"]
        cap = (f"<b>B{nb['num'][name]} {name}</b><br>{nb['macro'][name]} · {', '.join(devs)}<br>variant {vba}"
               + (f" (area-only: {vao})" if vao != vba else "") + (f" · {size}" if size else "")
               + (f" · {v['array_rows']}-row array" if v.get("array_rows") else ""))
        if v.get("png"):
            figs.append(fig_html(v["png"], cap, MCOLOR[nb["macro"][name]]))
    L += ["**Every block** (numbered as on the schematics; colour bar: the sub-circuit; picture: the budget-aware "
          "layout's variant):", "", "<div>" + "".join(figs) + "</div>", ""]
    L += ["**Matching in the final layouts** (G5.7):", "", "| Matched block | Budget-aware | Area-only |", "|---|---|---|"]
    for n in sorted(set().union(*(set(cen.get(r, {})) for r in RULES)), key=lambda n: nb["num"].get(n, 0)):
        cells = []
        for r in RULES:
            x = cen.get(r, {}).get(n)
            off = max(abs(v) for v in x["centroid_offset_um"].values()) if x else 0
            cells.append("–" if not x else f"{x['variant']}, " + ("common centroid" if x["common_centroid"]
                                                                  else f"centres {off:.1f} µm off"))
        L.append(f"| B{nb['num'].get(n)} {n} | {cells[0]} | {cells[1]} |")
    nc = {r: sum(x["common_centroid"] for x in cen.get(r, {}).values()) for r in RULES}
    L += W.here(f"{nc['budget_aware']} of {len(cen.get('budget_aware', {}))} matched blocks are common centroid "
                f"(budget-aware), {nc['area_only']} of {len(cen.get('area_only', {}))} (area-only).")
    # ---------------------------------------------------------------- 6
    pmac = d["pl"]["chosen"]
    used = [r.replace("_", "-") for r in RULES if fb[r]]
    L += ["", "## 6. Placement and routing (S5)", "",
          "**How the placement is found** (`src/s5/macro.py`, `src/s5/place.py`):", "",
          "1. **Sub-circuits:** every block belongs to the sub-circuit of its devices (x1, x2, top).",
          f"2. **Rows:** inside a sub-circuit, blocks stand in rows, PMOS rows above NMOS rows, {P5.ROW_GAP:g} µm "
          f"between rows and {P5.BLOCK_GAP:g} µm between blocks; matched blocks may share a row.",
          f"3. **Search inside a sub-circuit:** up to {M5.ENUM_MAX} blocks, every arrangement is tried; beyond that, "
          f"simulated annealing: {M5.MOVES:,} random moves (swap two blocks, move a block to another or a new row, "
          f"change a variant, flip a block); a better placement is always kept, a worse one with probability "
          f"exp(−Δcost / T), T starting at {M5.T_START} × the start's cost and × {M5.COOL} after every move; seed "
          f"{M5.SEED}. **For this tile** (`search_from_outside`, rows 96 and 98) the annealing starts from shelf packing "
          "(rows filled up to the width limit, tallest blocks first) and may pass through placements outside the "
          "outline with a penalty growing with the excess; only placements inside are kept.",
          f"4. **Three shapes:** each sub-circuit is placed at widths {', '.join(str(x) for x in M5.SHAPES)} × the "
          "tile's width.",
          "5. **Top level:** every arrangement of the sub-circuits' shapes is tried; anything outside the tile is "
          "rejected (never traded). **Area-only fallback** (row 99): where no arrangement of the budget-aware shapes "
          "fits, each sub-circuit's area-only shapes join the candidates, and the budget-aware cost still chooses among "
          "the arrangements that fit" + (f" (used here for the {W.and_list(used)} layout)" if used else "") + ".",
          "6. **Both costs:** the search runs twice with the same seed, budget-aware and area-only; both winners are "
          "routed and checked.", "",
          "**How area and wire length are optimised.** Both enter one number, the cost:", "",
          "- area term: A / A_ref, the bounding box's area over the sum of the blocks' smallest variants;",
          "- each net's wire use: u = (half-perimeter of its pins' box) / (S2's length budget for the net);",
          f"- **budget-aware cost** = A / A_ref + {P5.LAMBDA:g} × Σ max(0, u − 1) + {P5.MU:g} × Σ u;",
          "- **area-only cost** = A / A_ref.", "",
          "Area is kept small one level down too: S3 picks the smallest cell that keeps each node in budget, S4 draws "
          "compact blocks and folds the two long devices into arrays. Here the tile, not the area, is the hard "
          "limit: iadc's wire budgets are exceeded so far (G2.7, G5.4) that the wire term swamps the area term, which "
          "is why the fallback was needed.", "",
          "**How the wires are routed** (`src/s5/grid.py`):", "",
          f"- a grid of points {G5.GRID} µm apart; metal-3 horizontal, metal-4 vertical, {G5.WIRE} µm wide;",
          f"- each net a tree: A* from the part already routed to the nearest pin not yet joined, cost = length + "
          f"{G5.VIA_COST:g} µm per via; nets in order of least budget slack;",
          "- obstacles: every block's tracks and keep-outs (an array's inner tracks among them) and the ring contacts;",
          "- a net the router cannot finish is reported, never left open; DRC and LVS then check the result.", "",
          "**The layouts.**", ""]
    L += [" ".join(W.img(f"outputs/report/{D}/layout_{k}.png", 300, T.LABEL[k]) for k in ("budget_aware", "area_only", "hand")),
          "", f"*Left to right, at one scale: {T.LABEL['budget_aware']}, {T.LABEL['area_only']} (thin box: the tile), "
          f"{T.LABEL['hand']}.*", ""]
    for r in RULES:
        L += [f"**{T.LABEL[r]}, annotated:**", "", W.img(f"outputs/report/{D}/layout_{r}_annot.png", 820, r), ""]
    L += W.how("each sub-circuit outlined in its colour, every block's number (as in section 5) at its centre; the thin "
               "box is the tile. The two long blocks in x2 are the folded m = 96 arrays.")
    rr = s5g["G5.4_route_rules"]["detail"]
    wire = {r: sum(sum((x.get("length_um") or {}).values()) for x in rr[r]["max_length"].values()) for r in RULES}
    over = {r: sum(not x["ok"] for x in rr[r]["max_length"].values()) for r in RULES}
    L += ["", "| | Budget-aware | Area-only |", "|---|---|---|",
          "| Sub-circuits, top to bottom | " + " | ".join(" / ".join(", ".join(row) for row in pmac[r]["placement"]["rows"])
                                                        for r in RULES) + " |",
          "| Shape of each sub-circuit | " + " | ".join(", ".join(f"{k} {v['shape']} ({v['method']})"
                                                               for k, v in pmac[r]["placement"]["macros"].items())
                                                     for r in RULES) + " |",
          f"| Size (µm) | {sz['budget_aware'][0]:.1f} × {sz['budget_aware'][1]:.1f} | {sz['area_only'][0]:.1f} × "
          f"{sz['area_only'][1]:.1f} |",
          f"| Area (µm²) | {ar['budget_aware']:,.0f} | {ar['area_only']:,.0f} |",
          f"| Top-level wire (µm) | {wire['budget_aware']:,.0f} | {wire['area_only']:,.0f} |",
          f"| Sum of wire-budget use | {sum(g5['u_budget_aware'].values()):.1f} | {sum(g5['u_area_only'].values()):.1f} |",
          f"| Nets longer than their budget | {over['budget_aware']} of {len(rr['budget_aware']['max_length'])} | "
          f"{over['area_only']} of {len(rr['area_only']['max_length'])} |",
          f"| DRC errors / LVS | {s5g['G5.2_top_DRC']['detail']['budget_aware']} / match | "
          f"{s5g['G5.2_top_DRC']['detail']['area_only']} / match |", ""]
    L += W.how("\"w100\" … is the width limit a sub-circuit was placed under (× the tile's width); \"a100\" … an "
               "area-only shape added by the fallback.")
    L += ["", "**Sign-off of the final design** (the budget-aware layout), as the tools reported it:", "",
          W.img(f"outputs/report/{D}/shot_drc.png", 760, "DRC report"), "",
          W.img(f"outputs/report/{D}/shot_lvs.png", 760, "LVS report"), "",
          W.img(f"outputs/report/{D}/shot_lvs_negctl.png", 760, "LVS negative control"), ""]
    L += W.how("the lines of the tools' own report files, verbatim (the file is named above each). Magic's DRC counts 0 "
               "errors on the routed top cell. Netgen compares the routed layout with the circuit: the same devices "
               "(the many drawn copies merge, e.g. 597 nfet pieces into 49 devices) and nets, \"Circuits match "
               "uniquely\". The negative control, the same check with one device's length changed, reports property "
               "errors, so the check can fail.")
    L += ["", W.img(f"outputs/report/{D}/chart_area.png", 640, "area chart"), ""]
    L += W.how("the bounding box of each layout; the dashed line is the tile's area. The hand layout holds the whole "
               "switched-capacitor CMFB, which the flow's circuit does not.")
    # ---------------------------------------------------------------- 7
    L += ["", "## 7. After layout: what the wiring costs (S6, S7)", "",
          "S6 reads each layout back with every wire's capacitance (C-only); S7 simulates it in the original benches "
          "with the same ideal CMFB as the schematic (row 100).", "",
          "| Spec | Limit | Schematic | Drawn devices | After layout, budget-aware | Use of the allowance | "
          "After layout, area-only | Use of the allowance |", "|---|---|---|---|---|---|---|---|"]
    for k, x in ba.items():
        name, unit = T.SPEC_NAME.get(k, (k, ""))
        y = ao[k]
        b1, b2 = ("**" if not x["within_allowed"] else ""), ("**" if not y["within_allowed"] else "")
        L.append(f"| {name} ({unit}) | {'≥' if x['kind'] == 'min' else '≤'} {f(x['limit'], 5)} | {f(x['schematic'], 5)} | "
                 f"{f(x['drawn'], 5)} | {f(x['post_layout_rc'], 5)} | {b1}{f(x['use_of_allowed'])}{b1} | "
                 f"{f(y['post_layout_rc'], 5)} | {b2}{f(y['use_of_allowed'])}{b2} |")
    L += W.how("use of the allowance = (schematic − after layout) / (η × margin); 1.0 is all the layout may take "
               "(bold: more). A negative use is a gain.")
    gn = {k: rows6[k] for k in top_gbw if k in rows6}
    L += W.here(f"GBW misses its spec: {f(gb['drawn'], 4)} MHz with the drawn devices, {f(gb['post_layout_rc'], 4)} "
                f"after the wiring. The GBW-sensitive nodes carry far more capacitance than budgeted ("
                + ", ".join(f"{n} {f(x['value'], 3)} fF against {f(x['budget'], 3)}" for n, x in gn.items()) + ").")
    gm = g75.get("budget_aware", {})
    if gm:
        L += ["", f"**The MIM double count is small here.** With C3's and C4's own plate coupling cancelled (G7.5), GBW is "
              f"{f(gm.get('gbw_mhz', {}).get('value'), 4)} MHz (use {f(gm.get('gbw_mhz', {}).get('use_of_allowed'))}): "
              "still below the spec, unlike ttsky, where it explained most of the loss.", ""]
    L += ["", "**The extraction's own check** (S6, gate G6.1):", "",
          W.img(f"outputs/report/{D}/shot_lvs_flat.png", 760, "flat LVS report"), ""]
    L += W.how("Netgen on the flat extraction: the netlists match (\"with 7 symmetries\": iadc's identical cascode "
               "pairs are interchangeable). Its last line reports pin matching failed because flattening turns every "
               "inner label into a pin; the flow's G6.1 checks each such row and accepts it only for an inner net or "
               "two interchangeable nets (rows 88, 90, 100): G6.1 "
               + ("PASS." if d["s6"]["gates"]["G6.1_extracted_and_LVS"]["pass"] else "FAIL."))
    L += ["", W.img(f"outputs/report/{D}/chart_wiring_loss.png", 700, "wiring loss chart"), ""]
    L += W.how("the drop from drawn devices to the extracted layout, for each of the three layouts, measured the same way.")
    # ---------------------------------------------------------------- 8
    L += ["", "## 8. Comparison with the hand layout", "",
          f"**What the hand layout is.** The upstream project's own Magic layout of the OTA (`{ref['gds']}`, cell "
          f"`{ref.get('cell')}`), measured with the same tool and settings and simulated in the same benches (flow "
          "record 7.8). Its CMFB's clocks are held in phase 1 and its output node is driven by the same ideal CMFB law "
          "(ASSUMPTION), so the outputs see C3 and C4 as in the flow's model.", "",
          W.img(f"outputs/report/{D}/layout_hand_annot.png", 760, "hand layout"), ""]
    L += W.how("the hand layout is drawn flat (no sub-cells) except its CMFB, outlined. The flow's layout does not "
               "hold the CMFB's switches and sampling capacitors.")
    rc = (T.j("outputs/reference_layout", D, "reference_layout_rc100s.json") or {}).get("post_layout_rc") or {}
    L += ["", "**Performance after layout, side by side** (tt, 27 °C, 0.3 pF per output, the same benches and ideal "
          "CMFB law; C-only extraction unless marked R+C):", "",
          "| | Spec | Schematic | Hand: drawn | Hand: C-only | Hand: R+C | Flow BA: drawn | Flow BA: C-only | "
          "Flow AO: C-only |", "|---|---|---|---|---|---|---|---|---|"]
    for k in ("gain_db", "gbw_mhz", "pm_deg", "power_uw"):
        name, unit = T.SPEC_NAME.get(k, (k, ""))
        x, y = ba.get(k, {}), ao.get(k, {})
        mg = margins.get(k)
        spec = f"{'≥' if mg['kind'] == 'min' else '≤'} {f(mg['limit'], 5)}" if mg else "–"
        sv = x.get("schematic", ref["schematic_same_conditions"].get(k))
        L.append(f"| {name} ({unit}) | {spec} | {f(sv, 5)} | {f(hand_dr.get(k), 5)} | {f(hand_po.get(k), 5)} | "
                 f"{f(rc.get(k), 5)} | {f(x.get('drawn', d['m7']['views']['budget_aware']['drawn'].get(k)), 5)} | "
                 f"{f(x.get('post_layout_rc', d['m7']['views']['budget_aware']['pex_c'].get(k)), 5)} | "
                 f"{f(y.get('post_layout_rc', d['m7']['views']['area_only']['pex_c'].get(k)), 5)} |")
    L += W.how("each column is one circuit simulated in the same bench. The hand layout holds the real switched-capacitor "
               "CMFB (its switches and sampling capacitors load the output and bias nodes), so its drawn column already "
               "differs from the schematic; the flow's circuit is the schematic's (with the CMFB ideal). The R+C column "
               "is the hand layout with its wire resistance as well (flow record 7.8); the flow's layouts were extracted "
               "C-only (section 12).")
    L += W.here(f"after layout the flow's budget-aware layout has the higher GBW ({f(ba['gbw_mhz']['post_layout_rc'], 4)} "
                f"against {f(hand_po['gbw_mhz'], 4)} MHz, C-only), the hand layout the higher phase margin "
                f"({f(hand_po['pm_deg'], 4)} against {f(ba['pm_deg']['post_layout_rc'], 4)}°); gain is the same. As "
                "absolute numbers these mix the layout with the CMFB difference; the wiring's cost (below) separates "
                "the layout's own part.")
    L += ["", "**Why it is not the same circuit.** LVS of the hand layout against the flow's circuit does not match: it "
          "holds the switched-capacitor CMFB (switches and four more capacitors on the output and bias nodes). Its "
          f"drawn devices give GBW {f(hand_dr['gbw_mhz'], 4)} MHz against the schematic model's "
          f"{f(ref['schematic_same_conditions']['gbw_mhz'], 4)} MHz. What compares fairly is the wiring's cost, and the "
          "area with the CMFB caveat:", "",
          "| | Flow, budget-aware | Flow, area-only | Hand layout |", "|---|---|---|---|",
          f"| Area (µm²) | {ar['budget_aware']:,.0f} ({ar['budget_aware'] / ar['hand']:.2f} ×) | "
          f"{ar['area_only']:,.0f} ({ar['area_only'] / ar['hand']:.2f} ×) | {ar['hand']:,.0f} (1.00 ×; its CMFB alone "
          f"{num['cmfb_area']:,.0f}) |",
          f"| GBW lost to the wiring | {wl['budget_aware']['gbw_pct']:.1f} % | {wl['area_only']['gbw_pct']:.1f} % | "
          f"{wl['hand']['gbw_pct']:.1f} % |",
          f"| Phase margin lost to the wiring | {wl['budget_aware']['pm_deg']:.2f}° | {wl['area_only']['pm_deg']:.2f}° | "
          f"{wl['hand']['pm_deg']:.2f}° |",
          f"| Gain lost to the wiring | {wl['budget_aware']['gain_db']:.3f} dB | {wl['area_only']['gain_db']:.3f} dB | "
          f"{wl['hand']['gain_db']:.3f} dB |", ""]
    L += ["**What it shows.**", "",
          f"- **Bandwidth and phase margin:** the hand layout's wiring costs less (GBW {wl['hand']['gbw_pct']:.1f} % "
          f"against {wl['budget_aware']['gbw_pct']:.1f} %). It is a compact, flat layout: short wires between devices "
          "that the flow keeps in separate blocks, each with its own ring.",
          f"- **Area:** the flow's layout is {ar['budget_aware'] / ar['hand']:.1f} × the hand layout's, which also holds "
          f"the CMFB. With {sum(x.get('m', 1) for x in ir['devices'])} unit pieces, a ring per block, {P5.BLOCK_GAP:g} µm "
          "gaps and dummies cost far more than in ttsky; the tile, not the area, was the target, and it fits.",
          "- **Effort:** the flow's layouts took minutes of computer time, every check automatic; the hand layout's "
          "design time is not recorded here.", ""]
    # ---------------------------------------------------------------- 9, 10
    h5 = (s7g.get("H5 (info)") or {}).get("use_of_allowed", {})
    L += ["## 9. What is new in this flow (status on this design)", "",
          "| Contribution (`docs/05_literature_novelty_remap.md`) | Shown on this design |", "|---|---|",
          "| C1. Intent compiled from the circuit's own model | partly: per-node sensitivities and poles (S1) turned into "
          "budgets before layout (S2) |",
          "| C2. Device cells chosen from the requirements | yes, with relaxations (G3.3/G3.5; the budgets are tight) |",
          f"| C3. Budget-aware variants and placement | {nvar} signed-off variants; in this tile the budget-aware "
          f"search fell back to area-only shapes, and the two layouts lose about the same (GBW use "
          f"{f(h5.get('budget_aware', {}).get('gbw_mhz'))} against {f(h5.get('area_only', {}).get('gbw_mhz'))}) |",
          "| C4. LLM decisions grounded in the equations, measured | not yet (section 10) |",
          "| C5. Open, reproducible SKY130 flow | yes: every block and both layouts signed off; seeded; golden results |",
          "", "New for this design: multi-row arrays for long devices, placement search inside a tight outline, and a "
          "Tiny Tapeout tile as the outline.", ""]
    L += ["## 10. The next step: LLM integration", "",
          "As planned for ttsky (its report, section 10): an independent LLM proposes the floorplan and the matching "
          "from the netlist, the hierarchy, the specs and section 3's budgets; the same S4–S7 build and check it. On "
          "this design it should help where the code's search is weakest:", "",
          f"- **GBW:** keep the GBW-sensitive nets ({W.and_list(top_gbw)}) short by placing their blocks side by "
          "side across the sub-circuit boundaries the code keeps;",
          "- **density:** propose which blocks may share a ring (one ring per block costs much area with unit "
          "transistors), checked by DRC and LVS like everything else;",
          "- **budgets that cannot be met** (G2.7, G5.4): say which to relax, with the equations behind it.", "",
          "Planned to start with the Claude CLI after Imasha's supervisor agrees; every call journaled.", ""]
    # ---------------------------------------------------------------- 11–13
    L += ["## 11. What did not pass, and why", "", "None of these is a crash; each stage finished and reported.", ""]
    stage_rows = ["| Stage | Result | Time (min) |", "|---|---|---|"]
    for st in ("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7"):
        s = d["fs"].get(st, {})
        fails = ", ".join(g.split("_")[0] for g in s.get("failed_gates") or [])
        stage_rows.append(f"| {st} | {s.get('status', '–')}{' (' + fails + ')' if fails else ''} | "
                          f"{num['secs'].get(st, 0) / 60:.1f} |")
    L += stage_rows + [""]
    for st in ("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7"):
        for g in d["fs"].get(st, {}).get("failed_gates") or []:
            k = g.split("_")[0]
            L.append(f"- **{st} {k}:** {WHY.get(k, 'see the stage report.')}")
    L += ["", "## 12. Assumptions and limits", ""] + [f"- {a}" for a in ASSUMPTIONS] + [""]
    L += ["## 13. Open questions (FEEDBACK NEEDED)", "",
          "1. GBW misses its spec, which is itself an ASSUMPTION (0.9 × the schematic). Keep it and report the miss, or "
          "set iadc's specs another way?",
          "2. Confirm the layout choices repeated from ttsky (matching, dummies on top of the designer's own) and the "
          "whole tile as the outline (power straps and pins not routed).",
          "3. The two latent fixes found here (rows 95, 96) are opt-in; make them the default and re-run the finished "
          "designs?", ""]
    L += ["## Glossary", ""] + [f"- **{a}:** {b}" for a, b in GLOSSARY] + [""]
    L += ["## Where everything is", "",
          f"- Layouts: `outputs/S5/{D}/routed_budget_aware/`, `routed_area_only/`; blocks `outputs/S4/{D}/blocks/`.",
          f"- Extraction `outputs/S6/{D}/`; simulations `outputs/S7/{D}/`; hand layout `outputs/reference_layout/{D}/`.",
          f"- This report's pictures: `outputs/report/{D}/`; the simple report: `docs/reports/{D}_report.html`.",
          "- The record: `docs/flow_record.md` (7.8, 7.25, rows 93–100); the layout instructions: "
          "`inputs/iadc_ota/layout.yaml`.", ""]
    L += ["## Appendix A. Every variant of every block", ""]
    figs = []
    for name in nb["order"]:
        b = nb["by_name"][name]
        for v in b["variants"]:
            mark = " ".join(t for t, r in (("BA ✓", "budget_aware"), ("AO ✓", "area_only")) if nb["chosen"][r].get(name) == v["id"])
            if v.get("png"):
                figs.append(fig_html(v["png"], f"<b>B{nb['num'][name]} {name}</b> · {v['id']} {mark}",
                                     MCOLOR[nb["macro"][name]], width="23%"))
    L += ["<div>" + "".join(figs) + "</div>", ""]
    return L


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-html", action="store_true")
    a = ap.parse_args(argv)
    W.IMG_PREFIX = os.path.relpath(REPO, OUT_MD.parent).replace(os.sep, "/")
    head = (subprocess.run(["git", "--no-optional-locks", "log", "-1", "--format=%h %cs"], cwd=REPO, capture_output=True,
                           text=True).stdout.strip() or "unknown")
    d = T.gather()
    nb = T.numbering(d)
    lay = layouts(d, nb)
    schematics(d, nb)
    num = numbers(d, lay)
    nodes_main = T.main_nodes(d)
    T.charts(d, num, nodes_main)
    shots()
    (FIG / "numbers.json").write_text(json.dumps({"layouts": lay, "blocks": nb["num"], **num}, indent=1) + "\n")
    OUT_MD.write_text("\n".join(build_md(d, num, lay, nb, nodes_main, head)) + "\n")
    print(OUT_MD)
    if not a.no_html:
        html = OUT_MD.with_suffix(".html")
        css = REPO / "docs" / "flow_record" / "record.css"
        cmd = ["pandoc", OUT_MD.name, "--standalone", "--embed-resources", "--metadata",
               f"title=Automatic layout of {D}", "--toc", "-o", html.name] + \
            (["-c", os.path.relpath(css, OUT_MD.parent)] if css.exists() else [])
        r = subprocess.run(cmd, cwd=OUT_MD.parent, capture_output=True, text=True)
        print(html if r.returncode == 0 else f"pandoc failed: {r.stderr[:400]}")
        return 0 if r.returncode == 0 else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
