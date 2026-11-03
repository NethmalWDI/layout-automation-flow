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
Magic draws the block, so its contact rules apply; Magic DRC (full) and Netgen LVS against the IR's devices sign it off.
All lengths are in um.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from src.common import pcell
from src.common.tools import REPO, TOOL_ENV, rel

MAG_UNIT = 0.005     # um per Magic internal unit (sky130A, magscale 1 2)
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


def unit_pins(rec: dict) -> dict:
    """{name: {'layer', 'rect'}} of a unit cell, from its .mag labels; a single-finger strip label (met1, mid-height)
    is widened to the whole strip from S3's geometry record."""
    cell = rec["cell"]
    mag = (REPO / rec["gds"]).with_suffix(".mag").read_text()
    pins = {}
    for m in re.finditer(r"^rlabel\s+(\S+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+\d+\s+(\S+)", mag, re.M):
        layer, *xy, name = m.groups()
        pins[name] = {"layer": layer, "rect": [int(v) * MAG_UNIT for v in xy]}
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
    for t in ("G", "D", "S"):
        p = pins[t]
        if p["layer"] == "metal1":   # the gate pad on its own side; a single-finger cell's strips go down
            x0, y0, x1, y1 = p["rect"]
            side = ("top" if (y0 + y1) / 2 > h / 2 else "bottom") if t == "G" else "bottom"
            plan[t] = {"x": round((x0 + x1) / 2, 3), "side": side, "kind": "met1"}
    for t in ("G", "D", "S"):
        if t in plan:
            continue
        x0, y0, x1, y1 = pins[t]["rect"]
        side = "top" if (y0 + y1) / 2 > h / 2 else "bottom"
        taken = [v["x"] for v in plan.values() if v["side"] == side]
        lo, hi = max(x0, 0) + SLOT_MIN, min(x1, w) - SLOT_MIN
        cands = [round(lo + k * 0.005, 3) for k in range(int((hi - lo) / 0.005) + 1)] or [round((x0 + x1) / 2, 3)]
        x = max(cands, key=lambda c: (min([abs(c - t_) for t_ in taken] or [1e9]), -abs(c - (lo + hi) / 2)))
        plan[t] = {"x": x, "side": side, "kind": "met2"}
    for side in ("top", "bottom"):
        xs = sorted(v["x"] for v in plan.values() if v["side"] == side)
        if any(b - a < 2 * SLOT_MIN for a, b in zip(xs, xs[1:])):
            raise RuntimeError(f"stubs too close on the {side} side: {xs}")
    return plan


def layout(units: list) -> dict:
    """units: [{'device', 'rec', 'mirror', 'nets': {'D','G','S'}}] left to right. Returns the geometry: unit origins,
    the stubs (x, pin edge, side, net), the tracks per side, the ring box and the block's extent."""
    x, placed = 0.0, []
    for u in units:
        w, h = u["rec"]["geometry"]["bbox_um"]
        pins = unit_pins(u["rec"])
        sp = stub_plan(pins, w, h)
        def gx(lx): return round(x + (w - lx if u["mirror"] else lx), 3)   # noqa: E731
        stubs = []
        for t, s in sp.items():
            x0, y0, x1, y1 = pins[t]["rect"]
            stubs.append({"device": u["device"], "term": t, "net": u["nets"][t], "x": gx(s["x"]), "side": s["side"],
                          "kind": s["kind"], "edge": y1 if s["side"] == "top" else y0, "pin_rect_y": [y0, y1]})
        placed.append({**u, "x": round(x, 3), "w": w, "h": h, "stubs": stubs})
        x += w + GAP
    row_w, row_h = round(x - GAP, 3), max(p["h"] for p in placed)
    tracks = {}
    for side in ("top", "bottom"):
        nets = []
        for p in placed:
            for s in sorted(p["stubs"], key=lambda s: s["x"]):
                if s["side"] == side and s["net"] not in nets:
                    nets.append(s["net"])
        tracks[side] = {n: round(row_h + FIRST + k * PITCH, 3) if side == "top" else round(-FIRST - k * PITCH, 3)
                        for k, n in enumerate(nets)}
    # a net with pins on both sides: a met2 column right of the row joins its top and bottom tracks
    both = [n for n in tracks["top"] if n in tracks["bottom"]]
    columns = {n: round(row_w + COL0 + k * COL_PITCH, 3) for k, n in enumerate(both)}
    top = max(tracks["top"].values(), default=row_h) + RING_GAP
    bot = min(tracks["bottom"].values(), default=0.0) - RING_GAP
    right = max([row_w] + list(columns.values())) + RING_GAP
    ring = [round(-RING_GAP, 3), round(bot, 3), round(right, 3), round(top, 3)]
    return {"units": placed, "row": [0.0, 0.0, row_w, row_h], "tracks": tracks, "columns": columns, "ring": ring,
            "track_span": [round(ring[0] - EXT, 3), round(ring[2] + EXT, 3)]}


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
    x0, x1 = geo["track_span"]
    for side in ("top", "bottom"):
        for net, ty in geo["tracks"][side].items():
            c += [_b(x0, ty - TRACK_W / 2, x1, ty + TRACK_W / 2), "paint metal3",
                  _b(x0 + 0.1, ty - 0.05, x0 + 0.2, ty + 0.05), f"label {net} c metal3"]
    rx0, ry0, rx1, ry1 = geo["ring"]
    if dtype == "pmos":
        c += [_b(rx0 - NWELL_OVER, ry0 - NWELL_OVER, rx1 + NWELL_OVER, ry1 + NWELL_OVER), "paint nwell"]
    c += [_b(rx0, ry0, rx1, ry1), "sky130::guard_ring_draw " + ("nsc nsd" if dtype == "pmos" else "psc psd")]
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


def ref_netlist(name: str, devices: list, ports: list) -> str:
    """The block's reference for LVS: its ports (track nets and the ring's '<body>_body') and its devices from the
    IR, each with the total finger count drawn; a device's body is the ring's port."""
    lines = [f".subckt {name} {' '.join(ports)}"]
    for d in devices:
        n = d["nets"]
        lines.append(f"X{d['name']} {n['D']} {n['G']} {n['S']} {d['body_port']} {d['model']} "
                     f"L={d['L']:g} W={d['W']:g} nf={d['nf']}")
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
