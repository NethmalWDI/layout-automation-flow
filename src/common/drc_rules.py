"""SKY130A minimum spacings, widths and enclosures that layout rule set v2 builds on (docs/rules_v2/ruleset_v2.md).

Each value is the SkyWater sky130A Magic DRC deck's (`$PDK_ROOT/sky130A/libs.tech/magic/sky130A.tech`, in the image
hpretl/iic-osic-tools:2026.10), keyed by the deck's own rule id; `deck_values()` reads them back from the deck so a test
can confirm the table. `reserve()` is Imasha's spacing rule of 2026-11-05 (Q9, reading (a)): the minimum times 1.10,
rounded up to 0.05 um. All lengths in um.
"""
from __future__ import annotations

import math
import os
import re
from pathlib import Path

MIN = {                      # rule id: value (um), as the deck's message names it
    "diff/tap.3": 0.27,      # diffusion spacing
    "diff/tap.8": 0.18,      # n-well enclosure of p-diffusion
    "diff/tap.9": 0.34,      # n-diffusion to n-well
    "diff/tap.10": 0.18,     # n-well enclosure of n-tap
    "diff/tap.11": 0.13,     # p-tap to n-well
    "nwell.1": 0.84,         # n-well width
    "nwell.2a": 1.27,        # n-well spacing (touching wells merge)
    "poly.2": 0.21,          # poly spacing
    "poly.4": 0.075,         # poly (not a gate) to diffusion
    "li.3": 0.17,            # local interconnect spacing
    "licon.2": 0.17,         # diffusion contact spacing
    "met1.2": 0.14, "met2.2": 0.14, "met3.2": 0.30, "met4.2": 0.30,   # metal spacing
    "met3.1": 0.30,          # metal3 width
    "met4.5b": 0.40,         # metal4 wider than 3 um (3.005) to unrelated metal4
    "capm.2a": 0.84,         # MIM spacing
    "capm.11": 1.34,         # MIM to unrelated metal3
}
LATCHUP_UM = 15.0            # LU.2 / LU.3: diffusion within 15.0 um of a tap of the other type (a maximum)
RESERVE, SNAP = 1.10, 0.05


def snap_up(v: float, step: float = SNAP) -> float:
    """v rounded up to a multiple of step (a value already on it stays)."""
    return round(math.ceil(round(v / step, 6)) * step, 4)


def reserve(rule: str) -> float:
    """The v2 spacing for a rule: the minimum x 1.10, rounded up to 0.05 um."""
    return snap_up(MIN[rule] * RESERVE)


def deck_path() -> Path:
    return Path(os.environ.get("PDK_ROOT", "/foss/pdks")) / "sky130A" / "libs.tech" / "magic" / "sky130A.tech"


def deck_values(path: Path | None = None) -> dict:
    """{rule id: value in um} from the deck: for each rule id the first statement (continuation lines joined) whose
    message ends in '(<id>)', its last number before the message (the deck states lengths in nm)."""
    text = (path or deck_path()).read_text()
    stmts = re.sub(r"\\\n", " ", text).splitlines()
    out = {}
    for rid in MIN:
        for s in stmts:
            q = s.find('"')
            if q > 0 and re.search(r"\(" + re.escape(rid) + r"\)\s*\"", s):
                nums = re.findall(r"(?<![\w.*])(\d+)(?![\w.])", s[:q])
                if nums:
                    out[rid] = int(nums[-1]) / 1000
                    break
    return out
