"""Layout rule set v2, phase 1 (docs/rules_v2/ruleset_v2.md; PREREG amendment of 2026-11-05)."""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "tests"))
from test_s4s5 import _s4_inputs  # noqa: E402

CELLS = REPO / "outputs/S3/_cells"


def test_drc_table_is_the_decks_and_reserve_adds_ten_percent_on_a_005_grid():
    from src.common import drc_rules as D
    assert D.deck_values() == D.MIN
    assert [D.reserve(r) for r in ("diff/tap.3", "nwell.2a", "met1.2", "met3.2", "capm.11", "poly.4")] == \
        [0.30, 1.40, 0.20, 0.35, 1.50, 0.10]
    assert D.snap_up(0.30) == 0.30 and D.snap_up(0.3001) == 0.35


def test_v1_is_untouched_without_the_option():
    """No finished design asks for v2, nothing is switched, and iadc_ota's v1 blocks (with its opt-in options) are
    planned unit for unit as committed."""
    from src.common import ruleset as RS
    from src.s4 import block as B, run as S
    from src.s5 import place as P
    for d in ("example_ota_5t", "loadbench_miller", "ttsky25a_fd", "iadc_ota"):
        assert RS.name(d) == "v1" and not RS.apply_s4(d) and not RS.apply_s5(d)
    assert B.UNIT_GAP is None and P.GAP_FN is None and P.ROWGAP_FN is None and B.GAP == 0.6 and P.BLOCK_GAP == 3.0
    d = "iadc_ota"
    ir, groups, dd, rules, lu = _s4_inputs(d)
    opts = S.layout_options(d)
    blocks = {v["cell"]: v for b in json.loads((REPO / "outputs/S4" / d / "blocks.json").read_text())["blocks"]
              for v in b["variants"]}
    for b in S.plan_blocks(ir, groups)[:12]:
        for v in S.variants(b, ir, dd["decisions"], CELLS, rules, lu, opts):
            if not v["units"]:
                continue
            g = B.layout(v["units"], tap_limit=lu, bbox_origin=True,
                         internal=S.internal_nets(b, ir) if opts.get("pack_internal") else None)
            if g["row"][2] > opts["fold_row_um"] and len({u["device"] for u in v["units"]}) == 1:
                continue                                   # folded arrays: covered by test_s4s5
            want = blocks[f"{b['name']}__{v['id']}"]
            assert [(u["device"], u["x"]) for u in g["units"]] == [(a["device"], a["x"]) for a in want["arrangement"]]
            assert g["ring"] == want["geometry"]["ring"]


def _v2(monkeypatch):
    from src.common import ruleset as RS
    from src.s4 import block as B
    for k, v in RS.block_constants().items():
        monkeypatch.setattr(B, k, v)
    monkeypatch.setattr(B, "UNIT_GAP", RS.unit_gap)
    return RS, B


def test_v2_spacings_come_from_the_reserve_rule(monkeypatch):
    RS, B = _v2(monkeypatch)
    c = RS.block_constants()
    assert c == {"FIRST": 0.55, "PITCH": 0.75, "ROW_SEP": 0.75, "RING_GAP": 0.4, "TAP_GAP": 0.4, "COL0": 0.4,
                 "COL_PITCH": 0.6, "NWELL_OVER": 0.3, "EXT": 0.0, "CAPM_SPACE": 1.5, "MET_SPACE": 0.35,
                 "STRIP_CONT_IN": 0.3, "RING_GAP_BODY": 0.8}
    # a ringless NMOS cell: its diffusion 0.125 um in from the box on both sides, so two of them need 0.30 - 0.25
    ng = next(p for p in CELLS.glob("nfet_01v8_W1p4_L0p6_m1__nf1_gboth_sdfull_ng"))
    rec = json.loads((ng / "record.json").read_text())
    u = {"rec": rec, "mirror": False}
    assert RS.unit_gap(u, u) == 0.05 and RS.unit_gap(u, {**u, "mirror": True}) == 0.05


def test_v2_blocks_are_tighter_and_keep_their_devices_off_limits(monkeypatch):
    """iadc_ota's input pair under v2: the same units in the same order, nearer each other and to their ring; the
    device area is a metal3/metal4 keep-out (R1)."""
    from src.s4 import run as S
    ir, groups, dd, rules, lu = _s4_inputs("iadc_ota")
    opts = S.layout_options("iadc_ota")
    b = next(x for x in S.plan_blocks(ir, groups) if x["name"] == "nmos_differential_pair")
    v = S.variants(b, ir, dd["decisions"], CELLS, rules, lu, opts)[0]
    from src.s4 import block as B0
    g1 = B0.layout(v["units"], tap_limit=lu, bbox_origin=True)
    RS, B = _v2(monkeypatch)
    g2 = B.layout(v["units"], tap_limit=lu, bbox_origin=True)
    assert [u["device"] for u in g2["units"]] == [u["device"] for u in g1["units"]]
    w = lambda g: g["ring"][2] - g["ring"][0]          # noqa: E731
    h = lambda g: g["ring"][3] - g["ring"][1]          # noqa: E731
    assert w(g2) < w(g1) and h(g2) < h(g1)
    for a, c in zip(g2["units"], g2["units"][1:]):
        assert abs(c["x"] - (a["x"] + a["w"]) - RS.unit_gap(a, c)) < 1e-6
    assert g2["track_span"] == [g2["ring"][0], g2["ring"][2]]          # EXT 0: tracks end at the ring
    ko = RS.device_keepouts(g2)
    assert {k["layer"] for k in ko} == {"metal3", "metal4"} and all(k["box"] == g2["row"] for k in ko)


def test_v2_placement_abuts_one_body_and_keeps_the_rules_between_others(monkeypatch):
    from src.common import ruleset as RS
    from src.s5 import place as P
    monkeypatch.setattr(P, "GAP_FN", RS.gap_x)
    monkeypatch.setattr(P, "ROWGAP_FN", RS.gap_y)
    monkeypatch.setitem(RS.CHANNEL, "um", 0.0)

    def blk(t, body, w=10.0, h=4.0):
        geo = {"bbox_um": [0, 0, w, h], "row": [0, 0, w, h], "area_um2": w * h}
        return {"type": t, "body": body, "symmetric": False, "devices": [],
                "variants": [{"id": "A", "geometry": geo, "pins": {"tracks": {"top": {}, "bottom": {}}, "body": None}}]}
    blocks = {"p1": blk("pmos", "VDD"), "p2": blk("pmos", "VDD"), "p3": blk("pmos", "VB"), "n1": blk("nmos", "VSS"),
              "c": blk("cap", None)}
    ch = {b: (blocks[b]["variants"][0], False) for b in blocks}
    pl = P.realise([["p1", "p2", "p3"], ["n1", "c"]], ch, blocks, shared_rows=True)
    bb = {b: pl["blocks"][b]["bbox"] for b in blocks}
    assert bb["p2"][0] - bb["p1"][2] == 0.0                     # one body: abut
    assert round(bb["p3"][0] - bb["p2"][2], 4) == 1.4           # n-wells of two nets: nwell.2a reserve
    assert round(bb["c"][0] - bb["n1"][2], 4) == 1.5            # a capacitor: capm.11 reserve
    assert round(bb["p1"][1] - bb["n1"][3], 4) == 1.5           # rows: the widest pair's gap (the capacitor)
    monkeypatch.setitem(RS.CHANNEL, "um", 1.6)                  # R2: two router grids more in every gap
    pl2 = P.realise([["p1", "p2"], ["n1"]], ch, blocks, shared_rows=True)
    b2 = {b: pl2["blocks"][b]["bbox"] for b in ("p1", "p2", "n1")}
    assert round(b2["p2"][0] - b2["p1"][2], 4) == 1.6 and round(b2["p1"][1] - b2["n1"][3], 4) == 1.75
    from src.s5.run import legal
    assert legal(pl, blocks)["separation_ok"] and legal(pl2, blocks)["separation_ok"]


def test_grid_router_keeps_every_net_off_a_device_area():
    from src.s5 import grid as GR
    pl = {"bbox": [0, 0, 20, 10], "blocks": {
        "a": {"pins": [{"net": "n1", "x0": 1.0, "x1": 3.0, "y": 1.0, "kind": "track"}],
              "keepouts": [{"layer": "metal3", "box": [4, 0, 16, 10], "net": None},
                           {"layer": "metal4", "box": [4, 0, 16, 10], "net": None}]},
        "b": {"pins": [{"net": "n1", "x0": 17.0, "x1": 19.0, "y": 1.0, "kind": "track"}]}}}
    r = GR.route(pl, {}, [], ["n1"], [40.0, 40.0])
    assert not r["failed"]
    for layer, i, j in r["routes"]["n1"]["nodes"]:
        x, y = i * GR.GRID, j * GR.GRID
        assert not (4 - GR.GROW < x < 16 + GR.GROW and 0 - GR.GROW < y < 10 + GR.GROW), (layer, x, y)


# ------------------------------------------------------------------ phase 2: drawn blocks, 2-D arrangements, screening
def _centroids(rows):
    """{device: (x, y)} centroid of unit positions (column, row)."""
    acc = {}
    for j, row in enumerate(rows):
        for i, d in enumerate(row):
            acc.setdefault(d, []).append((i, j))
    return {d: (sum(p[0] for p in v) / len(v), sum(p[1] for p in v) / len(v)) for d, v in acc.items()}


def test_2d_arrangements_share_one_centroid_and_include_the_cross_quad():
    from src.s4 import v2 as V2
    devs = {n: {"terminals": {"d": n, "g": "g", "s": "s"}} for n in "ABCD"}
    for counts in ({"A": 2, "B": 2}, {"A": 6, "B": 6}, {"A": 96, "B": 96, "C": 36, "D": 36}, {"A": 18, "B": 18}):
        ar = V2.arrangements(list(counts), counts, devs)
        assert ar
        for vid, rows, strict in ar:
            assert len({len(r) for r in rows}) == 1, vid                      # equal rows
            assert {d: sum(r.count(d) for r in rows) for d in counts} == counts, vid
            if strict >= 2:                                                    # common centroid in x and y
                c = _centroids(rows)
                assert len({(round(x, 6), round(y, 6)) for x, y in c.values()}) == 1, (vid, c)
    xq = dict((a[0], a[1]) for a in V2.arrangements(["A", "B"], {"A": 2, "B": 2}, devs))["XQ"]
    assert xq == [["A", "B"], ["B", "A"]]


def test_series_strings_keep_one_string_per_row():
    from src.s4 import v2 as V2
    ir = json.loads((REPO / "outputs/S0/iadc_ota/circuit_ir.json").read_text())
    devs = {d["name"]: d for d in ir["devices"]}
    names = ["XX1_M33", "XX1_M49", "XX1_M50", "XX1_M63"] + [f"XX1_M{k}" for k in range(64, 80)]
    ch = V2.strings(names, devs)
    assert len(ch) == 5 and all(len(c) == 4 for c in ch) and ch[0] == ["XX1_M33", "XX1_M49", "XX1_M50", "XX1_M63"]
    assert V2.strings(["XX2_M1", "XX2_M2"], devs) is None


def test_designer_dummies_go_to_row_ends_and_rows_stay_equal():
    from src.s4 import v2 as V2
    rec = {"geometry": {"bbox_um": [1.0, 1.0]}}
    unit = lambda d: {"device": d, "rec": rec, "mirror": False, "nets": {"D": "x", "G": "y", "S": "z"}}  # noqa: E731
    rows = [[unit("A"), unit("B")], [unit("B"), unit("A")]]
    full = V2.with_designer_dummies(rows, [unit("D1"), unit("D1"), unit("D2")], "VSS", False)
    assert [len(r) for r in full] == [4, 4]
    assert [u["device"] for u in full[0]] == ["D1", "A", "B", "D1"]
    assert full[1][0]["device"] == "D2" and full[1][-1].get("dummy_of") == "A"      # padded with the flow's dummy
    assert all(t == "VSS" for t in full[1][-1]["nets"].values())


def test_the_drawn_blocks_cover_every_device_once_and_screening_respects_the_outline():
    from src.s4 import run as S, v2 as V2
    ir, groups, dd, rules, lu = _s4_inputs("iadc_ota")
    opts = S.layout_options("iadc_ota_v2")
    assert opts["ruleset"] == "v2" and len(opts["blocks"]) == 14
    blocks = V2.plan_blocks(ir, opts, S.plan_blocks(ir, groups))
    every = sorted(x for b in blocks for x in b["devices"])
    assert every == sorted([d["name"] for d in ir["devices"]] + S.caps_of(ir))
    left = [b["name"] for b in blocks if b["name"] not in {x["name"] for x in opts["blocks"]}]
    assert sorted(left) == ["XC3", "XC4", "nmos_dummy", "pmos_dummy", "pmos_dummy_2"]   # rail dummies, capacitors
    tail = next(b for b in blocks if b["name"] == "x2_cm_tail")
    assert tail["matched"] == ["XX2_M6", "XX2_M5", "XX2_M3", "XX2_M4"] and len(tail["dummies"]) == 4
    vs = [{"id": "wide", "units": [], "rows": 1, "strict": 3}]
    import src.s4.v2 as mod
    real = mod.estimate
    try:
        mod.estimate = lambda *a, **k: {"area_um2": 1.0, "w_um": 400.0, "h_um": 5.0, "wire_um": 1.0, "crossings": 0,
                                        "tap_distance_um": 1.0, "strips_aligned": True}
        kept, rec = V2.screen(tail, vs, lu, True, [161.0, 225.77])
    finally:
        mod.estimate = real
    assert kept == [] and rec[0]["valid"] is False and rec[0]["why"] == "larger than the outline"


def test_a_macro_with_too_many_arrangements_to_enumerate_is_annealed(monkeypatch):
    """iadc_ota_v2's x2: five blocks (<= ENUM_MAX) with three variants each, 746 496 arrangements; S5 stopped."""
    from src.s5 import macro as M, place as P
    calls = []

    def boom(*a, **k):
        raise RuntimeError("746496 candidates: above 50000, needs the annealer")
    monkeypatch.setattr(P, "enumerate_candidates", boom)
    monkeypatch.setattr(M, "anneal", lambda *a, **k: calls.append(a[0]) or {"cost": 1.0, "placement": {}, "rows": [],
                                                                            "choice": {}})
    r = M.place_macro(["a", "b"], {"a": {}, "b": {}}, {}, "area_only", None)
    assert r["method"] == "annealing" and calls == [["a", "b"]]


def test_a_track_next_to_its_devices_is_reached_without_a_wire_over_them():
    """Flow record row 104: the grid point beside a track 0.55 um from its devices lies in the device area; a device
    area holds no metal, so the stub still reaches the track and no wire's edge crosses into the area."""
    from src.s5 import grid as GR
    dev = [{"layer": l, "box": [0.0, 0.0, 20.0, 5.0], "net": None, "kind": "device_area"} for l in ("metal3", "metal4")]
    pl = {"bbox": [0, -2, 30, 5], "blocks": {
        "a": {"pins": [{"net": "n1", "x0": 0.0, "x1": 20.0, "y": -0.55, "kind": "track"}], "keepouts": dev},
        "b": {"pins": [{"net": "n1", "x0": 24.0, "x1": 29.0, "y": 3.0, "kind": "track"}]}}}
    r = GR.route(pl, {}, [], ["n1"], [60.0, 40.0])
    assert not r["failed"]
    for layer, i, j in r["routes"]["n1"]["nodes"]:
        x, y = i * GR.GRID, j * GR.GRID
        assert not (0 - GR.WIRE / 2 < x < 20 + GR.WIRE / 2 and 0 - GR.WIRE / 2 < y < 5 + GR.WIRE / 2), (layer, x, y)
