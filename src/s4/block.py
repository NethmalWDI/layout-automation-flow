"""S4 — one block: a row of S3 unit cells, wired on a track grid and closed by one guard ring (plan v4, section 2).

Template (generator code, not search; decision D8):
  * The units (S3's ringless cells) stand in one row, GAP apart; a unit marked 'mirror' is flipped about its
    vertical axis (Magic places an instance's bounding box at the box corner, flipped or not).
  * Every pin of a unit goes up (top side) or down (bottom side) on a met2 stub to one met3 TRACK per net. A met1 pin
    (gate pad, the strip of a single-finger cell) first gets a met1 patch and a via1; the strips of a single-finger
    cell go down, its gate up. The tracks run the whole block and EXT past the ring, so S5 can reach them from
    either side; each carries its net's label. A net with pins on both sides gets a met2 column, right of the row,
    joining its two tracks.
  * One tap ring around everything, drawn by the PDK's own sky130::guard_ring_draw: a p-tap (NMOS), or an n-tap in
    an n-well that covers the whole block (PMOS). It is labelled '<body>_body'; S5 ties it to the body net. The ring
    is what meets the tap rules S3 deferred (LU.2, LU.3, nwell.4), so the block's DRC defers nothing.
  * Where a row is too wide for the ring alone to keep every diffusion within S2's latch-up tap distance, a vertical
    tap STRIP (one side of the ring, drawn the same way) stands between two units, TAP_GAP from each, and joins the
    ring at both ends (plan v4 Phase 6; LOADBench's PMOS bank). A row that meets the distance gets no strip.
A MIM capacitor bound in S0's layout view (circuit_ir passives[].layout_binding) is a block of its own (cap_*): the
PDK's generator draws it, and each plate goes out to a met3 track on a met4 neck and a via3 (the top plate up, the
bottom plate's met4 strip down). It has no ring; its met3 plate and met4 are keep-outs S5's router respects.
Magic draws the block, so its contact rules apply; Magic DRC (full) and Netgen LVS against the IR's devices sign it off.
All lengths are in um.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from src.common import pcell
from src.common.tools import REPO, TOOL_ENV, rel

MAG_UNIT = 0.005     # um per Magic internal unit with magscale 1 2 (unit_pins reads each file's own scale)
GAP = 0.6            # between unit bounding boxes
SLOT_MIN = 0.26      # a stub's distance from its unit's edge, and the least distance between two stubs of a unit
STUB_W = 0.2         # met2 stub width
VIA1 = (0.26, 0.32)  # m2c (via1 with its met1/met2 surround), as in src/s3/strap.py
PATCH = 0.36         # met1 patch under a via1 on a met1 pin
VIA2 = 0.4           # m3c (via2 with surround), square
TRACK_W = 0.4        # met3 track width
PITCH = 0.9          # between track centres
FIRST = 1.0          # from the row's edge to the first track's centre (room for the via1 patches)
RING_GAP = 0.8       # from the outermost track or unit to the ring's centre line
EXT = 1.0            # how far each track runs past the ring
COL0, COL_PITCH = 0.8, 0.8   # met2 columns joining a net's top and bottom tracks, right of the row
NWELL_OVER = 0.5     # n-well beyond the ring's centre line (PMOS blocks)
TAP_GAP = 0.8        # from a unit's edge to a tap strip's centre line (as RING_GAP to the ring)
TAP_MARGIN = 0.5     # the strips keep every diffusion this much inside S2's latch-up distance
VIA3 = 0.4           # via3 with its met3/met4 surround, as in src/s5/route.py
MET_SPACE = 0.3      # met3 and met4 spacing around a capacitor's keep-outs (S5's MET3_SPACE)
CAPM_SPACE = 1.45    # from the MIM top plate (capm) to any met3 it does not own: capm.11 asks 1.34


def unit_pins(rec: dict) -> dict:
    """{name: {'layer', 'rect'}} of a unit cell, from its .mag labels; a single-finger strip label (met1, mid-height)
    is widened to the whole strip from S3's geometry record."""
    cell = rec["cell"]
    if rec.get("pins"):   # a unit that is not an S3 transistor cell (a resistor) carries its pins (plan v4 Phase 8)
        return {k: dict(v) for k, v in rec["pins"].items()}
    mag = (REPO / rec["gds"]).with_suffix(".mag").read_text()
    # Magic writes 'magscale 1 2' only when a cell has half-lambda geometry; without it a unit is 0.01 um
    # (ttsky25a_fd's cells; plan v4 Phase 8)
    ms = re.search(r"^magscale\s+(\d+)\s+(\d+)", mag, re.M)
    unit = 0.01 * int(ms.group(1)) / int(ms.group(2)) if ms else 0.01
    pins = {}
    for m in re.finditer(r"^rlabel\s+(\S+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+\d+\s+(\S+)", mag, re.M):
        layer, *xy, name = m.groups()
        pins[name] = {"layer": layer, "rect": [int(v) * unit for v in xy]}
    for s in rec["geometry"]["strips"]:
        p = pins.get(s["role"])
        if p and p["layer"] == "metal1":
            p["rect"] = [s["x0"], s["y0"], s["x1"], s["y1"]]
    if not {"D", "G", "S"} <= set(pins):
        raise RuntimeError(f"{cell}: pins {sorted(pins)} lack D, G or S")
    return pins


def stub_plan(pins: dict, w: float, h: float) -> dict:
    """Local x of the stub and the side (top/bottom) for each of D, G, S. met1 pins are placed first (their x is
    fixed by the pad or strip), then each met2 bar at the x within its span farthest from the stubs already placed."""
    plan = {}
    terms = ("G", "D", "S") if {"G", "D", "S"} <= set(pins) else tuple(pins)
    for t in terms:
        p = pins[t]
        if p["layer"] == "metal1":   # the gate pad on its own side; a single-finger cell's strips go down; another
            x0, y0, x1, y1 = p["rect"]   # unit's (a resistor's end) on its own side
            side = ("top" if (y0 + y1) / 2 > h / 2 else "bottom") if t not in ("D", "S") else "bottom"
            plan[t] = {"x": round((x0 + x1) / 2, 3), "side": side, "kind": "met1"}
    for t in terms:
        if t in plan:
            continue
        x0, y0, x1, y1 = pins[t]["rect"]
        side = "top" if (y0 + y1) / 2 > h / 2 else "bottom"
        taken = [v["x"] for v in plan.values() if v["side"] == side]
        lo, hi = max(x0, 0) + SLOT_MIN, min(x1, w) - SLOT_MIN
        cands = [round(lo + k * 0.005, 3) for k in range(int((hi - lo) / 0.005) + 1)] or [round((x0 + x1) / 2, 3)]
        x = max(cands, key=lambda c: (min([abs(c - t_) for t_ in taken] or [1e9]), -abs(c - (lo + hi) / 2)))
        plan[t] = {"x": x, "side": side, "kind": "met2"}
    def clash(side):   # two via1 patches (PATCH wide) need met1's 0.14 um between them (plan v4 Phase 8: was
        xs = sorted(v["x"] for v in plan.values() if v["side"] == side)   # 2 SLOT_MIN = 0.52, a stricter margin)
        return any(b - a < PATCH + 0.14 - 1e-9 for a, b in zip(xs, xs[1:]))
    # a single-finger strip runs the cell's whole height: when its stub at the bottom comes too close to another
    # (a gate pad at the bottom, ttsky25a_fd's L = 2 cells), it is taken at the top instead (plan v4 Phase 8)
    for t in ("D", "S"):
        if clash("bottom") and t in plan and plan[t]["kind"] == "met1" and plan[t]["side"] == "bottom":
            y0, y1 = pins[t]["rect"][1], pins[t]["rect"][3]
            if y1 - y0 > 0.8 * h:
                plan[t]["side"] = "top"
                if clash("top"):
                    plan[t]["side"] = "bottom"
    for side in ("top", "bottom"):
        if clash(side):
            xs = sorted(v["x"] for v in plan.values() if v["side"] == side)
            raise RuntimeError(f"stubs too close on the {side} side: {xs}")
    return plan


def layout(units: list, tap_limit: float | None = None, internal: set | None = None) -> dict:
    """units: [{'device', 'rec', 'mirror', 'nets': {'D','G','S'}}] left to right. Returns the geometry: unit origins,
    the stubs (x, pin edge, side, net), the tracks per side, the ring box, the tap strips and the block's extent.
    With tap_limit (S2's place.latchup_tap_distance), a strip goes between two units wherever the taps on either side
    of a unit would otherwise stand more than 2 (tap_limit - TAP_MARGIN) apart."""
    plans = []
    for u in units:
        w, h = u["rec"]["geometry"]["bbox_um"]
        pins = unit_pins(u["rec"])
        plans.append((u, w, h, pins, stub_plan(pins, w, h)))
    sides = {}
    for u, *_, sp in plans:
        for t, s in sp.items():
            sides.setdefault(u["nets"][t], set()).add(s["side"])
    n_cols = sum(1 for v in sides.values() if len(v) == 2)
    col_ext = COL0 + (n_cols - 1) * COL_PITCH if n_cols else 0.0   # the right ring moves out past the columns
    reach = 2 * (tap_limit - TAP_MARGIN) if tap_limit else None
    # the ring's lines above and below (as computed further down): a unit whose every point is within reach of one
    # of them needs no strip
    n_top, n_bot = (sum(1 for v in sides.values() if side in v) for side in ("top", "bottom"))
    hmax = max(p[2] for p in plans)
    ry1 = hmax + (FIRST + (n_top - 1) * PITCH if n_top else 0.0) + RING_GAP
    ry0 = -(FIRST + (n_bot - 1) * PITCH if n_bot else 0.0) - RING_GAP

    def far_from_ring(h):
        y = min(max((ry0 + ry1) / 2, 0.0), h)
        return reach is not None and min(y - ry0, ry1 - y) > reach / 2
    x, placed, strips, last_tap = 0.0, [], [], -RING_GAP
    for i, (u, w, h, pins, sp) in enumerate(plans):
        if reach and placed and far_from_ring(h):
            nxt = x + w + (col_ext if i == len(plans) - 1 else 0.0) + RING_GAP   # the nearest tap right of the unit
            if nxt - last_tap > reach:
                last_tap = round(x - GAP + TAP_GAP, 3)
                strips.append(last_tap)
                x = last_tap + TAP_GAP
        def gx(lx): return round(x + (w - lx if u["mirror"] else lx), 3)   # noqa: E731
        stubs = []
        for t, s in sp.items():
            x0, y0, x1, y1 = pins[t]["rect"]
            stubs.append({"device": u["device"], "term": t, "net": u["nets"][t], "x": gx(s["x"]), "side": s["side"],
                          "kind": s["kind"], "edge": y1 if s["side"] == "top" else y0, "pin_rect_y": [y0, y1]})
        placed.append({**u, "x": round(x, 3), "w": w, "h": h, "stubs": stubs})
        x += w + GAP
    row_w, row_h = round(x - GAP, 3), max(p["h"] for p in placed)
    tracks, spans = {}, {}
    internal = internal or set()
    for side in ("top", "bottom"):
        nets, xs = [], {}
        for p in placed:
            for s in sorted(p["stubs"], key=lambda s: s["x"]):
                if s["side"] == side:
                    xs.setdefault(s["net"], []).append(s["x"])
                    if s["net"] not in nets:
                        nets.append(s["net"])
        # a net only this block uses (internal) gets a short track, packed with others in rows nearest the units
        # (left-edge assignment; plan v4 Phase 8); every other net a track across the block, outside them
        rows = []
        for n in sorted((n for n in nets if n in internal), key=lambda n: min(xs[n])):
            lo, hi = min(xs[n]) - 0.5, max(xs[n]) + 0.5
            k = next((i for i, r in enumerate(rows) if r < lo - 0.6), None)
            if k is None:
                rows.append(hi)
                k = len(rows) - 1
            rows[k] = hi
            spans[n] = [round(lo, 3), round(hi, 3), k]
        ext = [n for n in nets if n not in internal]
        order = {n: spans[n][2] for n in nets if n in internal} | {n: len(rows) + i for i, n in enumerate(ext)}
        tracks[side] = {n: round(row_h + FIRST + order[n] * PITCH, 3) if side == "top" else round(-FIRST - order[n] * PITCH, 3)
                        for n in nets}
    # a net with pins on both sides: a met2 column right of the row joins its top and bottom tracks
    both = [n for n in tracks["top"] if n in tracks["bottom"]]
    columns = {n: round(row_w + COL0 + k * COL_PITCH, 3) for k, n in enumerate(both)}
    top = max(tracks["top"].values(), default=row_h) + RING_GAP
    bot = min(tracks["bottom"].values(), default=0.0) - RING_GAP
    right = max([row_w] + list(columns.values())) + RING_GAP
    ring = [round(-RING_GAP, 3), round(bot, 3), round(right, 3), round(top, 3)]
    for n, x in columns.items():                    # an internal net's short track reaches its column
        if n in spans:
            spans[n][1] = max(spans[n][1], x + 0.3)
    return {"units": placed, "row": [0.0, 0.0, row_w, row_h], "tracks": tracks, "columns": columns, "ring": ring,
            "strips": strips, "track_span": [round(ring[0] - EXT, 3), round(ring[2] + EXT, 3)],
            "spans": {n: v[:2] for n, v in spans.items()}}


def _b(x0, y0, x1, y1) -> str:
    return f"box {x0:.3f}um {y0:.3f}um {x1:.3f}um {y1:.3f}um"


def tcl(name: str, geo: dict, dtype: str, body_net: str) -> str:
    """dtype 'pmos' or 'nmos'. Draws the block in Magic and writes <name>.mag and <name>.gds in the working folder."""
    c = ["drc off", "snap internal"]
    for g in sorted({REPO / u["rec"]["gds"] for u in geo["units"]}):
        c.append(f"gds read {g}")
    c += [f"load {name} -silent", "tech unlock *"]
    for u in geo["units"]:
        c += [_b(u["x"], 0, u["x"], 0), f"getcell {u['rec']['cell']}" + (" h" if u["mirror"] else "")]
    for u in geo["units"]:
        for s in u["stubs"]:
            ty = geo["tracks"][s["side"]][s["net"]]
            x, up = s["x"], s["side"] == "top"
            if s["kind"] == "met1":   # met1 patch with a via1: outward from a gate pad, inside a strip's end
                back = 0.2 if s["term"] == "G" else PATCH
                y_in = s["edge"] - back if up else s["edge"] + back
                y_out = y_in + PATCH if up else y_in - PATCH
                c += [_b(x - PATCH / 2, min(y_in, y_out), x + PATCH / 2, max(y_in, y_out)), "paint metal1"]
                vy = (y_in + y_out) / 2
                c += [_b(x - VIA1[0] / 2, vy - VIA1[1] / 2, x + VIA1[0] / 2, vy + VIA1[1] / 2), "paint m2c"]
                y_from = vy
            else:                     # met2 bar: the stub starts inside it
                y_from = s["edge"] - 0.1 if up else s["edge"] + 0.1
            c += [_b(x - STUB_W / 2, min(y_from, ty), x + STUB_W / 2, max(y_from, ty)), "paint metal2"]
            c += [_b(x - VIA2 / 2, ty - VIA2 / 2, x + VIA2 / 2, ty + VIA2 / 2), "paint m3c"]
    for net, cx in geo.get("columns", {}).items():
        yb, yt = geo["tracks"]["bottom"][net], geo["tracks"]["top"][net]
        c += [_b(cx - STUB_W / 2, yb, cx + STUB_W / 2, yt), "paint metal2"]
        for ty in (yb, yt):
            c += [_b(cx - VIA2 / 2, ty - VIA2 / 2, cx + VIA2 / 2, ty + VIA2 / 2), "paint m3c"]
    for side in ("top", "bottom"):
        for net, ty in geo["tracks"][side].items():
            x0, x1 = geo.get("spans", {}).get(net) or geo["track_span"]
            c += [_b(x0, ty - TRACK_W / 2, x1, ty + TRACK_W / 2), "paint metal3",
                  _b(x0 + 0.1, ty - 0.05, x0 + 0.2, ty + 0.05), f"label {net} c metal3"]
    rx0, ry0, rx1, ry1 = geo["ring"]
    if dtype == "pmos":
        c += [_b(rx0 - NWELL_OVER, ry0 - NWELL_OVER, rx1 + NWELL_OVER, ry1 + NWELL_OVER), "paint nwell"]
    ctype, dtype_ = ("nsc", "nsd") if dtype == "pmos" else ("psc", "psd")
    c += [_b(rx0, ry0, rx1, ry1), f"sky130::guard_ring_draw {ctype} {dtype_}"]
    for sx in geo.get("strips", []):   # one side of the ring, as sky130::guard_ring_draw paints it
        c += [_b(sx - 0.085, ry0 - 0.085, sx + 0.085, ry1 + 0.085), "paint li",
              _b(sx - 0.085, ry0 + 0.215, sx + 0.085, ry1 - 0.215), f"paint {ctype}",
              _b(sx - 0.085, ry0 - 0.085, sx + 0.085, ry1 + 0.085), f"paint {dtype_}"]
    xm = (rx0 + rx1) / 2
    c += [_b(xm - 0.05, ry0 - 0.05, xm + 0.05, ry0 + 0.05), f"label {body_net}_body c locali"]
    c += ["tech revert", f"save {name}", f"gds write {name}", "quit -noprompt"]
    return "\n".join(c) + "\n"


def build(name: str, geo: dict, dtype: str, body_net: str, out: Path) -> dict:
    """Draw the block in out/ and return {'gds', 'rc', 'log'}."""
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob(f"{name}.*"):
        f.unlink()
    (out / "build.tcl").write_text(tcl(name, geo, dtype, body_net))
    r = subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", pcell.MAGICRC, str(out / "build.tcl")],
                       cwd=out, env=TOOL_ENV, capture_output=True, text=True, timeout=600)
    (out / "build_magic.log").write_text(r.stdout + r.stderr)
    gds = out / f"{name}.gds"
    return {"gds": rel(gds) if gds.exists() else None, "rc": r.returncode, "log": rel(out / "build_magic.log")}


def cap_cell(name: str, model: str, params: dict, out: Path) -> dict:
    """The PDK's capacitor drawn alone (outputs/S4/<d>/blocks/<block>/<name>.gds) and, per unit, its plates read from
    the GDS: the met3 bottom plate, capm, the met4 over the top plate (the larger met4 shape) and the bottom plate's
    met4 strip. A binding with M > 1 (ttsky25a_fd: 5 units of 10 x 10 um) is drawn as M units in a row (nx = M; plan v4
    Phase 8); without M, as before."""
    import klayout.db as kdb
    gp = {k.lower(): v for k, v in params.items() if k.upper() in ("W", "L")}
    n = int(float(params.get("M") or params.get("m") or 1))
    if n > 1:
        gp.update({"nx": n, "ny": 1})
    g = pcell.generate([{"cell": name, "model": model, "params": gp}], out)
    if name not in g["gds"]:
        return {"gds": None, "log": g["log"]}
    ly = kdb.Layout()
    ly.read(g["gds"][name])
    top = ly.top_cell()
    o = top.bbox()

    def boxes(layer, dt):
        return [[round((b.left - o.left) * ly.dbu, 3), round((b.bottom - o.bottom) * ly.dbu, 3),
                 round((b.right - o.left) * ly.dbu, 3), round((b.top - o.bottom) * ly.dbu, 3)]
                for b in (p.bbox() for p in kdb.Region(top.begin_shapes_rec(ly.layer(layer, dt))).merged().each())]
    m3, m4, capm = boxes(70, 20), boxes(71, 20), sorted(boxes(89, 44))
    units = []
    for c in capm:   # each unit: the shapes that overlap its plate (met3 plate and met4 strip extend past capm)
        mine3 = [b for b in m3 if b[0] <= c[2] and b[2] >= c[0]]
        plate = next(b for b in mine3 if b[0] <= c[0] and b[2] >= c[2])
        mine4 = sorted((b for b in m4 if b[0] < plate[2] and b[2] > plate[0]),
                       key=lambda b: (b[2] - b[0]) * (b[3] - b[1]), reverse=True)
        if len(mine4) != 2:
            raise RuntimeError(f"{name}: a unit needs two met4 shapes, got {len(mine4)}")
        units.append({"plate_m3": plate, "capm": c, "top_m4": mine4[0], "bottom_m4": mine4[1]})
    if len(units) != n or len(m3) != n:
        raise RuntimeError(f"{name}: expected {n} units, got {len(units)} capm and {len(m3)} met3 plates")
    return {"gds": rel(Path(g["gds"][name])), "log": g["log"], "units": units, **units[0],
            "bbox": [0.0, 0.0, round(o.width() * ly.dbu, 3), round(o.height() * ly.dbu, 3)]}


def cap_layout(cc: dict, top_net: str, bottom_net: str) -> dict:
    """A capacitor block's geometry: the cell at the origin, every unit's top plate on a top track, every bottom
    plate on a bottom track, each reached by a met4 neck and a via3; the keep-outs S5's router must respect."""
    us = cc.get("units") or [cc]
    yt = round(max(max(u["plate_m3"][3] for u in us) + FIRST, max(u["capm"][3] for u in us) + CAPM_SPACE + TRACK_W / 2), 3)
    yb = round(min(min(u["plate_m3"][1] for u in us) - FIRST, min(u["capm"][1] for u in us) - CAPM_SPACE - TRACK_W / 2), 3)
    g3 = CAPM_SPACE - MET_SPACE - 0.05   # S5 adds MET_SPACE: other met3 stays 1.4 um from capm
    keep, necks, vias = [], [], []
    for u in us:
        (px0, py0, px1, py1), (cx0, cy0, cx1, cy1) = u["plate_m3"], u["capm"]
        t, b = u["top_m4"], u["bottom_m4"]
        xt, xb = round((t[0] + t[2]) / 2, 3), round((b[0] + b[2]) / 2, 3)
        necks += [(top_net, [xt - TRACK_W / 2, t[3] - 0.2, xt + TRACK_W / 2, yt + VIA3 / 2]),
                  (bottom_net, [xb - TRACK_W / 2, yb - VIA3 / 2, xb + TRACK_W / 2, b[1] + 0.2])]
        vias += [(top_net, [xt, yt]), (bottom_net, [xb, yb])]
        m3 = [min(px0, cx0 - g3), min(py0, cy0 - g3), max(px1, cx1 + g3), max(py1, cy1 + g3)]
        keep += [{"layer": "metal3", "box": [round(v, 3) for v in m3], "net": None},
                 {"layer": "metal4", "box": [min(t[0], b[0]), min(t[1], b[1]), max(t[2], b[2]), max(t[3], b[3])],
                  "net": None}]
    keep += [{"layer": "metal4", "box": [round(v, 3) for v in bx], "net": nt} for nt, bx in necks]
    ring = [round(cc["bbox"][0] - RING_GAP, 3), round(yb - RING_GAP, 3), round(cc["bbox"][2] + RING_GAP, 3),
            round(yt + RING_GAP, 3)]
    return {"units": [], "row": cc["bbox"], "tracks": {"top": {top_net: yt}, "bottom": {bottom_net: yb}},
            "columns": {}, "ring": ring, "strips": [], "necks": necks, "vias": vias,
            "keepouts": keep, "track_span": [round(ring[0] - EXT, 3), round(ring[2] + EXT, 3)]}


def cap_build(name: str, cc: dict, geo: dict, out: Path) -> dict:
    """Draw the capacitor block in out/ and return {'gds', 'rc', 'log'}."""
    c = ["drc off", "snap internal", f"gds read {REPO / cc['gds']}", f"load {name} -silent", "tech unlock *",
         _b(0, 0, 0, 0), f"getcell {Path(cc['gds']).stem}"]
    for _, bx in geo["necks"]:
        c += [_b(*bx), "paint metal4"]
    for _, (x, y) in geo["vias"]:
        c += [_b(x - VIA3 / 2, y - VIA3 / 2, x + VIA3 / 2, y + VIA3 / 2), "paint via3"]
    x0, x1 = geo["track_span"]
    for side in ("top", "bottom"):
        for net, ty in geo["tracks"][side].items():
            c += [_b(x0, ty - TRACK_W / 2, x1, ty + TRACK_W / 2), "paint metal3",
                  _b(x0 + 0.1, ty - 0.05, x0 + 0.2, ty + 0.05), f"label {net} c metal3"]
    c += ["tech revert", f"save {name}", f"gds write {name}", "quit -noprompt"]
    for f in out.glob(f"{name}.*"):
        f.unlink()
    (out / "build.tcl").write_text("\n".join(c) + "\n")
    r = subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", pcell.MAGICRC, str(out / "build.tcl")],
                       cwd=out, env=TOOL_ENV, capture_output=True, text=True, timeout=600)
    (out / "build_magic.log").write_text(r.stdout + r.stderr)
    gds = out / f"{name}.gds"
    return {"gds": rel(gds) if gds.exists() else None, "rc": r.returncode, "log": rel(out / "build_magic.log")}


def ref_netlist(name: str, devices: list, ports: list) -> str:
    """The block's reference for LVS: its ports (track nets and the ring's '<body>_body') and its devices from the
    IR, each with the total finger count drawn; a device's body is the ring's port."""
    lines = [f".subckt {name} {' '.join(ports)}"]
    for d in devices:
        n = d["nets"]
        if "C" in n:   # a capacitor: top plate, bottom plate
            lines.append(f"X{d['name'].lstrip('X')} {n['C']} {n['B']} {d['model']} W={d['W']:g} L={d['L']:g}"
                         + (f" m={d['m']}" if d.get("m", 1) > 1 else ""))
            continue
        if "P" in n:   # a resistor: its two ends (plan v4 Phase 8)
            lines.append(f"X{d['name']} {n['P']} {n['N']} {d['model']} W={d['W']:g} L={d['L']:g}")
            continue
        lines.append(f"X{d['name']} {n['D']} {n['G']} {n['S']} {d['body_port']} {d['model']} "
                     f"L={d['L']:g} W={d['W']:g} nf={d['nf']}" + (f" m={d['m']}" if d.get("m", 1) > 1 else ""))
    return "\n".join(lines + [".ends"]) + "\n"


def lvs(gds: Path, name: str, ref_text: str, out: Path) -> dict:
    """LVS of the block's top cell (its labels are the ports), with a negative control: the same reference with
    the first device's L changed by 10 % (at least 0.1 um) must fail."""
    out.mkdir(parents=True, exist_ok=True)
    ref = out / "ref.spice"
    ref.write_text(ref_text)
    txt = subprocess.run(["bash", str(pcell.SCRIPTS / "magic_lvs.sh"), str(gds), name, str(ref), name, str(out / "lvs")],
                         env={**TOOL_ENV, "LVS_MODE": "top"}, capture_output=True, text=True, timeout=900).stdout
    m = re.search(r" L=([0-9.]+)", ref_text)
    bad_l = float(m.group(1)) + max(0.1, round(0.1 * float(m.group(1)), 3))
    bad = out / "ref_wrongL.spice"
    bad.write_text(ref_text.replace(f" L={m.group(1)}", f" L={bad_l:g}", 1))
    txt2 = subprocess.run(["bash", str(pcell.SCRIPTS / "magic_lvs.sh"), str(gds), name, str(bad), name,
                           str(out / "lvs_negctl")], env={**TOOL_ENV, "LVS_MODE": "top"},
                          capture_output=True, text=True, timeout=900).stdout
    ok, neg = "LVS_RESULT MATCH" in txt, "LVS_RESULT FAIL" in txt2
    return {"match": ok, "neg_control_rejected": neg, "pass": ok and neg,
            "report": rel(out / "lvs" / "lvs_report.txt"), "extracted": rel(out / "lvs" / "extracted.spice")}
