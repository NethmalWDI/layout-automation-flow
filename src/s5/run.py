"""S5 — placement (plan v4, Phase 3; routing follows in Phase 4).

Inputs: outputs/S4/<d>/blocks.json (signed-off block variants: bounding box, axis, pins), outputs/S0/<d>/
circuit_ir.json (designer rows, if any), outputs/S2/<d>/constraints.json (route.max_length.<net>.metal3).

Every candidate of src/s5/place.py is costed twice: budget-aware (area + S2's wire budgets) and area-only (the
AICL-like baseline). Each winner's blocks are assembled into one GDS (Magic places each block's bounding box where
the placement puts it) and checked with DRC: unrouted, it must already be clean (spacing between rings and wells).

usage (inside layout-s0s3): python3 -m src.s5.run inputs/<d>/package.yaml
Writes outputs/S5/<d>/: placement.json, s5_report.json (G5.1, G5.5), placed_<rule>/ (GDS, DRC, picture).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from src.common import pcell
from src.common.hygiene import fresh_output_dir, gate_exit, new_run_id
from src.common.tools import REPO, TOOL_ENV, provenance, rel, write_json
from src.s0.ingest import load_package
from src.s5 import place as P

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


def assemble(name: str, pl: dict, blocks: dict, out: Path) -> dict:
    """The placed (unrouted) blocks as one GDS: each block's bounding box at the placement's box, flipped upside
    down ('v') when the placement flips it."""
    out.mkdir(parents=True, exist_ok=True)
    c = ["drc off", "snap internal"]
    vmap = {b: next(v for v in blocks[b]["variants"] if v["id"] == p["variant"]) for b, p in pl["blocks"].items()}
    for v in vmap.values():
        c.append(f"gds read {REPO / v['build']['gds']}")
    c.append(f"load {name} -silent")
    for b, p in pl["blocks"].items():
        x0, y0 = p["bbox"][0], p["bbox"][1]
        c += [f"box {x0:.4f}um {y0:.4f}um {x0:.4f}um {y0:.4f}um", f"getcell {vmap[b]['cell']}" + (" v" if p["flip"] else "")]
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
    pm = [bs[b]["bbox"] for b in bs if blocks[b]["type"] == "pmos"]
    nm = [bs[b]["bbox"] for b in bs if blocks[b]["type"] != "pmos"]
    above = not pm or not nm or min(b[1] for b in pm) >= max(b[3] for b in nm)
    axis = {b: bs[b]["axis_x"] for b in bs if blocks[b]["symmetric"]}
    return {"min_separation_um": round(min(sep), 4) if sep else None,
            "separation_ok": not sep or min(sep) >= min(P.ROW_GAP, P.BLOCK_GAP) - 1e-6,
            "pmos_above_nmos": above, "symmetric_axes": axis,
            "axes_ok": all(abs(x) <= P.AXIS_TOL for x in axis.values())}


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
    cands = P.enumerate_candidates(blocks, max_len, drow)
    fresh_output_dir(out)
    out.mkdir(parents=True, exist_ok=True)
    best = {r: min(range(len(cands)), key=lambda i: (cands[i]["cost"][r], i)) for r in RULES}
    res = {}
    for r in RULES:
        c = cands[best[r]]
        res[r] = {"index": best[r], "cost": c["cost"], "placement": c["placement"],
                  "legal": legal(c["placement"], blocks),
                  "assembled": assemble(f"{design}_placed_{r}", c["placement"], blocks, out / f"placed_{r}")}
    ident = {"run_id": new_run_id(), "design": design,
             "s4_run_id": json.loads((s4 / "blocks.json").read_text()).get("run_id")}
    write_json(out / "placement.json", {
        **ident, "constants": {"ROW_GAP": P.ROW_GAP, "BLOCK_GAP": P.BLOCK_GAP, "LAMBDA": P.LAMBDA, "MU": P.MU},
        "max_length_metal3_um": max_len, "designer_rows": drow, "n_candidates": len(cands),
        "chosen": res,
        "candidates": [{"rows": c["placement"]["rows"],
                        "choice": {b: [p["variant"], p["flip"]] for b, p in c["placement"]["blocks"].items()},
                        **{k: c["cost"][k] for k in ("area_um2", "budget_aware", "area_only", "u")}} for c in cands]})
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
            "same_placement": ba["index"] == ao["index"]},
        "G5.2_G5.4_routing": {"pass": None, "note": "routing, top-level DRC/LVS and the route rules: plan v4 Phase 4"},
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
