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
from src.s0.pvt import with_conditions  # noqa: E402

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


def extract_rc(gds: Path, cell: str, out: Path, tol: float = 100.0) -> Path:
    """R+C PEX of the flattened cell: Magic's extresist (wire and via resistance; a resistor is kept when it
    exceeds tol x the driving device's resistance, so a larger tol gives a smaller network) on top of every
    capacitance. Separate from extract() so that the C-only results stay as they are. At tol = 10 the iadc
    OTA gave 324 k resistors and an AC run that needed more than 4 GB."""
    tcl = f"""gds read {gds}
load {cell}
select top cell
flatten {cell}_flat
load {cell}_flat
select top cell
port makeall
extract do local
extract all
ext2sim labels on
ext2sim
extresist tolerance {tol:g}
extresist all
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist on
ext2spice -o {out}/{cell}_pexrc.spice
"""
    # every file in rc_run/ (Magic's working directory): an extraction path or ext2spice -p would make
    # ext2spice read the C-only .ext of extract() instead of this one and ignore the .res.ext
    magic(tcl, out / "rc_run")
    return out / f"{cell}_pexrc.spice"


def shorted_ports(netlist_file: Path) -> dict:
    """{port: set of ports} from Magic's 'Ports "a" and "b" are electrically shorted' warnings in the log of
    the extraction that wrote netlist_file (rc_run/magic.log for the R+C netlist, magic.log otherwise)."""
    log = netlist_file.parent / ("rc_run" if netlist_file.name.endswith("_pexrc.spice") else ".") / "magic.log"
    groups: dict = {}
    if log.exists():
        for a_, b_ in re.findall(r'Ports "([^"]+)" and "([^"]+)" are electrically shorted', log.read_text()):
            g = groups.get(a_, {a_}) | groups.get(b_, {b_})
            for x in g:
                groups[x] = g
    return groups


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
    ap.add_argument("--corner", default=None, help="process corner of every run (default: the bench's)")
    ap.add_argument("--temp", type=float, default=None, help="temperature in C (default: the bench's)")
    ap.add_argument("--mim-load", default=None, metavar="W,L,MF",
                    help="replace each ideal load capacitor by a MIM capacitor W x L um, MF units (the designers' "
                         "load, simulated at the run's corner)")
    ap.add_argument("--tag", default=None, help="name of this condition set: reference_layout_<tag>.json, sim/<tag>/")
    ap.add_argument("--rc", action="store_true", help="also an R+C extraction (Magic extresist) and its simulation")
    ap.add_argument("--rc-tol", type=float, default=100.0, help="extresist tolerance (larger: fewer resistors)")
    ap.add_argument("--map-shorted", action="store_true",
                    help="tie every port Magic reports as electrically shorted to a mapped port to that port's node")
    a = ap.parse_args()
    d = a.design
    out = R_ / "outputs" / "reference_layout" / d
    out.mkdir(parents=True, exist_ok=True)
    sim_root = out / "sim" / a.tag if a.tag else out / "sim"

    def conditioned(txt: str) -> str:
        """The flow's bench at the requested corner / temperature / load (unchanged when none is given)."""
        if a.corner or a.temp is not None:
            txt = with_conditions(txt, a.corner or re.search(r"sky130\.lib\.spice\s+(\w+)", txt).group(1), None, a.temp)
        if a.mim_load:
            w, l_, mf = a.mim_load.split(",")
            # MF multiplies the MIM units (the instance multiplier M; the PDK subckt's own mf only scales mismatch)
            txt, n = re.subn(r"^C(load\w*)\s+(\S+)\s+(\S+)\s+\S+\s*$",
                             lambda m: f"XC{m.group(1)} {m.group(2)} {m.group(3)} sky130_fd_pr__cap_mim_m3_1 "
                                       f"W={w} L={l_} MF={mf} M={mf}", txt, flags=re.M)
            if not n:
                raise SystemExit("--mim-load: no 'Cload...' line in the bench to replace")
        # extracted metal islands that touch only capacitors have no DC path: 1 Tohm shunts (every netlist,
        # the schematic too, so that the three runs differ only in the DUT)
        return re.sub(r"^(\.lib .*)$", r"\1\n.option rshunt=1e12", txt, count=1, flags=re.M)
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

        shorted = shorted_ports(netlist_file) if a.map_shorted else {}

        def node(p):
            # Magic names a second, separately drawn piece of a labelled net <name>_uqN (e.g. VDD_uq3, a supply
            # strap joined only at the next level up): it is the same circuit node
            q = pmap.get(p) or pmap.get(re.sub(r"_uq\d+$", "", p))
            if not q and p in shorted:   # --map-shorted: a port Magic reports as shorted to a mapped one
                q = next((pmap.get(x) or pmap.get(re.sub(r"_uq\d+$", "", x)) for x in shorted[p]
                          if pmap.get(x) or pmap.get(re.sub(r"_uq\d+$", "", x))), None)
            return q or "NC_" + re.sub(r"[^A-Za-z0-9_]", "_", p)
        miss = [p for p in ports_ if node(p).startswith("NC_")]
        xdut = f"XDUT {' '.join(node(p) for p in ports_)} {a.cell}_flat"
        res = {}
        for kind in ("AC", "OP"):
            txt = conditioned(bench(tb, kind).read_text())
            txt = re.sub(r"^\.subckt dut_amp .*?^\.ends\s*$",
                         lambda _: ".subckt dut_amp INP INN OUTN VDD VSS OUTP\n" + xdut + "\n" +
                                   "\n".join(x.strip() for x in a.bias.split(";") if x.strip()) + "\n.ends",
                         txt, count=1, flags=re.S | re.M)
            body = net.replace(".end\n", "")
            txt = txt.replace("\n.end\n", "\n" + body + "\n.end\n") if "\n.end\n" in txt else txt + body
            if tag == "pex_rc":   # hundreds of thousands of resistors: KLU, the sparse solver for large circuits,
                # and only the output vectors kept (save all x 361 frequencies of 300 k nodes is gigabytes)
                txt = re.sub(r"^(\.lib .*)$", r"\1\n.options klu", txt, count=1, flags=re.M)
                if kind == "AC":
                    txt = re.sub(r"^(\s*)save all\s*$", r"\1save v(OUTP) v(OUTN)", txt, flags=re.M)
                    txt = re.sub(r"^\s*write\s*$", "", txt, flags=re.M)
            r = run_ngspice_text(txt, sim_root / tag / kind, kind.lower(), cache=False,
                                 timeout=3600 if tag == "pex_rc" else 600)
            res[kind] = r["meas"]
            runs[f"{tag}.{kind}"] = {"rc": r["rc"], "numerical_warnings": r.get("numerical_warnings", [])}
        return {**res.get("AC", {}), **res.get("OP", {})}, ports_, miss

    def schematic() -> dict:
        """The flow's own DUT (S0 layout view's source netlist, as in the bench) at the same conditions."""
        res = {}
        for kind in ("AC", "OP"):
            r = run_ngspice_text(conditioned(bench(tb, kind).read_text()), sim_root / "schematic" / kind,
                                 kind.lower(), cache=False)
            res[kind] = r["meas"]
            runs[f"schematic.{kind}"] = {"rc": r["rc"], "numerical_warnings": r.get("numerical_warnings", [])}
        return {**res.get("AC", {}), **res.get("OP", {})}

    runs: dict = {}
    sch = schematic()
    drawn, ports, missing = simulate(ex["lvs"], "drawn_devices_only")
    meas, _, _ = simulate(ex["pex"], "pex")
    meas_rc = None
    if a.rc:
        frc = out / f"{a.cell}_pexrc.spice"
        if not (a.skip_extract and frc.exists()):
            frc = extract_rc((R_ / a.gds).resolve(), a.cell, out, a.rc_tol)
        meas_rc = simulate(frc, "pex_rc")[0] if frc.exists() else None
    ir = json.loads((R_ / "outputs" / "S0" / d / "circuit_ir.json").read_text())
    s2 = json.loads((R_ / "outputs" / "S2" / d / "s2_report.json").read_text()) if (R_ / "outputs" / "S2" / d / "s2_report.json").exists() else {}
    g20 = (s2.get("gates", {}).get("G2.0_expected_layout_use (info)") or {}).get("checks", {})
    eta = s2.get("eta")
    cmp_ = {}
    nominal = not (a.corner or a.temp is not None or a.mim_load)
    for k, mg in ir["margins"].items():
        if not nominal:   # the S0 margins are at the bench's own conditions: no comparison off them (review B, item 4)
            break
        if meas.get(k) is None or mg.get("achieved") is None:
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
    reported = R_ / "circuits" / d / "source" / "paper_post_layout.json"
    rec = {"design": d, "gds": a.gds, "cell": a.cell, "lvs_vs_layout_view": lv, "pex_ports": ports,
           "conditions": {"corner": a.corner, "temp": a.temp, "mim_load": a.mim_load, "bias": a.bias,
                          "note": "None = the flow bench's own value"},
           "unmapped_ports": missing, "pex_caps": len(re.findall(r"^C", ex["pex"].read_text(), re.M)),
           "schematic_same_conditions": sch, "drawn_devices_only": drawn, "post_layout": meas,
           "lost_to_parasitics": {k: (drawn[k] - meas[k]) for k in ("gain_db", "gbw_mhz", "pm_deg")
                                  if drawn.get(k) is not None and meas.get(k) is not None},
           "post_layout_rc": meas_rc, "rc_tolerance": a.rc_tol if a.rc else None, "map_shorted": a.map_shorted,
           "lost_to_parasitics_rc": None if not meas_rc else
           {k: (drawn[k] - meas_rc[k]) for k in ("gain_db", "gbw_mhz", "pm_deg")
            if drawn.get(k) is not None and meas_rc.get(k) is not None},
           "runs": runs, "compare": cmp_ if nominal else None,
           "reported_post_layout": json.loads(reported.read_text()) if reported.exists() else None,
           "note": "PEX with capacitance only (cthresh 0, no wire resistance); LVS against the flow's layout view. "
                   "'compare' (against the flow's nominal S0 margins) only for runs at the bench's own conditions; "
                   "'lost_to_parasitics' = drawn devices only - PEX, at this run's conditions"}
    write_json(out / (f"reference_layout_{a.tag}.json" if a.tag else "reference_layout.json"), rec)
    print(json.dumps({"lvs_match": lv["match"], "unmapped": missing, "runs": runs, "schematic": sch,
                      "drawn": drawn, "pex": meas, "compare": cmp_ if nominal else "n/a (conditions differ)"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
