"""S3 step 1b — turn a PCell into a complete device cell: finger straps and terminal labels.

The SKY130 Magic PCell draws nf fingers with alternating drain/source met1 strips (drain strip on the
left) but leaves them unconnected (only the gates can be joined, with conn_gates = 1). This module adds,
in the wrapper cell, around the unchanged PCell instance:
  * one via1 (Magic contact type m2c) on every strip of a terminal, near the top end for the terminal
    connected at the top and near the bottom end for the other one,
  * one met2 bar per terminal across all strips (top bar / bottom bar),
  * labels D, G, S, B in the wrapper (so LVS compares the wrapper's ports D G S B),
  * on short-L devices, a met1 patch that widens each gate contact pad to the met1 minimum area: the PCell's
    pad is 0.29 x 0.23 um = 0.067 um2 at L = 0.2-0.24 um, below met1.6 (iadc_ota 1.2/0.2 LVT, LOADBench
    484/0.24 nf = 1; 2026-10-27). The pad is widened along the gate (x), away from the S/D strips.
Which strips are 'source' is a choice for even nf ('outer' = S puts the outer strips, which are not
shared between fingers, on the source; the drain then has the smaller diffusion area). The MOSFET is
symmetric, so this is a legal relabelling. Geometry is read from the generated GDS (KLayout); the
drawing is done by Magic so that its contact rules apply; DRC then checks the result.
"""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

from src.common import pcell
from src.common.tools import TOOL_ENV

class StrapDoesNotFit(RuntimeError):
    """The finger strips are too short to place a source bar and a drain bar apart (would short S and D)."""


VIA_W = 0.26   # m2c (via1 + surround) width: 0.15 cut + 2 x 0.055 enclosure (via.4a, met2.4)
VIA_H = 0.32   # m2c height: 0.15 cut + 2 x 0.085 enclosure in one direction (via.5a, met2.5)
BAR = 0.32     # met2 bar height, covers the m2c (>= met2 min width 0.14)
MET1_MIN_AREA = 0.083   # um2, met1.6 (the Magic sky130A DRC deck: "Metal1 minimum area < 0.083um^2")
GRID = 0.005            # um, manufacturing grid


def pad_patch(pad: list) -> list | None:
    """The gate pad widened symmetrically in x to reach the met1 minimum area, or None if it already does."""
    x0, y0, x1, y1 = pad
    w, h = x1 - x0, y1 - y0
    if w * h >= MET1_MIN_AREA:
        return None
    grow = math.ceil((MET1_MIN_AREA / h - w) / (2 * GRID) - 1e-9) * GRID   # per side, on the grid
    return [round(x0 - grow, 3), y0, round(x1 + grow, 3), y1]


def plan(gds: Path, outer: str) -> dict:
    """Read strips, gate pads and the bulk label position; decide which strips are S and D."""
    import klayout.db as kdb
    ly = kdb.Layout()
    ly.read(str(gds))
    top = ly.top_cell()
    dbu = ly.dbu
    m1 = kdb.Region(top.begin_shapes_rec(ly.find_layer(68, 20)))
    diff = kdb.Region(top.begin_shapes_rec(ly.find_layer(65, 20)))
    strips = sorted([p.bbox() for p in m1.interacting(diff).each()], key=lambda b: b.left)
    pads = [p.bbox() for p in m1.not_interacting(diff).each()]
    labels = {}
    for li in ly.layer_indexes():
        it = top.begin_shapes_rec(li)
        while not it.at_end():
            sh = it.shape()
            if sh.is_text():
                t = it.trans() * sh.text.trans
                labels.setdefault(sh.text.string, (t.disp.x * dbu, t.disp.y * dbu))
            it.next()
    n = len(strips)
    # PCell order is D S D S ... from the left (evens = 1). 'outer' = S swaps the roles when n is odd
    # (even nf -> n = nf + 1 strips, both outer strips have the same role).
    roles = ["D" if i % 2 == 0 else "S" for i in range(n)]
    if outer == "S" and n % 2 == 1:
        roles = ["S" if r == "D" else "D" for r in roles]
    st = [{"x0": b.left * dbu, "x1": b.right * dbu, "y0": b.bottom * dbu, "y1": b.top * dbu, "role": r}
          for b, r in zip(strips, roles)]
    top_pads = sorted([b for b in pads if b.bottom * dbu > max(s["y1"] for s in st)], key=lambda b: b.left)
    bot_pads = sorted([b for b in pads if b.top * dbu < min(s["y0"] for s in st)], key=lambda b: b.left)
    gpad = (top_pads or bot_pads)[0] if (top_pads or bot_pads) else None
    return {"strips": st, "gate_pad": None if gpad is None else
            [gpad.left * dbu, gpad.bottom * dbu, gpad.right * dbu, gpad.top * dbu],
            "gate_pads": [[b.left * dbu, b.bottom * dbu, b.right * dbu, b.top * dbu] for b in top_pads + bot_pads],
            "labels": labels, "n_strips": n}


def tcl(cell: str, pl: dict) -> str:
    st = pl["strips"]
    # start from the generated GDS (the PCell subcell exists only there, not as a .mag file)
    cmds = ["drc off", f"gds read {cell}.gds", f"load {cell}", "select top cell"]
    if len(st) > 2:   # multi-finger: straps needed
        x_lo, x_hi = min(s["x0"] for s in st), max(s["x1"] for s in st)
        y_top = min(s["y1"] for s in st) - 0.05 - VIA_H  # inside every strip, near its top end
        y_bot = max(s["y0"] for s in st) + 0.05            # inside every strip, near its bottom end
        if y_top - (y_bot + BAR) < 0.14:                   # met2.2 spacing between the two bars
            raise StrapDoesNotFit(f"strips too short for two met2 bars: {y_bot:.3f}..{y_top + VIA_H:.3f} um")
        for role, y in (("S", y_top), ("D", y_bot)):
            for s in st:
                if s["role"] != role:
                    continue
                xc = (s["x0"] + s["x1"]) / 2
                cmds += [f"box {xc - VIA_W / 2:.3f}um {y:.3f}um {xc + VIA_W / 2:.3f}um {y + VIA_H:.3f}um", "paint m2c"]
            cmds += [f"box {x_lo - 0.02:.3f}um {y:.3f}um {x_hi + 0.02:.3f}um {y + BAR:.3f}um", "paint metal2",
                     f"label {role} c metal2"]
    else:             # single finger: label the strips themselves
        for s in st:  # a small patch of the same layer under the label ties it to the child's strip
            yc = (s["y0"] + s["y1"]) / 2
            cmds += [f"box {s['x0']:.3f}um {yc:.3f}um {s['x1']:.3f}um {yc + 0.2:.3f}um", "paint metal1",
                     f"label {s['role']} c metal1"]
    for pad in pl["gate_pads"]:   # met1.6 patches (short L); the label goes on the first pad, as before
        p = pad_patch(pad)
        if p:
            cmds += [f"box {p[0]:.3f}um {p[1]:.3f}um {p[2]:.3f}um {p[3]:.3f}um", "paint metal1"]
    if pl["gate_pad"]:
        x0, y0, x1, y1 = pad_patch(pl["gate_pad"]) or pl["gate_pad"]
        cmds += [f"box {x0:.3f}um {y0:.3f}um {x1:.3f}um {y1:.3f}um", "paint metal1", "label G c metal1"]
    if "B" in pl["labels"]:
        bx, by = pl["labels"]["B"]
        cmds += [f"box {bx - 0.085:.3f}um {by - 0.085:.3f}um {bx + 0.085:.3f}um {by + 0.085:.3f}um", "paint locali",
                 "label B c locali"]
    cmds += [f"save {cell}", f"gds write {cell}", "quit -noprompt"]
    return "\n".join(cmds) + "\n"


def apply(cell_dir: Path, cell: str, outer: str) -> dict:
    gds = cell_dir / f"{cell}.gds"
    pl = plan(gds, outer)
    (cell_dir / "strap.tcl").write_text(tcl(cell, pl))
    r = subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", str(pcell.MAGICRC), str(cell_dir / "strap.tcl")],
                       cwd=cell_dir, env=TOOL_ENV, capture_output=True, text=True, timeout=300)
    (cell_dir / "strap_magic.log").write_text(r.stdout + r.stderr)
    return {"rc": r.returncode, "plan": pl, "strapped": pl["n_strips"] > 2,
            "roles": [s["role"] for s in pl["strips"]],
            "gate_pad_patch": [{"pad": p, "patched": pad_patch(p)} for p in pl["gate_pads"] if pad_patch(p)]}
