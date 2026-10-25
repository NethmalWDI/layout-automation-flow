"""S2 step 3 — the engine-neutral constraint IR (constraints.json).

Every entry: id, class (hard | soft | budget | budget_derived | info), type, targets, value, units,
derived_from (equation + input files), status (evaluated | not_evaluated | not_applicable | assumption).
"""
from __future__ import annotations

import math


def entry(cid, cls, typ, targets, value=None, units=None, derived_from=None, status="evaluated", note=None):
    e = {"id": cid, "class": cls, "type": typ, "targets": targets, "value": value, "units": units,
         "derived_from": derived_from or {}, "status": status}
    if note:
        e["note"] = note
    return e


def build(ir: dict, intent: dict, budgets: dict, pdk: dict, currents: dict, hier: dict, sizes: dict,
          offset: dict | None = None) -> list:
    out = []
    lay = pdk["layers"]
    route_layers = ["metal1", "metal2", "metal3", "metal4"]
    # 1. budgets themselves
    for b in budgets["elements"]:
        if b.get("budget") is None:
            continue
        out.append(entry(f"budget.{b['id']}", "budget", b["kind"], b["targets"], b["budget"], b["units"],
                         {"equation": "progressive-filling max-min allocation of eta*margin (budgets.py)",
                          "binding": b.get("binding"), "inputs": ["outputs/S1/<design>/sensitivity.json",
                                                                  "outputs/S1/<design>/sensitivity_r.json"]}))
    # 1b. elements no modelled check limits: a default cap (ASSUMPTION), never 'anything goes'
    from src.s2.budgets import KAPPA
    for b in budgets["elements"]:
        if b.get("budget") is None:
            out.append(entry(f"default_limit.{b['id']}", "soft", b["kind"], b["targets"], round(KAPPA * b["w"], 3),
                             b["units"], {"equation": "KAPPA x expected need", "kappa": KAPPA, "w": b["w"]},
                             status="assumption",
                             note="consumes no margin in any modelled check (gain, GBW, PM, noise, DC headroom); "
                                  "unmodelled effects (CMRR, PSRR, slew) are not covered"))
    # 2. routing rules derived from the capacitance budgets
    for b in budgets["elements"]:
        if b["kind"] == "net_capacitance" and b.get("budget") is not None:
            top = hier["nets"][b["targets"][0]]["route_budget_fF"]
            for L in route_layers:
                cg = lay[L].get("cap_worst_F_per_um", lay[L]["cap_to_substrate_F_per_um_single"]) * 1e15
                out.append(entry(f"route.max_length.{b['targets'][0]}.{L}", "budget_derived", "max_route_length",
                                 [b["targets"][0]], round(top / cg, 2), "um",
                                 {"equation": "L_max = C_route_share / C_per_um(layer, min width, worst measured environment)",
                                  "C_route_share_fF": top, "C_per_um_fF": cg,
                                  "inputs": ["outputs/S2/pdk/parasitics.json"]}))
        if b["kind"] == "coupling" and b.get("budget") is not None:
            for L in route_layers:
                cc = lay[L]["coupling_F_per_um_at_min_spacing"] * 1e15
                out.append(entry(f"route.max_parallel.{b['id']}.{L}", "budget_derived", "max_parallel_run_at_min_spacing",
                                 b["targets"], round(b["budget"] / cc, 2), "um",
                                 {"equation": "L_par = C_coupling_budget / C_coupling_per_um(layer, min spacing)",
                                  "C_budget_fF": b["budget"], "Cc_per_um_fF": cc,
                                  "inputs": ["outputs/S2/pdk/parasitics.json"]}))
        if b["kind"] == "terminal_resistance" and b.get("budget") is not None:
            r1 = lay["metal1"]["res_ohm_per_um_at_min_width"]
            out.append(entry(f"route.max_series_R.{b['id']}", "budget_derived", "max_series_resistance_device_to_net",
                             b["targets"], round(b["budget"], 3), "ohm",
                             {"equation": "R_access(PCell option, S3) + R_wire <= R_budget; "
                                          f"met1 at min width = {r1:.4g} ohm/um",
                              "met1_ohm_per_um": r1},
                             note="S3 reports how much of this the chosen PCell option uses; S5 gets the rest"))
    # 3. proximity: devices sharing a tightly budgeted net must be close (D4)
    for n, h in hier["nets"].items():
        if h.get("max_route_length_metal1_um") is not None and len(h["devices"]) >= 2:
            out.append(entry(f"place.proximity.{n}", "hard" if h["max_route_length_metal1_um"] < 50 else "soft",
                             "max_pin_distance", h["devices"], round(h["max_route_length_metal1_um"], 2), "um",
                             {"equation": "the route of the net must fit its met1 length budget",
                              "net": n, "hard_if_below_um": 50},
                             note="ASSUMPTION: hard below 50 um (a few device pitches), soft above"))
    # 4. matching / symmetry (rule-based: no mismatch model upstream)
    for m in intent["matching"]:
        devs = m["devices"]
        out.append(entry(f"match.same_pcell_options.{'_'.join(devs)}", "hard", "identical_device_options", devs,
                         derived_from={"rule": f"{m['kind']} from hierarchy", "evidence": m["evidence"]}))
        out.append(entry(f"place.symmetry.{'_'.join(devs)}", "hard", "symmetric_placement_common_axis", devs,
                         derived_from={"rule": f"{m['kind']} matching (offset, CMRR)"},
                         note="pattern (side-by-side / ABAB / ABBA / common centroid) chosen in S4"))
    # mismatch of matched terminals: systematic offset (S1, one-sided resistors); no offset spec given
    for term, o in sorted(((offset or {}).get("terminals") or {}).items()):
        if not o.get("ohm_per_mV_offset"):
            continue
        out.append(entry(f"match.max_R_difference.{term}", "hard", "max_resistance_mismatch_in_pair", [term],
                         round(o["ohm_per_mV_offset"], 2), "ohm per mV of allowed systematic offset",
                         {"equation": "systematic input offset per ohm, measured in a unity-gain follower (S1)",
                          "offset_uV_per_ohm": o["offset_uV_per_ohm_5ohm"],
                          "inputs": ["outputs/S1/<design>/sensitivity_r.json"]},
                         status="not_evaluated",
                         note="absolute limit needs an offset spec (not in the design package): requested"))
    ins = [p["name"] for p in ir["ports"] if p["role"] == "input"]
    if len(ins) == 2:
        out.append(entry("route.symmetric.inputs", "hard", "mirrored_routing", ins,
                         derived_from={"rule": "differential inputs of the diff pair"}))
    dp = next((m for m in intent["matching"] if m["kind"] == "diff_pair"), None)
    if dp:
        drains = sorted({d["terminals"]["d"] for d in ir["devices"] if d["name"] in dp["devices"]})
        out.append(entry("route.symmetric.pair_drains", "soft", "matched_routing_capacitance", drains,
                         derived_from={"rule": "pair drains should see equal capacitance up to the load"},
                         status="assumption",
                         note="not quantified: no mismatch/offset symbols upstream (request B3d); the per-net "
                              "C budgets still apply"))
    # 5. electromigration: data not available -> not evaluated (never invented)
    for n, c in currents["nets"].items():
        out.append(entry(f"route.em_width.{n}", "hard", "min_width_from_current", [n], None, "um",
                         {"trunk_current_A": c.get("trunk_A"), "max_branch_A": c["max_branch_A"],
                          "equation": "W >= I / J_max(layer, T)"},
                         status="not_evaluated",
                         note="SKY130 electromigration limits were not found in the PDK files or docs "
                              "searched; requested from you. Currents here are <= "
                              f"{max(x.get('trunk_A', x['max_branch_A']) for x in currents['nets'].values())*1e6:.1f} uA."))
    # 6. latch-up (PDK rule, enforced by the Magic deck)
    out.append(entry("place.latchup_tap_distance", "hard", "max_diff_to_tap_distance", ["all devices"], 15.0, "um",
                     {"rule": "LU.2 / LU.3 (text of the latch-up rules in sky130A.tech)", "pdk_file": pdk["rules"]["source"]},
                     status="assumption",
                     note="our Magic drc(full) run does not check it (the deck applies it with a chip-level marker); "
                          "it is met by construction while every PCell keeps its own guard ring (S3)"))
    for p in ir["ports"]:
        if p["role"] == "bias":
            out.append(entry(f"route.bias_net.{p['name']}", "soft", "coupling_to_bias_net", [p["name"]], None, None,
                             {"rule": "the testbench holds the bias node with an ideal source (AC ground)"},
                             status="not_evaluated",
                             note="couplings onto the bias net consume no margin in this model; the impedance of the "
                                  "real bias generator is needed to budget them (ASSUMPTION)"))
    out.append(entry("route.no_cross_digital", "hard", "no_crossing_over_high_impedance", [], None, None,
                     {"rule": "digital/clock nets must not cross high-impedance analog nets"},
                     status="not_applicable", note="no digital or clock nets in this circuit"))
    return out
