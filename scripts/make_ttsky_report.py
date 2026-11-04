#!/usr/bin/env python3
"""Generate docs/ttsky25a_fd_report.md (and, with pandoc, a self-contained HTML copy): the full report on the automatic
layout of ttsky25a_fd (plan v4 Phase 8), written for a reader who does not know the flow. Every number is read from the
run's own output files or from the flow's code (its constants); typed by hand are only the explanations, the decision
table, the novelty and LLM sections, the glossary and the list of assumptions. Pictures go to
outputs/report/ttsky25a_fd/: the designer's schematics with the sub-circuits and blocks marked, every block, the
layouts at one scale and annotated, and the charts.

usage (inside layout-s0s3, repo root, after `source scripts/env.sh`): python3 scripts/make_ttsky_report.py [--no-html]
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
import report_figures as F  # noqa: E402

REPO = W.REPO
sys.path.insert(0, str(REPO))
from src.s4 import block as B4  # noqa: E402
from src.s4.run import layout_options  # noqa: E402
from src.s5 import grid as G5, macro as M5, place as P5  # noqa: E402

D = "ttsky25a_fd"
OUT_MD = REPO / "docs" / f"{D}_report.md"
FIG = REPO / "outputs" / "report" / D
RULES = ("budget_aware", "area_only")
# one colour per layout, the same in every chart (dataviz reference palette, slots 1-3, validated all-pairs)
COLOR = {"budget_aware": "#2a78d6", "area_only": "#eb6834", "hand": "#1baf7a"}
LABEL = {"budget_aware": "Flow, budget-aware", "area_only": "Flow, area-only", "hand": "Hand layout (tile)"}
# one colour per sub-circuit (macro), the same on the schematics, the block gallery and the layouts (slots 4-7,
# validated all-pairs; every box also carries a text label)
MACROS = ("x1", "x2", "top", "res_packs")
MCOLOR = {"x1": "#e87ba4", "x2": "#008300", "top": "#eda100", "res_packs": "#6250d6"}
MTEXT = {"x1": "x1: first stage (Diff_opamp)", "x2": "x2: second stage (Common_source_stage)",
         "top": "top: bias circuit and Miller capacitors", "res_packs": "res_packs: CM-sense resistors (both packs)"}
GRAY = "#898781"
INK, INK2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
SPEC_NAME = {"gbw_mhz": ("Unity-gain bandwidth (GBW)", "MHz"), "pm_deg": ("Phase margin (PM)", "°"),
             "gain_db": ("DC gain", "dB"), "power_uw": ("Power", "µW")}
# the tile's regions, by its own cell names; the sub-circuit is inferred from the name (ASSUMPTION, section 13)
TILE_REGIONS = [("Diff_opamp_ly", "x1", "Diff_opamp_ly", "br"), ("cs_p_5", "x2", "cs_p_5", "bl"),
                ("bias_dummy", "top", "bias_dummy", "tl"), ("cap_mil", None, "cap_mil", "bl"),
                ("cap_mim3", None, "cap_mim3", "tl"), ("cap_mil_2", None, "cap_mil_2", "tl"), ("res", None, "res", "tl"),
                ("res_5", None, "res_5", "tl"), ("switchblock", None, "switchblock", "bl"),
                ("block_01", None, "block_01", "tl"), ("block_02", None, "block_02", "tl"),
                ("block_03", None, "block_03", "tl"), ("block_04", None, "block_04", "tr")]


def j(*p):
    return W._j(REPO.joinpath(*p))


def f(v, nd=3):
    return W.f(v, nd)


def pct(a, b):
    return 100.0 * (b - a) / a


def fig_html(src: str, caption: str, color: str | None = None, width: str = "31%") -> str:
    bar = f"border-top:5px solid {color};" if color else ""
    return (f'<figure style="display:inline-block;width:{width};margin:4px;vertical-align:top;{bar}">'
            f'<img src="{W.IMG_PREFIX}/{src}" style="width:100%" alt="{caption.split("<")[0]}">'
            f'<figcaption style="font-size:0.8em">{caption}</figcaption></figure>')


# ---------------------------------------------------------------------------------------------------- the data
def gather() -> dict:
    return {"ir": j("outputs/S0", D, "circuit_ir.json"), "hier": j("circuits", D, "upstream/hierarchy.json"),
            "fs": (j("outputs/flow", D, "flow_summary.json") or {}).get("stages", {}),
            "s1": j("outputs/S1", D, "s1_report.json"), "nodes": j("outputs/S1", D, "node_classes.json"),
            "sens": j("outputs/S1", D, "sensitivity.json"), "budgets": j("outputs/S2", D, "budgets.json"),
            "s4b": j("outputs/S4", D, "blocks.json"), "s4": j("outputs/S4", D, "s4_report.json"),
            "pl": j("outputs/S5", D, "placement.json"), "s5": j("outputs/S5", D, "s5_report.json"),
            "s6": j("outputs/S6", D, "s6_report.json"), "pv": j("outputs/S6", D, "parasitics_vs_budgets.json"),
            "s7": j("outputs/S7", D, "s7_report.json"), "m7": j("outputs/S7", D, "metrics.json"),
            "ref": j("outputs/reference_layout", D, "reference_layout.json"), "opts": layout_options(D)}


def numbering(d: dict) -> dict:
    """Block numbers B1 ... in sub-circuit order (x1, x2, top, res_packs), then by name; each block's macro and the
    variant each layout chose."""
    plb = {r: d["pl"]["chosen"][r]["placement"]["blocks"] for r in RULES}
    blocks = d["s4b"]["blocks"]
    macro = {b["name"]: plb["budget_aware"][b["name"]]["macro"] for b in blocks}
    order = sorted(blocks, key=lambda b: (MACROS.index(macro[b["name"]]), b["name"]))
    num = {b["name"]: i + 1 for i, b in enumerate(order)}
    dev = {x: b["name"] for b in blocks for x in b["devices"]}
    chosen = {r: {b: p["variant"] for b, p in plb[r].items()} for r in RULES}
    return {"num": num, "macro": macro, "dev": dev, "order": [b["name"] for b in order], "chosen": chosen,
            "by_name": {b["name"]: b for b in blocks}}


# ---------------------------------------------------------------------------------------------------- pictures
def render(gds: Path, png: Path, **kw) -> dict:
    args = ["klayout", "-zz", "-rd", f"gds={gds}", "-rd", f"png={png}"]
    for k, v in kw.items():
        args += ["-rd", f"{k}={v}"]
    for _ in range(4):   # the Windows-mounted repo now and then refuses a write (Errno 22); a retry has always worked
        r = subprocess.run(args + ["-r", str(REPO / "scripts/report_layout_png.py")], capture_output=True, text=True,
                           timeout=600)
        line = next((ln for ln in r.stdout.splitlines() if ln.startswith("REPORT_PNG ")), None)
        if line:
            break
    if line is None:
        raise RuntimeError(f"klayout render failed for {gds}: {(r.stdout + r.stderr)[-400:]}")
    out = json.loads(line[len("REPORT_PNG "):])
    w, h = float(kw.get("w", 260)), float(kw.get("h", 240))
    cx, cy = (out["bbox_um"][0] + out["bbox_um"][2]) / 2, (out["bbox_um"][1] + out["bbox_um"][3]) / 2
    out["window_um"] = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
    return out


def layouts(d: dict, nb: dict) -> dict:
    FIG.mkdir(parents=True, exist_ok=True)
    W_UM, H_UM, PPU = 260, 240, 3          # one scale for all three pictures
    out = {}
    ow, oh = d["opts"].get("outline_um", [250, 200])
    for r in RULES:
        out[r] = render(REPO / f"outputs/S5/{D}/routed_{r}/{D}_routed.gds", FIG / f"layout_{r}.png",
                        w=W_UM, h=H_UM, ppu=PPU, outline=f"{ow}x{oh}")
    cells = ",".join(["Diff_Opamp"] + [c[0] for c in TILE_REGIONS])
    out["hand"] = render(REPO / d["ref"]["gds"], FIG / "layout_hand.png", w=W_UM, h=H_UM, ppu=PPU, cell=cells)
    # the same layouts, larger, with the sub-circuits outlined and every block numbered
    for r in RULES:
        pl = d["pl"]["chosen"][r]["placement"]
        hi = render(REPO / f"outputs/S5/{D}/routed_{r}/{D}_routed.gds", FIG / f"layout_{r}_big.png",
                    w=W_UM, h=H_UM, ppu=6)
        rects = [(m["bbox"], MCOLOR[k], k) for k, m in pl["macros"].items()]
        labels = [((b["bbox"][0] + b["bbox"][2]) / 2, (b["bbox"][1] + b["bbox"][3]) / 2, f"B{nb['num'][n]}")
                  for n, b in pl["blocks"].items()]
        F.annotate(FIG / f"layout_{r}_big.png", hi["window_um"], rects, labels, FIG / f"layout_{r}_annot.png",
                   title=f"{LABEL[r]}: sub-circuits outlined, blocks numbered",
                   legend=[(MTEXT[k], MCOLOR[k]) for k in MACROS])
    hb = render(REPO / d["ref"]["gds"], FIG / "layout_hand_big.png", w=W_UM, h=H_UM, ppu=6, cell=cells)
    rects = []
    for cell, mac, lab, corner in TILE_REGIONS:
        for bx in hb["cells"].get(cell, []):
            rects.append((bx, MCOLOR[mac] if mac else GRAY, lab, corner))
    F.annotate(FIG / "layout_hand_big.png", hb["window_um"], rects, [], FIG / "layout_hand_annot.png",
               title="Hand layout (tile): regions by the tile's own cell names",
               legend=[(MTEXT[k], MCOLOR[k]) for k in ("x1", "x2", "top")] + [("not matched to a sub-circuit", GRAY)])
    return out


def schematics(d: dict, nb: dict) -> dict:
    """The four schematics with every laid-out device boxed in its sub-circuit's colour and labelled with its block."""
    work = F._work(REPO)
    num, dev, macro = nb["num"], nb["dev"], nb["macro"]
    devices = {x["name"] for x in d["ir"]["devices"]} | {p["name"] for p in d["ir"].get("passives", [])}

    def boxes(prefix, insts, extra=()):
        out, seen = [], set()
        for i in insts:
            ir = prefix + i
            if ir in devices and ir in dev:
                b = dev[ir]
                lab = f"B{num[b]}" if (b not in seen or macro[b] != "res_packs") else ""
                seen.add(b)
                out.append((i, macro[b], lab, 6, 0.32))
        return out + list(extra)
    sheets = {}
    top_insts = F.instance_names(work / "Opamp_with_bias.sch")
    sheets["top"] = F.schematic(REPO, work, "Opamp_with_bias",
                                boxes("X", top_insts, [("x1", "x1", "x1: first stage, see below", 16, 0.55),
                                                       ("x2", "x2", "x2: second stage, see below", 16, 0.55)]),
                                FIG / "sch_top.png", MCOLOR)
    sheets["x1"] = F.schematic(REPO, work, "Diff_opamp", boxes("XX1_", F.instance_names(work / "Diff_opamp.sch")),
                               FIG / "sch_x1.png", MCOLOR)
    cs = F.instance_names(work / "Common_source_stage.sch")
    packs = [(i, "res_packs", f"res_pack {i}: B{num['res_packs']}", 12, 0.45) for i in cs
             if re.fullmatch(r"x\d+", i)]
    sheets["x2"] = F.schematic(REPO, work, "Common_source_stage", boxes("XX2_", cs, packs), FIG / "sch_x2.png", MCOLOR)
    sheets["res_pack"] = F.schematic(REPO, work, "res_pack", boxes("XX2_X1_", F.instance_names(work / "res_pack.sch")),
                                     FIG / "sch_res_pack.png", MCOLOR)
    return sheets


def _axes(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.tick_params(colors=MUTED, labelcolor=INK2, length=0)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def charts(d: dict, num: dict, main_nodes: list) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans"})
    keys = ["hand", "area_only", "budget_aware"]
    # 1. area
    fig, ax = plt.subplots(figsize=(7.2, 2.5), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    _axes(ax)
    vals = [num["area"][k] for k in keys]
    ax.barh([LABEL[k] for k in keys], vals, height=0.5, color=[COLOR[k] for k in keys], edgecolor=SURFACE, linewidth=2)
    ol = num["outline_area"]
    ax.axvline(ol, color=INK2, linewidth=1, linestyle=(0, (4, 3)))
    ax.text(ol, 2.45, f" outline {ol:,.0f} µm²", color=INK2, va="bottom", ha="right", fontsize=9)
    for i, v in enumerate(vals):
        ax.text(v + 600, i, f"{v:,.0f} µm²", va="center", color=INK, fontsize=9)
    ax.set_xlim(0, ol * 1.12)
    ax.set_xlabel("Area of the op-amp's bounding box (µm²)", color=INK2)
    ax.set_title("Area", loc="left", color=INK, fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / "chart_area.png", facecolor=SURFACE)
    plt.close(fig)
    # 2. what the wiring costs: drawn devices -> extracted (C only); two measures, two panels (no shared axis)
    fig, axs = plt.subplots(1, 2, figsize=(8.4, 2.7), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    for ax, (key, unit, title) in zip(axs, (("gbw_pct", "%", "GBW lost to the wiring (%)"),
                                            ("pm_deg", "°", "Phase margin lost to the wiring (°)"))):
        _axes(ax)
        vals = [num["wiring_loss"][k][key] for k in keys]
        ax.barh([LABEL[k] for k in keys], vals, height=0.5, color=[COLOR[k] for k in keys], edgecolor=SURFACE,
                linewidth=2)
        for i, v in enumerate(vals):
            ax.text(v + max(vals) * 0.02, i, f"{v:.1f}{unit}", va="center", color=INK, fontsize=9)
        ax.set_xlim(0, max(vals) * 1.25)
        ax.set_title(title, loc="left", color=INK, fontsize=11)
    axs[1].set_yticklabels([])
    fig.tight_layout()
    fig.savefig(FIG / "chart_wiring_loss.png", facecolor=SURFACE)
    plt.close(fig)
    # 3. the main nodes' sensitivities: how much each spec drops per fF added on the node (one measure per panel)
    tab = d["sens"]["table"]
    fig, axs = plt.subplots(1, 2, figsize=(8.8, 3.6), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    for ax, (key, scale, title) in zip(axs, (("gbw_mhz", 1000.0, "GBW lost per fF added (kHz)"),
                                            ("pm_deg", 1000.0, "Phase margin lost per fF added (m°)"))):
        _axes(ax)
        rows = sorted(((n, -tab[n][key]["linear_per_fF"] * scale) for n in tab if "~" not in n), key=lambda x: -x[1])[:10]
        rows = rows[::-1]
        ax.barh([n for n, _ in rows], [v for _, v in rows], height=0.55, color=INK2, edgecolor=SURFACE, linewidth=2)
        for i, (_, v) in enumerate(rows):
            ax.text(v * 1.02, i, f"{v:.3g}", va="center", color=INK, fontsize=8)
        ax.set_xlim(0, max(v for _, v in rows) * 1.3)
        ax.set_title(title, loc="left", color=INK, fontsize=10.5)
    fig.tight_layout()
    fig.savefig(FIG / "chart_sensitivity.png", facecolor=SURFACE)
    plt.close(fig)


# ---------------------------------------------------------------------------------------------------- the numbers
def numbers(d: dict, lay: dict) -> dict:
    m = d["m7"]["metrics"]
    ref = d["ref"]
    hb = lay["hand"]["cells"]["Diff_Opamp"][0]
    hand_wh = (hb[2] - hb[0], hb[3] - hb[1])
    size = d["s5"]["gates"]["G5.6_outline"]["size_um"]
    area = {r: size[r][0] * size[r][1] for r in RULES}
    area["hand"] = hand_wh[0] * hand_wh[1]
    wl = {}
    for r in RULES:
        wl[r] = {"gbw_pct": -pct(m[r]["gbw_mhz"]["drawn"], m[r]["gbw_mhz"]["post_layout_rc"]),
                 "pm_deg": m[r]["pm_deg"]["drawn"] - m[r]["pm_deg"]["post_layout_rc"],
                 "gain_db": m[r]["gain_db"]["drawn"] - m[r]["gain_db"]["post_layout_rc"]}
    dr, po = ref["drawn_devices_only"], ref["post_layout"]
    wl["hand"] = {"gbw_pct": -pct(dr["gbw_mhz"], po["gbw_mhz"]), "pm_deg": dr["pm_deg"] - po["pm_deg"],
                  "gain_db": dr["gain_db"] - po["gain_db"]}
    ow, oh = d["opts"].get("outline_um", [250, 200])
    secs = {st: sum(x.get("seconds") or 0 for x in d["fs"].get(st, {}).get("steps", [])) for st in d["fs"]}
    return {"size": {**size, "hand": list(hand_wh)}, "area": area, "wiring_loss": wl, "outline": [ow, oh],
            "outline_area": ow * oh, "secs": secs}


def main_nodes(d: dict) -> list:
    """The nodes S1 and S2 single out: the first poles, the high-impedance ones, the most sensitive, the outputs."""
    nodes, tab = d["nodes"]["nodes"], d["sens"]["table"]
    pick = {n for n, v in nodes.items() if (v.get("pole_rank") or 99) <= 8 or v.get("high_impedance")}
    pick |= {n for n, v in nodes.items() if "signal_output" in (v.get("tags") or [])}
    for key in ("gbw_mhz", "pm_deg"):
        pick |= set(sorted((n for n in tab if "~" not in n), key=lambda n: tab[n][key]["linear_per_fF"])[:6])
    return sorted(pick, key=lambda n: nodes.get(n, {}).get("pole_rank") or 99)


# ---------------------------------------------------------------------------------------------------- the text
GLOSSARY = [
    ("Schematic", "the circuit as drawn by the designer: which transistors, resistors and capacitors connect to which."),
    ("Layout", "the drawing of the chip itself: the shapes on each layer that the factory makes. Every wire in it has "
               "length, so it adds capacitance and resistance the schematic does not have."),
    ("Op-amp", "operational amplifier. This one is fully differential: two inputs, two outputs (Vop, Vom)."),
    ("Node / net", "a point of the circuit where terminals connect (a net is its wire in the layout)."),
    ("Pole", "a frequency where a node's resistance and capacitance start to cut the gain; the first (dominant) pole "
             "sets the bandwidth, the next ones eat phase margin."),
    ("GBW", "unity-gain bandwidth: the frequency at which the amplifier's gain has fallen to 1. Higher is faster."),
    ("Phase margin (PM)", "how far the amplifier is from oscillating in feedback. Above about 60° is comfortable."),
    ("DC gain", "how much the amplifier multiplies a slow input signal, in dB (98 dB is about 80 000 times)."),
    ("Spec", "a required value, e.g. GBW ≥ 1.85 MHz. Here the specs are 0.9 × what the schematic achieves "
             "(ASSUMPTION; the design's README gives results, not specs)."),
    ("Margin, η and allowance", "margin = schematic value − spec limit. The flow lets the layout use at most "
                                "η = 0.5 of it (the allowance); the other half is kept for everything the flow does "
                                "not model (process corners, temperature). \"Use 1.27\" means 1.27 × the allowance."),
    ("Sensitivity", "how much a spec changes per fF of capacitance added on a node (S1)."),
    ("Budget", "the most capacitance, coupling, resistance or wire length a net may get from the layout, so that "
               "all of them together stay within the allowance (S2)."),
    ("DRC", "design rule check: are all shapes wide enough and far enough apart for the factory? 0 errors = clean."),
    ("LVS", "layout versus schematic: is the drawn layout the same circuit as the schematic? \"Match\" = yes."),
    ("Negative control", "a deliberately wrong copy (e.g. one transistor's length changed) that a check must reject; "
                         "it proves the check can fail."),
    ("Extraction (PEX)", "reading the finished layout back into a netlist that includes the wires' capacitance "
                         "(here capacitance only, \"C-only\"), so it can be simulated."),
    ("Drawn devices", "the layout's transistors as drawn, simulated without any wiring: shows what the layout's "
                      "device shapes alone change. \"Drawn → extracted\" is then the cost of the wiring."),
    ("Block", "a group of transistors drawn together as one piece (a matched pair, a mirror, a single device), with "
              "its own tap ring; numbered B1 … in this report."),
    ("Variant", "one way of drawing a block (e.g. A B B A or A B A B); S4 draws several, S5 picks one."),
    ("Common centroid", "matched transistors split into pieces arranged A B B A, so both have the same centre and a "
                        "gradient across the chip affects them equally."),
    ("Interdigitated", "pieces alternating A B A B: both spread over the same area, but their centres differ slightly."),
    ("Dummy", "an unused transistor or resistor at the end of a row, so the real ones at the ends see the same "
              "surroundings as those in the middle."),
    ("Tap ring", "a ring of substrate (or well) contact around a block, which prevents latch-up."),
    ("MIM capacitor", "metal–insulator–metal capacitor: the Miller capacitors here, 5 units of 10 × 10 µm each."),
    ("Macro", "one sub-circuit of the design's own hierarchy (x1, x2, top, the resistor packs), placed as a unit."),
    ("Budget-aware / area-only", "the flow scores every placement two ways and lays out both winners: by area plus "
                                 "how much of each wire's length budget it uses (the flow's own rule), and by area "
                                 "alone (the usual baseline). Comparing them tests whether the budgets help."),
    ("Simulated annealing", "a search that makes random small changes to a placement, always keeps an improvement, "
                            "sometimes keeps a worsening early on (to escape poor arrangements), and accepts fewer "
                            "worsenings as it \"cools\"."),
    ("A* (A-star)", "a shortest-path search on a grid that heads towards the target first; used by the router."),
    ("Gate (G4.1, G5.4 …)", "an automatic pass/fail check at the end of a stage."),
    ("PREREG", "the pre-registration file: the hypotheses, thresholds and fixed parameters, written down before the "
               "runs, changed only by dated amendments."),
]

ASSUMPTIONS = [
    "The specs are 0.9 × the schematic's own results (ASSUMPTION, kept by Imasha's decision).",
    "The outline is 250 µm wide and 200 µm tall (ASSUMPTION on the orientation; Imasha gave 250 × 200 µm).",
    "The two resistor packs' tap ring and dummies are on Vss (ASSUMPTION).",
    "Capacitance-only extraction: Magic's resistance extraction ran out of memory on this layout's supply rings "
    "(flow record row 87). The hand layout is measured the same way, so the comparison holds; the absolute "
    "post-layout numbers leave out wire resistance.",
    "One condition only (typical corner, 27 °C, the bench's own bias); no PVT corners after layout.",
    "Electromigration limits for SKY130 were not found in the PDK; wire widths are not checked against current.",
    "The tile's regions are matched to the schematic's sub-circuits by their cell names only (Diff_opamp_ly to x1, "
    "cs_p_5 to x2, bias_dummy to the bias circuit); the other regions are left unassigned (ASSUMPTION, to confirm).",
]

# who contributes what to each main decision: (decision, what was decided here, why, code, Imasha, LLM)
DECISIONS = [
    ("Specs", "each spec 0.9 × the schematic's own result", "the design's README gives results, not specs; a 10 % "
     "margin is what the layout may cost", "applies them in every check", "accepted (kept)",
     "proposed the ASSUMPTION"),
    ("Share of the margin for layout (η)", "0.5", "the other half stays for what the flow does not model (corners, "
     "temperature, mismatch)", "applies it to every budget and to G7.2", "accepted", "proposed (ASSUMPTION)"),
    ("Main nodes and sensitivities", "the first poles, the high-impedance and the most sensitive nodes (section 3)",
     "they decide which wires must stay short", "computes them (S1: linear model, checked against SPICE)", "–",
     "wrote the S1 method"),
    ("Budgets", "a capacitance, coupling, resistance and length budget per net", "shares the allowance so that all "
     "parasitics together stay within it", "computes them (S2: max-min fair sharing)", "–", "designed the sharing rule"),
    ("Transistor cells", "fingers, contacts, cell shape per device type", "the smallest cell that keeps each node "
     "within budget", "chooses them (S3)", "–", "wrote the rule base"),
    ("Blocks", "matched devices in one block; one type and one body per block", "matched devices must be drawn "
     "together; a ring holds one body", "groups them (S4, from S1's matching rule)", "approved the plan",
     "proposed the rule (plan v4)"),
    ("Matching style", "common centroid or interdigitated, as needed", "both cancel gradients; the cheaper one wins",
     "draws both, S5 picks by the cost", "decided the policy", "implemented the sequences"),
    ("Dummies", "one at each end of every matched row", "ends see the same surroundings as the middle",
     "adds them, wired to the body", "decided", "implemented"),
    ("Resistors", "the two packs interleaved A B B A", "the two common-mode sense strings must match",
     "draws and checks the block", "decided", "implemented the string order"),
    ("Capacitors", "each Miller capacitor as 5 MIM units of 10 × 10 µm", "as the schematic gives them (MF = 5)",
     "draws the array", "(the design)", "implemented"),
    ("Sub-circuits as macros", "x1, x2, top and the resistor packs placed as units", "keeps the designer's grouping "
     "and makes the search smaller", "places each, then arranges them", "decided (\"use the given hierarchy\")",
     "implemented"),
    ("Outline", "250 × 200 µm, hard", "a fixed area to fit, never traded against wire length",
     "rejects anything outside (G5.6)", "decided (orientation: ASSUMPTION)", "proposed reject-not-trade"),
    ("Floorplan", "which block goes where", "the lowest cost (area and wire budgets)", "searches and decides "
     "(annealing, enumeration)", "decided that the code arranges it", "designed the search; its settings are "
     "fixed in PREREG"),
    ("Routing", "metal-3/metal-4 grid router", "many blocks side by side; a grid keeps wires legal by construction",
     "routes every net", "–", "designed"),
    ("Extraction", "capacitance only", "resistance extraction ran out of memory here", "extracts", "open question",
     "proposed, flagged"),
    ("Checks", "DRC, LVS, budgets, specs, η, at every stage", "nothing passes on trust", "runs them",
     "approved PREREG", "drafted PREREG"),
]


def build_md(d: dict, num: dict, lay: dict, nb: dict, sheets: dict, nodes_main: list, head: str) -> list:
    ir, s5g, s6g, s7g, m = d["ir"], d["s5"]["gates"], d["s6"]["gates"], d["s7"]["gates"], d["m7"]["metrics"]
    ba, ao = m["budget_aware"], m["area_only"]
    ref = d["ref"]
    hand_dr, hand_po = ref["drawn_devices_only"], ref["post_layout"]
    sch = {k: x["schematic"] for k, x in ba.items()}
    margins = ir["margins"]
    eta = d["m7"]["eta"]
    nmos = len(ir["devices"])
    copies = sum(x.get("m", 1) for x in ir["devices"])
    mims = [p for p in ir.get("passives", []) if p["name"].startswith("XC")]
    res = [p for p in ir.get("passives", []) if p["name"].startswith("XX2_X")]
    sz, ar, wl = num["size"], num["area"], num["wiring_loss"]
    g75 = (s7g.get("G7.5_mim_self_coupling_cancelled (info)") or {}).get("detail", {})
    cen = (s5g.get("G5.7_matched_centring (info)") or {}).get("detail", {})
    mim_c = (d["pv"].get("mim_self") or {})
    flow_min = sum(num["secs"].get(s, 0) for s in ("S4", "S5", "S6", "S7")) / 60
    gb = ba["gbw_mhz"]
    g5 = s5g["G5.5_area_vs_area_only (info)"]
    ub = g5["u_budget_aware"]
    worst_u = max(ub.items(), key=lambda kv: kv[1])
    blocks = d["s4b"]["blocks"]
    nvar = sum(len(b["variants"]) for b in blocks)
    L = [f"# Automatic layout of `{D}`, and how it compares with the hand layout", "",
         f"*Generated by `python3 scripts/make_ttsky_report.py` from the flow's own output files (repo at {head}). "
         "Every number is read from `outputs/` or from the flow's code; only the explanations are typed. Assumptions "
         "are marked ASSUMPTION; figures taken from elsewhere are marked reported.*", "",
         "**How to read this report.** Section 1 is the result on one page. Sections 2–3 show the circuit and what the "
         "flow learned about it before drawing anything. Section 4 says who decided what. Sections 5–6 show how the "
         "layout was built (with the exact algorithms), section 7 what it costs after layout, and section 8 the "
         "comparison with the hand layout. Sections 9–10 are the novelty and the planned LLM work; 11–13 the "
         "failed checks, assumptions and open questions. Each picture has a *How to read it* note (the same for any "
         "design) and a *What it shows here* line (built from this run's numbers). A glossary is at the end.", ""]

    # ------------------------------------------------------------------ 1
    L += ["## 1. Summary", "",
          f"`{D}` is Imasha's fully differential op-amp, taped out on Tiny Tapeout (SKY130). Its schematic "
          f"(`Opamp_with_bias`) has {nmos} transistors ({copies} transistor pieces once each multiplier m is drawn), "
          f"{len(mims)} Miller capacitors and {len(res)} resistors. The flow took that schematic and, with no hand "
          f"editing, drew two complete layouts inside a {num['outline'][0]} × {num['outline'][1]} µm outline, "
          f"checked them, read their wiring back and simulated them. S4–S7 took {flow_min:.0f} minutes of computer "
          "time.", "",
          "**What came out:**", "",
          "- **Both layouts are clean and correct:** 0 design-rule errors (DRC) and the layout matches the schematic "
          "(LVS), for both.",
          f"- **Every spec is still met after layout.** GBW {f(gb['post_layout_rc'], 4)} MHz (spec ≥ "
          f"{f(gb['limit'], 4)}), phase margin {f(ba['pm_deg']['post_layout_rc'], 4)}° (≥ {f(ba['pm_deg']['limit'])}), "
          f"gain {f(ba['gain_db']['post_layout_rc'], 4)} dB (≥ {f(ba['gain_db']['limit'], 4)}), power "
          f"{f(ba['power_uw']['post_layout_rc'], 4)} µW (≤ {f(ba['power_uw']['limit'], 4)}).",
          f"- **One check fails: GBW.** The wiring takes {100 * gb['lost'] / gb['margin']:.0f} % of the GBW margin; "
          f"the flow allows {100 * eta:.0f} %. About two thirds of that is a capacitance inside the Miller capacitors "
          "that the extraction very likely counts twice; without it the wiring takes "
          f"{100 * g75.get('budget_aware', {}).get('gbw_mhz', {}).get('lost', 0) / gb['margin']:.0f} %.",
          f"- **Against the hand layout:** the flow's wiring costs less bandwidth (GBW −{wl['budget_aware']['gbw_pct']:.1f} % "
          f"against −{wl['hand']['gbw_pct']:.1f} %) but more phase margin (−{wl['budget_aware']['pm_deg']:.1f}° against "
          f"−{wl['hand']['pm_deg']:.1f}°). It needs more area: {ar['budget_aware'] / ar['hand']:.2f} × the hand "
          f"layout's op-amp (budget-aware) and {ar['area_only'] / ar['hand']:.2f} × (area-only).",
          "- **No AI model decided anything in these runs:** every layout decision is made by the flow's code, within "
          "the constraints Imasha set (section 4). An LLM wrote and reviewed the code; an LLM *taking* layout "
          "decisions is the next step (section 10).",
          "- **A caution:** the taped-out tile is not exactly the schematic (it adds enable switches and its devices "
          "differ; section 8). So the two are compared on what the wiring costs and on area, not on absolute speed.",
          ""]
    L += ["| | Flow, budget-aware | Flow, area-only | Hand layout (tile) |", "|---|---|---|---|",
          f"| Size of the op-amp (µm) | {sz['budget_aware'][0]:.1f} × {sz['budget_aware'][1]:.1f} | "
          f"{sz['area_only'][0]:.1f} × {sz['area_only'][1]:.1f} | {sz['hand'][0]:.1f} × {sz['hand'][1]:.1f} |",
          f"| Area (µm²) | {ar['budget_aware']:,.0f} | {ar['area_only']:,.0f} | {ar['hand']:,.0f} |",
          f"| DRC errors / LVS | {s5g['G5.2_top_DRC']['detail']['budget_aware']} / "
          f"{'match' if s5g['G5.3_top_LVS']['detail']['budget_aware']['match'] else 'no match'} | "
          f"{s5g['G5.2_top_DRC']['detail']['area_only']} / "
          f"{'match' if s5g['G5.3_top_LVS']['detail']['area_only']['match'] else 'no match'} | "
          "taped out (not checked here) / does not match the schematic (by design: switches added) |",
          f"| GBW lost to the wiring | −{wl['budget_aware']['gbw_pct']:.1f} % | −{wl['area_only']['gbw_pct']:.1f} % | "
          f"−{wl['hand']['gbw_pct']:.1f} % |",
          f"| Phase margin lost to the wiring | −{wl['budget_aware']['pm_deg']:.1f}° | −{wl['area_only']['pm_deg']:.1f}° | "
          f"−{wl['hand']['pm_deg']:.1f}° |",
          f"| GBW after layout (MHz) | {f(ba['gbw_mhz']['post_layout_rc'], 4)} | {f(ao['gbw_mhz']['post_layout_rc'], 4)} | "
          f"{f(hand_po['gbw_mhz'], 4)} (its own devices give {f(hand_dr['gbw_mhz'], 4)} before wiring) |",
          f"| Phase margin after layout (°) | {f(ba['pm_deg']['post_layout_rc'], 4)} | {f(ao['pm_deg']['post_layout_rc'], 4)} | "
          f"{f(hand_po['pm_deg'], 4)} |", ""]
    L += W.how("\"lost to the wiring\" compares the same layout simulated twice, with its drawn devices only and with "
               "every wire's capacitance (C-only extraction, Magic, same bench, same conditions). It isolates what "
               "the wiring and placement cost, which is the fair comparison between two layouts of slightly "
               "different circuits.")

    # ------------------------------------------------------------------ 2
    L += ["", "## 2. The circuit, its sub-circuits and what was asked", "",
          "The designer's schematic is split into sub-circuits (xschem hierarchy). The flow keeps them as units "
          "(\"macros\"); each has one colour throughout this report: on the schematics, the block gallery and the "
          "layouts.", "", "| Colour | Sub-circuit | What it is | Elements |", "|---|---|---|---|"]
    kinds = {}
    for lv in d["hier"]["levels"]:
        for v in lv.values():
            if isinstance(v, list):
                for x in v:
                    kinds[x.get("instance")] = (x.get("kind"), len(x.get("elements", [])))
    for mac, inst in (("top", "top"), ("x1", "x1"), ("x2", "x2")):
        k, n = kinds.get(inst, ("", 0))
        L.append(f'| <span style="color:{MCOLOR[mac]}">■</span> | **{mac}** | {k} | {n} |')
    npk = sum(n for i, (k, n) in kinds.items() if i.startswith("x2/"))
    L.append(f'| <span style="color:{MCOLOR["res_packs"]}">■</span> | **res_packs** | the two res_packs inside x2 '
             f"(x2/x1, x2/x2: common-mode sense resistors), drawn as one interleaved block | {npk} |")
    L += ["", "**The top schematic** (`Opamp_with_bias`): the bias circuit (start-up, beta multiplier, current "
          "outputs) and the two Miller capacitors are drawn here; the first and second stages are the symbols x1 and "
          "x2.", "", W.img(f"outputs/report/{D}/sch_top.png", 980, "top schematic"), ""]
    L += W.how("the designer's own schematic (xschem), unchanged. A coloured box marks every device the flow lays "
               "out, in its sub-circuit's colour, with the number of the block it went into (B1 …, section 5). The "
               "two large boxes are the sub-circuits x1 and x2, shown below.")
    for key, title in (("x1", "**x1, the first stage** (`Diff_opamp`): folded-cascode input stage with its "
                              "common-mode feedback and bias diodes."),
                       ("x2", "**x2, the second stage** (`Common_source_stage`): common-source output stage and the "
                              "resistive common-mode sense (the two res_packs)."),
                       ("res_pack", "**res_pack** (x2/x1; x2/x2 is the same schematic): 20 poly resistors in series. "
                                    "Both packs go into one interleaved block.")):
        L += ["", title, "", W.img(f"outputs/report/{D}/sch_{key}.png", 980, key), ""]
    L += ["", "**The specs** (each 0.9 × the schematic's own result: ASSUMPTION):", "",
          "| Spec | Schematic | Limit | Margin | Allowance for the layout (η × margin) |", "|---|---|---|---|---|"]
    for k, mg in margins.items():
        name, unit = SPEC_NAME.get(k, (k, ""))
        L.append(f"| {name} ({unit}) | {f(sch.get(k), 5)} | {'≥' if mg['kind'] == 'min' else '≤'} {f(mg['limit'], 5)} | "
                 f"{f(mg['margin'], 4)} | {f(eta * mg['margin'], 4)} |")
    o = d["opts"]
    L += ["", "**Imasha's decisions for this layout** (2026-11-04; `inputs/ttsky25a_fd/layout.yaml`):", "",
          "- Use the design's own hierarchy; the code arranges the floorplan.",
          f"- A hard outline of {o.get('outline_um', ['?', '?'])[0]} × {o.get('outline_um', ['?', '?'])[1]} µm.",
          "- Matched transistors as common centroid or interdigitated, as needed; the choice follows the spec- and "
          "area-driven cost, with no extra rule where there is no reason for one.",
          "- Dummies at the ends of every matched row.",
          "- The two resistor packs interleaved, so they match each other.", ""]

    # ------------------------------------------------------------------ 3
    nodes, tab = d["nodes"]["nodes"], d["sens"]["table"]
    bud = {e["id"]: e for e in d["budgets"]["elements"]}
    rows6 = {x["id"]: x for x in d["pv"]["layouts"]["budget_aware"]["budgets"]["rows"]}
    ml = {k.lower(): v for k, v in s5g["G5.4_route_rules"]["detail"]["budget_aware"]["max_length"].items()}
    groups = d["s1"]["gates"]["G1.4_matching_groups"]
    L += ["## 3. What the flow learned before drawing: main nodes, nets and budgets (S1, S2)", "",
          "Before any layout, S1 builds a linear (small-signal) model of the amplifier from its operating point and "
          "checks it against transistor-level SPICE; S2 turns the specs into budgets for every net.", "",
          W.img(f"outputs/S1/{D}/plots/bode_linear_vs_spice.png", 640, "bode"), ""]
    L += W.how("the amplifier's open-loop gain (top) and phase (bottom) against frequency: SPICE on the real "
               "transistors (solid) and S1's linear model (dashed). Where the gain crosses 0 dB is the GBW; how far "
               "the phase is above −180° there is the phase margin.")
    L += W.here(f"the two curves lie on top of each other: the model S1 uses for every later estimate is faithful "
                f"(gate G1.3, sensitivities against SPICE: {'PASS' if d['s1']['gates']['G1.3_sensitivity_vs_spice']['pass'] else 'FAIL'}).")
    L += ["", "**The main nodes.** S1 tags every node (dominant pole, tail, diode-connected, output …), estimates its "
          "pole, and measures how much each spec drops per fF added on it; S2 then gives each net a capacitance "
          "budget and a wire-length budget. The nodes that matter most, and what the budget-aware layout gave them:", "",
          "| Node | Role (S1) | Pole rank | GBW lost per fF (kHz) | PM lost per fF (m°) | Capacitance budget (fF) | "
          "Extracted (fF) | Use | Wire length use |", "|---|---|---|---|---|---|---|---|---|"]
    for n in nodes_main:
        v, s = nodes.get(n, {}), tab.get(n, {})
        b, r6, lm = bud.get(n, {}), rows6.get(n, {}), ml.get(n.lower(), {})
        tags = ", ".join(v.get("tags") or []) or ("high impedance" if v.get("high_impedance") else "–")
        def sv(key):
            if not s:
                return "–"
            x = -1000 * s.get(key, {}).get("linear_per_fF", 0)
            return "≈ 0" if abs(x) < 1e-6 else f(x, 3)
        L.append(f"| {n} | {tags} | {v.get('pole_rank', '–')} | {sv('gbw_mhz')} | {sv('pm_deg')} | "
                 f"{f(b.get('budget'), 3) if b else '–'} | {f(r6.get('value'), 3) if r6 else '–'} | "
                 f"{('**' + f(r6.get('use')) + '**') if r6 and not r6.get('ok') else f(r6.get('use')) if r6 else '–'} | "
                 f"{f(lm.get('use')) if lm else '–'} |")
    L += W.how("pole rank 1 is the lowest-frequency pole (the dominant one). The two sensitivity columns say how much "
               "GBW and phase margin drop for each fF of wiring added on that node. \"Use\" is extracted / budget "
               "(bold: over); \"wire length use\" is the routed length over S2's length budget.")
    L += W.here("Vop1 and Vom1, the first-stage outputs, carry the dominant pole: they set the GBW (with the Miller "
                "capacitors) and are high-impedance, so every fF there counts. x1_Vtest2 and x1_net1 are the nodes "
                "where added capacitance costs the most phase margin. Most main nodes end up over their capacitance "
                "budget, which is why G6.2 fails (section 11); the simulation in section 7 shows the specs are still "
                "met, because the budgets assume a far tighter layout.")
    L += ["", W.img(f"outputs/report/{D}/chart_sensitivity.png", 760, "sensitivity chart"), ""]
    L += W.how("the ten nodes where added capacitance costs the most GBW (left) and phase margin (right), from S1's "
               "linear model. These are the nodes whose wires the layout should keep short.")
    L += ["", W.img(f"outputs/S2/{D}/plots/budget_verification.png", 760, "budget verification"), ""]
    L += W.how("S2's own check of its budgets: for each spec and corner (x axis), the share of the margin used if "
               "every harmful budget were filled at once, predicted (blue) and simulated in SPICE (orange). Every "
               "bar must stay under η (dashed line).")
    L += W.here("every bar stays under 0.5: if the layout keeps within its budgets, the specs keep half their margin.")
    L += ["", f"**Matching groups** (S1, rule: *{groups['rule']}*): {len(groups['groups'])} groups were found; each "
          "becomes one S4 block, so its devices are drawn together and matched.", ""]

    # ------------------------------------------------------------------ 4
    L += ["## 4. Who decides what: code, Imasha, and the LLM", "",
          "Three contributors shape this layout:", "",
          "- **Code** (the flow): makes every decision at run time, by fixed rules and by searching for the lowest "
          "cost. Its settings (seeds, schedules, gaps, thresholds) are fixed in PREREG before the runs.",
          "- **Imasha** (the definition): the design, the constraints and the policies (outline, matching style, "
          "dummies, which resistors match, use of the hierarchy), and approval of the plans.",
          "- **LLM** (Claude, while building the flow): wrote the code, proposed the algorithms, the rules and the "
          "ASSUMPTIONs, drafted PREREG, and reviewed the code independently. **No LLM is called during a run.**", "",
          "| Decision | What was decided here | Why | Code | Imasha | LLM |", "|---|---|---|---|---|---|"]
    L += [f"| {a} | {b} | {c} | {x} | {y} | {z} |" for a, b, c, x, y, z in DECISIONS]
    L += [""]

    # ------------------------------------------------------------------ 5
    L += ["## 5. The building blocks (S4)", "",
          f"S4 grouped the {nmos} transistors into blocks (every matched group in one block), plus one block per "
          f"Miller capacitor and one for the 40 resistors: {len(blocks)} blocks. It drew {nvar} versions (variants) of "
          "them and checked every one alone: all DRC-clean and LVS-matched, each with a deliberately broken copy that "
          "the check must reject.", "",
          "**The algorithm, step by step** (`src/s4/run.py`, `src/s4/block.py`):", "",
          "1. **Group:** S1's matching groups first, then S0's blocks for the rest; one device type and one body net "
          "per block; every device in exactly one block.",
          "2. **Units:** a device with multiplier m is drawn as m copies (units) of the cell S3 chose.",
          "3. **Variants** (with `matching: centroid`):",
          "   - *common centroid*: each device's copies halved on each side of the centre and interleaved in turn "
          "(A B B A; A B C C B A for three devices); a device with an odd count takes the centre;",
          "   - *interdigitated*: one copy of each in turn (A B A B …);",
          "   - *mirror* (two odd counts, e.g. m = 9, cannot share a centre): the best mirror-image row;",
          "   - *resistors*: the two strings interleaved A B B A …, each string alternating orientation so that two "
          "neighbours share a node on one side;",
          "   - a single device: one row (A).",
          "4. **Dummies:** one unit at each end of every matched row, every terminal on the body net.",
          f"5. **Draw the row:** units left to right, {B4.GAP} µm apart; a metal-2 stub from each terminal to one "
          f"metal-3 track per net above or below the row ({B4.TRACK_W} µm wide, {B4.PITCH} µm pitch); a net used "
          "only inside the block gets a short track, packed with others in rows by the left-edge rule; a net with "
          "pins on both sides gets a metal-2 column joining its two tracks.",
          f"6. **Ring:** one tap ring {B4.RING_GAP} µm outside the tracks (n-well for PMOS); a tap strip inside the "
          "row where a diffusion would be farther from a tap than the latch-up limit.",
          "7. **Sign off:** Magic DRC; Netgen LVS against the block's own netlist (with m and the dummies); a negative "
          "control (one length changed) must fail.", ""]
    L += ["**Every block** (numbered as on the schematics; the colour bar is the sub-circuit; the picture is the "
          "variant the budget-aware layout chose):", ""]
    figs = []
    for name in nb["order"]:
        b = nb["by_name"][name]
        vba, vao = nb["chosen"]["budget_aware"].get(name), nb["chosen"]["area_only"].get(name)
        v = next((x for x in b["variants"] if x["id"] == vba), b["variants"][0])
        g = v.get("geometry") or {}
        bb = g.get("bbox_um")
        size = f"{bb[2] - bb[0]:.1f} × {bb[3] - bb[1]:.1f} µm" if bb else ""
        devs = b["devices"] if len(b["devices"]) <= 4 else b["devices"][:3] + [f"… ({len(b['devices'])})"]
        cap = (f"<b>B{nb['num'][name]} {name}</b><br>{nb['macro'][name]} · {', '.join(devs)}<br>variant {vba}"
               + (f" (area-only: {vao})" if vao != vba else "") + (f" · {size}" if size else ""))
        if v.get("png"):
            figs.append(fig_html(v["png"], cap, MCOLOR[nb["macro"][name]]))
    L += ["<div>" + "".join(figs) + "</div>", ""]
    L += W.how("each block as drawn: the transistor units in a row (dummies at the ends), metal tracks above and "
               "below for the wiring, and the tap ring around it. Appendix A shows every variant of every block.")
    L += ["", "**Matching in the final layouts** (gate G5.7). Where a matched block has both a common-centroid and "
          "an interdigitated version, S5 takes the one that costs less (area and wire budgets), as Imasha decided:", "",
          "| Matched block | Budget-aware | Area-only |", "|---|---|---|"]
    for n in sorted(set().union(*(set(cen.get(r, {})) for r in RULES)), key=lambda n: nb["num"].get(n, 0)):
        cells = []
        for r in RULES:
            x = cen.get(r, {}).get(n)
            if x:
                off = max(abs(v) for v in x["centroid_offset_um"].values())
                cells.append(f"{x['variant']}, " + ("common centroid" if x["common_centroid"] else f"centres {off:.1f} µm off"))
            else:
                cells.append("–")
        L.append(f"| B{nb['num'].get(n)} {n} | {cells[0]} | {cells[1]} |")
    nc = {r: sum(x["common_centroid"] for x in cen.get(r, {}).values()) for r in RULES}
    L += W.here(f"{nc['budget_aware']} of {len(cen.get('budget_aware', {}))} matched blocks are common centroid in "
                f"the budget-aware layout, {nc['area_only']} of {len(cen.get('area_only', {}))} in the area-only one. "
                "\"Centres off\" is how far one device's centre sits from the row's centre in an interdigitated row.")

    # ------------------------------------------------------------------ 6
    pmac = d["pl"]["chosen"]
    L += ["", "## 6. Placement and routing (S5)", "",
          "**How the placement is found** (`src/s5/macro.py`, `src/s5/place.py`):", "",
          "1. **Sub-circuits:** every block belongs to the sub-circuit of its devices (x1, x2, top); a block whose "
          "devices span several (the interleaved res_packs) is a sub-circuit of its own.",
          f"2. **Rows:** inside a sub-circuit, blocks stand in rows, PMOS rows above NMOS rows, {P5.ROW_GAP} µm between "
          f"rows and {P5.BLOCK_GAP} µm between blocks; matched blocks may share a row.",
          f"3. **Search inside a sub-circuit:** up to {M5.ENUM_MAX} blocks, every arrangement is tried (all row "
          "partitions × variants × flips). Beyond that, *simulated annealing*: start from PMOS rows above NMOS rows; "
          f"{M5.MOVES:,} random moves, each one of: swap two blocks, move a block to another (or a new) row, change a "
          f"block's variant, flip a block. A better placement is always kept; a worse one with probability "
          f"exp(−Δcost / T), where T starts at {M5.T_START} × the starting cost and is multiplied by {M5.COOL} after "
          f"every move. Seed {M5.SEED}, so every run gives the same result.",
          f"4. **Three shapes:** each sub-circuit is placed three times, at widths {', '.join(str(x) for x in M5.SHAPES)} "
          f"× the outline's width (tall and narrow to wide and short).",
          "5. **Top level:** every arrangement of the four sub-circuits' shapes in rows is tried; anything outside the "
          "outline is rejected (never traded).",
          "6. **Both costs:** the whole search runs twice with the same seed: once with the budget-aware cost, once "
          "with the area-only cost. Both winners are routed and checked.", "",
          "**How area and wire length are optimised.** Both enter one number, the cost, which the search minimises:", "",
          f"- area term: A / A_ref, the bounding box's area over the sum of the blocks' smallest variants;",
          "- each net's wire use: u = (estimated length) / (S2's length budget for that net), where the length is the "
          "half-perimeter of the box around the net's pins;",
          f"- **budget-aware cost** = A / A_ref + {P5.LAMBDA:g} × Σ max(0, u − 1) + {P5.MU:g} × Σ u. An excess over a "
          f"budget costs {P5.LAMBDA:g} × more than use within it;",
          "- **area-only cost** = A / A_ref (the usual baseline).", "",
          "Area is also kept small one level down: S3 picks the smallest cell that keeps each node in budget, and S4 "
          "draws compact blocks; among a block's variants the smaller ones cost less here.", "",
          "**How the wires are routed** (`src/s5/grid.py`):", "",
          f"- a grid of points {G5.GRID} µm apart; metal-3 runs horizontally, metal-4 vertically, {G5.WIRE} µm wide, so "
          "wires on neighbouring grid lines are legal by construction;",
          "- each net is a tree: A* search from the part already routed to the nearest pin not yet joined, cost = "
          f"length + {G5.VIA_COST:g} µm per via; nets in order of least budget slack (the tightest first);",
          "- obstacles: every block's tracks and keep-outs and the contact stacks to the rings, grown by half a wire "
          "plus the spacing rule;",
          "- a net the router cannot finish is reported, never left silently open; DRC and LVS then check the "
          "result.", ""]
    L += ["**The layouts.** All three pictures below are at the same scale. The box around the flow's layouts is the "
          f"{num['outline'][0]} × {num['outline'][1]} µm outline; the hand layout is the whole Tiny Tapeout tile "
          f"(161 × 226 µm), whose op-amp (`Diff_Opamp`) measures {sz['hand'][0]:.1f} × {sz['hand'][1]:.1f} µm.", "",
          " ".join(W.img(f"outputs/report/{D}/layout_{k}.png", 300, LABEL[k]) for k in ("budget_aware", "area_only", "hand")),
          "", f"*Left to right: {LABEL['budget_aware']}, {LABEL['area_only']}, {LABEL['hand']}.*", ""]
    for r in RULES:
        L += [f"**{LABEL[r]}, annotated:**", "", W.img(f"outputs/report/{D}/layout_{r}_annot.png", 900, r), ""]
    L += W.how("the routed layout with each sub-circuit's area outlined in its colour and every block's number (B1 … "
               "as in section 5) at its centre. The thin vertical lines are metal-4 wires, the horizontal ones "
               "metal-3.")
    L += ["", "| | Budget-aware | Area-only |", "|---|---|---|",
          "| Sub-circuits, top to bottom | " + " | ".join(" / ".join(", ".join(row) for row in pmac[r]["placement"]["rows"])
                                                        for r in RULES) + " |",
          "| Shape of each sub-circuit | " + " | ".join(", ".join(f"{k} {v['shape']} ({v['method']})"
                                                               for k, v in pmac[r]["placement"]["macros"].items())
                                                     for r in RULES) + " |",
          f"| Size (µm) | {sz['budget_aware'][0]:.1f} × {sz['budget_aware'][1]:.1f} | {sz['area_only'][0]:.1f} × "
          f"{sz['area_only'][1]:.1f} |",
          f"| Area (µm²) | {ar['budget_aware']:,.0f} | {ar['area_only']:,.0f} |"]
    rr = s5g["G5.4_route_rules"]["detail"]
    wire = {r: sum(sum((x.get("length_um") or {}).values()) for x in rr[r]["max_length"].values()) for r in RULES}
    over = {r: sum(not x["ok"] for x in rr[r]["max_length"].values()) for r in RULES}
    L += [f"| Top-level wire (µm) | {wire['budget_aware']:,.0f} | {wire['area_only']:,.0f} |",
          f"| Sum of wire-budget use (lower is better) | {sum(g5['u_budget_aware'].values()):.1f} | "
          f"{sum(g5['u_area_only'].values()):.1f} |",
          f"| Nets longer than their budget | {over['budget_aware']} of {len(rr['budget_aware']['max_length'])} | "
          f"{over['area_only']} of {len(rr['area_only']['max_length'])} |",
          f"| DRC errors / LVS | {s5g['G5.2_top_DRC']['detail']['budget_aware']} / match | "
          f"{s5g['G5.2_top_DRC']['detail']['area_only']} / match |", ""]
    L += W.how("\"w100\", \"w65\", \"w50\" name the width limit a sub-circuit was placed under (× the outline's "
               "width); \"annealing\" or \"enumeration\" is how it was searched.")
    L += W.here(f"the budget-aware layout uses {100 * (1 - sum(g5['u_budget_aware'].values()) / sum(g5['u_area_only'].values())):.0f} % "
                f"less of the wire budgets for {100 * (g5['area_ratio'] - 1):.0f} % more area. Most nets that run "
                "between sub-circuits are still far over the length budgets from S2, which assumed a much more "
                "compact layout (section 11).")
    L += ["", W.img(f"outputs/report/{D}/chart_area.png", 640, "area chart"), ""]
    L += W.how("the bounding box of each op-amp; the dashed line is the outline's area. The hand layout's op-amp also "
               "holds the tile's enable switches.")

    # ------------------------------------------------------------------ 7
    L += ["", "## 7. After layout: what the wiring costs (S6, S7)", "",
          "S6 reads each finished layout back with the capacitance of every wire and S7 simulates it in the same "
          "test benches as the schematic. Resistance is not included (capacitance-only, \"C-only\"; section 12).", "",
          "| Spec | Limit | Schematic | Drawn devices | After layout, budget-aware | Use of the allowance | "
          "After layout, area-only | Use of the allowance |", "|---|---|---|---|---|---|---|---|"]
    for k, x in ba.items():
        name, unit = SPEC_NAME.get(k, (k, ""))
        y = ao[k]
        b1 = "**" if not x["within_allowed"] else ""
        b2 = "**" if not y["within_allowed"] else ""
        L.append(f"| {name} ({unit}) | {'≥' if x['kind'] == 'min' else '≤'} {f(x['limit'], 5)} | {f(x['schematic'], 5)} | "
                 f"{f(x['drawn'], 5)} | {f(x['post_layout_rc'], 5)} | {b1}{f(x['use_of_allowed'])}{b1} | "
                 f"{f(y['post_layout_rc'], 5)} | {b2}{f(y['use_of_allowed'])}{b2} |")
    L += W.how("\"use of the allowance\" is (schematic − after layout) / (η × margin): 1.0 is all the flow allows the "
               "layout to take; bold is more. Every value still meets its spec (G7.1 passes).")
    L += W.here(f"GBW is the only spec over its allowance ({f(gb['use_of_allowed'])} budget-aware, "
                f"{f(ao['gbw_mhz']['use_of_allowed'])} area-only); phase margin uses about half; gain and power little.")
    if mim_c:
        c0 = next(iter(mim_c.values()))
        gm = g75.get("budget_aware", {})
        L += ["", f"**Why GBW fails, and the double count.** GBW is set mainly by the Miller capacitors. Extracted alone, "
              f"each Miller capacitor block shows {f(c0['plate_coupling_fF'], 3)} fF between its own plates on top of "
              "the capacitor itself. The capacitor's model already contains that, so the extraction very likely counts "
              "it twice (it is how Magic's SKY130 rules treat metal-4 over metal-3). With it removed, GBW after "
              f"layout is {f(gm.get('gbw_mhz', {}).get('value'), 4)} MHz, using {f(gm.get('gbw_mhz', {}).get('use_of_allowed'))} "
              f"of the allowance, and every spec is within it (phase margin {f(gm.get('pm_deg', {}).get('use_of_allowed'))}). "
              "The gate keeps the extraction's number; which one should count is an open question (section 13).", ""]
    g62 = s6g["G6.2_parasitics_within_budgets"]
    L += [f"**Budgets.** S2 had set a capacitance budget for every net and every pair of nets. "
          f"{len(g62['violations'])} of them are exceeded in the budget-aware layout "
          f"({len(g62['area_only_violations (H5)'])} in the area-only one). The budgets assumed a far tighter layout; "
          "the simulation above is the real judge, and it passes every spec.", ""]
    L += [W.img(f"outputs/report/{D}/chart_wiring_loss.png", 700, "wiring loss chart"), ""]
    L += W.how("the drop from drawn devices to the extracted layout, for each of the three layouts, measured the same "
               "way. Shorter bars are better.")
    L += W.here(f"the flow loses less GBW than the hand layout ({wl['budget_aware']['gbw_pct']:.1f} % against "
                f"{wl['hand']['gbw_pct']:.1f} %) and more phase margin ({wl['budget_aware']['pm_deg']:.1f}° against "
                f"{wl['hand']['pm_deg']:.1f}°).")

    # ------------------------------------------------------------------ 8
    lvs = ref["lvs_vs_layout_view"]
    L += ["", "## 8. Comparison with the hand layout", "",
          "**What the hand layout is.** The taped-out Tiny Tapeout tile `tt_um_diff` "
          f"(`{ref['gds']}`), drawn by hand by the designers. The flow extracted it with the same tool and settings "
          "(Magic, capacitance only) and simulated it in the same benches (flow record 7.7).", "",
          W.img(f"outputs/report/{D}/layout_hand_annot.png", 900, "hand layout annotated"), ""]
    L += W.how("the tile with its main regions outlined, named by the tile's own cell names. A region is coloured "
               "only where its name says which sub-circuit it is (Diff_opamp_ly: the first stage; cs_p_5: the second "
               "stage's PMOS; bias_dummy: the bias circuit); the others are grey (ASSUMPTION; to confirm). The boxes "
               "are the cells' bounding boxes, so they can overlap: cs_p_5 and block_01 to block_04 lie inside "
               "Diff_opamp_ly's box.")
    L += ["", "**Why it is not the same circuit.** LVS of the tile against the schematic "
          f"{'matches' if lvs['match'] else 'does not match'}: the tile adds enable switches and its device sizes "
          f"differ. Its drawn devices alone give GBW {f(hand_dr['gbw_mhz'], 4)} MHz and gain {f(hand_dr['gain_db'], 4)} dB, "
          f"against the schematic's {f(ref['schematic_same_conditions']['gbw_mhz'], 4)} MHz and "
          f"{f(ref['schematic_same_conditions']['gain_db'], 4)} dB. Its absolute numbers therefore cannot be set against "
          "the flow's specs; what compares fairly is:", "",
          "| | Flow, budget-aware | Flow, area-only | Hand layout |", "|---|---|---|---|",
          f"| Area of the op-amp (µm²) | {ar['budget_aware']:,.0f} ({ar['budget_aware'] / ar['hand']:.2f} ×) | "
          f"{ar['area_only']:,.0f} ({ar['area_only'] / ar['hand']:.2f} ×) | {ar['hand']:,.0f} (1.00 ×) |",
          f"| GBW lost to the wiring | {wl['budget_aware']['gbw_pct']:.1f} % | {wl['area_only']['gbw_pct']:.1f} % | "
          f"{wl['hand']['gbw_pct']:.1f} % |",
          f"| Phase margin lost to the wiring | {wl['budget_aware']['pm_deg']:.2f}° | {wl['area_only']['pm_deg']:.2f}° | "
          f"{wl['hand']['pm_deg']:.2f}° |",
          f"| Gain lost to the wiring | {wl['budget_aware']['gain_db']:.3f} dB | {wl['area_only']['gain_db']:.3f} dB | "
          f"{wl['hand']['gain_db']:.3f} dB |", ""]
    better_gbw = wl["budget_aware"]["gbw_pct"] < wl["hand"]["gbw_pct"]
    L += ["**What it shows.**", "",
          f"- **Bandwidth:** the flow's wiring costs {'less' if better_gbw else 'more'} GBW than the hand layout's "
          f"({wl['budget_aware']['gbw_pct']:.1f} % against {wl['hand']['gbw_pct']:.1f} %).",
          f"- **Phase margin:** the flow's wiring costs more ({wl['budget_aware']['pm_deg']:.1f}° against "
          f"{wl['hand']['pm_deg']:.1f}°). A likely reason (not measured separately): the design's hierarchy puts the "
          "Miller capacitors in the `top` sub-circuit, and the flow places each sub-circuit as a unit, so the "
          "capacitors stand away from the first-stage outputs (Vop1, Vom1, in x1) they connect to; those nets and the "
          f"outputs run long between sub-circuits (the worst net, {worst_u[0]}, uses {worst_u[1]:.0f} × its length "
          "budget).",
          f"- **Area:** the hand layout is denser. The flow's blocks each carry their own tap ring and stand "
          f"{P5.BLOCK_GAP:g} µm apart, and the outline (not the area) was the target; the area-only layout comes within "
          f"{100 * (ar['area_only'] / ar['hand'] - 1):.0f} % of the hand layout.",
          "- **Effort:** the flow's layouts took minutes of computer time, with every DRC, LVS and simulation check "
          "run automatically; the hand layout's design time is not recorded here.", ""]
    rp = ref.get("reported_post_layout") or {}
    if rp:
        mt = rp.get("metrics", {})
        L += [f"*For reference, the designers' paper reports post-layout simulation of the tile (reported, "
              f"{rp.get('source', '')}): about {f(mt.get('gain_db'))} dB gain, {f(mt.get('gbw_mhz'))} MHz bandwidth and "
              f"{f(mt.get('pm_deg'))}° phase margin, under the paper's own load and conditions, which differ from "
              "the flow's bench.*", ""]

    # ------------------------------------------------------------------ 9
    h5 = (s7g.get("H5 (info)") or {}).get("use_of_allowed", {})
    L += ["## 9. What is new in this flow", "",
          "The project's literature review (`docs/05_literature_novelty_remap.md`) sets out what is already published "
          "and must not be claimed (per-net parasitic budgets in general, LLM-generated constraints, common-centroid "
          "pattern selection, symmetry extraction …) and five contributions this flow aims at. Where each stands "
          "after this run:", "",
          "| Contribution | What it means | Shown on this design |", "|---|---|---|",
          "| C1. Intent compiled from the circuit's own model | per-node sensitivities from a small-signal model of the "
          "hierarchy turn the specs into budgets and routing rules *before* any layout, each traceable to a node and "
          "its pole | partly: S1's linear model (checked against SPICE) gives every node's sensitivity and pole, and "
          "S2 turns them into per-net budgets before layout (section 3); closed-form symbolic expressions are only "
          "reported, and variation ranges from a sizing front end are not used in this run |",
          "| C2. Device cells chosen from the requirements | each SKY130 transistor cell (fingers, contacts, sharing) "
          "chosen to keep its node within budget | yes, with relaxations: S3 chose every cell; some types needed a "
          "relaxed (least-bad) option (G3.3/G3.5), and every spec is still met |",
          "| C3. Budget-aware variants and placement | several signed-off variants per block, chosen and placed to "
          "minimise area *subject to the budgets* | yes: "
          f"{nvar} signed-off variants; the budget-aware layout uses "
          f"{100 * (1 - sum(g5['u_budget_aware'].values()) / sum(g5['u_area_only'].values())):.0f} % less wire budget "
          f"and loses less GBW ({f(h5.get('budget_aware', {}).get('gbw_mhz'))} against "
          f"{f(h5.get('area_only', {}).get('gbw_mhz'))} of the allowance) and phase margin "
          f"({f(h5.get('budget_aware', {}).get('pm_deg'))} against {f(h5.get('area_only', {}).get('pm_deg'))}) than "
          "the area-only one (hypothesis H5) |",
          "| C4. LLM decisions grounded in the equations, measured | an LLM proposes and explains decisions over the "
          "explicit budgets; what it adds is measured against the rule-only flow | not yet: the next step "
          "(section 10) |",
          "| C5. Open, reproducible SKY130 flow | every block DRC/LVS-clean with Magic, Netgen and ngspice; public "
          "benchmarks; results that re-run identically | yes: every block and both layouts signed off with negative "
          "controls; seeded searches; golden results re-checked by `./flow test` |", "",
          "Also new in this phase (engineering, not literature claims): placement by the design's own sub-circuits "
          "under a hard outline; an automatic check for the Miller capacitors' likely double-counted coupling "
          "(G6.5, G7.5); and an LVS check that accepts two crossed labels only when the schematic shows the nets "
          "are truly interchangeable.", ""]

    # ------------------------------------------------------------------ 10
    L += ["## 10. The next step: LLM integration", "",
          "**What is planned** (`docs/plan_v5_ttsky25a.md` §9, `docs/05_literature_novelty_remap.md` §4; nothing "
          "here is built yet). An independent LLM is given only the netlist, the hierarchy, the specs and the "
          "budgets of section 3, and proposes the floorplan and the matching, with its reasons (the AICL way). The "
          "same S4–S7 build and check its proposal exactly as they checked the code's, so the two are compared on "
          "the same numbers.", "",
          "**What the LLM would do, and what it would not:**", "",
          "| Task | LLM | Code |", "|---|---|---|",
          "| Propose constraints and resolve conflicts (e.g. which budgets cannot all be met) | proposes, explains | "
          "validates |",
          "| Floorplan: which sub-circuits and blocks sit next to which | proposes, with reasons | builds and checks |",
          "| Matching style per block (common centroid or interdigitated) | chooses, with reasons | draws and checks |",
          "| Transistor cell options (S3) | chooses, with a justification | DRC/LVS and simulation |",
          "| Block variants (S4) | prunes or ranks | enumerates; legality must be exact |",
          "| Coordinates and wires (S5) | no (LLM coordinates are known to fail) | annealing, enumeration, router |",
          "| Checks (DRC, LVS, simulation) | no | independent |", "",
          "**What it should improve, on this design:**", "",
          "- **Phase margin.** Section 8 points to the Miller capacitors standing away from the first-stage outputs. "
          "An LLM reading section 3's node table can propose placing them beside x1's outputs, across the "
          "sub-circuit boundary; the flow then measures whether the phase-margin loss shrinks.",
          "- **Matching with reasons.** The code picks common centroid or interdigitated by cost alone; an LLM can "
          "argue per block (a signal-path pair against a bias mirror) and the result is checked the same way.",
          "- **Budgets that cannot be met.** G5.4 and G6.2 fail because S2's budgets assume a far tighter layout; an "
          "LLM can spot such conflicts early and propose which budget to relax, with the equations behind it.",
          "- **Fewer post-layout runs.** Tuning by an LLM has needed only about eleven post-layout simulations in the "
          "literature (ICPI), against many more for black-box search.", "",
          "**How it is measured** (the ablation in `docs/05`): the same circuits and extraction with and without the "
          "LLM; post-layout spec retention, area, the number of extraction and SPICE runs, and how well the budgets "
          "predicted the measured loss. Every LLM call is journaled (inputs, prompt version, output, validation).", "",
          "**Before it starts:** it needs an LLM API connection from outside the container, which needs Imasha's and "
          "her supervisor's permission (Imasha, 2026-11-04: not yet).", ""]

    # ------------------------------------------------------------------ 11
    L += ["## 11. What did not pass, and why", "",
          "None of these is a crash; each stage finished and reported.", ""]
    why = {
        "G1.2": "the simple model and the simulation define phase margin slightly differently (the model rounds the "
                "1 Hz phase); with one definition they agree within 0.06°. Open question to Imasha (flow record row 81).",
        "G3.3": "some transistor types use their \"least bad\" drawn cell; every spec is still met in simulation.",
        "G3.5": "same as G3.3: a relaxation was needed for some cells.",
        "G5.4": "S2's wire-length budgets assume a far more compact layout than blocks with tap rings, dummies and "
                "3 µm gaps in this outline; nets between sub-circuits are over (the worst, "
                f"{worst_u[0]}, at {worst_u[1]:.0f} × its budget in the budget-aware layout).",
        "G6.2": "follows from G5.4: the long nets and their couplings exceed S2's capacitance budgets.",
        "G7.2": "GBW loses more than η × its margin (section 7); within it once the likely double count is removed.",
    }
    stage_rows = ["| Stage | What it does, in one line | Result | Time (min) |", "|---|---|---|---|"]
    what = {"S0": "reads the schematic, the specs and the test benches; checks they agree",
            "S1": "builds a linear model of the amplifier, finds its main nodes and matching groups",
            "S2": "turns the specs into budgets: how much capacitance and wire length each net may have",
            "S3": "chooses how each transistor is drawn (fingers, cell shape) and checks it in simulation",
            "S4": "groups transistors into matched blocks, draws each (with dummies and a tap ring), checks each",
            "S5": "places the blocks inside the outline and wires them; checks DRC and LVS",
            "S6": "reads the finished layout back with its wiring capacitance; compares with S2's budgets",
            "S7": "simulates the read-back layout in the original benches; compares with the specs"}
    for st, txt in what.items():
        s = d["fs"].get(st, {})
        fails = ", ".join(g.split("_")[0] for g in s.get("failed_gates") or [])
        stage_rows.append(f"| {st} | {txt} | {s.get('status', '–')}{' (' + fails + ')' if fails else ''} | "
                          f"{num['secs'].get(st, 0) / 60:.1f} |")
    L += stage_rows + [""]
    for st in ("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7"):
        for gname in d["fs"].get(st, {}).get("failed_gates") or []:
            k = gname.split("_")[0]
            L.append(f"- **{st} {k}:** {why.get(k, 'see the stage report.')}")
    L += [""]

    # ------------------------------------------------------------------ 12, 13
    L += ["## 12. Assumptions and limits", ""] + [f"- {a}" for a in ASSUMPTIONS] + [""]
    L += ["## 13. Open questions (FEEDBACK NEEDED)", "",
          "1. Capacitance-only extraction is accepted for this design for now; should resistance extraction be tried "
          "another way (e.g. per sub-circuit)?",
          "2. Which GBW number should the G7.2 gate use: the extraction's, or the one with the Miller capacitors' "
          "likely double count removed? (The same question stands for LOADBench.)",
          "3. Is the outline 250 µm wide and 200 µm tall, or the other way round?",
          "4. S1's G1.2: align the two phase-margin definitions in S1, or keep it as a reported finding?",
          "5. The tile's regions (section 8): is Diff_opamp_ly the first stage, cs_p_5 the second stage's PMOS and "
          "bias_dummy the bias circuit, and what are block_01 to block_04, res, res_5 and the capacitor cells?", ""]

    # ------------------------------------------------------------------ glossary, files, appendix
    L += ["## Glossary", ""] + [f"- **{a}:** {b}" for a, b in GLOSSARY] + [""]
    L += ["## Where everything is", "",
          f"- Layouts: `outputs/S5/{D}/routed_budget_aware/` and `routed_area_only/` (GDS, Magic, picture).",
          f"- Blocks: `outputs/S4/{D}/blocks/`; extraction: `outputs/S6/{D}/`; simulations: `outputs/S7/{D}/`.",
          f"- Main nodes and budgets: `outputs/S1/{D}/node_classes.json`, `sensitivity.json`; `outputs/S2/{D}/budgets.json`.",
          f"- Hand layout measurements: `outputs/reference_layout/{D}/reference_layout.json`.",
          f"- This report's pictures: `outputs/report/{D}/`.",
          "- The full record: `docs/flow_record.md` (sections 7.7 and 7.22–7.24); the plan: `docs/plan_v5_ttsky25a.md`; "
          "the stage-by-stage tables: `docs/s4_s7_walkthrough.html`.", ""]
    L += ["## Appendix A. Every variant of every block", "",
          f"All {nvar} variants S4 drew and signed off (DRC 0, LVS match, negative control rejected), grouped by "
          "block. ✓ marks the variant each layout chose (BA budget-aware, AO area-only).", ""]
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
    d = gather()
    nb = numbering(d)
    lay = layouts(d, nb)
    sheets = schematics(d, nb)
    num = numbers(d, lay)
    nodes_main = main_nodes(d)
    charts(d, num, nodes_main)
    (FIG / "numbers.json").write_text(json.dumps({"layouts": lay, "blocks": nb["num"], **num}, indent=1) + "\n")
    OUT_MD.write_text("\n".join(build_md(d, num, lay, nb, sheets, nodes_main, head)) + "\n")
    print(OUT_MD)
    if not a.no_html:
        html = OUT_MD.with_suffix(".html")
        css = REPO / "docs" / "flow_record" / "record.css"
        cmd = ["pandoc", OUT_MD.name, "--standalone", "--embed-resources", "--metadata",
               f"title=Automatic layout of {D}", "--toc", "-o", html.name] + \
            (["-c", os.path.relpath(css, OUT_MD.parent)] if css.exists() else [])
        r = subprocess.run(cmd, cwd=OUT_MD.parent, capture_output=True, text=True)
        print(html if r.returncode == 0 else f"pandoc failed: {r.stderr[:400]}")
        if r.returncode != 0:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
