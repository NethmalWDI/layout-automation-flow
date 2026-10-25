#!/usr/bin/env python3
"""S0 gate G0.7 — every device binds to a real SKY130 PDK PCell that is DRC- and LVS-clean.

Generates each device of device_map.json with the PDK's Magic PCell at its exact netlist
size and default options, then runs Magic DRC (drc(full), with negative control) and
device-level Netgen LVS (W, L, nf compared; negative control with a wrong L).
S3 later replaces the default options with requirement-driven ones and re-runs these checks.

usage (inside layout-s0s3):  python3 -m src.s0.pcell_binding outputs/S0/example_ota_5t
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from src.common import pcell
from src.common.tools import REPO, rel, write_json


def main(argv=None) -> int:
    s0 = Path((argv or sys.argv[1:])[0])
    s0 = s0 if s0.is_absolute() else REPO / s0
    dm = json.loads((s0 / "device_map.json").read_text())
    out = s0 / "pcell"
    devs = [{"cell": d["device"], "model": d["model"], "params": d["pcell"]["params"]} for d in dm["devices"]]
    gen = pcell.generate(devs, out)
    results = []
    for d in dm["devices"]:
        cell, n = d["device"], d["netlist"]
        gds = Path(gen["gds"].get(cell, out / f"{cell}.gds"))
        if not gds.exists():
            results.append({"device": cell, "pass": False, "error": "PCell generation produced no GDS", "log": gen["log"]})
            continue
        r_drc = pcell.drc(gds, cell, out / f"drc_{cell}")
        r_lvs = pcell.lvs_device(gds, cell, d["model"], n["W_um"], n["L_um"], n["nf"], n["m"], out / f"lvs_{cell}")
        img = pcell.png(gds, out / f"{cell}.png")
        results.append({"device": cell, "pcell": d["pcell"]["cell"], "params": d["pcell"]["params"],
                        "gds": rel(gds), "png": img, "drc": r_drc, "lvs": r_lvs,
                        "extracted": pcell.extracted_params(out / f"lvs_{cell}"),
                        "pass": r_drc["pass"] and r_lvs["pass"]})
        print(f"{cell}: DRC errors={r_drc['errors']} (neg ctl {r_drc['neg_control_flagged']}), "
              f"LVS match={r_lvs['match']} (neg ctl {r_lvs['neg_control_rejected']})")
    gate = {"pass": bool(results) and all(r["pass"] for r in results), "devices": results, "generation": gen}
    write_json(s0 / "pcell_binding.json", gate)
    rep_f = s0 / "s0_report.json"
    rep = json.loads(rep_f.read_text())
    rep["gates"]["G0.7_pcell_binding_drc_lvs"] = {"pass": gate["pass"], "detail": rel(s0 / "pcell_binding.json"),
                                                  "summary": {r["device"]: r["pass"] for r in results}}
    rep["all_pass"] = all(g.get("pass") in (True, None) for g in rep["gates"].values())
    write_json(rep_f, rep)
    print("G0.7", "PASS" if gate["pass"] else "FAIL")
    return 0 if gate["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
