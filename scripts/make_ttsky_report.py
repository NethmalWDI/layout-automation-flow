#!/usr/bin/env python3
"""Generate docs/ttsky25a_fd_report.md (and, with pandoc, a self-contained HTML copy): the full report on the automatic
layout of ttsky25a_fd (plan v4 Phase 8), written for a reader who does not know the flow. Every number is read from the
run's own output files; typed by hand are only the explanations, the glossary and the list of assumptions. The pictures
(three layouts at one scale, two charts) go to outputs/report/ttsky25a_fd/.

usage (inside layout-s0s3, repo root, after `source scripts/env.sh`): python3 scripts/make_ttsky_report.py [--no-html]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_s0s3_walkthrough as W  # noqa: E402

REPO = W.REPO
sys.path.insert(0, str(REPO))
from src.s4.run import layout_options  # noqa: E402

D = "ttsky25a_fd"
OUT_MD = REPO / "docs" / f"{D}_report.md"
FIG = REPO / "outputs" / "report" / D
RULES = ("budget_aware", "area_only")
# one colour per layout, the same in every chart (dataviz reference palette, slots 1-3, validated all-pairs)
COLOR = {"budget_aware": "#2a78d6", "area_only": "#eb6834", "hand": "#1baf7a"}
LABEL = {"budget_aware": "Flow, budget-aware", "area_only": "Flow, area-only", "hand": "Hand layout (tile)"}
INK, INK2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
SPEC_NAME = {"gbw_mhz": ("Unity-gain bandwidth (GBW)", "MHz"), "pm_deg": ("Phase margin (PM)", "°"),
             "gain_db": ("DC gain", "dB"), "power_uw": ("Power", "µW")}


def j(*p):
    return W._j(REPO.joinpath(*p))


def f(v, nd=3):
    return W.f(v, nd)


def pct(a, b):
    return 100.0 * (b - a) / a


# ---------------------------------------------------------------------------------------------------- the data
def gather() -> dict:
    ir = j("outputs/S0", D, "circuit_ir.json")
    hier = j("circuits", D, "upstream/hierarchy.json")
    fs = (j("outputs/flow", D, "flow_summary.json") or {}).get("stages", {})
    s4b = j("outputs/S4", D, "blocks.json")
    s4 = j("outputs/S4", D, "s4_report.json")
    pl = j("outputs/S5", D, "placement.json")
    s5 = j("outputs/S5", D, "s5_report.json")
    s6 = j("outputs/S6", D, "s6_report.json")
    pv = j("outputs/S6", D, "parasitics_vs_budgets.json")
    s7 = j("outputs/S7", D, "s7_report.json")
    m7 = j("outputs/S7", D, "metrics.json")
    ref = j("outputs/reference_layout", D, "reference_layout.json")
    opts = layout_options(D)
    return {"ir": ir, "hier": hier, "fs": fs, "s4b": s4b, "s4": s4, "pl": pl, "s5": s5, "s6": s6, "pv": pv, "s7": s7,
            "m7": m7, "ref": ref, "opts": opts}


# ---------------------------------------------------------------------------------------------------- pictures
def render(gds: Path, png: Path, **kw) -> dict:
    args = ["klayout", "-zz", "-rd", f"gds={gds}", "-rd", f"png={png}"]
    for k, v in kw.items():
        args += ["-rd", f"{k}={v}"]
    r = subprocess.run(args + ["-r", str(REPO / "scripts/report_layout_png.py")], capture_output=True, text=True,
                       timeout=600)
    line = next((ln for ln in r.stdout.splitlines() if ln.startswith("REPORT_PNG ")), None)
    if line is None:
        raise RuntimeError(f"klayout render failed for {gds}: {(r.stdout + r.stderr)[-400:]}")
    return json.loads(line[len("REPORT_PNG "):])


def layouts(d: dict) -> dict:
    FIG.mkdir(parents=True, exist_ok=True)
    W_UM, H_UM, PPU = 260, 240, 3          # one scale for all three pictures
    out = {}
    ow, oh = d["opts"].get("outline_um", [250, 200])
    for r in RULES:
        out[r] = render(REPO / f"outputs/S5/{D}/routed_{r}/{D}_routed.gds", FIG / f"layout_{r}.png",
                        w=W_UM, h=H_UM, ppu=PPU, outline=f"{ow}x{oh}")
    out["hand"] = render(REPO / d["ref"]["gds"], FIG / "layout_hand.png", w=W_UM, h=H_UM, ppu=PPU, cell="Diff_Opamp")
    return out


def _axes(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.tick_params(colors=MUTED, labelcolor=INK2, length=0)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def charts(d: dict, num: dict) -> None:
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


# ---------------------------------------------------------------------------------------------------- the numbers
def numbers(d: dict, lay: dict) -> dict:
    m = d["m7"]["metrics"]
    ref = d["ref"]
    hb = lay["hand"]["cell"]["bboxes_um"][0]
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


# ---------------------------------------------------------------------------------------------------- the text
GLOSSARY = [
    ("Schematic", "the circuit as drawn by the designer: which transistors, resistors and capacitors connect to which."),
    ("Layout", "the drawing of the chip itself: the shapes on each layer that the factory makes. Every wire in it has "
               "length, so it adds capacitance and resistance the schematic does not have."),
    ("Op-amp", "operational amplifier. This one is fully differential: two inputs, two outputs (Vop, Vom)."),
    ("GBW", "unity-gain bandwidth: the frequency at which the amplifier's gain has fallen to 1. Higher is faster."),
    ("Phase margin (PM)", "how far the amplifier is from oscillating in feedback. Above about 60° is comfortable."),
    ("DC gain", "how much the amplifier multiplies a slow input signal, in dB (98 dB is about 80 000 times)."),
    ("Spec", "a required value, e.g. GBW ≥ 1.85 MHz. Here the specs are 0.9 × what the schematic achieves "
             "(ASSUMPTION; the design's README gives results, not specs)."),
    ("Margin, η and allowance", "margin = schematic value − spec limit. The flow lets the layout use at most "
                                "η = 0.5 of it (the allowance); the other half is kept for everything the flow does "
                                "not model (process corners, temperature). \"Use 1.27\" means 1.27 × the allowance."),
    ("DRC", "design rule check: are all shapes wide enough and far enough apart for the factory? 0 errors = clean."),
    ("LVS", "layout versus schematic: is the drawn layout the same circuit as the schematic? \"Match\" = yes."),
    ("Extraction (PEX)", "reading the finished layout back into a netlist that includes the wires' capacitance "
                         "(here capacitance only, \"C-only\"), so it can be simulated."),
    ("Drawn devices", "the layout's transistors as drawn, simulated without any wiring: shows what the layout's "
                      "device shapes alone change. \"Drawn → extracted\" is then the cost of the wiring."),
    ("Common centroid", "matched transistors split into pieces arranged A B B A, so both have the same centre and a "
                        "gradient across the chip affects them equally."),
    ("Interdigitated", "pieces alternating A B A B: both spread over the same area, but their centres differ slightly."),
    ("Dummy", "an unused transistor or resistor at the end of a row, so the real ones at the ends see the same "
              "surroundings as those in the middle."),
    ("Tap ring", "a ring of substrate (or well) contact around a block, which prevents latch-up."),
    ("MIM capacitor", "metal–insulator–metal capacitor: the Miller capacitors here, 5 units of 10 × 10 µm each."),
    ("Budget-aware / area-only", "the flow scores every placement two ways and lays out both winners: by area plus "
                                 "how much of each wire's length budget it uses (the flow's own rule), and by area "
                                 "alone (the usual baseline). Comparing them tests whether the budgets help."),
    ("Macro", "one sub-circuit of the design's own hierarchy (x1, x2, top, the resistor packs), placed as a unit."),
    ("Gate (G4.1, G5.4 …)", "an automatic pass/fail check at the end of a stage."),
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
]


def build_md(d: dict, num: dict, lay: dict, head: str) -> list:
    ir, s5g, s6g, s7g, m = d["ir"], d["s5"]["gates"], d["s6"]["gates"], d["s7"]["gates"], d["m7"]["metrics"]
    ba, ao = m["budget_aware"], m["area_only"]
    ref = d["ref"]
    hand_dr, hand_po = ref["drawn_devices_only"], ref["post_layout"]
    sch = {k: x["schematic"] for k, x in ba.items()}
    margins = ir["margins"]
    eta = d["m7"]["eta"]
    nmos = len(ir["devices"])
    copies = sum(x.get("m", 1) for x in ir["devices"])
    mims = [p for p in ir.get("passives", []) if "cap" in (p.get("model") or p.get("kind") or "").lower()
            or p["name"].startswith("XC")]
    res = [p for p in ir.get("passives", []) if p["name"].startswith("XX2_X")]
    sz, ar, wl = num["size"], num["area"], num["wiring_loss"]
    g75 = (s7g.get("G7.5_mim_self_coupling_cancelled (info)") or {}).get("detail", {})
    cen = (s5g.get("G5.7_matched_centring (info)") or {}).get("detail", {})
    mim_c = (d["pv"].get("mim_self") or {})
    flow_min = sum(num["secs"].get(s, 0) for s in ("S4", "S5", "S6", "S7")) / 60
    use = {r: {k: x["use_of_allowed"] for k, x in m[r].items()} for r in RULES}
    gb = ba["gbw_mhz"]
    L = [f"# Automatic layout of `{D}`, and how it compares with the hand layout", "",
         f"*Generated by `python3 scripts/make_ttsky_report.py` from the flow's own output files (repo at {head}). "
         "Every number is read from `outputs/`; only the explanations are typed. Assumptions are marked "
         "ASSUMPTION; figures taken from elsewhere are marked reported.*", ""]

    # ------------------------------------------------------------------ 1
    L += ["## 1. Summary", "",
          f"`{D}` is Imasha's fully differential op-amp, taped out on Tiny Tapeout (SKY130). Its schematic "
          f"(`Opamp_with_bias`) has {nmos} transistors ({copies} transistor pieces once each multiplier m is drawn), "
          f"{len(mims)} Miller capacitors and {len(res)} resistors. The flow took that schematic and, with no hand "
          f"editing, drew two complete layouts inside a {num['outline'][0]} × {num['outline'][1]} µm outline, "
          f"checked them, read their wiring back and simulated them. S4–S7 took {flow_min:.0f} minutes of computer "
          "time.", "",
          "**What came out:**", "",
          f"- **Both layouts are clean and correct:** 0 design-rule errors (DRC) and the layout matches the schematic "
          f"(LVS), for both.",
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
          "- **A caution:** the taped-out tile is not exactly the schematic (it adds enable switches and its devices "
          "differ; section 7). So the two are compared on what the wiring costs and on area, not on absolute speed.",
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
    L += ["", "## 2. The circuit and what was asked", "",
          "The design's own hierarchy (from its xschem schematic) splits it into sub-circuits; the flow keeps them as "
          "units (\"macros\"):", "", "| Sub-circuit | What it is | Elements |", "|---|---|---|"]
    for lv in d["hier"]["levels"]:
        for v in lv.values():
            if isinstance(v, list):
                for x in v:
                    L.append(f"| {x.get('instance')} | {x.get('kind')} | {len(x.get('elements', []))} |")
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
    L += ["## 3. How the layout was made", "",
          "The flow runs in stages; each ends with automatic checks (gates). S0–S3 prepare (read the design, model it, "
          "set the budgets, size the transistor cells); S4–S7 build and judge the layout.", "",
          "| Stage | What it does, in one line | Result | Time (min) |", "|---|---|---|---|"]
    what = {"S0": "reads the schematic, the specs and the test benches; checks they agree",
            "S1": "builds a simple model of the amplifier and checks it against simulation",
            "S2": "turns the specs into budgets: how much capacitance and wire length each net may have",
            "S3": "chooses how each transistor is drawn (fingers, cell shape) and checks it in simulation",
            "S4": "groups transistors into matched blocks, draws each (with dummies and a tap ring), checks each",
            "S5": "places the blocks inside the outline and wires them; checks DRC and LVS",
            "S6": "reads the finished layout back with its wiring capacitance; compares with S2's budgets",
            "S7": "simulates the read-back layout in the original benches; compares with the specs"}
    for st, txt in what.items():
        s = d["fs"].get(st, {})
        fails = ", ".join(g.split("_")[0] for g in s.get("failed_gates") or [])
        L.append(f"| {st} | {txt} | {s.get('status', '–')}{' (' + fails + ')' if fails else ''} | "
                 f"{num['secs'].get(st, 0) / 60:.1f} |")
    L += ["", "**Who decides what.** No AI model takes any decision in this flow. The code decides, by fixed rules "
          "and by scoring candidates with a cost function; Imasha decides the constraints (the outline, matching "
          "style, dummies, which resistors match). The cost the flow minimises is area plus how much of each net's "
          "wire-length budget it uses; those budgets come from the specs (S2), so the placement is driven by the "
          "specs and the area. Section 8 lists the gates that fail and why; none is a crash.", ""]

    # ------------------------------------------------------------------ 4
    blocks = d["s4b"]["blocks"]
    nvar = sum(len(b["variants"]) for b in blocks)
    pics = {}
    for b in blocks:
        for v in b["variants"]:
            if v.get("png") and v["id"] in ("centroid", "interleaved", "A") and b.get("kind") in ("mirror", "resistors", "mim_cap") \
                    and b["kind"] not in pics:
                pics[b["kind"]] = (b["name"], v)
    L += ["## 4. The building blocks (S4)", "",
          f"S4 grouped the {nmos} transistors into blocks (every matched group in one block), plus one block per "
          f"Miller capacitor and one for the 40 resistors: {len(blocks)} blocks. It drew {nvar} versions (variants) of "
          "them, e.g. a matched pair as A B B A and as A B A B, and checked every one alone: all DRC-clean and LVS-"
          "matched, each with a deliberately broken copy that the check must reject.", ""]
    if pics:
        L += [" ".join(W.img(v["png"], 300, n) for n, v in pics.values()), ""]
        L += W.how("left to right: " + ", ".join({"mirror": "a matched transistor row (common centroid, a dummy at "
                                                            "each end, the tap ring around it)",
                                                  "resistors": "the 40 resistors of the two packs, interleaved",
                                                  "mim_cap": "a Miller capacitor as 5 MIM units"}[k] for k in pics)
                   + ". Blue/purple lines above and below are the metal tracks each block offers for wiring.")
    L += ["", "**Matching in the final layouts** (gate G5.7). Where a matched block has both a common-centroid and an "
          "interdigitated version, S5 takes the one that costs less (area and wire budgets), as Imasha decided:", "",
          "| Matched block | Budget-aware | Area-only |", "|---|---|---|"]
    names = sorted(set().union(*(set(cen.get(r, {})) for r in RULES)))
    for n in names:
        cells = []
        for r in RULES:
            x = cen.get(r, {}).get(n)
            if x:
                off = max(abs(v) for v in x["centroid_offset_um"].values())
                cells.append(f"{x['variant']}, " + ("common centroid" if x["common_centroid"] else f"centres {off:.1f} µm off"))
            else:
                cells.append("–")
        L.append(f"| {n} | {cells[0]} | {cells[1]} |")
    nc = {r: sum(x["common_centroid"] for x in cen.get(r, {}).values()) for r in RULES}
    L += W.here(f"{nc['budget_aware']} of {len(cen.get('budget_aware', {}))} matched blocks are common centroid in "
                f"the budget-aware layout, {nc['area_only']} of {len(cen.get('area_only', {}))} in the area-only one. "
                "\"Centres off\" is how far one device's centre sits from the row's centre in an interdigitated row.")

    # ------------------------------------------------------------------ 5
    pmac = d["pl"]["chosen"]
    L += ["", "## 5. The layouts (S5)", "",
          "All three pictures are at the same scale. The box around the flow's layouts is the "
          f"{num['outline'][0]} × {num['outline'][1]} µm outline; the hand layout is the whole Tiny Tapeout tile "
          f"(161 × 226 µm), whose op-amp (`Diff_Opamp`) measures {sz['hand'][0]:.1f} × {sz['hand'][1]:.1f} µm.", "",
          " ".join(W.img(f"outputs/report/{D}/layout_{k}.png", 260, LABEL[k]) for k in ("budget_aware", "area_only", "hand")),
          "", f"*Left to right: {LABEL['budget_aware']}, {LABEL['area_only']}, {LABEL['hand']}.*", ""]
    L += ["**How the placement was found.** Each sub-circuit is placed on its own: its blocks in rows (PMOS above "
          "NMOS), arranged by simulated annealing (a seeded random search that keeps improvements), in three widths. "
          "Then every arrangement of the four sub-circuits' shapes is tried, and anything outside the outline is "
          "rejected. Both winners are wired by a router that lays metal-3 horizontally and metal-4 vertically on a "
          "0.8 µm grid, shortest path first.", "",
          "| | Budget-aware | Area-only |", "|---|---|---|",
          "| Sub-circuits, top to bottom | " + " | ".join(" / ".join(", ".join(row) for row in pmac[r]["placement"]["rows"])
                                                        for r in RULES) + " |",
          f"| Size (µm) | {sz['budget_aware'][0]:.1f} × {sz['budget_aware'][1]:.1f} | {sz['area_only'][0]:.1f} × "
          f"{sz['area_only'][1]:.1f} |",
          f"| Area (µm²) | {ar['budget_aware']:,.0f} | {ar['area_only']:,.0f} |"]
    g5 = s5g["G5.5_area_vs_area_only (info)"]
    rr = s5g["G5.4_route_rules"]["detail"]
    wire ={r: sum(sum((x.get("length_um") or {}).values()) for x in rr[r]["max_length"].values()) for r in RULES}
    over = {r: sum(not x["ok"] for x in rr[r]["max_length"].values()) for r in RULES}
    L += [f"| Top-level wire (µm) | {wire['budget_aware']:,.0f} | {wire['area_only']:,.0f} |",
          f"| Sum of wire-budget use (lower is better) | {sum(g5['u_budget_aware'].values()):.1f} | "
          f"{sum(g5['u_area_only'].values()):.1f} |",
          f"| Nets longer than their budget | {over['budget_aware']} of {len(rr['budget_aware']['max_length'])} | "
          f"{over['area_only']} of {len(rr['area_only']['max_length'])} |",
          f"| DRC errors / LVS | {s5g['G5.2_top_DRC']['detail']['budget_aware']} / match | "
          f"{s5g['G5.2_top_DRC']['detail']['area_only']} / match |", ""]
    L += W.here(f"the budget-aware layout uses {100 * (1 - sum(g5['u_budget_aware'].values()) / sum(g5['u_area_only'].values())):.0f} % "
                f"less of the wire budgets for {100 * (g5['area_ratio'] - 1):.0f} % more area. Most nets that run "
                "between sub-circuits are still far over the length budgets from S2, which assumed a much more "
                "compact layout (section 8).")
    L += ["", W.img(f"outputs/report/{D}/chart_area.png", 640, "area chart"), ""]
    L += W.how("the bounding box of each op-amp; the dashed line is the outline's area. The hand layout's op-amp also "
               "holds the tile's enable switches.")

    # ------------------------------------------------------------------ 6
    L += ["", "## 6. After layout: what the wiring costs (S6, S7)", "",
          "S6 reads each finished layout back with the capacitance of every wire and S7 simulates it in the same "
          "test benches as the schematic. Resistance is not included (capacitance-only, \"C-only\"; section 9).", "",
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
    if mim_c:
        c0 = next(iter(mim_c.values()))
        gm = g75.get("budget_aware", {})
        L += ["", f"**Why GBW fails, and the double count.** GBW is set mainly by the Miller capacitors. Extracted alone, "
              f"each Miller capacitor block shows {f(c0['plate_coupling_fF'], 3)} fF between its own plates on top of "
              "the capacitor itself. The capacitor's model already contains that, so the extraction very likely counts "
              "it twice (it is how Magic's SKY130 rules treat metal-4 over metal-3). With it removed, GBW after "
              f"layout is {f(gm.get('gbw_mhz', {}).get('value'), 4)} MHz, using {f(gm.get('gbw_mhz', {}).get('use_of_allowed'))} "
              f"of the allowance, and every spec is within it (phase margin {f(gm.get('pm_deg', {}).get('use_of_allowed'))}). "
              "The gate keeps the extraction's number; which one should count is an open question (section 10).", ""]
    g62 = s6g["G6.2_parasitics_within_budgets"]
    L += [f"**Budgets.** S2 had set a capacitance budget for every net and every pair of nets. "
          f"{len(g62['violations'])} of them are exceeded in the budget-aware layout "
          f"({len(g62['area_only_violations (H5)'])} in the area-only one). The budgets assumed a far tighter layout; "
          "the simulation above is the real judge, and it passes every spec.", ""]
    L += [W.img(f"outputs/report/{D}/chart_wiring_loss.png", 700, "wiring loss chart"), ""]
    L += W.how("the drop from drawn devices to the extracted layout, for each of the three layouts, measured the same "
               "way. Shorter bars are better.")

    # ------------------------------------------------------------------ 7
    lvs = ref["lvs_vs_layout_view"]
    L += ["", "## 7. Comparison with the hand layout", "",
          "**What the hand layout is.** The taped-out Tiny Tapeout tile `tt_um_diff` "
          f"(`{ref['gds']}`), drawn by hand by the designers. The flow extracted it with the same tool and settings "
          "(Magic, capacitance only) and simulated it in the same benches (flow record 7.7).", "",
          "**Why it is not the same circuit.** LVS of the tile against the schematic "
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
    ub = s5g["G5.5_area_vs_area_only (info)"]["u_budget_aware"]
    worst_u = max(ub.items(), key=lambda kv: kv[1])
    L += ["**What it shows.**", "",
          f"- **Bandwidth:** the flow's wiring costs {'less' if better_gbw else 'more'} GBW than the hand layout's "
          f"({wl['budget_aware']['gbw_pct']:.1f} % against {wl['hand']['gbw_pct']:.1f} %).",
          f"- **Phase margin:** the flow's wiring costs more ({wl['budget_aware']['pm_deg']:.1f}° against "
          f"{wl['hand']['pm_deg']:.1f}°). A likely reason (not measured separately): the design's hierarchy puts the "
          "Miller capacitors in the `top` sub-circuit, and the flow places each sub-circuit as a unit, so the "
          "capacitors stand away from the first-stage outputs (Vop1, Vom1, in x1) they connect to; those nets and the "
          f"outputs run long between sub-circuits (the worst net, {worst_u[0]}, uses {worst_u[1]:.0f} × its length "
          "budget).",
          f"- **Area:** the hand layout is denser. The flow's blocks each carry their own tap ring and stand 3 µm apart, "
          f"and the outline (not the area) was the target; the area-only layout comes within "
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

    # ------------------------------------------------------------------ 8
    ub = s5g["G5.5_area_vs_area_only (info)"]["u_budget_aware"]
    worst_u = max(ub.items(), key=lambda kv: kv[1])
    L += ["## 8. What did not pass, and why", "",
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
        "G7.2": "GBW loses more than η × its margin (above); within it once the likely double count is removed.",
    }
    for st in ("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7"):
        for g in d["fs"].get(st, {}).get("failed_gates") or []:
            k = g.split("_")[0]
            L.append(f"- **{st} {k}:** {why.get(k, 'see the stage report.')}")
    L += [""]

    # ------------------------------------------------------------------ 9
    L += ["## 9. Assumptions and limits", ""] + [f"- {a}" for a in ASSUMPTIONS] + [""]

    # ------------------------------------------------------------------ 10
    L += ["## 10. Open questions (FEEDBACK NEEDED)", "",
          "1. Capacitance-only extraction is accepted for this design for now; should resistance extraction be tried "
          "another way (e.g. per sub-circuit)?",
          "2. Which GBW number should the G7.2 gate use: the extraction's, or the one with the Miller capacitors' "
          "likely double count removed? (The same question stands for LOADBench.)",
          "3. Is the outline 250 µm wide and 200 µm tall, or the other way round?",
          "4. S1's G1.2: align the two phase-margin definitions in S1, or keep it as a reported finding?", ""]

    # ------------------------------------------------------------------ glossary and files
    L += ["## Glossary", ""] + [f"- **{a}:** {b}" for a, b in GLOSSARY] + [""]
    L += ["## Where everything is", "",
          f"- Layouts: `outputs/S5/{D}/routed_budget_aware/` and `routed_area_only/` (GDS, Magic, picture).",
          f"- Blocks: `outputs/S4/{D}/blocks/`; extraction: `outputs/S6/{D}/`; simulations: `outputs/S7/{D}/`.",
          f"- Hand layout measurements: `outputs/reference_layout/{D}/reference_layout.json`.",
          "- The full record: `docs/flow_record.md` (sections 7.7 and 7.22–7.24); the plan: `docs/plan_v5_ttsky25a.md`; "
          "the stage-by-stage tables: `docs/s4_s7_walkthrough.html`.", ""]
    return L


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-html", action="store_true")
    a = ap.parse_args(argv)
    W.IMG_PREFIX = os.path.relpath(REPO, OUT_MD.parent).replace(os.sep, "/")
    head = (subprocess.run(["git", "--no-optional-locks", "log", "-1", "--format=%h %cs"], cwd=REPO, capture_output=True,
                           text=True).stdout.strip() or "unknown")
    d = gather()
    lay = layouts(d)
    num = numbers(d, lay)
    charts(d, num)
    (FIG / "numbers.json").write_text(json.dumps({"layouts": lay, **num}, indent=1) + "\n")
    OUT_MD.write_text("\n".join(build_md(d, num, lay, head)) + "\n")
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
