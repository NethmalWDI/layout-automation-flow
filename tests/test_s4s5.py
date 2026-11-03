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


# ------------------------------------------------------------------ Phase 3: S5 placement
def test_ordered_partitions_count_and_rows():
    from src.s5.place import ordered_partitions
    assert sorted(map(str, ordered_partitions(["a", "b"]))) == sorted(map(str, [[["a", "b"]], [["b", "a"]], [["a"], ["b"]], [["b"], ["a"]]]))
    assert len(ordered_partitions(list("abcd"))) == 24 * 8


def test_hpwl_counts_the_gap_between_tracks_not_their_span():
    from src.s5.place import hpwl
    a = {"x0": 0.0, "x1": 10.0, "y": 0.0}
    assert hpwl([a, {"x0": 5.0, "x1": 12.0, "y": 4.0}]) == 4.0          # overlapping spans: vertical only
    assert hpwl([a, {"x0": 13.0, "x1": 20.0, "y": 4.0}]) == 7.0         # 3 um gap + 4 um


def test_realise_rejects_two_symmetric_blocks_in_a_row_and_centres_the_axis():
    from src.s5.place import realise
    def var(w):
        return {"id": "AB", "geometry": {"bbox_um": [-1.0, -1.0, w + 1.0, 5.0], "row": [0.0, 0.0, w, 4.0]},
                "pins": {"tracks": {"top": {}, "bottom": {}}, "body": {"net": "VSS", "at": [w / 2, -1.0]}}}
    blocks = {"p": {"symmetric": True, "type": "nmos"}, "q": {"symmetric": True, "type": "nmos"},
              "t": {"symmetric": False, "type": "nmos"}}
    assert realise([["p", "q"]], {"p": (var(4.0), False), "q": (var(4.0), False)}, blocks) is None
    pl = realise([["p", "t"]], {"p": (var(4.0), False), "t": (var(2.0), False)}, blocks)
    assert abs(pl["blocks"]["p"]["axis_x"]) < 1e-9


def test_5t_placement_legal_and_budget_aware_uses_less_wire_budget():
    """The 5T's budget-aware placement is legal (separation, PMOS above NMOS, symmetric blocks on the axis, unrouted
    DRC clean), stacks mirror, pair and tail with the pair and tail flipped so their shared tracks face each other,
    and uses no more of any net's wire budget than the area-only placement."""
    import pytest
    f = REPO / "outputs/S5/example_ota_5t/placement.json"
    if not f.exists():
        pytest.skip("needs the 5T's S5 outputs")
    rep = json.loads((REPO / "outputs/S5/example_ota_5t/s5_report.json").read_text())
    assert rep["gates"]["G5.1_placement_legal"]["pass"]
    ch = json.loads(f.read_text())["chosen"]
    ba, ao = ch["budget_aware"], ch["area_only"]
    assert ba["placement"]["rows"] == [["pmos_current_mirror_load"], ["nmos_differential_pair"], ["nmos_current_mirror_bias"]]
    assert ba["placement"]["blocks"]["nmos_differential_pair"]["flip"] and ba["placement"]["blocks"]["nmos_current_mirror_bias"]["flip"]
    assert all(ba["cost"]["u"][n] <= ao["cost"]["u"][n] for n in ba["cost"]["u"])
    assert ba["cost"]["area_um2"] <= 1.25 * ao["cost"]["area_um2"]


# ------------------------------------------------------------------ Phase 4: S5 routing
def test_net_map_takes_the_layout_view_names():
    """The layout view renames a node (net2 -> VBIAS: the internal source V1 is removed and its node is a port);
    the router must label the port with that name (the first top-level LVS missed it)."""
    from src.s5 import route as R
    ir = json.loads((REPO / "outputs/S0/example_ota_5t/circuit_ir.json").read_text())
    ref = (REPO / "outputs/S0/example_ota_5t/ref/example_ota_5t_layout.spice").read_text()
    m = R.net_map(ir, ref)
    assert m["net2"] == "VBIAS" and m["net1"] == "net1" and m["VSS"] == "VSS"
    assert R.ports_of(ref) == ["VDD", "OUTP", "INP", "INN", "VSS", "VBIAS"]


def test_router_mirrors_the_hard_pair_and_keeps_spines_apart():
    import pytest
    from src.s5 import route as R
    f = REPO / "outputs/S5/example_ota_5t/placement.json"
    if not f.exists():
        pytest.skip("needs the 5T's S5 outputs")
    pl = json.loads(f.read_text())["chosen"]["budget_aware"]["placement"]
    ir = json.loads((REPO / "outputs/S0/example_ota_5t/circuit_ir.json").read_text())
    ref = (REPO / "outputs/S0/example_ota_5t/ref/example_ota_5t_layout.spice").read_text()
    rt = R.plan_routes(pl, R.net_map(ir, ref), R.ports_of(ref), ["net3", "OUTP", "net1"],
                       [("INP", "INN", "hard"), ("OUTP", "net3", "soft")])
    assert rt["INP"]["spine"]["x"] == -rt["INN"]["spine"]["x"] != 0
    assert {"VDD", "OUTP", "INP", "INN", "VSS", "VBIAS", "net1", "net3"} <= set(rt)
    sp = [(n, r["spine"]) for n, r in rt.items()]
    for i, (a, s) in enumerate(sp):
        for b, t in sp[i + 1:]:
            if abs(s["x"] - t["x"]) < R.GRID - 1e-6:   # one column: far enough apart in y
                assert s["y"][1] < t["y"][0] - R.Y_CLEAR + 1e-6 or t["y"][1] < s["y"][0] - R.Y_CLEAR + 1e-6, (a, b)


def test_5t_routed_signed_off_and_area_only_needs_more_wire():
    """Both 5T layouts pass top-level DRC and LVS (controls caught) and every evaluated route rule; the area-only
    placement, routed by the same router, uses more of every budgeted net's wire length."""
    import pytest
    f = REPO / "outputs/S5/example_ota_5t/s5_report.json"
    if not f.exists():
        pytest.skip("needs the 5T's S5 outputs")
    g = json.loads(f.read_text())["gates"]
    assert all(g[k]["pass"] for k in ("G5.1_placement_legal", "G5.2_top_DRC", "G5.3_top_LVS", "G5.4_route_rules"))
    for r in ("budget_aware", "area_only"):
        assert g["G5.3_top_LVS"]["detail"][r]["neg_control_rejected"]
    ba, ao = (g["G5.4_route_rules"]["detail"][r]["max_length"] for r in ("budget_aware", "area_only"))
    assert all(ba[n]["use"] < ao[n]["use"] for n in ba)


# ------------------------------------------------------------------ Phase 5: S6 extraction and S7 post-layout
def test_capacitances_split_into_net_and_coupling(tmp_path):
    """A capacitance to an AC ground counts toward its net; between two signal nets, toward their coupling; a block
    prefix and a ring name map to the net; an unnamed node is reported, never guessed."""
    from src.s6.run import capacitances
    f = tmp_path / "p.spice"
    f.write_text(".subckt x_flat OUTP VDD\nC0 OUTP VDD 1.5f\nC1 blk_0.net1 OUTP 0.25f\nC2 VSS_body blk_0.net3 2f\n"
                 "C3 OUTP a_1_2# 0.1f\nC4 VDD VSS 9f\n.ends\n")
    c = capacitances(f, {"OUTP", "VDD", "VSS", "net1", "net3"}, {}, {"VDD", "VSS"})
    assert c["net"] == {"OUTP": 1.5, "net3": 2.0}
    assert c["coupling"] == {"OUTP~net1": 0.25}
    assert c["unassigned"] == [["OUTP", "a_1_2#", 0.1]] and c["n_caps"] == 5


def test_flat_lvs_accepts_only_inner_nets_as_extra_ports(tmp_path):
    from src.s6.run import flat_lvs
    good = ("Circuits match uniquely.\nSubcircuit pins:\nblk_0.net1          |(no pin, node is net1)\n"
            "Final result: Top level cell failed pin matching.\n")
    bad = good.replace("node is net1)", "node is net9)")
    prop = good + "Property errors were found.\n"
    for txt, ok in ((good, True), (bad, False), (prop, False)):
        f = tmp_path / "r.txt"
        f.write_text(txt)
        assert flat_lvs(f)["match"] is ok


def test_wrapper_connects_only_the_first_port_of_a_name():
    """In the R+C netlist a name repeats (VDD twice; each unit's D/G/S/B): only its first port reaches the bench,
    every other gets its own node (the first S7 run shorted all D pins together and drew 1.6 A)."""
    from src.s7.run import wrapped
    net = ".subckt c_flat OUTP INN INP VBIAS VDD VSS VDD D D S\nR0 VDD D 1\n.ends\n"
    ir = {"internal_sources": [{"name": "V1", "p": "net2", "n": "VSS", "dc": 0.75,
                                "layout_handling": "removed in layout view; node exposed as port VBIAS"}]}
    txt = wrapped(".lib x tt\n.subckt dut_amp INP INN OUTN VDD VSS OUTP\nXDUT a b\n.ends\n.end\n", net, "c",
                  ir, {"net2": "VBIAS"}, set(), {})
    x = next(l for l in txt.splitlines() if l.startswith("XDUT")).split()
    assert x[1:7] == ["OUTP", "INN", "INP", "N_VBIAS", "VDD", "VSS"]
    assert x[7] != "VDD" and x[8] != x[9] and len(set(x[7:11])) == 4
    assert "VV1_layout N_VBIAS VSS 0.75" in txt and ".option rshunt=1e12" in txt


def test_5t_post_layout_within_budgets_and_eta():
    """The 5T's budget-aware layout: every budgeted parasitic within S2's budget (G6.2), every spec met post-layout
    (R+C) and each spec's loss within eta x margin (G7.1, G7.2), so H4 holds on the 5T."""
    import pytest
    f6, f7 = REPO / "outputs/S6/example_ota_5t/s6_report.json", REPO / "outputs/S7/example_ota_5t/s7_report.json"
    if not (f6.exists() and f7.exists()):
        pytest.skip("needs the 5T's S6 and S7 outputs")
    g6, g7 = json.loads(f6.read_text())["gates"], json.loads(f7.read_text())["gates"]
    assert g6["G6.1_extracted_and_LVS"]["pass"] and g6["G6.2_parasitics_within_budgets"]["pass"]
    assert g7["G7.1_specs_met_post_layout"]["pass"] and g7["G7.2_loss_within_eta_margin"]["pass"]
    assert g7["H4 (info)"]["G6.2"] and g7["H4 (info)"]["G7.1_and_G7.2"]
