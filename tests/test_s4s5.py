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
    LOADBench: P5 goes to the bias bank (a matching group), so cs_stage keeps only N3; Capacitor2, which S0 binds
    to a MIM device for the layout view, is a block of its own (plan v4 Phase 6)."""
    from src.s4.run import plan_blocks
    ir, g = _ir_groups("example_ota_5t")
    bl = {b["name"]: b for b in plan_blocks(ir, g)}
    assert {k: sorted(v["devices"]) for k, v in bl.items()} == {
        "pmos_current_mirror_load": ["XM3", "XM4"], "nmos_differential_pair": ["XM1", "XM2"],
        "nmos_current_mirror_bias": ["XM5"]}
    ir, g = _ir_groups("loadbench_miller")
    bl = plan_blocks(ir, g)
    names = [x for b in bl for x in b["devices"]]
    assert sorted(names) == sorted([d["name"] for d in ir["devices"]] + ["Capacitor2"]) and len(names) == len(set(names))
    by = {b["name"]: b for b in bl}
    assert "XNormalTransistorPmos5" in by["pmos_bias_bank"]["devices"]
    assert by["cs_stage"]["devices"] == ["XNormalTransistorNmos3"]
    assert by["input_pair"]["body"] == "FirstStageYsourceTransconductance"     # its own n-well
    devs = {d["name"]: d for d in ir["devices"]}
    assert by["Capacitor2"]["kind"] == "mim_cap"
    for b in bl:
        if b["kind"] == "mim_cap":
            continue
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


# ------------------------------------------------------------------ Phase 6: LOADBench through S4–S7
def _s4_inputs(design):
    from src.s3 import options as O  # noqa: F401  (the S3 cell records the plan reads)
    ir = json.loads((REPO / "outputs/S0" / design / "circuit_ir.json").read_text())
    groups = json.loads((REPO / "outputs/S1" / design / "s1_report.json").read_text())["gates"].get(
        "G1.4_matching_groups", {}).get("groups", [])
    dd = json.loads((REPO / "outputs/S3" / design / "device_decisions.json").read_text())
    rules = json.loads((REPO / "outputs/S2/pdk/parasitics.json").read_text())["rules"]
    cons = json.loads((REPO / "outputs/S2" / design / "constraints.json").read_text())["constraints"]
    lu = next(c["value"] for c in cons if c["id"] == "place.latchup_tap_distance")
    return ir, groups, dd, rules, lu


def test_tap_strips_only_where_the_ring_is_too_far():
    """LOADBench's PMOS bank (P5: 16 fingers of 55 um) is too wide for its ring alone (16.0 um > 15 um, LU.3): one
    tap strip goes between P8 and P5. No 5T block, and no other LOADBench block, gets a strip (plan v4 Phase 6)."""
    from src.s4 import block as B, run as S
    for design in ("loadbench_miller", "example_ota_5t"):
        ir, groups, dd, rules, lu = _s4_inputs(design)
        for b in S.plan_blocks(ir, groups):
            for v in S.variants(b, ir, dd["decisions"], REPO / "outputs/S3/_cells", rules, lu):
                if not v["units"]:
                    assert b["kind"] == "mim_cap"
                    continue
                g = B.layout(v["units"], tap_limit=lu)
                assert S.tap_distance(g) <= lu - B.TAP_MARGIN + 1e-6, (b["name"], v["id"])
                assert bool(g["strips"]) == (b["name"] == "pmos_bias_bank"), (b["name"], v["id"], g["strips"])


def test_mim_capacitor_is_a_block_with_its_plates_on_tracks():
    """S0's PREDICTED binding of LOADBench's ideal Capacitor2 to sky130_fd_pr__cap_mim_m3_1 makes a block of its own:
    top plate on outFirstStage, bottom plate on out (the layout view's order), signed off, met3/met4 kept out."""
    import pytest
    from src.s4 import run as S
    ir, groups, *_ = _s4_inputs("loadbench_miller")
    cap = [b for b in S.plan_blocks(ir, groups) if b["kind"] == "mim_cap"]
    assert len(cap) == 1 and cap[0]["binding"]["top"] == "outFirstStage" and cap[0]["binding"]["bottom"] == "out"
    f = REPO / "outputs/S4/loadbench_miller/blocks.json"
    if not f.exists():
        pytest.skip("needs LOADBench's S4 outputs")
    v = next(v for b in json.loads(f.read_text())["blocks"] if b["kind"] == "mim_cap" for v in b["variants"])
    assert v["ok"] and v["lvs"]["neg_control_rejected"] and v["drc"]["errors"] == 0
    assert {k["layer"] for k in v["geometry"]["keepouts"]} == {"metal3", "metal4"}
    assert list(v["pins"]["tracks"]["top"]) == ["outFirstStage"] and list(v["pins"]["tracks"]["bottom"]) == ["out"]


def test_joined_tracks_count_once_and_runs_are_drawn_at_least_min_len():
    from src.s5 import route as R
    from src.s5.place import joined_once, hpwl
    pins = [{"block": "m", "kind": "track", "y": 0.0, "x0": 0, "x1": 5}, {"block": "m", "kind": "track", "y": 12.0, "x0": 0, "x1": 5},
            {"block": "p", "kind": "track", "y": 15.0, "x0": 0, "x1": 5}, {"block": "m", "kind": "body", "y": -2.0, "x0": 2, "x1": 2}]
    kept = joined_once(pins)
    assert [p["y"] for p in kept] == [12.0, 15.0, -2.0]          # the mirror's upper track, nearer the pair
    assert hpwl([p for p in kept if p["kind"] == "track"]) == 3.0
    a, b = R.drawn(1.6, 1.74)
    assert abs((b - a) - R.MIN_LEN) < 1e-9 and a < 1.6 - R.WIRE / 2


def test_wrapper_maps_ports_as_the_bench_does_and_puts_back_a_current_source():
    """LOADBench's bench connects its DUT as XDUT INN INP OUTP VSS VDD loadbench_miller (in1 in2 out sourceNmos
    sourcePmos); the extracted cell's ports follow that map, and Ibias (a current source the layout view removed)
    goes back on IBIAS."""
    from src.s7.run import bench_ports, wrapped
    tb = (REPO / "outputs/S0/loadbench_miller/tb/diso_amp_AC.spice").read_text()
    w, pm = bench_ports(tb)
    assert pm == {"in1": "INN", "in2": "INP", "out": "OUTP", "sourceNmos": "VSS", "sourcePmos": "VDD"}
    net = ".subckt c_flat out IBIAS in1 in2 sourceNmos sourcePmos blk_0.x\nR0 out IBIAS 1\n.ends\n"
    ir = {"internal_sources": [{"name": "Ibias", "kind": "I", "p": "ibias", "n": "sourceNmos", "dc": 1e-05,
                                "layout_handling": "removed in layout view; node exposed as port IBIAS"}]}
    txt = wrapped(tb, net, "c", ir, {"ibias": "IBIAS"}, set(), {"IBIAS": "ibias"})
    x = next(l for l in txt.splitlines() if l.startswith("XDUT") and "c_flat" in l).split()
    assert x[1:7] == ["OUTP", "N_IBIAS", "INN", "INP", "VSS", "VDD"]
    assert "IIbias_layout N_IBIAS VSS 1e-05" in txt


def test_ext_capacitances_total_and_gate_net(tmp_path):
    """G6.4's .ext reading: equiv records join names into nets, a node record's capacitance goes to the substrate's
    net (a ground), cap records are couplings; values in aF."""
    from src.s6.run import ext_capacitances
    f = tmp_path / "x.ext"
    f.write_text('node "u_0.pc.G" 10 2000 0 0 li\nnode "u_0.pc.D" 10 500 0 0 li\nsubstrate "u_0.pc.S" 0 0 0 0 li\n'
                 'equiv "u_0.pc.G" "blk_0.net2"\nequiv "u_0.pc.D" "OUTP"\nequiv "u_0.pc.S" "VSS_body"\n'
                 'cap "u_0.pc.G" "u_0.pc.D" 250\n')
    c = ext_capacitances(f, {"net2", "OUTP", "VSS"}, {}, {"VSS"})
    assert c["substrate_net"] == "VSS" and c["net"] == {"net2": 2.0, "OUTP": 0.5}
    assert c["coupling"] == {"OUTP~net2": 0.25} and c["total_fF"] == 2.75 and not c["unassigned"]


def test_loadbench_s4_s5_signed_off_and_route_rules_report_the_upstream_misses():
    """LOADBench: every S4 variant signed off (the bank with its strip, the MIM block); both S5 layouts legal, DRC
    clean and LVS-matched; G5.4 fails only on rules a row placement of these blocks cannot meet (outFirstStage's
    length) or S3 already used up (the input pair's access R), and both placements are the same one."""
    import pytest
    f4, f5 = REPO / "outputs/S4/loadbench_miller/s4_report.json", REPO / "outputs/S5/loadbench_miller/s5_report.json"
    if not (f4.exists() and f5.exists()):
        pytest.skip("needs LOADBench's S4 and S5 outputs")
    g4, g5 = json.loads(f4.read_text())["gates"], json.loads(f5.read_text())["gates"]
    assert all(g4[k]["pass"] for k in g4 if "(info)" not in k)
    assert list(g4["G4.5_latchup_tap_distance"]["tap_strips"]) == ["pmos_bias_bank__row"]
    assert all(g5[k]["pass"] for k in ("G5.1_placement_legal", "G5.2_top_DRC", "G5.3_top_LVS"))
    assert g5["G5.5_area_vs_area_only (info)"]["same_placement"]
    d = g5["G5.4_route_rules"]["detail"]["budget_aware"]
    assert [n for n, v in d["max_length"].items() if not v["ok"]] == ["outFirstStage"]
    assert all(v["ok"] for v in d["max_parallel"].values())


def test_loadbench_post_layout_meets_specs_but_loses_more_gbw_than_eta_allows():
    """LOADBench: one placement for both costs, so S6 extracts it once and S7 simulates it once; every spec met post-
    layout (G7.1) with no failed run, but GBW loses more than eta x margin (G7.2), while gain and PM lose almost
    nothing (PREREG predicted the failure on gain)."""
    import pytest
    f6, f7 = REPO / "outputs/S6/loadbench_miller/parasitics_vs_budgets.json", REPO / "outputs/S7/loadbench_miller/metrics.json"
    if not (f6.exists() and f7.exists()):
        pytest.skip("needs LOADBench's S6 and S7 outputs")
    assert json.loads(f6.read_text())["layouts"]["area_only"]["same_as"] == "budget_aware"
    m = json.loads(f7.read_text())
    assert not m["failed_runs"]
    ba = m["metrics"]["budget_aware"]
    assert all(x["meets_spec"] for x in ba.values())
    assert not ba["gbw_mhz"]["within_allowed"] and ba["gain_db"]["use_of_allowed"] < 0.1 and ba["pm_deg"]["use_of_allowed"] < 0.1


def test_mim_self_coupling_is_cancelled_across_the_device_terminals():
    """G7.5's view: a negative capacitor equal to the plate-to-plate coupling that S6 extracted from the lone
    capacitor block, across the MIM device's own two terminals; nothing without a MIM device (plan v4 Phase 7)."""
    from src.s7.run import mim_cancelled
    mims = {"Capacitor2": {"model": "sky130_fd_pr__cap_mim_m3_1", "plate_coupling_fF": 22.47}}
    net = ".subckt c_flat out\nX0 a.t5 out sky130_fd_pr__cap_mim_m3_1 l=15.66 w=15.66\nR0 a.t5 b 1\n.ends\n"
    fixed = mim_cancelled(net, mims).splitlines()
    assert fixed[2] == "Cmimself0 a.t5 out -22.47f" and fixed[1].startswith("X0")
    assert mim_cancelled(".subckt c_flat out\nR0 a b 1\n.ends\n", mims) is None
    # two capacitors drawn as units (ttsky25a_fd, plan v4 Phase 8): each line goes to the capacitor its nets name, and
    # the coupling is split over that capacitor's units; a line neither claims gives None
    m = "sky130_fd_pr__cap_mim_m3_1"
    two = {"XC1": {"model": m, "top": "Vop1", "bottom": "Vom", "plate_coupling_fF": 40.0},
           "XC2": {"model": m, "top": "Vom1", "bottom": "Vop", "plate_coupling_fF": 30.0}}
    net = "".join(f"X{i} {a} {b} {m} l=10 w=10\n" for i, (a, b) in
                  enumerate([("XC1__A_0.Vop1", "Vom"), ("XC2__A_0.Vom1", "Vop")] * 2 + [("XC1__A_0.Vop1", "Vom")]))
    neg = [ln.split() for ln in mim_cancelled(net, two).splitlines() if ln.startswith("Cmimself")]
    assert abs(sum(float(t[3][:-1]) for t in neg if t[2] == "Vom") + 40.0) < 1e-4
    assert abs(sum(float(t[3][:-1]) for t in neg if t[2] == "Vop") + 30.0) < 1e-4 and len(neg) == 5
    assert mim_cancelled(net + f"X9 n1 n2 {m} l=10 w=10\n", two) is None


def test_g62_never_reads_a_net_lower_than_the_ext_and_flat_lvs_reads_cut_names(tmp_path):
    """Review of plan v4 Phase 7: a gate net the C-only netlist leaves at 0 fF is compared with its .ext capacitance;
    Netgen's 43-character columns cut a name (no closing parenthesis), and two different pins in one row fail."""
    from src.s6.run import against_budgets, flat_lvs
    b = {"elements": [{"id": "g1", "kind": "net_capacitance", "budget": 10.0, "units": "fF"}]}
    rows = against_budgets({"net": {}, "coupling": {}}, b, {}, {}, {"devices": []}, {"g1": 37.0})["rows"]
    assert rows[0]["value"] == 37.0 and not rows[0]["ok"] and ".ext" in rows[0]["source"]
    head = "Circuits match uniquely.\nSubcircuit pins:\nCircuit 1: a |Circuit 2: b\n----|----\n"
    cut = "input_pair__AB_0.FirstStageYsourceTranscon |(no pin, node is FirstStageYsourceTranscon \n"
    for rows_, ok in ((cut, True), ("out | out\n", True), ("out | in1\n", False),
                      ("blk_0.net1 |(no pin, node is net9)\n", False)):
        f = tmp_path / "r.txt"
        f.write_text(head + rows_ + "Cell pin lists are equivalent.\n")
        assert flat_lvs(f)["match"] is ok, rows_


def test_block_names_stay_apart():
    from src.s4.run import plan_blocks
    ir = {"devices": [{"name": "XA", "type": "pmos", "terminals": {"b": "VDD", "d": "a", "g": "g", "s": "VDD"}},
                      {"name": "XB", "type": "pmos", "terminals": {"b": "w", "d": "b", "g": "g", "s": "w"}}],
          "hierarchy": {"blocks": [{"name": "pair", "devices": ["XA", "XB"]}]}}
    names = [b["name"] for b in plan_blocks(ir, [])]
    assert len(names) == len(set(names)) == 2


def test_m_copies_centroid_rows_and_dummies():
    """Plan v4 Phase 8: an m = 2 pair is drawn as its copies; with `matching: centroid` it is offered as ABBA and ABAB
    only (no AB); with `dummies` one dummy unit, every terminal on the body, stands at each end; an odd pair (m = 9)
    gets the mirror-image row; the LVS reference carries m."""
    import copy
    from src.s3 import options as O
    from src.s4 import run as S, block as B
    ir, groups, dd, rules, lu = _s4_inputs("example_ota_5t")
    ir = copy.deepcopy(ir)
    for d in ir["devices"]:
        if d["name"] in ("XM1", "XM2"):
            d["m"] = 2
    blk = next(b for b in S.plan_blocks(ir, groups) if set(b["devices"]) == {"XM1", "XM2"})
    cells = REPO / "outputs/S3/_cells"
    old = next(v for v in dd["decisions"].values() if "XM1" in v.get("devices", []))

    def decs():   # S3's type ids include m: the same decision under the patched type's id
        return {**dd["decisions"], **{t: old for t, v in O.device_types(ir).items() if "XM1" in v["devices"]}}
    plain = S.variants(blk, ir, decs(), cells, rules, lu, {})
    assert [v["id"] for v in plain] == ["AB", "ABBA", "ABAB"] and len(plain[0]["units"]) == 4
    cc = S.variants(blk, ir, decs(), cells, rules, lu, {"matching": "centroid", "dummies": True})
    assert [v["id"] for v in cc] == ["ABBA", "ABAB"]
    abba = cc[0]["units"]
    assert [u["device"] for u in abba] == ["DUMMY0", "XM1", "XM2", "XM2", "XM1", "DUMMY1"]
    assert all(u["nets"] == {"D": blk["body"], "G": blk["body"], "S": blk["body"]} for u in (abba[0], abba[-1]))
    for d in ir["devices"]:
        if d["name"] in ("XM1", "XM2"):
            d["m"] = 9
    odd = S.variants(blk, ir, decs(), cells, rules, lu, {"matching": "centroid"})
    assert [v["id"] for v in odd] == ["mirror", "ABAB"]
    seq = [u["device"] for u in odd[0]["units"]]
    assert seq == [("XM2" if x == "XM1" else "XM1") for x in reversed(seq)] and seq.count("XM1") == 9
    ref = B.ref_netlist("b", [{"name": "XM1", "model": "m", "L": 1, "W": 2, "nf": 1, "m": 2, "body_port": "VSS_body",
                               "nets": {"D": "d", "G": "g", "S": "s"}}], ["d", "g", "s", "VSS_body"])
    assert "nf=1 m=2" in ref


def test_s4_plans_of_the_5t_and_loadbench_are_unchanged():
    """Without a layout.yaml, every variant of the 5T and LOADBench is planned unit for unit as committed."""
    from src.s4 import run as S, block as B
    for design in ("example_ota_5t", "loadbench_miller"):
        ir, groups, dd, rules, lu = _s4_inputs(design)
        assert S.layout_options(design) == {}
        got = {}
        for b in S.plan_blocks(ir, groups):
            for v in S.variants(b, ir, dd["decisions"], REPO / "outputs/S3/_cells", rules, lu, {}):
                if v["units"]:
                    g = B.layout(v["units"], tap_limit=lu)
                    got[f"{b['name']}__{v['id']}"] = [(u["device"], u["rec"]["cell"], u["mirror"], u["x"]) for u in g["units"]]
        blocks = json.loads((REPO / "outputs/S4" / design / "blocks.json").read_text())["blocks"]
        want = {v["cell"]: [(a["device"], a["cell"], a["mirror"], a["x"]) for a in v["arrangement"]]
                for b in blocks for v in b["variants"] if v.get("arrangement") and b["kind"] != "mim_cap"}
        assert got == want, design

def test_resistor_strings_interleave_mirrored_with_internal_nets_short():
    """Plan v4 Phase 8 (ttsky25a_fd): each res_pack is one series string; its order is walked from an end, units
    alternate orientation so a shared node sits on one side of both; two packs interleave A B B A (each pack's
    centroid on the centre) with the second string reversed (Vom's end near the right, Vop's at the left); the strings' inner nodes are the
    block's internal nets."""
    import pytest
    from collections import Counter
    from src.s4 import run as S
    ir = json.loads((REPO / "outputs/S0/ttsky25a_fd/circuit_ir.json").read_text())
    opts = S.layout_options("ttsky25a_fd")
    blk = S.resistor_blocks(ir, opts)[0]
    a, b = blk["packs"]
    assert len(a) == len(b) == 20 and a[0]["first"] == "Vop" and a[-1]["last"] == "x2_Vcm"
    assert all(x["last"] == y["first"] for x, y in zip(a, a[1:]))
    if not (REPO / "outputs/S4/_res").exists():
        pytest.skip("needs the resistor unit (outputs/S4/_res)")
    units = S.variants(blk, ir, {}, REPO / "outputs/S3/_cells", {}, 15.0, opts)[0]["units"]
    real = [u for u in units if "dummy_of" not in u]
    pat = ["A" if u["device"].startswith("XX2_X1_") else "B" for u in real]
    assert pat == pat[::-1] and pat[:4] == ["A", "B", "B", "A"]
    side = Counter((u["nets"]["P"], "P") for u in real) + Counter((u["nets"]["N"], "N") for u in real)
    inner = S.internal_nets(blk, ir)
    assert all(side[(n, "P")] in (0, 2) and side[(n, "N")] in (0, 2) for n in inner)
    assert len(inner) == 38 and not {"Vop", "Vom", "x2_Vcm"} & inner
    # the strings' output ends: Vop's at the left end, Vom's next to the right end (the palindrome ends on pack A)
    assert real[0]["device"] == "XX2_X1_R1" and real[-2]["device"] == "XX2_X2_R16"


def test_shared_rows_only_when_asked_and_macros_flatten_by_their_origin():
    """Plan v4 Phase 8: two symmetric blocks may share a row only inside a macro (shared_rows), which is then centred;
    a macro's blocks are placed at the macro's origin when flattened."""
    from src.s5.place import realise
    from src.s5.macro import flatten

    def var(w):
        return {"id": "AB", "geometry": {"bbox_um": [0.0, 0.0, w, 5.0], "row": [0.0, 0.0, w, 5.0]},
                "pins": {"tracks": {"top": {}, "bottom": {}}, "body": None}}
    blocks = {"p": {"symmetric": True, "type": "nmos"}, "q": {"symmetric": True, "type": "nmos"}}
    ch = {"p": (var(4.0), False), "q": (var(6.0), False)}
    assert realise([["p", "q"]], ch, blocks) is None
    pl = realise([["p", "q"]], ch, blocks, shared_rows=True)
    assert abs(pl["bbox"][0] + pl["bbox"][2]) < 1e-9          # the row is centred
    top = {"rows": [["m"]], "bbox": [0, 0, 1, 1], "area_um2": 1,
           "blocks": {"m": {"origin": [10.0, -2.0], "bbox": [0, 0, 1, 1], "variant": "w100"}}}
    flat = flatten(top, {"m": {"w100": {"placement": pl, "method": "enumeration", "cost": 1.0}}})
    assert flat["blocks"]["p"]["origin"][0] == round(pl["blocks"]["p"]["origin"][0] + 10.0, 4)
    assert flat["blocks"]["q"]["macro"] == "m" and flat["macros"]["m"]["shape"] == "w100"


def test_wrapper_puts_back_an_off_chip_passive():
    """ttsky25a_fd: S0 removed the off-chip 12 kohm Rgm_ext from the layout view and exposed its node as RGM; S7's
    bench puts it back between RGM and the bench's VSS, as it puts Vref_ext back on VREF (plan v4 Phase 8)."""
    from src.s7.run import wrapped
    tb = (REPO / "outputs/S0/ttsky25a_fd/tb/dido_amp_AC.spice").read_text()
    ir = json.loads((REPO / "outputs/S0/ttsky25a_fd/circuit_ir.json").read_text())
    net = ".subckt c_flat Vop Vm Vdd Vss Vom Vp RGM VREF\nR0 Vop Vm 1\n.ends\n"
    txt = wrapped(tb, net, "c", ir, {"Rgm": "RGM", "Vref": "VREF"}, set(), {"RGM": "Rgm", "VREF": "Vref"})
    assert "RRgm_ext_layout N_RGM VSS 12000.0" in txt and "VVref_ext_layout N_VREF VSS 0.9" in txt


def test_grid_router_joins_pins_and_keeps_wires_clear_of_tracks():
    """Plan v4 Phase 8.5: two blocks side by side; net a has a track in each; port p has one pin. The router joins
    a's pins (a stub and a via3 down to each track), gives p a stub for its label, and no metal3 wire comes within
    SPACE of any track."""
    from src.s5 import grid as GR

    def blk(x, nets):
        return {"pins": [{"net": n, "kind": "track", "x0": x, "x1": x + 6.0, "y": y} for n, y in nets],
                "bbox": [x, -2.0, x + 6.0, 6.0]}
    pl = {"bbox": [0.0, -2.0, 20.0, 6.0],
          "blocks": {"L": blk(0.0, [("a", 5.05), ("b", 4.15)]), "R": blk(14.0, [("a", -1.05), ("p", 5.05)])}}
    res = GR.route(pl, {}, ["p"], ["a"])
    assert not res["failed"] and set(res["routes"]) == {"a", "p"}
    a = res["routes"]["a"]
    assert len(a["stubs"]) == 2 and {round(y, 2) for _, _, y in a["stubs"]} == {5.05, -1.05}
    assert len(res["routes"]["p"]["stubs"]) == 1
    tracks = [(q["y"], q["x0"], q["x1"]) for b in pl["blocks"].values() for q in b["pins"]]
    for n, r in res["routes"].items():
        for y, x0, x1 in GR.segments(r)["metal3"]:
            for ty, tx0, tx1 in tracks:
                if x1 + GR.WIRE / 2 > tx0 and x0 - GR.WIRE / 2 < tx1:
                    assert abs(y - ty) >= GR.WIRE + GR.SPACE - 1e-9, (n, y, ty)


def test_flat_lvs_accepts_a_symmetric_match(tmp_path):
    from src.s6.run import flat_lvs
    f = tmp_path / "r.txt"
    f.write_text("Netlists match with 3 symmetries.\nSubcircuit pins:\nblk_0.x1_net3 |(no pin, node is x1_net3)\n"
                 "Final result: Top level cell failed pin matching.\n")
    assert flat_lvs(f)["match"]
    f.write_text("Netlists do not match.\n")
    assert not flat_lvs(f)["match"]


def test_flat_lvs_accepts_crossed_labels_only_on_interchangeable_nets(tmp_path):
    """Flow record row 90: Netgen cuts a name at 42 characters plus a space, and with symmetries it can pair two
    interchangeable nets crosswise (ttsky25a_fd's x1_net3 / x1_net4, two identical stacks between x1_net2 and Vss)."""
    from src.s6.run import flat_lvs
    ref = tmp_path / "ref.spice"
    ref.write_text(".subckt top a b g\n"
                   "M1 n3 g b b nfet L=10 W=1\nM2 n4 g b b nfet L=10 W=1\n"
                   "M19 a g n3 b nfet L=1 W=1\nM3 a g n4 b nfet L=1 W=1\n"
                   "M4 b g n5 b nfet L=1 W=1\nM7 n5 g b b nfet L=10 W=1\n.ends\n")
    def report(rows, head="Netlists match with 3 symmetries.\n"):
        f = tmp_path / "r.txt"
        f.write_text(head + "Subcircuit pins:\nCircuit 1: x |Circuit 2: y\n---|---\n"
                     + "".join(f"{a:<42} |(no pin, node is {b})\n" for a, b in rows)
                     + "Final result: Top level cell failed pin matching.\n")
        return f
    cut = "c" * 38 + "_0.n"                         # 42 characters: Netgen cut the label n4 to "n"
    assert len(cut) == 42
    # n3 and n4 cross: interchangeable, so accepted; the cut label is resolved to n4
    r = flat_lvs(report([("blk_0.n3", "n4"), (cut, "n3")]), ref)
    assert r["match"] and r["symmetric_relabel"] == {"n4": "n3", "n3": "n4"}
    r = flat_lvs(report([("blk_0.n3", "n4"), ("blk_0.n4", "n3")]), ref)
    assert r["match"] and r["symmetric_relabel"] == {"n4": "n3", "n3": "n4"}
    assert not flat_lvs(report([("blk_0.n3", "n4"), ("blk_0.n4", "n3")], "Circuits match uniquely.\n"), ref)["match"]
    # n3 and n5 are not interchangeable (M19's drain is a, M4's is b): a label on the wrong net
    assert not flat_lvs(report([("blk_0.n3", "n5"), ("blk_0.n5", "n3")]), ref)["match"]
    # without the reference, or without symmetries, a crossing fails
    assert not flat_lvs(report([("blk_0.n3", "n4"), ("blk_0.n4", "n3")]))["match"]
    # a name cut at 42 characters is read as a prefix
    assert flat_lvs(report([("x" * 36 + "_0.net", "net7")]), ref)["match"]


def test_phase8_review_fixes(tmp_path):
    """The review of plan v4 Phase 8 (flow record row 92): (1) an internal net with stubs on both sides gets its own
    track span on each side; (2) a node a removed source leaves as a port is never internal; (3) S5 calls a block
    symmetric only with a mirror-image variant; (4) S5's dummies go into the top cell, not the first subcircuit."""
    from src.s4 import run as S, block as B
    from src.s5 import run as R
    ir, groups, dd, rules, lu = _s4_inputs("example_ota_5t")
    blk = next(b for b in S.plan_blocks(ir, groups) if b["name"] == "pmos_current_mirror_load")
    v = next(v for v in S.variants(blk, ir, dd["decisions"], REPO / "outputs/S3/_cells", rules, lu, {}) if v["id"] == "AB")
    g = B.layout(v["units"], tap_limit=lu, internal={"net3", "OUTP"})
    cx = g["columns"]["net3"]
    for side in ("top", "bottom"):
        xs = [s["x"] for u in g["units"] for s in u["stubs"] if s["side"] == side and s["net"] == "net3"]
        lo, hi = g["spans"][side]["net3"]
        assert xs and lo <= min(xs) and hi >= max(xs) and hi >= cx       # covers its own side's stubs and the column
    # (2) a port node: 5T's VBIAS is net2, the node of the removed source V1
    assert "net2" in {s["p"] for s in ir["internal_sources"]}
    fake = {"devices": [{"name": "M1", "terminals": {"d": "x", "g": "net2", "s": "VSS", "b": "VSS"}},
                        {"name": "M2", "terminals": {"d": "y", "g": "x", "s": "VSS", "b": "VSS"}}],
            "ports": [{"name": "VBIAS"}], "internal_sources": ir["internal_sources"]}
    assert S.internal_nets({"devices": ["M1", "M2"], "body": "VSS"}, fake) == {"x", "y"}
    # (3) ttsky25a_fd's unmatched pair (6/1 against 1/5 um) is not symmetric; the 5T's pairs still are
    tt = R.load_blocks(REPO / "outputs/S4/ttsky25a_fd")
    assert not tt["pmos_current_mirror_2"]["symmetric"] and tt["nmos_differential_pair"]["symmetric"]
    five = R.load_blocks(REPO / "outputs/S4/example_ota_5t")
    assert five["nmos_differential_pair"]["symmetric"] and five["pmos_current_mirror_load"]["symmetric"]
    # (4) dummies inside the top cell of a hierarchical view
    vdir = tmp_path / "v"
    (vdir / "lvs").mkdir(parents=True)
    (vdir / "ref.spice").write_text(".subckt b d g s VSS_body\nXb_DUMMY0 VSS_body VSS_body VSS_body VSS_body "
                                    "sky130_fd_pr__nfet_01v8 L=1 W=1 nf=1\nXXM1 d g s VSS_body sky130_fd_pr__nfet_01v8 "
                                    "L=1 W=1 nf=2\n.ends\n")
    blocks = {"b": {"variants": [{"id": "A", "lvs": {"report": str(vdir / "lvs" / "lvs_report.txt")}}]}}
    ref = ".subckt sub a b\nR1 a b 1\n.ends\n.subckt top a VSS\nXM1 a a VSS VSS sky130_fd_pr__nfet_01v8 L=1 W=1 nf=1\n.ends\n"
    out = R.top_ref(ref, {"blocks": {"b": {"variant": "A"}}}, blocks, tmp_path, {}, "top").splitlines()
    dummy = next(i for i, ln in enumerate(out) if "_DUMMY0" in ln)
    assert out.index(".subckt top a VSS") < dummy and out[dummy].split()[1:5] == ["VSS"] * 4
    assert "nf=2" in out[out.index(".subckt top a VSS") + 1]
