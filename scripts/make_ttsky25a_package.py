#!/usr/bin/env python3
"""Design package for the TTSKY25a fully differential op-amp (NethmalWDI/Fully_differential_opamp,
Apache-2.0, vendored read-only in circuits/ttsky25a_fd/upstream_src/).

What exists upstream: xschem schematics (two-stage FD op-amp: folded cascode + common source, a CMFB
per stage, Miller MIM capacitors, beta-multiplier bias with start-up), the designers' testbench
(Opamp_with_Bias_tb: 12 kohm off-chip bias resistor, Vref = 0.9 V, 0.9 V input common mode, 200x MIM
loads), the GDS of the taped-out tile, and post-layout figures in the README.
What is missing for this flow and is made here: a flat netlist, specs (ASSUMPTION), dido testbenches,
the hierarchy as primitives (PREDICTED, rule-based), the symbolic model (PREDICTED, textbook).

Run inside the EDA image from the repository root:
    source scripts/env.sh && python3 scripts/make_ttsky25a_package.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))
import benchlib  # noqa: E402
import flatten_spice  # noqa: E402
import recognize_structures as rs  # noqa: E402
from src.common import spice  # noqa: E402

DESIGN = "ttsky25a_fd"
BASE = REPO / "circuits" / DESIGN
SRC = BASE / "upstream_src" / "Opamp_Design"
WORK = REPO / "runs" / "tmp" / f"{DESIGN}_pkg"
XSCHEMRC = Path(os.environ.get("PDK_ROOT", "/foss/pdks")) / "sky130A/libs.tech/xschem/xschemrc"

# from the designers' testbench Opamp_with_Bias_tb.sch
RGM_OHM = 12e3          # R1 from Rgm to Vss (off-chip in the TT tile)
VREF_V = 0.9            # V2 on Vref (CM reference of both CMFB loops)
MIM_LOAD_MF = 200       # C3/C4: cap_mim_m3_1 W=1 L=1 MF=200 on each output
CL_F = 200 * 2e-15 * (1 + 0.15) ** 2   # = 529 fF, the tt model value of those loads, as ideal capacitors

CONDITIONS = {"VDD_V": 1.8, "VCM_V": 0.9, "CL_F": f"{CL_F * 1e15:.0f}f", "temp": 27, "corner": "tt"}
# README, post-layout simulation (reported, not re-run here)
README_POSTLAYOUT = {"gain_db": 100.0, "gbw_mhz": 2.3, "pm_deg_min": 52.0, "power_uw": 500.0, "cmrr_db_1k": 91.0}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def xschem_netlist(sch: str, out_dir: Path) -> Path:
    """Netlist one schematic of a private copy whose absolute symbol paths point at the copy."""
    cp = WORK / "Opamp_Design"
    if cp.exists():
        shutil.rmtree(cp)
    shutil.copytree(SRC, cp)
    for f in cp.rglob("*.sch"):
        t = f.read_text()
        t2 = re.sub(r"/foss/designs/FYP/Sky130_[A-Za-z]+/Opamp_Design/", f"{cp}/", t)
        if t2 != t:
            f.write_text(t2)
    out_dir.mkdir(parents=True, exist_ok=True)
    sch_path = next(cp.rglob(sch))
    r = subprocess.run(["xschem", "-n", "-s", "-q", "--no_x", "-x", "-o", str(out_dir), "--rcfile", str(XSCHEMRC),
                        str(sch_path)], cwd=sch_path.parent, capture_output=True, text=True, timeout=120)
    net = out_dir / (sch_path.stem + ".spice")
    if not net.exists():
        raise SystemExit(f"xschem produced no netlist for {sch}: {r.stdout[-500:]} {r.stderr[-500:]}")
    return net


def dut_netlist() -> tuple[str, dict]:
    net = xschem_netlist("Opamp_with_bias.sch", WORK / "xschem")
    flat = WORK / "flat.spice"
    stats = flatten_spice.flatten(net, "Opamp_with_bias", flat, DESIGN)
    lines = flat.read_text().splitlines()
    out = []
    for ln in lines:
        if ln.startswith(f".subckt {DESIGN}"):
            # Rgm and Vref become internal nodes driven by elements inside the DUT that the layout view removes
            ports = [p for p in ln.split()[2:] if p not in ("Rgm", "Vref")]
            out.append(f".subckt {DESIGN} " + " ".join(ports))
            continue
        if ln.startswith("*.ipin Rgm") or ln.startswith("*.ipin Vref"):
            continue
        if ln.startswith(".ends"):
            out.append(f"* off-chip bias resistor and CM reference from the designers' testbench (bias_sources)")
            out.append(f"Rgm_ext Rgm Vss {RGM_OHM:g}")
            out.append(f"Vref_ext Vref Vss {VREF_V:g}")
        out.append(ln)
    text = "\n".join(out) + "\n"
    return text, {**stats, "xschem_netlist": str(net.relative_to(REPO))}


def reference_run() -> dict:
    """The designers' own testbench, netlisted by xschem, with measurements added (op + ac)."""
    net = xschem_netlist("Opamp_with_Bias_tb.sch", WORK / "xschem_tb")
    txt = net.read_text()
    ctrl = """.control
save all
op
let isup = abs(i(Vmeas))
let power_uw = isup * 1.8 * 1e6
echo MEAS power_uw $&power_uw
ac dec 40 1 1G
let hsig = (v(Vop) - v(Vom)) / (v(Vp) - v(Vm))
let hdb = db(hsig)
let hph = 180/pi * cph(hsig)
meas ac gain_db find hdb at=1
meas ac gbw_hz when hdb=0
meas ac ph_dc find hph at=1
meas ac ph_ugb find hph when hdb=0
let gbw_mhz = gbw_hz / 1e6
let pm_deg = 180 + (ph_ugb - ph_dc)
echo MEAS gain_db $&gain_db
echo MEAS gbw_mhz $&gbw_mhz
echo MEAS pm_deg $&pm_deg
quit 0
.endc
"""
    txt2, n = re.subn(r"^\.control.*?^\.endc", lambda _: ctrl, txt, count=1, flags=re.S | re.M)
    if n != 1:
        raise SystemExit("designers' testbench: no .control block")
    deck = WORK / "ref_tb.spice"
    deck.write_text(txt2)
    r = subprocess.run(["ngspice", "-b", str(deck)], cwd=WORK, capture_output=True, text=True, timeout=600)
    (WORK / "ref_tb.log").write_text(r.stdout + r.stderr)
    meas = {m.group(1): float(m.group(2)) for m in re.finditer(r"^MEAS (\w+) (\S+)", r.stdout, re.M)}
    if len(meas) < 4:
        raise SystemExit(f"reference run incomplete: {meas}; see {WORK / 'ref_tb.log'}")
    return meas


def predicted_equations() -> dict:
    """Textbook two-stage fully differential op-amp with Miller compensation, differential half circuit
    (Johns & Martin 2nd ed., ch. 6 and 7; Razavi 2nd ed., ch. 10). PREDICTED, not from upstream.
    Half circuit of the Vom1 -> Vop path: input M6 (Vp), first-stage output Vom1 (cascodes M12, M8 over
    M14, M9), second stage PMOS M9 of x2 with NMOS load M2 of x2 and the resistive CM sense (20 poly
    resistors of x2_x1 from Vop to the CM node, an AC ground in differential mode), Miller C2."""
    r_pack = " + ".join(f"R_XX2_X1_R{i}" for i in range(1, 21))
    return {
        "design": DESIGN, "mode": "differential", "provenance": "PREDICTED",
        "assumes": "purely differential drive; CMFB loops inactive in differential mode; first-stage cascode "
                   "output resistances by gm*ro*ro; folding-node and CMFB-sense poles neglected; two poles, one RHP zero",
        "source": "textbook two-stage FD op-amp (Johns & Martin, Analog IC Design, 2nd ed., ch. 6-7); written for this "
                  "flow as a stand-in for the upstream symbolic stage",
        "naming": "level-0 symbols: C1..C5 gate-bulk, gate-source, gate-drain, drain-bulk, source-bulk; G1 gm; R1 1/gds; "
                  "C_<passive>, R_<passive> the values of netlist passives",
        "performance": {
            "circuit": DESIGN, "input": "vd", "output": "v(Vop) - v(Vom)", "load": {"CL": "each output to GND"},
            "terms": {
                "gm1": "G1_XX1_M6",
                "rdn": "G1_XX1_M8*R1_XX1_M8*R1_XX1_M9",
                "rup": "G1_XX1_M12*R1_XX1_M12*(R1_XX1_M6*R1_XX1_M14/(R1_XX1_M6 + R1_XX1_M14))",
                "R1o": "rdn*rup/(rdn + rup)",
                "gm2": "G1_XX2_M9",
                "Rpk": r_pack,
                "R2o": "1/(1/R1_XX2_M9 + 1/R1_XX2_M2 + 1/Rpk)",
                "Cc": "C_XC2 + C3_XX2_M9",
                "C1n": "C2_XX2_M9 + C1_XX2_M9 + C4_XX1_M12 + C4_XX1_M8 + C3_XX1_M12 + C3_XX1_M8",
                "C2n": "CL + C4_XX2_M9 + C4_XX2_M2 + C3_XX2_M2",
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


def hierarchy_from_names(nl: spice.Netlist) -> dict:
    """The schematic hierarchy survives in the flat names: X<INST>_... belongs to sub-block <inst>."""
    groups: dict = {}
    for e in [m.name for m in nl.mosfets] + [p.name for p in nl.passives]:
        m = re.match(r"^X(X\d+)_(X\d+_)?", e)
        key = "top" if not m else (m.group(1).lower() + ("/" + m.group(2).rstrip("_").lower() if m.group(2) else ""))
        groups.setdefault(key, []).append(e)
    names = {"top": "Opamp_with_bias (bias: beta multiplier, start-up, current outputs; Miller capacitors)",
             "x1": "Diff_opamp (folded-cascode first stage + its CMFB + bias diodes)",
             "x2": "Common_source_stage (second stage + resistive-sense CMFB)",
             "x2/x1": "res_pack (CM sense resistors, OUTP side)", "x2/x2": "res_pack (CM sense resistors, OUTN side)"}
    return {"design": DESIGN, "provenance": "upstream xschem hierarchy (real), read from the flat instance names",
            "root": {"level": 2, "kind": "differential-input-differential-output-amplifier", "subckt": DESIGN},
            "levels": [{"level": 1, "top": [{"instance": k, "kind": names.get(k, k), "elements": sorted(v)}
                                            for k, v in sorted(groups.items())]}]}


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    for sub in ("source", "testbenches", "upstream"):
        (BASE / sub).mkdir(parents=True, exist_ok=True)
    dut, stats = dut_netlist()
    (BASE / "source" / f"{DESIGN}.spice").write_text(dut + ".end\n")
    nl = spice.parse(BASE / "source" / f"{DESIGN}.spice")
    # wrapper port order of the DUT: map to INP INN OUTN VDD VSS OUTP
    std = {"Vp": "INP", "Vm": "INN", "Vom": "OUTN", "Vdd": "VDD", "Vss": "VSS", "Vop": "OUTP"}
    xdut = "XDUT " + " ".join(std[p] for p in nl.ports) + f" {DESIGN}"
    dut_sub = re.search(rf"^\.subckt {DESIGN}.*?^\.ends {DESIGN}\n", dut, re.S | re.M).group(0)
    for kind in ("AC", "OP", "NOISE"):
        (BASE / "testbenches" / f"dido_amp_{kind}.spice").write_text(
            benchlib.bench(DESIGN, kind, dut_sub, xdut, differential_output=True))

    ref = reference_run()
    (BASE / "source" / "reference.json").write_text(json.dumps({
        "source": "designers' testbench Opamp_with_Bias_tb.sch (xschem netlist), re-run by this flow with "
                  "measurements added; MIM loads (200 x 1x1 um), open loop, tt, 27 C",
        "simulator_setup": "same PDK and simulator; MIM loads instead of ideal 529 fF, open-loop bench instead "
                           "of DC-feedback chokes",
        "metrics": ref,
        "readme_post_layout_reported": README_POSTLAYOUT}, indent=1) + "\n")

    cfg = {
        "name": DESIGN,
        "description": "Two-stage fully differential op-amp (folded cascode + common source, CMFB per stage, Miller "
                       "MIM capacitors, beta-multiplier bias), TTSKY25a tile tt_um_diff.",
        "interface": {"input": "differential", "output": "differential", "kind": "amp", "dut_symbol": "dut_amp",
                      "ports": {"INP": "Vp", "INN": "Vm", "OUTP": "Vop", "OUTN": "Vom", "VDD": "Vdd", "VSS": "Vss"}},
        "analyses": ["AC", "OP", "NOISE"],
        "conditions": CONDITIONS,
        "specs": {"pm_deg": {"min": 60}},
        "spec_notes": {"ASSUMPTION": "the repository gives post-layout results, not specs (README/paper: ~100 dB, 2.3 MHz, "
                                     "52 deg, ~500 uW), and the designer chose the schematic's own performance as the "
                                     "reference (2026-10-26). Same rule as loadbench_miller: gain_db, gbw_mhz and power_uw "
                                     "from this flow's own simulation of the schematic (package key specs_from_achieved: "
                                     "gain -1 dB, GBW x 0.9, power x 1.1); PM >= 60 deg."},
    }
    (BASE / "source" / "config.yaml").write_text("# Generated by scripts/make_ttsky25a_package.py. Specs: ASSUMPTION.\n" +
                                                 yaml.safe_dump(cfg, sort_keys=False))

    rails = {"Vdd", "Vss"}
    prim = rs.to_primitives(rs.recognize(nl, rails), nl, DESIGN)
    up = BASE / "upstream"
    (up / "primitives.json").write_text(json.dumps(prim, indent=1) + "\n")
    (up / "hierarchy.json").write_text(json.dumps(hierarchy_from_names(nl), indent=1) + "\n")
    nets = sorted(nl.nets())
    (up / "name_map.yaml").write_text(yaml.safe_dump({
        "upstream_design": DESIGN, "target_design": DESIGN,
        "devices": {m.name: m.name for m in nl.mosfets}, "nets": {n: n for n in nets},
        "manual": ["Identity map: the predicted primitives were recognised on this same flat netlist."]}, sort_keys=False))
    (up / "equations.predicted.json").write_text(json.dumps(predicted_equations(), indent=1) + "\n")

    files = [BASE / "source" / f"{DESIGN}.spice", BASE / "source" / "config.yaml", BASE / "source" / "reference.json"] + \
            sorted((BASE / "testbenches").glob("*.spice")) + sorted(up.glob("*"))
    commit = (BASE / "upstream_src" / "UPSTREAM_COMMIT.txt").read_text().strip()
    (BASE / "SOURCE.md").write_text(f"""# {DESIGN}: provenance

Generated {dt.date.today().isoformat()} by `scripts/make_ttsky25a_package.py` from the vendored upstream copy
`upstream_src/` (NethmalWDI/Fully_differential_opamp, commit {commit}, Apache-2.0).

| Item | Origin | Status |
|---|---|---|
| Circuit | `Opamp_with_bias.sch` netlisted by xschem, flattened by `scripts/flatten_spice.py` ({stats['devices']} devices) | copied, flattened |
| Off-chip 12 kohm bias resistor, Vref = 0.9 V | the designers' testbench, kept inside the DUT as `Rgm_ext`, `Vref_ext` (bias_sources) | **adapted** |
| Load | 529 fF per output: the tt value of the testbench's 200 x (1 um x 1 um) MIM loads, as ideal capacitors | adapted |
| Reference metrics | `source/reference.json`: the designers' testbench re-run here; README post-layout figures | re-run / reported |
| Paper post-layout figures | `source/paper_post_layout.json`: ICM 2026 paper text supplied by the designer (hand-entered, not generated by this script) | reported |
| Testbenches | `dido_amp_AC/OP/NOISE` (scripts/benchlib.py), DC unity feedback through chokes | **new** |
| Specs | `config.yaml`: **ASSUMPTION** (README figures are results, not specs) | **new** |
| Hierarchy | schematic sub-blocks (Diff_opamp, Common_source_stage, res_pack), from the flat names | real |
| Primitives | `upstream/primitives.json`: rule-based recognition (scripts/recognize_structures.py) | **PREDICTED** |
| Symbolic equations | `upstream/equations.predicted.json`: textbook two-stage FD model | **PREDICTED** |
| Layout reference | `upstream_src/gds/tt_um_diff.gds` (taped-out tile) | copied |

SHA-256 of the generated files:
""" + "".join(f"- `{f.relative_to(BASE)}` {sha(f)}\n" for f in files))
    print("reference (designers' bench):", ref)
    print("devices:", stats)
    print("wrote", BASE.relative_to(REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
