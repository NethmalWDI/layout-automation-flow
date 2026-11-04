"""S5 — placement and routing (plan v4, Phases 3 and 4).

Inputs: outputs/S4/<d>/blocks.json (signed-off block variants: bounding box, axis, pins), outputs/S0/<d>/
circuit_ir.json (designer rows, if any), outputs/S0/<d>/ref/<d>_layout.spice (the layout view: ports and net names),
outputs/S2/<d>/constraints.json (route.*), outputs/S3/<d>/device_decisions.json (the cells' access R).

Every candidate of src/s5/place.py is costed twice: budget-aware (area + S2's wire budgets) and area-only (the
AICL-like baseline). Each winner is
  * assembled unrouted and checked with DRC (spacing between rings and wells), then
  * routed by src/s5/route.py, drawn, and signed off: DRC (G5.2) and LVS against the layout view with the drawn finger
    counts (G5.3), both with negative controls, and every route.* rule of S2 checked on the wires (G5.4).
Both are routed by the same router, so H5 compares them on equal terms.

usage (inside layout-s0s3): python3 -m src.s5.run inputs/<d>/package.yaml   (or ./flow run <d> --stage S5)
Writes outputs/S5/<d>/: placement.json (the two winners), candidates.json.gz (every candidate with its cost terms),
s5_report.json (G5.1-G5.5), placed_<rule>/ and routed_<rule>/ (GDS, DRC, LVS, picture).
"""
from __future__ import annotations

import argparse
import gzip
import json
import re
import subprocess
import sys
from pathlib import Path

from src.common import pcell
from src.common.hygiene import fresh_output_dir, gate_exit, new_run_id
from src.common.tools import REPO, TOOL_ENV, provenance, rel, write_json
from src.s0.ingest import load_package
from src.s5 import place as P
from src.s5 import route as R
from src.s4.run import layout_options

RULES = ("budget_aware", "area_only")


def load_blocks(s4: Path) -> dict:
    bj = json.loads((s4 / "blocks.json").read_text())
    out = {}
    for b in bj["blocks"]:
        ok = [v for v in b["variants"] if v.get("ok")]
        if not ok:
            raise RuntimeError(f"block {b['name']} has no signed-off variant")
        out[b["name"]] = {"type": b["type"], "body": b["body"], "devices": b["devices"],
                          "symmetric": any(v.get("symmetry") for v in ok), "variants": ok}
    return out


def designer_rows(ir: dict, blocks: dict) -> dict:
    rows = (ir.get("hierarchy") or {}).get("floorplan_rows") or []
    where = {d: i for i, r in enumerate(rows) for d in r}
    return {b: min(where[d] for d in v["devices"]) for b, v in blocks.items() if all(d in where for d in v["devices"])}


def assemble(name: str, pl: dict, blocks: dict, out: Path, extra: list | None = None) -> dict:
    """The placed blocks as one GDS: each block's bounding box at the placement's box, flipped upside down ('v')
    when the placement flips it; `extra` Magic commands (the routes) are drawn in the top cell."""
    out.mkdir(parents=True, exist_ok=True)
    c = ["drc off", "snap internal"]
    vmap = {b: next(v for v in blocks[b]["variants"] if v["id"] == p["variant"]) for b, p in pl["blocks"].items()}
    for v in vmap.values():
        c.append(f"gds read {REPO / v['build']['gds']}")
    c.append(f"load {name} -silent")
    for b, p in pl["blocks"].items():
        x0, y0 = p["bbox"][0], p["bbox"][1]
        c += [f"box {x0:.4f}um {y0:.4f}um {x0:.4f}um {y0:.4f}um", f"getcell {vmap[b]['cell']}" + (" v" if p["flip"] else "")]
    c += ["tech unlock *"] + (extra or []) + ["tech revert"]
    c += [f"save {name}", f"gds write {name}", "quit -noprompt"]
    (out / "assemble.tcl").write_text("\n".join(c) + "\n")
    r = subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", pcell.MAGICRC, str(out / "assemble.tcl")],
                       cwd=out, env=TOOL_ENV, capture_output=True, text=True, timeout=600)
    (out / "assemble_magic.log").write_text(r.stdout + r.stderr)
    gds = out / f"{name}.gds"
    res = {"gds": rel(gds) if gds.exists() else None}
    if gds.exists():
        res["drc"] = pcell.drc(gds, name, out / "drc")
        res["png"] = pcell.png(gds, out / f"{name}.png")
        import klayout.db as kdb
        ly = kdb.Layout()
        ly.read(str(gds))
        bb = ly.top_cell().dbbox()
        res["gds_bbox"] = [round(bb.left, 3), round(bb.bottom, 3), round(bb.right, 3), round(bb.top, 3)]
    return res


def top_ref(ref_spice: str, pl: dict, blocks: dict, s4: Path, nmap: dict | None = None) -> str:
    """The layout view's netlist with each device's nf set to the fingers drawn (S3's option, split by S4's units);
    W, L and m stay. nf is read from the chosen S4 variant's own LVS reference, and so are its dummies (plan v4
    Phase 8), added with every terminal on their body net in the layout view's name."""
    nmap = nmap or {}
    nf, dummies = {}, []
    for b, p in pl["blocks"].items():
        v = next(v for v in blocks[b]["variants"] if v["id"] == p["variant"])
        for ln in (REPO / v["lvs"]["report"]).parent.parent.joinpath("ref.spice").read_text().splitlines():
            m = re.match(r"^X(\S+)\s.*\bnf=(\d+)", ln)
            t = ln.split()
            if t and t[0].startswith("X") and "_DUMMY" in t[0]:   # a dummy transistor or resistor: its nets up to
                k = next(i for i, x in enumerate(t) if x.startswith("sky130_fd_pr__"))   # the model, in the view's names
                nets = [nmap.get(re.sub(r"_body$", "", x), re.sub(r"_body$", "", x)) for x in t[1:k]]
                dummies.append(" ".join([t[0]] + nets + t[k:]))
            elif m:
                nf[m.group(1)] = int(m.group(2))
    lines = []
    for ln in ref_spice.splitlines():
        t = ln.split()
        if t and t[0][:1] in "Xx" and t[0] in nf:
            ln = re.sub(r"\bnf=\d+", f"nf={nf[t[0]]}", ln)
        if dummies and re.match(r"^\.ends\b", ln):
            lines += dummies
            dummies = []
        lines.append(ln)
    return "\n".join(lines) + "\n"


def lvs_top(gds: Path, design: str, ref_text: str, out: Path) -> dict:
    """Top-level LVS against the layout view (its ports are the top cell's labels), with a negative control: the
    same reference with the first device's L changed by 10 % (at least 0.1 um) must fail."""
    out.mkdir(parents=True, exist_ok=True)

    def run(text, tag):
        f = out / f"ref_{tag}.spice"
        f.write_text(text)
        return subprocess.run(["bash", str(pcell.SCRIPTS / "magic_lvs.sh"), str(gds), design + "_routed", str(f), design,
                               str(out / tag)], env={**TOOL_ENV, "LVS_MODE": "top"}, capture_output=True, text=True,
                              timeout=1200).stdout
    m = re.search(r" L=([0-9.]+)", ref_text)
    bad = ref_text.replace(f" L={m.group(1)}", f" L={float(m.group(1)) + max(0.1, round(0.1 * float(m.group(1)), 3)):g}", 1)
    ok, neg = "LVS_RESULT MATCH" in run(ref_text, "lvs"), "LVS_RESULT FAIL" in run(bad, "lvs_negctl")
    return {"match": ok, "neg_control_rejected": neg, "pass": ok and neg, "report": rel(out / "lvs" / "lvs_report.txt")}


def route_rules(routes: dict, cons: list, nmap: dict, ir: dict, s3_dec: dict, rules: dict) -> dict:
    """G5.4: every route.* rule of S2 checked on the top-level wires. Lengths and parallel runs are the router's own
    geometry; series R is the wires plus their vias, against what is left after S3's cell (the block's internal
    wiring is S6's to extract)."""
    inv = {}
    for k, v in nmap.items():
        inv.setdefault(v, k)
    L = {n: R.lengths(r) for n, r in routes.items()}
    res = {"max_length": {}, "max_parallel": {}, "max_series_R": {}, "symmetric": {}, "not_evaluated": [],
           "covered": "max_length on metal4 enters the metal3+metal4 sum; top-level routing uses no metal1 or metal2, "
                      "so those layers' length and parallel rules have no top-level wire to apply to"}

    def par3(a, b):   # the longest x-overlap of two nets' metal3 runs within two pitches in y
        best = 0.0
        for ya, xa0, xa1 in routes.get(a, {}).get("met3", []):
            for yb, xb0, xb1 in routes.get(b, {}).get("met3", []):
                if abs(ya - yb) <= 2 * R.GRID + 1e-6:
                    best = max(best, min(xa1, xb1) - max(xa0, xb0))
        return max(0.0, best)
    for c in cons:
        cid = c["id"]
        tg = [nmap.get(t, t) for t in c["targets"]]       # S2 names IR nets; the routes carry the layout view's
        if cid.startswith("route.max_length.") and cid.endswith(".metal3"):
            n = tg[0]
            m4 = next(x["value"] for x in cons if x["id"] == f"route.max_length.{c['targets'][0]}.metal4")
            u = (L[n]["metal3"] / c["value"] + L[n]["metal4"] / m4) if n in L else 0.0
            res["max_length"][n] = {"use": round(u, 4), "ok": u <= 1.0, "length_um": L.get(n)}
        elif cid.startswith("route.max_parallel.") and cid.endswith(".metal4"):
            a, b = tg
            run = 0.0
            if a in routes and b in routes:
                sa, sb = routes[a]["spine"], routes[b]["spine"]
                if abs(sa["x"] - sb["x"]) <= 2 * R.GRID + 1e-6:   # beyond two pitches the coupling is ignored (ASSUMPTION)
                    run = max(0.0, min(sa["y"][1], sb["y"][1]) - max(sa["y"][0], sb["y"][0]))
            res["max_parallel"][f"{a}~{b}"] = {"run_um": round(run, 4), "limit_um": c["value"], "ok": run <= c["value"]}
        elif cid.startswith("route.max_parallel.") and cid.endswith(".metal3"):
            a, b = tg
            run = par3(a, b)
            res["max_parallel"][f"{a}~{b}.metal3"] = {"run_um": round(run, 4), "limit_um": c["value"], "ok": run <= c["value"]}
        elif cid.startswith(("route.max_length.", "route.max_parallel.")):
            continue                                       # metal4 lengths in the sum; metal1/metal2 unused (covered)
        elif cid.startswith("route.max_series_R."):
            devs = {d["name"]: d for d in ir["devices"]}
            types = {d: t for t, v in s3_dec.items() for d in v["devices"]}
            worst = None
            for tgt in c["targets"]:
                dn, term = tgt.split(".")
                net = nmap.get(devs[dn]["terminals"][term], devs[dn]["terminals"][term])
                acc = s3_dec[types[dn]]["access_resistance_ohm"][term]
                r = routes.get(net)
                rw = 0.0 if r is None else (rules["layers"]["metal4"]["sheet_res_ohm_sq"] * L[net]["metal4"] / R.WIRE +
                                            rules["layers"]["metal3"]["sheet_res_ohm_sq"] * L[net]["metal3"] / R.WIRE +
                                            len(r["vias"]) * rules["contacts"]["via3"]["ohm_per_contact"])
                left = c["value"] - acc
                if worst is None or rw - left > worst["route_ohm"] - worst["left_ohm"]:
                    worst = {"net": net, "route_ohm": round(rw, 3), "left_ohm": round(left, 3)}
            res["max_series_R"][cid.split("route.max_series_R.")[1]] = {**worst, "ok": worst["route_ohm"] <= worst["left_ohm"]}
        elif cid.startswith("route.symmetric."):
            a, b = tg
            if a in routes and b in routes:
                xa, xb = routes[a]["spine"]["x"], routes[b]["spine"]["x"]
                la, lb = L[a]["metal4"] + L[a]["metal3"], L[b]["metal4"] + L[b]["metal3"]
                ok = abs(xa + xb) <= P.AXIS_TOL and abs(la - lb) <= R.GRID
            else:
                ok, xa, xb = False, None, None
            res["symmetric"][cid] = {"class": c["class"], "x": [xa, xb], "ok": ok}
        elif cid.startswith("route."):
            res["not_evaluated"].append({"id": cid, "class": c["class"], "note": c.get("note")})
    hard_ok = all(v["ok"] for k in ("max_length", "max_parallel", "max_series_R") for v in res[k].values()) and \
        all(v["ok"] for v in res["symmetric"].values() if v["class"] == "hard")
    res["pass"] = hard_ok
    return res


def legal(pl: dict, blocks: dict) -> dict:
    """Separation of every pair of blocks (at least the gap in x or in y), PMOS above NMOS, symmetric blocks on x = 0."""
    bs = pl["blocks"]
    names = list(bs)
    sep = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            A, B = bs[a]["bbox"], bs[b]["bbox"]
            gx = max(B[0] - A[2], A[0] - B[2])
            gy = max(B[1] - A[3], A[1] - B[3])
            sep.append(max(gx, gy))
    # with macros (plan v4 Phase 8) the rows are a macro's own: PMOS above NMOS, and the symmetric blocks on one
    # axis, inside each macro; without, across the layout and on x = 0, as before
    groups = {}
    for b, p in bs.items():
        groups.setdefault(p.get("macro"), []).append(b)
    above, axes_ok, axis = True, True, {}
    for g, mem in groups.items():
        pm = [bs[b]["bbox"] for b in mem if blocks[b]["type"] == "pmos"]
        nm = [bs[b]["bbox"] for b in mem if blocks[b]["type"] != "pmos"]
        above = above and (not pm or not nm or min(b[1] for b in pm) >= max(b[3] for b in nm))
        ax = {b: bs[b]["axis_x"] for b in mem if blocks[b]["symmetric"]}
        axis.update(ax)
        if g is None:                               # no macros: every symmetric block's axis on x = 0
            axes_ok = axes_ok and all(abs(x) <= P.AXIS_TOL for x in ax.values())
        # in a macro, pairs may share a row (the hard outline, plan v4 Phase 8): their axes are reported, not gated
    return {"min_separation_um": round(min(sep), 4) if sep else None,
            "separation_ok": not sep or min(sep) >= min(P.ROW_GAP, P.BLOCK_GAP) - 1e-6,
            "pmos_above_nmos": above, "symmetric_axes": axis, "axes_ok": axes_ok}


def signature(pl: dict) -> list:
    """What makes two placements the same: every block's variant, flip and place."""
    return sorted((b, p["variant"], p["flip"], tuple(p["origin"])) for b, p in pl["blocks"].items())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package")
    a = ap.parse_args(argv)
    pkg = load_package(REPO / a.package)
    design = pkg["design"]
    s0, s2, s4 = (REPO / "outputs" / s / design for s in ("S0", "S2", "S4"))
    out = REPO / "outputs" / "S5" / design
    blocks = load_blocks(s4)
    ir = json.loads((s0 / "circuit_ir.json").read_text())
    cons = json.loads((s2 / "constraints.json").read_text())["constraints"]
    max_len = {c["targets"][0]: c["value"] for c in cons if c["id"].startswith("route.max_length.")
               and c["id"].endswith(".metal3")}
    drow = designer_rows(ir, blocks)
    opts = layout_options(design)
    outline = opts.get("outline_um")
    if opts.get("hierarchy") == "upstream":   # macros per sub-circuit, then the macros (plan v4 Phase 8)
        from src.s5 import macro as M
        chosen = {r: M.hierarchical(design, blocks, max_len, r, outline) for r in RULES}
        cands = []
    else:
        cands = P.enumerate_candidates(blocks, max_len, drow)
        best = {r: min(range(len(cands)), key=lambda i: (cands[i]["cost"][r], i)) for r in RULES}
        chosen = {r: {**cands[best[r]], "index": best[r]} for r in RULES}
    fresh_output_dir(out)
    out.mkdir(parents=True, exist_ok=True)
    ref_spice = (s0 / "ref" / f"{design}_layout.spice").read_text()
    nmap = R.net_map(ir, ref_spice)
    ports = R.ports_of(ref_spice)
    order = [nmap.get(n, n) for n in sorted(max_len, key=lambda n: max_len[n])]   # least budget slack first,
    # in the layout view's names, which the router uses (ibias -> IBIAS; review of plan v4 Phase 7)
    mirrored = [(*(nmap.get(t, t) for t in c["targets"]), c["class"]) for c in cons if c["id"].startswith("route.symmetric.")]
    par_limit = {frozenset(nmap.get(t, t) for t in c["targets"]): c["value"] for c in cons
                 if c["id"].startswith("route.max_parallel.") and c["id"].endswith(".metal4")}
    s3_dec = json.loads((REPO / "outputs" / "S3" / design / "device_decisions.json").read_text())["decisions"]
    rules = json.loads((REPO / "outputs" / "S2" / "pdk" / "parasitics.json").read_text())["rules"]
    res = {}
    for r in RULES:
        c = chosen[r]
        pl = c["placement"]
        res[r] = {"index": c["index"], "cost": c["cost"], "placement": pl, "legal": legal(pl, blocks),
                  "assembled": assemble(f"{design}_placed_{r}", pl, blocks, out / f"placed_{r}")}
        try:
            routes = R.plan_routes(pl, nmap, ports, order, mirrored, par_limit)
        except RuntimeError as e:
            res[r]["routing"] = {"ok": False, "error": str(e)}
            continue
        d = out / f"routed_{r}"
        asm = assemble(f"{design}_routed", pl, blocks, d, R.tcl(routes))
        res[r]["routing"] = {"ok": True, "routes": {n: {k: v for k, v in x.items() if k != "points"} for n, x in routes.items()},
                             "lengths": {n: R.lengths(x) for n, x in routes.items()}, "assembled": asm,
                             "rules": route_rules(routes, cons, nmap, ir, s3_dec, rules)}
        if asm.get("gds"):
            (d / "ref_top.spice").write_text(top_ref(ref_spice, pl, blocks, s4, nmap))
            res[r]["routing"]["lvs"] = lvs_top(REPO / asm["gds"], design, (d / "ref_top.spice").read_text(), d / "lvs")
    ident = {"run_id": new_run_id(), "design": design,
             "s4_run_id": json.loads((s4 / "blocks.json").read_text()).get("run_id")}
    write_json(out / "placement.json", {
        **ident, "constants": {"ROW_GAP": P.ROW_GAP, "BLOCK_GAP": P.BLOCK_GAP, "LAMBDA": P.LAMBDA, "MU": P.MU},
        "max_length_metal3_um": max_len, "designer_rows": drow, "n_candidates": len(cands),
        "chosen": res, "candidates_file": "candidates.json.gz"})
    # every candidate with its cost terms, gzipped: LOADBench's 20 736 made placement.json 17 MB (plan v4 Phase 7)
    with gzip.open(out / "candidates.json.gz", "wt", encoding="utf-8") as fz:
        json.dump({**ident, "candidates": [
            {"rows": c["placement"]["rows"], "choice": {b: [p["variant"], p["flip"]] for b, p in c["placement"]["blocks"].items()},
             **{k: c["cost"][k] for k in ("area_um2", "budget_aware", "area_only", "u")}} for c in cands]}, fz)
    def ok(r):
        L, A = res[r]["legal"], res[r]["assembled"]
        return bool(L["separation_ok"] and L["pmos_above_nmos"] and L["axes_ok"] and (A.get("drc") or {}).get("pass"))
    ba, ao = res["budget_aware"], res["area_only"]
    gates = {
        "G5.1_placement_legal": {"pass": all(ok(r) for r in RULES),
                                 "detail": {r: {**res[r]["legal"], "drc_unrouted": (res[r]["assembled"].get("drc") or {}).get("errors")}
                                            for r in RULES}},
        "G5.5_area_vs_area_only (info)": {
            "pass": None, "budget_aware_area_um2": ba["cost"]["area_um2"], "area_only_area_um2": ao["cost"]["area_um2"],
            "area_ratio": round(ba["cost"]["area_um2"] / ao["cost"]["area_um2"], 4),
            "u_budget_aware": ba["cost"]["u"], "u_area_only": ao["cost"]["u"],
            "same_placement": signature(ba["placement"]) == signature(ao["placement"])},
        **({"G5.6_outline": {
            "pass": all(res[r]["placement"]["bbox"][2] - res[r]["placement"]["bbox"][0] <= outline[0] + 1e-6 and
                        res[r]["placement"]["bbox"][3] - res[r]["placement"]["bbox"][1] <= outline[1] + 1e-6
                        for r in RULES),
            "outline_um": outline,
            "size_um": {r: [round(res[r]["placement"]["bbox"][2] - res[r]["placement"]["bbox"][0], 3),
                            round(res[r]["placement"]["bbox"][3] - res[r]["placement"]["bbox"][1], 3)] for r in RULES},
            "note": "the hard outline of layout.yaml (plan v4 Phase 8): a placement outside it is rejected"}}
           if outline else {}),
        "G5.2_top_DRC": {"pass": all(((res[r].get("routing") or {}).get("assembled") or {}).get("drc", {}).get("pass")
                                     for r in RULES),
                         "detail": {r: (((res[r].get("routing") or {}).get("assembled") or {}).get("drc") or {}).get("errors")
                                    for r in RULES}},
        "G5.3_top_LVS": {"pass": all(((res[r].get("routing") or {}).get("lvs") or {}).get("pass") for r in RULES),
                         "detail": {r: (res[r].get("routing") or {}).get("lvs") for r in RULES}},
        "G5.4_route_rules": {"pass": all(((res[r].get("routing") or {}).get("rules") or {}).get("pass") for r in RULES),
                             "detail": {r: (res[r].get("routing") or {}).get("rules") for r in RULES}},
    }
    prov = provenance([s4 / "blocks.json", s0 / "circuit_ir.json", s2 / "constraints.json", REPO / a.package])
    report = {**ident, "gates": gates, "all_pass": all(g.get("pass") in (True, None) for g in gates.values()),
              "provenance": prov}
    write_json(out / "s5_report.json", report)
    print(f"{len(cands)} candidates")
    for r in RULES:
        c = res[r]
        print(f"  {r:13s} area={c['cost']['area_um2']:8.1f} u={c['cost']['u']} rows={c['placement']['rows']} "
              f"choice={ {b: (p['variant'], p['flip']) for b, p in c['placement']['blocks'].items()} } "
              f"drc={(c['assembled'].get('drc') or {}).get('errors')}")
    for k, g in gates.items():
        print(f"{k:34s} {g.get('pass')}")
    return gate_exit(report["all_pass"])


if __name__ == "__main__":
    sys.exit(main())
