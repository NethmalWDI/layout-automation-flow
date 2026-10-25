"""S0 integration tests that need the EDA tools (run inside layout-s0s3).
The LVS checker must catch a wiring change: a checker that always says 'match' would be useless.
"""
import shutil
from pathlib import Path

import pytest

from src.common import spice
from src.common.tools import TOOL_ENV, run_netgen_compare
from src.s0 import ingest

REPO = Path(__file__).resolve().parents[1]
NETLIST = REPO / "circuits/example_ota_5t/source/example_ota_5t_sized.spice"
needs_netgen = pytest.mark.skipif(shutil.which("netgen", path=TOOL_ENV["PATH"]) is None, reason="netgen not available")


@needs_netgen
def test_round_trip_matches(tmp_path):
    nl = spice.parse(NETLIST)
    (tmp_path / "full.spice").write_text(ingest.write_full(nl, "dut"))
    ingest.wrap_original(NETLIST, tmp_path / "orig.spice", nl.name)
    r = run_netgen_compare(tmp_path / "full.spice", "dut", tmp_path / "orig.spice", nl.name, tmp_path / "lvs.txt")
    assert r["pass"], r


@needs_netgen
def test_round_trip_detects_rewiring(tmp_path):
    nl = spice.parse(NETLIST)
    bad = ingest.write_full(nl, "dut").replace("XM4 OUTP net3 VDD VDD", "XM4 OUTP INP VDD VDD")
    (tmp_path / "bad.spice").write_text(bad)
    ingest.wrap_original(NETLIST, tmp_path / "orig.spice", nl.name)
    r = run_netgen_compare(tmp_path / "bad.spice", "dut", tmp_path / "orig.spice", nl.name, tmp_path / "lvs.txt")
    assert not r["pass"], r


@needs_netgen
def test_round_trip_detects_size_change(tmp_path):
    nl = spice.parse(NETLIST)
    bad = ingest.write_full(nl, "dut").replace("L=0.5 W=24", "L=0.5 W=20", 1)
    (tmp_path / "bad.spice").write_text(bad)
    ingest.wrap_original(NETLIST, tmp_path / "orig.spice", nl.name)
    r = run_netgen_compare(tmp_path / "bad.spice", "dut", tmp_path / "orig.spice", nl.name, tmp_path / "lvs.txt")
    assert not r["pass"], r
