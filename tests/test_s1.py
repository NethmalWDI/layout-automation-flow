"""S1 unit tests that need no simulator: linear-model stamps, metric definitions, deck editing,
charge-matrix convention check and the upstream symbol mapping."""
import math
from pathlib import Path

import numpy as np
import pytest

from src.s1 import linear, op as opmod, spice_fd, symbolic

CAPS = [k for k in linear.CMAT.values()] + ["cgso", "cgdo", "cgbo", "capbd", "capbs"]


def cs_amp(gm=1e-3, gds=1e-5, cl="1p", cgdo=0.0):
    """Common-source NMOS: IN -> gate, OUT -> drain, source/bulk on VSS."""
    ir = {"ports": [{"name": "VDD", "role": "supply"}, {"name": "OUT", "role": "output"},
                    {"name": "IN", "role": "input"}, {"name": "VSS", "role": "ground"}],
          "nets": [{"name": n} for n in ("VDD", "OUT", "IN", "VSS")],
          "devices": [{"name": "M1", "terminals": {"d": "OUT", "g": "IN", "s": "VSS", "b": "VSS"}}],
          "internal_sources": [], "conditions": {"CL_F": cl}}
    o = {k: 0.0 for k in CAPS}
    o.update({"gm": gm, "gds": gds, "gmbs": 0.0, "cgdo": cgdo})
    return ir, {"M1": o}


def test_dc_gain_and_pole_of_common_source():
    ir, op = cs_amp()
    lm = linear.LinearModel(ir, op, drive={"IN": 1.0})
    H = lm.response(np.array([1.0, 1e3]))
    assert H[0].real == pytest.approx(-100.0, rel=1e-6)          # -gm/gds
    assert lm.dc_node_resistance()["OUT"] == pytest.approx(1e5)  # 1/gds
    assert lm.node_capacitance()["OUT"] == pytest.approx(1e-12)  # CL


def test_one_pole_metrics_match_textbook():
    ir, op = cs_amp()
    lm = linear.LinearModel(ir, op, drive={"IN": 1.0})
    m = linear.metrics(lm.response(linear.FREQ))
    assert m["gain_db"] == pytest.approx(40.0, abs=1e-6)
    # unity-gain frequency of A0/(1+s/wp): wp*sqrt(A0^2-1)
    fu = 1e-5 / (2 * math.pi * 1e-12) * math.sqrt(100 ** 2 - 1)
    assert m["gbw_mhz"] == pytest.approx(fu / 1e6, rel=2e-3)     # linear interpolation on dec-40 grid
    assert m["pm_deg"] == pytest.approx(180 - math.degrees(math.atan(math.sqrt(100 ** 2 - 1))), abs=0.05)


def test_feedforward_cap_creates_rhp_zero_and_reduces_pm():
    ir, op = cs_amp()
    base = linear.metrics(linear.LinearModel(ir, op, drive={"IN": 1.0}).response(linear.FREQ))
    ir2, op2 = cs_amp(cgdo=50e-15)
    m2 = linear.metrics(linear.LinearModel(ir2, op2, drive={"IN": 1.0}).response(linear.FREQ))
    assert m2["pm_deg"] < base["pm_deg"]


def test_extra_cap_to_ground_lowers_gbw():
    ir, op = cs_amp()
    s = linear.sensitivities(ir, op, ["OUT"], [])
    assert s["per_fF"]["OUT"]["gbw_mhz"] < 0
    assert s["per_fF"]["OUT"]["gain_db"] == pytest.approx(0.0, abs=1e-9)


def test_cap_convention_detects_derivative_form():
    good = {f"c{i}{j}": 0.0 for i in "gdsb" for j in "gdsb"}
    good.update({"cgg": 3.0, "cgs": -2.0, "cgd": -1.0, "csg": -2.0, "css": 2.0, "cdg": -1.0, "cdd": 1.0})
    assert opmod.cap_convention(good)["derivative_convention"]
    bad = dict(good, cgs=2.0, cgd=1.0)  # "positive capacitance" form does not sum to zero
    assert not opmod.cap_convention(bad)["derivative_convention"]


def test_deck_with_cap_inserts_inside_dut_only(tmp_path: Path):
    deck = tmp_path / "ac.spice"
    deck.write_text(".subckt other A B\nR1 A B 1k\n.ends\n.subckt dut X Y VSS\nM1 X Y VSS VSS n\n.ends\n")
    txt = spice_fd.deck_with_cap(deck, "dut", "X", None, 5.0)
    assert ".subckt dut X Y VSS\nCpar_s1 X VSS 5.0f\n" in txt
    assert txt.count("Cpar_s1") == 1
    with pytest.raises(RuntimeError):
        spice_fd.deck_with_cap(deck, "missing", "X", None, 5.0)


def test_level0_symbols_follow_name_map():
    op = {"XM3": {"cgb": -1e-15, "cgbo": 1e-16, "cgs": -2e-15, "cgso": 2e-16, "cgd": -3e-18, "cgdo": 3e-16,
                  "capbd": 4e-15, "cbd": -1e-16, "capbs": 5e-15, "cbs": -2e-16, "gm": 1e-3, "gmbs": 2e-4, "gds": 1e-5}}
    vals = symbolic.level0_values(op, {"devices": {"XM1": "XM3", "XM6": None}})
    assert vals["G1_XM1"] == 1e-3 and vals["R1_XM1"] == pytest.approx(1e5)
    assert vals["C3_XM1"] == pytest.approx(3e-18 + 3e-16)
    assert not any(k.endswith("_XM6") for k in vals)


def test_series_resistor_tends_to_no_resistor():
    ir, op = cs_amp()
    base = linear.LinearModel(ir, op, drive={"IN": 1.0}).response(np.array([1e6]))
    tiny = linear.LinearModel(ir, op, drive={"IN": 1.0}, extra_r=[("M1", "g", 1e-6)]).response(np.array([1e6]))
    assert abs(tiny[0] - base[0]) / abs(base[0]) < 1e-6


def test_gate_resistor_and_gate_capacitance_form_a_pole():
    # gm = gds = 1 mS, CL = 1 pF: output pole at 1/(2*pi*1k*1p); a 1 kOhm gate resistor into a 1 pF
    # gate-source capacitance gives a second pole at the same frequency -> |H| halves there.
    ir, op = cs_amp(gm=1e-3, gds=1e-3, cl="1p")
    o = op["M1"]
    o.update({"cgg": 1e-12, "cgs": -1e-12, "css": 1e-12, "csg": -1e-12})
    fp = 1 / (2 * math.pi * 1e3 * 1e-12)
    lm = linear.LinearModel(ir, op, drive={"IN": 1.0}, extra_r=[("M1", "g", 1e3)])
    H = lm.response(np.array([1.0, fp]))
    assert abs(H[1]) / abs(H[0]) == pytest.approx(0.5, rel=1e-3)


def test_deck_with_res_rewires_only_the_dut_terminal():
    from src.s1 import resistance
    deck = "x1 a b dut\n.subckt dut D G S\nXM1 D G S S sky130_fd_pr__nfet_01v8 L=1 W=2\n.ends\nXM1 q r s t other\n"
    out = resistance.deck_with_res(deck, "dut", "XM1", "s", 50)
    assert "XM1 D G s1r_XM1_s S sky130_fd_pr__nfet_01v8 L=1 W=2\nRpar_s1_XM1_s s1r_XM1_s S 50\n" in out
    assert out.rstrip().endswith("XM1 q r s t other")  # outside the DUT: untouched
    with pytest.raises(RuntimeError):
        resistance.deck_with_res(deck, "dut", "XM9", "s", 50)


def test_numerical_trouble_is_detected_in_logs():
    from src.common.tools import numerical_warnings
    assert numerical_warnings("Warning: singular matrix:  check node x1.xm4.vsubs\nok") != []
    assert numerical_warnings("Note: Starting dynamic gmin stepping\nDoing analysis") == []
    assert numerical_warnings("Warning: Dynamic gmin stepping failed") != []
