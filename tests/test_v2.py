"""Unit tests for the plan-v2 additions: generality (parser, linear model), allocation floors and the R19
fix, baselines, the fast corner model, W bins, flattening, structure recognition, testbench templates."""
import math
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from src.common import spice  # noqa: E402
from src.s1 import linear  # noqa: E402
from src.s2 import baselines as BL, budgets as B  # noqa: E402


# ------------------------------------------------------------------ parser
NET = """.subckt amp in1 in2 out vss vdd
*.ipin in1
XM1 a in1 t vss sky130_fd_pr__nfet_01v8 L=0.5 W=4 nf=1 mult=1
XM2 out in2 t vss sky130_fd_pr__nfet_01v8 L=0.5 W=4 nf=1 mult=1
XM3 a a vdd vdd sky130_fd_pr__pfet_01v8 L=1 W=2 nf=1 mult=1
XM4 out a vdd vdd sky130_fd_pr__pfet_01v8 L=1 W=2 nf=1 mult=1
XM5 t b vss vss sky130_fd_pr__nfet_01v8 L=1 W=4 nf=1 mult=1
XM6 b b vss vss sky130_fd_pr__nfet_01v8 L=1 W=4 nf=1 mult=1
Ib vdd b DC 10u
Cc a out 0.5p
XC1 out vss sky130_fd_pr__cap_mim_m3_1 W=10 L=10 MF=2 m=2
XR1 out r2 sky130_fd_pr__res_generic_po W=0.5 L=40
XR2 r2 vss sky130_fd_pr__res_generic_po W=0.5 L=40
.ends
"""


def test_parser_sources_and_passives(tmp_path):
    f = tmp_path / "n.spice"
    f.write_text(NET)
    nl = spice.parse(f)
    assert [s.kind for s in nl.sources] == ["I"] and nl.sources[0].dc == pytest.approx(10e-6)
    kinds = {p.name: (p.kind, p.model) for p in nl.passives}
    assert kinds["Cc"] == ("C", "ideal") and kinds["XC1"][0] == "C" and kinds["XR1"][0] == "R"
    cc = next(p for p in nl.passives if p.name == "Cc")
    assert cc.nominal == pytest.approx(0.5e-12)
    mim = next(p for p in nl.passives if p.name == "XC1")
    assert mim.nominal == pytest.approx(2 * 2e-15 * 10.15 ** 2)
    assert next(p for p in nl.passives if p.name == "XR1").nominal is None   # read from the simulator
    assert not spice.validate(nl, ["sky130_fd_pr__nfet_01v8", "sky130_fd_pr__pfet_01v8"])


def test_parser_still_refuses_unknown_elements(tmp_path):
    f = tmp_path / "n.spice"
    f.write_text(".subckt x a b\nE1 a 0 b 0 10\n.ends\n")
    with pytest.raises(spice.SpiceError):
        spice.parse(f)


@pytest.mark.parametrize("txt,val", [("10u", 1e-5), ("1e-05", 1e-5), ("0.5p", 5e-13), ("2meg", 2e6),
                                     ("200fF", 2e-13), ("'1.8'", 1.8)])
def test_si(txt, val):
    assert spice.si(txt) == pytest.approx(val)


# ------------------------------------------------------------------ allocation
EL = [{"id": "a", "w": 1.0}, {"id": "b", "w": 1.0}, {"id": "c", "w": 2.0}, {"id": "d", "w": 1.0}]
CO = [{"id": "g", "b": 1.0, "margin": 1.0, "a": {"a": 0.5, "b": 0.1}},
      {"id": "p", "b": 1.0, "margin": 1.0, "a": {"b": 0.2, "c": 0.1}}]


def test_allocate_maxmin_matches_closed_form():
    r = B.allocate(EL, CO)
    assert r["x"]["a"] == pytest.approx(1 / 0.6) and r["x"]["b"] == pytest.approx(1 / 0.6)
    assert r["x"]["c"] == pytest.approx((1 - 0.2 / 0.6) / 0.1)
    assert r["unconstrained"] == ["d"]
    assert B.lp_first_round(EL, CO)["t"] == pytest.approx(1 / 0.6)


def test_allocate_with_floor_and_lp_agree():
    r = B.allocate(EL, CO, floors={"a": 1.8})
    assert r["x"]["a"] == pytest.approx(1.8) and r["rounds"][0]["at_floor"] == ["a"]
    assert r["x"]["b"] == pytest.approx(1.0, rel=1e-6)
    assert B.lp_first_round(EL, CO, floors={"a": 1.8})["t"] == pytest.approx(1.0, rel=1e-6)
    assert all(c["ok"] for c in B.check(r["x"], CO))


def test_infeasible_floors_are_reported_not_used():
    r = B.allocate(EL, CO, floors={"a": 3.0})
    assert r["floors_feasible"] is False and r["x"]["a"] == pytest.approx(1 / 0.6)


def test_r19_phase2_never_trims_below_need():
    """phase 1 gives a and b 1/0.6 of their need; with a third element in g sharing tightly, R19: no element
    at or below its need may be trimmed by phase 2"""
    el = [{"id": "a", "w": 1.0}, {"id": "b", "w": 1.0}, {"id": "z", "w": 0.01}]
    co = [{"id": "g", "b": 1.0, "margin": 1.0, "a": {"a": 0.9, "b": 0.9, "z": 0.05}}]
    x = B.allocate(el, co)["x"]
    assert x["a"] < 1.0   # binding element below its need
    v1 = B.refine(el, co, x, protect_need=False)["x"]
    v2 = B.refine(el, co, x, protect_need=True)["x"]
    assert v1["a"] < x["a"] * 0.999           # the v1 behaviour (finding R19)
    assert v2["a"] >= x["a"] * (1 - 1e-9)     # fixed


def test_refine_large_matches_slsqp():
    rng = np.random.default_rng(3)
    el = [{"id": f"e{i}", "w": float(rng.uniform(0.5, 5))} for i in range(60)]
    co = [{"id": f"c{j}", "b": 1.0, "margin": 1.0,
           "a": {f"e{i}": float(rng.uniform(0, 1e-2)) for i in rng.choice(60, 20, replace=False)}} for j in range(6)]
    x = B.allocate(el, co)["x"]
    a = B.refine(el, co, x)["x"]
    old = B.SLSQP_MAX_VARS
    B.SLSQP_MAX_VARS = 0
    try:
        b = B.refine(el, co, x)["x"]
    finally:
        B.SLSQP_MAX_VARS = old
    obj = lambda xx: sum(math.log(xx[e["id"]] / e["w"]) for e in el if e["id"] in xx)  # noqa: E731
    assert obj(b) == pytest.approx(obj(a), abs=1e-3)


def test_baselines_safety_and_starvation():
    s = BL.run_all(EL, CO, B.refine(EL, CO, B.allocate(EL, CO)["x"])["x"])
    assert s["per_net"]["score"]["worst_use_of_allowed"] > 1          # over-commits the shared check
    assert s["equal"]["score"]["worst_use_of_allowed"] <= 1 + 1e-9    # safe by construction
    assert s["ours"]["score"]["worst_use_of_allowed"] <= 1 + 1e-9
    assert s["lp_sum"]["score"]["worst_use_of_allowed"] <= 1 + 1e-6
    assert s["lp_floor"]["score"]["worst_use_of_allowed"] <= 1 + 1e-6
    assert all(v <= e["w"] * (1 + 1e-9) for e in EL for k, v in s["lp_floor"]["budgets"].items() if k == e["id"])


def test_lp_floor_respects_floors_and_outcome_words():
    fl = {e["id"]: 0.1 * e["w"] for e in EL}
    x, floored = BL.lp_floor(EL, CO, fl)
    assert floored and all(x[k] >= fl[k] * (1 - 1e-9) for k in x)
    # a failed SPICE run is 'unverified', never a violation
    assert BL.outcome({"worst_use_of_allowed": 0.5, "spice_worst_use_of_allowed": None, "spice_specs_violated": [],
                       "spice_failed_runs": ["gbw_mhz"], "below_floor": []}) == "ok (unverified: failed runs)"
    assert BL.outcome({"worst_use_of_allowed": 0.9, "spice_worst_use_of_allowed": 1.3, "spice_specs_violated": [],
                       "below_floor": ["a"]}) == "unsafe + infeasible"


# ------------------------------------------------------------------ linear model: passives, current sources, dido
def _ir(diff_out=False):
    """A resistively loaded differential pair as an IR with an ideal capacitor and a current source."""
    devs = []
    op = {}
    for n, (d, g, s) in {"M1": ("o1", "i1", "t"), "M2": ("o2", "i2", "t")}.items():
        devs.append({"name": n, "type": "nmos", "model": "m", "terminals": {"d": d, "g": g, "s": s, "b": "vss"},
                     "W_um": 1, "L_um": 1, "nf": 1, "m": 1})
        z = {k: 0.0 for k in ("cgg", "cgd", "cgs", "cgb", "cdg", "cdd", "cds", "cdb", "csg", "csd", "css", "csb",
                              "cbg", "cbd", "cbs", "cbb", "capbd", "capbs", "cgso", "cgdo", "cgbo")}
        op[n] = {**z, "gm": 1e-3, "gmbs": 0.0, "gds": 0.0}
    ports = [{"name": "i1", "role": "input", "testbench_port": "INP"}, {"name": "i2", "role": "input", "testbench_port": "INN"},
             {"name": "o2", "role": "output", "testbench_port": "OUTP"}, {"name": "vdd", "role": "supply", "testbench_port": "VDD"},
             {"name": "vss", "role": "ground", "testbench_port": "VSS"}]
    if diff_out:
        ports.append({"name": "o1", "role": "output", "testbench_port": "OUTN"})
    nets = ["i1", "i2", "o1", "o2", "t", "vdd", "vss"]
    return {"ports": ports, "devices": devs, "nets": [{"name": n} for n in nets], "conditions": {"CL_F": "1p"},
            "internal_sources": [{"name": "It", "kind": "I", "p": "t", "n": "vss"}],
            "passives": [{"name": "R1", "kind": "R", "a": "o1", "b": "vdd", "value": 10e3},
                         {"name": "R2", "kind": "R", "a": "o2", "b": "vdd", "value": 10e3},
                         {"name": "Cx", "kind": "C", "a": "o2", "b": "vss", "value": 1e-12}]}, op


def test_linear_passives_and_current_source_open():
    ir, op = _ir()
    lm = linear.LinearModel(ir, op, drive={"i1": 0.5, "i2": -0.5})
    assert "t" in lm.unknown          # the tail fed by an ideal current source is solved, not AC ground
    H = lm.response(np.array([1.0]))[0]
    # half circuit: v(o2) = -gm * R * v(i2)... with the tail floating: o2 = +gm R vd / 2
    assert abs(H) == pytest.approx(1e-3 * 10e3 / 2, rel=1e-6)


def test_linear_differential_output():
    ir, op = _ir(diff_out=True)
    lm = linear.LinearModel(ir, op, drive={"i1": 0.5, "i2": -0.5})
    H = lm.response(np.array([1.0]))[0]
    assert abs(H) == pytest.approx(1e-3 * 10e3, rel=1e-6)   # v(o2) - v(o1) = gm R vd


def test_fast_model_matches_finite_differences():
    ir, op = _ir(diff_out=True)
    lm = linear.LinearModel(ir, op, drive={"i1": 0.5, "i2": -0.5})
    fm = linear.FastModel(lm)
    r = fm.rates_c("o2", None)
    f = np.logspace(0, 9, 9 * 4000 + 1)   # dense grid: the 40/decade grid interpolates the UGB linearly
    mp = linear.metrics(linear.LinearModel(ir, op, drive={"i1": 0.5, "i2": -0.5}, extra_c=[("o2", None, 1e-15)]).response(f), f)
    mm = linear.metrics(linear.LinearModel(ir, op, drive={"i1": 0.5, "i2": -0.5}, extra_c=[("o2", None, -1e-15)]).response(f), f)
    assert r["gbw_mhz"] == pytest.approx((mp["gbw_mhz"] - mm["gbw_mhz"]) / 2, rel=0.005)


# ------------------------------------------------------------------ scripts
def test_flatten_and_recognise(tmp_path):
    import flatten_spice
    import recognize_structures as rs
    src = tmp_path / "h.spice"
    src.write_text(".subckt pair a b o1 o2 t vss\nXM1 o1 a t vss sky130_fd_pr__nfet_01v8 L=1 W=2 nf=1 "
                   "ad='int((nf+1)/2) * W/nf * 0.29' m=1\nXM2 o2 b t vss sky130_fd_pr__nfet_01v8 L=1 W=2 nf=1 m=1\n.ends\n"
                   ".subckt top a b o1 o2 vss vdd\nx1 a b o1 o2 tail vss pair\nXM3 tail g vss vss sky130_fd_pr__nfet_01v8 L=1 W=4 nf=1 m=1\n"
                   "XM4 g g vss vss sky130_fd_pr__nfet_01v8 L=1 W=4 nf=1 m=1\nIb vdd g 10u\n.ends\n")
    dst = tmp_path / "f.spice"
    st = flatten_spice.flatten(src, "top", dst, "flat")
    assert st["devices"] == 4 and st["instances"] == 1
    txt = dst.read_text()
    assert "XX1_M1 o1 a tail vss" in txt and "ad=0.58" in txt
    nl = spice.parse(dst)
    blocks = rs.recognize(nl, {"vss", "vdd"})
    kinds = sorted(b["primitive"] for b in blocks)
    assert "nmos-differential-pair" in kinds and "nmos-current-mirror" in kinds


def test_recognise_dummies_never_join_a_mirror(tmp_path):
    """A dummy with d = g = s looks diode-connected; it must not form a mirror with the diode it sits next
    to (iadc_ota: 24 of its 38 dummies had formed 6 false blocks)."""
    import recognize_structures as rs
    f = tmp_path / "d.spice"
    f.write_text(".subckt t g o x vss\nXM1 g g vss vss sky130_fd_pr__nfet_01v8 L=1 W=4 nf=1 m=1\n"
                 "XM2 o g vss vss sky130_fd_pr__nfet_01v8 L=1 W=4 nf=1 m=1\n"
                 "XM3 x x x vss sky130_fd_pr__nfet_01v8 L=1 W=4 nf=1 m=1\n"
                 "XM4 g vss vss vss sky130_fd_pr__nfet_01v8 L=1 W=4 nf=1 m=1\n"
                 "XM5 vss vss vss vss sky130_fd_pr__nfet_01v8 L=1 W=4 nf=1 m=1\n.ends\n")
    blocks = rs.recognize(spice.parse(f), {"vss"})
    by = {tuple(b["devices"]): b["primitive"] for b in blocks}
    assert by[("XM1", "XM2")] == "nmos-current-mirror"
    assert all(by[(d,)] == "nmos-dummy" for d in ("XM3", "XM4", "XM5"))


def test_recognise_off_devices_mos_caps_and_rail_gates(tmp_path):
    """review B, item 6: polarity-aware off test, native devices, MOS capacitors, and no rail-gated
    device in a differential pair."""
    import recognize_structures as rs
    f = tmp_path / "e.spice"
    f.write_text(".subckt t a b o1 o2 t x VDD VSS\n"
                 "XM1 o1 a t VSS sky130_fd_pr__nfet_01v8 L=1 W=4 nf=1 m=1\n"
                 "XM2 o2 b t VSS sky130_fd_pr__nfet_01v8 L=1 W=4 nf=1 m=1\n"
                 "XM3 x VSS t VSS sky130_fd_pr__nfet_01v8 L=1 W=4 nf=1 m=1\n"      # edge dummy on the tail
                 "XM4 VSS VDD VSS VSS sky130_fd_pr__nfet_01v8 L=1 W=4 nf=1 m=1\n"  # NMOS decap, on
                 "XM5 x x x VSS sky130_fd_pr__nfet_01v8_nvt L=1 W=4 nf=1 m=1\n"     # native, not off at Vgs = 0
                 "XM6 o1 o1 o1 VDD sky130_fd_pr__pfet_01v8 L=1 W=4 nf=1 m=1\n"
                 "XM7 o2 a o2 VSS sky130_fd_pr__nfet_01v8 L=1 W=4 nf=1 m=1\n.ends\n")   # MOS cap on a signal
    blocks = rs.recognize(spice.parse(f), {"VDD", "VSS"})
    by = {d: b["primitive"] for b in blocks for d in b["devices"]}
    assert by["XM1"] == by["XM2"] == "nmos-differential-pair"
    assert by["XM3"] == "nmos-dummy" and by["XM6"] == "pmos-dummy"
    assert by["XM4"] == "nmos-mos-capacitor" and by["XM7"] == "nmos-mos-capacitor"
    assert by["XM5"] != "nmos-dummy"


def test_benchlib_dido_has_both_loads_and_chokes():
    import benchlib
    t = benchlib.bench("d", "AC", ".subckt d a b c d e f\n.ends d\n", "XDUT INP INN OUTP OUTN VDD VSS d", True)
    for s in ("Lfbp OUTP INN", "Lfbn OUTN INP", "Cloadp OUTP 0", "Cloadn OUTN 0", "v(OUTP) - v(OUTN)"):
        assert s in t


def test_wbins_read_from_pdk():
    from src.s3 import wbins
    if not wbins.MODEL_DIR.exists():
        pytest.skip("PDK not installed here")
    b = wbins.bins("sky130_fd_pr__nfet_01v8_lvt")
    assert b and all(l0 < l1 and w0 < w1 for l0, l1, w0, w1 in b)
    assert wbins.bin_index("sky130_fd_pr__nfet_01v8_lvt", 24, 0.5) is not None


def test_s3_unit_cell_scaling_for_m_copies():
    """A device with m > 1 is m unit cells in parallel: access R / m, area x m, PCell drawn with m = 1."""
    from src.s3 import options as O
    rules = {"poly_sheet_res_ohm_sq": 48.2, "contacts": {k: {"ohm_per_contact": v} for k, v in
             {"licon_poly": 152.0, "licon_ndiff": 185.0, "licon_pdiff": 585.0, "mcon": 9.3, "via1": 4.5}.items()},
             "layers": {"metal1": {"sheet_res_ohm_sq": 0.125}, "locali": {"sheet_res_ohm_sq": 12.8}}}
    geo = {"n_licon_poly": 4, "n_mcon_gate": 2,
           "strips": [{"role": "D", "n_licon": 6, "n_mcon": 6, "length_um": 1.4, "width_um": 0.17},
                      {"role": "S", "n_licon": 6, "n_mcon": 6, "length_um": 1.4, "width_um": 0.17}]}
    opt = {"nf": 1, "gate_contacts": "both"}
    t1 = {"W": 1.4, "L": 0.6, "m": 1, "type": "nmos"}
    t6 = {**t1, "m": 6}
    r1, r6 = O.access_resistance(t1, opt, geo, rules), O.access_resistance(t6, opt, geo, rules)
    for k in "dgs":
        assert abs(r6[k] * 6 - r1[k]) < 1e-9 * r1[k]
    assert r6["unit_cell_ohm"]["d"] == r1["d"]
    assert O.magic_params(t6, {"nf": 2, "magic": {}})["m"] == 1
