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
