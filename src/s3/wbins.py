"""SKY130 model bins (W, L) read from the PDK's own model files, for the S3 option modes.

The sky130 MOSFET subcircuits pass the instance W (not W/nf) and no nf to the BSIM4 card, so a netlist
device W = 24 um, nf = 1 is simulated in the bin that contains W = 24 um. A layout built from nf fingers
is extracted as fingers of W/nf each, which the simulator places in the bin that contains W/nf. When the
two bins differ, the drawn device is a different model from the sized one (Vth, mobility, flicker noise
parameters change), not only a different parasitic. Mode A-bin keeps W/nf in the sized device's bin.

    bins(model) -> [(lmin, lmax, wmin, wmax) in um]
    bin_index(model, W, L) -> index of the bin that contains (W, L), or None
"""
from __future__ import annotations

import functools
import re
from pathlib import Path

from src.common.tools import PDK_ROOT

MODEL_DIR = Path(PDK_ROOT) / "sky130A/libs.tech/combined/continuous/models_fet"


@functools.lru_cache(maxsize=None)
def bins(model: str) -> tuple:
    f = MODEL_DIR / f"{model}.spice"
    if not f.exists():
        return ()
    txt = f.read_text()
    out = []
    for m in re.finditer(r"^\.model\s+\S+\s+[np]mos\s*\n(.*?)(?=^\.model|\Z)", txt, re.S | re.M):
        body = m.group(1)
        v = {}
        for k in ("lmin", "lmax", "wmin", "wmax"):
            mm = re.search(rf"\b{k}\s*=\s*([0-9.eE+-]+)", body)
            if mm:
                v[k] = float(mm.group(1)) * 1e6
        if len(v) == 4:
            out.append((v["lmin"], v["lmax"], v["wmin"], v["wmax"]))
    return tuple(out)


def bin_index(model: str, W: float, L: float) -> int | None:
    eps = 1e-9
    for i, (l0, l1, w0, w1) in enumerate(bins(model)):
        if l0 - eps <= L < l1 - eps and w0 - eps <= W < w1 - eps:   # SPICE: min <= value < max
            return i
    return None


def same_bin(model: str, W: float, L: float, Wf: float) -> bool:
    a, b = bin_index(model, W, L), bin_index(model, Wf, L)
    return a is not None and a == b


def table(models: list) -> dict:
    return {m: [{"lmin_um": a, "lmax_um": b, "wmin_um": c, "wmax_um": d} for a, b, c, d in bins(m)] for m in models}
