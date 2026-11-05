"""The README's picture of iadc_ota_v2's flat-packed area-only layout of 2026-11-06 that failed DRC (8 x nwell.2a,
flow record row 107), with every error ringed. Reads outputs/report/iadc_ota_v2/flat_drc_failed/ (the layout and the
error boxes saved before the re-run); writes outputs/report/readme/iadc_ota_v2_flat_drc_failed.png.
Run inside layout-s0s3 after `source scripts/env.sh`.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import make_ttsky_report as T  # noqa: E402
import report_figures as F  # noqa: E402

K = REPO / "outputs/report/iadc_ota_v2/flat_drc_failed"
OUT = REPO / "outputs/report/readme"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    boxes = []
    for ln in (K / "drc_errors_um.txt").read_text().splitlines():
        x0, y0, x1, y1 = (float(v) for v in ln.split()[:4])
        boxes.append([x0, y0, x1, y1])
    raw = OUT / "iadc_ota_v2_flat_raw.png"
    r = T.render(K / "iadc_ota_v2_routed.gds", raw, w=100, h=190, ppu=4)
    m = 2.0                                           # ring each error 2 um wide so it shows at this scale
    rects = [([b[0] - m, b[1] - m, b[2] + m, b[3] + m], "#e5484d", "") for b in boxes]
    F.annotate(raw, r["window_um"], rects, [], OUT / "iadc_ota_v2_flat_drc_failed.png",
               title="iadc_ota_v2 area-only, flat (2026-11-06)\n79.6 × 175.8 µm; DRC: 8 × nwell.2a (ringed)",
               legend=[("nwell.2a: two PMOS n-wells 0.8 µm apart (need 1.27, or touching)", "#e5484d")])
    print(OUT / "iadc_ota_v2_flat_drc_failed.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
