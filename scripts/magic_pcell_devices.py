#!/usr/bin/env python3
"""Generate every MOSFET of a sized netlist with the SKY130 PDK's own PCells (open_pdks Magic
device generator, sky130A.tcl: magic::gencell sky130::<model> ...), one cell per device.

usage (inside layout-s0s3):
  python3 scripts/magic_pcell_devices.py <sized.spice> <out_dir> [--guard 1]
Writes <out_dir>/<dev>.gds/.mag, gen.tcl and pcell_manifest.json.
Parameters passed to the PCell are exactly the netlist values: w = W/nf (per finger, the PCell
convention), l = L, nf, m.  Nothing is legalised.
"""
import argparse, json, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from make_align_input import parse

ap = argparse.ArgumentParser(); ap.add_argument("sized_spice"); ap.add_argument("out_dir")
ap.add_argument("--guard", default="1")
a = ap.parse_args()
_, ports, devs, _ = parse(Path(a.sized_spice))
out = Path(a.out_dir).resolve(); out.mkdir(parents=True, exist_ok=True)
tcl = ["drc off", "snap internal"]
man = []
for d in devs:
    cell = d["ref_name"].lstrip("Xx")
    w_f = d["W_um"] / d["nf"]
    params = f"w {w_f:g} l {d['L_um']:g} nf {d['nf']} m {d['m']} guard {a.guard}"
    tcl += [f"cellname delete {cell}", f"load {cell} -silent", "box 0 0 0 0",
            f"magic::gencell sky130::{d['model']} {cell}_pc {params}",
            "select top cell", "expand", f"save {cell}",
            f"gds write {cell}"]
    man.append({"device": d["ref_name"], "cell": cell, "pcell": f"sky130::{d['model']}",
                "pcell_params": {"w_per_finger_um": w_f, "l_um": d["L_um"], "nf": d["nf"], "m": d["m"], "guard": int(a.guard)},
                "netlist": {k: d[k] for k in ("W_um", "L_um", "nf", "m", "d", "g", "s", "b", "model")},
                "gds": f"{cell}.gds"})
tcl.append("quit -noprompt")
(out / "gen.tcl").write_text("\n".join(tcl) + "\n")
rc = os.environ.get("PDK_ROOT", "/foss/pdks") + "/sky130A/libs.tech/magic/sky130A.magicrc"
r = subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", rc, str(out / "gen.tcl")],
                   cwd=out, capture_output=True, text=True, timeout=600)
(out / "gen_magic.log").write_text(r.stdout + r.stderr)
(out / "pcell_manifest.json").write_text(json.dumps(man, indent=2) + "\n")
for m in man:
    print(m["cell"], m["pcell"], m["pcell_params"], "gds_exists=", (out / m["gds"]).exists())
print("magic rc", r.returncode)
