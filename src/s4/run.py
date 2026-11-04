"""S4 — block generation (plan v4, docs/plan_v4_S4_S7.md): S3's chosen cells grouped into signed-off blocks.

Inputs: outputs/S0/<d>/circuit_ir.json (devices, type, body net, S0 blocks), outputs/S1/<d>/s1_report.json (G1.4
matching groups), outputs/S3/<d>/device_decisions.json and the S3 cells (outputs/S3/_cells/), outputs/S2/<d>/
constraints.json (place.latchup_tap_distance).

Blocks (plan, section 2): S1's matching groups first, then S0's blocks with what is left, each split so that a
block holds one device type with one body net. Variants per block:
  * one device: A;
  * two devices of the same type (a matched pair or mirror): AB, the second flipped (mirror-symmetric); and, when
    the chosen cell has an even finger count, ABBA (common centroid, 1-D) and ABAB (interdigitated) from half units:
    S3's option with half the fingers, at the same finger width, built as an S3 cell (outputs/S3/_cells/);
  * more devices, or devices of different sizes: side by side in the S0 order.
A unit too wide for S2's latch-up distance even with a tap strip on each side is replaced by two of its half units
(as ABBA's), and block.py puts tap strips between units where needed (plan v4 Phase 6). A capacitor that S0 binds to
a PDK device for the layout view (passives[].layout_binding) is a block of its own, variant A.
Each variant is drawn (block.py), DRC'd (full) and LVS'd with negative controls.

usage (inside layout-s0s3): python3 -m src.s4.run inputs/<d>/package.yaml [--workers 4]
Writes outputs/S4/<d>/: blocks.json, s4_report.json (G4.1-G4.6), blocks/<block>__<variant>/. Exit 0 PASS, 3 FAIL.
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.common import pcell
from src.common.hygiene import fresh_output_dir, gate_exit, new_run_id
from src.common.tools import REPO, provenance, rel, write_json
from src.s0.ingest import load_package
from src.s3 import options as O
from src.s4 import block as B

SYM_TOL = 0.005    # um: a mirror-symmetric variant's centroid offset (manufacturing grid)


def plan_blocks(ir: dict, groups: list) -> list:
    """[{'name', 'kind', 'type', 'body', 'devices'}]: matching groups first, then S0's blocks; one type and one body
    net per block (rule 1 of the plan); every device in exactly one block."""
    devs = {d["name"]: d for d in ir["devices"]}
    s0 = (ir.get("hierarchy") or {}).get("blocks", [])
    name_of = {frozenset(b["devices"]): b["name"] for b in s0}
    used, out = set(), []

    def add(name, members, kind):
        by = {}
        for m in members:
            if m not in used and m in devs:
                d = devs[m]
                by.setdefault((d["type"], d["terminals"]["b"]), []).append(m)
        for (ty, body), ms in by.items():
            out.append({"name": name if len(by) == 1 else f"{name}_{ty}", "kind": kind, "type": ty, "body": body,
                        "devices": ms})
            used.update(ms)
    for g in groups:
        add(name_of.get(frozenset(g["devices"]), f"{g.get('kind', 'group')}_" + "_".join(g["devices"])),
            g["devices"], g.get("kind") or "group")
    for b in s0:
        add(b["name"], b["devices"], b.get("primitive") or b.get("kind") or "block")
    for d in ir["devices"]:
        add(d["name"], [d["name"]], "single")
    for p in ir.get("passives", []):
        lb = p.get("layout_binding")
        if lb and lb.get("model", "").startswith("sky130_fd_pr__cap_mim"):
            out.append({"name": p["name"], "kind": "mim_cap", "type": "cap", "body": None, "devices": [p["name"]],
                        "binding": {"model": lb["model"], "params": lb["params"], "status": lb.get("status"),
                                    "top": p["a"], "bottom": p["b"]}})
    return out


def caps_of(ir: dict) -> list:
    return [p["name"] for p in ir.get("passives", []) if (p.get("layout_binding") or {}).get("model", "").startswith(
        "sky130_fd_pr__cap_mim")]


def split_wide(units: list, ir: dict, dec: dict, cells: Path, rules: dict, limit: float | None) -> list:
    """Each unit wider than 2 (limit - TAP_MARGIN - TAP_GAP), which a tap strip on each side cannot cover, becomes
    two of its half units (repeatedly); a unit that cannot be halved stays, and G4.5 reports it."""
    if not limit:
        return units
    wmax = 2 * (limit - B.TAP_MARGIN - B.TAP_GAP)
    types = O.device_types(ir)
    tid_of = {d: t for t, v in types.items() for d in v["devices"]}
    out = []
    for u in units:
        todo = [(u["rec"], types[tid_of[u["device"]]], tid_of[u["device"]])]
        while todo:
            r, t, tid = todo.pop(0)
            h = half_unit(t, tid, r["option"], cells, rules) if r["geometry"]["bbox_um"][0] > wmax else None
            if h is None:
                out.append({**u, "rec": r})
                continue
            tid_h = f"{t['model'].replace('sky130_fd_pr__', '')}_W{h[1]['W']:g}_L{t['L']:g}_m{t.get('m', 1)}".replace(".", "p")
            todo[:0] = [(h[0], h[1], tid_h), (h[0], h[1], tid_h)]
    return out


def half_unit(t: dict, tid: str, opt: dict, cells: Path, rules: dict) -> tuple[dict, dict] | None:
    """The S3 cell with half the fingers at the same finger width (a unit for ABBA/ABAB), built if needed."""
    nf = opt["nf"]
    if nf < 2 or nf % 2:
        return None
    th = {**t, "W": round(t["W"] / 2, 4)}
    tid_h = f"{t['model'].replace('sky130_fd_pr__', '')}_W{th['W']:g}_L{t['L']:g}_m{t.get('m', 1)}".replace(".", "p")
    want = {"nf": nf // 2, "gate_contacts": opt["gate_contacts"], "sd_cov": opt["sd_cov"]}
    cand = [o for o in O.grid(th["W"], guard=opt["magic"]["guard"]) if all(o[k] == v for k, v in want.items())
            and (o["nf"] % 2 or o["outer"] == opt["outer"])]
    if not cand:
        return None
    oh = cand[0]
    f = cells / O.cell_name(tid_h, oh) / "record.json"
    if f.exists():
        rec = json.loads(f.read_text())
    else:
        rec = O.build_one(th, tid_h, oh, cells, rules)
        write_json(f, rec)
    return (rec, th) if rec.get("ok") else None


def variants(blk: dict, ir: dict, dec: dict, cells: Path, rules: dict, limit: float | None = None) -> list:
    if blk["kind"] == "mim_cap":
        return [{"id": "A", "units": []}]
    vs = _variants(blk, ir, dec, cells, rules)
    return [{**v, "units": split_wide(v["units"], ir, dec, cells, rules, limit)} for v in vs]


def _variants(blk: dict, ir: dict, dec: dict, cells: Path, rules: dict) -> list:
    devs = {d["name"]: d for d in ir["devices"]}
    types = O.device_types(ir)
    tid_of = {d: t for t, v in types.items() for d in v["devices"]}

    def rec(d):
        return json.loads((cells / dec[tid_of[d]]["cell"] / "record.json").read_text())

    def unit(d, r, mirror):
        t = devs[d]["terminals"]
        return {"device": d, "rec": r, "mirror": mirror, "nets": {"D": t["d"], "G": t["g"], "S": t["s"]}}
    ds = blk["devices"]
    if len(ds) == 1:
        return [{"id": "A", "units": [unit(ds[0], rec(ds[0]), False)]}]
    if len(ds) == 2 and tid_of[ds[0]] == tid_of[ds[1]]:
        a, b = ds
        out = [{"id": "AB", "units": [unit(a, rec(a), False), unit(b, rec(b), True)]}]
        t = types[tid_of[a]]
        h = half_unit(t, tid_of[a], rec(a)["option"], cells, rules)
        if h:
            r = h[0]
            out.append({"id": "ABBA", "units": [unit(a, r, False), unit(b, r, False), unit(b, r, True), unit(a, r, True)]})
            out.append({"id": "ABAB", "units": [unit(a, r, False), unit(b, r, False), unit(a, r, False), unit(b, r, False)]})
        return out
    return [{"id": "row", "units": [unit(d, rec(d), False) for d in ds]}]


def symmetry(geo: dict, devices: list) -> dict:
    """For a two-device block:
      error_um          half the offset of the two devices' centroids from mirror images about the row's centre;
      centroid_offset_um the distance between the two centroids (0 = common centroid, as ABBA);
      mirror_image      every unit faces, across the centre, a unit of the same cell flipped the other way (AB,
                        ABBA); interdigitated ABAB is not a mirror image.
    Empty for any other block."""
    if len(devices) != 2:
        return {}
    us = geo["units"]
    xc = (geo["row"][0] + geo["row"][2]) / 2
    cen = {d: [u["x"] + u["w"] / 2 for u in us if u["device"] == d] for d in devices}
    ca, cb = (sum(cen[d]) / len(cen[d]) for d in devices)
    mirror = all(us[k]["rec"]["cell"] == us[-1 - k]["rec"]["cell"] and us[k]["mirror"] != us[-1 - k]["mirror"]
                 and {us[k]["device"], us[-1 - k]["device"]} <= set(devices) for k in range(len(us) // 2))
    return {"error_um": round(abs(ca + cb - 2 * xc) / 2, 4), "centroid_offset_um": round(abs(ca - cb), 4),
            "mirror_image": mirror and len(us) % 2 == 0}


def tap_distance(geo: dict) -> float | None:
    """The largest distance from any point of a unit's box to the ring or a tap strip (sampled every 0.25 um): the
    latch-up rule's diffusion-to-tap distance, bounded from above. None for a block without units (a capacitor)."""
    if not geo["units"]:
        return None
    rx0, ry0, rx1, ry1 = geo["ring"]
    strips = geo.get("strips", [])
    worst = 0.0
    for u in geo["units"]:
        nx, ny = max(2, int(u["w"] / 0.25) + 1), max(2, int(u["h"] / 0.25) + 1)
        for i in range(nx):
            for j in range(ny):
                x, y = u["x"] + u["w"] * i / (nx - 1), u["h"] * j / (ny - 1)
                worst = max(worst, min([x - rx0, rx1 - x, y - ry0, ry1 - y] + [abs(x - s) for s in strips]))
    return round(worst, 3)


def gds_bbox(gds: Path) -> list:
    import klayout.db as kdb
    ly = kdb.Layout()
    ly.read(str(gds))
    b = ly.top_cell().dbbox()
    return [round(b.left, 3), round(b.bottom, 3), round(b.right, 3), round(b.top, 3)]


def build_cap(blk: dict, v: dict, out: Path) -> dict:
    """A capacitor block: the PDK device, its plates on two tracks; DRC (full) and LVS with a negative control."""
    name = f"{blk['name']}__{v['id']}"
    d = out / "blocks" / name
    d.mkdir(parents=True, exist_ok=True)
    bd = blk["binding"]
    cc = B.cap_cell(f"{blk['name']}_mim", bd["model"], bd["params"], d)
    res = {"id": v["id"], "cell": name, "arrangement": [{"device": blk["name"], "cell": f"{blk['name']}_mim",
                                                         "mirror": False, "x": 0.0}], "binding": bd}
    if not cc.get("gds"):
        return {**res, "ok": False, "error": "the PDK capacitor was not generated", "build": cc}
    geo = B.cap_layout(cc, bd["top"], bd["bottom"])
    b = B.cap_build(name, cc, geo, d)
    res["build"] = b
    if not b["gds"]:
        return {**res, "ok": False, "error": "Magic did not write the block"}
    gds = REPO / b["gds"]
    dev = {"name": blk["name"], "model": bd["model"], "W": bd["params"]["W"], "L": bd["params"]["L"],
           "nets": {"C": bd["top"], "B": bd["bottom"]}}
    res["drc"] = pcell.drc(gds, name, d / "drc")
    res["lvs"] = B.lvs(gds, name, B.ref_netlist(name, [dev], [bd["top"], bd["bottom"]]), d / "lvs")
    res["geometry"] = {"bbox_um": gds_bbox(gds), "ring": geo["ring"], "row": geo["row"], "strips": [],
                       "tap_distance_max_um": None, "keepouts": geo["keepouts"]}
    res["geometry"]["area_um2"] = round((res["geometry"]["bbox_um"][2] - res["geometry"]["bbox_um"][0]) *
                                        (res["geometry"]["bbox_um"][3] - res["geometry"]["bbox_um"][1]), 2)
    res["pins"] = {"tracks": {side: {n: {"layer": "metal3", "y": y, "x": geo["track_span"], "width": B.TRACK_W}
                                     for n, y in geo["tracks"][side].items()} for side in ("top", "bottom")},
                   "body": None}
    res["symmetry"] = {}
    res["png"] = pcell.png(gds, d / f"{name}.png")
    res["ok"] = bool(res["drc"]["pass"] and res["lvs"]["pass"])
    return res


def build_variant(blk: dict, v: dict, ir: dict, out: Path, lu: float | None = None) -> dict:
    if blk["kind"] == "mim_cap":
        return build_cap(blk, v, out)
    name = f"{blk['name']}__{v['id']}"
    d = out / "blocks" / name
    geo = B.layout(v["units"], tap_limit=lu)
    res = {"id": v["id"], "cell": name, "arrangement": [{"device": u["device"], "cell": u["rec"]["cell"],
                                                         "mirror": u["mirror"], "x": u["x"]} for u in geo["units"]]}
    b = B.build(name, geo, blk["type"], blk["body"], d)
    res["build"] = b
    if not b["gds"]:
        return {**res, "ok": False, "error": "Magic did not write the block"}
    gds = REPO / b["gds"]
    devs = {x["name"]: x for x in ir["devices"]}
    body_port = f"{blk['body']}_body"
    dl = []
    for dn in blk["devices"]:
        x = devs[dn]
        nf = sum(u["rec"]["option"]["nf"] for u in geo["units"] if u["device"] == dn)
        t = x["terminals"]
        dl.append({"name": dn, "model": x["model"], "W": x["W_um"], "L": x["L_um"], "nf": nf, "body_port": body_port,
                   "nets": {"D": t["d"], "G": t["g"], "S": t["s"]}})
    ports = sorted({n for side in geo["tracks"].values() for n in side}) + [body_port]
    res["drc"] = pcell.drc(gds, name, d / "drc")
    res["lvs"] = B.lvs(gds, name, B.ref_netlist(name, dl, ports), d / "lvs")
    res["geometry"] = {"bbox_um": gds_bbox(gds), "ring": geo["ring"], "row": geo["row"], "strips": geo["strips"],
                       "tap_distance_max_um": tap_distance(geo)}
    res["geometry"]["area_um2"] = round((res["geometry"]["bbox_um"][2] - res["geometry"]["bbox_um"][0]) *
                                        (res["geometry"]["bbox_um"][3] - res["geometry"]["bbox_um"][1]), 2)
    res["pins"] = {"tracks": {side: {n: {"layer": "metal3", "y": y, "x": geo["track_span"], "width": B.TRACK_W}
                                     for n, y in geo["tracks"][side].items()} for side in ("top", "bottom")},
                   "body": {"net": blk["body"], "port": body_port, "layer": "locali",
                            "at": [round((geo["ring"][0] + geo["ring"][2]) / 2, 3), geo["ring"][1]]}}
    res["symmetry"] = symmetry(geo, blk["devices"])
    res["png"] = pcell.png(gds, d / f"{name}.png")
    res["ok"] = bool(res["drc"]["pass"] and res["lvs"]["pass"])
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args(argv)
    pkg = load_package(REPO / a.package)
    design = pkg["design"]
    s0, s1, s2, s3 = (REPO / "outputs" / s / design for s in ("S0", "S1", "S2", "S3"))
    out = REPO / "outputs" / "S4" / design
    cells = REPO / "outputs" / "S3" / "_cells"
    ir = json.loads((s0 / "circuit_ir.json").read_text())
    groups = json.loads((s1 / "s1_report.json").read_text())["gates"].get("G1.4_matching_groups", {}).get("groups", [])
    dd = json.loads((s3 / "device_decisions.json").read_text())
    rules = json.loads((REPO / "outputs" / "S2" / "pdk" / "parasitics.json").read_text())["rules"]
    cons = json.loads((s2 / "constraints.json").read_text())
    cons = cons.get("constraints", cons) if isinstance(cons, dict) else cons
    lu = next((c["value"] for c in cons if c.get("id") == "place.latchup_tap_distance"), None)
    fresh_output_dir(out)
    out.mkdir(parents=True, exist_ok=True)
    blocks = plan_blocks(ir, groups)
    jobs = [(b, v) for b in blocks for v in variants(b, ir, dd["decisions"], cells, rules, lu)]
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        built = list(ex.map(lambda j: build_variant(j[0], j[1], ir, out, lu), jobs))
    for b in blocks:
        b["variants"] = [r for (bb, _), r in zip(jobs, built) if bb is b]
    allv = [v for b in blocks for v in b["variants"]]
    devs = {d["name"]: d for d in ir["devices"]}
    tblocks = [b for b in blocks if b["kind"] != "mim_cap"]
    gates = {
        "G4.1_one_type_and_body_per_block": {
            "pass": all(len({devs[x]["type"] for x in b["devices"]}) == 1 and
                        len({devs[x]["terminals"]["b"] for x in b["devices"]}) == 1 for b in tblocks) and
            sorted(x for b in blocks for x in b["devices"]) == sorted(list(devs) + caps_of(ir)) and
            all((v.get("build") or {}).get("gds") for v in allv),
            "blocks": {b["name"]: {"type": b["type"], "body": b["body"], "devices": b["devices"]} for b in blocks}},
        "G4.2_DRC_every_variant": {"pass": all((v.get("drc") or {}).get("pass") for v in allv),
                                   "detail": {v["cell"]: (v.get("drc") or {}).get("errors") for v in allv}},
        "G4.3_LVS_every_variant": {"pass": all((v.get("lvs") or {}).get("pass") for v in allv),
                                   "detail": {v["cell"]: (v.get("lvs") or {}).get("match") for v in allv}},
        "G4.4_symmetry": {
            "pass": all(any(v.get("ok") and v["symmetry"].get("mirror_image") and v["symmetry"]["error_um"] <= SYM_TOL
                            for v in b["variants"]) for b in blocks if len(b["devices"]) == 2),
            "tolerance_um": SYM_TOL, "detail": {v["cell"]: v.get("symmetry") for v in allv if v.get("symmetry")},
            "note": "every two-device block has a signed-off variant that is a mirror image about its centre; "
                    "centroid_offset_um is 0 for a common centroid (ABBA)"},
        "G4.5_latchup_tap_distance": {
            "pass": lu is not None and all((v.get("geometry") or {}).get("tap_distance_max_um", 1e9) <= lu
                                           for b in tblocks for v in b["variants"]),
            "limit_um": lu, "detail": {v["cell"]: (v.get("geometry") or {}).get("tap_distance_max_um") for v in allv},
            "tap_strips": {v["cell"]: (v.get("geometry") or {}).get("strips") for v in allv
                           if (v.get("geometry") or {}).get("strips")},
            "note": "the LU rules are also in the block's own DRC (G4.2), which defers nothing; a capacitor block "
                    "has no diffusion (None)"},
        "G4.6_port_capacitance (info)": {"pass": None, "note": "block port C against S2's hierarchy.json: S6 extraction (plan Phase 5)"},
    }
    ident = {"run_id": new_run_id(), "design": design, "s3_run_id": dd.get("run_id")}
    write_json(out / "blocks.json", {**ident, "blocks": [{k: v for k, v in b.items()} for b in blocks]})
    prov = provenance([s0 / "circuit_ir.json", s1 / "s1_report.json", s3 / "device_decisions.json", s2 / "constraints.json",
                       REPO / a.package])
    report = {**ident, "gates": gates, "all_pass": all(g.get("pass") in (True, None) for g in gates.values()),
              "provenance": prov}
    write_json(out / "s4_report.json", report)
    for k in gates:
        print(f"{k:40s} {gates[k].get('pass')}")
    for v in allv:
        print(f"  {v['cell']:44s} drc={(v.get('drc') or {}).get('errors')} lvs={(v.get('lvs') or {}).get('match')} "
              f"area={(v.get('geometry') or {}).get('area_um2')} sym={v.get('symmetry')}")
    return gate_exit(report["all_pass"])


if __name__ == "__main__":
    sys.exit(main())
