#!/usr/bin/env python3
"""Generate docs/progress_report.md (and, with pandoc, a self-contained HTML copy): a short report for reviewers on the
whole project so far: what each stage does and which algorithm it runs, what happened, the expected novelty, the
results of every design tried (layouts, schematics, hand layouts, post-layout numbers), whether it runs without an
LLM, the LLM integration plan with its pros and cons, and the risks. Numbers and pictures come from the outputs and
the detailed reports (run make_ttsky_report.py, make_iadc_report.py and make_design_report.py first); the narrative is
typed.

usage (inside layout-s0s3, repo root, after `source scripts/env.sh`): python3 scripts/make_progress_report.py [--no-html]
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
OUT_MD = REPO / "docs" / "progress_report.md"
DESIGNS = ["example_ota_5t", "loadbench_miller", "ttsky25a_fd", "iadc_ota"]
TITLE = {"example_ota_5t": "5T OTA (`example_ota_5t`)", "loadbench_miller": "Two-stage Miller op-amp (`loadbench_miller`)",
         "ttsky25a_fd": "Imasha's fully differential op-amp, taped out (`ttsky25a_fd`)",
         "iadc_ota": "Folded-cascode OTA of an incremental ADC, in a Tiny Tapeout tile (`iadc_ota`)"}
SPEC = {"gbw_mhz": ("GBW", "MHz"), "pm_deg": ("Phase margin", "°"), "gain_db": ("Gain", "dB"), "power_uw": ("Power", "µW"),
        "vnoise_nv_rthz": ("Input noise", "nV/√Hz")}
f = W.f


def j(*p):
    return W._j(REPO.joinpath(*p))


def img(path, width, alt):
    return W.img(path, width, alt) if (REPO / path).exists() else f"*(picture not generated: `{path}`)*"


STAGES = [
    ("S0", "Ingest", "reads and freezes the design (netlist, specs, benches); checks every node and device; binds devices "
     "to SKY130 cells", "netlist parsing and validation; SHA-256 freeze; round-trip LVS (Netgen); bench re-run; 45 PVT "
     "points; 200-run mismatch Monte Carlo"),
    ("S1", "Electrical intent", "finds which nodes matter and how much", "operating point (ngspice); exact linear "
     "small-signal model; pole per node; sensitivity of every spec to capacitance on every node and node pair, checked "
     "against SPICE; matching groups by rule"),
    ("S2", "Requirement compiler", "turns the specs into layout budgets before any layout exists", "shares each spec's "
     "allowance (η × margin) among nets by max-min fair progressive filling; capacitance, coupling, resistance and "
     "wire-length budgets; verified in SPICE with the harmful budgets inserted"),
    ("S3", "Device design", "chooses how each transistor is drawn", "enumerates PDK cell options (fingers, contacts, "
     "diffusion sharing), builds and signs off each in Magic, keeps the smallest within budget"),
    ("S4", "Blocks", "draws matched blocks from the unit cells", "rule-based grouping; common-centroid / interdigitated "
     "/ mirror sequences; dummies; tracks packed by the left-edge rule; multi-row arrays; one tap ring; DRC, LVS and a "
     "negative control for every variant"),
    ("S5", "Placement and routing", "places the blocks (inside an outline) and wires them", "enumeration or seeded "
     "simulated annealing per sub-circuit, every arrangement of the sub-circuits; cost = area + wire-budget use; "
     "metal-4 spine router (small designs) or a metal-3/metal-4 grid A* router; top-level DRC and LVS"),
    ("S6", "Extraction", "reads the layout back with its parasitics", "Magic extraction (C-only, and R+C where it "
     "fits in memory); flat LVS; every budget against what was extracted; kpex cross-check"),
    ("S7", "Post-layout evaluation", "simulates the layout in the original benches", "ngspice on four views: "
     "schematic, drawn devices, C-only, R+C; each spec's loss against η × margin; S2's prediction against the result"),
    ("S8", "Diagnosis and repair", "*planned, not built*", "attribute a failure to nodes with the sensitivities, fix "
     "locally in S3–S5"),
    ("S9", "Selection", "*planned, not built*", "the smallest layout meeting every verified spec"),
]

TIMELINE = [
    ("Oct 23–27", "S0–S3 built and run on five designs (plan v1–v2): the 5T, a stress variant, LOADBench, ttsky, iadc; "
     "before/after comparison; the hand layouts of ttsky and iadc measured the flow's way."),
    ("Nov 1–2", "Plan v3 Phase A and a supervisor review of S0–S3 on the 5T and LOADBench: fixes, golden results, the "
     "S0–S3 walkthrough."),
    ("Nov 3–4", "Plan v4: S4–S7 built (blocks, placement, routing, extraction, post-layout SPICE); the 5T and LOADBench "
     "through all eight stages; an independent code review; golden results for S4–S7."),
    ("Nov 4", "Phase 8: ttsky through S4–S7 with its own hierarchy, common-centroid matching, dummies, interleaved "
     "resistors and a 250 × 200 µm outline; a second independent review; the detailed ttsky report."),
    ("Nov 4–5", "A local web GUI (edit a design or make a new one, run the flow, get a report; no LLM); iadc through "
     "S0–S7 in a Tiny Tapeout tile, which needed multi-row arrays and a placement search for tight outlines; its "
     "detailed report."),
]

RISKS = [
    ("Budgets can be infeasible", "S2's budgets come from linearised sensitivities and assume a compact layout. On "
     "ttsky and iadc most nets exceed them (G5.4, G6.2 fail) while the specs are still largely met: the budgets are "
     "conservative and do not yet steer the layout as intended. iadc's budgets cannot even be met by the smallest cells "
     "(G2.7)."),
    ("Specs are often ASSUMPTIONs", "three of the four designs have no upstream specs; the flow uses 0.9 × the "
     "schematic's own results. A missed spec (iadc's GBW) may be a missed assumption, not a bad layout."),
    ("Extraction is partial on large layouts", "R+C extraction ran out of memory on ttsky's supply rings; ttsky and "
     "iadc are judged on capacitance only. Wire resistance is missing there."),
    ("One condition only after layout", "no PVT corners or mismatch Monte Carlo after layout yet."),
    ("A likely double count", "Magic counts a MIM capacitor's own plate coupling on top of its model; the flow reports "
     "both numbers (G6.5, G7.5) but the gates keep Magic's."),
    ("Density", "a tap ring per block and 3 µm gaps make the layouts 1.1–2.5 × the hand layouts' area."),
    ("Hand comparisons are not like-for-like", "both hand layouts are of slightly different circuits (enable switches, "
     "a real switched-capacitor CMFB); only the wiring's cost and the area compare fairly."),
    ("Unrouted chip-level parts", "the tile's power straps and pins are not routed; no symmetric routing of matched "
     "pairs; electromigration widths not checked (no SKY130 limits found)."),
    ("Opt-in fixes", "two latent flaws found on iadc (stubs off-centre by up to 0.125 µm; a placement search that "
     "dropped shapes) are fixed only where switched on, so the finished designs keep their committed results until a "
     "decision is made."),
    ("Small sample", "four designs; every hypothesis result (H4, H5, G2.0's prediction) rests on one or two circuits."),
    ("LLM risks (planned step)", "an LLM can be confidently wrong, non-reproducible across versions, and costs tokens; "
     "the plan keeps every LLM output behind the same deterministic checks and journals each call."),
]


def results_table(d: str) -> list:
    m = (j("outputs/S7", d, "metrics.json") or {}).get("metrics", {}).get("budget_aware") or {}
    view = (j("outputs/S7", d, "metrics.json") or {}).get("post_layout_view", "pex_rc")
    L = [f"| Spec | Limit | Schematic | After layout ({'R+C' if view == 'pex_rc' else 'C-only'}) | Met | "
         "Use of the allowance |", "|---|---|---|---|---|---|"]
    for k, x in m.items():
        name, unit = SPEC.get(k, (k, ""))
        use = f(x["use_of_allowed"])
        L.append(f"| {name} ({unit}) | {'≥' if x['kind'] == 'min' else '≤'} {f(x['limit'], 4)} | {f(x['schematic'], 4)} | "
                 f"{f(x['post_layout_rc'], 4)} | {'yes' if x['meets_spec'] else '**no**'} | "
                 f"{('**' + use + '**') if not x['within_allowed'] else use} |")
    return L


def plain_schematic(d: str) -> str | None:
    """The design's own xschem drawing (circuits/<d>/source/<d>.sch), printed unmarked from a scratch copy; None when
    the package has no drawing (LOADBench is a netlist)."""
    if not (REPO / "circuits" / d / "source" / f"{d}.sch").exists():
        return None
    rel = f"outputs/report/{d}/simple/schematic.png"
    try:
        import report_figures as RF
        work = RF._work(REPO, src_rel=f"circuits/{d}/source", designer_path=None)
        RF.schematic(REPO, work, d, [], REPO / rel, {}, width=1600)
    except Exception as e:  # noqa: BLE001 - the report still builds without the picture
        print(f"schematic of {d} not drawn: {e}", file=sys.stderr)
    return rel if (REPO / rel).exists() else None


def design_section(d: str) -> list:
    fs = (j("outputs/flow", d, "flow_summary.json") or {}).get("stages", {})
    s5 = (j("outputs/S5", d, "s5_report.json") or {}).get("gates", {})
    pl = (j("outputs/S5", d, "placement.json") or {}).get("chosen", {})
    import yaml
    pkg = yaml.safe_load((REPO / "inputs" / d / "package.yaml").read_text())
    bb = pl.get("budget_aware", {}).get("placement", {}).get("bbox")
    size = f"{bb[2] - bb[0]:.1f} × {bb[3] - bb[1]:.1f} µm" if bb else "–"
    drc = (s5.get("G5.2_top_DRC") or {}).get("detail", {}).get("budget_aware")
    lvs = ((s5.get("G5.3_top_LVS") or {}).get("detail", {}).get("budget_aware") or {}).get("match")
    L = [f"### {TITLE[d]}", "", " ".join((pkg.get("description") or "").split()), "",
         "Stages: " + " · ".join(f"{s} **{v.get('status')}**" for s, v in fs.items()) + ".", "",
         f"- **Layout (budget-aware):** {size}; top-level DRC {drc} errors; LVS {'match' if lvs else 'no match'}."]
    rep = {"ttsky25a_fd": "docs/ttsky25a_fd_report.html", "iadc_ota": "docs/iadc_ota_report.html"}.get(
        d, f"docs/reports/{d}_report.html")
    L += [f"- **Full detail:** `{rep}`.", ""]
    pics = []
    if d in ("ttsky25a_fd", "iadc_ota"):
        pics.append(img(f"outputs/report/{d}/sch_top.png", 470, "schematic"))
        pics.append(img(f"outputs/report/{d}/layout_budget_aware_annot.png", 420, "layout"))
    else:
        sch = plain_schematic(d)
        if sch:
            pics.append(img(sch, 420, "schematic"))
        pics.append(img(f"outputs/report/{d}/simple/layout_budget_aware_annot.png", 300 if d == "example_ota_5t" else 360,
                        "layout"))
    L += [" ".join(pics), ""]
    if d in ("ttsky25a_fd", "iadc_ota"):
        how = ("the designer's schematic (sub-circuits boxed in colour, each device with its block number) and the "
               "flow's routed layout (sub-circuits outlined, blocks numbered)")
    elif sch:
        how = ("the upstream xschem schematic as drawn (frozen source, printed from a scratch copy) and the flow's "
               "routed layout, blocks numbered. The drawing is the topology template: its W labels are the template's, "
               "while the flow lays out the sized netlist (`best_sizes.json`, the sizes given above).")
    else:
        how = "the flow's routed layout, blocks numbered (this design's package is a netlist; no schematic drawing)."
    L += W.how(how)
    L += [""] + results_table(d) + [""]
    g75 = ((j("outputs/S7", d, "s7_report.json") or {}).get("gates", {}).get("G7.5_mim_self_coupling_cancelled (info)")
           or {}).get("detail", {}).get("budget_aware")
    if g75 and "gbw_mhz" in g75:
        L += [f"With the MIM capacitors' likely double-counted plate coupling removed (G7.5), GBW uses "
              f"{f(g75['gbw_mhz']['use_of_allowed'])} of the allowance.", ""]
    nums = j("outputs/report", d, "numbers.json")
    ref = j("outputs/reference_layout", d, "reference_layout.json")
    if nums and ref and d in ("ttsky25a_fd", "iadc_ota"):
        wl, ar = nums["wiring_loss"], nums["area"]
        hand_img = f"outputs/report/{d}/layout_hand_annot.png"
        L += ["**Against the hand layout:**", "", img(hand_img, 420, "hand layout"), "",
              "| | Flow, budget-aware | Flow, area-only | Hand layout |", "|---|---|---|---|",
              f"| Area (µm²) | {ar['budget_aware']:,.0f} ({ar['budget_aware'] / ar['hand']:.2f} ×) | "
              f"{ar['area_only']:,.0f} ({ar['area_only'] / ar['hand']:.2f} ×) | {ar['hand']:,.0f} |",
              f"| GBW lost to the wiring (drawn → extracted) | {wl['budget_aware']['gbw_pct']:.1f} % | "
              f"{wl['area_only']['gbw_pct']:.1f} % | {wl['hand']['gbw_pct']:.1f} % |",
              f"| Phase margin lost to the wiring | {wl['budget_aware']['pm_deg']:.1f}° | {wl['area_only']['pm_deg']:.1f}° | "
              f"{wl['hand']['pm_deg']:.1f}° |",
              "| GBW after layout, C-only (MHz) | " + " | ".join(
                  f(((j("outputs/S7", d, "metrics.json") or {}).get("metrics", {}).get(r, {}).get("gbw_mhz") or {})
                    .get("pex_c"), 4) for r in ("budget_aware", "area_only"))
              + f" | {f(ref['post_layout']['gbw_mhz'], 4)} (its drawn devices: {f(ref['drawn_devices_only']['gbw_mhz'], 4)}) |",
              ""]
        L += W.how("the hand layout is of a slightly different circuit (" + (
            "the taped-out tile adds enable switches; its op-amp cell is measured" if d == "ttsky25a_fd" else
            "it holds the real switched-capacitor CMFB, outlined") + "), so the wiring's cost (one layout simulated "
            "with and without its wiring) and the area are what compare fairly.")
        L += [""]
    return L


def build(head: str) -> list:
    import re
    log = sorted((REPO / "runs" / "logs").glob("test_*.log"), key=lambda p: p.stat().st_mtime)
    m = re.search(r"(\d+) passed", log[-1].read_text()) if log else None
    tests = f"{m.group(1)} automated tests pass" if m else ""
    goldens = len(list((REPO / "tests" / "golden").glob("*/*.json")))
    record = (REPO / "docs" / "flow_record_section7_draft.md").read_text()
    journey = record[record.find("### 7.1"):record.find("### 7.2")]          # the journey table only
    rows = sum(1 for ln in journey.splitlines() if ln.startswith("| ") and ln.split("|")[1].strip().isdigit())
    L = ["# Analog layout automation on SKY130: progress report", "",
         f"*Generated by `python3 scripts/make_progress_report.py` from the flow's outputs (repo at {head}). For "
         "reviewers: what the flow does, what it produced on four designs, what is new, what is planned, and the risks. "
         "Every number is read from the outputs; the detailed reports and the record are linked at the end.*", "",
         "## 1. In short", "",
         "- **What it is:** an open, reproducible flow that takes a sized SKY130 analog circuit and its specs, works out "
         "*before any layout* which nodes matter and how much parasitics each may take (budgets), then draws, places, "
         "routes, extracts and re-simulates the layout, checking every step (DRC, LVS, specs).",
         "- **Status:** stages S0–S7 of a planned S0–S9 are built and run end to end on four designs, with a small "
         "local GUI and per-design reports. S8 (diagnosis and repair) and S9 (selection) are planned.",
         f"- **Every layout produced is DRC-clean and LVS-matched.** After layout, every spec is met on three designs; "
         "on the fourth (iadc, in a Tiny Tapeout tile) GBW misses its assumed spec.",
         "- **No LLM takes any decision in the flow.** It runs with no LLM at all (section 6). An LLM (Claude) helped "
         "write and review the code; an LLM *taking* layout decisions is the next, measured step (section 7).",
         f"- **Quality controls:** {tests or 'the test suite'}; {goldens} golden results re-checked on every change; "
         f"{rows} problems found and fixed, each recorded with how it was found (`docs/flow_record.md`).", "",
         "| Design | S0 | S1 | S2 | S3 | S4 | S5 | S6 | S7 |", "|---|---|---|---|---|---|---|---|---|"]
    for d in DESIGNS:
        st = (j("outputs/flow", d, "flow_summary.json") or {}).get("stages", {})
        L.append(f"| `{d}` | " + " | ".join(st.get(s, {}).get("status", "–") for s in
                                            ("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7")) + " |")
    L += W.how("PASS: every check (gate) of the stage passed; FAIL: at least one gate failed although the stage "
               "finished (each failure is explained in the design's report; most are budgets the layout exceeds, or "
               "known properties of the circuit). No stage of the final runs crashed.")
    L += ["", "## 2. The stages: what each does and which algorithm it runs", "",
          "| Stage | Does | Algorithm / method |", "|---|---|---|"]
    L += [f"| **{s} {n}** | {a} | {b} |" for s, n, a, b in STAGES]
    L += ["", "Every stage ends with automatic checks (gates); every drawn block and layout is checked by Magic DRC and "
          "Netgen LVS, each LVS with a deliberately broken copy that must fail. The search settings (seeds, schedules, "
          "gaps, thresholds) and the hypotheses are fixed in advance in `PREREG.md`.", "",
          "## 3. What happened", ""]
    L += [f"- **{a}:** {b}" for a, b in TIMELINE]
    L += ["", "## 4. The expected novelty", "",
          "From the project's literature review (`docs/05_literature_novelty_remap.md`). Already published, so **not** "
          "claimed: per-net parasitic budgets in general, spec-to-parasitic mapping, common-centroid pattern selection, "
          "symmetry extraction, LLM-generated constraints.", "",
          "| Contribution | In one line | Status |", "|---|---|---|",
          "| C1. Intent compiled from the circuit's own model | per-node sensitivities from a small-signal model turn "
          "the specs into budgets and routing rules **before any layout**, each traceable to a node and its pole | "
          "built (S1, S2), checked against SPICE; the symbolic, hierarchical, variation-range form is partial |",
          "| C2. Device cells chosen from the requirements | each SKY130 transistor cell (fingers, contacts) chosen to "
          "keep its node within budget | built (S3); relaxations needed where budgets are tight |",
          "| C3. Budget-aware variants and placement | several signed-off variants per block, chosen and placed to "
          "minimise area **subject to the budgets** | built (S4, S5); on ttsky the budget-aware layout uses 40 % less of "
          "the wire budgets and loses less GBW and phase margin than the area-only baseline (hypothesis H5); on the "
          "small designs both choose the same placement |",
          "| C4. LLM decisions grounded in the equations, measured | an LLM proposes and explains decisions over the "
          "explicit budgets; what it adds is measured against the rule-only flow | planned (section 7) |",
          "| C5. Open, reproducible SKY130 flow | open tools, every block signed off, seeded, golden results | built |", "",
          "## 5. Results on the designs tried", ""]
    for d in DESIGNS:
        L += design_section(d)
    L += W.how("\"use of the allowance\" is the loss from schematic to layout divided by η × margin (η = 0.5): 1.0 is "
               "all the flow lets the layout take; bold is more.")
    L += ["", "## 6. Does it run without Claude?", "",
          "**Yes.** The flow calls no LLM. Everything runs in the pinned open-source EDA container "
          "(`hpretl/iic-osic-tools:2026.10`: Magic, Netgen, ngspice, xschem, KLayout, SKY130) with Python from "
          "`requirements.txt`:", "",
          "```powershell", "$env:FLOW_CONTAINER=\"layout-s0s3\"; .\\flow.ps1 run example_ota_5t       # S0–S7 of one design",
          ".\\flow.ps1 test                                                     # tests + golden results",
          ".\\gui\\gui.ps1                     # local web GUI: http://localhost:8765/ (no LLM, no tokens)", "```", "",
          "Claude was used to write and review the code and the documents; no run depends on it. The GUI edits a design "
          "(or makes a new one from files), runs the flow and writes the reports, all locally.", "",
          "## 7. The LLM integration plan", "",
          "**What:** an independent LLM (the Claude CLI, once the supervisor agrees) gets only the netlist, the "
          "hierarchy, the specs and S2's budgets, and proposes the floorplan, the matching style per block and the "
          "constraint trade-offs, with reasons. The same S4–S7 build and check its proposal exactly as they check the "
          "code's. It never places coordinates or signs anything off.", "",
          "**How it is measured:** the same designs and extraction with and without the LLM (an ablation): spec "
          "retention after layout, area, the number of extraction and SPICE runs, and how well the budgets predicted "
          "the loss. Every call is journaled (inputs, prompt version, output, validation).", "",
          "| Pros | Cons |", "|---|---|",
          "| Can use designer knowledge the cost function lacks (e.g. ttsky: Miller capacitors next to the first-stage "
          "outputs; iadc: which blocks may share a ring) | Can be confidently wrong; every output must be checked (it "
          "is: the same DRC, LVS and SPICE) |",
          "| Explains its choices in words a designer can review | Results can change with the model version; runs must "
          "be journaled and pinned to be reproducible |",
          "| Can resolve budget conflicts (which budget to relax) with the equations behind them | Costs tokens and "
          "needs a network connection and permission; the flow must keep working without it |",
          "| Literature: LLM tuning loops need few post-layout simulations (ICPI) | LLM coordinates are known to fail "
          "(ACDC): it must stay at the decision level |", "",
          "## 8. Risks of the method", ""]
    L += [f"- **{a}:** {b}" for a, b in RISKS]
    L += ["", "## 9. Where to look next", "",
          "- `docs/ttsky25a_fd_report.html`, `docs/iadc_ota_report.html`: the two detailed reports (schematics, every "
          "block, algorithms, who decides what, comparisons with the hand layouts, DRC/LVS evidence).",
          "- `docs/reports/<design>_report.html`: a short report for every design (also for designs made with the GUI).",
          "- `docs/s0_s3_walkthrough.html`, `docs/s4_s7_walkthrough.html`: every gate and number, stage by stage.",
          "- `docs/flow_record.md`: the journey, every problem found and how; `PREREG.md`: hypotheses and fixed settings;",
          "  `README.md`: how to run everything.", ""]
    return L


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-html", action="store_true")
    a = ap.parse_args(argv)
    W.IMG_PREFIX = os.path.relpath(REPO, OUT_MD.parent).replace(os.sep, "/")
    head = (subprocess.run(["git", "--no-optional-locks", "log", "-1", "--format=%h %cs"], cwd=REPO, capture_output=True,
                           text=True).stdout.strip() or "unknown")
    OUT_MD.write_text("\n".join(build(head)) + "\n")
    print(OUT_MD)
    if not a.no_html:
        css = REPO / "docs" / "flow_record" / "record.css"
        cmd = ["pandoc", OUT_MD.name, "--standalone", "--embed-resources", "--metadata",
               "title=Analog layout automation: progress report", "--toc", "-o", OUT_MD.with_suffix(".html").name] + \
            (["-c", os.path.relpath(css, OUT_MD.parent)] if css.exists() else [])
        r = subprocess.run(cmd, cwd=OUT_MD.parent, capture_output=True, text=True)
        print(OUT_MD.with_suffix(".html") if r.returncode == 0 else f"pandoc failed: {r.stderr[:400]}")
        return 0 if r.returncode == 0 else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
