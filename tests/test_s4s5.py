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


# ------------------------------------------------------------------ Phase 1: S3 unit cells without guard rings
def test_unit_cells_are_ringless_and_named_apart():
    """Plan v4: S3's cells have no guard ring by default and carry '_ng', so the ringed cells of the reviewed S3,
    which S2's frozen library floors were read from, keep their own names (and `--guard 1` reproduces them)."""
    from src.s3 import options as O
    assert O.GUARD == 0 and set(O.TAP_RULES) == {"LU.2", "LU.3", "nwell.4"}
    ng = O.grid(8.0)[0]
    g1 = O.grid(8.0, guard=1)[0]
    assert ng["magic"]["guard"] == 0 and g1["magic"]["guard"] == 1 and ng["id"] == g1["id"]
    assert O.cell_name("pfet_01v8_W8_L1_m1", ng) == f"pfet_01v8_W8_L1_m1__{ng['id']}_ng"
    assert O.cell_name("pfet_01v8_W8_L1_m1", g1) == f"pfet_01v8_W8_L1_m1__{g1['id']}"


def test_drc_defers_only_the_named_rules(tmp_path, monkeypatch):
    """A ringless cell fails the tap rules by construction; they are counted apart (checked on the S4 block), from
    Magic's per-rule list, whose counts Magic's merged total does not match. Any other error still fails."""
    from src.common import pcell
    rep = ("top x (flattened) gds x\nDRC_TOTAL 1\n1\tAll nwells must contain metal-connected N+ taps (nwell.4)\n"
           "2\tP-diff distance to N-tap must be < 15.0um (LU.3)\n")
    (tmp_path / "drc_report.txt").write_text(rep)
    monkeypatch.setattr(pcell, "_run", lambda cmd, *a, **k: "DRC_TOTAL 1\nNEG_CONTROL_TOTAL 2\n")
    r = pcell.drc(tmp_path / "x.gds", "x", tmp_path, defer=("LU.2", "LU.3", "nwell.4"))
    assert r["errors"] == 0 and r["pass"] and r["deferred"] == {"nwell.4": 1, "LU.3": 2}
    (tmp_path / "drc_report.txt").write_text(rep + "1\tMetal1 width < 0.14um (met1.1)\n")
    r = pcell.drc(tmp_path / "x.gds", "x", tmp_path, defer=("LU.2", "LU.3", "nwell.4"))
    assert r["errors"] == 1 and not r["pass"]
    r = pcell.drc(tmp_path / "x.gds", "x", tmp_path)          # without defer: unchanged behaviour (S0)
    assert r["errors"] == 1 and "deferred" not in r


def test_s2_cells_step_and_v1_keep_the_ringed_cells():
    """S2's 'cells' step and the v1 variant build ringed cells: S2 reads its floors from them by their old names."""
    from argparse import Namespace
    from src import flow
    cells = dict(flow.steps("S2", "example_ota_5t", Namespace(workers=4, variant="v2")))["cells"]
    assert cells[cells.index("--guard") + 1] == "1"
    assert flow.VARIANT_ARGS["v1"]["S3"][-2:] == ["--guard", "1"]
