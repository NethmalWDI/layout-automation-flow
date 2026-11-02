#!/usr/bin/env python3
"""Generate docs/s0_s3_walkthrough.md (and, with pandoc, a self-contained HTML copy): what S0, S1, S2 and S3 did on
each design and what came out, read only from the run's own output files (outputs/<stage>/<design>/, the flow
summary, the plots). Nothing in it is typed by hand except the one-line meaning of each gate and the explanation
of a known finding.

usage (inside layout-s0s3, repo root): python3 scripts/make_s0s3_walkthrough.py [design ...] [--no-html] [--out FILE.md]
default designs: example_ota_5t loadbench_miller
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = next(p for p in Path(__file__).resolve().parents if (p / "src").is_dir())
OUT_MD = REPO / "docs" / "s0_s3_walkthrough.md"
IMG_PREFIX = ".."     # image paths relative to the output file's folder (set in main)

GATE_MEANING = {
    "G0.1": "every element of the netlist is recognised (MOSFETs, sources, passives counted)",
    "G0.2": "netlist and package are consistent (no undefined nodes, models or ports)",
    "G0.3": "the design sources match their frozen SHA-256 hashes",
    "G0.4": "the upstream names map onto this netlist",
    "G0.5": "the IR written back as SPICE is LVS-identical to the source netlist (Netgen)",
    "G0.6": "the testbenches run and reproduce the performance; the specs are fixed from it",
    "G0.7": "each device, drawn by the SKY130 PCell at its exact size, passes Magic DRC and Netgen LVS (both with negative controls)",
    "G0.8": "this flow's simulation reproduces the external reference values",
    "G0.9": "45 PVT points (5 corners × 3 supplies × 3 temperatures) simulated",
    "G0.10": "mismatch Monte Carlo (200 runs)",
    "G0.11": "the designer's groups compared with the automatic blocks",
    "G1.1": "operating point: functional devices saturated, supply current reproduced, charge conservation",
    "G1.2": "the exact linear model reproduces SPICE's gain, GBW and PM",
    "G1.3": "capacitance sensitivities of the linear model agree with SPICE finite differences",
    "G1.4": "matching groups (differential pair, mirrors) are present and consistent",
    "G1.5": "hand (symbolic) model against SPICE: reported, not gated",
    "G1.6": "resistance sensitivities agree with SPICE (small-signal, or a confirmed bias shift)",
    "G2.0": "share of each margin a compact layout would use (expected need), before any budget",
    "G2.1": "every rule names a net, device or terminal that exists",
    "G2.2": "every rule has units and provenance",
    "G2.3": "the joint allocation (max-min fair + refinement) is feasible and reproducible",
    "G2.4": "first-order use against the linear model with all budgets inserted (reported)",
    "G2.5": "SPICE verification: each check with all its harmful budgets inserted stays within eta × margin",
    "G2.6": "block-level shares add up to the budgets",
    "G2.7": "the S3 library's cheapest cells fit inside the budgets (library floors)",
    "G2.8": "five other budget rules scored on the same sensitivities (reported)",
    "G2.9": "use of each PVT point's margin by the final budgets, first order (reported)",
    "G2.10": "first order against SPICE for every simulated check (reported)",
    "G3.1": "the chosen cells are DRC-clean (Magic)",
    "G3.2": "the chosen cells are LVS-correct for W, L and nf (Netgen)",
    "G3.3": "the circuit with every chosen cell meets every spec in SPICE, saturated, within its allowance",
    "G3.4": "every option of the library was built and signed off",
    "G3.5": "no device type had to be relaxed (every type has an option within its allowance)",
    "G3.6": "the transistor model has no gate resistance, so S3 adds the cells' own",
    "G3.7": "option modes (reported)",
}
STAGE_DOES = {
    "S0": "Ingest: reads the sized netlist and the package, freezes the sources by hash, builds the circuit IR "
          "(devices, nets, blocks), draws every device with the SKY130 PCell and signs it off (DRC, LVS), reproduces "
          "the testbenches, and simulates 45 PVT points and a mismatch Monte Carlo.",
    "S1": "Electrical intent: extracts the operating point, builds the exact small-signal (linear) model and checks "
          "it against SPICE, computes how every net capacitance, coupling and terminal resistance moves gain, GBW, PM "
          "and noise (checked against SPICE finite differences), and finds the matching groups.",
    "S2": "Budgets: shares a fraction eta of each spec margin between all layout parasitics (fF, Ω) by a joint "
          "max-min fair allocation, floors every budget at what the cheapest library cell already adds, verifies the "
          "budgets in SPICE, and scores five other budget rules on the same data.",
    "S3": "Devices: builds a library of layout cells per device type (fingers, gate and diffusion options; each "
          "DRC/LVS-signed and extracted), picks for every type the smallest cell that stays within its S2 "
          "allowance, and simulates the whole circuit with all chosen cells.",
}
# Units by the spec name's suffix, for IRs whose margins carry none (LOADBench).
SPEC_UNITS = {"db": "dB", "mhz": "MHz", "deg": "deg", "uw": "uW", "rthz": "nV/sqrt(Hz)"}


def _j(p: Path):
    return json.loads(p.read_text()) if p.exists() else None


def f(v, nd=3):
    if v is None:
        return "–"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, float):
        return f"{v:.{nd}g}" if abs(v) < 1e4 else f"{v:.3e}"
    return str(v)


def img(path: str, width: int = 520, alt: str = "") -> str:
    return f'<img src="{IMG_PREFIX}/{path}" width="{width}" alt="{alt}">'


def gate_rows(gates: dict) -> list:
    rows = ["| Gate | Result | What it checks |", "|---|---|---|"]
    for g, v in gates.items():
        key = g.split("_")[0]
        p = v.get("pass")
        res = "PASS" if p is True else ("**FAIL**" if p is False else "info")
        rows.append(f"| {g.replace('_', ' ')} | {res} | {GATE_MEANING.get(key, '')} |")
    return rows


def known_findings(d: str, gates: dict, stage: str) -> list:
    """An explanation for every failed gate, with its numbers read from the files."""
    out = []
    for g, v in gates.items():
        if v.get("pass") is not False:
            continue
        key = g.split("_")[0]
        if key == "G0.7":
            pb = _j(REPO / "outputs/S0" / d / "pcell_binding.json") or {}
            bad = [(x["device"], x["drc"].get("errors"), x["lvs"].get("match")) for x in pb.get("devices", []) if not x["pass"]]
            ok = sum(1 for x in pb.get("devices", []) if x["pass"])
            out.append(f"- **G0.7 (PDK finding, not a flow error).** {ok} of {len(pb.get('devices', []))} devices pass. "
                       + "; ".join(f"`{n}`: {e} DRC errors, LVS {'match' if m else 'no match'}" for n, e, m in bad)
                       + ". The SKY130 PCell drawn at the netlist's exact size (one 484 µm finger) breaks the PDK's "
                         "minimum metal-area rule at its gate contact pad (met1.6). S3 builds its own cells and widens "
                         "that pad (flow record row 37), so every cell S3 chooses is DRC-clean (G3.1).")
        elif key == "G1.6":
            bad = [c for c in v.get("checks", []) if not c.get("pass", True)]
            out.append(f"- **G1.6 (a modelling limit, reported).** {len(v.get('checks', [])) - len(bad)} of "
                       f"{len(v.get('checks', []))} resistance checks pass. "
                       + "; ".join(f"`{c['case']}` on {c['spec']}: first-order error at 100 Ω = "
                                   f"{f(c.get('pred_err_at_100ohm_frac_of_margin'), 2)} of the margin (limit 0.05), "
                                   f"mechanism: {c.get('mechanism')}" for c in bad)
                       + ". The resistor shifts the bias point; re-solving the linear model at the shifted operating "
                         "point explains the effect, but the first-order prediction misses by more than the limit. S2 "
                         "uses the SPICE-measured rate for such terminals.")
        elif key == "G3.5":
            rel = v.get("relaxed", [])
            out.append(f"- **G3.5 (the budgets are tighter than any cell, flagged).** {len(rel)} device type(s) "
                       f"relaxed: {', '.join(f'`{r}`' for r in rel)}. No option of these types stays within its S2 "
                       f"allowance, so S3 keeps the option whose worst check is broken least ('{v.get('fallback')}', "
                       "access resistance included) and flags the type. The circuit with every chosen cell is then "
                       "simulated (G3.3).")
        else:
            out.append(f"- **{g}** failed: see `outputs/{stage}/{d}/{stage.lower()}_report.json`.")
    return out


def schematic_values(g06: dict) -> dict:
    """The schematic's testbench values from G0.6: `measured` (no upstream run) or the rerun side of `compare`."""
    if g06.get("measured"):
        return g06["measured"]
    return {k: v.get("rerun") for k, v in (g06.get("compare") or {}).items() if isinstance(v, dict)}


def s0_section(d: str, rep: dict) -> list:
    g = rep["gates"]
    ir = _j(REPO / "outputs/S0" / d / "circuit_ir.json") or {}
    L = []
    inv = g.get("G0.1_inventory", {})
    L.append(f"- **Netlist:** {inv.get('mosfets')} MOSFETs, {inv.get('sources')} source(s), {inv.get('passives')} "
             f"passive(s); {len(ir.get('nets', []))} nets; {len((ir.get('hierarchy') or {}).get('blocks', []))} blocks.")
    blocks = (ir.get("hierarchy") or {}).get("blocks", [])
    if blocks:
        L += ["", "| Block | Kind | Devices | Source |", "|---|---|---|---|"]
        for b in blocks:
            L.append(f"| {b.get('name')} | {b.get('primitive') or b.get('category') or b.get('kind', '')} | "
                     f"{', '.join(b.get('devices', []))} | {b.get('source', 'automatic')} |")
    g06 = g.get("G0.6_testbench_reproduction", {})
    cmp_ = g06.get("compare") or {}
    if cmp_:
        L += ["", f"**Testbench reproduction (G0.6):** the upstream testbenches re-run here, nominal corner (tolerance "
                  f"{f(100 * g06.get('tolerance_rel', 0), 2)} %).", "",
              "| Quantity | Upstream | This run | Within tolerance |", "|---|---|---|---|"]
        for k, v in cmp_.items():
            if isinstance(v, dict):
                L.append(f"| {k} | {f(v.get('upstream'), 6)} | {f(v.get('rerun'), 6)} | "
                         f"{'yes' if v.get('ok') else '**no**'} |")
    m = g06.get("measured", {})
    if m:
        L += ["", "**Testbench reproduction (G0.6), schematic, nominal corner:**", "",
              "| gain (dB) | GBW (MHz) | PM (deg) | supply current (µA) | power (µW) | input noise at 1 kHz (nV/√Hz) |",
              "|---|---|---|---|---|---|",
              f"| {f(m.get('gain_db'), 6)} | {f(m.get('gbw_mhz'), 5)} | {f(m.get('pm_deg'), 4)} | {f(m.get('isup_ua'), 4)} | "
              f"{f(m.get('power_uw'), 4)} | {f(m.get('vnoise_nv_rthz'), 4)} |"]
    margins = ir.get("margins") or {}
    if margins:
        L += ["", "**Specs and margins** (margin = how far the schematic is from the spec):", "",
              "| Spec | Kind | Limit | Schematic | Margin |", "|---|---|---|---|---|"]
        for k, v in margins.items():
            L.append(f"| {k} | {v.get('kind')} | {f(v.get('limit'), 6)} | {f(v.get('value', v.get('achieved')), 6)} | "
                     f"{f(v.get('margin'), 4)} {v.get('units') or SPEC_UNITS.get(k.rsplit('_', 1)[-1], '')} |")
    ref = g.get("G0.8_external_reference", {}).get("compare")
    if ref:
        L += ["", "**External reference (G0.8):** " + "; ".join(
            f"{k} {f(v.get('reference'), 4)} vs {f(v.get('this_flow'), 4)}" for k, v in ref.items()) + "."]
    pb = _j(REPO / "outputs/S0" / d / "pcell_binding.json") or {}
    if pb.get("devices"):
        L += ["", "**PCell binding (G0.7):** every device drawn by the SKY130 PCell at its exact size, then Magic DRC "
                  "and Netgen LVS, each with a negative control that must fail.", "",
              "| Device | DRC errors | DRC control caught | LVS | LVS control caught | Pass |", "|---|---|---|---|---|---|"]
        for x in pb["devices"]:
            L.append(f"| {x['device']} | {f(x['drc'].get('errors'))} | {f(x['drc'].get('neg_control_flagged'))} | "
                     f"{'match' if x['lvs'].get('match') else 'no match'} | {f(x['lvs'].get('neg_control_rejected'))} | "
                     f"{'PASS' if x['pass'] else '**FAIL**'} |")
        pics = [x for x in pb["devices"] if x.get("png")][:3]
        if pics:
            L += ["", " ".join(img(x["png"], 240, x["device"]) for x in pics),
                  "", f"*PCells as drawn: {', '.join(x['device'] for x in pics)}.*"]
    pv = g.get("G0.9_pvt (info)", {})
    if pv:
        L += ["", f"**PVT (G0.9):** {pv.get('points')} points; the schematic meets every spec at "
                  f"{pv.get('meeting_all_specs')} of them."]
    mc = (g.get("G0.10_mismatch_mc (info)") or {}).get("summary") or {}
    if mc:
        L += ["", "**Mismatch Monte Carlo (G0.10):** " + "; ".join(
            f"{k} {f(v.get('mean'), 4)} ± {f(v.get('std'), 2)} (n = {v.get('n')})" for k, v in mc.items()
            if isinstance(v, dict)) + "."]
    pl = REPO / "outputs/S0" / d / "plots" / "pvt_specs.png"
    if pl.exists():
        L += ["", img(f"outputs/S0/{d}/plots/pvt_specs.png", 640, "PVT"), "", "*Specs at the 45 PVT points.*"]
    return L


def s1_section(d: str, rep: dict) -> list:
    g = rep["gates"]
    L = []
    op = g.get("G1.1_operating_point", {})
    sat = op.get("saturation") or {}
    mins = sorted(((k, v.get("vds_minus_vdsat_V") if isinstance(v, dict) else v) for k, v in sat.items()),
                  key=lambda t: (t[1] is None, t[1]))
    L.append(f"- **Operating point (G1.1):** supply current {f(op.get('isup_uA'), 4)} µA (testbench "
             f"{f(op.get('isup_achieved_uA'), 4)} µA); devices not saturated: {op.get('not_saturated') or 'none'}"
             + (f"; smallest vds − vdsat: {mins[0][0]} {f(mins[0][1], 3)} V" if mins and isinstance(mins[0][1], float) else "") + ".")
    lm = g.get("G1.2_linear_model_vs_spice", {})
    if lm:
        a, s, dl = lm.get("linear", {}), lm.get("spice", {}), lm.get("delta", {})
        L += ["", "**Linear model against SPICE (G1.2):**", "", "| | gain (dB) | GBW (MHz) | PM (deg) |", "|---|---|---|---|",
              f"| linear model | {f(a.get('gain_db'), 6)} | {f(a.get('gbw_mhz'), 6)} | {f(a.get('pm_deg'), 6)} |",
              f"| SPICE | {f(s.get('gain_db'), 6)} | {f(s.get('gbw_mhz'), 6)} | {f(s.get('pm_deg'), 6)} |",
              f"| difference | {f(dl.get('gain_db'), 2)} dB | {f(100 * (dl.get('gbw_rel') or 0), 2)} % | {f(dl.get('pm_deg'), 2)} deg |"]
    c3 = g.get("G1.3_sensitivity_vs_spice", {}).get("checks", [])
    c6 = g.get("G1.6_resistance_sensitivity_vs_spice", {}).get("checks", [])
    if c3 or c6:
        L += ["", f"- **Sensitivities checked against SPICE:** capacitance (G1.3) "
                  f"{sum(1 for c in c3 if c.get('pass', True))} of {len(c3)} checks pass; resistance (G1.6) "
                  f"{sum(1 for c in c6 if c.get('pass', True))} of {len(c6)}."]
    sens = _j(REPO / "outputs/S1" / d / "sensitivity.json") or {}
    rows = []
    for item, row in (sens.get("table") or {}).items():
        for spec, v in row.items():
            if isinstance(v, dict) and v.get("fF_to_consume_margin") not in (None, 0):
                rows.append((abs(v["fF_to_consume_margin"]), item, spec, v.get("linear_per_fF")))
    if rows:
        L += ["", "**The most critical capacitances** (fF that alone would use the whole margin; smallest first):", "",
              "| Net or coupling | Spec | fF to use the margin | Change per fF |", "|---|---|---|---|"]
        for fm, item, spec, per in sorted(rows)[:8]:
            L.append(f"| `{item}` | {spec} | {f(fm, 3)} | {f(per, 3)} |")
    mg = g.get("G1.4_matching_groups", {}).get("groups", [])
    if mg:
        L += ["", "**Matching groups (G1.4):** " + "; ".join(
            f"{(x.get('kind') or '').replace('_', ' ')}: {', '.join(x.get('devices', []))}"
            + ("" if x.get("consistent", True) else " (not consistent)") for x in mg) + "."]
    sp = _j(REPO / "outputs/S1" / d / "symbolic_patch_check.json")
    if sp and sp.get("models"):
        L += ["", "**Hand model against SPICE (G1.5, report only):**", "", "| Model | gain (dB) | GBW (MHz) | PM (deg) |",
              "|---|---|---|---|"]
        for k, v in sp["models"].items():
            p = v["predicted"]
            L.append(f"| {k} | {f(p.get('gain_db'), 4)} | {f(p.get('gbw_mhz'), 4)} | {f(p.get('pm_deg'), 4)} |")
        s = sp.get("spice", {})
        L.append(f"| SPICE | {f(s.get('gain_db'), 4)} | {f(s.get('gbw_mhz'), 4)} | {f(s.get('pm_deg'), 4)} |")
    for name, cap, w in (("bode_linear_vs_spice.png", "Open-loop response: linear model against SPICE.", 560),
                         ("sensitivity_comparison.png", "Sensitivities: linear model against SPICE finite differences.", 560),
                         ("symbolic_patch.png", "Hand model against SPICE.", 460)):
        if (REPO / "outputs/S1" / d / "plots" / name).exists():
            L += ["", img(f"outputs/S1/{d}/plots/{name}", w, name), "", f"*{cap}*"]
    return L


def s2_section(d: str, rep: dict) -> list:
    g = rep["gates"]
    b = _j(REPO / "outputs/S2" / d / "budgets.json") or {}
    L = [f"- **eta = {rep.get('eta')}**: layout may use {f(100 * rep.get('eta', 0), 2)} % of each margin. Budgets are set "
         f"at the {'nominal corner' if rep.get('budget_corners') == 'nominal' else 'nominal and PVT points'}; "
         f"round-1 t (budget / expected need of the tightest elements) = {f(g.get('G2.3_allocation', {}).get('t_round1'), 3)}."]
    g0 = g.get("G2.0_expected_layout_use (info)", {}).get("checks", {})
    if g0:
        L += ["", "**Expected layout use (G2.0):** the share of each margin a compact layout would use (above eta, the "
                  "budgets fall below the expected need).", "", "| Check | Share of margin |", "|---|---|"]
        for k, v in g0.items():
            if "@" not in k:
                L.append(f"| {k} | {f(v.get('fraction_of_margin'), 3)} |")
    el = [e for e in b.get("elements", []) if e.get("budget") is not None]
    if el:
        el.sort(key=lambda e: e["budget"] / e["w"])
        L += ["", f"**Budgets** ({len(el)} elements; the 10 tightest relative to their expected need):", "",
              "| Element | Kind | Expected need | Budget | Budget / need | Binding check |", "|---|---|---|---|---|---|"]
        for e in el[:10]:
            L.append(f"| `{e['id']}` | {e['kind'].replace('_', ' ')} | {f(e['w'], 3)} {e['units']} | {f(e['budget'], 3)} {e['units']} | "
                     f"{f(e['budget'] / e['w'], 3)} | {', '.join(e.get('binding') or [])} |")
    v5 = g.get("G2.5_spice_budget_verification", {})
    if v5.get("rows"):
        L += ["", f"**SPICE verification (G2.5,** {v5.get('iterations')} iteration(s)**):** for each check, every "
                  "harmful budget inserted at once in the transistor-level circuit.", "",
              "| Check | Allowed use | First order | SPICE | Within |", "|---|---|---|---|---|"]
        for r in v5["rows"]:
            L.append(f"| {r['check']} | {f(r.get('allowed_eta_margin'), 3)} | {f(r.get('first_order_use_frac_of_allowed'), 3)} × | "
                     f"{f(r.get('spice_use_frac_of_allowed'), 3)} × | {'yes' if r.get('ok') else '**no**'} |")
        L += ["", "*Within: SPICE use at most 1.02 × the allowed use (`TOL_USE` = 0.02, `src/common/tolerance.py`; "
                  "PREREG amendment of 2026-11-01).*"]
        if v5.get("closure_scaled_elements"):
            L += ["", f"*Closure step: {', '.join(v5['closure_scaled_elements'])} scaled down so that SPICE stays within "
                      "the allowance.*"]
    sc = g.get("G2.8_baselines (info)", {}).get("scores", {})
    if sc:
        L += ["", "**Other budget rules on the same data (G2.8):** outcome over every simulated check (nominal and each "
                  "rule's most-used PVT points), and at the nominal corner alone.", "",
              "| Rule | Outcome | Nominal only | Worst SPICE use of allowed | Budget / need (min) |", "|---|---|---|---|---|"]
        for m, s in sc.items():
            L.append(f"| {m} | {s.get('outcome')} | {s.get('outcome_nominal', '–')} | {f(s.get('spice_worst_use_of_allowed'), 3)} | "
                     f"{f(s.get('min_ratio_to_need'), 3)} |")
        L += ["", "*G2.8 scores every rule before G2.5's closure step, which is fair to all of them, so 'ours' here is "
                  "the allocation before the closure. The budgets S2 hands to S3 are the closed ones that pass G2.5 "
                  "above (flow record 7.13). The budgets are set at the nominal corner, so a rule can be ok there and "
                  "unsafe at a PVT point (G2.9 below).*"]
    g9 = g.get("G2.9_pvt_constraints (info)", {})
    if g9.get("worst"):
        w = g9["worst"]
        L += ["", f"**PVT points (G2.9, reported):** worst first-order use {f(w.get('use_of_allowed'), 3)} × at "
                  f"{w.get('spec')} {w.get('point')}; {len(g9.get('over_allowed', []))} point-spec checks above 1."]
    g10 = g.get("G2.10_model_agreement (info)", {})
    if g10:
        L += ["", f"**First order against SPICE (G2.10):** {g10.get('checks_compared')} checks compared, "
                  f"{len(g10.get('flagged', []))} flagged (sign disagreement, or a difference above "
                  f"{g10.get('flag_diff_frac_of_margin')} of the margin)."]
    for name, cap in (("budgets.png", "Budgets against expected need."), ("budget_verification.png", "SPICE verification."),
                      ("baselines.png", "The six budget rules.")):
        if (REPO / "outputs/S2" / d / "plots" / name).exists():
            L += ["", img(f"outputs/S2/{d}/plots/{name}", 600, name), "", f"*{cap}*"]
    return L


def s3_section(d: str, rep: dict) -> list:
    g = rep["gates"]
    dd = _j(REPO / "outputs/S3" / d / "device_decisions.json") or {}
    types = {k: v for k, v in (dd.get("decisions") or {}).items() if isinstance(v, dict) and v.get("cell")}
    L = []
    if types:
        L += [f"**Chosen cells** ({len(types)} device types; {g.get('G3.4_option_table_complete', {}).get('options')} "
              "options built and signed off):", "",
              "| Device type | Devices | Chosen option | Area (µm²) | Relaxed | Why |", "|---|---|---|---|---|---|"]
        for tid, v in types.items():
            opt = v["cell"].split("__", 1)[-1]
            why = (v.get("reason") or "").split(":")[0].split(" (")[0]
            L.append(f"| `{tid}` | {', '.join(v.get('devices', []))} | `{opt}` | {f(v.get('area_um2'), 4)} | "
                     f"{'**yes**' if v.get('relaxed') else 'no'} | {why} |")
        tot = sum((v.get("area_um2") or 0) * len(v.get("devices", [])) for v in types.values())   # as S3 counts it
        L += ["", f"Total device area (every device counted): {f(tot, 4)} µm²."]
    g7 = g.get("G3.7_modes (info)", {})
    if g7.get("summary"):
        L += ["", f"**Option modes (G3.7, reported):** S3 decides in its main mode, {g7.get('main_mode')}; the others are "
                  "reported for comparison (B: nf as in the netlist; A-bin: each finger stays in the sized device's "
                  "SKY130 model bin; A-free: no bin restriction; RoT: a rule-of-thumb folding baseline).", "",
              "| Mode | Total area (µm²) | Relaxed types | Types with fingers outside the sized bin |", "|---|---|---|---|"]
        for m, v in g7["summary"].items():
            L.append(f"| {f'**{m}** (main)' if m == g7.get('main_mode') else m} | {f(v.get('total_area_um2'), 4)} | "
                     f"{len(v.get('relaxed') or [])} | {len(v.get('fingers_outside_sized_bin') or [])} |")
    g3 = g.get("G3.3_all_chosen_devices_in_circuit", {})
    s0 = schematic_values((_j(REPO / "outputs/S0" / d / "s0_report.json") or {}).get("gates", {})
                          .get("G0.6_testbench_reproduction", {}))
    if g3.get("specs"):
        L += ["", "**The circuit with every chosen cell, in SPICE (G3.3):**", "",
              "| Spec | Schematic | With the chosen cells | Meets the spec |", "|---|---|---|---|"]
        for k, v in g3["specs"].items():
            L.append(f"| {k} | {f(s0.get(k), 6)} | {f(v, 6)} | {'yes' if g3.get('meets', {}).get(k) else '**no**'} |")
    cells = [v for v in types.values() if v.get("png")]
    if cells:
        L += ["", " ".join(img(v["png"], 220, v["cell"]) for v in cells[:6]), "",
              "*Chosen cells (DRC- and LVS-signed, G3.1 and G3.2).*"]
    if (REPO / "outputs/S3" / d / "plots" / "option_space.png").exists():
        L += ["", img(f"outputs/S3/{d}/plots/option_space.png", 600, "options"), "", "*Every option per device type: area "
                                                                                    "against its worst use of the allowance.*"]
    return L


def design_section(d: str) -> list:
    fs = _j(REPO / "outputs/flow" / d / "flow_summary.json") or {}
    stages = fs.get("stages", {})
    L = [f"## {d}", "", f"Run: `./flow run {d}` (all four stages). Status, run time and the files of each stage:", "",
         "| Stage | Status | Started | Run time | Steps |", "|---|---|---|---|---|"]
    for st in ("S0", "S1", "S2", "S3"):
        s = stages.get(st, {})
        secs = sum(x.get("seconds") or 0 for x in s.get("steps", []))
        L.append(f"| {st} | **{s.get('status', '–')}** | {s.get('started', '–')} | {secs / 60:.1f} min | "
                 f"{', '.join(x.get('step', '') for x in s.get('steps', []))} |")
    findings = []
    builders = {"S0": s0_section, "S1": s1_section, "S2": s2_section, "S3": s3_section}
    body = []
    for st in ("S0", "S1", "S2", "S3"):
        rep = _j(REPO / "outputs" / st / d / f"{st.lower()}_report.json")
        if rep is None:
            body += [f"### {st}", "", "*No report: the stage has not run.*", ""]
            continue
        findings += known_findings(d, rep["gates"], st)
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
    global IMG_PREFIX
    out_md = Path(a.out).resolve()
    out_md.parent.mkdir(parents=True, exist_ok=True)
    IMG_PREFIX = os.path.relpath(REPO, out_md.parent).replace(os.sep, "/")
    head = (subprocess.run(["git", "--no-optional-locks", "log", "-1", "--format=%h %cs"], cwd=REPO, capture_output=True,
                           text=True).stdout.strip() or "unknown")
    L = ["# S0–S3 walkthrough: what each stage does and what it produced", "",
         f"Generated by `python3 scripts/make_s0s3_walkthrough.py` from the run's own output files (repo at {head}). "
         "Every number below is read from `outputs/`; nothing is typed by hand except the one-line meaning of each gate "
         "and the explanation of a known finding. The flow and its rules are described in `README.md` and "
         "`docs/flow_record.md` (section 7.13 for the current version).", "",
         "**The four stages:**", ""]
    L += [f"- **{st}**: {txt}" for st, txt in STAGE_DOES.items()]
    L += ["", "**Status per design** (PASS: every gate passes; FAIL: a gate reports a finding, explained under the design; "
              "ERROR would be a crash):", "", "| Design | S0 | S1 | S2 | S3 |", "|---|---|---|---|---|"]
    for d in a.designs:
        st = (_j(REPO / "outputs/flow" / d / "flow_summary.json") or {}).get("stages", {})
        L.append(f"| {d} | " + " | ".join(st.get(s, {}).get("status", "–") for s in ("S0", "S1", "S2", "S3")) + " |")
    L.append("")
    for d in a.designs:
        L += design_section(d)
    out_md.write_text("\n".join(L) + "\n")
    print(out_md)
    if not a.no_html:
        html = out_md.with_suffix(".html")
        css = REPO / "docs" / "flow_record" / "record.css"
        cmd = ["pandoc", out_md.name, "--standalone", "--embed-resources", "--metadata", "title=S0–S3 walkthrough",
               "-o", html.name] + (["-c", os.path.relpath(css, out_md.parent)] if css.exists() else [])
        r = subprocess.run(cmd, cwd=out_md.parent, capture_output=True, text=True)
        print(html if r.returncode == 0 else f"pandoc failed: {r.stderr[:400]}")
        if r.returncode != 0:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
