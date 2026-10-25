"""S2 unit tests: the allocation (max-min fair progressive filling) and its LP cross-check, and the
rule IR basics. No simulator needed."""
import pytest

from src.s2 import budgets as B


def test_single_constraint_shares_in_proportion_to_need():
    els = [{"id": "a", "w": 1.0}, {"id": "b", "w": 3.0}]
    cons = [{"id": "gbw", "b": 8.0, "a": {"a": 1.0, "b": 1.0}}]
    r = B.allocate(els, cons)
    assert r["x"]["a"] == pytest.approx(2.0) and r["x"]["b"] == pytest.approx(6.0)  # t = 8 / (1 + 3) = 2
    assert all(c["ok"] for c in B.check(r["x"], cons))
    assert B.lp_first_round(els, cons)["t"] == pytest.approx(2.0)


def test_progressive_filling_gives_leftover_to_unblocked_elements():
    # 'a' is limited by a tight constraint; 'b' only by a loose one -> b keeps growing after a freezes
    els = [{"id": "a", "w": 1.0}, {"id": "b", "w": 1.0}]
    cons = [{"id": "pm", "b": 1.0, "a": {"a": 1.0}}, {"id": "gbw", "b": 10.0, "a": {"a": 1.0, "b": 1.0}}]
    r = B.allocate(els, cons)
    assert r["x"]["a"] == pytest.approx(1.0)
    assert r["x"]["b"] == pytest.approx(9.0)
    assert [x["binding"] for x in r["rounds"]] == [["pm"], ["gbw"]]


def test_zero_rate_elements_are_unconstrained_not_infinite():
    els = [{"id": "a", "w": 1.0}, {"id": "z", "w": 1.0}]
    cons = [{"id": "gbw", "b": 1.0, "a": {"a": 2.0, "z": 0.0}}]
    r = B.allocate(els, cons)
    assert r["unconstrained"] == ["z"] and "z" not in r["x"]


def test_harmful_rate_counts_only_degradation():
    assert B.harmful_rate("min", -0.5) == 0.5 and B.harmful_rate("min", +0.5) == 0.0
    assert B.harmful_rate("max", +0.5) == 0.5 and B.harmful_rate("max", -0.5) == 0.0
    assert B.harmful_rate("min", None) == 0.0


def test_no_margin_means_zero_budget():
    els = [{"id": "a", "w": 1.0}]
    cons = [{"id": "gbw", "b": 0.0, "a": {"a": 1.0}}]
    r = B.allocate(els, cons)
    assert r["x"]["a"] == pytest.approx(0.0)


def test_cap_limits_elements_that_no_spec_binds():
    els = [{"id": "a", "w": 1.0}, {"id": "b", "w": 2.0}]
    cons = [{"id": "gbw", "b": 1000.0, "a": {"a": 1.0, "b": 1.0}}]
    r = B.allocate(els, cons, kappa=10.0)
    assert r["x"]["a"] == pytest.approx(10.0) and r["x"]["b"] == pytest.approx(20.0)
    assert r["rounds"][-1]["binding"] == ["cap_kappa"]


def test_rule_ir_builds_from_stage_outputs_and_every_entry_is_complete():
    """Synthetic minimal inputs with the same keys S0/S1/S2 write; catches key mismatches between stages."""
    from src.s2 import rules as R
    ir = {"ports": [{"name": "INP", "role": "input"}, {"name": "INN", "role": "input"},
                    {"name": "VBIAS", "role": "bias"}, {"name": "VSS", "role": "ground"}],
          "devices": [{"name": "XM1", "terminals": {"d": "n3", "g": "INP", "s": "n1", "b": "VSS"}},
                      {"name": "XM2", "terminals": {"d": "OUT", "g": "INN", "s": "n1", "b": "VSS"}}]}
    intent = {"matching": [{"devices": ["XM1", "XM2"], "kind": "diff_pair", "evidence": ["x"]}]}
    lay = {L: {"cap_to_substrate_F_per_um_single": 8e-17, "cap_worst_F_per_um": 1.6e-16,
               "coupling_F_per_um_at_min_spacing": 5e-17, "res_ohm_per_um_at_min_width": 0.9}
           for L in ("metal1", "metal2", "metal3", "metal4")}
    pdk = {"layers": lay, "rules": {"source": "sky130A.tech"}}
    budgets = {"elements": [
        {"id": "n3", "kind": "net_capacitance", "targets": ["n3"], "units": "fF", "budget": 40.0, "binding": ["gbw"], "w": 2.0},
        {"id": "n3~OUT", "kind": "coupling", "targets": ["n3", "OUT"], "units": "fF", "budget": 10.0, "binding": ["gbw"], "w": 1.0},
        {"id": "XM1+XM2.s", "kind": "terminal_resistance", "targets": ["XM1.s", "XM2.s"], "units": "ohm",
         "budget": 70.0, "binding": ["gbw"], "w": 3.0},
        {"id": "n1", "kind": "net_capacitance", "targets": ["n1"], "units": "fF", "budget": None, "w": 2.0}]}
    currents = {"nets": {"n1": {"max_branch_A": 4e-5, "trunk_A": 8e-5}}}
    hier = {"nets": {"n3": {"route_budget_fF": 20.0, "devices": ["XM1"], "max_route_length_metal1_um": 125.0}}}
    offset = {"terminals": {"XM1.s": {"offset_uV_per_ohm_5ohm": 50.0, "ohm_per_mV_offset": 20.0}}}
    out = R.build(ir, intent, budgets, pdk, currents, hier, {}, offset)
    ids = {e["id"] for e in out}
    assert "budget.n3" in ids and "route.max_parallel.n3~OUT.metal1" in ids and "default_limit.n1" in ids
    assert "match.max_R_difference.XM1.s" in ids and "route.bias_net.VBIAS" in ids
    for e in out:
        assert e["derived_from"], e["id"]
        assert e["value"] is None or e["units"], e["id"]


def test_refine_gives_cheap_elements_more_without_breaking_constraints():
    # one binding constraint: 'big' costs 1 per unit, 'tiny' costs 0.001 per unit
    els = [{"id": "big", "w": 1.0}, {"id": "tiny", "w": 1.0}]
    cons = [{"id": "pm", "b": 2.0, "a": {"big": 1.0, "tiny": 0.001}}]
    mm = B.allocate(els, cons, kappa=10.0)["x"]
    assert mm["tiny"] == pytest.approx(mm["big"])                       # max-min: same multiple
    r = B.refine(els, cons, mm, delta=0.05, kappa=10.0)
    assert r["success"]
    assert r["x"]["tiny"] == pytest.approx(10.0, rel=1e-3)              # freed margin buys the cap
    assert r["x"]["big"] >= 0.95 * mm["big"] - 1e-9
    assert all(c["ok"] for c in B.check(r["x"], cons))
