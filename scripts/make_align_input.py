#!/usr/bin/env python3
"""Convert a sized sky130 subcircuit (xschem netlist) into an ALIGN-SKY130 input folder.

Usage:
    python3 scripts/make_align_input.py <sized.spice> <out_dir> [--subckt NAME] [--bias-port NAME]

What it does (and logs every deviation in <out_dir>/conversion_report.json):
  * keeps connectivity and terminal order (D G S B) of every MOSFET;
  * removes ideal bias voltage sources and exposes their positive node as a port
    (ALIGN lays out devices only; the source belongs to the testbench);
  * legalises widths for ALIGN-pdk-sky130 (gen_param.py asserts):
      - per-finger width must be a multiple of Fin_pitch = 210 nm,
      - NF must be even;
    it picks the even NF and fin count whose total width is closest to the
    reference (ties -> fewer fingers);  ASSUMPTION, ALIGN-only;
  * keeps L as written, but records that ALIGN-pdk-sky130 draws a fixed 150 nm
    poly (layers.json Poly Width = 150) - so L != 0.15 um cannot be represented.
Nothing here edits the source file.
"""
import argparse
import json
import re
from pathlib import Path

FIN_PITCH_UM = 0.21
ALIGN_POLY_L_UM = 0.15


def read_logical_lines(path: Path):
    lines, cur = [], ""
    for raw in path.read_text().splitlines():
        if raw.startswith("+"):
            cur += " " + raw[1:].strip()
        else:
            if cur:
                lines.append(cur)
            cur = raw.strip()
    if cur:
        lines.append(cur)
    return lines


def parse(path: Path, subckt_name=None):
    ports, devices, sources = None, [], []
    for ln in read_logical_lines(path):
        low = ln.lower()
        m = re.match(r"^\*{0,2}\.subckt\s+(\S+)\s+(.*)$", ln, re.I)
        if m:
            subckt_name = subckt_name or m.group(1)
            ports = m.group(2).split()
            continue
        if not ln or ln.startswith("*") or low.startswith("."):
            continue
        tok = ln.split()
        name = tok[0]
        if name[0] in "Xx" and len(tok) >= 6 and "fet" in tok[5]:
            params = dict(re.findall(r"(\w+)\s*=\s*([^\s]+)", ln))
            params = {k.upper(): v for k, v in params.items()}
            devices.append({
                "ref_name": name, "d": tok[1], "g": tok[2], "s": tok[3], "b": tok[4],
                "model": tok[5],
                "W_um": float(params["W"]), "L_um": float(params["L"]),
                "nf": int(float(params.get("NF", 1))), "m": int(float(params.get("MULT", params.get("M", 1)))),
            })
        elif name[0] in "Vv":
            sources.append({"name": name, "p": tok[1], "n": tok[2], "value": " ".join(tok[3:])})
        else:
            raise ValueError(f"unsupported element: {ln}")
    if ports is None:
        raise ValueError("no .subckt line found")
    return subckt_name, ports, devices, sources


def legalise_width(w_total_um, max_fins=12, min_fins=2):
    """Closest even-NF x k-fin realisation. ALIGN-pdk-sky130 limits: mos.py asserts
    fin > 1 and (height - fin)/2 >= 8 with the default unit-cell height of 28 fins,
    so 2 <= k <= 12. Ties -> fewer fingers."""
    best = None
    for nf in range(2, 129, 2):
        k = round(w_total_um / (FIN_PITCH_UM * nf))
        if k < min_fins or k > max_fins:
            continue
        w = round(k * FIN_PITCH_UM * nf, 6)
        cand = (abs(w - w_total_um), nf, k, w)
        if best is None or cand[:2] < best[:2]:
            best = cand
    err, nf, k, w = best
    return {"nf": nf, "fins_per_finger": k, "w_finger_um": round(k * FIN_PITCH_UM, 6),
            "w_total_um": w, "rel_error": round((w - w_total_um) / w_total_um, 6)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sized_spice")
    ap.add_argument("out_dir")
    ap.add_argument("--subckt", default=None, help="name for the ALIGN subckt (default: from file)")
    ap.add_argument("--bias-port", default="VBIAS", help="port name for nets driven by ideal sources")
    a = ap.parse_args()

    src = Path(a.sized_spice)
    name, ports, devs, srcs = parse(src)
    name = (a.subckt or name).lower().replace("-", "_")
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    report = {"source": str(src), "subckt": name, "assumptions": [], "devices": [], "removed_sources": []}
    new_ports = [p.lower() for p in ports]
    rename = {}
    for s in srcs:
        # an ideal source from an internal node to a rail: expose the node as a port
        rename[s["p"]] = a.bias_port
        new_ports.append(a.bias_port.lower())
        report["removed_sources"].append({**s, "exposed_as_port": a.bias_port})
    report["assumptions"].append(
        "ASSUMPTION (ALIGN-only): widths legalised to even NF x (k x 210 nm); see devices[].align")
    report["assumptions"].append(
        f"LIMITATION: ALIGN-pdk-sky130 draws a fixed {ALIGN_POLY_L_UM} um gate (layers.json Poly Width=150 nm); "
        "devices with other L are NOT represented correctly; LVS against the reference will flag it")

    lines = [f".subckt {name} " + " ".join(new_ports)]
    for i, d in enumerate(devs):
        w_ref = d["W_um"] * d["nf"] * d["m"]          # xschem/sky130: W is total per device instance
        leg = legalise_width(w_ref)
        aname = "M" + d["ref_name"].lstrip("Xx").lstrip("Mm")
        nets = [rename.get(d[t], d[t]).lower() for t in ("d", "g", "s", "b")]
        lines.append(f"{aname} {' '.join(nets)} {d['model']} L={d['L_um']:.3g}e-6 w={leg['w_finger_um']:.4g}e-6 nf={leg['nf']}")
        report["devices"].append({**d, "align_name": aname, "w_total_ref_um": w_ref, "align": leg,
                                  "L_represented_by_align": abs(d["L_um"] - ALIGN_POLY_L_UM) < 1e-9})
    lines.append(f".ends {name}")
    (out / f"{name}.sp").write_text("\n".join(lines) + "\n")
    const = [{"constraint": "PowerPorts", "ports": ["vdd"]},
             {"constraint": "GroundPorts", "ports": ["vss"]}]
    (out / f"{name}.const.json").write_text(json.dumps(const, indent=2) + "\n")
    (out / "conversion_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print((out / f"{name}.sp").read_text())
    for d in report["devices"]:
        print(f"{d['ref_name']}: W_ref={d['w_total_ref_um']} -> {d['align']['w_total_um']} "
              f"(nf={d['align']['nf']}, {d['align']['fins_per_finger']} fins/finger, err={d['align']['rel_error']:+.2%}); "
              f"L={d['L_um']} represented={d['L_represented_by_align']}")


if __name__ == "__main__":
    main()
