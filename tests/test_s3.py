"""S3 unit tests (no simulator, no Magic): device replacement in a testbench and the cell subcircuit."""
import pytest

from src.s3 import evaluate as E, options as O


def _rec(tmp_path, body):
    f = tmp_path / "pex.spice"
    f.write_text(body)
    return {"cell": "cellA", "pex": {"file": str(f), "subckt": "cellA", "ports": ["S", "D", "G", "B"], "fingers": [{}]}}


def test_substrate_node_becomes_a_port_tied_to_ground(tmp_path):
    rec = _rec(tmp_path, ".subckt cellA S D G B\nX0 D G S B sky130_fd_pr__pfet_01v8 w=4 l=1\nC9 B VSUBS 3.8f\n.ends\n")
    name, body, ports = E.cell_subckt(rec)
    assert ports == ["S", "D", "G", "B", "SUB"] and "VSUBS" not in body and "C9 B SUB 3.8f" in body
    deck = "x1 a b dut\n.subckt dut d g s b\nXM3 d g s b sky130_fd_pr__pfet_01v8 L=1 W=8\n.ends\n.end\n"
    out = E.replace_devices(deck, "dut", {"XM3": (rec, {"d": 1.0, "g": 2.0, "s": 3.0})}, gnd="VSS")
    assert "XM3 s3_XM3_s s3_XM3_d s3_XM3_g b VSS s3c_cella\n" in out
    assert "Rs3_XM3_g s3_XM3_g g 2\n" in out
    assert ".subckt s3c_cella S D G B SUB" in out and out.rstrip().endswith(".end")


def test_replacing_an_unknown_device_or_dut_fails_loudly(tmp_path):
    rec = _rec(tmp_path, ".subckt cellA S D G B\nX0 D G S B sky130_fd_pr__nfet_01v8 w=4 l=1\n.ends\n")
    deck = ".subckt dut d g s b\nXM1 d g s b sky130_fd_pr__nfet_01v8 L=1 W=8\n.ends\n.end\n"
    with pytest.raises(RuntimeError):
        E.replace_devices(deck, "dut", {"XM9": (rec, None)})
    with pytest.raises(RuntimeError):
        E.replace_devices(deck, "nodut", {"XM1": (rec, None)})


def test_option_grid_respects_min_finger_width_and_source_side():
    g = O.grid(1.0)                       # W = 1 um: nf = 4 and 8 would give fingers < 0.42 um
    assert {o["nf"] for o in g} == {1, 2}
    assert {o["outer"] for o in g if o["nf"] == 2} == {"S", "D"}
    assert all(o["magic"]["conn_gates"] == (1 if o["nf"] > 1 else 0) for o in g)


def test_relaxed_pick_default_keeps_the_pcell_least_bad_takes_the_largest_slack():
    nf1 = {"option": {"id": O.default_option_id()}, "min_slack": -422.3}     # LOADBench 484/0.24: 8.2 kohm gate
    nf64 = {"option": {"id": "nf64_gboth_sdfull_outS"}, "min_slack": -1.19}
    nf8 = {"option": {"id": "nf8_gboth_sdhalf_outS"}, "min_slack": -40.0}
    assert O.relaxed_pick([nf8, nf1, nf64]) is nf64                          # the S3 default since 2026-10-27
    assert O.relaxed_pick([nf8, nf1, nf64], "least-bad") is nf64
    assert O.relaxed_pick([nf8, nf1, nf64], "default") is nf1                # every plan-v2 run
    assert O.relaxed_pick([nf8, nf64], "default") is nf64                    # default not built: largest slack
    with pytest.raises(ValueError):
        O.relaxed_pick([nf1], "smallest")


def test_flow_passes_the_relaxed_type_rule_to_s3():
    from argparse import Namespace
    from src import flow

    def s3_args(**kw):
        return flow.steps("S3", "example_ota_5t", Namespace(workers=2, **kw))[0][1]
    assert "--relax-fallback" not in s3_args(variant="v2")                          # S3's own default: least-bad
    v1 = s3_args(variant="v1")                                                      # 'before' keeps the old rule
    assert v1[v1.index("--relax-fallback") + 1] == "default"
    assert s3_args(variant="v2", relax_fallback="default")[-2:] == ["--relax-fallback", "default"]


def test_bsim4_gate_resistance_formula():
    t = {"W": 24.0, "L": 0.5, "type": "nmos"}
    geo = {"n_licon_poly": 1, "n_mcon_gate": 1, "strips": []}
    rules = {"poly_sheet_res_ohm_sq": 48.2, "contacts": {"licon_poly": {"ohm_per_contact": 0.0}, "mcon": {"ohm_per_contact": 0.0},
             "licon_ndiff": {"ohm_per_contact": 185.0}, "licon_pdiff": {"ohm_per_contact": 585.0},
             "via1": {"ohm_per_contact": 4.5}}, "layers": {"metal1": {"sheet_res_ohm_sq": 0.125}, "locali": {"sheet_res_ohm_sq": 12.8}}}
    both = O.access_resistance(t, {"nf": 1, "gate_contacts": "both"}, geo, rules)["g"]
    top = O.access_resistance(t, {"nf": 1, "gate_contacts": "top"}, geo, rules)["g"]
    nf4 = O.access_resistance(t, {"nf": 4, "gate_contacts": "both"}, geo, rules)["g"]
    assert both == pytest.approx(48.2 * 24 / (12 * 0.5))      # two contacted ends: W/(12 L)
    assert top == pytest.approx(4 * both)                       # one end: W/(3 L)
    assert nf4 == pytest.approx(both / 16)                      # W_f = W/4 and 4 fingers in parallel
