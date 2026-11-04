"""Figures for scripts/make_ttsky_report.py (run inside layout-s0s3 after `source scripts/env.sh`):

* schematics(): the designer's xschem schematics, drawn from a scratch copy (the sources are frozen and refer to their
  symbols by the designer's absolute paths), with every device the flow lays out boxed in its sub-circuit's colour and
  labelled with its S4 block number (B1 ...); on the top schematic the sub-circuit symbols x1 and x2 are outlined.
  Two xschem passes: the first writes each instance's bounding box, the second prints the annotated copy as SVG;
  cairosvg turns it into a PNG.
* annotate(): a layout picture (rendered by scripts/report_layout_png.py at a known window and scale) with coloured
  rectangles and labels drawn over it in layout coordinates (um).
The boxes and labels are drawing only: no schematic or layout file of the design is changed.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

SRC_REL = "circuits/ttsky25a_fd/upstream_src/Opamp_Design/src"
DESIGNER_PATH = "/foss/designs/FYP/Sky130_Design/Opamp_Design/src/"
# xschem layers the designer's schematics leave unused (they use 0, 1, 4, 5, 6, 15): one per sub-circuit, one for labels
LAYER = {"top": 7, "x1": 8, "x2": 9, "res_packs": 10}
LABEL_LAYER = 11


def _work(repo: Path) -> Path:
    w = repo / "runs" / "tmp" / "report_sch"
    if w.exists():
        shutil.rmtree(w)
    w.mkdir(parents=True)
    for f in (repo / SRC_REL).iterdir():
        if f.suffix in (".sch", ".sym"):
            (w / f.name).write_text(f.read_text().replace(DESIGNER_PATH, str(w) + "/"))
    return w


def _xschem(repo: Path, work: Path, tcl: str) -> None:
    script = work / "run.tcl"
    script.write_text(tcl)
    rc = os.path.join(os.environ.get("PDK_ROOT", "/foss/pdks"), "sky130A/libs.tech/xschem/xschemrc")
    subprocess.run(["xschem", "-x", "--rcfile", rc, "--script", str(script)], cwd=work, capture_output=True, text=True,
                   timeout=300)


def instance_names(sch: Path) -> list:
    return re.findall(r"^C \{[^}]*\}[^{\n]*\{name=([^\s}]+)", sch.read_text(), re.M)


def bboxes(repo: Path, work: Path, base: str) -> dict:
    names = instance_names(work / f"{base}.sch")
    out = work / f"{base}.bb"
    tcl = ["set dark_colorscheme 0", "xschem build_colors", f"xschem load {work / (base + '.sch')}",
           f"set f [open {out} w]"]
    tcl += [f'puts $f "{n}|[string map {{"\\n" " "}} [xschem instance_bbox {n}]]"' for n in names]
    tcl += ["close $f", "exit"]
    _xschem(repo, work, "\n".join(tcl) + "\n")
    res = {}
    for ln in out.read_text().splitlines() if out.exists() else []:
        n, rest = ln.split("|", 1)
        m = re.search(r"Instance:\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)", rest)
        if m:
            res[n] = [float(x) for x in m.groups()]
    return res


def schematic(repo: Path, work: Path, base: str, boxes: list, out_png: Path, colors: dict, width: int = 2400) -> Path:
    """boxes: [(name, macro, label, pad, text_scale)] for instances of `base`. Writes <out_png> (and the .svg)."""
    bb = bboxes(repo, work, base)
    extra = []
    for name, macro, label, pad, ts in boxes:
        if name not in bb:
            continue
        x0, y0, x1, y1 = bb[name]
        extra.append(f"B {LAYER[macro]} {x0 - pad} {y0 - pad} {x1 + pad} {y1 + pad} {{}}")
        if label:
            extra.append(f"T {{{label}}} {x0 - pad} {y0 - pad - 30 * ts} 0 0 {ts} {ts} {{layer={LABEL_LAYER}}}")
    annot = work / f"{base}_annot.sch"
    annot.write_text((work / f"{base}.sch").read_text().rstrip("\n") + "\n" + "\n".join(extra) + "\n")
    svg = out_png.with_suffix(".svg")
    _xschem(repo, work, "\n".join(["set dark_colorscheme 0", "xschem build_colors", f"xschem load {annot}",
                                   "xschem zoom_full", f"xschem print svg {svg}", "exit"]) + "\n")
    txt = svg.read_text()
    # the sub-circuit layers: a light fill and a clear outline in the report's colours; the labels in dark ink
    for macro, layer in LAYER.items():
        c = colors[macro]
        txt = re.sub(rf"\.l{layer}\{{[^}}]*\}}", f".l{layer}{{fill: {c}; fill-opacity: 0.13; stroke: {c}; "
                     "stroke-width: 2.2; stroke-linecap:round; stroke-linejoin:round;}", txt)
    # xschem writes a text's colour inline: only the labels added here turn dark and bold
    for lab in {b[2] for b in boxes if b[2]}:
        txt = re.sub(r'<text fill="#[0-9a-fA-F]{6}"([^>]*)>(' + re.escape(lab) + r")</text>",
                     r'<text fill="#0b0b0b" font-weight="bold"\1>\2</text>', txt)
    svg.write_text(txt)
    import cairosvg
    cairosvg.svg2png(bytestring=txt.encode(), write_to=str(out_png), output_width=width, background_color="white")
    return out_png


def annotate(png: Path, window: list, rects: list, labels: list, out: Path, title: str = "",
             legend: list | None = None) -> Path:
    """window: [x0, y0, x1, y1] um the picture spans. rects: [(box, colour, label)], labels: [(x, y, text)]."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.image as mpimg
    import matplotlib.patheffects as pe
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch, Rectangle
    img = mpimg.imread(str(png))
    x0, y0, x1, y1 = window
    k = 9.0 / max(x1 - x0, y1 - y0)                  # the longer side 9 inches, whatever the layout's shape
    fig, ax = plt.subplots(figsize=(max(4.5, (x1 - x0) * k + 1.2), (y1 - y0) * k + 1.2), dpi=150)
    ax.imshow(img, extent=[x0, x1, y0, y1], interpolation="lanczos")
    halo = [pe.withStroke(linewidth=2.6, foreground="white")]
    for rect in rects:
        box, col, lab = rect[:3]
        corner = rect[3] if len(rect) > 3 else "tl"     # where the label sits: tl, tr, bl or br
        ax.add_patch(Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1], fill=True, facecolor=col,
                               alpha=0.10, edgecolor="none"))
        ax.add_patch(Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1], fill=False, edgecolor=col,
                               linewidth=2.2))
        if lab:
            x = box[0] + 1 if corner[1] == "l" else box[2] - 1
            y = box[3] - 1.5 if corner[0] == "t" else box[1] + 1.5
            ax.text(x, y, lab, color="#0b0b0b", fontsize=8.5, va="top" if corner[0] == "t" else "bottom",
                    ha="left" if corner[1] == "l" else "right", fontweight="bold", path_effects=halo)
    for x, y, t in labels:
        ax.text(x, y, t, color="#0b0b0b", fontsize=6.8, ha="center", va="center", path_effects=halo)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_xlabel("x (µm)", color="#52514e", fontsize=8)
    ax.set_ylabel("y (µm)", color="#52514e", fontsize=8)
    ax.tick_params(labelsize=7, colors="#898781")
    if title:
        ax.set_title(title, loc="left", fontsize=10, color="#0b0b0b")
    if legend:
        ax.legend(handles=[Patch(facecolor=c, edgecolor=c, alpha=0.6, label=lab) for lab, c in legend],
                  loc="upper center", bbox_to_anchor=(0.5, -0.07), ncol=2, fontsize=7.5,
                  frameon=False)
    fig.tight_layout()
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return out
