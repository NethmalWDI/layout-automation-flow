"""The README's result pictures (outputs/report/readme/): each design's layouts side by side at one scale, with the
hand-drawn layout where there is one, and the hard outline where the design has one. Run inside layout-s0s3 after
`source scripts/env.sh`:  python3 scripts/make_readme_figures.py
Nothing of a design is changed; the pictures are drawn from the committed GDS files by KLayout (fixed scale) and laid
side by side by matplotlib.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import make_ttsky_report as T  # noqa: E402

OUT = REPO / "outputs" / "report" / "readme"
PPU = 3


def j(*p):
    f = REPO.joinpath(*p)
    return json.loads(f.read_text()) if f.exists() else None


def flow_panel(d: str, rule: str, label: str) -> dict:
    gds = REPO / "outputs" / "S5" / d / f"routed_{rule}" / f"{d}_routed.gds"
    pl = j("outputs/S5", d, "placement.json")["chosen"][rule]["placement"]["bbox"]
    w, h = pl[2] - pl[0], pl[3] - pl[1]
    return {"gds": gds, "label": label, "size": (w, h)}


def hand_panel(d: str, cell: str | None = None, label: str = "hand-drawn") -> dict:
    """cell: the hand layout's op-amp inside a larger file (ttsky's tile holds Diff_Opamp); its box is measured and
    outlined, as the detailed reports measure it."""
    ref = j("outputs/reference_layout", d, "reference_layout.json")
    return {"gds": REPO / ref["gds"], "label": label, "hand": True, "cell": cell}


def figure(name: str, panels: list, w_um: float, h_um: float, outline: list | None, note: str) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    OUT.mkdir(parents=True, exist_ok=True)
    hand_area = None
    for k, p in enumerate(panels):
        png = OUT / f"{name}_{k}.png"
        r = T.render(p["gds"], png, w=w_um, h=h_um, ppu=PPU, **({"cell": p["cell"]} if p.get("cell") else {}))
        p["png"], p["win"] = png, r["window_um"]
        if p.get("hand"):
            box = (r.get("cells") or {}).get(p.get("cell"), [None])[0] if p.get("cell") else None
            p["box"] = box
            p["size"] = (box[2] - box[0], box[3] - box[1]) if box else (r["w_um"], r["h_um"])
            hand_area = p["size"][0] * p["size"][1]
    fig, axes = plt.subplots(1, len(panels), figsize=(3.6 * len(panels), 3.6 * h_um / w_um + 0.9), dpi=150)
    for ax, p in zip(axes, panels):
        x0, y0, x1, y1 = p["win"]
        ax.imshow(mpimg.imread(str(p["png"])), extent=[x0, x1, y0, y1], interpolation="lanczos")
        if outline:
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            ax.add_patch(Rectangle((cx - outline[0] / 2, cy - outline[1] / 2), outline[0], outline[1], fill=False,
                                   edgecolor="#898781", linestyle="--", linewidth=1.0))
        if p.get("box"):
            b = p["box"]
            ax.add_patch(Rectangle((b[0], b[1]), b[2] - b[0], b[3] - b[1], fill=False, edgecolor="#1baf7a", linewidth=1.6))
        w, h = p["size"]
        sub = f"{w:.0f} × {h:.0f} µm = {w * h:,.0f} µm²"
        if hand_area and not p.get("hand"):
            sub += f"\n{w * h / hand_area:.2f} × the hand layout"
        ax.set_title(f"{p['label']}\n{sub}", fontsize=8.5, color="#0b0b0b", loc="left")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#d0cfcb")
    fig.text(0.01, 0.01, note, fontsize=7, color="#52514e")
    fig.tight_layout(rect=(0, 0.05, 1, 0.97))
    out = OUT / f"{name}.png"
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return out


def main() -> int:
    figure("iadc_ota_compare", [flow_panel("iadc_ota", "budget_aware", "v1 rules (budget-aware)"),
                                flow_panel("iadc_ota_v2", "budget_aware", "v2 rules (budget-aware)"),
                                flow_panel("iadc_ota_v2", "area_only", "v2 rules (area-only)"),
                                hand_panel("iadc_ota")],
           170, 230, [161.0, 225.77],
           "One scale for all four; dashed: the Tiny Tapeout tile (161 × 225.77 µm). The hand layout also holds the "
           "switched-capacitor CMFB (3,265 µm²), which the flow does not lay out.")
    tt = [flow_panel("ttsky25a_fd", "budget_aware", "v1 rules (budget-aware)"),
          flow_panel("ttsky25a_fd", "area_only", "v1 rules (area-only)")]
    for r, lab in (("budget_aware", "v2 rules (budget-aware)"), ("area_only", "v2 rules (area-only)")):
        # ttsky25a_fd_v2 (started 2026-11-05, scripts/finish_ttsky_v2.sh): shown once its routed layout exists
        if (REPO / "outputs/S5/ttsky25a_fd_v2" / f"routed_{r}" / "ttsky25a_fd_v2_routed.gds").exists():
            tt.append(flow_panel("ttsky25a_fd_v2", r, lab))
    tt.append(hand_panel("ttsky25a_fd", "Diff_Opamp", "hand-drawn (op-amp outlined in the tile)"))
    figure("ttsky25a_fd_compare", tt, 260, 210, [250.0, 200.0],
           f"One scale for all {len(tt)}; dashed: the 250 × 200 µm outline. The taped-out tile also holds enable switches.")
    print(sorted(str(p.relative_to(REPO)) for p in OUT.glob("*_compare.png")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
