#!/usr/bin/env python3
"""The hand-drawn reference layout of a design, measured the way this flow measures its own (plan v2,
baseline 8 and the G2.0 validity test of PREREG.md).

  1. extract the layout cell with Magic: LVS netlist (no parasitics) and a flat PEX netlist with every
     capacitance (cthresh 0; no resistance);
  2. LVS (Netgen) of the layout against the flow's layout view outputs/S0/<design>/ref/<design>_layout.spice;
  3. simulate the PEX netlist in the flow's own AC/OP testbenches (the DUT replaced, off-chip test
     elements such as a bias resistor or a CM reference reconnected in the wrapper);
  4. compare: post-layout specs, the margin each spec lost, and what S2 predicted before any layout
     (G2.0 expected use, eta x margin allowed) -> outputs/S2/<design>/reference_layout.json.

usage (inside the image, repository root):
  python3 scripts/reference_layout.py <design> <gds> <cell> --ports "<layout label>=<DUT or bias port>,..."
e.g. ttsky25a_fd circuits/ttsky25a_fd/upstream_src/gds/tt_um_diff.gds Diff_Opamp --ports "Vop=Vop,..."
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from src.common.tools import PDK_ROOT, REPO as R_, TOOL_ENV, bench, rel, run_ngspice_text, write_json  # noqa: E402

MAGICRC = f"{PDK_ROOT}/sky130A/libs.tech/magic/sky130A.magicrc"


def magic(tcl: str, cwd: Path, timeout: int = 1800) -> str:
    cwd.mkdir(parents=True, exist_ok=True)
    (cwd / "run.tcl").write_text(tcl + "\nquit -noprompt\n")
    r = subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", MAGICRC, str(cwd / "run.tcl")], cwd=cwd,
                       env=TOOL_ENV, capture_output=True, text=True, timeout=timeout)
    (cwd / "magic.log").write_text(r.stdout + r.stderr)
    return r.stdout + r.stderr


def extract(gds: Path, cell: str, out: Path) -> dict:
    tcl = f"""gds read {gds}
load {cell}
select top cell
flatten {cell}_flat
load {cell}_flat
select top cell
port makeall
extract path {out}
extract do local
extract all
ext2spice lvs
ext2spice -o {out}/{cell}_lvs.spice
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist off
ext2spice -o {out}/{cell}_pex.spice
"""
    log = magic(tcl, out)
    return {"lvs": out / f"{cell}_lvs.spice", "pex": out / f"{cell}_pex.spice", "log": log[-2000:]}


def lvs(layout: Path, cell: str, ref: Path, ref_cell: str, out: Path) -> dict:
    rep = out / "lvs_report.txt"
    subprocess.run(["netgen", "-batch", "lvs", f"{layout} {cell}_flat", f"{ref} {ref_cell}",
                    f"{PDK_ROOT}/sky130A/libs.tech/netgen/sky130A_setup.tcl", str(rep)],
                   cwd=out, env=TOOL_ENV, capture_output=True, text=True, timeout=1800)
    txt = rep.read_text() if rep.exists() else ""
    return {"match": "Circuits match uniquely" in txt and "property errors" not in txt.lower(),
            "report": rel(rep), "summary": [ln for ln in txt.splitlines()
                                            if re.search(r"Number of devices|Number of nets|match|Mismatch|failed", ln)][-12:]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("design")
    ap.add_argument("gds")
    ap.add_argument("cell")
    ap.add_argument("--ports", required=True,
                    help="layout label=wrapper node, for every port of the extracted cell (wrapper nodes: INP INN "
                         "OUTP OUTN VDD VSS, or a bias port of the layout view such as RGM, VREF, IBIAS)")
    ap.add_argument("--bias", default="", help="wrapper lines for off-chip elements, ';'-separated")
    ap.add_argument("--skip-extract", action="store_true", help="reuse the extracted netlists")
    a = ap.parse_args()
    d = a.design
    out = R_ / "outputs" / "reference_layout" / d
    out.mkdir(parents=True, exist_ok=True)
    if a.skip_extract:
        ex = {"lvs": out / f"{a.cell}_lvs.spice", "pex": out / f"{a.cell}_pex.spice"}
    else:
        ex = extract((R_ / a.gds).resolve(), a.cell, out)
    ref = R_ / "outputs" / "S0" / d / "ref" / f"{d}_layout.spice"
    lv = lvs(ex["lvs"], a.cell, ref, d, out)
    pmap = dict(x.split("=") for x in a.ports.split(","))
    tb = R_ / "outputs" / "S0" / d / "tb"

    def simulate(netlist_file: Path, tag: str) -> tuple[dict, list, list]:
        net = netlist_file.read_text()
        joined = re.sub(r"\n\+", " ", net)          # continuation lines of the header
        m = re.search(rf"^\.subckt\s+{re.escape(a.cell)}_flat\s+(.*?)$", joined, re.M)
        ports_ = m.group(1).split() if m else []
        miss = [p for p in ports_ if p not in pmap]
        xdut = f"XDUT {' '.join(pmap.get(p, 'NC_' + re.sub(r'[^A-Za-z0-9_]', '_', p)) for p in ports_)} {a.cell}_flat"
        res = {}
        for kind in ("AC", "OP"):
            txt = bench(tb, kind).read_text()
            txt = re.sub(r"^\.subckt dut_amp .*?^\.ends\s*$",
                         lambda _: ".subckt dut_amp INP INN OUTN VDD VSS OUTP\n" + xdut + "\n" +
                                   "\n".join(x.strip() for x in a.bias.split(";") if x.strip()) + "\n.ends",
                         txt, count=1, flags=re.S | re.M)
            # extracted metal islands that touch only capacitors have no DC path: 1 Tohm shunts (both netlists)
            txt = re.sub(r"^(\.lib .*)$", r"\1\n.option rshunt=1e12", txt, count=1, flags=re.M)
            body = net.replace(".end\n", "")
            txt = txt.replace("\n.end\n", "\n" + body + "\n.end\n") if "\n.end\n" in txt else txt + body
            r = run_ngspice_text(txt, out / "sim" / tag / kind, kind.lower(), cache=False)
            res[kind] = r["meas"]
        return {**res.get("AC", {}), **res.get("OP", {})}, ports_, miss

    drawn, ports, missing = simulate(ex["lvs"], "drawn_devices_only")
    meas, _, _ = simulate(ex["pex"], "pex")
    ir = json.loads((R_ / "outputs" / "S0" / d / "circuit_ir.json").read_text())
    s2 = json.loads((R_ / "outputs" / "S2" / d / "s2_report.json").read_text()) if (R_ / "outputs" / "S2" / d / "s2_report.json").exists() else {}
    g20 = (s2.get("gates", {}).get("G2.0_expected_layout_use (info)") or {}).get("checks", {})
    eta = s2.get("eta")
    cmp_ = {}
    for k, mg in ir["margins"].items():
        if k not in meas or mg.get("achieved") is None:
            continue
        lost = (mg["achieved"] - meas[k]) if mg["kind"] == "min" else (meas[k] - mg["achieved"])
        b0 = drawn.get(k)
        lost_par = None if b0 is None else ((b0 - meas[k]) if mg["kind"] == "min" else (meas[k] - b0))
        cmp_[k] = {"schematic": mg["achieved"], "hand_layout_drawn_devices_only": b0, "hand_layout_pex": meas[k],
                   "lost_to_parasitics": lost_par,
                   "lost_to_parasitics_frac_of_margin": None if lost_par is None or not mg["margin"] else lost_par / mg["margin"],
                   "limit": mg["limit"],
                   "margin": mg["margin"], "lost": lost, "lost_frac_of_margin": lost / mg["margin"] if mg["margin"] else None,
                   "meets_spec": (meas[k] >= mg["limit"]) if mg["kind"] == "min" else (meas[k] <= mg["limit"]),
                   "S2_G2.0_predicted_frac": (g20.get(k) or {}).get("fraction_of_margin"), "eta": eta}
    rec = {"design": d, "gds": a.gds, "cell": a.cell, "lvs_vs_layout_view": lv, "pex_ports": ports,
           "unmapped_ports": missing, "pex_caps": len(re.findall(r"^C", ex["pex"].read_text(), re.M)),
           "drawn_devices_only": drawn, "post_layout": meas, "compare": cmp_,
           "note": "PEX with capacitance only (cthresh 0, no wire resistance); LVS against the flow's layout view"}
    write_json(out / "reference_layout.json", rec)
    print(json.dumps({"lvs_match": lv["match"], "ports": ports, "unmapped": missing, "compare": cmp_}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
