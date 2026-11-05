"""S4 under layout rule set v2, phase 2 (docs/rules_v2/ruleset_v2.md, sections 3 and 7; PREREG amendment of
2026-11-05): the blocks of Imasha's hierarchy drawing, the designer's dummies at their block's row ends, 2-D
arrangements, and the screening that keeps 2-3 candidates per block for sign-off.

* Blocks (P1, I1): layout.yaml `blocks:` lists them as Imasha drew them (one coloured box = one block), each with its
  devices, its designer dummies and its matching level. Every other device keeps the v1 plan's block; every
  capacitor too. S1's matching groups are not used to cut blocks (they stay S1's cross-check).
* Arrangements (M1-M8): a block's units in r rows (r = 1 is v1's single row). Each row holds the same share of every
  matched device; the row is a common-centroid sequence (palindromic: A B B A), or, where no palindrome exists, an
  interdigitated one with every second row reversed (A B / B A: the cross-quad), so each device's centroid falls on
  the array's centre in x and y. A single device is folded into r rows. Series strings (devices joined drain to
  source with one gate, as x1's cm stack) keep one string per row, as drawn. The right half of each row is the
  mirror image, so each device has as many left- as right-facing units (orientation balance). r is kept where every
  row has at least two units and every share is whole.
* Dummies (Y1-Y3): the designer's dummy units go to the row ends (left, right, next row, ...); rows left shorter are
  padded with the flow's own dummy (the neighbour's cell, every terminal on the body) so every row has the same
  units and the tap strips line up.
* Screening (M5, Imasha Q4): every candidate is laid out on paper (src/s4/block.py, no Magic) and scored by its box
  area, its wiring (track and stub lengths) and its crossings (stubs passing other nets' tracks). Kept: the smallest,
  the least-wired and the best of the strictest arrangement the matching level asks for (2-D common centroid when the
  level is `centroid`), filled to three with the squarest; only those are drawn and signed off. A kept candidate whose
  signed-off area misses its estimate by more than 15 % (ASSUMPTION) brings in the next candidate (S4's main).
All lengths in um.
"""
from __future__ import annotations

import json
from pathlib import Path

from src.s3 import options as O
from src.s4 import block as B

KEEP = 3
EST_TOL = 0.15
MAX_ROWS = 12


# ---------------------------------------------------------------------------------------------------- blocks
def plan_blocks(ir: dict, opts: dict, v1_plan: list) -> list:
    devs = {d["name"]: d for d in ir["devices"]}
    out, used = [], set()
    for b in opts.get("blocks") or []:
        ds, dm = list(b["devices"]), list(b.get("dummies") or [])
        tb = {(devs[x]["type"], devs[x]["terminals"]["b"]) for x in ds + dm}
        if len(tb) != 1:
            raise RuntimeError(f"layout.yaml block {b['name']}: one device type and body per block, got {sorted(tb)}")
        (ty, body), = tb
        out.append({"name": b["name"], "kind": b.get("kind") or "group", "type": ty, "body": body, "devices": ds + dm,
                    "matched": ds, "dummies": dm, "level": b.get("level") or opts.get("matching"),
                    "drawn": b.get("drawn")})
        used |= set(ds + dm)
    for b in v1_plan:                                  # every other element keeps v1's block
        rest = [x for x in b["devices"] if x not in used]
        if rest:
            out.append({**b, "devices": rest})
    return out


# ----------------------------------------------------------------------------------------------- arrangements
def strings(names: list, devs: dict) -> list | None:
    """Series strings: chains drain -> source of one gate net, each starting where no other member's source feeds
    it; None unless every member is in a chain of two or more and all chains are equally long."""
    src = {devs[n]["terminals"]["s"]: n for n in names}
    starts = [n for n in names if devs[n]["terminals"]["d"] not in src or src.get(devs[n]["terminals"]["d"]) == n]
    chains, seen = [], set()
    for s in sorted(starts):
        ch, cur = [], s
        while cur and cur not in seen:
            ch.append(cur)
            seen.add(cur)
            nxt = [m for m in names if devs[m]["terminals"]["d"] == devs[cur]["terminals"]["s"] and m not in seen]
            cur = nxt[0] if len(nxt) == 1 else None
        chains.append(ch)
    if seen != set(names) or len({len(c) for c in chains}) != 1 or len(chains[0]) < 2 or len(chains) < 2:
        return None
    if len({devs[n]["terminals"]["g"] for n in names}) != 1:
        return None
    return chains


def _row_seq(per: dict, style: str) -> tuple[list, bool]:
    """(sequence, palindromic) of one row with per[d] units of each device."""
    from src.s4.run import centroid_sequence, interdigitated
    if style == "cc":
        seq = centroid_sequence(per)
        if seq:
            return seq, True
    seq = interdigitated(per)
    return seq, seq == seq[::-1]


def arrangements(names: list, counts: dict, devs: dict) -> list:
    """[(id, [[device, ...] per row], strictness)]: 3 = 2-D common centroid, 2 = 1-D common centroid, 1 =
    interdigitated, 0 = folded single device or strings."""
    out = []
    if len(names) == 1:
        n = counts[names[0]]
        for r in range(1, min(MAX_ROWS, n // 2) + 1):
            if n % r == 0:                             # equal rows: no padding, the tap strips line up
                out.append((f"f{r}", [[names[0]] * (n // r) for _ in range(r)], 0))
        return out or [("A", [[names[0]] * n], 0)]
    ch = strings(names, devs) if all(counts[n] == 1 for n in names) else None
    if ch:
        out.append((f"strings{len(ch)}", ch, 0))
        out.append(("strings1", [[x for c in ch for x in c]], 0))
    for r in range(1, MAX_ROWS + 1):
        if any(counts[d] % r for d in names):
            continue
        per = {d: counts[d] // r for d in names}
        if sum(per.values()) < 2:
            continue
        for style in ("cc", "id"):
            seq, pal = _row_seq(per, style)
            if r % 2 and not pal and r > 1:
                continue                               # an odd number of rows needs palindromic rows
            if r == 1 and not pal and style == "cc":
                continue
            rows = [seq if (k % 2 == 0 or pal) else seq[::-1] for k in range(r)]
            # rows paired (S, S reversed) or palindromic: every centroid on the array's centre in x and y
            strict = 1 if (r == 1 and not pal) else (3 if r >= 2 else 2)
            vid = "XQ" if (r == 2 and all(v == 1 for v in per.values()) and len(names) == 2) else f"{style}{r}"
            if not any(vid == o[0] or rows == o[1] for o in out):
                out.append((vid, rows, strict))
    return out


def _units(rows: list, unit_of, mirror_rows: bool = True) -> list:
    """Unit dicts row by row; the right half of each row mirrored (orientation balance)."""
    out = []
    for row in rows:
        n = len(row)
        out.append([unit_of(d, mirror_rows and k >= n - n // 2) for k, d in enumerate(row)])
    return out


def with_designer_dummies(rows: list, dummy_units: list, body: str, flow_dummies: bool) -> list:
    """The designer's dummy units to the row ends (row 0 left, row 0 right, row 1 left, ...); then every row padded
    to the longest with the flow's dummy (the neighbour's cell, all terminals on the body), and, when the layout asks
    for dummies and a row has none at an end, one there too (Y3: never beside a designer dummy)."""
    left = [[] for _ in rows]
    right = [[] for _ in rows]
    for k, u in enumerate(dummy_units):
        slot = k % (2 * len(rows))
        (left if slot % 2 == 0 else right)[slot // 2].append(u)
    k_flow = [0]

    def flow(u):
        k_flow[0] += 1
        return {"device": f"DUMMY{k_flow[0] - 1}", "rec": u["rec"], "mirror": u["mirror"], "dummy_of": u["device"],
                "nets": {t: body for t in u["nets"]}}
    if flow_dummies:
        for i, row in enumerate(rows):
            if not left[i]:
                left[i].append(flow(row[0]))
            if not right[i]:
                right[i].append(flow(row[-1]))
    full = [left[i] + row + right[i] for i, row in enumerate(rows)]
    n = max(len(r) for r in full)
    for i, r in enumerate(full):
        while len(r) < n:                              # equal rows: the strips line up through the array
            if len(left[i]) <= len(right[i]):
                r.insert(0, flow(r[0]))
                left[i].append(None)
            else:
                r.append(flow(r[-1]))
                right[i].append(None)
    return full


def candidates(blk: dict, ir: dict, dec: dict, cells: Path, rules: dict, opts: dict) -> list:
    """Every arrangement of a v2 block as an S4 variant: {'id', 'units' (row after row), 'rows', 'strict'}."""
    from src.s4.run import half_unit
    devs = {d["name"]: d for d in ir["devices"]}
    types = O.device_types(ir)
    tid_of = {d: t for t, v in types.items() for d in v["devices"]}
    matched = blk.get("matched") or blk["devices"]
    dummies = blk.get("dummies") or []

    def rec(d):
        return json.loads((cells / dec[tid_of[d]]["cell"] / "record.json").read_text())

    def unit(d, r, mirror):
        t = devs[d]["terminals"]
        return {"device": d, "rec": r, "mirror": mirror, "nets": {"D": t["d"], "G": t["g"], "S": t["s"]}}
    counts = {d: devs[d].get("m") or 1 for d in matched}
    recs = {d: rec(d) for d in matched + dummies}
    ar = arrangements(matched, counts, devs)
    # one copy each of two devices: the half units make ABBA, ABAB and the cross-quad (A B / B A) possible
    if len(matched) == 2 and all(c == 1 for c in counts.values()) and len({tid_of[d] for d in matched}) == 1:
        h = half_unit(types[tid_of[matched[0]]], tid_of[matched[0]], recs[matched[0]]["option"], cells, rules)
        if h:
            recs = {**recs, **{d: h[0] for d in matched}}
            ar = arrangements(matched, {d: 2 for d in matched}, devs)
    if (blk.get("level") or opts.get("matching")) == "centroid":
        ar = [a for a in ar if a[2] >= 1 or len(matched) == 1 or a[0].startswith("strings")]
    dunits = [unit(d, recs[d], False) for d in dummies for _ in range(devs[d].get("m") or 1)]
    out = []
    for vid, rows, strict in ar:
        urows = _units(rows, lambda d, m: unit(d, recs[d], m))
        urows = with_designer_dummies(urows, dunits, blk["body"], bool(opts.get("dummies")))
        out.append({"id": vid, "units": [u for r in urows for u in r], "rows": len(urows), "strict": strict})
    return out


# -------------------------------------------------------------------------------------------------- screening
def geometry(v: dict, lu: float | None, bo: bool, internal: set | None = None) -> dict:
    """The generator's geometry, as S4's build_variant makes it (one row: short tracks for internal nets)."""
    return B.layout_array(v["units"], v["rows"], tap_limit=lu, bbox_origin=bo) if v["rows"] > 1 else \
        B.layout(v["units"], tap_limit=lu, internal=internal, bbox_origin=bo)


def estimate(v: dict, dtype: str, lu: float | None, bo: bool, internal: set | None = None) -> dict:
    """Box area (the ring plus the n-well or the p-implant beyond it), wiring (tracks, stubs, columns) and crossings
    of an arrangement, from the generator's own geometry, before anything is drawn."""
    g = geometry(v, lu, bo, internal)
    m = B.NWELL_OVER if dtype == "pmos" else 0.21
    x0, y0, x1, y1 = g["ring"]
    w, h = x1 - x0 + 2 * m, y1 - y0 + 2 * m
    tracks = [(side, n, y) for side in ("top", "bottom") for n, y in g["tracks"][side].items()]
    tracks += [(t["side"], t["net"], t["y"]) for t in g.get("inner_tracks", [])]
    span = g["track_span"][1] - g["track_span"][0]
    short = {side: (g.get("spans") or {}).get(side, {}) for side in ("top", "bottom")}
    wire = sum((short[sd][n][1] - short[sd][n][0]) if n in short.get(sd, {}) else span for sd, n, _ in tracks)
    cross = 0
    for u in g["units"]:
        for s in u["stubs"]:
            ty = s.get("ty", g["tracks"][s["side"]].get(s["net"], s["edge"]))
            wire += abs(ty - s["edge"])
            lo, hi = sorted((s["edge"], ty))
            cross += sum(1 for _, n, y in tracks if n != s["net"] and lo < y < hi)
    for n, (cx, ys) in (g.get("col_spans") or {}).items():
        wire += max(ys) - min(ys)
    from src.s4.run import tap_distance
    return {"area_um2": round(w * h, 2), "w_um": round(w, 3), "h_um": round(h, 3), "wire_um": round(wire, 1),
            "crossings": cross, "tap_distance_um": tap_distance(g), "strips_aligned": _strips_aligned(g)}


def _strips_aligned(g: dict) -> bool:
    """A tap strip runs through the whole ring: in an array it must not cut through a unit of any row."""
    return all(not (u["x"] < s < u["x"] + u["w"]) for s in g["strips"] for u in g["units"])


def screen(blk: dict, vs: list, lu: float | None, bo: bool, outline: list | None = None,
           internal: set | None = None) -> tuple[list, list]:
    """(kept, record): up to KEEP candidates, as the module says; the record lists every candidate's estimate. With
    a hard outline, a candidate wider or taller than it is not one (it could never be placed)."""
    rec = []
    for v in vs:
        try:
            e = estimate(v, blk["type"], lu, bo, internal)
        except Exception as ex:   # noqa: BLE001 - an arrangement the generator cannot lay out is not a candidate
            e = {"error": str(ex)[:200]}
        ok = "error" not in e and e["strips_aligned"] and (lu is None or e["tap_distance_um"] is None
                                                            or e["tap_distance_um"] <= lu)
        if ok and outline and (e["w_um"] > outline[0] or e["h_um"] > outline[1]):
            ok, e = False, {**e, "why": "larger than the outline"}
        rec.append({"id": v["id"], "rows": v["rows"], "strict": v["strict"], **e, "valid": ok})
    good = [(v, r) for v, r in zip(vs, rec) if r["valid"]]
    if not good:
        return [], rec
    by_area = min(good, key=lambda x: (x[1]["area_um2"], x[1]["wire_um"]))
    by_wire = min(good, key=lambda x: (x[1]["wire_um"], x[1]["area_um2"]))
    top = max(r["strict"] for _, r in good)
    strict = min((x for x in good if x[1]["strict"] == top), key=lambda x: (x[1]["area_um2"] + x[1]["wire_um"] * 0.1))
    kept = []
    for x in (by_area, by_wire, strict):
        if all(x[0]["id"] != k[0]["id"] for k in kept):
            kept.append(x)
    rest = sorted((x for x in good if all(x[0]["id"] != k[0]["id"] for k in kept)),
                  key=lambda x: abs(1 - x[1]["w_um"] / x[1]["h_um"]) if x[1]["w_um"] < x[1]["h_um"] else
                  abs(1 - x[1]["h_um"] / x[1]["w_um"]))
    while len(kept) < KEEP and rest:
        kept.append(rest.pop(0))
    ids = [k[0]["id"] for k in kept]
    for r in rec:
        r["kept"] = r["id"] in ids
    order = [v for v, _ in good if v["id"] not in ids]
    return [k[0] for k in kept], rec + [{"spares": [v["id"] for v in order]}]
