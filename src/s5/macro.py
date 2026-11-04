"""S5 for a design with a hierarchy of its own (plan v4 Phase 8, docs/plan_v5_ttsky25a.md; PREREG amendment of
2026-11-04 morning).

1. Every S4 block belongs to the sub-circuit (xschem instance) of its devices (`circuits/<d>/upstream/hierarchy.json`);
   a block whose devices span several instances (the interleaved res_packs) is a macro of its own.
2. Inside a macro the blocks are placed in rows with src/s5/place.py's rules: exhaustive enumeration up to
   ENUM_MAX blocks, beyond that simulated annealing over row placements (seed, moves and schedule fixed in PREREG).
   Both costs (budget-aware, area-only) run the same search with the same seed; each net's wire use counts the pins
   inside the macro only.
3. Each macro, as placed, becomes one large block (its pins and keep-outs those of its blocks) for the top level,
   where src/s5/place.py enumerates every arrangement as before. Macros are not flipped.
Every placement, at either level, must fit the hard outline (`layout.yaml` outline_um: width, height); one that does
not is rejected, never traded.
"""
from __future__ import annotations

import json
import math
import random

from src.common.tools import REPO
from src.s5 import place as P

ENUM_MAX = 6          # blocks: exhaustive enumeration up to this many (as for the 5T and LOADBench)
SEED = 20261104
MOVES = 40000
T_START = 0.05        # x the starting placement's cost
COOL = 0.9998         # per move
OUTSIDE = 100.0       # the penalty of a placement outside the outline, x (1 + its relative excess); used only when the
                      # start itself is outside (row 96)
SHAPES = (1.0, 0.65, 0.5)   # each macro placed under these widths x the outline's (amendment of 2026-11-04, after a
                            # dry run: one shape per macro left no arrangement inside 250 x 200 um)


def macro_of(design: str, blocks: dict) -> dict:
    """{block: macro}: the xschem instance of the block's devices, or the block's own name when they span several."""
    h = json.loads((REPO / "circuits" / design / "upstream" / "hierarchy.json").read_text())
    inst = {e: x["instance"] for lv in h["levels"] for x in lv.get("top", []) for e in x["elements"]}
    out = {}
    for b, v in blocks.items():
        ms = {inst.get(d, "top") for d in v["devices"]}
        out[b] = ms.pop() if len(ms) == 1 else b
    return out


def fits(pl: dict, outline: list | None) -> bool:
    if not outline:
        return True
    x0, y0, x1, y1 = pl["bbox"]
    return x1 - x0 <= outline[0] + 1e-6 and y1 - y0 <= outline[1] + 1e-6


def _side(b, blocks):
    return "p" if blocks[b]["type"] == "pmos" else "n"


def _start(names: list, blocks: dict) -> list:
    """The starting rows: PMOS rows above the others; each symmetric block opens a row of its own, the others fill
    the rows in the given (S0) order, a new row when none is open."""
    rows = []
    for side in ("p", "n"):
        mine = [b for b in names if _side(b, blocks) == side]
        sym = [[b] for b in mine if blocks[b]["symmetric"]]
        rest = [b for b in mine if not blocks[b]["symmetric"]]
        side_rows = sym or ([[rest.pop(0)]] if rest else [])
        for k, b in enumerate(rest):
            side_rows[k % len(side_rows)].append(b)
        rows += side_rows
    return rows


def _valid_rows(rows: list, blocks: dict) -> bool:
    if any(not r for r in rows):
        return False
    sides = ["p" if all(_side(b, blocks) == "p" for b in r) else ("n" if all(_side(b, blocks) == "n" for b in r) else "x")
             for r in rows]
    return "x" not in sides and sides == sorted(sides, key=lambda s: s != "p")   # one side per row, PMOS rows first


def anneal(names: list, blocks: dict, max_len: dict, rule: str, outline: list | None, rng: random.Random,
           from_outside: bool = False) -> dict:
    """The best placement of `names` under `rule` ('budget_aware' or 'area_only') by simulated annealing."""
    a_ref = sum(min(v["geometry"]["area_um2"] for v in blocks[b]["variants"]) for b in names)
    rows = _start(names, blocks)
    choice = {b: (blocks[b]["variants"][0], False) for b in names}

    # A start outside the outline (iadc_ota's x1: every matched block opens a row, far taller than the tile) could never
    # move: every step outside was rejected. With `search_from_outside` (layout.yaml, opt-in: it also changes
    # ttsky25a_fd's narrower macro shapes, so the finished designs keep the old search until Imasha decides), a
    # placement outside the outline is then scored with a penalty that grows with its excess, so the search can walk
    # back inside; only placements inside are ever kept as the result (flow record row 96).
    soft = False

    def evaluate(rows, choice):
        pl = P.realise(rows, choice, blocks, shared_rows=True)
        if pl is None:
            return None, None, False
        c = P.cost(pl, a_ref, max_len)[rule]
        if fits(pl, outline):
            return pl, c, True
        if not soft:
            return None, None, False
        x0, y0, x1, y1 = pl["bbox"]
        over = max(0.0, (x1 - x0) / outline[0] - 1) + max(0.0, (y1 - y0) / outline[1] - 1)
        return pl, c + OUTSIDE * (1 + over), False
    pl, cur, inside = evaluate(rows, choice)
    if pl is None and outline and from_outside:
        soft = True
        pl, cur, inside = evaluate(rows, choice)
    if pl is None:   # not even a placement: keep searching from it, scored as very costly
        cur = 1e9
    best = (cur if inside else 1e9, pl if inside else None, [list(r) for r in rows], dict(choice))
    temp = T_START * (cur if cur < 1e9 else 1.0)
    for _ in range(MOVES):
        r2, c2 = [list(r) for r in rows], dict(choice)
        move = rng.randrange(4)
        b = rng.choice(names)
        if move == 0:                                   # swap two blocks
            o = rng.choice(names)
            ra = next(i for i, r in enumerate(r2) if b in r)
            rb = next(i for i, r in enumerate(r2) if o in r)
            ia, ib = r2[ra].index(b), r2[rb].index(o)
            r2[ra][ia], r2[rb][ib] = o, b
        elif move == 1:                                 # move a block to another row, or to a new one
            ra = next(i for i, r in enumerate(r2) if b in r)
            r2[ra].remove(b)
            k = rng.randrange(len(r2) + 1)
            if k == len(r2):
                r2.insert(rng.randrange(len(r2) + 1), [b])
            else:
                r2[k].insert(rng.randrange(len(r2[k]) + 1), b)
            r2 = [r for r in r2 if r]
        elif move == 2:                                 # another variant
            c2[b] = (rng.choice(blocks[b]["variants"]), c2[b][1])
        else:                                           # flip
            c2[b] = (c2[b][0], not c2[b][1])
        if not _valid_rows(r2, blocks):
            temp *= COOL
            continue
        pl2, new, in2 = evaluate(r2, c2)
        if pl2 is not None and (new < cur or rng.random() < math.exp(-(new - cur) / max(temp, 1e-12))):
            rows, choice, cur, pl = r2, c2, new, pl2
            if in2 and cur < best[0]:      # only a placement inside the outline is ever kept
                best = (cur, pl, [list(r) for r in rows], dict(choice))
        temp *= COOL
    return {"cost": best[0], "placement": best[1], "rows": best[2],
            "choice": {b: [v["id"], f] for b, (v, f) in best[3].items()}}


def place_macro(names: list, blocks: dict, max_len: dict, rule: str, outline: list | None,
                from_outside: bool = False) -> dict:
    """One macro under one cost: enumeration up to ENUM_MAX blocks, annealing beyond (seeded, so reproducible)."""
    sub = {b: blocks[b] for b in names}
    if len(names) <= ENUM_MAX:
        cands = [c for c in P.enumerate_candidates(sub, max_len) if fits(c["placement"], outline)]
        if not cands:
            return {"cost": None, "placement": None, "method": "enumeration", "n": 0}
        best = min(range(len(cands)), key=lambda i: (cands[i]["cost"][rule], i))
        return {"cost": cands[best]["cost"][rule], "placement": cands[best]["placement"], "method": "enumeration",
                "n": len(cands)}
    r = anneal(names, sub, max_len, rule, outline, random.Random(SEED), from_outside)
    return {**r, "method": "annealing", "n": MOVES}


def as_block(name: str, shapes: list, blocks: dict) -> dict:
    """A placed macro as one block for the top level: its bounding box, its blocks' pins and keep-outs, its axis at
    the centre of its box. place.local() reads the pins from `pins.list` (already placed)."""
    vs = []
    for sid, pl in shapes:   # each placed shape of the macro is one variant
        x0, y0, x1, y1 = pl["bbox"]
        pins, keep = [], []
        for b, p in pl["blocks"].items():
            pins += [{**q, "inner": b} for q in p["pins"]]
            keep += p.get("keepouts", [])
        vs.append({"id": sid, "geometry": {"bbox_um": [x0, y0, x1, y1], "row": [x0, y0, x1, y1],
                                           "area_um2": round((x1 - x0) * (y1 - y0), 3), "keepouts": keep},
                   "pins": {"list": pins, "tracks": {"top": {}, "bottom": {}}, "body": None}})
    pl = shapes[0][1]
    return {"type": "macro", "symmetric": False, "devices": [d for b in pl["blocks"] for d in blocks[b]["devices"]],
            "variants": vs}


def flatten(top: dict, shapes: dict) -> dict:
    """The top placement with every macro's blocks at their absolute place: each inner block shifted by its macro's
    origin, so assembly, routing and the checks see ordinary blocks."""
    flat = {}
    for m, p in top["blocks"].items():
        tx, ty = p["origin"]
        for b, q in shapes[m][p["variant"]]["placement"]["blocks"].items():
            flat[b] = {**q, "macro": m,
                       "origin": [round(q["origin"][0] + tx, 4), round(q["origin"][1] + ty, 4)],
                       "bbox": [round(q["bbox"][0] + tx, 4), round(q["bbox"][1] + ty, 4),
                                round(q["bbox"][2] + tx, 4), round(q["bbox"][3] + ty, 4)],
                       "axis_x": None if q.get("axis_x") is None else round(q["axis_x"] + tx, 4),
                       "pins": [{**x, **{k: round(x[k] + tx, 4) for k in ("x0", "x1", "rx0", "rx1") if k in x},
                                 "y": round(x["y"] + ty, 4)} for x in q["pins"]],
                       **({"keepouts": [{**k, "box": [round(k["box"][0] + tx, 4), round(k["box"][1] + ty, 4),
                                                      round(k["box"][2] + tx, 4), round(k["box"][3] + ty, 4)]}
                                        for k in q["keepouts"]]} if q.get("keepouts") else {})}
    return {"rows": top["rows"], "blocks": flat, "bbox": top["bbox"], "area_um2": top["area_um2"],
            "macros": {m: {"shape": p["variant"], "origin": p["origin"], "bbox": p["bbox"],
                           "rows": shapes[m][p["variant"]]["placement"]["rows"],
                           "method": shapes[m][p["variant"]]["method"], "macro_cost": shapes[m][p["variant"]]["cost"]}
                       for m, p in top["blocks"].items()}}


def hierarchical(design: str, blocks: dict, max_len: dict, rule: str, outline: list | None) -> dict:
    """The whole S5 placement of a design with its own hierarchy, under one cost: every macro placed, then every
    arrangement of the macros (no flips) inside the outline; the best flattened."""
    mof = macro_of(design, blocks)
    from src.s4.run import layout_options
    outside = bool(layout_options(design).get("search_from_outside"))   # row 96, opt-in
    groups = {}
    for b in blocks:
        groups.setdefault(mof[b], []).append(b)
    shapes = {}
    for m, names in groups.items():   # each macro under each width limit: its shapes, distinct ones kept
        for f in (SHAPES if outline else (1.0,)):
            lim = [outline[0] * f, outline[1]] if outline else None
            x = place_macro(names, blocks, max_len, rule, lim, outside)
            if x["placement"] is None:
                continue
            size = (round(x["placement"]["bbox"][2] - x["placement"]["bbox"][0], 3),
                    round(x["placement"]["bbox"][3] - x["placement"]["bbox"][1], 3))
            if all(size != y["size"] for y in shapes.get(m, {}).values()):
                shapes.setdefault(m, {})[f"w{int(round(f * 100))}"] = {**x, "size": size}
    bad = [m for m in groups if not shapes.get(m)]
    if bad:
        raise RuntimeError(f"no placement of macro(s) {bad} fits the outline {outline}")
    top_blocks = {m: as_block(m, [(sid, x["placement"]) for sid, x in shapes[m].items()], blocks) for m in groups}
    cands = [c for c in P.enumerate_candidates(top_blocks, max_len) if fits(c["placement"], outline)]
    if not cands:
        sizes = {m: [list(x["size"]) for x in shapes[m].values()] for m in groups}
        raise RuntimeError(f"no arrangement of the macros fits the outline {outline}; macro shapes (w, h) {sizes}")
    i = min(range(len(cands)), key=lambda k: (cands[k]["cost"][rule], k))
    flat = flatten(cands[i]["placement"], shapes)
    a_ref = sum(min(v["geometry"]["area_um2"] for v in blocks[b]["variants"]) for b in blocks)
    return {"placement": flat, "cost": P.cost(flat, a_ref, max_len), "index": i, "n_top": len(cands),
            "macro_of": mof}
