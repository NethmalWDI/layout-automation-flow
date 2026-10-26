#!/usr/bin/env python3
"""Turn one LOADBench Pareto point into a design package for this flow (S0 input).

LOADBench (MLCAD'26, Zenodo 10.5281/zenodo.21759759, CC BY 4.0) ships, per op-amp: the sized
netlist template (example_run/CombinedTestBench.cir + params.cir), the Pareto-optimal sizes and their
simulated metrics (FinalPOF*.csv), and a structure recognition (struct_recognition.xml). It has no
specs, no noise testbench, no symbolic model, and its bias current source and Miller capacitor are
ideal elements. This script copies what exists and marks what is predicted:

  circuits/<design>/source/<design>.spice          sized DUT (numbers from the chosen CSV row)
  circuits/<design>/source/config.yaml             interface, conditions, specs (ASSUMPTION rule)
  circuits/<design>/source/loadbench_reference.json the row's LOADBench metrics (external reference)
  circuits/<design>/testbenches/diso_amp_{AC,OP,NOISE}.spice   our testbench convention
  circuits/<design>/upstream/primitives.json, hierarchy.json   from struct_recognition.xml (real)
  circuits/<design>/upstream/name_map.yaml          identity map
  circuits/<design>/upstream/equations.predicted.json  textbook two-stage Miller model (PREDICTED)
  circuits/<design>/SOURCE.md                       provenance, selection rule, licence

usage:  python3 scripts/make_loadbench_package.py <loadbench folder> <design> [--row N | --select]
Nothing in the LOADBench folder is modified.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]

# Selection rule for --select (ASSUMPTION, written into SOURCE.md): a stable, mid-performance point,
# not the extreme of any objective. Lowest device area among points with PM 55..75 deg,
# gain > 45 dB, GBW > 10 MHz, power < 1.5 mW.
SELECT = {"pm_deg": (55.0, 75.0), "gain_db_min": 45.0, "ft_hz_min": 10e6, "p_w_max": 1.5e-3}

# Testbench conditions: LOADBench's own (vdd 1.8 V, Cload 1 pF, ibias 10 uA, 27 C, tt); the input
# common mode is vdd/2 as in its open-loop bench.
CONDITIONS = {"VDD_V": 1.8, "VCM_V": 0.9, "CL_F": "1p", "temp": 27, "corner": "tt"}
IBIAS_A = 10e-6

# Spec rule (ASSUMPTION; LOADBench has no specs): derived from this flow's own re-simulation of the
# point (S0, specs_from_achieved) so that a library difference cannot make the spec unreachable;
# PM is the common 60 deg target; power gets 10 % headroom over the LOADBench value.
SPEC_RULE = {"gain_db": {"min_delta": -1.0}, "gbw_mhz": {"min_factor": 0.9}}
SPEC_FIXED = {"pm_deg": {"min": 60}}
POWER_HEADROOM = 1.10


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_params(params_cir: Path) -> dict:
    out = {}
    for ln in params_cir.read_text().splitlines():
        m = re.match(r"^\.param\s+(\w+)\s*=\s*(\S+)", ln.strip())
        if m:
            out[m.group(1)] = m.group(2)
    return out


def resolve(name: str, row: dict, rel: dict, seen=()) -> float:
    if name in row and row[name] != "":
        return float(row[name])
    expr = rel.get(name)
    if expr is None:
        raise KeyError(f"{name}: not in the CSV row and not defined in params.cir")
    if re.fullmatch(r"\w+", expr) and expr in rel:
        if expr in seen:
            raise ValueError(f"cyclic alias {name}")
        return resolve(expr, row, rel, seen + (name,))
    # a literal in params.cir that the CSV does not override: it is the example run's value,
    # not the Pareto point's -> refuse rather than mix two designs
    raise ValueError(f"{name} = {expr} in params.cir is not an alias and the CSV row has no value")


def subckt_block(tb: Path, name: str) -> list[str]:
    lines, inside = [], False
    for ln in tb.read_text().splitlines():
        if re.match(rf"^\.subckt\s+{re.escape(name)}\b", ln.strip()):
            inside = True
            lines.append(ln.strip())
            continue
        if inside:
            lines.append(ln.strip())
            if ln.strip().startswith(".ends"):
                break
    if not lines:
        raise SystemExit(f"subckt {name} not found in {tb}")
    return lines


def sized_dut(block: list[str], row: dict, rel: dict, design: str) -> tuple[str, list]:
    hdr = block[0].split()
    ports = hdr[2:]
    assert ports == ["ibias", "in1", "in2", "out", "sourceNmos", "sourcePmos"], ports
    out_lines = [f".subckt {design} in1 in2 out sourceNmos sourcePmos",
                 "*.ipin in1", "*.ipin in2", "*.opin out", "*.iopin sourceNmos", "*.iopin sourcePmos"]
    devices = []
    for ln in block[1:-1]:
        if not ln or ln.startswith("*"):
            continue
        tok = ln.split()
        if tok[0].upper().startswith("X"):
            name, d, g, s, b, model = tok[:6]
            vals = {}
            for key in ("w", "l", "m"):
                m = re.search(rf"\b{key}=\{{(\w+)\}}", ln)
                vals[key] = resolve(m.group(1), row, rel)
            nf = int(re.search(r"\bnf=(\d+)", ln).group(1))
            if vals["m"] != 1 or nf != 1:
                raise SystemExit(f"{name}: m={vals['m']} nf={nf}; only m=1, nf=1 handled")
            W, L = round(vals["w"], 6), round(vals["l"], 6)
            # LOADBench's own formulas for nf=1: ad=as=0.29*W, pd=ps=2*(W+0.29), nrd=nrs=0.29/W
            ad = 0.29 * W
            pd = 2 * (W + 0.29)
            nr = 0.29 / W
            out_lines.append(f"{name} {d} {g} {s} {b} {model} L={L:g} W={W:g} nf=1 ad={ad:.6g} as={ad:.6g} "
                             f"pd={pd:.6g} ps={pd:.6g} nrd={nr:.6g} nrs={nr:.6g} sa=0 sb=0 sd=0 mult=1")
            devices.append({"name": name, "model": model, "W": W, "L": L, "d": d, "g": g, "s": s, "b": b})
        elif tok[0].upper().startswith("C"):
            m = re.search(r"\{(\w+)\}", ln)
            c = resolve(m.group(1), row, rel)
            out_lines.append(f"{tok[0]} {tok[1]} {tok[2]} {c:.6g}")
            devices.append({"name": tok[0], "model": "ideal_capacitor", "C": c, "a": tok[1], "b": tok[2]})
        else:
            raise SystemExit(f"unhandled element {tok[0]}")
    # LOADBench drives 'ibias' from an ideal sink in its testbench (Ibias net_ibias 0 DC 10u). The flow
    # keeps the source inside the DUT, as the 5T example keeps its ideal V1, and declares it a bias
    # source: removed in the layout view, its node exposed as port IBIAS.
    out_lines.append(f"Ibias ibias sourceNmos {IBIAS_A:g}")
    out_lines.append(f".ends {design}")
    return "\n".join(out_lines) + "\n", devices


TB_HEAD = """* {design} on {tb}
.lib $PDK_ROOT/sky130A/libs.tech/combined/sky130.lib.spice tt
.param VDD_V=1.8 VCM_V=0.9 CL_F=1p
.temp 27

**.subckt {tb}
x1 INP INN net1 VDD 0 OUT dut_amp
Vsup VDD 0 'VDD_V'
Vinp INP 0 dc 'VCM_V' ac {ac}
* DC unity feedback, AC open loop: a 1 GH choke from OUT to INN and a 1 F capacitor from INN to
* ground. At DC the amplifier is a follower, so OUT sits at VCM as in LOADBench's offset-corrected
* open-loop bench; from 1 Hz up INN is an AC ground and the loop is open (corner ~5 uHz).
Lfb OUT INN 1G
Cfb INN 0 1
Cload OUT 0 'CL_F'
* noconn #net1
"""

TB_AC = """.control
  save all
  ac dec 40 1 1G
  let gph_deg = 180/pi * cph(v(OUT))
  meas ac gain_db find vdb(OUT) at=1
  meas ac gbw_hz  when vdb(OUT)=0
  meas ac ph_dc   find gph_deg at=1
  meas ac ph_ugb  find gph_deg when vdb(OUT)=0
  let gbw_mhz = gbw_hz / 1e6
  let pm_deg  = 180 + (ph_ugb - ph_dc)
  echo MEAS gain_db $&gain_db
  echo MEAS gbw_mhz $&gbw_mhz
  echo MEAS pm_deg $&pm_deg
  write
  quit 0
.endc
"""

TB_OP = """.control
  save all
  op
  let isup    = abs(i(vsup))
  let isup_ua = isup * 1e6
  let power_uw = isup * v(VDD) * 1e6
  let vout_v  = v(OUT)
  echo MEAS isup_ua $&isup_ua
  echo MEAS power_uw $&power_uw
  echo MEAS vout_v $&vout_v
  write
  quit 0
.endc
"""

TB_NOISE = """.control
  save all
  let npd    = 20
  let fstart = 1
  let fspot  = 1e3
  noise v(OUT) Vinp dec 20 1 1e9
  setplot noise1
  let idx = npd * log10(fspot/fstart)
  let vnoise_nv_rthz = inoise_spectrum[$&idx] * 1e9
  echo MEAS vnoise_nv_rthz $&vnoise_nv_rthz
  write
  set appendwrite
  setplot noise2
  let vnoise_rms_uv_rms = inoise_total * 1e6
  echo MEAS vnoise_rms_uv_rms $&vnoise_rms_uv_rms
  write
  quit 0
.endc
"""


def testbench(design: str, kind: str, dut: str) -> str:
    ac = {"AC": "1", "OP": "0", "NOISE": "1"}[kind]
    body = {"AC": TB_AC, "OP": TB_OP, "NOISE": TB_NOISE}[kind]
    return (TB_HEAD.format(design=design, tb=f"diso_amp_{kind}", ac=ac) + body + "**.ends\n\n"
            ".subckt dut_amp INP INN OUTN VDD VSS OUTP\n"
            f"XDUT INN INP OUTP VSS VDD {design}\n.ends\n\n" + dut + ".end\n")


# ---------------------------------------------------------------- structure -> upstream format
CATEGORY = {"MosfetDifferentialPair": ("gm-structure", "differential-pair"),
            "MosfetSimpleCurrentMirror": ("bias-structure", "current-mirror"),
            "MosfetAnalogInverter": ("gm-structure", "common-source-stage")}


def structures(xml: Path, device_names: set) -> list:
    """Top-level structures of LOADBench's recognition, with their transistors."""
    root = ET.parse(xml).getroot()
    res = root.find("structure_recognition_results")
    out = []
    # LOADBench does not say whether a mirror is a load or a bias: a mirror whose pins touch the
    # differential pair's outputs is the first stage's active load
    pair_outs = {p.get("net").lstrip("/") for st in res.findall("structure")
                 if st.get("name").startswith("MosfetDifferentialPair")
                 for p in st.find("pins").findall("pin") if p.get("name").startswith("Output")}
    for i, st in enumerate(res.findall("structure"), start=1):
        kind = st.get("name").split("[")[0]
        tech = st.get("techType")
        devs = []
        for dv in st.iter("device"):
            nm = "X" + dv.get("name").lstrip("/")[1:]  # '/mNormalTransistorPmos5' -> 'XNormalTransistorPmos5'
            if nm not in device_names:
                raise SystemExit(f"structure device {nm} not in the netlist")
            devs.append(nm)
        pins = {p.get("name"): p.get("net").lstrip("/") for p in st.find("pins").findall("pin")}
        cat, prim = CATEGORY.get(kind, ("other", kind))
        if kind == "MosfetSimpleCurrentMirror" and pair_outs & set(pins.values()):
            cat, prim = "load-structure", "current-mirror-load"
        out.append({"instance": f"X{i}", "subckt": f"{tech}_{prim}".replace("-", "_"),
                    "primitive": f"{tech}mos-{prim}" if tech in "np" else prim, "category": cat,
                    "library": f"LOADBench structure recognition: {st.get('name')}",
                    "transistors": {f"M{j}": d for j, d in enumerate(devs, start=1)}, "ports": pins})
    return out


def predicted_equations(design: str) -> dict:
    """Textbook two-stage Miller op-amp (Allen-Holberg 6.2; Razavi 10.5), in the flow's level-0 symbols:
    C1..C5 = gate-bulk, gate-source, gate-drain, drain-bulk, source-bulk of a device, G1 = gm,
    R1 = 1/gds, C_<name> = a passive's value. PREDICTED: no upstream team produced it."""
    P6, P7, N3, N4, N1, P5 = ("XNormalTransistorPmos6", "XNormalTransistorPmos7", "XNormalTransistorNmos3",
                              "XNormalTransistorNmos4", "XDiodeTransistorNmos1", "XNormalTransistorPmos5")
    return {
        "design": design, "mode": "differential", "provenance": "PREDICTED",
        "assumes": "inputs purely differential (vd = Vinp - Vinn); tail node a virtual ground; first-stage "
                   "mirror pole-zero doublet neglected; two poles and one RHP zero (no nulling resistor)",
        "source": "textbook two-stage Miller model, Allen & Holberg, CMOS Analog Circuit Design, 3rd ed., sec. 6.2; "
                  "written for this flow as a stand-in for the upstream symbolic stage (not produced upstream)",
        "naming": "level-0 symbols as in the upstream 5t-ota file: C1_<dev> gate-bulk, C2 gate-source, C3 gate-drain, "
                  "C4 drain-bulk, C5 source-bulk, G1 gm, R1 1/gds; C_<passive> the value of a netlist capacitor",
        "performance_note": "terms each in those before it; pm_deg from the dominant pole, the second pole and the RHP zero",
        "performance": {
            "circuit": design, "input": "vd", "output": "v(out)", "load": {"CL": "from out to GND"},
            "terms": {
                "gm1": f"G1_{P6}",
                "R1o": f"R1_{P6}*R1_{N4}/(R1_{P6} + R1_{N4})",
                "gm2": f"G1_{N3}",
                "R2o": f"R1_{N3}*R1_{P5}/(R1_{N3} + R1_{P5})",
                "Cc": f"C_Capacitor2 + C3_{N3}",
                "C1n": f"C2_{N3} + C1_{N3} + C4_{P6} + C4_{N4} + C3_{N4} + C3_{P6}",
                "C2n": f"CL + C4_{N3} + C4_{P5} + C3_{P5}",
                "A0": "gm1*R1o*gm2*R2o",
                "wgbw": "gm1/Cc",
                "wp2": "gm2*Cc/(C1n*C2n + Cc*(C1n + C2n))",
                "wz": "gm2/Cc",
                "wu": "wgbw",
            },
            "gain_db": "20*log(Abs(A0))/log(10)",
            "gbw_mhz": "wu/(2000000*pi)",
            "pm_deg": "180 - 180*(atan(wu*A0*Cc/gm1) + atan(wu/wp2) + atan(wu/wz))/pi",
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", help="LOADBench op-amp folder (contains FinalPOFfull.csv, example_run/)")
    ap.add_argument("design")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--row", type=int)
    g.add_argument("--select", action="store_true")
    a = ap.parse_args()
    src = (REPO / a.folder).resolve()
    rows = list(csv.DictReader((src / "FinalPOFfull.csv").open()))
    if a.select:
        ok = [i for i, r in enumerate(rows)
              if SELECT["pm_deg"][0] <= float(r["phasemargin"]) <= SELECT["pm_deg"][1]
              and float(r["dc_gain"]) > SELECT["gain_db_min"] and float(r["ft"]) > SELECT["ft_hz_min"]
              and float(r["p"]) < SELECT["p_w_max"]]
        idx = min(ok, key=lambda i: float(rows[i]["area"]))
        how = f"--select: lowest area among {len(ok)} of {len(rows)} rows meeting {SELECT}"
    else:
        idx, how = a.row, f"--row {a.row}"
    row = rows[idx]
    rel = read_params(src / "example_run" / "params.cir")
    opamp = re.search(r"OPAMP_NAME = '(\w+)'", (src / "example_run" / "standalone_tb_extract.py").read_text()).group(1)
    block = subckt_block(src / "example_run" / "CombinedTestBench.cir", opamp)
    dut, devices = sized_dut(block, row, rel, a.design)

    base = REPO / "circuits" / a.design
    for sub in ("source", "testbenches", "upstream"):
        (base / sub).mkdir(parents=True, exist_ok=True)
    (base / "source" / f"{a.design}.spice").write_text(
        f"* {a.design}: LOADBench {opamp}, FinalPOFfull.csv row {idx} (0-based), generated by "
        f"scripts/make_loadbench_package.py\n" + dut + ".end\n")
    for kind in ("AC", "OP", "NOISE"):
        (base / "testbenches" / f"diso_amp_{kind}.spice").write_text(testbench(a.design, kind, dut))

    ref = {"source": f"LOADBench {opamp}, FinalPOFfull.csv row {idx}",
           "simulator_setup": "LOADBench reduced sky130 library (reduced_sky130_combined), tt, 27 C; offset-corrected "
                              "open-loop AC, ft and PM by its own interpolation; not the same testbench as this flow",
           "metrics": {"gain_db": float(row["dc_gain"]), "gbw_mhz": float(row["ft"]) / 1e6,
                       "pm_deg": float(row["phasemargin"]), "power_uw": float(row["p"]) * 1e6,
                       "sr_pos_v_per_us": float(row["sr_pos"]) / 1e6, "sr_neg_v_per_us": float(row["sr_neg"]) / 1e6,
                       "voffset_v": float(row["voffset"]), "icmr_min_v": float(row["icmr_min"]),
                       "icmr_max_v": float(row["icmr_max"]), "vout_min_v": float(row["vout_min"]),
                       "vout_max_v": float(row["vout_max"]), "area_um2_sum_WL": float(row["area"])},
           "row": row}
    (base / "source" / "loadbench_reference.json").write_text(json.dumps(ref, indent=1) + "\n")

    p_uw = float(row["p"]) * 1e6
    cfg = {
        "name": a.design,
        "description": f"Two-stage Miller op-amp (PMOS input pair, NMOS mirror, NMOS CS second stage, ideal Miller "
                       f"capacitor, ideal 10 uA bias sink), LOADBench {opamp} row {idx}.",
        "interface": {"input": "differential", "output": "single_ended", "kind": "amp", "dut_symbol": "dut_amp",
                      "ports": {"INP": "in2", "INN": "in1", "OUTP": "out", "OUTN": "NC",
                                "VDD": "sourcePmos", "VSS": "sourceNmos"}},
        "analyses": ["AC", "OP", "NOISE"],
        "conditions": dict(CONDITIONS),
        "specs": {**SPEC_FIXED, "power_uw": {"max": round(p_uw * POWER_HEADROOM, 1)}},
        "spec_notes": {
            "ASSUMPTION": "LOADBench gives no specs. gain_db and gbw_mhz are derived by the package rule "
                          f"{SPEC_RULE} from this flow's own simulation (package key specs_from_achieved); "
                          f"pm_deg >= 60 deg is the usual target; power_uw <= {POWER_HEADROOM} x the LOADBench "
                          "value. No noise spec (LOADBench has no noise analysis; noise is reported, not specified)."},
    }
    (base / "source" / "config.yaml").write_text(
        "# Generated by scripts/make_loadbench_package.py. Specs are an ASSUMPTION (see spec_notes).\n" +
        yaml.safe_dump(cfg, sort_keys=False))

    names = {d["name"] for d in devices if d["model"] != "ideal_capacitor"}
    prims = structures(src / "struct_recognition.xml", names)
    covered = {d for p in prims for d in p["transistors"].values()}
    missing = sorted(names - covered)
    up = base / "upstream"
    (up / "primitives.json").write_text(json.dumps({
        "design": a.design, "provenance": "LOADBench struct_recognition.xml (real, converted to the upstream "
                                          "primitives format by scripts/make_loadbench_package.py)",
        "netlist": f"circuits/{a.design}/source/{a.design}.spice", "subckt": a.design,
        "ports": ["in1", "in2", "out", "sourceNmos", "sourcePmos"], "instances": prims,
        "not_in_any_structure": missing}, indent=1) + "\n")
    (up / "hierarchy.json").write_text(json.dumps({
        "design": a.design, "provenance": "LOADBench struct_recognition.xml / partitioning.xml (real)",
        "root": {"level": 2, "kind": "differential-input-single-output-amplifier", "subckt": a.design},
        "levels": [{"level": 1, "top": [{"instance": p["instance"], "kind": p["category"], "subckt": p["subckt"],
                                         "nodes": sorted(set(p["ports"].values()))} for p in prims]}]},
        indent=1) + "\n")
    nets = sorted({d[k] for d in devices if d["model"] != "ideal_capacitor" for k in "dgsb"} | {"ibias"})
    (up / "name_map.yaml").write_text(yaml.safe_dump({
        "upstream_design": a.design, "target_design": a.design,
        "devices": {n: n for n in sorted(names)}, "nets": {n: n for n in nets},
        "manual": ["Identity map: the LOADBench structure recognition was made on this same netlist."]},
        sort_keys=False))
    (up / "equations.predicted.json").write_text(json.dumps(predicted_equations(a.design), indent=1) + "\n")

    files = [up / "primitives.json", up / "hierarchy.json", up / "name_map.yaml", up / "equations.predicted.json"]
    (base / "SOURCE.md").write_text(f"""# {a.design}: provenance

Generated {dt.date.today().isoformat()} by `scripts/make_loadbench_package.py {a.folder} {a.design} {'--select' if a.select else f'--row {idx}'}`.

| Item | Origin | Status |
|---|---|---|
| Topology, device names, ad/as/pd/ps formulas | LOADBench `{opamp}` `example_run/CombinedTestBench.cir` | copied |
| Sizes W, L, Cc | `FinalPOFfull.csv` row {idx} (0-based); tied sizes resolved through `params.cir` aliases | copied |
| Bias | ideal 10 uA sink, moved from LOADBench's testbench into the DUT as `Ibias` (bias source) | **adapted** |
| Miller capacitor | ideal capacitor `Capacitor2` (LOADBench has no PDK capacitor) | copied, **no layout device** |
| Reference metrics | `loadbench_reference.json` (LOADBench's simulation, reduced sky130 library) | copied |
| Testbenches | `diso_amp_AC/OP/NOISE`: this flow's convention, DC unity feedback through a 1 GH choke | **new** |
| Specs | `config.yaml`: **ASSUMPTION**, see `spec_notes` | **new** |
| Hierarchy / primitives | LOADBench `struct_recognition.xml` | converted |
| Symbolic equations | `upstream/equations.predicted.json`: textbook two-stage Miller model | **PREDICTED** |
| Operating point, variation ranges | not provided | S1 generates the OP; ranges pending |

Selection: {how}.
LOADBench: Zenodo 10.5281/zenodo.21759759, licence CC BY 4.0 (attribution in THIRD_PARTY.md).
Devices not in any recognised structure: {missing or 'none'}.

SHA-256 of the generated upstream files:
""" + "".join(f"- `{f.relative_to(base)}` {sha(f)}\n" for f in files))
    print(f"row {idx}: {how}")
    print("wrote", base.relative_to(REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
