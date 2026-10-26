"""Golden-reference regression on the committed outputs (no simulation is run here).

Each snapshot in tests/golden/<design>/<stage>.json must match outputs/<stage>/<design>/ within its
tolerances. To re-run a stage first and then compare: `python3 -m src.flow test --stage S2 --rerun`.
"""
import pytest

from src import golden

CASES = [(d, s) for d in golden.designs_with_snapshots() for s in ("S0", "S1", "S2", "S3")
         if golden.snapshot_path(d, s).exists()]


@pytest.mark.parametrize("design,stage", CASES)
def test_outputs_match_golden(design, stage):
    diffs = golden.compare(design, stage)
    assert not diffs, f"{design} {stage}: " + "; ".join(diffs[:10])


def test_compare_detects_a_change(tmp_path, monkeypatch):
    """The comparison itself must fail on a moved number (negative control)."""
    import json
    snap = tmp_path / "golden" / "d" / "S2.json"
    snap.parent.mkdir(parents=True)
    snap.write_text(json.dumps({"rtol": 1e-3, "values": {"budget.OUTP": 4.0, "gate.G2.3_allocation": True}}))
    monkeypatch.setattr(golden, "GOLDEN", tmp_path / "golden")
    monkeypatch.setattr(golden, "extract", lambda d, s: {"budget.OUTP": 4.1, "gate.G2.3_allocation": True})
    assert golden.compare("d", "S2") == ["budget.OUTP: 4 -> 4.1"]
    monkeypatch.setattr(golden, "extract", lambda d, s: {"budget.OUTP": 4.001, "gate.G2.3_allocation": True})
    assert golden.compare("d", "S2") == []
