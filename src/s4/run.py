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
            twin = sum(1 for t, _ in by if t == ty) > 1   # one type on two bodies: the body names the block too
            nm = name if len(by) == 1 else (f"{name}_{ty}_{body}" if twin else f"{name}_{ty}")
            k, base = 2, nm
            while any(o["name"] == nm for o in out):      # S0 may give several blocks one name (ttsky25a_fd's four
                nm, k = f"{base}_{k}", k + 1               # pmos_matched_current_source_pair): numbered in order
            out.append({"name": nm, "kind": kind, "type": ty, "body": body, "devices": ms})
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


def resistor_blocks(ir: dict, opts: dict) -> list:
    """layout.yaml's resistor_blocks (plan v4 Phase 8): [{name, members: [name prefix per matched pack], body}]. Each
    becomes one block of the passives whose layout binding is a PDK resistor and whose name starts with a prefix;
    'packs' keeps them per prefix, in the order of their string."""
    out = []
    pas = [p for p in ir.get("passives", []) if "res_" in (p.get("layout_binding") or {}).get("model", "")]
    for rb in opts.get("resistor_blocks") or []:
        packs = [chain_order([p for p in pas if p["name"].startswith(pre)]) for pre in rb["members"]]
        out.append({"name": rb["name"], "kind": "resistors", "type": "res", "body": rb["body"],
                    "devices": [p["name"] for pk in packs for p in pk], "packs": packs})
    return out


def chain_order(rs: list) -> list:
    """A series string of resistors (a res_pack) in order from one end, each with 'first' (the node it shares with
    the previous one, or the string's end) and 'last'."""
    from collections import Counter
    deg = Counter(n for r in rs for n in (r["a"], r["b"]))
    start = sorted(n for n, c in deg.items() if c == 1)[0]
    out, node, left = [], start, list(rs)
    while left:
        r = next(r for r in left if node in (r["a"], r["b"]))
        left.remove(r)
        nxt = r["b"] if r["a"] == node else r["a"]
        out.append({**r, "first": node, "last": nxt})
        node = nxt
    return out


def res_unit(model: str, params: dict, cells: Path) -> dict:
    """A resistor drawn by the PDK's generator without its own guard ring (the block has one), as a unit record with
    its two metal1 ends as pins: P at the top, N at the bottom (outputs/S4/_res/<cell>/)."""
    import klayout.db as kdb
    w, l = float(params["W"]), float(params["L"])
    name = f"{model.replace('sky130_fd_pr__', '')}_W{w:g}_L{l:g}".replace(".", "p")
    d = cells / name
    f = d / "record.json"
    if f.exists():
        return json.loads(f.read_text())
    g = pcell.generate([{"cell": name, "model": model, "params": {"w": w, "l": l, "guard": 0}}], d.resolve())
    ly = kdb.Layout()
    ly.read(g["gds"][name])
    top = ly.top_cell()
    o = top.dbbox()
    boxes = [p.bbox() for p in kdb.Region(top.begin_shapes_rec(ly.layer(68, 20))).merged().each()]
    m1 = sorted(([round(b.left * ly.dbu - o.left, 3), round(b.bottom * ly.dbu - o.bottom, 3),
                  round(b.right * ly.dbu - o.left, 3), round(b.top * ly.dbu - o.bottom, 3)] for b in boxes),
                key=lambda r: r[1])
    if len(m1) != 2:
        raise RuntimeError(f"{name}: expected two metal1 ends, got {len(m1)}")
    rec = {"cell": name, "gds": rel(Path(g["gds"][name])), "kind": "resistor", "ok": True, "option": {"nf": 1},
           "model": model, "W": w, "L": l,
           "geometry": {"bbox_um": [round(o.width(), 3), round(o.height(), 3)], "strips": []},
           "pins": {"P": {"layer": "metal1", "rect": m1[1]}, "N": {"layer": "metal1", "rect": m1[0]}}}
    write_json(f, rec)
    return rec


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
        tid = tid_of[u["device"]]
        full = types[tid]
        nf_full = dec[tid]["chosen"]["nf"]
        # a unit may already be a half unit (ABBA, ABAB): its type has the width its own fingers carry
        t0 = {**full, "W": round(full["W"] * u["rec"]["option"]["nf"] / nf_full, 4)}
        todo = [(u["rec"], t0, tid)]
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


def layout_options(design: str) -> dict:
    """inputs/<d>/layout.yaml (plan v4 Phase 8): {matching: centroid, dummies: true}; empty when absent, which keeps
    every design that has none (the 5T, LOADBench) exactly as before. S0-S3 never read it."""
    import yaml
    f = REPO / "inputs" / design / "layout.yaml"
    return (yaml.safe_load(f.read_text()) or {}) if f.exists() else {}


def centroid_sequence(counts: dict) -> list | None:
    """A mirror-symmetric (palindromic) row of copies, so every device's centroid sits on the row's centre: each
    device's count halved on each side, interleaved in turn (A B C | C B A); a device with an odd count takes the
    centre, and two odd counts cannot be centred (None)."""
    odd = [d for d, c in counts.items() if c % 2]
    if len(odd) > 1:
        return None
    left, rest = [], {d: c // 2 for d, c in counts.items()}
    while any(rest.values()):
        for d in counts:
            if rest[d]:
                left.append(d)
                rest[d] -= 1
    return left + odd + left[::-1]


def interdigitated(counts: dict) -> list:
    """One copy of each device in turn (A B A B ...), as long as copies are left."""
    out, rest = [], dict(counts)
    while any(rest.values()):
        for d in counts:
            if rest[d]:
                out.append(d)
                rest[d] -= 1
    return out


def variants(blk: dict, ir: dict, dec: dict, cells: Path, rules: dict, limit: float | None = None,
             opts: dict | None = None) -> list:
    if blk["kind"] == "mim_cap":
        return [{"id": "A", "units": []}]
    if blk["kind"] == "resistors":
        vs = resistor_variants(blk, REPO / "outputs" / "S4" / "_res")
        return [{**v, "units": with_dummies(v["units"], blk)} for v in vs] if (opts or {}).get("dummies") else vs
    vs = _variants(blk, ir, dec, cells, rules, opts or {})
    vs = [{**v, "units": split_wide(v["units"], ir, dec, cells, rules, limit)} for v in vs]
    if (opts or {}).get("dummies") and len(blk["devices"]) >= 2:
        vs = [{**v, "units": with_dummies(v["units"], blk)} for v in vs]
    return vs


def resistor_variants(blk: dict, cells: Path) -> list:
    """The packs of a resistor block interleaved: two packs as A B B A A B B A ... (each pack's centroid on the row's
    centre), more packs in turn. Along each pack's string the units alternate orientation, so the node two
    neighbours of the string share is on one side (top or bottom) of both."""
    queues = []
    for pk in blk["packs"]:
        q = []
        for k, r in enumerate(pk):
            top, bot = (r["last"], r["first"]) if k % 2 == 0 else (r["first"], r["last"])
            lb = r["layout_binding"]
            q.append({"device": r["name"], "rec": res_unit(lb["model"], lb["params"], cells), "mirror": False,
                      "nets": {"P": top, "N": bot}})
        queues.append(q)
    seq = []
    if len(queues) == 2:   # the second string runs right to left, so its output end (Vom) sits near the right end,
        # as the first's (Vop) sits at the left; the A B B A palindrome keeps both centroids on the centre
        queues[1].reverse()
        k = 0
        while queues[0] or queues[1]:
            for i in ((0, 1) if k % 2 == 0 else (1, 0)):
                if queues[i]:
                    seq.append(queues[i].pop(0))
            k += 1
    else:
        while any(queues):
            for q in queues:
                if q:
                    seq.append(q.pop(0))
    return [{"id": "interleaved", "units": seq}]


def with_dummies(units: list, blk: dict) -> list:
    """One dummy unit at each end of a matched row (plan v4 Phase 8): the same cell as its neighbour, every terminal
    on the block's body net."""
    def dummy(u, k):
        return {"device": f"DUMMY{k}", "rec": u["rec"], "mirror": u["mirror"], "dummy_of": u["device"],
                "nets": {t: blk["body"] for t in u["nets"]}}
    return [dummy(units[0], 0)] + units + [dummy(units[-1], 1)]


def _variants(blk: dict, ir: dict, dec: dict, cells: Path, rules: dict, opts: dict) -> list:
    devs = {d["name"]: d for d in ir["devices"]}
    types = O.device_types(ir)
    tid_of = {d: t for t, v in types.items() for d in v["devices"]}
    centroid = opts.get("matching") == "centroid"

    def rec(d):
        return json.loads((cells / dec[tid_of[d]]["cell"] / "record.json").read_text())

    def unit(d, r, mirror):
        t = devs[d]["terminals"]
        return {"device": d, "rec": r, "mirror": mirror, "nets": {"D": t["d"], "G": t["g"], "S": t["s"]}}

    def copies(d):
        return devs[d].get("m") or 1

    def row(seq, mirrored_half=False):
        """Units for a sequence of device names; the right half flipped when the row is a mirror image."""
        n = len(seq)
        return [unit(d, rec(d), mirrored_half and k >= n - n // 2) for k, d in enumerate(seq)]
    ds = blk["devices"]
    if len(ds) == 1:
        return [{"id": "A", "units": row([ds[0]] * copies(ds[0]))}]
    counts = {d: copies(d) for d in ds}
    same = len({tid_of[d] for d in ds}) == 1
    if len(ds) == 2 and same:
        a, b = ds
        out = []
        if not centroid:   # as before (the 5T, LOADBench): the mirror image AB, then ABBA/ABAB from half units
            out.append({"id": "AB", "units": row([a] * counts[a] + [b] * counts[b], True)})
        # whole copies (plan v4 Phase 8): most of ttsky25a_fd's devices have m = 2. Either device with m >= 2 (review
        # of Phase 8: m_a = 1, m_b = 2 fell to the half-unit ABBA, one copy of b against m = 2 in the reference)
        if max(counts.values()) >= 2:
            seq = centroid_sequence(counts)
            if seq:
                out.append({"id": "ABBA", "units": row(seq, True)})
            elif counts[a] == counts[b]:   # both odd (m = 9): no common centroid in one row; the best mirror image
                left = interdigitated({a: (counts[a] + 1) // 2, b: counts[b] // 2})
                out.append({"id": "mirror", "units": row(left + [b if x == a else a for x in reversed(left)], True)})
            out.append({"id": "ABAB", "units": row(interdigitated(counts))})
            return out
        h = half_unit(types[tid_of[a]], tid_of[a], rec(a)["option"], cells, rules)
        if h:
            r = h[0]
            out.append({"id": "ABBA", "units": [unit(a, r, False), unit(b, r, False), unit(b, r, True), unit(a, r, True)]})
            out.append({"id": "ABAB", "units": [unit(a, r, False), unit(b, r, False), unit(a, r, False), unit(b, r, False)]})
        if not out:   # matching: centroid, but one copy each and no half unit (odd fingers): neither a common
            # centroid nor an interdigitated row exists, so the mirror image AB, the best left (GUI test of
            # 2026-11-04: the 5T's PMOS mirror got no variant at all and S5 stopped; flow record row 93)
            out.append({"id": "AB", "units": row([a] * counts[a] + [b] * counts[b], True),
                        "note": "matching: centroid asked, impossible here (one copy each, odd fingers): mirror image"})
        return out
    if centroid and same:   # three or more matched devices (or unequal m): one row, centroids on its centre
        seq = centroid_sequence(counts)
        out = [{"id": "centroid", "units": row(seq, True)}] if seq else []
        return out + [{"id": "interdigitated", "units": row(interdigitated(counts))}]
    return [{"id": "row", "units": [u for d in ds for u in row([d] * counts[d])]}]


def symmetry(geo: dict, devices: list) -> dict:
    """For a two-device block:
      error_um          half the offset of the two devices' centroids from mirror images about the row's centre;
      centroid_offset_um the distance between the two centroids (0 = common centroid, as ABBA);
      mirror_image      every unit faces, across the centre, a unit of the same cell flipped the other way (AB,
                        ABBA); interdigitated ABAB is not a mirror image.
    Empty for any other block."""
    if len(devices) != 2:
        return {}
    us = [u for u in geo["units"] if u["device"] in devices]   # dummies at the ends are not part of the pair
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
    dev = {"name": blk["name"], "model": bd["model"], "W": float(bd["params"]["W"]), "L": float(bd["params"]["L"]),
           "m": int(float(bd["params"].get("M") or 1)),
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


def internal_nets(blk: dict, ir: dict) -> set:
    """Nets that only this block's elements use (no other device, passive or port): their tracks are short."""
    mine = set(blk["devices"])
    ends = [(d["name"], [d["terminals"][k] for k in "dgsb"]) for d in ir["devices"]]
    ends += [(p["name"], [p["a"], p["b"]]) for p in ir.get("passives", [])]
    inside = {n for nm, ns in ends if nm in mine for n in ns}
    outside = {n for nm, ns in ends if nm not in mine for n in ns} | {p["name"] for p in ir["ports"]}
    # a source removed in the layout view leaves its nodes as ports under other names (VREF for net Vref; review of
    # plan v4 Phase 8): they are never internal
    outside |= {s[k] for s in ir.get("internal_sources", []) for k in ("p", "n") if s.get(k)}
    return inside - outside - {blk["body"]}


def build_variant(blk: dict, v: dict, ir: dict, out: Path, lu: float | None = None, opts: dict | None = None) -> dict:
    if blk["kind"] == "mim_cap":
        return build_cap(blk, v, out)
    name = f"{blk['name']}__{v['id']}"
    d = out / "blocks" / name
    inner = internal_nets(blk, ir) if (opts or {}).get("pack_internal") else set()
    geo = B.layout(v["units"], tap_limit=None if blk["kind"] == "resistors" else lu, internal=inner,
                   bbox_origin=(opts or {}).get("pin_origin") == "bbox")   # flow record row 95 (opt-in)
    res = {"id": v["id"], "cell": name, "arrangement": [{"device": u["device"], "cell": u["rec"]["cell"],
                                                         "mirror": u["mirror"], "x": u["x"]} for u in geo["units"]]}
    b = B.build(name, geo, blk["type"], blk["body"], d)
    res["build"] = b
    if not b["gds"]:
        return {**res, "ok": False, "error": "Magic did not write the block"}
    gds = REPO / b["gds"]
    devs = {x["name"]: x for x in ir["devices"]}
    body_port = f"{blk['body']}_body"
    dl, per_copy = [], {}
    for dn in blk["devices"] if blk["kind"] != "resistors" else []:
        x = devs[dn]
        m = x.get("m") or 1                        # m copies drawn, each a whole S3 cell or two half units
        nf = sum(u["rec"]["option"]["nf"] for u in geo["units"] if u["device"] == dn)
        per_copy[dn] = nf / m
        t = x["terminals"]
        dl.append({"name": dn, "model": x["model"], "W": x["W_um"], "L": x["L_um"], "nf": round(nf / m), "m": m,
                   "body_port": body_port, "nets": {"D": t["d"], "G": t["g"], "S": t["s"]}})
    for u in geo["units"]:                         # resistors: each unit is one, its ends on the tracks
        if blk["kind"] == "resistors":
            r = u["rec"]
            dum = "dummy_of" in u
            dl.append({"name": f"{blk['name']}_{u['device']}" if dum else u["device"], "model": r["model"],
                       "W": r["W"], "L": r["L"], "nets": dict(u["nets"]), "dummy": dum})
    for u in geo["units"]:                         # dummies: every terminal on the body (plan v4 Phase 8)
        if "dummy_of" in u and blk["kind"] != "resistors":
            x = devs[u["dummy_of"]]
            unf = u["rec"]["option"]["nf"]
            dl.append({"name": f"{blk['name']}_{u['device']}", "model": x["model"], "L": x["L_um"],
                       "W": round(x["W_um"] * unf / per_copy[u["dummy_of"]], 4), "nf": unf, "m": 1,
                       "body_port": body_port, "nets": {t: blk["body"] for t in ("D", "G", "S")}, "dummy": True})
    ports = sorted({n for side in geo["tracks"].values() for n in side}) + [body_port]
    res["drc"] = pcell.drc(gds, name, d / "drc")
    res["lvs"] = B.lvs(gds, name, B.ref_netlist(name, dl, ports), d / "lvs")
    res["geometry"] = {"bbox_um": gds_bbox(gds), "ring": geo["ring"], "row": geo["row"], "strips": geo["strips"],
                       "tap_distance_max_um": tap_distance(geo)}
    res["geometry"]["area_um2"] = round((res["geometry"]["bbox_um"][2] - res["geometry"]["bbox_um"][0]) *
                                        (res["geometry"]["bbox_um"][3] - res["geometry"]["bbox_um"][1]), 2)
    res["pins"] = {"tracks": {side: {n: {"layer": "metal3", "y": y, "x": geo["track_span"], "width": B.TRACK_W}
                                     for n, y in geo["tracks"][side].items() if n not in inner}
                              for side in ("top", "bottom")},
                   "body": {"net": blk["body"], "port": body_port, "layer": "locali",
                            "at": [round((geo["ring"][0] + geo["ring"][2]) / 2, 3), geo["ring"][1]]}}
    res["geometry"]["keepouts"] = [                # internal short tracks: S5's met3 runs keep clear
        {"layer": "metal3", "box": [geo["spans"][side][n][0], y - B.TRACK_W / 2, geo["spans"][side][n][1], y + B.TRACK_W / 2],
         "net": n} for side in ("top", "bottom") for n, y in geo["tracks"][side].items() if n in inner]
    if blk["kind"] == "resistors":
        res["geometry"]["tap_distance_max_um"] = None   # poly on field oxide: no diffusion to tap
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
    opts = layout_options(design)
    blocks = plan_blocks(ir, groups) + resistor_blocks(ir, opts)
    jobs = [(b, v) for b in blocks for v in variants(b, ir, dd["decisions"], cells, rules, lu, opts)]
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        built = list(ex.map(lambda j: build_variant(j[0], j[1], ir, out, lu, opts), jobs))
    for b in blocks:
        b["variants"] = [r for (bb, _), r in zip(jobs, built) if bb is b]
    allv = [v for b in blocks for v in b["variants"]]
    devs = {d["name"]: d for d in ir["devices"]}
    tblocks = [b for b in blocks if b["kind"] not in ("mim_cap", "resistors")]
    bound_res = [p["name"] for p in ir.get("passives", []) if "res_" in (p.get("layout_binding") or {}).get("model", "")]
    tid_of = {d: t for t, v in O.device_types(ir).items() for d in v["devices"]}
    matched = [b for b in tblocks if len(b["devices"]) == 2 and tid_of[b["devices"][0]] == tid_of[b["devices"][1]]]
    gates = {
        "G4.1_one_type_and_body_per_block": {
            "pass": all(len({devs[x]["type"] for x in b["devices"]}) == 1 and
                        len({devs[x]["terminals"]["b"] for x in b["devices"]}) == 1 for b in tblocks) and
            sorted(x for b in blocks for x in b["devices"]) == sorted(list(devs) + caps_of(ir) + bound_res) and
            all((v.get("build") or {}).get("gds") for v in allv),
            "blocks": {b["name"]: {"type": b["type"], "body": b["body"], "devices": b["devices"]} for b in blocks}},
        "G4.2_DRC_every_variant": {"pass": all((v.get("drc") or {}).get("pass") for v in allv),
                                   "detail": {v["cell"]: (v.get("drc") or {}).get("errors") for v in allv}},
        "G4.3_LVS_every_variant": {"pass": all((v.get("lvs") or {}).get("pass") for v in allv),
                                   "detail": {v["cell"]: (v.get("lvs") or {}).get("match") for v in allv}},
        "G4.4_symmetry": {
            "pass": all(any(v.get("ok") and v["symmetry"].get("mirror_image") and v["symmetry"]["error_um"] <= SYM_TOL
                            for v in b["variants"]) for b in matched),
            "tolerance_um": SYM_TOL, "detail": {v["cell"]: v.get("symmetry") for v in allv if v.get("symmetry")},
            "not_matched": [b["name"] for b in tblocks if len(b["devices"]) == 2 and b not in matched],
            "note": "every two-device block of one device type (a matched pair or mirror of one size) has a signed-off "
                    "variant that is a mirror image about its centre; centroid_offset_um is 0 for a common centroid "
                    "(ABBA). Two devices of different sizes (not_matched) cannot be mirror images"},
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
    ident = {"run_id": new_run_id(), "design": design, "s3_run_id": dd.get("run_id"), "layout_options": opts}
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
