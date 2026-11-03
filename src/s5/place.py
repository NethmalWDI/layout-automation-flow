"""S5 placement (plan v4, section 2; constants fixed in the PREREG amendment of 2026-11-03, late evening).

Rows by device type, PMOS above NMOS (designer rows, when the package has them, order the rows). Within a row the
blocks stand BLOCK_GAP apart, bottom-aligned; rows are ROW_GAP apart. A row with one symmetric block (a matched pair
or mirror) puts that block's own axis at x = 0; a row without one is centred; two symmetric blocks may not share a
row. Every ordered row partition, every block variant and a vertical flip of every block are enumerated.

Cost of a candidate:
  budget-aware  A / A_ref + LAMBDA * sum_n max(0, u_n - 1) + MU * sum_n u_n
  area-only     A / A_ref            (the AICL-like baseline: connectivity-agnostic)
A is the bounding-box area, A_ref the sum of each block's smallest variant; u_n is net n's half-perimeter wire
estimate over S2's route.max_length.<n>.metal3. All lengths in um.
"""
from __future__ import annotations

import itertools

ROW_GAP = 3.0
BLOCK_GAP = 3.0
LAMBDA, MU = 10.0, 1.0
MAX_CANDIDATES = 50000
AXIS_TOL = 0.005


def ordered_partitions(items: list) -> list:
    """Every way to split items into an ordered list of non-empty ordered rows (n! 2^(n-1) of them)."""
    if not items:
        return [[]]
    out = []
    for perm in itertools.permutations(items):
        for cuts in itertools.product((False, True), repeat=len(perm) - 1):
            rows, cur = [], [perm[0]]
            for it, cut in zip(perm[1:], cuts):
                if cut:
                    rows.append(cur)
                    cur = [it]
                else:
                    cur.append(it)
            out.append(rows + [cur])
    return out


def local(variant: dict, flip: bool) -> dict:
    """A block variant's geometry in its own coordinates, flipped upside down (y -> -y) if asked."""
    x0, y0, x1, y1 = variant["geometry"]["bbox_um"]
    row = variant["geometry"]["row"]
    s = -1.0 if flip else 1.0
    pins = []
    for side in ("top", "bottom"):
        for net, t in variant["pins"]["tracks"][side].items():
            pins.append({"net": net, "x0": t["x"][0], "x1": t["x"][1], "y": s * t["y"], "kind": "track"})
    b = variant["pins"]["body"]
    pins.append({"net": b["net"], "x0": b["at"][0], "x1": b["at"][0], "y": s * b["at"][1], "kind": "body"})
    return {"bbox": [x0, min(s * y0, s * y1), x1, max(s * y0, s * y1)], "axis": (row[0] + row[2]) / 2, "pins": pins}


def realise(rows: list, choice: dict, blocks: dict) -> dict | None:
    """rows: [[block, ...], ...] top to bottom; choice: {block: (variant, flip)}. None if two symmetric blocks share
    a row. Returns the placed blocks (origin, bounding box, pins) and the overall bounding box."""
    placed, y_top = {}, 0.0
    for row in rows:
        geo = {b: local(choice[b][0], choice[b][1]) for b in row}
        sym = [b for b in row if blocks[b]["symmetric"]]
        if len(sym) > 1:
            return None
        h = max(g["bbox"][3] - g["bbox"][1] for g in geo.values())
        y_bot = y_top - h
        xs, x = {}, 0.0
        for b in row:
            xs[b] = x - geo[b]["bbox"][0]          # origin x so that the box starts at x
            x += geo[b]["bbox"][2] - geo[b]["bbox"][0] + BLOCK_GAP
        width = x - BLOCK_GAP
        shift = -(xs[sym[0]] + geo[sym[0]]["axis"]) if sym else -width / 2
        for b in row:
            g = geo[b]
            tx, ty = xs[b] + shift, y_bot - g["bbox"][1]
            placed[b] = {"variant": choice[b][0]["id"], "flip": choice[b][1], "origin": [round(tx, 4), round(ty, 4)],
                         "bbox": [round(g["bbox"][0] + tx, 4), round(g["bbox"][1] + ty, 4),
                                  round(g["bbox"][2] + tx, 4), round(g["bbox"][3] + ty, 4)],
                         "axis_x": round(g["axis"] + tx, 4) if blocks[b]["symmetric"] else None,
                         "pins": [{**p, "x0": round(p["x0"] + tx, 4), "x1": round(p["x1"] + tx, 4),
                                   "y": round(p["y"] + ty, 4)} for p in g["pins"]]}
        y_top = y_bot - ROW_GAP
    bb = [min(p["bbox"][0] for p in placed.values()), min(p["bbox"][1] for p in placed.values()),
          max(p["bbox"][2] for p in placed.values()), max(p["bbox"][3] for p in placed.values())]
    return {"rows": rows, "blocks": placed, "bbox": [round(v, 4) for v in bb],
            "area_um2": round((bb[2] - bb[0]) * (bb[3] - bb[1]), 3)}


def hpwl(pins: list) -> float:
    """Half-perimeter of the box a net's pins need: a track is a horizontal segment (its whole span can be tapped),
    so the horizontal part is the gap between the segments, not their span."""
    xs0, xs1, ys = [p["x0"] for p in pins], [p["x1"] for p in pins], [p["y"] for p in pins]
    return max(0.0, max(xs0) - min(xs1)) + (max(ys) - min(ys))


def wires(pl: dict) -> dict:
    """{net: half-perimeter estimate} for every net with pins in two or more places (the pins of one block's track and
    its own ring count as two places)."""
    by = {}
    for b, p in pl["blocks"].items():
        for q in p["pins"]:
            by.setdefault(q["net"], []).append(q)
    return {n: round(hpwl(ps), 4) for n, ps in by.items() if len(ps) > 1}


def cost(pl: dict, a_ref: float, max_len: dict) -> dict:
    w = wires(pl)
    u = {n: round(w.get(n, 0.0) / L, 4) for n, L in max_len.items()}
    over = sum(max(0.0, x - 1) for x in u.values())
    return {"area_um2": pl["area_um2"], "area_term": round(pl["area_um2"] / a_ref, 4), "hpwl_um": w, "u": u,
            "budget_aware": round(pl["area_um2"] / a_ref + LAMBDA * over + MU * sum(u.values()), 4),
            "area_only": round(pl["area_um2"] / a_ref, 4)}


def designer_ok(rows: list, drow: dict) -> bool:
    """With designer rows (block -> its designer row index, top = 0): a block from a higher designer row may not sit
    in a lower placement row than a block from a lower designer row."""
    if not drow:
        return True
    at = {b: i for i, r in enumerate(rows) for b in r}
    return all(not (drow[a] < drow[b] and at[a] > at[b]) for a in at for b in at if a in drow and b in drow)


def enumerate_candidates(blocks: dict, max_len: dict, drow: dict | None = None) -> list:
    """blocks: {name: {'type', 'symmetric', 'variants': [ok variants]}}. Every candidate with its cost terms."""
    pm = [b for b in blocks if blocks[b]["type"] == "pmos"]
    nm = [b for b in blocks if blocks[b]["type"] != "pmos"]
    a_ref = sum(min(v["geometry"]["area_um2"] for v in blocks[b]["variants"]) for b in blocks)
    opts = {b: [(v, f) for v in blocks[b]["variants"] for f in (False, True)] for b in blocks}
    names = list(blocks)
    n_choice = 1
    for b in names:
        n_choice *= len(opts[b])
    row_sets = [p + q for p in ordered_partitions(pm) for q in ordered_partitions(nm)]
    row_sets = [r for r in row_sets if designer_ok(r, drow or {})]
    if len(row_sets) * n_choice > MAX_CANDIDATES:
        raise RuntimeError(f"{len(row_sets) * n_choice} candidates: above {MAX_CANDIDATES}, needs the annealer")
    out = []
    for rows in row_sets:
        for combo in itertools.product(*(opts[b] for b in names)):
            choice = dict(zip(names, combo))
            pl = realise(rows, choice, blocks)
            if pl is None:
                continue
            out.append({"placement": pl, "cost": cost(pl, a_ref, max_len)})
    return out
