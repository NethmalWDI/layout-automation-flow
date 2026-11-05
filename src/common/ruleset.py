"""Layout rule set v2 (docs/rules_v2/ruleset_v2.md; PREREG amendment of 2026-11-05), opt-in per design.

`ruleset: v2` in inputs/<d>/layout.yaml switches S4 and S5 to it; without it (every finished design) nothing here is
called and both stages run v1 exactly as before. Phase 1 (this module):

* D (spacing): every spacing S4's block generator and S5's placement choose is the deck minimum x 1.10, rounded up
  to 0.05 um (src/common/drc_rules.py). The unit cells and S4's stub planner keep their own geometry (DRC-minimum
  already, signed off by every block's DRC).
    - Units in a row: `unit_gap` measures each unit cell's distance from its box edge to its diffusion, poly, local
      interconnect, metal1 and metal2, and keeps the facing pair's reserve spacing.
    - Blocks (S5): two blocks of one transistor type on one body net abut (their n-wells or p-implants merge, their
      taps stay > 0.30 um apart); a PMOS block above an NMOS block keeps p-tap to n-well (diff/tap.11); wells on
      different nets nwell.2a; anything next to a macro or a capacitor capm.11 (MIM to unrelated metal3).
* R1 (no routing over devices): S4 lists each block's device area (its rows of units) as a keep-out for metal3 and
  metal4; S5's grid router leaves it to every net.
* R2 (channels): every gap of S5 gets CHANNEL um more; S5 starts at one router grid and widens one grid at a time
  until every net routes (phase 1: one width for every gap).
All lengths in um.
"""
from __future__ import annotations

import math

from src.common import drc_rules as D

CHANNEL = {"um": 0.0}        # R2: added to every gap of S5's placement (set by S5's channel loop)
CHANNEL_STEPS = 10           # R2: at most 10 router grids (8 um) added before S5 gives up widening


def name(design: str) -> str:
    from src.s4.run import layout_options
    return str(layout_options(design).get("ruleset") or "v1")


def is_v2(design: str) -> bool:
    return name(design) == "v2"


# ------------------------------------------------------------------------------------------------- S4 (blocks)
def block_constants() -> dict:
    """The block generator's spacings under v2, each from the reserve of the rule that binds it."""
    from src.s4 import block as B
    r = D.reserve
    pitch = max(B.TRACK_W, B.VIA2) + r("met3.2")                     # via2 landings on neighbouring tracks
    return {
        # the first track: a gate pad's via1 surround reaches 0.14 um past the cell; its met2 to the track's via2
        # landing (met2) keeps met2.2's reserve
        "FIRST": D.snap_up(0.14 + r("met2.2") + B.VIA2 / 2),
        "PITCH": round(pitch, 3), "ROW_SEP": round(pitch, 3),
        # ring and tap strip centre lines: half the tap (0.085) plus diffusion spacing to the units
        "RING_GAP": D.snap_up(0.085 + r("diff/tap.3")), "TAP_GAP": D.snap_up(0.085 + r("diff/tap.3")),
        "COL0": D.snap_up(B.VIA2 / 2 + r("met2.2")), "COL_PITCH": round(B.VIA2 + r("met2.2"), 3),
        "NWELL_OVER": D.snap_up(0.085 + r("diff/tap.10")),           # n-well round the n-tap ring
        "EXT": 0.0,             # tracks end at the ring: the grid router reaches them from above (R1 keeps it off
                                # the units, not off the tracks)
        "CAPM_SPACE": r("capm.11"), "MET_SPACE": r("met3.2"),
        # a tap strip's contacts end clear of the ring's: half the ring's contact (0.085) plus licon.2's reserve (v1's
        # 0.215 left 0.13 um, below 0.17; caught by a v2 array's block DRC, 2026-11-05)
        "STRIP_CONT_IN": D.snap_up(0.085 + r("licon.2")),
        # the ring edge with the body pin: S5 drops a contact stack (li to metal3, its metal3 square 0.5 um) on it,
        # which needs half its square, met3.2's reserve and half a track to the nearest track (flow record row 105:
        # at 0.40 the stacks met the outermost tracks, top-level DRC 11-16 errors)
        "RING_GAP_BODY": D.snap_up(0.25 + r("met3.2") + B.TRACK_W / 2),
    }


_MARGINS = {}
_LAYERS = {"diff": (65, 20), "tap": (65, 44), "poly": (66, 20), "li": (67, 20), "met1": (68, 20), "met2": (69, 20)}
_SPACE = {"diff": "diff/tap.3", "tap": "diff/tap.3", "poly": "poly.2", "li": "li.3", "met1": "met1.2", "met2": "met2.2"}


def margins(gds: str) -> dict:
    """{layer: (left, right)}: the distance from the cell's bounding box to its outermost shape of each layer."""
    if gds not in _MARGINS:
        import klayout.db as kdb
        from src.common.tools import REPO
        ly = kdb.Layout()
        ly.read(str(REPO / gds))
        c = ly.top_cell()
        bb = c.dbbox()
        m = {}
        for n, (a, d) in _LAYERS.items():
            li = ly.find_layer(a, d)
            if li is None:
                continue
            b = c.dbbox_per_layer(li)
            if not b.empty():
                m[n] = (round(b.left - bb.left, 4), round(bb.right - b.right, 4))
        _MARGINS[gds] = m
    return _MARGINS[gds]


def unit_gap(left: dict, right: dict) -> float:
    """The v2 gap between two neighbouring units' bounding boxes (left unit, right unit; a 'mirror' unit is flipped
    about its vertical axis, so its sides swap): the largest facing-layer reserve spacing, less the two margins,
    diffusion against diffusion or tap, and poly against diffusion (poly.4), rounded up to the 0.005 um grid."""
    ml, mr = margins(left["rec"]["gds"]), margins(right["rec"]["gds"])
    a = {n: (v[0] if left["mirror"] else v[1]) for n, v in ml.items()}        # left unit's right side
    b = {n: (v[1] if right["mirror"] else v[0]) for n, v in mr.items()}       # right unit's left side
    need = [0.0]
    for n in a:
        for k in b:
            if n == k or {n, k} == {"diff", "tap"}:
                need.append(D.reserve(_SPACE[n]) - a[n] - b[k])
            elif {n, k} == {"poly", "diff"}:
                need.append(D.reserve("poly.4") - a[n] - b[k])
    return round(math.ceil(round(max(need) / 0.005, 6)) * 0.005, 3)


def apply_s4(design: str) -> bool:
    """Switch S4's block generator to v2 for this process (S4 builds one design per run). True when v2."""
    if not is_v2(design):
        return False
    from src.s4 import block as B
    for k, v in block_constants().items():
        setattr(B, k, v)
    B.UNIT_GAP = unit_gap
    return True


def device_keepouts(geo: dict) -> list:
    """R1: the block's device area (its rows of units, the gaps between them included) for metal3 and metal4."""
    x0, y0, x1, y1 = geo["row"]
    return [{"layer": layer, "box": [x0, y0, x1, y1], "net": None, "kind": "device_area"} for layer in ("metal3", "metal4")]


# ------------------------------------------------------------------------------------------------ S5 (placement)
def _base_gap(ta: dict, tb: dict) -> float:
    kinds = {ta["type"], tb["type"]}
    if kinds & {"macro", "cap", "res"}:
        return D.reserve("capm.11")
    if ta["type"] == tb["type"]:
        if ta["body"] == tb["body"]:
            return 0.0                       # one body: n-wells or p-implants merge
        return D.reserve("nwell.2a") if ta["type"] == "pmos" else D.reserve("diff/tap.3")
    return D.reserve("diff/tap.11")          # n-well (PMOS) facing a p-tap ring (NMOS)


def gap_x(blocks: dict, a: str, b: str) -> float:
    return round(_base_gap(blocks[a], blocks[b]) + CHANNEL["um"], 4)


def gap_y(blocks: dict, upper: list, lower: list) -> float:
    return round(max(_base_gap(blocks[a], blocks[b]) for a in upper for b in lower) + CHANNEL["um"], 4)


def apply_s5(design: str) -> bool:
    if not is_v2(design):
        return False
    from src.s5 import place as P
    P.GAP_FN, P.ROWGAP_FN = gap_x, gap_y
    return True
