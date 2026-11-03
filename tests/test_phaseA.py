"""Unit tests for Plan v3 Phase A (docs/plan_v3_phaseA.md). Step 2: run hygiene, i.e. exit codes, clean output
folders and the snapshot identity check (flow record 7.1, rows 40 and 43)."""
import datetime as dt
import json
import re
import sys
from argparse import Namespace
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import compare_before_after as CB  # noqa: E402
from src import flow  # noqa: E402
from src.common import hygiene as H  # noqa: E402


# ------------------------------------------------------------------ step 2: exit codes and run identity
def test_exit_codes_and_run_id():
    assert (H.EXIT_PASS, H.EXIT_GATE_FAIL) == (0, 3)
    assert H.gate_exit(True) == 0 and H.gate_exit(False) == 3
    rid = H.new_run_id()
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d-[0-9a-f]{8}", rid) and rid != H.new_run_id()


def _report_step(code: str, report: Path) -> list:
    return [sys.executable, "-c", code, str(report)]


WRITE = "import json, sys, pathlib; p = pathlib.Path(sys.argv[1]); p.parent.mkdir(parents=True, exist_ok=True); "


@pytest.mark.parametrize("code,status", [
    (WRITE + "p.write_text(json.dumps({'gates': {'G9.1': {'pass': True}}}))", "PASS"),
    (WRITE + "p.write_text(json.dumps({'gates': {'G9.1': {'pass': False}}})); sys.exit(3)", "FAIL"),
    ("raise RuntimeError('boom')", "ERROR"),                                       # a crash exits with 1
    (WRITE + "p.write_text(json.dumps({'gates': {'G9.1': {'pass': True}}})); raise RuntimeError('late')", "ERROR"),
    (WRITE + "p.write_text(json.dumps({'gates': {'G9.1': {'pass': False}}})); sys.exit(1)", "ERROR"),
])
def test_flow_status_comes_from_the_exit_code(tmp_path, monkeypatch, code, status):
    """0 -> PASS, 3 -> FAIL, anything else -> ERROR, even when the step left a fresh report (row 40)."""
    monkeypatch.setattr(flow, "REPO", tmp_path)
    rp = tmp_path / "outputs" / "S2" / "d" / "s2_report.json"
    monkeypatch.setattr(flow, "steps", lambda st, d, a: [("run", _report_step(code, rp))])
    rec = flow.run_stage("S2", "d", Namespace())
    assert rec["status"] == status, rec


def test_flow_stops_at_a_crashed_step(tmp_path, monkeypatch):
    monkeypatch.setattr(flow, "REPO", tmp_path)
    marker = tmp_path / "second_step_ran"
    monkeypatch.setattr(flow, "steps", lambda st, d, a: [
        ("cells", [sys.executable, "-c", "raise SystemExit('no PDK')"]),
        ("run", [sys.executable, "-c", f"open({str(marker)!r}, 'w').close()"])])
    rec = flow.run_stage("S2", "d", Namespace())
    assert rec["status"] == "ERROR" and "cells" in rec["reason"] and not marker.exists()


# ------------------------------------------------------------------ step 2: clean output folders
def test_a_run_leaves_no_file_from_an_earlier_run(tmp_path):
    out = tmp_path / "S2" / "d"
    (out / "work").mkdir(parents=True)
    (out / "budgets.json").write_text("old")
    (out / "work" / "ac.log").write_text("old")
    prev = H.fresh_output_dir(out)
    assert out.is_dir() and not any(out.iterdir())
    assert (prev / "budgets.json").read_text() == "old" and (prev / "work" / "ac.log").exists()
    (out / "baselines.json").write_text("second run")
    H.fresh_output_dir(out)                                    # an earlier .prev is replaced, not merged
    assert sorted(p.name for p in prev.iterdir()) == ["baselines.json"] and not any(out.iterdir())


def test_kept_caches_stay_in_place(tmp_path):
    out = tmp_path / "S3" / "d"
    (out / "sim" / "baseline").mkdir(parents=True)
    (out / "s3_report.json").write_text("old")
    (out / "sim" / "baseline" / "ac.log").write_text("cache")
    prev = H.fresh_output_dir(out, keep=("sim",))
    assert sorted(p.name for p in out.iterdir()) == ["sim"] and (out / "sim" / "baseline" / "ac.log").exists()
    assert sorted(p.name for p in prev.iterdir()) == ["s3_report.json"]
    assert H.fresh_output_dir(tmp_path / "S3" / "new") is None and (tmp_path / "S3" / "new").is_dir()


# ------------------------------------------------------------------ step 2: snapshot identity check
def _s2(tmp_path, files: dict):
    s2 = tmp_path / "outputs" / "S2" / "d"
    s2.mkdir(parents=True, exist_ok=True)
    for name, doc in files.items():
        (s2 / name).write_text(json.dumps(doc))


def _snap_env(tmp_path, monkeypatch):
    monkeypatch.setattr(CB, "REPO", tmp_path)
    monkeypatch.setattr(CB, "OUT", tmp_path / "outputs" / "compare")


def test_snap_refuses_mixed_run_ids(tmp_path, monkeypatch):
    _snap_env(tmp_path, monkeypatch)
    _s2(tmp_path, {"budgets.json": {"run_id": "A", "eta": 0.9, "elements": []},
                   "s2_report.json": {"run_id": "B", "eta": 0.5, "gates": {}}})
    with pytest.raises(CB.SnapRefused) as e:
        CB.snap("d", "t")
    assert "run_id" in str(e.value) and "eta" in str(e.value)
    assert not (tmp_path / "outputs" / "compare" / "d" / "t.json").exists()


def test_snap_refuses_an_unfinished_or_stale_s2(tmp_path, monkeypatch):
    _snap_env(tmp_path, monkeypatch)
    _s2(tmp_path, {"budgets.json": {"run_id": "A", "eta": 0.5, "elements": []}})
    with pytest.raises(CB.SnapRefused, match="did not finish"):
        CB.snap("d", "t")
    _s2(tmp_path, {"s2_report.json": {"run_id": "A", "eta": 0.5, "gates": {}}})
    summ = tmp_path / "outputs" / "flow" / "d" / "flow_summary.json"
    summ.parent.mkdir(parents=True)
    later = (dt.datetime.now() + dt.timedelta(minutes=5)).isoformat(timespec="seconds")
    summ.write_text(json.dumps({"stages": {"S2": {"started": later, "status": "ERROR"}}}))
    with pytest.raises(CB.SnapRefused, match="older than the S2 start"):
        CB.snap("d", "t")


def test_snap_accepts_one_run_and_records_its_id(tmp_path, monkeypatch):
    _snap_env(tmp_path, monkeypatch)
    _s2(tmp_path, {"budgets.json": {"run_id": "A", "eta": 0.5, "elements": []},
                   "s2_report.json": {"run_id": "A", "eta": 0.5, "gates": {}},
                   "baselines.json": {"run_id": "A", "eta": 0.5, "methods": {}}})
    rec = json.loads(CB.snap("d", "t").read_text())
    assert rec["S2"]["run_id"] == "A" and rec["S2"]["eta"] == 0.5


# ------------------------------------------------------------------ step 3: nominal-only budgets, PVT reported
def test_nominal_budgets_allocate_with_nominal_checks_only():
    from src.s2 import run as S2
    nom = [{"id": "gbw_mhz"}, {"id": "pm_deg"}]
    pvt = [{"id": "gbw_mhz@tt_v0.9_t27"}, {"id": "pm_deg@ss_v1.1_t85"}]
    assert [c["id"] for c in S2.allocation_constraints(nom, pvt, "nominal")] == ["gbw_mhz", "pm_deg"]
    assert [c["id"] for c in S2.allocation_constraints(nom, pvt, "all")] == [c["id"] for c in nom + pvt]
    with pytest.raises(ValueError):
        S2.allocation_constraints(nom, pvt, "middle9")


def test_pvt_use_table_lists_every_point_with_its_use():
    from src.s2 import run as S2
    pts = {"tt_v1_t27": {"margin": {"gbw_mhz": 10.0, "pm_deg": 5.0}},
           "ss_v0.9_t85": {"margin": {"gbw_mhz": -1.0, "pm_deg": 2.0}},
           "ff_v1.1_t-40": {"margin": {"gbw_mhz": 3.0, "pm_deg": 1.0}},
           "sf_v0.9_t-40": {"margin": {"gain_db": -45.9}, "meas": {"gain_db": -15.9}}}   # no unity-gain crossing
    eta = 0.5
    info = {"constraints": [
        {"id": "gbw_mhz@tt_v1_t27", "spec": "gbw_mhz", "point": "tt_v1_t27", "b": eta * 10, "a": {"e1": 1.0, "e2": 2.0}},
        {"id": "pm_deg@tt_v1_t27", "spec": "pm_deg", "point": "tt_v1_t27", "b": eta * 5, "a": {"e1": 0.5}},
        {"id": "pm_deg@ss_v0.9_t85", "spec": "pm_deg", "point": "ss_v0.9_t85", "b": eta * 2, "a": {"e2": 1.0}}],
        "skipped_spec_not_met": {"ss_v0.9_t85": ["gbw_mhz"], "sf_v0.9_t-40": ["gbw_mhz", "pm_deg"]},
        "op_failed": ["ff_v1.1_t-40"]}
    t = S2.pvt_use_table(info, pts, ("gbw_mhz", "pm_deg"), {"e1": 2.0, "e2": 1.5})
    tab = t["use_of_allowed"]
    assert sorted(tab) == sorted(pts)                                       # every point is listed
    assert tab["tt_v1_t27"]["gbw_mhz"] == pytest.approx((1.0 * 2.0 + 2.0 * 1.5) / 5.0)   # exactly 1: not "over"
    assert tab["tt_v1_t27"]["pm_deg"] == pytest.approx(0.5 * 2.0 / 2.5)
    assert tab["ss_v0.9_t85"] == {"gbw_mhz": "spec not met before layout", "pm_deg": pytest.approx(1.5)}
    assert set(tab["ff_v1.1_t-40"].values()) == {"no operating point at this point"}
    assert set(tab["sf_v0.9_t-40"].values()) == {"not defined: gain below 0 dB (no unity-gain crossing)"}
    assert t["worst"] == {"point": "ss_v0.9_t85", "spec": "pm_deg", "use_of_allowed": pytest.approx(1.5)}
    assert t["over_allowed"] == ["pm_deg@ss_v0.9_t85"]                     # reported, not gated


def test_only_the_two_phase_A_packages_budget_at_nominal():
    from src.s0.ingest import load_package
    corners = {d: load_package(REPO / "inputs" / d / "package.yaml").get("budget_corners", "all")
               for d in ("example_ota_5t", "loadbench_miller", "ota5t_stress", "iadc_ota", "ttsky25a_fd")}
    assert corners == {"example_ota_5t": "nominal", "loadbench_miller": "nominal", "ota5t_stress": "all",
                       "iadc_ota": "all", "ttsky25a_fd": "all"}   # ota5t_stress inherits the 5T package


# ------------------------------------------------------------------ step 4: S3 saturation do-no-harm (row 41)
def test_do_no_harm_below_vdsat():
    """Schematic vds - vdsat = -0.05 V: an option may lower it by at most TOL_USE x 0.05 V = 1 mV."""
    from src.common.tolerance import TOL_USE
    from src.s3.run import DO_NO_HARM, use_check
    scale = abs(-0.05)
    none_, small, at_lim, big = (use_check(u, 0.0, scale, 0.5, below_vdsat=True) for u in (0.0, 0.0005, TOL_USE * scale, 0.002))
    assert none_["ok"] and small["ok"] and at_lim["ok"] and not big["ok"]       # 2 mV of further harm fails
    assert none_["rule"] == DO_NO_HARM
    assert none_["slack_frac_of_margin"] > small["slack_frac_of_margin"] > 0 > big["slack_frac_of_margin"]
    assert none_["slack_frac_of_margin"] == pytest.approx(TOL_USE)
    old = lambda u: u <= 0.0 + 0.01 * (-0.05)   # noqa: E731  plan v2: margin = the negative schematic value
    assert not old(0.0)                         # ... so even an option that does no harm failed (row 41)


# ------------------------------------------------------------------ step 5: tagging and grouping (A3; D-e)
LB_DEV = {   # LOADBench (plan-v2 circuit_ir.json): type, d, g, s, W (um); m = 1 everywhere
    "XDiodeTransistorNmos1": ("nmos", "FirstStageYout1", "FirstStageYout1", "sourceNmos", 66.13),
    "XDiodeTransistorPmos2": ("pmos", "ibias", "ibias", "sourcePmos", 37.3),
    "XNormalTransistorNmos3": ("nmos", "out", "outFirstStage", "sourceNmos", 484.2),
    "XNormalTransistorNmos4": ("nmos", "outFirstStage", "FirstStageYout1", "sourceNmos", 66.13),
    "XNormalTransistorPmos5": ("pmos", "out", "ibias", "sourcePmos", 887.03),
    "XNormalTransistorPmos6": ("pmos", "outFirstStage", "in2", "FirstStageYsourceTransconductance", 14.21),
    "XNormalTransistorPmos7": ("pmos", "FirstStageYout1", "in1", "FirstStageYsourceTransconductance", 14.21),
    "XNormalTransistorPmos8": ("pmos", "FirstStageYsourceTransconductance", "ibias", "sourcePmos", 90.63)}
P2, P5, P8 = "XDiodeTransistorPmos2", "XNormalTransistorPmos5", "XNormalTransistorPmos8"


def _lb_devices():
    return {n: {"type": t, "terminals": {"d": d, "g": g, "s": s, "b": s}, "W_um": w, "m": 1}
            for n, (t, d, g, s, w) in LB_DEV.items()}


def _lb_blocks():   # LOADBench's blocks before Phase A: upstream primitives through the name map
    def b(name, cat, prim, devs, inst):
        return {"name": name, "category": cat, "primitive": prim, "devices": devs, "source": "name_map",
                "upstream_instance": inst}
    return [b("undefined_common_source_stage", "gm-structure", "common-source-stage", [P5, "XNormalTransistorNmos3"], "X1"),
            b("p_differential_pair", "gm-structure", "pmos-differential-pair",
              ["XNormalTransistorPmos7", "XNormalTransistorPmos6"], "X2"),
            b("n_current_mirror_load", "load-structure", "nmos-current-mirror-load",
              ["XDiodeTransistorNmos1", "XNormalTransistorNmos4"], "X3"),
            b("p_current_mirror", "bias-structure", "pmos-current-mirror", [P2, P8], "X4"),
            b("p_current_mirror", "bias-structure", "pmos-current-mirror", [P2, P5], "X5")]


def test_mirror_bank_rule_merges_loadbench_pmos_mirrors():
    from src.s0.ingest import merge_mirror_banks
    blocks, notes = merge_mirror_banks(_lb_blocks(), _lb_devices())
    banks = [b for b in blocks if b["primitive"] == "pmos-current-mirror-bank"]
    assert len(banks) == 1 and banks[0]["devices"] == [P2, P8, P5] and banks[0]["gate_net"] == "ibias"
    assert banks[0]["ratio_Wm"] == {P2: 1.0, P8: pytest.approx(2.4298), P5: pytest.approx(23.781)}   # 1 : 2.43 : 23.8
    assert [m_["upstream_instance"] for m_ in banks[0]["merged_from"]] == ["X4", "X5"]
    assert [b["name"] for b in blocks][:3] == ["undefined_common_source_stage", "p_differential_pair", "n_current_mirror_load"]
    assert len({b["name"] for b in blocks}) == len(blocks) == 4 and len(notes) == 1   # names are unique now


def test_mirror_bank_rule_leaves_the_5t_unchanged():
    from src.s0.ingest import merge_mirror_banks
    ir = json.loads((REPO / "outputs" / "S0" / "example_ota_5t" / "circuit_ir.json").read_text())
    blocks, notes = merge_mirror_banks(ir["hierarchy"]["blocks"], {d["name"]: d for d in ir["devices"]})
    assert blocks == ir["hierarchy"]["blocks"] and notes == []


def test_designer_groups_agree_with_the_automatic_blocks():
    import yaml
    from src.s0.ingest import apply_designer_groups, merge_mirror_banks
    doc = yaml.safe_load((REPO / "inputs" / "loadbench_miller" / "designer_groups.yaml").read_text())
    auto, _ = merge_mirror_banks(_lb_blocks(), _lb_devices())
    blocks, rep = apply_designer_groups(auto, doc, _lb_devices())
    assert rep["agreement"] == "full" and not rep["automatic_blocks_replaced"] and rep["source"] == "designer review (Imasha)"
    assert [b["name"] for b in blocks] == ["cs_stage", "input_pair", "nmos_mirror_load", "pmos_bias_bank"]   # in place
    assert all(b["source"] == "designer" for b in blocks)
    assert blocks[-1]["devices"] == [P2, P8, P5] and blocks[-1]["primitive"] == "pmos-current-mirror-bank"
    assert blocks[0]["matching"] == "none" and doc["floorplan_rows"][0] == [P2, P8, P5]


def test_designer_group_wins_where_it_disagrees():
    from src.s0.ingest import apply_designer_groups
    doc = {"groups": [{"name": "bank", "kind": "mirror_bank", "devices": [P8, P5, P2]}]}
    blocks, rep = apply_designer_groups(_lb_blocks(), doc, _lb_devices())   # no bank rule: X4 and X5 disagree
    assert rep["agreement"] == "partial" and rep["automatic_blocks_replaced"] == ["p_current_mirror", "p_current_mirror"]
    assert [b["name"] for b in blocks] == ["undefined_common_source_stage", "p_differential_pair",
                                           "n_current_mirror_load", "bank"]   # the CS stage (another class) stays
    assert blocks[-1]["devices"][0] == P2                                    # the diode device first
    with pytest.raises(ValueError):
        apply_designer_groups(_lb_blocks(), {"groups": [{"name": "x", "kind": "mirror", "devices": ["XM9"]}]}, _lb_devices())


def test_dummies_tag_no_node():
    """Row 47: a dummy with d = g = s looked diode-connected, and dummies sharing a source net looked like a tail."""
    from src.s1.run import classify_nodes

    class LM:
        def dc_node_resistance(self):
            return {"bias": 1e3, "VSS": 1.0, "nx": 1e4, "ny": 1e4, "out": 1e5}

        def node_capacitance(self):
            return dict.fromkeys(("bias", "VSS", "nx", "ny", "out"), 1e-15)
    term = lambda d, g, s: {"d": d, "g": g, "s": s, "b": "VSS"}   # noqa: E731
    ir = {"ports": [{"name": "VSS", "role": "ground"}, {"name": "out", "role": "output"}], "internal_sources": [],
          "nets": [{"name": n} for n in ("bias", "VSS", "nx", "ny", "out")],
          "hierarchy": {"blocks": [{"name": "dummies", "category": "dummy", "primitive": "nmos-dummy",
                                    "devices": ["MD4", "MD5"]}]},
          "devices": [{"name": "M1", "terminals": term("bias", "bias", "VSS")},        # a real diode-connected device
                      {"name": "MD1", "terminals": term("VSS", "VSS", "VSS")},         # d = g = s
                      {"name": "MD2", "terminals": term("nx", "nx", "nx")},
                      {"name": "MD3", "terminals": term("nx", "nx", "nx")},
                      {"name": "MD4", "terminals": term("out", "VSS", "ny")},          # dummies by hierarchy role
                      {"name": "MD5", "terminals": term("out", "VSS", "ny")}]}
    res = classify_nodes(ir, LM())
    tags = {n: v["tags"] for n, v in res["nodes"].items()}
    assert "mirror_node (diode-connected)" in tags["bias"]
    assert not any("mirror_node" in t or "tail" in t for n in ("VSS", "nx", "ny") for t in tags[n])
    assert res["dummies_excluded_from_tags"] == ["MD1", "MD2", "MD3", "MD4", "MD5"]


def test_saturated_devices_and_specs_keep_the_plan_v2_rule():
    """Saturated devices and specs: u <= allowed + TOL_USE x eta x margin, i.e. plan v2's 1 % of the margin at eta 0.5."""
    from src.s3.run import use_check
    c = use_check(0.004, allowed=0.003, scale=0.2, eta=0.5)       # sat margin 0.2 V, allowance 3 mV
    assert c["ok"] == (0.004 <= 0.003 + 0.01 * 0.2) and "rule" not in c
    assert c["slack_frac_of_margin"] == pytest.approx((0.003 + 0.01 * 0.2 - 0.004) / 0.2)
    assert use_check(0.0, allowed=0.0, scale=None, eta=0.5) == {"ok": True, "slack_frac_of_margin": None}


# ------------------------------------------------------------------ step 6: one tolerance (Q3), fair scoring
def test_one_tolerance_for_every_use_check():
    import inspect
    import re as re_
    from src.common.tolerance import TOL_USE
    from src.s2 import baselines as BL
    from src.s3 import run as S3
    src = {p.relative_to(REPO).as_posix(): p.read_text() for p in (REPO / "src").rglob("*.py")}
    assert not [f for f, t in src.items() if "TOL_VERIFY" in t] and not hasattr(S3, "TOL")
    assert inspect.signature(BL.outcome).parameters["tol"].default == TOL_USE
    s2 = src["src/s2/run.py"]
    used = re_.findall(r"\(1 \+ (\w+)\)", s2)          # every '(1 + X)' tolerance in S2's use checks
    assert sorted(set(used)) == ["FIRST_ORDER_ERROR_REPORTED", "TOL_USE"] and used.count("TOL_USE") == 2
    assert [ln for ln in s2.splitlines() if "(1 + FIRST_ORDER_ERROR_REPORTED)" in ln][0].strip().startswith(
        '"within_first_order_error_10pct"')            # the 10 % survives as a reported column only
    assert BL.outcome({"spice_worst_use_of_allowed": 1.0 + TOL_USE * 0.9}) == "ok"
    assert BL.outcome({"spice_worst_use_of_allowed": 1.0 + TOL_USE * 1.1}) == "unsafe"


def test_lp_floor_k_has_ours_bounds_and_at_least_lp_floors_objective():
    """Imasha's choice (a), 2026-11-01: lp_floor_k is lp_floor with ours' cap, KAPPA x need. It is not >= lp_floor
    element by element: with more room the max-sum LP may starve an element (LOADBench: 13 of 40). Its objective
    is >= lp_floor's when every floor is at most its need, because lp_floor's bounds then lie inside lp_floor_k's."""
    from src.s2 import baselines as BL, budgets as B
    EL = [{"id": "e1", "w": 1.0}, {"id": "e2", "w": 1.0}]
    CO = [{"id": "gbw", "b": 3.0, "a": {"e1": 1.0, "e2": 2.0}}]   # one check; e2 costs twice as much margin
    obj = lambda x: sum(x.values())                               # noqa: E731  sum of budget / need (w = 1)
    xf, _ = BL.lp_floor(EL, CO)
    xk, _ = BL.lp_floor(EL, CO, upper=B.KAPPA)
    assert xf == pytest.approx({"e1": 1.0, "e2": 1.0})             # capped at need: both get their need
    assert xk == pytest.approx({"e1": 3.0, "e2": 0.0})             # ours' cap: e2 is starved, e1 gets 3 x need
    assert obj(xk) >= obj(xf) and all(-1e-9 <= v <= B.KAPPA + 1e-9 for v in xk.values())
    xk2, floored = BL.lp_floor(EL, CO, {"e2": 0.5}, upper=B.KAPPA)   # floors stay lower bounds, as for ours
    assert floored and xk2["e2"] == pytest.approx(0.5) and xk2["e1"] == pytest.approx(2.0)
    res = BL.run_all(EL, CO, {"e1": 1.0, "e2": 1.0})
    assert list(res) == ["per_net", "equal", "lp_sum", "lp_floor", "lp_floor_k", "ours"]
    assert res["lp_floor_k"]["score"]["floors_applied"] is True


# ------------------------------------------------------------------ step 7: PM reference phase (row 46)
POLE_HZ = 25.0          # TTSKY25a's dominant pole is at about 25 Hz


def test_pm_reference_is_the_1hz_phase_rounded_to_180_deg():
    import math
    import numpy as np
    from src.s1 import linear
    f = linear.FREQ
    for sign, ref in ((1, 0.0), (-1, 180.0)):                     # non-inverting and inverting output
        H = sign * 1e4 / (1 + 1j * f / POLE_HZ)
        m, p1 = linear.metrics(H), linear.phase_1hz(H)
        assert p1["pm_reference_deg"] == ref and p1["distance_deg"] == pytest.approx(-math.degrees(math.atan(1 / POLE_HZ)))
        assert m["pm_deg"] == pytest.approx(180 - math.degrees(math.atan(m["gbw_mhz"] * 1e6 / POLE_HZ)), abs=0.01)
        ph = np.degrees(np.unwrap(np.angle(H)))
        k = int(np.where(20 * np.log10(abs(H)) <= 0)[0][0])
        t = 20 * np.log10(abs(H[k - 1])) / (20 * np.log10(abs(H[k - 1])) - 20 * np.log10(abs(H[k])))
        pm_old = 180 + (ph[k - 1] + t * (ph[k] - ph[k - 1]) - ph[0])        # plan v2: minus the 1 Hz phase itself
        assert pm_old - m["pm_deg"] == pytest.approx(2.29, abs=0.01)       # the old formula reads ~2.3 deg high
    assert linear.pm_reference(179.9) == linear.pm_reference(-180.1) + 360 == 180.0
    assert linear.pm_reference(-89.0) == 0.0 and linear.pm_reference(-91.0) == -180.0


def test_fast_model_pm_change_uses_the_same_reference():
    import numpy as np
    from src.s1 import linear
    from tests.test_v2 import _ir
    ir, op = _ir()
    ir["passives"][2]["value"] = 1 / (2 * np.pi * 10e3 * POLE_HZ)     # Cx on o2: pole at 25 Hz
    drive = {"i1": 0.5, "i2": -0.5}
    fm = linear.FastModel(linear.LinearModel(ir, op, drive=drive))
    dc = 0.1e-6                                                     # pole 25 -> 21.6 Hz: the 1 Hz phase moves 0.36 deg
    d = fm.delta(*fm.cap_matrices("o2", None, dc))
    f = np.logspace(0, 9, 9 * 4000 + 1)
    H0 = linear.LinearModel(ir, op, drive=drive).response(f)
    H1 = linear.LinearModel(ir, op, drive=drive, extra_c=[("o2", None, dc)]).response(f)
    m0, m1 = linear.metrics(H0, f), linear.metrics(H1, f)
    assert d["pm_deg"] == pytest.approx(m1["pm_deg"] - m0["pm_deg"], abs=0.01)
    # one pole, same DC gain: the phase at the UGB stays at -atan(sqrt(24)), so PM does not change; plan v2's
    # delta also subtracted the 1 Hz phase's change, -0.36 deg, and read +0.36
    assert m0["pm_deg"] == pytest.approx(180 - np.degrees(np.arctan(np.sqrt(24))), abs=0.01)
    assert d["pm_deg"] == pytest.approx(0.0, abs=0.01)
    assert float(np.degrees(np.angle(H1[0] / H0[0]))) == pytest.approx(-0.36, abs=0.01)


def test_bench_template_pm_reference_in_ngspice(tmp_path):
    import shutil
    import subprocess
    import benchlib
    assert "let ph_ref  = 180 * floor(ph_dc / 180 + 0.5)" in benchlib.AC and "(ph_ugb - ph_ref)" in benchlib.AC
    if not shutil.which("ngspice"):
        pytest.skip("ngspice not on PATH (source scripts/env.sh)")
    for gain in ("1e4", "-1e4"):
        deck = tmp_path / "onepole.spice"
        deck.write_text(f"* one pole at 25 Hz\nVin in 0 dc 0 ac 1\nE1 a 0 in 0 {gain}\nR1 a out 1k\n"
                        f"C1 out 0 {1 / (2 * 3.141592653589793 * 1e3 * POLE_HZ):.7e}\n"
                        + benchlib.AC.format(sig="v(out)") + ".end\n")
        r = subprocess.run(["ngspice", "-b", deck.name], cwd=tmp_path, capture_output=True, text=True, timeout=60)
        pm = float(re.search(r"^MEAS pm_deg (\S+)", r.stdout, re.M).group(1))
        assert pm == pytest.approx(90.006, abs=0.005)               # the old bench formula gave 92.296


def test_frozen_benches_1hz_phase_is_near_a_multiple_of_180_deg():
    """The frozen benches (S0, S2, S3) keep the unrounded 1 Hz phase; the plan asks that it be < 0.01 deg from the
    rounded reference for the 5T and LOADBench (stop and ask above 0.05 deg)."""
    from src.s1 import linear
    for d in ("example_ota_5t", "loadbench_miller"):
        log = (REPO / "outputs" / "S0" / d / "tb" / "diso_amp_AC.log").read_text(errors="replace")
        p = float(re.search(r"^ph_dc\s*=\s*(\S+)", log, re.M).group(1))
        assert abs(p - linear.pm_reference(p)) < 0.01, (d, p)


# ------------------------------------------------------------------ step 8: route lengths (row 44; decision (b))
def _route(design):
    """S2's own path: as-sized problem -> library representatives -> route sizes -> problem with those routes."""
    from src.s1 import op as opmod
    from src.s2 import run as S2
    s0, s1 = REPO / "outputs" / "S0" / design, REPO / "outputs" / "S1" / design
    ir = json.loads((s0 / "circuit_ir.json").read_text())
    opmod.apply_passives(ir, json.loads((s1 / "operating_point.json").read_text()))
    pdk = json.loads((REPO / "outputs" / "S2" / "pdk" / "parasitics.json").read_text())
    sizes = S2.device_sizes(s0)
    els, _, _ = S2.build_problem(ir, s1, pdk, sizes, 0.5)
    lib = S2.library_floors(ir, els, json.loads((s1 / "sensitivity.json").read_text())["table"])
    sizes2, route = S2.route_sizes(ir, sizes, lib["representative_option"])
    els2, _, _ = S2.build_problem(ir, s1, pdk, sizes2, 0.5)
    return lib, route, {e["id"]: e for e in els2}, pdk["layers"]["metal1"]["res_ohm_per_um_at_min_width"]


def test_loadbench_route_lengths_drop_to_the_representative_cells():
    pytest.importorskip("klayout.db")
    lib, route, els, r1 = _route("loadbench_miller")
    for dev in ("XNormalTransistorNmos3", "XNormalTransistorPmos5"):        # N3 and P5: 484 and 887 um single fingers
        r = route[dev]
        tid, opt = r["route_from"].removeprefix("representative cell ").split("__")
        w, h = json.loads((REPO / "outputs/S3/_cells" / f"{tid}__{opt}" / "record.json").read_text())["geometry"]["bbox_um"]
        assert r["half_perimeter_um"] == pytest.approx((w + h) / 2)
        assert r["half_perimeter_um"] < 0.2 * r["half_perimeter_as_sized_um"]       # 244 -> 34 and 446 -> 61 um
        assert els[f"{dev}.g"]["w_parts"]["wiring"] == pytest.approx(r["half_perimeter_um"] * r1)   # the need moved
    assert route["Capacitor2"]["route_from"] == "as-sized PCell"              # no library cell: listed as such


def test_5t_route_lengths_change_little():
    pytest.importorskip("klayout.db")
    _, route, _, _ = _route("example_ota_5t")
    moved = {d: (r["half_perimeter_as_sized_um"], r["half_perimeter_um"]) for d, r in route.items()
             if abs(r["half_perimeter_um"] - r["half_perimeter_as_sized_um"]) > 0.05}
    assert set(moved) == {"XM5"} and moved["XM5"][1] == pytest.approx(9.06, abs=0.01)   # nf2 cell instead of nf1


def test_route_sizes_scales_m_copies_and_falls_back(monkeypatch):
    from src.s2 import run as S2
    from src.s3 import options as O
    tid, opt = "nfet_01v8_W1p4_L0p6_m18", "nf1_gboth_sdfull"           # a real record: unit bbox 2.45 x 3.39 um
    monkeypatch.setattr(O, "device_types", lambda ir: {tid: {"devices": ["D1"], "m": 4}, "T2": {"devices": ["D2"], "m": 1}})
    sizes = {"D1": {"w_um": 100.0, "h_um": 10.0}, "D2": {"w_um": 5.0, "h_um": 5.0}, "C1": {"w_um": 8.0, "h_um": 8.0}}
    out, route = S2.route_sizes({}, sizes, {tid: {"option": opt}})
    assert route["D1"]["half_perimeter_um"] == pytest.approx(2 * (2.45 + 3.39) / 2)   # sqrt(4) x the unit cell
    assert route["D1"]["half_perimeter_as_sized_um"] == 55.0
    assert route["D2"]["route_from"] == route["C1"]["route_from"] == "as-sized PCell" and out["D2"] == sizes["D2"]


def test_g20_is_rate_times_the_need_the_allocation_uses():
    """Replaces the plan's "'ours' budgets identical" (Imasha's choice (b)): the route is part of the need."""
    bj = json.loads((REPO / "outputs/S2/example_ota_5t/budgets.json").read_text())
    rep = json.loads((REPO / "outputs/S2/example_ota_5t/s2_report.json").read_text())["gates"]
    g20 = rep["G2.0_expected_layout_use (info)"]
    assert g20["route_lengths"]["XM5"]["route_from"].startswith("representative cell")
    w = {e["id"]: e["w"] for e in bj["elements"]}
    for e in bj["elements"]:
        assert e["w"] == pytest.approx(e["w_parts"]["wiring"] + e["w_parts"]["device_cells"])
        assert e["w_parts"]["wiring_as_sized_pcell"] is not None
    for cid, a in bj["rates"].items():
        use = g20["checks"][cid]
        assert use["use_at_expected_need"] == pytest.approx(sum(v * w[k] for k, v in a.items()))
        assert "fraction_of_margin_route_as_sized_pcell" in use


# ------------------------------------------------------------------ step 9: SPICE vs first order (row 42)
def test_agreement_fields_per_verified_check():
    from src.s2 import run as S2
    a = S2.agreement(pred=0.5, use=-0.16, allowed=0.5, margin=1.0)        # row 42: first order full, SPICE improves
    assert a["first_order_use_frac_of_allowed"] == pytest.approx(1.0)
    assert a["spice_use_frac_of_allowed"] == pytest.approx(-0.32)
    assert a["diff_frac_of_margin"] == pytest.approx(0.66) and a["sign_disagrees"] is True
    b = S2.agreement(pred=0.40, use=0.45, allowed=0.5, margin=1.0)
    assert b["diff_frac_of_margin"] == pytest.approx(0.05) and b["sign_disagrees"] is False
    c = S2.agreement(pred=0.40, use=None, allowed=0.5, margin=1.0)         # failed run: nothing to compare
    assert c["spice_use_frac_of_allowed"] is None and c["diff_frac_of_margin"] is None and c["sign_disagrees"] is False


def test_model_agreement_summary_on_fake_numbers():
    from src.s2 import run as S2
    row = lambda check, pred, use: {"check": check, **S2.agreement(pred, use, 0.5, 1.0)}   # noqa: E731
    g25 = [row("gain_db", 0.48, 0.49), row("gbw_mhz", 0.50, -0.16), row("pm_deg", 0.10, 0.40)]
    srcs = {"G2.5 iteration 0": g25, "G2.8 equal": [row("gain_db", 0.2, 0.21), row("pm_deg", 0.3, None)]}
    pvt = {"use_of_allowed": {"tt_v0.9_t27": {"gbw_mhz": 7.8, "gain_db": "spec not met before layout"},
                              "ss_v1_t27": {"gbw_mhz": 0.4, "gain_db": 0.9}}}
    g = S2.model_agreement(srcs, g25, pvt)
    assert g["pass"] is None and g["flag_diff_frac_of_margin"] == 0.25 and "ASSUMPTION" in g["flag_note"]
    assert g["checks_compared"] == 4                                        # the failed run is not compared
    assert [(f["source"], f["check"]) for f in g["flagged"]] == [("G2.5 iteration 0", "gbw_mhz"),   # sign
                                                                ("G2.5 iteration 0", "pm_deg")]    # 0.30 > 0.25
    w = g["pvt_worst_points"]
    assert w["gbw_mhz"]["point"] == "tt_v0.9_t27" and w["gbw_mhz"]["first_order_use_of_allowed"] == 7.8
    assert "differs" in w["gbw_mhz"]["note"]                               # nominal -0.32 in SPICE, corner 7.8 first order
    assert w["gain_db"]["point"] == "ss_v1_t27" and "note" not in w["gain_db"]   # 0.9 <= 1: no note
    assert "pvt_worst_points" not in S2.model_agreement(srcs, g25, None)


# ------------------------------------------------------------------ step 10: LOADBench hand model + mirror doublet
LB_EQ = "circuits/loadbench_miller/upstream/equations.predicted.json"


def test_miller_patch_builds_a_labelled_copy_with_the_doublet():
    from src.common.tools import sha256
    from src.s1 import symbolic_patch_miller as M
    orig = json.loads((REPO / LB_EQ).read_text())
    p = M.build_patched(orig, LB_EQ, 1.1e-12)
    assert p["provenance"] == p["patch"]["status"].split(":")[0] == "PREDICTED (patched, post hoc)"
    assert p["patch"]["based_on"] == {"file": LB_EQ, "sha256": sha256(REPO / LB_EQ)}
    assert p["performance_original"] == orig["performance"] and orig["provenance"] == "PREDICTED"   # original untouched
    t = p["performance"]["terms"]
    assert list(t)[-1] == "wu" and t["wu0"] == orig["performance"]["terms"]["wu"]   # resolved after its inputs
    assert t["tau_z"] == "tau_m/2" and t["C_m"].startswith("C4_XDiodeTransistorNmos1 + ")
    assert p["performance"]["gain_db"] == orig["performance"]["gain_db"]             # Gm(0) = gm1: DC gain unchanged
    assert "atan(wu*tau_m) - atan(wu*tau_z)" in p["performance"]["pm_deg"]


def test_miller_exact_rational_doublet_costs_phase():
    from src.s1 import symbolic_patch_miller as M
    t = {"R1o": 1e6, "R2o": 1e5, "gm1": 1e-4, "gm2": 1e-3, "Cc": 1e-12, "C1n": 1e-13, "C2n": 1e-12}
    a, b = M.exact(t, None), M.exact(t, 5e-9)          # gm1/Cc = 1e8 rad/s (~16 MHz); doublet pole ~32 MHz
    assert a["gbw_mhz"] > b["gbw_mhz"] and a["pm_deg"] - b["pm_deg"] > 5


def test_loadbench_hand_pm_gap_closes_and_the_original_is_unchanged():
    d = json.loads((REPO / "outputs/S1/loadbench_miller/symbolic_patch_check.json").read_text())
    g15 = json.loads((REPO / "outputs/S1/loadbench_miller/s1_report.json").read_text())["gates"][
        "G1.5_symbolic_vs_spice (reported, not gated)"]
    orig, p1, spice = d["models"]["original"], d["models"]["P1"], d["spice"]
    assert orig["predicted"] == pytest.approx(g15["predicted"])                       # the unpatched file, as in G1.5
    assert abs(orig["error_vs_spice"]["pm_deg"]) == pytest.approx(17.02, abs=0.05)    # the 17 deg gap of row 49
    assert abs(p1["error_vs_spice"]["pm_deg"]) < 3.0                                   # recorded: 1.67 deg
    assert abs(d["exact_checks"]["P1_exact_rational"]["pm_deg"] - spice["pm_deg"]) < 3.0   # recorded: 2.95 deg
    assert p1["predicted"]["gain_db"] == pytest.approx(orig["predicted"]["gain_db"])
    assert d["mirror_node"]["pole_mhz"] == pytest.approx(33.2, abs=0.5)                # the plan's "about 33 MHz"
    assert d["mirror_node"]["g_S"] == pytest.approx(d["mirror_node"]["g_linear_model_S"], rel=1e-6)
    assert orig["per_fF"]["FirstStageYout1"]["pm_deg"] == 0.0 < -p1["per_fF"]["FirstStageYout1"]["pm_deg"]
    assert d["label"] == "PREDICTED (patched, post hoc)" and not p1["unresolved_symbols"]
    assert g15["pass"] is None                                                          # G1.5 stays report-only
    assert not list((REPO / "circuits").rglob("*.P1.json"))                             # nothing written into circuits/


def test_s2_does_not_read_hand_models():
    """S2 budgets come from the SPICE-linearised model (S1 sensitivities): no hand model reaches them."""
    for f in (REPO / "src" / "s2").glob("*.py"):
        t = f.read_text()
        assert "symbolic" not in t and "upstream_patched" not in t and "equations" not in t, f.name


# ------------------------------------------------------------------ step 12: a budget at its floor is not below it
def test_budget_at_its_floor_or_need_is_not_below_it():
    """LOADBench, step 12: phase 2 left ibias~out at 20.38719997961 = floor 20.3872 x (1 - 1e-9) - rounding, and a 1e-9
    test scored ours 'infeasible'. AT_BOUND_TOL is wider than refine's 1e-9 room."""
    from src.s2 import baselines as BL
    EL = [{"id": "a", "w": 22.3567}, {"id": "b", "w": 1.0}]
    CO = [{"id": "pm_deg", "b": 100.0, "a": {"a": 1.0, "b": 1.0}}]
    fl = {"a": 20.3872}
    at = BL.score({"a": 20.3871999796128, "b": 1.0 * (1 - 1e-9)}, EL, CO, fl)
    assert at["below_floor"] == [] and at["starved"] == ["a"]           # a is below its need (22.36), b is at it
    assert BL.outcome(at) == "ok"
    below = BL.score({"a": 20.3872 * (1 - 1e-5), "b": 1.0 * (1 - 1e-5)}, EL, CO, fl)
    assert below["below_floor"] == ["a"] and below["starved"] == ["a", "b"] and BL.outcome(below) == "infeasible"
    assert 1e-9 < BL.AT_BOUND_TOL <= 1e-6


# ------------------------------------------------------------------ after review D 1: G2.8 checks PVT points again
def test_top_corner_checks_picks_each_sets_most_used_points():
    from src.s2 import run as S2
    pool = [{"id": f"gbw_mhz@p{i}", "b": 1.0, "margin": 2.0 + i, "a": {"e": float(i)}} for i in range(8)]
    pick = S2.top_corner_checks(pool, [{"e": 1.0}], set(), n=3)
    assert [c["id"] for c in pick] == ["gbw_mhz@p5", "gbw_mhz@p6", "gbw_mhz@p7"]     # the 3 most used, first order
    pick_b = S2.top_corner_checks(pool, [{"e": 1.0}], {"gbw_mhz@p0"}, n=2)
    assert {c["id"] for c in pick_b} == {"gbw_mhz@p0", "gbw_mhz@p6", "gbw_mhz@p7"}  # binding corners always kept
    assert S2.top_corner_checks([], [{"e": 1.0}], set()) == []


def test_g25_keeps_budgeted_corners_and_g28_uses_the_pvt_pool():
    """G2.5's closure acts on every check it runs, so it may only see budgeted corners; G2.8 is scored at G2.9's PVT
    points as well when budgets are nominal (Imasha, 2026-11-02, after review D 1)."""
    t = (REPO / "src" / "s2" / "run.py").read_text()
    assert "checks = nom_cons + top_corner_checks(corner_cons, [xv], binding_corners)" in t
    assert "top_corner_checks(g28_pool, [v_[\"budgets\"]], binding_corners)" in t
    assert 'pvt_info["constraints"] if pvt_info is not None and budget_corners == "nominal"' in t


# ------------------------------------------------------------------ review branch: env.sh under `set -u` (row 62)
def test_env_sh_works_for_callers_with_nounset():
    """magic_drc.sh and magic_lvs.sh run with `set -uo pipefail` and source env.sh; the image's sak-pdk script reads
    unset variables, which stopped them before Magic ran (S0 G0.7 then had no DRC/LVS result for any device)."""
    import shutil
    import subprocess
    if not shutil.which("bash") or not (Path("/foss/tools/sak/sak-pdk-script.sh")).exists():
        pytest.skip("needs the layout-s0s3 container")
    r = subprocess.run(["bash", "-c", f"set -uo pipefail; . {REPO}/scripts/env.sh; echo PDK=$PDK; "
                                      "case $- in *u*) echo NOUNSET_KEPT;; esac"], capture_output=True, text=True)
    assert r.returncode == 0 and "PDK=sky130A" in r.stdout and "NOUNSET_KEPT" in r.stdout, r.stderr


def test_magic_drc_script_runs_on_a_committed_pcell(tmp_path):
    import shutil
    from src.common import pcell
    if not shutil.which("magic", path="/foss/tools/bin:/usr/bin"):
        pytest.skip("needs Magic (layout-s0s3 container)")
    r = pcell.drc(REPO / "outputs/S0/example_ota_5t/pcell/XM1.gds", "XM1", tmp_path / "drc")
    assert r["errors"] == 0 and r["neg_control_flagged"] and r["pass"], r   # Magic ran, and its control was caught


# ------------------------------------------------------------------ review phase 2: robustness
def test_write_text_retries_errno22_only(tmp_path, monkeypatch):
    import errno
    from src.common import tools
    monkeypatch.setattr(tools.time, "sleep", lambda s: None)
    real, calls = Path.write_text, {"n": 0}

    def flaky(self, text, *a, **k):                       # Errno 22 twice, then a normal write
        calls["n"] += 1
        if calls["n"] <= 2:
            raise OSError(errno.EINVAL, "Invalid argument")
        return real(self, text, *a, **k)
    monkeypatch.setattr(Path, "write_text", flaky)
    tools.write_json(tmp_path / "a.json", {"x": 1})
    assert calls["n"] == 3 and json.loads((tmp_path / "a.json").read_text()) == {"x": 1}

    def denied(self, text, *a, **k):                      # any other error is raised at once
        raise PermissionError(errno.EACCES, "denied")
    monkeypatch.setattr(Path, "write_text", denied)
    with pytest.raises(PermissionError):
        tools.write_text(tmp_path / "b.txt", "x")


def test_env_sh_cleans_a_user_name_with_a_newline():
    """The image's login profile sets USER to "1000\ndesigner"; pytest's temp folder then has a newline in its name
    and Netgen fails the S0 round-trip test (row 55)."""
    import shutil
    import subprocess
    if not shutil.which("bash") or not Path("/foss/tools/sak/sak-pdk-script.sh").exists():
        pytest.skip("needs the layout-s0s3 container")
    r = subprocess.run(["bash", "-c", f"export USER=$(printf '1000\ndesigner'); . {REPO}/scripts/env.sh; "
                                      "printf '[%s]' \"$USER\""], capture_output=True, text=True)
    assert r.stdout == "[designer]", (r.stdout, r.stderr)
    r = subprocess.run(["bash", "-c", f"set -u; unset USER; . {REPO}/scripts/env.sh; echo ok"], capture_output=True, text=True)
    assert r.stdout.strip() == "ok", r.stderr


# ------------------------------------------------------------------ review phase 4: S0-S3 walkthrough
def test_walkthrough_reads_both_shapes_of_g06():
    """G0.6 keeps the schematic's values under `compare` (upstream run, the 5T) or `measured` (no upstream, LOADBench);
    the first walkthrough read `measured` only and left the 5T's G3.3 schematic column empty."""
    import make_s0s3_walkthrough as W
    assert W.schematic_values({"measured": {"gain_db": 58.0}}) == {"gain_db": 58.0}
    assert W.schematic_values({"compare": {"gain_db": {"upstream": 31.7, "rerun": 31.697, "ok": True}}}) == {"gain_db": 31.697}
    assert W.schematic_values({}) == {}


def test_walkthrough_covers_both_designs_and_explains_every_failed_gate(tmp_path):
    """Read from outputs/ only: each design gets a section with its stage statuses, every failed gate gets an
    explanation (not the generic line), and no G3.3 row has an empty schematic value."""
    import make_s0s3_walkthrough as W
    designs = ["example_ota_5t", "loadbench_miller"]
    if not all((REPO / "outputs/flow" / d / "flow_summary.json").exists() for d in designs):
        pytest.skip("needs the S0-S3 outputs of both designs")
    out = tmp_path / "w.md"
    assert W.main(designs + ["--no-html", "--out", str(out)]) == 0
    md = out.read_text()
    for d in designs:
        sec = md.split(f"\n## {d}\n", 1)[1].split("\n## ", 1)[0]
        st = json.loads((REPO / "outputs/flow" / d / "flow_summary.json").read_text())["stages"]
        assert f"| {d} | " + " | ".join(st[s]["status"] for s in ("S0", "S1", "S2", "S3")) + " |" in md
        for s in ("S0", "S1", "S2", "S3"):
            assert f"\n### {s}\n" in sec
            gates = json.loads((REPO / f"outputs/{s}/{d}/{s.lower()}_report.json").read_text())["gates"]
            for g, v in gates.items():
                if v.get("pass") is False:
                    assert f"- **{g.split('_')[0]} (" in sec, (d, g)
        mode = json.loads((REPO / f"outputs/S3/{d}/device_decisions.json").read_text())["mode"]   # S3's own total
        s3_area = gates["G3.7_modes (info)"]["summary"][mode]["total_area_um2"]                   # (every device)
        m = re.search(r"Total device area \(every device counted\): ([0-9.e+]+) µm²", sec)
        assert m and float(m.group(1)) == pytest.approx(s3_area, rel=1e-3), (d, m and m.group(1), s3_area)
        for s in ("S0", "S1", "S2", "S3"):     # every stage explains its tables and plots
            stage = sec.split(f"\n### {s}\n", 1)[1].split("\n### ", 1)[0]
            assert stage.count("> **How to read it.**") >= 2, (d, s)
        assert "**In short** (built from the reports):" in sec and "- **Devices (S3):**" in sec
        assert "**What it shows here:** with every chosen cell in place, the circuit" in sec
    assert md.count("\n## How to read this page\n") == 1
    rows =[r for r in md.splitlines() if re.fullmatch(r"\| (gain_db|gbw_mhz|pm_deg|power_uw) \|[^|]+\|[^|]+\| (yes|\*\*no\*\*) \|", r)]
    assert rows and not any("| – |" in r for r in rows)


# ------------------------------------------------------------------ after the review: S3 option plot, line endings
@pytest.mark.parametrize("d", ["example_ota_5t", "loadbench_miller"])
def test_s3_chooses_a_filled_option_and_none_smaller_fits(d, tmp_path):
    """The option plot fills the main mode's options and leaves the other modes hollow (row 65). What S3 chose is a
    filled option, and no filled option that fits is smaller than it by more than the 2 % area tie."""
    from src.s3 import options as O
    from src.s3.run import AREA_TIE, plot_option_space
    s3 = REPO / "outputs/S3" / d
    if not (s3 / "option_table.json").exists():
        pytest.skip("needs the committed S3 outputs")
    types = O.device_types(json.loads((REPO / "outputs/S0" / d / "circuit_ir.json").read_text()))
    table = json.loads((s3 / "option_table.json").read_text())["options"]
    dd = json.loads((s3 / "device_decisions.json").read_text())
    for tid, v in dd["decisions"].items():
        main = [r for r in table if r["type"] == tid and r.get("min_slack") is not None
                and O.in_mode(types[tid], r["option"], dd["mode"])]
        chosen = next(r for r in table if r["cell"] == v["cell"])
        assert chosen in main, tid
        fits = [r["geometry"]["area_um2"] for r in main if r["feasible"]]
        assert v["relaxed"] == (not fits), tid
        if fits:
            assert chosen["geometry"]["area_um2"] <= min(fits) * (1 + AREA_TIE) + 1e-9, tid
    plot_option_space(tmp_path / "o.png", table, types, dd["decisions"], dd["mode"])
    assert (tmp_path / "o.png").stat().st_size > 10_000


def test_shell_files_have_lf_line_endings():
    """bash cannot parse CRLF. A Windows checkout with core.autocrlf=true wrote it into scripts/env.sh, which every
    flow command sources (row 66); .gitattributes now checks text out with LF."""
    files = [REPO / "flow", *sorted((REPO / "scripts").glob("*.sh")), *sorted((REPO / "src").rglob("*.sh"))]
    bad = [str(p.relative_to(REPO)) for p in files if b"\r" in p.read_bytes()]
    assert not bad, bad
    assert "* text=auto eol=lf" in (REPO / ".gitattributes").read_text()


def test_status_time_comes_from_the_report_not_the_file(tmp_path):
    """A checkout rewrote every report file, so `flow status` showed the checkout's time for every stage (row 66).
    It now shows the report's own provenance time, on the local clock, and the file time only without one."""
    import datetime as dt_
    rp = tmp_path / "r.json"
    rp.write_text("{}")
    created = "2026-11-02T18:45:01+00:00"
    want = dt_.datetime.fromisoformat(created).astimezone().strftime("%Y-%m-%dT%H:%M")
    assert flow.report_time({"provenance": {"created": created}}, rp) == want
    assert flow.report_time({}, rp) == dt_.datetime.fromtimestamp(rp.stat().st_mtime).strftime("%Y-%m-%dT%H:%M")
