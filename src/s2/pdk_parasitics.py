"""S2 step 0 — interconnect parasitics per unit length, measured on the PDK itself.

Nothing here is typed in by hand:
  * minimum width and spacing per layer are read from the Magic DRC rules of sky130A.tech
    (rule ids li.1/li.3, met1.1/met1.2, ...);
  * sheet and contact resistances are read from the extract section of sky130A.tech
    (milliohm/square and milliohm/contact), i.e. the values Magic uses for PEX;
  * capacitance per um is MEASURED by extracting test wires with Magic (the same extractor S6 uses):
      - one wire of length 50 um and 100 um at minimum width   -> C to substrate per um,
      - two parallel wires at minimum spacing, 50 and 100 um   -> coupling C per um.
    Taking the difference of the two lengths removes the end (fringe) contributions.
Wires sit over field oxide/substrate with nothing above them. Real routes over devices or under
other metal see more capacitance; S6 extraction checks the real values.

usage (inside layout-s0s3):  python3 -m src.s2.pdk_parasitics   -> outputs/S2/pdk/parasitics.json
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from src.common.tools import PDK_ROOT, REPO, TOOL_ENV, provenance, rel, write_json

TECH = Path(PDK_ROOT) / "sky130A/libs.tech/magic/sky130A.tech"
MAGICRC = Path(PDK_ROOT) / "sky130A/libs.tech/magic/sky130A.magicrc"
LAYERS = {  # magic paint layer: (DRC width rule id, DRC spacing rule id, extract resist class)
    "locali": ("li.1", "li.3", "allli"),
    "metal1": ("met1.1", "met1.2", "allm1"),
    "metal2": ("met2.1", "met2.2", "allm2"),
    "metal3": ("met3.1", "met3.2", "allm3"),
    "metal4": ("met4.1", "met4.2", "allm4"),
}
CONTACTS = {"licon_ndiff": "ndc", "licon_pdiff": "pdc", "licon_poly": "pc", "mcon": "mcon",
            "via1": "m2c", "via2": "m3c", "via3": "via3"}
POLY_CLASS = "allpolynonres"
BELOW = {"locali": "poly", "metal1": "locali", "metal2": "metal1", "metal3": "metal2", "metal4": "metal3"}


def tech_rules() -> dict:
    """Min width/spacing (um) per layer from the DRC section, sheet/contact R from the extract section
    (first extract style = nominal)."""
    t = re.sub(r"\\\s*\n", " ", TECH.read_text())  # join backslash-continued rule lines
    out: dict = {"source": rel(TECH) if str(TECH).startswith(str(REPO)) else str(TECH), "layers": {}, "contacts": {}}
    for layer, (wid, sid, rcls) in LAYERS.items():
        w = re.search(r"^\s*width\s+\S+\s+(\d+)\s+\"[^\"]*\(" + re.escape(wid) + r"\)\"", t, re.M)
        s = re.search(r"^\s*spacing\s+.*?\s(\d+)\s+(?:touching_ok\s+)?\"[^\"]*\(" + re.escape(sid) + r"\)\"", t, re.M)
        r = re.search(r"^\s*resist\s+\(" + re.escape(rcls) + r"\)/\S+\s+(\d+)", t, re.M)
        out["layers"][layer] = {"min_width_um": int(w.group(1)) / 1000 if w else None, "width_rule": wid,
                                "min_spacing_um": int(s.group(1)) / 1000 if s else None, "spacing_rule": sid,
                                "sheet_res_ohm_sq": int(r.group(1)) / 1000 if r else None}
    for name, ctype in CONTACTS.items():
        m = re.search(r"^\s*contact\s+(?:\S+,)*" + re.escape(ctype) + r"(?:,\S+)*\s+(\d+)", t, re.M)
        out["contacts"][name] = {"magic_type": ctype, "ohm_per_contact": int(m.group(1)) / 1000 if m else None}
    m = re.search(r"^\s*resist\s+\(" + POLY_CLASS + r"\)/\S+\s+(\d+)", t, re.M)
    out["poly_sheet_res_ohm_sq"] = int(m.group(1)) / 1000 if m else None
    return out


def _wire_cell(name: str, layer: str, w: float, s: float, length: float, pair: bool, plane: str | None = None) -> str:
    cmds = [f"load {name} -silent", "box 0 0 0 0"]
    if plane:  # a wide plate of the layer below, extending 2 um past the wire on every side
        cmds += [f"box -2um -2um {length + 2}um {w + 2}um", f"paint {plane}", f"label P c {plane}"]
    cmds += [f"box 0um 0um {length}um {w}um", f"paint {layer}", f"label A c {layer}"]
    if pair:
        y0 = w + s
        cmds += [f"box 0um {y0}um {length}um {y0 + w}um", f"paint {layer}", f"label B c {layer}"]
    cmds += ["port makeall", f"save {name}", "extract all", "ext2spice cthresh 0", "ext2spice format ngspice",
             f"ext2spice -o {name}.spice"]
    return "\n".join(cmds)


def measure(work: Path) -> dict:
    rules = tech_rules()
    work.mkdir(parents=True, exist_ok=True)
    cells = []
    tcl = ["drc off", "snap internal"]
    for layer, r in rules["layers"].items():
        for L in (50, 100):
            for pair in (False, True):
                name = f"w_{layer}_{'pair' if pair else 'single'}_{L}"
                cells.append((layer, L, pair, name))
                tcl.append(_wire_cell(name, layer, r["min_width_um"], r["min_spacing_um"], L, pair))
            name = f"w_{layer}_plane_{L}"
            cells.append((layer, L, "plane", name))
            tcl.append(_wire_cell(name, layer, r["min_width_um"], r["min_spacing_um"], L, False, BELOW[layer]))
    tcl.append("quit -noprompt")
    (work / "wires.tcl").write_text("\n".join(tcl) + "\n")
    p = subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", str(MAGICRC), str(work / "wires.tcl")],
                       cwd=work, env=TOOL_ENV, capture_output=True, text=True, timeout=600)
    (work / "wires_magic.log").write_text(p.stdout + p.stderr)
    caps: dict = {}
    for layer, L, pair, name in cells:
        f = work / f"{name}.spice"
        cg, cc = 0.0, 0.0
        if f.exists():
            for m in re.finditer(r"^C\S*\s+(\S+)\s+(\S+)\s+([0-9.eE+-]+)([afpnum]?)", f.read_text(), re.M):
                a, b, v, u = m.groups()
                val = float(v) * {"a": 1e-18, "f": 1e-15, "p": 1e-12, "n": 1e-9, "u": 1e-6, "m": 1e-3, "": 1.0}[u]
                nets = {a, b}
                if nets == {"A", "B"}:
                    cc += val
                elif "A" in nets:   # to substrate, or to the plate below (counted as total C to 'ground')
                    cg += val
        caps[(layer, L, pair)] = {"A_to_substrate_F": cg, "A_to_B_F": cc, "file": rel(f)}
    out = {}
    for layer, r in rules["layers"].items():
        s50, s100 = caps[(layer, 50, False)], caps[(layer, 100, False)]
        p50, p100 = caps[(layer, 50, True)], caps[(layer, 100, True)]
        w = r["min_width_um"]
        pl50, pl100 = caps[(layer, 50, "plane")], caps[(layer, 100, "plane")]
        c_plane = (pl100["A_to_substrate_F"] - pl50["A_to_substrate_F"]) / 50
        c_field = (s100["A_to_substrate_F"] - s50["A_to_substrate_F"]) / 50
        out[layer] = {
            **r,
            "cap_over_lower_plane_F_per_um": c_plane, "lower_plane_layer": BELOW[layer],
            "cap_worst_F_per_um": max(c_plane, c_field),
            "res_ohm_per_um_at_min_width": r["sheet_res_ohm_sq"] / w if r["sheet_res_ohm_sq"] else None,
            "cap_to_substrate_F_per_um_single": (s100["A_to_substrate_F"] - s50["A_to_substrate_F"]) / 50,
            "cap_to_substrate_F_per_um_in_pair": (p100["A_to_substrate_F"] - p50["A_to_substrate_F"]) / 50,
            "coupling_F_per_um_at_min_spacing": (p100["A_to_B_F"] - p50["A_to_B_F"]) / 50,
            "raw": {f"{k[1]}um_{k[2] if k[2] == 'plane' else ('pair' if k[2] else 'single')}": v
                    for k, v in caps.items() if k[0] == layer},
        }
    return {"rules": rules, "layers": out, "magic_log": rel(work / "wires_magic.log"),
            "method": "Magic extraction (sky130A.tech nominal style) of straight min-width wires over field; "
                      "per-um values from the 100 um - 50 um difference",
            "caveat": "two environments measured: over field and over a plate of the layer below; the larger "
                      "(cap_worst_F_per_um) is used for length rules. Metal above a route adds more; S6 checks."}


def main() -> int:
    out = REPO / "outputs" / "S2" / "pdk"
    res = measure(out / "work")
    res["provenance"] = provenance([TECH])
    write_json(out / "parasitics.json", res)
    ok = all(v["coupling_F_per_um_at_min_spacing"] > 0 and v["cap_to_substrate_F_per_um_single"] > 0
             for v in res["layers"].values())
    for k, v in res["layers"].items():
        print(f"{k:7s} w={v['min_width_um']} s={v['min_spacing_um']}  R={v['res_ohm_per_um_at_min_width']:.4g} ohm/um  "
              f"Cg={v['cap_to_substrate_F_per_um_single']*1e18:.2f} aF/um  Cplane={v['cap_over_lower_plane_F_per_um']*1e18:.2f} aF/um  "
              f"Cc={v['coupling_F_per_um_at_min_spacing']*1e18:.2f} aF/um")
    print("PDK parasitics", "OK" if ok else "INCOMPLETE", "->", rel(out / "parasitics.json"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
