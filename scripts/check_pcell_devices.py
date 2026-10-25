#!/usr/bin/env python3
"""DRC + device-level LVS + PNG for every cell in a pcell_manifest.json (inside layout-s0s3)."""
import json, subprocess, sys, os
from pathlib import Path
d = Path(sys.argv[1]).resolve()
man = json.loads((d / "pcell_manifest.json").read_text())
S = "/foss/designs/scripts"
res = []
for m in man:
    c, n = m["cell"], m["netlist"]
    ref = d / f"ref_{c}.spice"
    ref.write_text(f".subckt {c} D G S B\nX{c} D G S B {n['model']} L={n['L_um']:g} W={n['W_um']:g} nf={n['nf']}\n.ends\n")
    drc = subprocess.run(["bash", f"{S}/magic_drc.sh", str(d / m["gds"]), c, str(d / f"drc_{c}")], capture_output=True, text=True).stdout
    lvs = subprocess.run(["bash", f"{S}/magic_lvs.sh", str(d / m["gds"]), c, str(ref), c, str(d / f"lvs_{c}")],
                         capture_output=True, text=True, env={**os.environ, "FLATTEN": "1"}).stdout
    subprocess.run(["klayout", "-zz", "-rd", f"gds={d / m['gds']}", "-rd", f"png={d / (c + '.png')}", "-r", f"{S}/gds_to_png.py"], capture_output=True)
    tot = [l.split()[-1] for l in drc.splitlines() if l.startswith("DRC_TOTAL")]
    neg = [l.split()[-1] for l in drc.splitlines() if l.startswith("NEG_CONTROL")]
    r = {"cell": c, "drc_total": tot[0] if tot else "RUN_FAILED", "neg_control": neg[0] if neg else "?",
         "lvs": "MATCH" if "LVS_RESULT MATCH" in lvs else "FAIL"}
    res.append(r); print(r)
(d / "pcell_check.json").write_text(json.dumps(res, indent=2) + "\n")
