#!/usr/bin/env python3
"""S2 — requirement compiler: joint budgets, hierarchical port budgets, typed rules, verification.

usage (inside layout-s0s3):  python3 -m src.s2.run inputs/<design>/package.yaml [--eta 0.5] [--no-spice]
       eta: --eta on the command line, else the package key 'eta', else ETA_DEFAULT = 0.5

Inputs : outputs/S0/<design>/{circuit_ir.json, pcell_binding.json, tb/}, outputs/S1/<design>/{sensitivity.json,
         sensitivity_r.json, intent.json, currents.json, operating_point.json}, outputs/S2/pdk/parasitics.json
Outputs: outputs/S2/<design>/
  budgets.json       per parasitic element: budget, units, expected need, binding constraint, margin used
  hierarchy.json     the same budgets pushed down to blocks: block-port and top-level shares (N1)
  constraints.json   typed rule IR (budgets, derived routing/placement rules, matching, EM, latch-up)
  verification.json  all budgets inserted at once: linear model and transistor-level SPICE vs specs
  plots/*.png, s2_report.json (gates G2.1-G2.6)
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.common.tools import REPO, provenance, rel, run_ngspice_text, write_json
from src.s0.ingest import load_package
from src.s1 import linear, op as opmod, resistance
from src.s1.run import ac_drive
from src.s2 import budgets as B, rules as R

ETA_DEFAULT = 0.5          # ASSUMPTION (accepted): half of every margin is reserved for layout
COUPLE_FRACTION = 0.25     # ASSUMPTION: expected parallel run = 1/4 of the shorter of the two routes
SPECS = ("gain_db", "gbw_mhz", "pm_deg", "vnoise_nv_rthz")
TOL_VERIFY = 0.10          # ASSUMPTION: 10 % of the allowed use for first-order model error
CLOSURE_ITERS = 2


def device_sizes(s0: Path) -> dict:
    """Bounding box (um) of every device's PCell from S0/G0.7 (measured on the GDS)."""
    import klayout.db as kdb
    pb = json.loads((s0 / "pcell_binding.json").read_text())
    out = {}
    for d in pb["devices"]:
        ly = kdb.Layout()
        ly.read(str(REPO / d["gds"]))
        bb = ly.top_cell().dbbox()
        out[d["device"]] = {"w_um": bb.width(), "h_um": bb.height()}
    return out


def expected_access_r(dev: dict, term: str, pdk: dict) -> float:
    """Expected device-access resistance at default PCell options, for the allocation weights only.
    gate: BSIM4 distributed gate resistance with contacts on both ends (ngcon=2):
          Rsh_poly * W_f / (12 * L * nf)  (BSIM4 manual, Rgeltd with XGW = XGL = 0)  + poly contacts;
    s/d : licon contacts along the finger in parallel (pitch 0.34 um assumed for the count)."""
    W, L, nf = dev["W_um"], dev["L_um"], dev["nf"]
    wf = W / nf
    rules = pdk["rules"]
    if term == "g":
        rpc = rules["contacts"]["licon_poly"]["ohm_per_contact"]
        n_pc = max(1, int((L - 0.17) / 0.34) + 1) * 2 * nf
        return rules["poly_sheet_res_ohm_sq"] * wf / (12 * L * nf) + rpc / n_pc
    key = "licon_pdiff" if dev["type"] == "pmos" else "licon_ndiff"
    n_lic = max(1, int((wf - 0.17) / 0.34) + 1) * nf
    return rules["contacts"][key]["ohm_per_contact"] / n_lic


def default_cells(ir: dict) -> dict:
    """Measured default device cells (S3 option library, built before S2 with `src.s3.run --cells-only`):
    per device, the cell's own capacitances between its terminals (Magic, cthresh 0) mapped to circuit
    nets, and its measured access resistance per terminal. Empty if the library has not been built."""
    import re as _re
    from src.s3 import options as O
    out = {}
    types = O.device_types(ir)
    gnd = next(p["name"] for p in ir["ports"] if p["role"] == "ground")
    for tid, t in types.items():
        rec_f = REPO / "outputs" / "S3" / "_cells" / f"{tid}__{O.default_option_id()}" / "record.json"
        if not rec_f.exists():
            continue
        rec = json.loads(rec_f.read_text())
        if not rec.get("ok"):
            continue
        txt = (REPO / rec["pex"]["file"]).read_text()
        caps = []
        for m in _re.finditer(r"^C\S*\s+(\S+)\s+(\S+)\s+([0-9.eE+-]+)([afp]?)", txt, _re.M):
            caps.append((m.group(1), m.group(2), float(m.group(3)) * {"a": 1e-3, "f": 1.0, "p": 1e3, "": 1e15}[m.group(4)]))
        for d in t["devices"]:
            term = next(x for x in ir["devices"] if x["name"] == d)["terminals"]
            net = {"D": term["d"], "G": term["g"], "S": term["s"], "B": term["b"], "VSUBS": gnd}
            out[d] = {"cell": rec["cell"], "caps_fF": [(net.get(a, a), net.get(b, b), c) for a, b, c in caps],
                      "access_ohm": {k: rec["access_resistance_ohm"][k] for k in ("d", "g", "s")}}
    return out


def build_problem(ir, s1, pdk, sizes, eta):
    margins = ir["margins"]
    kinds = {k: v["kind"] for k, v in margins.items()}
    sens = json.loads((s1 / "sensitivity.json").read_text())["table"]
    sr = json.loads((s1 / "sensitivity_r.json").read_text())
    devs = {d["name"]: d for d in ir["devices"]}
    lay = pdk["layers"]
    cg1 = lay["metal1"]["cap_to_substrate_F_per_um_single"] * 1e15     # fF/um
    cc1 = lay["metal1"]["coupling_F_per_um_at_min_spacing"] * 1e15     # fF/um
    r1 = lay["metal1"]["res_ohm_per_um_at_min_width"]                  # ohm/um
    pins = {}
    for d in ir["devices"]:
        for t in ("d", "g", "s"):
            pins.setdefault(d["terminals"][t], []).append(d["name"])
    unit = {d: (s["w_um"] + s["h_um"]) / 2 for d, s in sizes.items()}   # half perimeter of the PCell
    L_est = {n: sum(unit[d] for d in ds) for n, ds in pins.items()}   # one device-crossing stub per pin
    # what the default device cells themselves put on each element (measured, S3 library), so that the
    # expected need -- and the share S3 may use -- includes the cells and not only the wiring
    cells = default_cells(ir)
    acg = {p["name"] for p in ir["ports"] if p["role"] in ("supply", "ground")} | \
          {x for s_ in ir.get("internal_sources", []) for x in (s_["p"], s_["n"])}
    cell_need: dict = {}   # element label -> {device: fF}
    for d, c in cells.items():
        for a_, b_, f in c["caps_fF"]:
            if a_ == b_ or (a_ in acg and b_ in acg):
                continue
            if a_ in acg or b_ in acg:
                lab = b_ if a_ in acg else a_
            else:
                lab = next((l for l in sens if "~" in l and set(l.split("~")) == {a_, b_}), None)
            if lab in sens:
                cell_need.setdefault(lab, {}).setdefault(d, 0.0)
                cell_need[lab][d] += f
    elements, rates = [], {}
    for label, row in sens.items():
        if "~" in label:
            a, b = label.split("~")
            w = COUPLE_FRACTION * min(L_est.get(a, 0), L_est.get(b, 0)) * cc1
            kind, targets, units = "coupling", [a, b], "fF"
        else:
            w = L_est.get(label, 0) * cg1
            kind, targets, units = "net_capacitance", [label], "fF"
        w_wire = w
        w_cell = sum(cell_need.get(label, {}).values())
        w = w_wire + w_cell
        if w <= 0:
            continue
        rates[label] = {k: B.harmful_rate(kinds.get(k, "min"), row[k]["linear_per_fF"]) for k in row if k in margins}
        elements.append({"id": label, "kind": kind, "targets": targets, "units": units, "w": w,
                         "w_parts": {"wiring": w_wire, "device_cells": w_cell,
                                     "device_cells_by_device": cell_need.get(label, {})},
                         "w_basis": f"{'coupling' if kind == 'coupling' else 'route'} estimate "
                                    f"{w_wire / (cc1 if kind == 'coupling' else cg1):.1f} um of met1"
                                    + (f" + {w_cell:.3g} fF inside the default device cells" if w_cell else "")})
    for gid, row in sr["groups"].items():
        members = [m.split(".") for m in row["members"]]
        per = dict(row.get("per_ohm_used") or row["linear_per_ohm"])   # SPICE-based where S1 measured it
        r = {k: B.harmful_rate(kinds.get(k, "min"), v) for k, v in per.items() if k in margins}
        for k, v in (row.get("dc_saturation") or {}).items():
            r[k] = -v["slope_V_per_ohm"]   # V of headroom lost per ohm (only negative slopes are stored)
        d0, t0 = members[0]
        measured = d0 in cells
        acc = cells[d0]["access_ohm"][t0] if measured else expected_access_r(devs[d0], t0, pdk)
        w = acc + unit[d0] * r1
        rates[gid] = r
        elements.append({"id": gid, "kind": "terminal_resistance", "targets": row["members"], "units": "ohm", "w": w,
                         "w_parts": {"device_cells": acc, "wiring": unit[d0] * r1},
                         "w_basis": f"per member: {'measured default-cell' if measured else 'estimated'} access "
                                    f"{acc:.3g} ohm + {unit[d0]:.1f} um met1"})
    constraints = []
    for k in SPECS:
        if k in margins:
            constraints.append({"id": k, "b": eta * margins[k]["margin"], "margin": margins[k]["margin"],
                                "units": margins[k]["units"], "a": {e["id"]: rates[e["id"]].get(k, 0.0) for e in elements}})
    for d, m0 in sr["dc_saturation_margin_V"].items():
        constraints.append({"id": f"sat_{d}", "b": eta * m0, "margin": m0, "units": "V",
                            "a": {e["id"]: rates[e["id"]].get(f"sat_{d}", 0.0) for e in elements}})
    return elements, constraints, {"pins": pins, "L_est_um": L_est, "unit_um": unit,
                                   "default_cells_used": sorted({c["cell"] for c in cells.values()})}


def hierarchy_split(ir, elements, x, geo, pdk):
    """N1: push net budgets down to blocks. A net's capacitance budget is shared between the blocks
    that touch it (their internal wiring to the port) and the top-level route between blocks, in
    proportion to the expected wiring of each part (ASSUMPTION: one device-crossing stub per pin inside a
    block; the top-level route needs one stub per extra block)."""
    blk_of = {}
    for b in ir["hierarchy"]["blocks"]:
        for d in b["devices"]:
            blk_of[d] = b["name"]
    cg1 = pdk["layers"]["metal1"].get("cap_worst_F_per_um", pdk["layers"]["metal1"]["cap_to_substrate_F_per_um_single"]) * 1e15
    nets = {}
    for e in elements:
        if e["kind"] != "net_capacitance" or e["id"] not in x:
            continue
        n = e["id"]
        devs = geo["pins"].get(n, [])
        by_blk = {}
        for d in devs:
            by_blk.setdefault(blk_of.get(d, "unassigned"), 0.0)
            by_blk[blk_of.get(d, "unassigned")] += geo["unit_um"][d]
        top_w = (len(by_blk) - 1) * (sum(by_blk.values()) / max(1, len(devs))) if len(by_blk) > 1 else 0.0
        tot = sum(by_blk.values()) + top_w
        shares = {blk: x[n] * v / tot for blk, v in by_blk.items()}
        top = x[n] * top_w / tot
        route = top if top > 0 else x[n]   # what the routing of this net may add (top level, or inside the block)
        nets[n] = {"budget_fF": x[n], "devices": sorted(set(devs)),
                   "block_port_fF": shares, "top_level_fF": top,
                   "route_budget_fF": route, "max_route_length_metal1_um": route / cg1,
                   "note": None if top > 0 else "single block: the whole budget is internal to it"}
    term = {}
    for e in elements:
        if e["kind"] == "terminal_resistance" and e["id"] in x:
            d, t = e["targets"][0].split(".")
            term[e["id"]] = {"block": blk_of.get(d), "members": e["targets"], "terminal": t,
                             "budget_ohm_each": x[e["id"]]}
    blocks = {}
    for n, h in nets.items():
        for blk, v in h["block_port_fF"].items():
            blocks.setdefault(blk, {"ports_fF": {}, "terminals_ohm": {}})["ports_fF"][n] = v
    for k, v in term.items():
        blocks.setdefault(v["block"], {"ports_fF": {}, "terminals_ohm": {}})["terminals_ohm"][k] = v["budget_ohm_each"]
    return {"nets": nets, "terminals": term, "blocks": blocks,
            "check_sum_equals_budget": all(abs(sum(h["block_port_fF"].values()) + h["top_level_fF"] - h["budget_fF"])
                                           <= 1e-9 * max(1, h["budget_fF"]) for h in nets.values())}


def deck_with_budgets(txt: str, ir: dict, caps: list, res: list) -> str:
    dut = ir["subckt"]
    gnd = next(p["name"] for p in ir["ports"] if p["role"] == "ground")
    for d, t, r in res:
        txt = resistance.deck_with_res(txt, dut, d, t, r)
    lines = []
    for i, (a, b, c) in enumerate(caps):
        lines.append(f"Cbud_s2_{i} {a} {b or gnd} {c:.6g}f\n")
    pat = re.compile(rf"^(\.subckt\s+{re.escape(dut)}\b[^\n]*\n)", re.M)
    return pat.sub(lambda m: m.group(1) + "".join(lines), txt, count=1)


def run_scenarios(s0, ir, scen: dict, work: Path, workers: int = 4) -> dict:
    """scen: {name: (kind, caps, res)} with kind in ac | noise | op | opmeas. Each scenario is one
    ngspice run in its own folder. Returns {name: measurements or None if the run failed}."""
    tb = s0 / "tb"
    src = {"ac": "diso_amp_AC.spice", "noise": "diso_amp_NOISE.spice", "op": "diso_amp_OP.spice",
           "opmeas": "diso_amp_OP.spice"}
    jobs = []
    for name, (kind, caps, res) in scen.items():
        wd = work / name
        txt = deck_with_budgets((tb / src[kind]).read_text(), ir, caps, res)
        if kind == "op":
            wd.mkdir(parents=True, exist_ok=True)
            (wd / "op_src.spice").write_text(txt)
            txt = opmod.op_deck(wd / "op_src.spice", ir["devices"])
        jobs.append((name, kind, txt, wd))

    def one(j):
        name, kind, txt, wd = j
        r = run_ngspice_text(txt, wd, kind)
        if r["rc"] != 0 or r.get("numerical_warnings"):
            return name, None
        if kind == "op":
            o = resistance._sat_from_log((wd / "op.log").read_text())
            return name, o if len(o["vds_minus_vdsat_V"]) == len(ir["devices"]) else None
        return name, r["meas"] or None

    with ThreadPoolExecutor(max_workers=workers) as ex:
        return dict(ex.map(one, jobs))


def resolve_eta(cli_eta, pkg: dict) -> tuple[float, str]:
    """eta: command line > package key 'eta' > ETA_DEFAULT; the source is recorded in the outputs."""
    if cli_eta is not None:
        eta, src = float(cli_eta), "command line"
    elif "eta" in pkg:
        eta, src = float(pkg["eta"]), "package key 'eta'"
    else:
        eta, src = ETA_DEFAULT, "ETA_DEFAULT"
    if not 0.0 < eta <= 1.0:
        raise ValueError(f"eta must be in (0, 1], got {eta} ({src})")
    return eta, src


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package")
    ap.add_argument("--eta", type=float, default=None,
                    help="fraction of each margin given to layout; default: package key 'eta', else ETA_DEFAULT")
    ap.add_argument("--no-spice", action="store_true")
    a = ap.parse_args(argv)
    pkg = load_package(REPO / a.package)
    design = pkg["design"]
    eta, eta_source = resolve_eta(a.eta, pkg)
    s0, s1 = REPO / "outputs" / "S0" / design, REPO / "outputs" / "S1" / design
    out = REPO / "outputs" / "S2" / design
    (out / "plots").mkdir(parents=True, exist_ok=True)
    pdk_f = REPO / "outputs" / "S2" / "pdk" / "parasitics.json"
    ir = json.loads((s0 / "circuit_ir.json").read_text())
    pdk = json.loads(pdk_f.read_text())
    intent = json.loads((s1 / "intent.json").read_text())
    currents = json.loads((s1 / "currents.json").read_text())
    op = json.loads((s1 / "operating_point.json").read_text())["devices"]
    sizes = device_sizes(s0)
    gates = {}

    elements, constraints, geo = build_problem(ir, s1, pdk, sizes, eta)
    # D6 metric, before any layout: the fraction of each margin a compact default layout would use
    expected_use = {c["id"]: {"use_at_expected_need": sum(c["a"].get(e["id"], 0.0) * e["w"] for e in elements),
                              "margin": c["margin"],
                              "fraction_of_margin": sum(c["a"].get(e["id"], 0.0) * e["w"] for e in elements) / c["margin"]
                              if c["margin"] else None} for c in constraints}
    gates["G2.0_expected_layout_use (info)"] = {
        "pass": None, "checks": expected_use, "default_cells_used": geo["default_cells_used"],
        "note": "fraction of each margin that a compact layout with the default device cells would use (sum of "
                "rate x expected need); above eta the budgets fall below the expected need"}
    alloc = B.allocate(elements, constraints)
    lp = B.lp_first_round(elements, constraints)
    t1 = alloc["rounds"][0]["t"] if alloc["rounds"] else None
    used = B.check(alloc["x"], constraints)
    alloc2 = B.allocate(elements, constraints)  # determinism
    gates["G2.3_allocation"] = {
        "pass": bool(alloc["rounds"]) and t1 > 0 and all(u["ok"] for u in used) and lp.get("success", False)
                and abs(lp["t"] - t1) <= 1e-6 * t1 and alloc2["x"] == alloc["x"],
        "t_round1": t1, "lp_round1": lp, "rounds": alloc["rounds"], "constraint_use": used,
        "reproducible": alloc2["x"] == alloc["x"]}
    ref = B.refine(elements, constraints, alloc["x"])
    gates["G2.3_allocation"]["phase2_refine"] = {"success": ref["success"], "message": ref.get("message"),
                                                  "delta": ref.get("delta"),
                                                  "constraint_use": B.check(ref["x"], constraints)}
    gates["G2.3_allocation"]["pass"] = gates["G2.3_allocation"]["pass"] and ref["success"]
    x = ref["x"]
    by_id = {e["id"]: e for e in elements}
    bud = []
    for e in elements:
        rec = {k: e[k] for k in ("id", "kind", "targets", "units", "w", "w_basis", "w_parts")}
        if e["id"] in x:
            rnd = next(r for r in alloc["rounds"] if e["id"] in r["frozen"])
            rec.update({"budget": x[e["id"]], "budget_maxmin": alloc["x"][e["id"]],
                        "multiple_of_expected": x[e["id"]] / e["w"], "binding": rnd["binding"],
                        "margin_used": {c["id"]: c["a"].get(e["id"], 0.0) * x[e["id"]] for c in constraints
                                        if c["a"].get(e["id"], 0.0) > 0}})
        else:
            rec.update({"budget": None, "status": "unconstrained by the specs (consumes no margin in any check)"})
        bud.append(rec)
    budgets_doc = {"design": design, "eta": eta, "eta_source": eta_source, "eta_note": "ASSUMPTION (accepted): fraction of each margin given to layout",
                   "expected_layout_use": expected_use, "default_cells_used": geo["default_cells_used"],
                   "elements": bud, "constraints": [{k: c[k] for k in ("id", "b", "margin", "units")} for c in constraints],
                   "method": "max-min fair progressive filling (budgets.allocate), then proportional-fairness refinement "
                             "keeping >= 95 % of every max-min budget (budgets.refine)",
                   "rates": {c["id"]: c["a"] for c in constraints}}
    write_json(out / "budgets.json", budgets_doc)

    # verification (H1): for every check, insert at their full budget all the parasitics that are
    # harmful for it (those that help it are left out: a layout may not realise them), simulate, and
    # require the margin used to stay within eta*margin (+TOL_VERIFY for first-order model error) and
    # the spec to stay met. If a check exceeds it, the budgets of its elements are scaled down by the
    # measured ratio and the check is repeated (closure iteration, at most CLOSURE_ITERS).
    drive = ac_drive(s0, ir)
    base_lin = linear.evaluate(ir, op, drive=drive)
    by_kind = {e["id"]: e for e in elements}

    def parts(ids, xx):
        caps_, res_ = [], []
        for k in ids:
            e = by_kind[k]
            if e["kind"] == "net_capacitance":
                caps_.append((e["targets"][0], None, xx[k]))
            elif e["kind"] == "coupling":
                caps_.append((e["targets"][0], e["targets"][1], xx[k]))
            else:
                res_ += [(*m.split("."), xx[k]) for m in e["targets"]]
        return caps_, res_

    def kind_of(cid):
        return "noise" if cid == "vnoise_nv_rthz" else ("op" if cid.startswith("sat_") else "ac")

    ach = ir["achieved"]
    lim = {k: v["limit"] for k, v in ir["margins"].items()}
    ver = {"method": "per check: harmful elements only, at full budget; closure iteration if over eta*margin",
           "tolerance": TOL_VERIFY, "iterations": []}
    xv = dict(x)
    if not a.no_spice:
        base = run_scenarios(s0, ir, {"base_ac": ("ac", [], []), "base_noise": ("noise", [], []),
                                      "base_op": ("op", [], [])}, out / "work" / "verify" / "base")
        for it in range(CLOSURE_ITERS + 1):
            scen = {}
            for c in constraints:
                ids = [k for k, v in c["a"].items() if v > 0 and k in xv]
                if ids:
                    caps_, res_ = parts(ids, xv)
                    scen[c["id"]] = (kind_of(c["id"]), caps_, res_)
            r = run_scenarios(s0, ir, scen, out / "work" / "verify" / f"iter{it}")
            rows, over = [], {}
            for c in constraints:
                if c["id"] not in scen:
                    continue
                m = r.get(c["id"])
                if c["id"].startswith("sat_"):
                    d_ = c["id"][4:]
                    now = None if not m or not base["base_op"] else m["vds_minus_vdsat_V"].get(d_)
                    b0 = base["base_op"]["vds_minus_vdsat_V"][d_] if base["base_op"] else None
                    use = None if now is None or b0 is None else b0 - now
                    meets = now is not None and now > 0
                else:
                    bk = base["base_noise"] if c["id"] == "vnoise_nv_rthz" else base["base_ac"]
                    now = None if not m else m.get(c["id"])
                    b0 = None if not bk else bk.get(c["id"])
                    kind = ir["margins"][c["id"]]["kind"]
                    use = None if now is None or b0 is None else ((b0 - now) if kind == "min" else (now - b0))
                    meets = now is not None and ((now >= lim[c["id"]]) if kind == "min" else (now <= lim[c["id"]]))
                pred = sum(c["a"].get(k, 0.0) * xv[k] for k in xv if c["a"].get(k, 0.0) > 0)
                ok = use is not None and meets and use <= c["b"] * (1 + TOL_VERIFY)
                rows.append({"check": c["id"], "margin": c["margin"], "allowed_eta_margin": c["b"],
                             "first_order_predicted_use": pred, "spice_use": use, "value_now": now,
                             "spice_use_frac_of_margin": None if use is None else use / c["margin"],
                             "meets_spec": meets, "ok": ok, "n_elements": len(scen[c["id"]][1]) + len(scen[c["id"]][2])})
                if use is not None and use > c["b"] * (1 + TOL_VERIFY) and use > 0:
                    over[c["id"]] = c["b"] / use
            ver["iterations"].append({"iteration": it, "rows": rows,
                                      "scaled": {k: v for k, v in over.items()}})
            if not over:
                break
            for cid, f in over.items():   # closure: shrink every element that is harmful for the failing check
                c = next(cc for cc in constraints if cc["id"] == cid)
                for k, v in c["a"].items():
                    if v > 0 and k in xv:
                        xv[k] *= 0.98 * f
        last = ver["iterations"][-1]["rows"]
        gates["G2.5_spice_budget_verification"] = {
            "pass": bool(last) and all(rr["ok"] for rr in last) and all(
                rr["spice_use"] is not None for rr in last),
            "iterations": len(ver["iterations"]), "rows": last,
            "closure_scaled_elements": sorted(k for k in x if abs(xv[k] - x[k]) > 1e-12 * max(1, x[k]))}
        # realistic mix (every budget, helpful ones included): reported, not gated
        caps_all, res_all = parts(list(xv), xv)
        mix = run_scenarios(s0, ir, {"mix_ac": ("ac", caps_all, res_all), "mix_noise": ("noise", caps_all, res_all),
                                     "mix_op": ("op", caps_all, res_all)}, out / "work" / "verify" / "mix")
        ver["all_budgets_at_once"] = mix
        ver["base"] = base
    else:
        gates["G2.5_spice_budget_verification"] = {"pass": None, "note": "--no-spice"}
    # write back the verified (possibly scaled) budgets
    for rec in bud:
        if rec.get("budget") is not None and abs(xv[rec["id"]] - rec["budget"]) > 1e-12 * max(1, rec["budget"]):
            rec["budget_first_order"] = rec["budget"]
            rec["budget"] = xv[rec["id"]]
            rec["multiple_of_expected"] = xv[rec["id"]] / rec["w"]
            rec["margin_used"] = {c["id"]: c["a"].get(rec["id"], 0.0) * xv[rec["id"]] for c in constraints
                                  if c["a"].get(rec["id"], 0.0) > 0}
            rec["closure_note"] = "scaled down in S2 verification (closure iteration)"
    write_json(out / "budgets.json", budgets_doc)
    caps, res = parts(list(xv), xv)
    lin = linear.evaluate(ir, op, extra_c=[(a_, b_, c_ * 1e-15) for a_, b_, c_ in caps], extra_r=res, drive=drive)
    pred_first = {c["id"]: sum(c["a"].get(k, 0.0) * v for k, v in xv.items()) for c in constraints}
    ver["budget_point"] = {"caps_fF": caps, "res_ohm": res}
    ver["linear_model"] = {"base": base_lin, "at_budget": lin, "first_order_use": pred_first}
    gates["G2.4_linear_all_budgets_at_once"] = {
        "pass": None, "note": "reported: first-order sum vs exact linear model with every budget inserted",
        "compare": {k: {"first_order_use": pred_first.get(k),
                        "linear_model_use": (base_lin[k] - lin[k]) if ir["margins"][k]["kind"] == "min" else (lin[k] - base_lin[k])}
                    for k in ("gain_db", "gbw_mhz", "pm_deg")}}
    write_json(out / "verification.json", ver)

    hier = hierarchy_split(ir, elements, xv, geo, pdk)
    write_json(out / "hierarchy.json", hier)
    gates["G2.6_hierarchy_sums"] = {"pass": hier["check_sum_equals_budget"]}

    offset = json.loads((s1 / "sensitivity_r.json").read_text()).get("mismatch_offset")
    cons = R.build(ir, intent, budgets_doc, pdk, currents, hier, sizes, offset)
    names = {n["name"] for n in ir["nets"]} | {d["name"] for d in ir["devices"]} | {"all devices"} | \
            {f"{d['name']}.{t}" for d in ir["devices"] for t in ("d", "g", "s")} | {p_["name"] for p_ in ir["ports"]}
    unresolved = [c["id"] for c in cons for t in c["targets"] if t not in names]
    no_units = [c["id"] for c in cons if c["value"] is not None and not c["units"]]
    no_deriv = [c["id"] for c in cons if not c["derived_from"]]
    gates["G2.1_names_resolve"] = {"pass": not unresolved, "unresolved": unresolved}
    gates["G2.2_units_and_provenance"] = {"pass": not no_units and not no_deriv, "missing_units": no_units,
                                          "missing_derived_from": no_deriv,
                                          "not_evaluated": [c["id"] for c in cons if c["status"] == "not_evaluated"]}
    write_json(out / "constraints.json", {"design": design, "constraints": cons,
                                          "counts": {k: sum(1 for c in cons if c["class"] == k)
                                                     for k in sorted({c["class"] for c in cons})}})


    # plots
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axs = plt.subplots(1, 3, figsize=(15, 4.6), gridspec_kw={"width_ratios": [1.1, 1.1, 1.4]})
        for ax, kind, unit_ in ((axs[0], "net_capacitance", "fF"), (axs[1], "coupling", "fF")):
            es = [e for e in bud if e["kind"] == kind and e.get("budget") is not None]
            ax.barh([e["id"] for e in es], [e["budget"] for e in es], color="#4C78A8")
            ax.barh([e["id"] for e in es], [e["w"] for e in es], color="none", edgecolor="#E45756", hatch="//",
                    label="expected need (weight)")
            ax.set_xlabel(unit_); ax.set_title(f"{design}: {kind.replace('_', ' ')} budgets"); ax.legend(fontsize=7)
            ax.set_xscale("log")
            from matplotlib.ticker import LogLocator, NullFormatter, LogFormatterSciNotation
            ax.xaxis.set_major_locator(LogLocator(base=10)); ax.xaxis.set_major_formatter(LogFormatterSciNotation())
            ax.xaxis.set_minor_formatter(NullFormatter())
        es = sorted([e for e in bud if e["kind"] == "terminal_resistance" and e.get("budget") is not None],
                    key=lambda e: e["budget"])
        axs[2].barh([e["id"] for e in es], [e["budget"] for e in es], color="#54A24B")
        axs[2].barh([e["id"] for e in es], [e["w"] for e in es], color="none", edgecolor="#E45756", hatch="//")
        axs[2].set_xscale("log"); axs[2].set_xlabel("ohm"); axs[2].set_title("series-R budgets per device terminal")
        fig.tight_layout(); fig.savefig(out / "plots" / "budgets.png", dpi=110); plt.close(fig)
        if ver.get("iterations"):
            fig, ax = plt.subplots(figsize=(9, 3.8))
            rows = [r for r in ver["iterations"][-1]["rows"] if r["spice_use"] is not None]
            xs = range(len(rows))
            ax.bar([i - 0.2 for i in xs], [r["first_order_predicted_use"] / r["margin"] for r in rows], 0.4,
                   label="predicted (first order)")
            ax.bar([i + 0.2 for i in xs], [r["spice_use_frac_of_margin"] for r in rows], 0.4,
                   label="SPICE, harmful budgets inserted")
            ax.axhline(eta, color="grey", ls="--", lw=1, label=f"eta = {eta}")
            ax.axhline(1.0, color="#E45756", lw=1, label="whole margin")
            ax.set_xticks(list(xs)); ax.set_xticklabels([r["check"] for r in rows], rotation=20, ha="right")
            ax.set_ylabel("fraction of margin used"); ax.set_title(f"{design}: budget verification"); ax.legend(fontsize=8)
            fig.tight_layout(); fig.savefig(out / "plots" / "budget_verification.png", dpi=110); plt.close(fig)
    except Exception as e:  # evidence, not a gate
        gates["G2.3_allocation"]["plot_error"] = str(e)

    prov = provenance([s0 / "circuit_ir.json", s1 / "sensitivity.json", s1 / "sensitivity_r.json", s1 / "intent.json",
                       pdk_f, REPO / a.package])
    report = {"design": design, "eta": eta, "gates": gates,
              "all_pass": all(g.get("pass") in (True, None) for g in gates.values()), "provenance": prov}
    write_json(out / "s2_report.json", report)
    for k in sorted(gates):
        g = gates[k]
        print(f"{k:38s} {'PASS' if g.get('pass') else ('INFO' if g.get('pass') is None else 'FAIL')}")
    print("S2", "PASS" if report["all_pass"] else "FAIL", "->", rel(out))
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
