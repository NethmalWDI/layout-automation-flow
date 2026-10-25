"""Probe S3 options end to end (development aid): python3 scripts/s3_probe.py <type-substring> <option-id>..."""
import json, sys
from src.common.tools import REPO
from src.s3 import options as O
ir = json.loads((REPO / "outputs/S0/example_ota_5t/circuit_ir.json").read_text())
rules = json.loads((REPO / "outputs/S2/pdk/parasitics.json").read_text())["rules"]
types = O.device_types(ir)
tid = [k for k in types if sys.argv[1] in k][0]
opts = {o["id"]: o for o in O.grid(types[tid]["W"])}
print(tid, sorted(opts))
for oid in sys.argv[2:]:
    rec = O.build_one(types[tid], tid, opts[oid], REPO / "runs/tmp/s3_probe", rules, cross_check=True)
    rec.pop("option", None)
    g = rec.get("geometry", {})
    print(oid, "ok", rec.get("ok"), "drc", rec.get("drc"), "lvs", {k: rec.get("lvs", {}).get(k) for k in ("match", "neg_control_rejected")},
          "roles", rec.get("strap"), "area", g.get("area_um2"), "pex", {k: rec.get("pex", {}).get(k) for k in ("ports", "n_devices", "n_caps", "sum_caps_F")},
          "R", {k: v for k, v in rec.get("access_resistance_ohm", {}).items()}, "magicR", rec.get("magic_extresist", {}).get("largest_resistor_on_net_ohm"))
