#!/usr/bin/env python3
"""A simple report for any design, from the flow's own outputs only (no LLM, no hand-typed numbers): what the design
is, the specs, the stages and their checks, the main nodes and budgets, every block, the layouts, the results after
layout, and a comparison with a hand-drawn reference layout where one was measured. Sections a design has not reached
yet are left out. The local GUI (gui/gui.ps1) runs it after the flow; docs/ttsky25a_fd_report.html is the long,
hand-explained version of the same report for one design.

usage (inside layout-s0s3, repo root, after `source scripts/env.sh`):
  python3 scripts/make_design_report.py <design> [--no-html]
writes docs/reports/<design>_report.md and .html (self-contained), pictures in outputs/report/<design>/simple/.
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
import report_figures as F  # noqa: E402

REPO = W.REPO
sys.path.insert(0, str(REPO))
from src.s4.run import layout_options  # noqa: E402
from src.s5 import macro as M5, place as P5  # noqa: E402

RULES = ("budget_aware", "area_only")
COLOR = {"budget_aware": "#2a78d6", "area_only": "#eb6834", "hand": "#1baf7a"}
LABEL = {"budget_aware": "Flow, budget-aware", "area_only": "Flow, area-only", "hand": "Hand layout"}
GROUP_COLORS = ["#e87ba4", "#008300", "#eda100", "#6250d6"]   # validated all-pairs (dataviz slots 4-7)
GRAY = "#898781"
INK, INK2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
SPEC_NAME = {"gbw_mhz": ("Unity-gain bandwidth (GBW)", "MHz"), "pm_deg": ("Phase margin", "°"),
             "gain_db": ("DC gain", "dB"), "power_uw": ("Power", "µW"), "cmrr_db": ("CMRR", "dB"),
             "vnoise_nv_rthz": ("Input noise", "nV/√Hz")}
STAGE_DOES = {"S0": "reads the netlist, specs and test benches; checks they agree (and that the sources are unchanged)",
              "S1": "builds a linear model of the circuit; finds its main nodes and matching groups",
              "S2": "turns the specs into budgets: how much capacitance, resistance and wire length each net may have",
              "S3": "chooses how each transistor is drawn (fingers, cell shape), checked in simulation",
              "S4": "draws the matched blocks (with dummies and tap rings where asked) and checks each",
              "S5": "places the blocks (inside the outline, if one is given) and routes them; DRC and LVS",
              "S6": "reads the layout back with its wiring capacitance; compares with the budgets",
              "S7": "simulates the read-back layout in the original benches; compares with the specs"}
GLOSSARY = [
    ("GBW", "unity-gain bandwidth: where the gain falls to 1. Higher is faster."),
    ("Phase margin", "how far the amplifier is from oscillating in feedback; above about 60° is comfortable."),
    ("Margin, η, allowance", "margin = schematic value − spec limit; the layout may use η of it (the allowance)."),
    ("DRC / LVS", "design-rule check (0 errors = manufacturable) / layout versus schematic (\"match\" = same circuit)."),
    ("Extraction", "reading the layout back with its wires' capacitance (C-only) or also resistance (R+C)."),
    ("Drawn devices", "the layout's transistors without any wiring; \"drawn → extracted\" is the wiring's cost."),
    ("Block / variant", "transistors drawn together as one piece (B1 …) / one way of drawing it (A B B A, A B A B …)."),
    ("Budget-aware / area-only", "placement scored by area plus wire budgets (the flow's rule) / by area alone."),
    ("Gate", "an automatic pass/fail check at the end of a stage (G4.1, G5.4 …)."),
]
WHO = [("Specs, budgets, cells, blocks, placement, routing, checks", "code (fixed rules and searches; settings in PREREG)"),
       ("Design, specs' basis, layout instructions (outline, matching, dummies, hierarchy)", "the designer (the GUI's inputs)"),
       ("The flow's code, its rules and defaults", "written with an LLM (Claude); no LLM is called during a run")]


def j(p: Path):
    return W._j(p)


def f(v, nd=3):
    return W.f(v, nd)


def fig_html(src: str, caption: str, color: str | None = None, width: str = "31%") -> str:
    bar = f"border-top:5px solid {color};" if color else ""
    return (f'<figure style="display:inline-block;width:{width};margin:4px;vertical-align:top;{bar}">'
            f'<img src="{W.IMG_PREFIX}/{src}" style="width:100%" alt="{caption.split("<")[0]}">'
            f'<figcaption style="font-size:0.8em">{caption}</figcaption></figure>')


def render(gds: Path, png: Path, **kw) -> dict | None:
    args = ["klayout", "-zz", "-rd", f"gds={gds}", "-rd", f"png={png}"]
    for k, v in kw.items():
        args += ["-rd", f"{k}={v}"]
    for _ in range(4):   # the Windows-mounted repo now and then refuses a write (Errno 22)
        r = subprocess.run(args + ["-r", str(REPO / "scripts/report_layout_png.py")], capture_output=True, text=True,
                           timeout=600)
        line = next((ln for ln in r.stdout.splitlines() if ln.startswith("REPORT_PNG ")), None)
        if line:
            o = json.loads(line[len("REPORT_PNG "):])
            w, h = float(kw.get("w", 260)), float(kw.get("h", 240))
            cx, cy = (o["bbox_um"][0] + o["bbox_um"][2]) / 2, (o["bbox_um"][1] + o["bbox_um"][3]) / 2
            o["window_um"] = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
            return o
    return None


def _axes(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.tick_params(colors=MUTED, labelcolor=INK2, length=0)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def bars(fig_path: Path, panels: list) -> None:
    """panels: [(title, unit, [(key, value)])]: one horizontal bar chart per measure, layouts in fixed colours."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans"})
    fig, axs = plt.subplots(1, len(panels), figsize=(4.4 * len(panels), 0.6 + 0.55 * max(len(p[2]) for p in panels)),
                            dpi=150, squeeze=False)
    fig.patch.set_facecolor(SURFACE)
    for k, (ax, (title, unit, rows)) in enumerate(zip(axs[0], panels)):
        _axes(ax)
        vals = [v for _, v in rows]
        ax.barh([LABEL[k_] for k_, _ in rows], vals, height=0.5, color=[COLOR[k_] for k_, _ in rows],
                edgecolor=SURFACE, linewidth=2)
        top = max(max(vals), 1e-9)
        for i, v in enumerate(vals):
            ax.text(v + top * 0.02, i, f"{v:,.3g}{unit}", va="center", color=INK, fontsize=9)
        ax.set_xlim(0, top * 1.3)
        ax.set_title(title, loc="left", color=INK, fontsize=10.5)
        if k:
            ax.set_yticklabels([])
    fig.tight_layout()
    fig.savefig(fig_path, facecolor=SURFACE)
    plt.close(fig)


def build(d: str) -> list:
    out_dir = REPO / "outputs" / "report" / d / "simple"
    out_dir.mkdir(parents=True, exist_ok=True)
    rel_fig = f"outputs/report/{d}/simple"
    pkg_text = (REPO / "inputs" / d / "package.yaml").read_text()
    import yaml
    pkg = yaml.safe_load(pkg_text)
    opts = layout_options(d)
    fs = (j(REPO / "outputs/flow" / d / "flow_summary.json") or {}).get("stages", {})
    ir = j(REPO / "outputs/S0" / d / "circuit_ir.json")
    rep = {s: j(REPO / "outputs" / s / d / f"{s.lower()}_report.json") for s in fs}
    m7 = j(REPO / "outputs/S7" / d / "metrics.json")
    pl = j(REPO / "outputs/S5" / d / "placement.json")
    s4b = j(REPO / "outputs/S4" / d / "blocks.json")
    ref = j(REPO / "outputs/reference_layout" / d / "reference_layout.json")
    head = (subprocess.run(["git", "--no-optional-locks", "log", "-1", "--format=%h %cs"], cwd=REPO, capture_output=True,
                           text=True).stdout.strip() or "unknown")
    L = [f"# Layout report: `{d}`", "",
         f"*Generated by `python3 scripts/make_design_report.py {d}` from the flow's own output files (repo at {head}); "
         "no number is typed by hand and no LLM is used. Assumptions are marked ASSUMPTION in the inputs.*", "",
         "## 1. The design", "", " ".join((pkg.get("description") or "").split()), ""]
    if ir:
        nm = len(ir["devices"])
        L += [f"- **Devices:** {nm} transistors ({sum(x.get('m', 1) for x in ir['devices'])} pieces once each "
              f"multiplier m is drawn), {len(ir.get('passives', []))} passives.",
              f"- **Netlist:** `{pkg['netlist']}`; specs: `{pkg['config']}`.",
              f"- **Layout instructions:** " + (f"`inputs/{d}/layout.yaml`: " + ", ".join(
                  f"{k} = {v}" for k, v in opts.items() if not isinstance(v, (list, dict)) or k == "outline_um")
                  if opts else "none (the flow's defaults)") + ".", ""]
    # ---------------------------------------------------------------- stages
    L += ["## 2. The stages and their checks", "", "| Stage | What it does | Result | Failed checks | Time (min) |",
          "|---|---|---|---|---|"]
    for st, txt in STAGE_DOES.items():
        s = fs.get(st, {})
        secs = sum(x.get("seconds") or 0 for x in s.get("steps", []))
        fails = ", ".join(g.replace("_", " ") for g in s.get("failed_gates") or []) or "–"
        L.append(f"| {st} | {txt} | **{s.get('status', 'not run')}** | {fails} | {secs / 60:.1f} |")
    L += ["", "*Who decides what:* " + "; ".join(f"{a}: {b}" for a, b in WHO) + ".", ""]
    # ---------------------------------------------------------------- specs and results
    if ir and ir.get("margins"):
        eta = (m7 or {}).get("eta", 0.5)
        L += ["## 3. Specs", "", "| Spec | Schematic | Limit | Margin | Allowance for the layout |", "|---|---|---|---|---|"]
        for k, mg in ir["margins"].items():
            name, unit = SPEC_NAME.get(k, (k, ""))
            L.append(f"| {name} ({unit}) | {f(mg.get('achieved'), 5)} | {'≥' if mg['kind'] == 'min' else '≤'} "
                     f"{f(mg['limit'], 5)} | {f(mg['margin'], 4)} | {f(eta * mg['margin'], 4)} |")
        L += [""]
    # ---------------------------------------------------------------- main nodes
    nodes = (j(REPO / "outputs/S1" / d / "node_classes.json") or {}).get("nodes")
    sens = (j(REPO / "outputs/S1" / d / "sensitivity.json") or {}).get("table")
    bud = {e["id"]: e for e in (j(REPO / "outputs/S2" / d / "budgets.json") or {}).get("elements", [])}
    pv = j(REPO / "outputs/S6" / d / "parasitics_vs_budgets.json")
    rows6 = {x["id"]: x for x in (((pv or {}).get("layouts") or {}).get("budget_aware") or {}).get("budgets", {}).get("rows", [])}
    if nodes and sens:
        pick = {n for n, v in nodes.items() if (v.get("pole_rank") or 99) <= 6 or v.get("high_impedance")
                or "signal_output" in (v.get("tags") or [])}
        for key in ("gbw_mhz", "pm_deg"):
            if all(key in sens[n] for n in sens if "~" not in n):
                pick |= set(sorted((n for n in sens if "~" not in n), key=lambda n: sens[n][key]["linear_per_fF"])[:4])
        L += ["## 4. The main nodes (S1) and their budgets (S2)", "",
              "| Node | Role | Pole rank | GBW lost per fF (kHz) | PM lost per fF (m°) | Budget (fF) | Extracted (fF) | Use |",
              "|---|---|---|---|---|---|---|---|"]
        for n in sorted(pick, key=lambda n: nodes.get(n, {}).get("pole_rank") or 99):
            v, s, b, r6 = nodes.get(n, {}), sens.get(n, {}), bud.get(n, {}), rows6.get(n, {})

            def sv(key):
                x = -1000 * (s.get(key) or {}).get("linear_per_fF", 0)
                return "≈ 0" if abs(x) < 1e-6 else f(x, 3)
            L.append(f"| {n} | {', '.join(v.get('tags') or []) or ('high impedance' if v.get('high_impedance') else '–')} | "
                     f"{v.get('pole_rank', '–')} | {sv('gbw_mhz')} | {sv('pm_deg')} | {f(b.get('budget'), 3) if b else '–'} | "
                     f"{f(r6.get('value'), 3) if r6 else '–'} | "
                     f"{('**' + f(r6['use']) + '**') if r6 and not r6.get('ok') else (f(r6['use']) if r6 else '–')} |")
        L += W.how("pole rank 1 is the dominant pole; the two sensitivity columns say how much GBW and phase margin "
                   "drop per fF of wiring on the node; \"use\" is extracted / budget in the budget-aware layout (bold: "
                   "over).")
        bode = REPO / "outputs/S1" / d / "plots/bode_linear_vs_spice.png"
        if bode.exists():
            L += ["", W.img(f"outputs/S1/{d}/plots/bode_linear_vs_spice.png", 560, "bode"), ""]
            L += W.how("open-loop gain and phase: SPICE on the transistors (solid) against S1's linear model (dashed); "
                       "where they agree, every estimate built on the model can be trusted.")
        L += [""]
    # ---------------------------------------------------------------- blocks
    if s4b and pl:
        ch = pl["chosen"]["budget_aware"]["placement"]
        group = {b: (p.get("macro") or next((x["type"] for x in s4b["blocks"] if x["name"] == b), "?"))
                 for b, p in ch["blocks"].items()}
        gnames = list(dict.fromkeys(sorted(set(group.values()))))
        gcol = {g: (GROUP_COLORS[i] if i < len(GROUP_COLORS) else GRAY) for i, g in enumerate(gnames)}
        order = sorted(s4b["blocks"], key=lambda b: (gnames.index(group.get(b["name"], "?")) if b["name"] in group else 99,
                                                     b["name"]))
        num = {b["name"]: i + 1 for i, b in enumerate(order)}
        nvar = sum(len(b["variants"]) for b in s4b["blocks"])
        L += ["## 5. The blocks (S4)", "",
              f"{len(s4b['blocks'])} blocks, {nvar} variants, "
              + ("all signed off (DRC 0, LVS match, negative control rejected)." if all(
                  v.get("ok") for b in s4b["blocks"] for v in b["variants"]) else "not all signed off.")
              + " Colour bar: " + ", ".join(f'<span style="color:{gcol[g]}">■</span> {g}' for g in gnames)
              + ". The picture is the variant the budget-aware layout chose.", ""]
        figs = []
        for b in order:
            vba = pl["chosen"]["budget_aware"]["placement"]["blocks"].get(b["name"], {}).get("variant")
            vao = pl["chosen"]["area_only"]["placement"]["blocks"].get(b["name"], {}).get("variant")
            v = next((x for x in b["variants"] if x["id"] == vba), b["variants"][0])
            devs = b["devices"] if len(b["devices"]) <= 4 else b["devices"][:3] + [f"… ({len(b['devices'])})"]
            if v.get("png"):
                figs.append(fig_html(v["png"], f"<b>B{num[b['name']]} {b['name']}</b><br>{', '.join(devs)}<br>"
                                     f"variant {vba}" + (f" (area-only: {vao})" if vao != vba else ""),
                                     gcol.get(group.get(b["name"]), GRAY)))
        L += ["<div>" + "".join(figs) + "</div>", ""]
        # ------------------------------------------------------------ layouts
        L += ["## 6. The layouts (S5)", ""]
        s5g = rep.get("S5", {}).get("gates", {}) if rep.get("S5") else {}
        for r in RULES:
            gds = REPO / f"outputs/S5/{d}/routed_{r}/{d}_routed.gds"
            if not gds.exists():
                continue
            plr = pl["chosen"][r]["placement"]
            bb = plr["bbox"]
            w, h = (bb[2] - bb[0]) * 1.12 + 10, (bb[3] - bb[1]) * 1.12 + 10
            ol = opts.get("outline_um")
            if ol:
                w, h = max(w, ol[0] * 1.04), max(h, ol[1] * 1.04)
            kw = {"w": round(w, 1), "h": round(h, 1), "ppu": round(min(40, 1400 / max(w, h)), 2)}
            if ol:
                kw["outline"] = f"{ol[0]}x{ol[1]}"
            o = render(gds, out_dir / f"layout_{r}.png", **kw)
            if not o:
                continue
            rects = [(m["bbox"], gcol.get(k, GRAY), k) for k, m in (plr.get("macros") or {}).items()]
            labels = [((b["bbox"][0] + b["bbox"][2]) / 2, (b["bbox"][1] + b["bbox"][3]) / 2, f"B{num[n]}")
                      for n, b in plr["blocks"].items() if n in num]
            F.annotate(out_dir / f"layout_{r}.png", o["window_um"], rects, labels, out_dir / f"layout_{r}_annot.png",
                       title=f"{LABEL[r]}" + (" (box: the outline)" if ol else ""),
                       legend=[(g, gcol[g]) for g in gnames] if plr.get("macros") else None)
            L += [f"**{LABEL[r]}**", "", W.img(f"{rel_fig}/layout_{r}_annot.png", 760, r), ""]
        size = (s5g.get("G5.6_outline") or {}).get("size_um") or {
            r: [round(pl["chosen"][r]["placement"]["bbox"][2] - pl["chosen"][r]["placement"]["bbox"][0], 2),
                round(pl["chosen"][r]["placement"]["bbox"][3] - pl["chosen"][r]["placement"]["bbox"][1], 2)] for r in RULES}
        g5 = s5g.get("G5.5_area_vs_area_only (info)") or {}
        drc = (s5g.get("G5.2_top_DRC") or {}).get("detail") or {}
        lvs = (s5g.get("G5.3_top_LVS") or {}).get("detail") or {}
        L += ["| | Budget-aware | Area-only |", "|---|---|---|",
              "| Size (µm) | " + " | ".join(f"{size[r][0]:.1f} × {size[r][1]:.1f}" for r in RULES) + " |",
              "| Area (µm²) | " + " | ".join(f"{size[r][0] * size[r][1]:,.0f}" for r in RULES) + " |",
              "| DRC errors / LVS | " + " | ".join(f"{drc.get(r, '–')} / " + ("match" if (lvs.get(r) or {}).get("match")
                                                                              else "no match") for r in RULES) + " |"]
        if g5.get("u_budget_aware"):
            L.append("| Sum of wire-budget use (lower is better) | " + " | ".join(
                f"{sum(g5['u_' + r].values()):.1f}" for r in RULES) + " |")
        if g5.get("same_placement"):
            L += W.here("both costs chose the same placement, so this design cannot tell them apart.")
        L += W.how("blocks are numbered as in section 5" + ("; coloured boxes are the sub-circuits" if
                                                           pl["chosen"]["budget_aware"]["placement"].get("macros") else "")
                   + f". The budget-aware cost is A / A_ref + {P5.LAMBDA:g} × Σ max(0, u − 1) + {P5.MU:g} × Σ u (u: a "
                   "net's length over its budget); the area-only cost is A / A_ref. "
                   + (f"Sub-circuits are placed by seeded annealing ({M5.MOVES:,} moves, seed {M5.SEED}) or enumeration."
                      if pl["chosen"]["budget_aware"]["placement"].get("macros") else
                      "Every row arrangement, variant and flip is enumerated."))
        L += [""]
    # ---------------------------------------------------------------- post-layout
    if m7:
        mm = m7["metrics"]
        view = m7.get("post_layout_view", "pex_rc")
        L += ["## 7. After layout (S6, S7)", "",
              f"The layout read back with its wiring ({'capacitance and resistance' if view == 'pex_rc' else 'capacitance only'}) "
              "and simulated in the original benches.", "",
              "| Spec | Limit | Schematic | Drawn devices | After layout, budget-aware | Use of allowance | "
              "After layout, area-only | Use of allowance |", "|---|---|---|---|---|---|---|---|"]
        for k, x in mm["budget_aware"].items():
            name, unit = SPEC_NAME.get(k, (k, ""))
            y = mm["area_only"].get(k, {})
            b1 = "**" if not x["within_allowed"] else ""
            b2 = "**" if not y.get("within_allowed", True) else ""
            L.append(f"| {name} ({unit}) | {'≥' if x['kind'] == 'min' else '≤'} {f(x['limit'], 5)} | {f(x['schematic'], 5)} | "
                     f"{f(x['drawn'], 5)} | {f(x['post_layout_rc'], 5)} | {b1}{f(x['use_of_allowed'])}{b1} | "
                     f"{f(y.get('post_layout_rc'), 5)} | {b2}{f(y.get('use_of_allowed'))}{b2} |")
        met = all(x["meets_spec"] for x in mm["budget_aware"].values())
        over = [k for k, x in mm["budget_aware"].items() if not x["within_allowed"]]
        L += W.how("use of allowance = (schematic − after layout) / (η × margin); 1.0 is all the layout may take (bold: more).")
        L += W.here(("every spec is met after layout" if met else "a spec is missed after layout")
                    + ("; " + ", ".join(over) + " lose more than the allowance" if over else "; every spec within the allowance")
                    + ".")
        g75 = ((rep.get("S7") or {}).get("gates", {}).get("G7.5_mim_self_coupling_cancelled (info)") or {}).get("detail", {})
        if g75.get("budget_aware"):
            L += W.here("with the MIM capacitors' own plate coupling cancelled (very likely counted twice by the "
                        "extraction): " + ", ".join(f"{k} uses {f(z['use_of_allowed'])}" for k, z in g75["budget_aware"].items()) + ".")
        # wiring cost against the reference layout
        wl = {r: {"gbw": -100 * (mm[r]["gbw_mhz"]["post_layout_rc"] - mm[r]["gbw_mhz"]["drawn"]) / mm[r]["gbw_mhz"]["drawn"],
                  "pm": mm[r]["pm_deg"]["drawn"] - mm[r]["pm_deg"]["post_layout_rc"]}
              for r in RULES if "gbw_mhz" in mm[r] and "pm_deg" in mm[r]}
        if ref and ref.get("drawn_devices_only") and ref.get("post_layout"):
            dr, po = ref["drawn_devices_only"], ref["post_layout"]
            wl["hand"] = {"gbw": -100 * (po["gbw_mhz"] - dr["gbw_mhz"]) / dr["gbw_mhz"], "pm": dr["pm_deg"] - po["pm_deg"]}
        if wl:
            keys = [k for k in ("hand", "area_only", "budget_aware") if k in wl]
            bars(out_dir / "chart_wiring.png", [("GBW lost to the wiring", "%", [(k, wl[k]["gbw"]) for k in keys]),
                                                ("Phase margin lost to the wiring", "°", [(k, wl[k]["pm"]) for k in keys])])
            L += ["", W.img(f"{rel_fig}/chart_wiring.png", 720, "wiring loss"), ""]
            L += W.how("each layout simulated with its drawn devices only and again with its wiring, by the same "
                       "extraction and bench; the drop is what the wiring and placement cost. Shorter is better.")
        L += [""]
    # ---------------------------------------------------------------- reference layout
    if ref and ref.get("gds") and (REPO / ref["gds"]).exists():
        o = render(REPO / ref["gds"], out_dir / "layout_hand.png", w=300, h=300, ppu=3)
        L += ["## 8. The hand-drawn reference layout", "",
              f"`{ref['gds']}` (cell `{ref.get('cell')}`), extracted and simulated the same way (C-only). LVS against "
              f"this flow's schematic: {'match' if (ref.get('lvs_vs_layout_view') or {}).get('match') else 'no match (it is not exactly the same circuit; compare the wiring cost and area, not absolute numbers)'}.", ""]
        if o:
            L += [W.img(f"{rel_fig}/layout_hand.png", 520, "hand layout"), "",
                  f"Its top cell measures {o['w_um']:.1f} × {o['h_um']:.1f} µm ({o['w_um'] * o['h_um']:,.0f} µm², the "
                  "whole cell, including anything beside the circuit itself).", ""]
    # ---------------------------------------------------------------- failed checks, inputs
    L += ["## 9. What did not pass", ""]
    fails = [(st, g) for st in STAGE_DOES for g in (fs.get(st, {}).get("failed_gates") or [])]
    L += ([f"- **{st} {g.split('_')[0]}** ({W.GATE_MEANING.get(g.split('_')[0], '') or g.replace('_', ' ')})"
           for st, g in fails] or ["- nothing: every gate that ran passed."])
    L += ["", "Explanations of each gate: `docs/s4_s7_walkthrough.html` (S4–S7) and `docs/s0_s3_walkthrough.html` "
          "(S0–S3).", "", "## 10. The inputs used", "", "```yaml", pkg_text.strip(), "```", ""]
    if opts:
        L += ["```yaml", (REPO / "inputs" / d / "layout.yaml").read_text().strip(), "```", ""]
    L += ["## Glossary", ""] + [f"- **{a}:** {b}" for a, b in GLOSSARY] + [""]
    return L


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("design")
    ap.add_argument("--no-html", action="store_true")
    a = ap.parse_args(argv)
    out_md = REPO / "docs" / "reports" / f"{a.design}_report.md"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    W.IMG_PREFIX = os.path.relpath(REPO, out_md.parent).replace(os.sep, "/")
    out_md.write_text("\n".join(build(a.design)) + "\n")
    print(out_md)
    if not a.no_html:
        css = REPO / "docs" / "flow_record" / "record.css"
        cmd = ["pandoc", out_md.name, "--standalone", "--embed-resources", "--metadata",
               f"title=Layout report: {a.design}", "--toc", "-o", out_md.with_suffix(".html").name] + \
            (["-c", os.path.relpath(css, out_md.parent)] if css.exists() else [])
        r = subprocess.run(cmd, cwd=out_md.parent, capture_output=True, text=True)
        print(out_md.with_suffix(".html") if r.returncode == 0 else f"pandoc failed: {r.stderr[:400]}")
        return 0 if r.returncode == 0 else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
