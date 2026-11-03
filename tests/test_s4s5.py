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


# ------------------------------------------------------------------ Phase 2: S4 blocks
def _ir_groups(d):
    ir = json.loads((REPO / f"outputs/S0/{d}/circuit_ir.json").read_text())
    g = json.loads((REPO / f"outputs/S1/{d}/s1_report.json").read_text())["gates"]["G1.4_matching_groups"]["groups"]
    return ir, g


def test_block_plan_one_type_and_body_per_block():
    """Matching groups first, then S0's blocks; one device type with one body net per block; every device once.
    LOADBench: P5 goes to the bias bank (a matching group), so cs_stage keeps only N3."""
    from src.s4.run import plan_blocks
    ir, g = _ir_groups("example_ota_5t")
    bl = {b["name"]: b for b in plan_blocks(ir, g)}
    assert {k: sorted(v["devices"]) for k, v in bl.items()} == {
        "pmos_current_mirror_load": ["XM3", "XM4"], "nmos_differential_pair": ["XM1", "XM2"],
        "nmos_current_mirror_bias": ["XM5"]}
    ir, g = _ir_groups("loadbench_miller")
    bl = plan_blocks(ir, g)
    names = [x for b in bl for x in b["devices"]]
    assert sorted(names) == sorted(d["name"] for d in ir["devices"]) and len(names) == len(set(names))
    by = {b["name"]: b for b in bl}
    assert "XNormalTransistorPmos5" in by["pmos_bias_bank"]["devices"]
    assert by["cs_stage"]["devices"] == ["XNormalTransistorNmos3"]
    assert by["input_pair"]["body"] == "FirstStageYsourceTransconductance"     # its own n-well
    devs = {d["name"]: d for d in ir["devices"]}
    for b in bl:
        assert len({devs[x]["type"] for x in b["devices"]}) == 1 and len({devs[x]["terminals"]["b"] for x in b["devices"]}) == 1


def test_symmetry_measures_tell_ab_abba_abab_apart():
    from src.s4.run import symmetry
    cell = {"cell": "u"}
    def geo(seq):
        us, x = [], 0.0
        for dev, mir in seq:
            us.append({"device": dev, "mirror": mir, "rec": cell, "x": x, "w": 1.0})
            x += 1.5
        return {"units": us, "row": [0.0, 0.0, x - 0.5, 1.0]}
    ab = symmetry(geo([("A", False), ("B", True)]), ["A", "B"])
    abba = symmetry(geo([("A", False), ("B", False), ("B", True), ("A", True)]), ["A", "B"])
    abab = symmetry(geo([("A", False), ("B", False), ("A", False), ("B", False)]), ["A", "B"])
    assert ab["mirror_image"] and ab["error_um"] == 0 and ab["centroid_offset_um"] == 1.5
    assert abba["mirror_image"] and abba["centroid_offset_um"] == 0
    assert not abab["mirror_image"] and abab["centroid_offset_um"] == 1.5


def test_stub_plan_sends_single_finger_strips_down_and_keeps_stubs_apart():
    import pytest
    from src.s4 import block as B
    pins = {"D": {"layer": "metal1", "rect": [0.2, 0.3, 0.4, 8.0]}, "S": {"layer": "metal1", "rect": [1.5, 0.3, 1.7, 8.0]},
            "G": {"layer": "metal1", "rect": [0.5, 8.5, 1.4, 8.7]}}
    p = B.stub_plan(pins, 1.9, 8.8)
    assert p["D"]["side"] == p["S"]["side"] == "bottom" and p["G"]["side"] == "top"
    tight = {"D": {"layer": "metal1", "rect": [0.1, 0.3, 0.2, 8.0]}, "S": {"layer": "metal1", "rect": [0.35, 0.3, 0.45, 8.0]},
             "G": {"layer": "metal1", "rect": [0.2, 8.5, 0.4, 8.7]}}
    with pytest.raises(RuntimeError):
        B.stub_plan(tight, 0.6, 8.8)


def test_5t_blocks_signed_off_with_their_controls():
    """Every 5T block variant passes DRC (nothing deferred; the control sliver caught) and LVS (the wrong-L
    reference rejected); the pair has a common-centroid mirror-image variant (ABBA)."""
    import pytest
    rep_f = REPO / "outputs/S4/example_ota_5t/s4_report.json"
    if not rep_f.exists():
        pytest.skip("needs the 5T's S4 outputs")
    rep = json.loads(rep_f.read_text())
    assert rep["all_pass"] and all(g["pass"] in (True, None) for g in rep["gates"].values())
    bl = json.loads((REPO / "outputs/S4/example_ota_5t/blocks.json").read_text())["blocks"]
    vs = [v for b in bl for v in b["variants"]]
    assert len(vs) == 5
    for v in vs:
        assert v["drc"]["errors"] == 0 and v["drc"]["neg_control_flagged"], v["cell"]
        assert v["lvs"]["match"] and v["lvs"]["neg_control_rejected"], v["cell"]
        assert v["geometry"]["tap_distance_max_um"] <= 15.0
    abba = next(v for v in vs if v["cell"] == "nmos_differential_pair__ABBA")
    assert abba["symmetry"]["mirror_image"] and abba["symmetry"]["centroid_offset_um"] == 0
