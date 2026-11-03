"""Tests for plan v4: S3 without guard rings and the new stages S4-S7 (docs/plan_v4_S4_S7.md)."""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import freeze_outputs as F  # noqa: E402


# ------------------------------------------------------------------ Phase 0: the reviewed S0-S2 state is frozen
def test_s0_s2_outputs_unchanged():
    """Work on S3-S7 must not change what S0-S2 produced at tag s0s3-reviewed (plan v4, section 6). A deliberate
    change re-runs scripts/freeze_outputs.py and is logged."""
    m = json.loads(F.MANIFEST.read_text())
    assert len(m["sha256"]) >= 60 and set(m["designs"]) == {"example_ota_5t", "loadbench_miller"}
    bad = F.changed(m)
    assert not bad, f"{len(bad)} frozen S0-S2 files changed, e.g. {bad[:5]}"


def test_freeze_covers_what_later_stages_read():
    """The manifest holds the files S3-S7 read: the IR, the budgets, constraints and hierarchy, the LVS reference
    netlist and the testbenches, for both designs."""
    keys = set(json.loads(F.MANIFEST.read_text())["sha256"])
    for d in ("example_ota_5t", "loadbench_miller"):
        for need in (f"outputs/S0/{d}/circuit_ir.json", f"outputs/S2/{d}/budgets.json",
                     f"outputs/S2/{d}/constraints.json", f"outputs/S2/{d}/hierarchy.json",
                     f"outputs/S0/{d}/ref/{d}_layout.spice", f"outputs/S1/{d}/sensitivity.json"):
            assert need in keys, need
    assert "outputs/S2/pdk/parasitics.json" in keys
