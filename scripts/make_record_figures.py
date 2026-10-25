#!/usr/bin/env python3
"""Figures for docs/flow_record.md (the living record of the flow).

usage (inside layout-s0s3):  python3 scripts/make_record_figures.py <design> [<design> ...]

For each design it writes into docs/flow_record/img/:
  <design>_pcell_montage.png   klayout renders of every PCell device with its DRC/LVS verdict
  <design>_pcell_evidence.png  verbatim lines from the Magic DRC logs and Netgen LVS reports
                               (positive run and negative control), so the reader sees the tool
                               output itself, not our summary of it
  <design>_s1_*.png            copies of the S1 plots (if S1 has run)
Every number on the figures is read from the report files named on the figure.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
IMG = REPO / "docs" / "flow_record" / "img"


def grep(path: Path, pats: list[str]) -> list[str]:
    if not path.exists():
        return [f"(missing: {path.relative_to(REPO)})"]
    out = []
    for line in path.read_text(errors="replace").splitlines():
        if any(re.search(p, line) for p in pats):
            out.append(line.strip())
    return out


def crop(img, pad: int = 12):
    """Trim the white canvas around a KLayout render (keeps the drawing untouched)."""
    import numpy as np
    rgb = img[..., :3]
    mask = (rgb < 0.97).any(axis=2)
    if not mask.any():
        return img
    ys, xs = np.where(mask)
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, img.shape[0])
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, img.shape[1])
    return img[y0:y1, x0:x1]


def montage(design: str, pb: dict) -> Path:
    devs = pb["devices"]
    fig, axs = plt.subplots(1, len(devs), figsize=(2.9 * len(devs), 7.2))
    for ax, d in zip(axs, devs):
        img = crop(mpimg.imread(REPO / d["png"]))
        ax.imshow(img)
        ax.set_xticks([]); ax.set_yticks([])
        p = d["params"]
        kind = "pfet" if "pfet" in d["pcell"] else "nfet"
        ok = d["drc"]["pass"] and d["lvs"]["pass"]
        ax.set_title(f"{d['device']}  {kind}_01v8\nW={p['w']:g} L={p['l']:g} nf={p['nf']} m={p['m']}", fontsize=10)
        ax.set_xlabel(f"DRC errors: {d['drc']['errors']}  (neg. ctl flagged: {d['drc']['neg_control_flagged']})\n"
                      f"LVS: {'match' if d['lvs']['match'] else 'MISMATCH'}  (neg. ctl rejected: {d['lvs']['neg_control_rejected']})",
                      fontsize=8.5, color="#1a7f37" if ok else "#cf222e")
    fig.suptitle(f"{design}: Magic open_pdks PCells (default options), rendered with KLayout + sky130A.lyp", fontsize=11)
    fig.tight_layout()
    out = IMG / f"{design}_pcell_montage.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)
    return out


def prop_errors(path: Path) -> str:
    """Property differences from Netgen's JSON report (list of circuit comparisons)."""
    if not path.exists():
        return "(no lvs_report.json)"
    out = []
    for c in json.loads(path.read_text()):
        for pair in c.get("properties", []) or []:
            a, b = pair
            out.append(f"layout {a[1]} vs reference {b[1]}")
    return "; ".join(out) if out else "none"


def evidence(design: str, pb: dict) -> Path:
    s0 = REPO / "outputs" / "S0" / design / "pcell"
    lines = []
    for d in pb["devices"]:
        n = d["device"]
        lines.append(f"== {n}  ({d['pcell']}  w={d['params']['w']:g} l={d['params']['l']:g} nf={d['params']['nf']})")
        for ln in grep(s0 / f"drc_{n}" / "drc_magic.log", [r"^DRC_TOTAL", r"^NEG_CONTROL_TOTAL"]):
            lines.append(f"  drc_{n}/drc_magic.log        : {ln}")
        for ln in grep(s0 / f"lvs_{n}" / "lvs" / "lvs_report.txt", [r"^Final result", r"Property errors", r"Netlists"]):
            lines.append(f"  lvs_{n}/lvs/lvs_report.txt   : {ln}")
        lines.append(f"  lvs_{n}/lvs/lvs_report.json  : property differences: "
                     f"{prop_errors(s0 / f'lvs_{n}' / 'lvs' / 'lvs_report.json')}")
        for ln in grep(s0 / f"lvs_{n}" / "lvs_negctl" / "lvs_report.txt", [r"^Final result", r"Property errors", r"Netlists"]):
            lines.append(f"  lvs_{n}/lvs_negctl (L+0.1um) : {ln}")
        lines.append(f"  lvs_{n}/lvs_negctl json      : property differences: "
                     f"{prop_errors(s0 / f'lvs_{n}' / 'lvs_negctl' / 'lvs_report.json')}")
        lines.append(f"  -> flow verdict (pcell_binding.json): DRC {'PASS' if d['drc']['pass'] else 'FAIL'}, "
                     f"LVS {'MATCH' if d['lvs']['match'] else 'NO MATCH'}, "
                     f"negative control {'REJECTED (checker live)' if d['lvs']['neg_control_rejected'] else 'NOT REJECTED'}")
    h = 0.165 * len(lines) + 0.7
    fig = plt.figure(figsize=(12.5, h))
    fig.text(0.01, 1 - 0.12 / h, f"{design}: verbatim tool output (paths under outputs/S0/{design}/pcell/)",
             va="top", fontsize=10, weight="bold")
    fig.text(0.01, 1 - 0.45 / h, "\n".join(lines), va="top", family="monospace", fontsize=8.2, linespacing=1.25)
    out = IMG / f"{design}_pcell_evidence.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)
    return out


def s3_montage(design: str) -> list:
    """Chosen device cells (and the default PCell for comparison) with their sign-off verdicts."""
    f = REPO / "outputs" / "S3" / design / "device_decisions.json"
    if not f.exists():
        return []
    dec = json.loads(f.read_text())["decisions"]
    panels = []
    for tid, d in dec.items():
        dv = d.get("vs_default") or {}
        if dv.get("default_cell") and dv["default_cell"] != d["cell"]:
            panels.append(("default", tid, dv["default_cell"], None))
        panels.append(("chosen", tid, d["cell"], d))
    fig, axs = plt.subplots(1, len(panels), figsize=(2.7 * len(panels), 6.4))
    axs = axs if len(panels) > 1 else [axs]
    for ax, (kind, tid, cell, d) in zip(axs, panels):
        png = REPO / "outputs" / "S3" / "_cells" / cell / f"{cell}.png"
        if png.exists():
            ax.imshow(crop(mpimg.imread(png)))
        ax.set_xticks([]); ax.set_yticks([])
        rec = json.loads((REPO / "outputs" / "S3" / "_cells" / cell / "record.json").read_text())
        opt = rec["option"]["id"]
        devs = ", ".join(dec[tid]["devices"])
        ax.set_title(f"{kind.upper()}  {devs}\n{opt}\narea {rec['geometry']['area_um2']:.1f} um2", fontsize=8,
                     color="#1a7f37" if kind == "chosen" else "#57606a")
        ax.set_xlabel(f"DRC {rec['drc']['errors']} (neg ctl {rec['drc']['neg_control_flagged']})\n"
                      f"LVS {'match' if rec['lvs']['match'] else 'MISMATCH'} (neg ctl {rec['lvs']['neg_control_rejected']})",
                      fontsize=7.5, color="#1a7f37" if rec.get("ok") else "#cf222e")
    fig.suptitle(f"{design}: S3 device cells (SKY130 Magic PCell + finger straps), default vs chosen", fontsize=10)
    fig.tight_layout()
    out = IMG / f"{design}_s3_cells.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)
    lines = []
    for tid, d in dec.items():
        c = REPO / "outputs" / "S3" / "_cells" / d["cell"]
        lines.append(f"== {d['cell']}  ({', '.join(d['devices'])})")
        for ln in grep(c / "drc" / "drc_magic.log", [r"^DRC_TOTAL", r"^NEG_CONTROL_TOTAL"]):
            lines.append(f"  drc/drc_magic.log            : {ln}")
        for ln in grep(c / "lvs" / "lvs" / "lvs_report.txt", [r"^Final result", r"Property errors", r"Netlists"]):
            lines.append(f"  lvs/lvs/lvs_report.txt       : {ln}")
        lines.append(f"  lvs/lvs/lvs_report.json      : property differences: {prop_errors(c / 'lvs' / 'lvs' / 'lvs_report.json')}")
        for ln in grep(c / "lvs" / "lvs_negctl" / "lvs_report.txt", [r"^Final result", r"Property errors"]):
            lines.append(f"  lvs/lvs_negctl (L+0.1um)     : {ln}")
    h = 0.165 * len(lines) + 0.7
    fig = plt.figure(figsize=(12.5, h))
    fig.text(0.01, 1 - 0.12 / h, f"{design}: chosen S3 cells, verbatim tool output (outputs/S3/_cells/<cell>/)",
             va="top", fontsize=10, weight="bold")
    fig.text(0.01, 1 - 0.45 / h, "\n".join(lines), va="top", family="monospace", fontsize=8.2, linespacing=1.25)
    out2 = IMG / f"{design}_s3_evidence.png"
    fig.savefig(out2, dpi=110)
    plt.close(fig)
    return [out, out2]


def main(argv: list[str]) -> int:
    IMG.mkdir(parents=True, exist_ok=True)
    for design in argv:
        pbf = REPO / "outputs" / "S0" / design / "pcell_binding.json"
        if pbf.exists():
            pb = json.loads(pbf.read_text())
            print(montage(design, pb).relative_to(REPO))
            print(evidence(design, pb).relative_to(REPO))
        for st in ("S1", "S2", "S3"):
            plots = REPO / "outputs" / st / design / "plots"
            for p in sorted(plots.glob("*.png")) if plots.exists() else []:
                dst = IMG / f"{design}_{st.lower()}_{p.name}"
                shutil.copyfile(p, dst)
                print(dst.relative_to(REPO))
        for f in s3_montage(design):
            print(f.relative_to(REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
