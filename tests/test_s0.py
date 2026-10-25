"""S0 tests: parser, validation (positive and negative), name map, layout view.
Run inside layout-s0s3 from /foss/designs:  python3 -m pytest -q tests/test_s0.py
"""
from pathlib import Path

import pytest

from src.common import spice
from src.s0 import ingest

REPO = Path(__file__).resolve().parents[1]
NETLIST = REPO / "circuits/example_ota_5t/source/example_ota_5t_sized.spice"
PKG = REPO / "inputs/example_ota_5t/package.yaml"

GOOD = """**.subckt t VDD OUT IN VSS
*.ipin IN
XM1 OUT IN VSS VSS sky130_fd_pr__nfet_01v8 L=0.5 W=2 nf=1 mult=1
XM2 OUT OUT VDD VDD sky130_fd_pr__pfet_01v8 L=0.5 W=2 nf=1 mult=1
**.ends
"""


def _write(tmp_path, text):
    f = tmp_path / "n.spice"
    f.write_text(text)
    return f


def test_inventory_of_real_design():
    nl = spice.parse(NETLIST)
    assert nl.name == "example_ota_5t_sized"
    assert nl.ports == ["VDD", "OUTP", "INP", "INN", "VSS"]
    assert sorted(m.name for m in nl.mosfets) == ["XM1", "XM2", "XM3", "XM4", "XM5"]
    assert [s.name for s in nl.sources] == ["V1"]
    assert nl.port_dirs["INP"] == "input" and nl.port_dirs["OUTP"] == "output"
    m1 = {m.name: m for m in nl.mosfets}["XM1"]
    assert (m1.num("W"), m1.num("L"), m1.num("NF")) == (24.0, 0.5, 1.0)


def test_real_design_validates():
    assert spice.validate(spice.parse(NETLIST), ingest.ALLOWED_MODELS) == []


def test_good_small_netlist(tmp_path):
    assert spice.validate(spice.parse(_write(tmp_path, GOOD)), ingest.ALLOWED_MODELS) == []


def test_reject_unknown_model(tmp_path):
    bad = GOOD.replace("sky130_fd_pr__nfet_01v8", "sky130_fd_pr__nfet_g5v0d10v5")
    errs = spice.validate(spice.parse(_write(tmp_path, bad)), ingest.ALLOWED_MODELS)
    assert any("not in allowed set" in e for e in errs)


def test_reject_missing_width(tmp_path):
    bad = GOOD.replace(" W=2 nf=1 mult=1\nXM2", " nf=1 mult=1\nXM2")
    errs = spice.validate(spice.parse(_write(tmp_path, bad)), ingest.ALLOWED_MODELS)
    assert any("W missing" in e for e in errs)


def test_reject_dangling_net(tmp_path):
    bad = GOOD.replace("XM1 OUT IN VSS VSS", "XM1 OUT IN floating VSS")
    errs = spice.validate(spice.parse(_write(tmp_path, bad)), ingest.ALLOWED_MODELS)
    assert any("dangling" in e for e in errs)


def test_reject_duplicate_name(tmp_path):
    bad = GOOD.replace("XM2 OUT OUT", "XM1 OUT OUT")
    errs = spice.validate(spice.parse(_write(tmp_path, bad)), ingest.ALLOWED_MODELS)
    assert any("duplicate" in e for e in errs)


def test_reject_unsupported_element(tmp_path):
    bad = GOOD.replace("**.ends", "E1 OUT 0 IN 0 10\n**.ends")
    with pytest.raises(spice.SpiceError):
        spice.parse(_write(tmp_path, bad))


def test_name_map_consistent():
    pkg = ingest.load_package(PKG)
    blocks, findings, _ = ingest.map_hierarchy(pkg, spice.parse(NETLIST))
    assert not [f for f in findings if f["level"] == "error"], findings
    by = {b["name"]: b for b in blocks}
    assert sorted(by["nmos_differential_pair"]["devices"]) == ["XM1", "XM2"]
    assert sorted(by["pmos_current_mirror_load"]["devices"]) == ["XM3", "XM4"]
    assert by["nmos_current_mirror_bias"]["devices"] == ["XM5"]
    assert any(f["level"] == "manual" for f in findings)  # tail gate / missing XM6 flagged, not hidden


def test_name_map_catches_wrong_mapping(tmp_path):
    import yaml
    pkg = ingest.load_package(PKG)
    nm = yaml.safe_load((REPO / pkg["upstream"]["name_map"]).read_text())
    nm["devices"]["XM3"], nm["devices"]["XM4"] = "XM2", "XM1"   # swap the pair: drains no longer match
    f = tmp_path / "nm.yaml"
    f.write_text(yaml.safe_dump(nm))
    pkg["upstream"] = dict(pkg["upstream"], name_map=str(f))
    _, findings, _ = ingest.map_hierarchy(pkg, spice.parse(NETLIST))
    assert any(x["level"] == "error" for x in findings)


def test_layout_view_exposes_bias_port():
    txt, unhandled = ingest.write_layout(spice.parse(NETLIST), "x", {"V1": "VBIAS"})
    assert ".subckt x VDD OUTP INP INN VSS VBIAS" in txt
    assert "V1" not in txt and "net2" not in txt and unhandled == []
    assert "XM5 net1 VBIAS VSS VSS" in txt
