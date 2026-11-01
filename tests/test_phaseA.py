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
