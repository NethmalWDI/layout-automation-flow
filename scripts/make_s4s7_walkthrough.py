#!/usr/bin/env python3
"""Generate docs/s4_s7_walkthrough.md (and, with pandoc, a self-contained HTML copy): what S4, S5, S6 and S7 did on
each design and what came out, read only from the run's own output files. The companion of the reviewed
docs/s0_s3_walkthrough.md (scripts/make_s0s3_walkthrough.py), whose helpers and conventions it reuses: typed by hand
are the meaning of each gate, the explanation of each known finding and the "How to read it" notes; the "What it shows
here" lines and the summaries are built from the numbers.

usage (inside layout-s0s3, repo root): python3 scripts/make_s4s7_walkthrough.py [design ...] [--no-html] [--out FILE.md]
default designs: example_ota_5t loadbench_miller
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_s0s3_walkthrough as W  # noqa: E402

REPO = W.REPO
OUT_MD = REPO / "docs" / "s4_s7_walkthrough.md"
STAGES = ("S4", "S5", "S6", "S7")
RULES = ("budget_aware", "area_only")

GATE_MEANING = {
    "G4.1": "every block holds one device type with one body net, and every device is in exactly one block",
    "G4.2": "every block variant passes Magic DRC with nothing deferred (its ring meets the tap rules)",
    "G4.3": "every block variant passes Netgen LVS against the IR's devices (negative control caught)",
    "G4.4": "every matched pair or mirror has a signed-off variant that is a mirror image about its centre",
    "G4.5": "no diffusion is farther from a tap than S2's latch-up distance (ring and tap strips)",
    "G4.6": "block port capacitance (reported; comes with S6)",
    "G5.1": "the placements are legal: blocks apart, PMOS above NMOS, symmetric blocks on the axis, unrouted DRC clean",
    "G5.2": "the routed top cell passes Magic DRC (negative control caught)",
    "G5.3": "the routed top cell passes LVS against S0's layout view with the drawn finger counts (control caught)",
    "G5.4": "the routes meet S2's route rules: length, parallel runs, series R against what S3 left, symmetry",
    "G5.5": "budget-aware against the area-only baseline (reported)",
    "G6.1": "both layouts extracted (C-only and R+C) and the flat extraction LVS-matched",
    "G6.2": "every budgeted net capacitance, coupling and terminal R of the budget-aware layout within S2's budget",
    "G6.3": "kpex 2.5D against Magic (reported)",
    "G6.4": "Magic's C-only netlist against its own .ext (reported)",
    "G6.5": "a MIM capacitor's plate-to-plate coupling extracted alone (reported)",
    "G7.1": "every spec met post-layout (R+C), with no failed simulation",
    "G7.2": "each spec loses at most eta × margin from schematic to post-layout",
    "G7.3": "S2's G2.0 prediction against the actual loss (reported)",
    "G7.4": "PVT points post-layout (reported: not simulated here)",
    "G7.5": "post-layout AC with the MIM capacitor's own plate coupling cancelled (reported)",
    "H4": "hypothesis: parasitics within their budgets (G6.2) keep every spec within eta × margin (G7.1, G7.2)",
    "H5": "hypothesis: the budget-aware placement loses less than the area-only one (reported per spec)",
}
STAGE_DOES = {
    "S4": "Blocks: groups S3's ringless cells into blocks (matching groups first; one device type and one body per "
          "block), draws the variants (A, AB mirror image, ABBA common centroid, ABAB interdigitated, or a row), closes "
          "each with one tap ring (tap strips where a row is too wide), draws a bound MIM capacitor as its own block, "
          "and signs every variant off with DRC and LVS.",
    "S5": "Placement and routing: enumerates every row partition (PMOS above NMOS, in the designer's row order), "
          "variant and flip, scores each twice (budget-aware: area plus S2's wire budgets; area-only: the AICL-like "
          "baseline), routes both winners with one metal-4 spine per net, and signs them off (DRC, LVS, S2's route "
          "rules).",
    "S6": "Extraction: Magic extracts each routed layout capacitance-only and R+C, LVS-checks the extraction, and "
          "compares every budgeted parasitic of S2 with what was extracted.",
    "S7": "Post-layout SPICE: the schematic, the drawn devices, the C-only and the R+C netlists in S0's own benches; "
          "each spec's loss against eta × margin.",
}
# Known findings, typed by hand: (design, gate) -> explanation.
KNOWN = {
    ("loadbench_miller", "G5.4"): "outFirstStage joins the input pair, the mirror, N3's gate and the Miller capacitor, and "
        "S2 allows it 16.3 µm of metal3; no row placement of these blocks gets it under 1.65 × that. The input pair's "
        "series-R budget was already used by S3's cells (the known G3.5 relaxation), so no wire fits in it.",
    ("loadbench_miller", "G6.2"): "the largest excesses sit at the Miller capacitor: its own fringe and bottom-plate "
        "capacitance land on out and outFirstStage, and S2's budgets were set without them (G6.5 shows the part that "
        "is very likely counted twice). The input pair's terminal R is over because S3's cells already used it.",
    ("loadbench_miller", "G7.2"): "GBW loses more than eta × its 2.34 MHz margin. GBW is about gm1 / Cc, and the "
        "out~outFirstStage coupling sits beside the 0.5 pF Miller capacitor; most of it is the capacitor's own "
        "plate-to-plate coupling as Magic extracts it, very likely counted twice (G6.5). With that coupling "
        "cancelled (G7.5) every spec stays within eta × margin; every spec is met either way (G7.1).",
}


def gate_rows(gates: dict) -> list:
    rows = ["| Gate | Result | What it checks |", "|---|---|---|"]
    for g, v in gates.items():
        p = v.get("pass")
        res = "PASS" if p is True else ("**FAIL**" if p is False else "info")
        rows.append(f"| {g.replace('_', ' ')} | {res} | {GATE_MEANING.get(g.split('_')[0].split(' ')[0], '')} |")
    return rows


def _load(stage, d, name):
    return W._j(REPO / "outputs" / stage / d / name)


def s4_section(d: str, rep: dict) -> list:
    bj = _load("S4", d, "blocks.json") or {}
    L = ["| Block | Devices | Variant | Area (µm²) | Worst tap distance (µm) | Tap strips | DRC errors | LVS | Mirror image |",
         "|---|---|---|---|---|---|---|---|---|"]
    for b in bj.get("blocks", []):
        for v in b["variants"]:
            g, sym = v.get("geometry") or {}, v.get("symmetry") or {}
            L.append(f"| {b['name']} | {', '.join(x.replace('XNormalTransistor', '').replace('XDiodeTransistor', '') for x in b['devices'])} | "
                     f"{v['id']} | {W.f(g.get('area_um2'), 4)} | {W.f(g.get('tap_distance_max_um'))} | {len(g.get('strips') or [])} | "
                     f"{(v.get('drc') or {}).get('errors')} | {W.f((v.get('lvs') or {}).get('match'))} | "
                     f"{W.f(sym.get('mirror_image')) if sym else '–'} |")
    L += W.how("one row per drawn variant of each block. The tap distance is how far the farthest diffusion stands from "
               "its ring or a tap strip; S2's latch-up rule allows "
               f"{W.f(rep['gates'].get('G4.5_latchup_tap_distance', {}).get('limit_um'))} µm. A mirror image means every "
               "unit faces a flipped copy across the centre (AB, ABBA); ABAB is interdigitated, not a mirror image.")
    strips = rep["gates"].get("G4.5_latchup_tap_distance", {}).get("tap_strips") or {}
    caps = [b for b in bj.get("blocks", []) if b.get("kind") == "mim_cap"]
    n = sum(len(b["variants"]) for b in bj.get("blocks", []))
    txt = f"{len(bj.get('blocks', []))} blocks, {n} variants, " + \
        ("all signed off" if all(v.get("ok") for b in bj.get("blocks", []) for v in b["variants"]) else "not all signed off")
    txt += (f"; {W.and_list(list(strips))} needed a tap strip" if strips else "; no block needed a tap strip")
    if caps:
        bd = caps[0]["binding"]
        txt += (f"; {caps[0]['name']} is drawn as {bd['model']} ({W.f(bd['params'].get('W'))} × {W.f(bd['params'].get('L'))} µm, "
                f"{bd.get('status')}), top plate on {bd['top']}, bottom plate on {bd['bottom']}")
    L += W.here(txt + ".")
    pics = []
    for b in bj.get("blocks", []):
        v = b["variants"][0]
        if v.get("png"):
            pics.append(W.img(v["png"], 240, v["cell"]))
    if pics:
        L += ["", " ".join(pics)]
        L += W.how("the first variant of each block as drawn: the units in a row, metal-2 stubs to one metal-3 track per "
                   "net above and below, and the ring around everything (n-well for PMOS).")
    return L


def s5_section(d: str, rep: dict) -> list:
    pj = _load("S5", d, "placement.json") or {}
    ch = pj.get("chosen") or {}
    nets = sorted(set().union(*(set(c["cost"]["u"]) for c in ch.values()))) if ch else []
    L = [f"{pj.get('n_candidates')} candidate placements were scored.", "",
         "| | " + " | ".join(r.replace("_", "-") for r in RULES) + " |", "|---|" + "---|" * len(RULES)]
    L.append("| Rows (top to bottom) | " + " | ".join(" / ".join(", ".join(row) for row in ch[r]["placement"]["rows"])
                                                     for r in RULES) + " |")
    L.append("| Variants (flipped) | " + " | ".join(", ".join(f"{b} {x['variant']}{' (flipped)' if x['flip'] else ''}"
                                                            for b, x in ch[r]["placement"]["blocks"].items()) for r in RULES) + " |")
    L.append("| Area (µm²) | " + " | ".join(W.f(ch[r]["cost"]["area_um2"], 5) for r in RULES) + " |")
    lr = (rep["gates"].get("G5.4_route_rules") or {}).get("detail") or {}
    for n in nets:
        cells = []
        for r in RULES:
            routed = ((lr.get(r) or {}).get("max_length") or {})
            rn = next((x for k, x in routed.items() if k.lower() == n.lower()), None)
            cells.append(f"{W.f(ch[r]['cost']['u'].get(n))} → {W.f(rn['use']) if rn else '–'}")
        L.append(f"| {n}: wire-budget use, estimate → routed | " + " | ".join(cells) + " |")
    L += W.how("each column is the winner of one cost. A net's wire-budget use is its length over S2's maximum length "
               "for it (1.0 = the limit): first the placer's half-perimeter estimate, then the routed spine and runs. "
               "The budget-aware cost adds 10 × any excess and the uses themselves to the area; the area-only cost is "
               "the area alone.")
    g5 = rep["gates"].get("G5.5_area_vs_area_only (info)") or {}
    if g5.get("same_placement"):
        txt = "both costs chose the same placement, so this design cannot tell them apart (H5 not testable)"
    else:
        ba, ao = ch["budget_aware"]["cost"]["u"], ch["area_only"]["cost"]["u"]
        less = [n for n in ba if ba[n] < ao[n] - 1e-9]
        txt = (f"at {W.f(g5.get('area_ratio'))} × the area-only area, the budget-aware placement uses less of the budget "
               f"on {W.and_list(less) if less else 'no net'}")
    over = [n for n, x in ((lr.get("budget_aware") or {}).get("max_length") or {}).items() if not x.get("ok")]
    txt += ("; after routing, " + (f"{W.and_list(over)} still exceed{'s' if len(over) == 1 else ''} its budget"
                                   if over else "every net is within its length budget"))
    L += W.here(txt + ".")
    pics = [W.img(f"outputs/S5/{d}/routed_{r}/{d}_routed.png", 300, r) for r in RULES
            if (REPO / f"outputs/S5/{d}/routed_{r}/{d}_routed.png").exists()]
    if pics:
        L += ["", " ".join(pics)]
        L += W.how("the routed layouts, budget-aware first. PMOS blocks are above NMOS; the vertical purple lines are the "
                   "metal-4 spines, one per net, joined to the blocks' metal-3 tracks by vias.")
    return L


def s6_section(d: str, rep: dict) -> list:
    pj = _load("S6", d, "parasitics_vs_budgets.json") or {}
    lay = pj.get("layouts") or {}
    same = (lay.get("area_only") or {}).get("same_as")
    rows = {r: {x["id"]: x for x in lay[r]["budgets"]["rows"]} for r in RULES if r in lay}
    L = ["| Element | Kind | Budget | Budget-aware | Use | " + ("" if same else "Area-only | Use |"),
         "|---|---|---|---|---|" + ("" if same else "---|---|")]
    for k, x in rows["budget_aware"].items():
        line = (f"| {k} | {x['kind'].replace('_', ' ')} | {W.f(x['budget'], 4)} {x.get('units') or ''} | {W.f(x['value'], 4)} | "
                f"{'**' if not x['ok'] else ''}{W.f(x['use'])}{'**' if not x['ok'] else ''} |")
        if not same:
            y = rows["area_only"].get(k) or {}
            line += f" {W.f(y.get('value'), 4)} | {W.f(y.get('use'))} |"
        L.append(line)
    L += W.how("every parasitic S2 budgeted, as extracted from the routed layout: net capacitance to an AC ground, "
               "coupling between two signal nets (fF), and terminal resistance (Ω, S3's cell plus S5's wires and vias). "
               "Use is extracted / budget; bold marks an element over its budget.")
    v = rep["gates"]["G6.2_parasitics_within_budgets"]
    txt = (f"{len(v.get('violations') or [])} of {len(rows['budget_aware'])} elements are over budget"
           + (f", the worst {v['worst'][0][1]} at {W.f(v['worst'][0][0])} ×" if v.get("worst") else ""))
    c4 = ((rep["gates"].get("G6.4_c_only_netlist_complete (info)") or {}).get("detail") or {}).get("budget_aware") or {}
    if c4:
        txt += (f"; Magic's C-only netlist holds {W.f(100 * (c4.get('netlist_short_of_ext') or 0), 2)} % less capacitance "
                "than its .ext (G6.4)" + (f", none on {W.and_list(c4['nets_without_ground_C_in_netlist'])} to ground"
                                          if c4.get("nets_without_ground_C_in_netlist") else ""))
    for c, m in (pj.get("mim_self") or {}).items():
        txt += (f"; the {c} block alone carries {W.f(m['plate_coupling_fF'], 3)} fF between its plates (very likely "
                f"counted twice, G6.5) and {W.f(m['bottom_to_substrate_fF'], 3)} fF from its bottom plate to the substrate")
    if same:
        txt += "; both costs chose one layout, so it is extracted once"
    L += W.here(txt + ".")
    return L


def s7_section(d: str, rep: dict) -> list:
    m = _load("S7", d, "metrics.json") or {}
    ba = (m.get("metrics") or {}).get("budget_aware") or {}
    ao = (m.get("metrics") or {}).get("area_only") or {}
    mm = ((rep["gates"].get("G7.5_mim_self_coupling_cancelled (info)") or {}).get("detail") or {}).get("budget_aware") or {}
    L = ["| Spec | Limit | Schematic | Drawn devices | C-only | R+C | Loss / (eta × margin) | Area-only R+C (use) |"
         + (" R+C, MIM self-coupling cancelled (use) |" if mm else ""),
         "|---|---|---|---|---|---|---|---|" + ("---|" if mm else "")]
    for k, x in ba.items():
        unit = W.SPEC_UNITS.get(k.rsplit("_", 1)[-1], "")
        y = ao.get(k) or {}
        z = mm.get(k)
        L.append(f"| {k.rsplit('_', 1)[0]} ({unit}) | {'≥' if x['kind'] == 'min' else '≤'} {W.f(x['limit'], 5)} | "
                 f"{W.f(x['schematic'], 5)} | {W.f(x['drawn'], 5)} | {W.f(x['pex_c'], 5)} | {W.f(x['post_layout_rc'], 5)} | "
                 f"{'**' if not x['within_allowed'] else ''}{W.f(x['use_of_allowed'])}{'**' if not x['within_allowed'] else ''} | "
                 f"{W.f(y.get('post_layout_rc'), 5)} ({W.f(y.get('use_of_allowed'))}) |"
                 + (f" {W.f(z['value'], 5)} ({W.f(z['use_of_allowed'])}) |" if z else (" – |" if mm else "")))
    L += W.how("the same benches as S0, with the circuit replaced by each view of the layout: drawn devices only, then "
               "every capacitance, then capacitance and wire resistance (the post-layout result). The loss is how much of "
               "the margin the layout takes; 1.0 is all that eta allows (bold: more).")
    g = rep["gates"]
    worst = max(ba.items(), key=lambda kv: kv[1]["use_of_allowed"] or 0) if ba else None
    txt = ("every spec is met post-layout" if g["G7.1_specs_met_post_layout"]["pass"] else "a spec is missed post-layout")
    if worst:
        txt += (f"; the largest loss is {worst[0]} at {W.f(worst[1]['use_of_allowed'])} of eta × margin"
                + (" (over)" if not worst[1]["within_allowed"] else ""))
    h4 = g.get("H4 (info)") or {}
    txt += (f"; H4: G6.2 {'passed' if h4.get('G6.2') else 'failed'} and G7.1/G7.2 "
            f"{'passed' if h4.get('G7.1_and_G7.2') else 'did not both pass'}")
    if mm:
        txt += ("; with the capacitor's own plate coupling cancelled, " +
                ", ".join(f"{k} uses {W.f(z['use_of_allowed'])}" for k, z in mm.items()))
    L += W.here(txt + ".")
    return L


def design_section(d: str) -> list:
    fs = W._j(REPO / "outputs/flow" / d / "flow_summary.json") or {}
    stages = fs.get("stages", {})
    L = [f"## {d}", "", f"Run: `./flow run {d} --from S4`. Status, run time and the steps of each stage:", "",
         "| Stage | Status | Started | Run time | Steps |", "|---|---|---|---|---|"]
    for st in STAGES:
        s = stages.get(st, {})
        secs = sum(x.get("seconds") or 0 for x in s.get("steps", []))
        L.append(f"| {st} | **{s.get('status', '–')}** | {s.get('started', '–')} | {secs / 60:.1f} min | "
                 f"{', '.join(x.get('step', '') for x in s.get('steps', []))} |")
    builders = {"S4": s4_section, "S5": s5_section, "S6": s6_section, "S7": s7_section}
    findings, body = [], []
    for st in STAGES:
        rep = _load(st, d, f"{st.lower()}_report.json")
        if rep is None:
            body += [f"### {st}", "", "*No report: the stage has not run.*", ""]
            continue
        for gname, v in rep["gates"].items():
            if v.get("pass") is False:
                key = gname.split("_")[0]
                findings.append(f"- **{st} {key}** ({GATE_MEANING.get(key, '')}): "
                                + KNOWN.get((d, key), "not explained yet; see the stage's report."))
        body += [f"### {st}", "", STAGE_DOES[st], "", f"Outputs: `outputs/{st}/{d}/` (report: `{st.lower()}_report.json`).", ""]
        body += gate_rows(rep["gates"]) + [""] + builders[st](d, rep) + [""]
    L += ["", "**Known findings** (failed gates and why; none is a crash):", ""] + (findings or ["- none: every gate passes."]) + [""]
    return L + body


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("designs", nargs="*", default=["example_ota_5t", "loadbench_miller"])
    ap.add_argument("--no-html", action="store_true")
    ap.add_argument("--out", default=str(OUT_MD), help="Markdown file to write (the HTML goes next to it)")
    a = ap.parse_args(argv)
    out_md = Path(a.out).resolve()
    out_md.parent.mkdir(parents=True, exist_ok=True)
    W.IMG_PREFIX = os.path.relpath(REPO, out_md.parent).replace(os.sep, "/")
    head = (subprocess.run(["git", "--no-optional-locks", "log", "-1", "--format=%h %cs"], cwd=REPO, capture_output=True,
                           text=True).stdout.strip() or "unknown")
    L = ["# S4–S7 walkthrough: blocks, placement, routing, extraction and post-layout SPICE", "",
         f"Generated by `python3 scripts/make_s4s7_walkthrough.py` from the run's own output files (repo at {head}). "
         "Every number below is read from `outputs/`. Typed by hand: the meaning of each gate, the explanation of each "
         "known finding, and the *How to read it* notes. The companion page `docs/s0_s3_walkthrough.html` covers "
         "S0–S3 (its reading guide applies here too); the plan is `docs/plan_v4_S4_S7.md`, the record "
         "`docs/flow_record.md` sections 7.15–7.20.", "", "**The four stages:**", ""]
    L += [f"- **{st}**: {txt}" for st, txt in STAGE_DOES.items()]
    L += ["", "**Status per design:**", "", "| Design | S4 | S5 | S6 | S7 |", "|---|---|---|---|---|"]
    for d in a.designs:
        st = (W._j(REPO / "outputs/flow" / d / "flow_summary.json") or {}).get("stages", {})
        L.append(f"| {d} | " + " | ".join(st.get(s, {}).get("status", "–") for s in STAGES) + " |")
    L += ["", "**Two more ideas this page uses** (the rest are in the S0–S3 page's reading guide):", "",
          "- **Budget-aware and area-only.** S5 scores every placement twice: by area plus S2's wire budgets (the flow's "
          "own rule) and by area alone (the baseline of the AICL paper). Both winners are routed by the same router, "
          "so the two layouts differ only in the placement; that comparison is hypothesis H5.",
          "- **H4.** If every parasitic stays within its S2 budget (G6.2), the layout should keep every spec within "
          "eta × margin (G7.1, G7.2).", ""]
    for d in a.designs:
        L += design_section(d)
    out_md.write_text("\n".join(L) + "\n")
    print(out_md)
    if not a.no_html:
        html = out_md.with_suffix(".html")
        css = REPO / "docs" / "flow_record" / "record.css"
        cmd = ["pandoc", out_md.name, "--standalone", "--embed-resources", "--metadata", "title=S4–S7 walkthrough",
               "-o", html.name] + (["-c", os.path.relpath(css, out_md.parent)] if css.exists() else [])
        r = subprocess.run(cmd, cwd=out_md.parent, capture_output=True, text=True)
        print(html if r.returncode == 0 else f"pandoc failed: {r.stderr[:400]}")
        if r.returncode != 0:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
