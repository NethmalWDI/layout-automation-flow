#!/usr/bin/env python3
"""Schematic pictures of the structure groups the flow uses (matched pairs, mirrors, dummies...), with the
SPICE device names: each device of a group is boxed in the group's colour and tagged with the group number,
on the designers' own xschem schematic. Output: docs/flow_record/img/<design>_groups_<schematic>.svg and a
Markdown table of the groups (docs/flow_record/img/<design>_groups.md).

  python3 scripts/schematic_groups.py ttsky25a_fd            # inside the EDA image (xschem + Xvfb)
  python3 scripts/schematic_groups.py ttsky25a_fd --svg-dir runs/tmp/xs   # reuse exported SVGs

The groups are the IR's hierarchy blocks (circuits/<design>/upstream/primitives.json, PREDICTED unless the
designer annotated them), with S1's view where it differs (an L-ratioed mirror is split into its equal-L
subsets, outputs/S1/<design>/intent.json).
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# per design: schematic -> how a flat SPICE name maps to an instance name of that schematic
DESIGNS = {
    "ttsky25a_fd": {
        "src": "runs/tmp/ttsky25a_fd_pkg/Opamp_Design/src",     # private copy made by make_ttsky25a_package.py
        "sheets": {"Opamp_with_bias": r"^X(M\d+|C\d+)$", "Diff_opamp": r"^XX1_(M\d+)$",
                   "Common_source_stage": r"^XX2_(M\d+)$"},
    },
}
KIND_COLOUR = {"differential-pair": "#1f77b4", "current-mirror": "#ff7f0e", "current-mirror-load": "#d62728",
               "matched-current-source-pair": "#2ca02c", "matched-cascode-pair": "#9467bd",
               "L-ratioed": "#8c564b", "dummy": "#7f7f7f"}
PALETTE = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#17becf", "#bcbd22",
           "#393b79", "#ad494a", "#637939", "#8c6d31", "#7b4173", "#3182bd", "#e6550d", "#31a354", "#756bb1"]


def export_svgs(design: str, out: Path) -> None:
    cfg = DESIGNS[design]
    rc = Path(os.environ.get("PDK_ROOT", "/foss/pdks")) / "sky130A/libs.tech/xschem/xschemrc"
    out.mkdir(parents=True, exist_ok=True)
    for s in cfg["sheets"]:
        cmd = ["xvfb-run", "-a", "-s", "-screen 0 2200x1500x24", "xschem", "-q", "--rcfile", str(rc), "--command",
               f"set dark_colorscheme 0; xschem build_colors; xschem zoom_full; xschem print svg {out / (s + '.svg')}; exit",
               f"{s}.sch"]
        subprocess.run(cmd, cwd=REPO / cfg["src"], capture_output=True, text=True, timeout=120)


def groups_of(design: str) -> list:
    ir = json.loads((REPO / "outputs" / "S0" / design / "circuit_ir.json").read_text())
    intent_f = REPO / "outputs" / "S1" / design / "intent.json"
    intent = json.loads(intent_f.read_text()) if intent_f.exists() else {}
    split = {tuple(sorted(b["devices"])): b["subsets"] for b in intent.get("not_matching_blocks", [])
             if b.get("kind") == "L-ratioed mirror"}
    out = []
    for b in ir["hierarchy"]["blocks"]:
        devs = [d for d in b["devices"] if d.startswith("X")]
        if len(devs) < 2 and "dummy" not in b["primitive"]:
            continue
        prim = re.sub(r"^[np]mos-", "", b["primitive"])
        if tuple(sorted(devs)) in split:
            for i, sub in enumerate(split[tuple(sorted(devs))]):
                lab = f"{b['primitive']} ratioed by L, subset {i + 1}" + (" (single device: nothing to match)" if len(sub) == 1 else "")
                out.append({"kind": "L-ratioed", "label": lab, "devices": sub})
        else:
            out.append({"kind": prim, "label": b["primitive"], "devices": devs})
    return out


def annotate(svg: str, members: dict) -> tuple[str, list]:
    """members: instance name -> (group number, colour). Boxes each instance label's device and tags it."""
    placed, extra = [], []
    for m in re.finditer(r'<text[^>]*transform="translate\(([-0-9.]+),\s*([-0-9.]+)\)"[^>]*>([^<]+)</text>', svg):
        name = html.unescape(m.group(3)).strip()
        if name not in members:
            continue
        x, y = float(m.group(1)), float(m.group(2))
        g, col = members[name]
        extra.append(f'<rect x="{x - 14:.1f}" y="{y - 6:.1f}" width="46" height="40" rx="3" fill="{col}" '
                     f'fill-opacity="0.13" stroke="{col}" stroke-width="1.2"/>')
        extra.append(f'<text x="{x - 13:.1f}" y="{y + 32:.1f}" font-size="7.5" font-weight="bold" fill="{col}">G{g}</text>')
        placed.append(name)
    svg = re.sub(r'(<rect class="l0"[^>]*/>)', r'\1' + "".join(extra), svg, count=1) if extra else svg
    # light background, dark wires/text (xschem's SVG export keeps the screen's dark scheme)
    svg = re.sub(r"(\.l0\{\s*fill:\s*)#[0-9a-fA-F]{6}", r"\1#ffffff", svg)
    return svg, placed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("design")
    ap.add_argument("--svg-dir", default=None, help="use these xschem SVG exports instead of running xschem")
    a = ap.parse_args()
    cfg = DESIGNS[a.design]
    svg_dir = Path(a.svg_dir) if a.svg_dir else REPO / "runs" / "tmp" / f"{a.design}_schematic_svg"
    if not a.svg_dir:
        export_svgs(a.design, svg_dir)
    groups = groups_of(a.design)
    img = REPO / "docs" / "flow_record" / "img"
    img.mkdir(parents=True, exist_ok=True)
    rows, placed_all = [], set()
    for i, g in enumerate(groups, start=1):
        g["n"], g["colour"] = i, ("#7f7f7f" if g["kind"] == "dummy" else PALETTE[(i - 1) % len(PALETTE)])
    for sheet, pat in cfg["sheets"].items():
        f = svg_dir / f"{sheet}.svg"
        if not f.exists():
            continue
        members = {}
        for g in groups:
            for d in g["devices"]:
                mm = re.match(pat, d)
                if mm:
                    members[mm.group(1)] = (g["n"], g["colour"])
                    g.setdefault("sheet", sheet)
        out_svg, placed = annotate(f.read_text(), members)
        (img / f"{a.design}_groups_{sheet}.svg").write_text(out_svg)
        placed_all |= {f"{sheet}:{p}" for p in placed}
    lines = [f"| G | kind | devices (SPICE name -> schematic instance) | sheet |", "|---|---|---|---|"]
    for g in groups:
        if g["kind"] == "dummy":
            continue
        names = []
        for d in g["devices"]:
            inst = next((re.match(p, d).group(1) for s, p in cfg["sheets"].items() if re.match(p, d)), d)
            names.append(f"{d} -> {inst}")
        lines.append(f"| G{g['n']} | {g['label']} | {', '.join(names)} | {g.get('sheet', '')} |")
    dummies = [d for g in groups if g["kind"] == "dummy" for d in g["devices"]]
    if dummies:
        lines.append(f"| (grey) | dummy | {', '.join(dummies)} | |")
    (img / f"{a.design}_groups.md").write_text("\n".join(lines) + "\n")
    print(f"{len(groups)} groups, {len(placed_all)} instances boxed -> {img}/{a.design}_groups_*.svg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
