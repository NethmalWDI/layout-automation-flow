"""S2 baselines (plan v2, recommendation A3): other ways to turn the same S1 sensitivities into budgets.

All methods get exactly the same inputs: the elements (expected need w_k), the harmful rates a_ik and the
allowed use b_i = eta * m_i of every check i. They differ only in how b_i is shared.

  per_net   each element alone may use the whole allowed use of its most limiting check:
            x_k = min_i b_i / a_ik  ("budget = margin_fraction x margin / per_unit", the rule of SpiceXplorer's
            postlayout.score_c_budgets, re-implemented here; their code is PolyForm-NC and is not vendored).
            It ignores that the other elements consume the same margin.
  equal     every element of a check gets an equal share of it: x_k = min_i b_i / (N_i a_ik), N_i = number of
            elements with a_ik > 0. Safe by construction, blind to what a layout needs.
  lp_sum    Choudhury & Sangiovanni-Vincentelli style linear program: maximise sum_k x_k / w_k subject to
            A x <= b, x_k <= kappa w_k (HiGHS). Safe, but puts the margin where it is cheapest.
  ours      max-min fair progressive filling in units of expected need, phase-2 proportional fairness,
            R19 floor and library floors (budgets.allocate/refine), i.e. what S2 outputs.

Scores, all first order (SPICE checks of the same budget sets are run by S2 when SPICE is enabled):
  worst_use      max_i sum_k a_ik x_k / b_i       (> 1: the set is unsafe; the margin is over-committed)
  starved        elements with x_k < w_k          (the budget is below what a compact layout puts there)
  below_floor    elements with x_k < f_k          (no cell of the library can meet the budget at all)
  min_ratio      min_k x_k / w_k                  (worst element, in units of its need)
  geo_ratio      geometric mean of x_k / w_k
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import linprog

from src.s2 import budgets as B


def per_net(elements, constraints, kappa=B.KAPPA):
    x = {}
    for e in elements:
        k = e["id"]
        lim = [c["b"] / c["a"][k] for c in constraints if c["a"].get(k, 0.0) > 0]
        if lim:
            x[k] = min(min(lim), kappa * e["w"])
    return x


def equal(elements, constraints, kappa=B.KAPPA):
    n = {c["id"]: sum(1 for v in c["a"].values() if v > 0) for c in constraints}
    x = {}
    for e in elements:
        k = e["id"]
        lim = [c["b"] / (n[c["id"]] * c["a"][k]) for c in constraints if c["a"].get(k, 0.0) > 0]
        if lim:
            x[k] = min(min(lim), kappa * e["w"])
    return x


def lp_sum(elements, constraints, kappa=B.KAPPA):
    ids = [e["id"] for e in elements if any(c["a"].get(e["id"], 0) > 0 for c in constraints)]
    if not ids:
        return {}
    w = {e["id"]: e["w"] for e in elements}
    cobj = -np.array([1.0 / w[k] for k in ids])
    A = np.array([[c["a"].get(k, 0.0) for k in ids] for c in constraints])
    b = np.array([c["b"] for c in constraints])
    r = linprog(cobj, A_ub=A, b_ub=b, bounds=[(0, kappa * w[k]) for k in ids], method="highs")
    if not r.success:
        return {}
    return {k: float(v) for k, v in zip(ids, r.x)}


def score(x: dict, elements: list, constraints: list, floors: dict | None = None) -> dict:
    w = {e["id"]: e["w"] for e in elements}
    use = {}
    for c in constraints:
        u = sum(c["a"].get(k, 0.0) * v for k, v in x.items())
        use[c["id"]] = u / c["b"] if c["b"] > 0 else None
    ratios = [x[k] / w[k] for k in x if w.get(k)]
    fl = floors or {}
    return {"worst_use_of_allowed": max((v for v in use.values() if v is not None), default=None),
            "use_of_allowed": use,
            "unsafe_checks": sorted(k for k, v in use.items() if v is not None and v > 1 + 1e-9),
            "n_elements": len(x),
            "starved": sorted(k for k in x if x[k] < w[k] * (1 - 1e-9)),
            "below_floor": sorted(k for k in x if x[k] < fl.get(k, 0.0) * (1 - 1e-9)),
            "min_ratio_to_need": min(ratios) if ratios else None,
            "geo_mean_ratio_to_need": math.exp(sum(math.log(max(r_, 1e-30)) for r_ in ratios) / len(ratios)) if ratios else None}


def run_all(elements: list, constraints: list, ours: dict, floors: dict | None = None) -> dict:
    sets = {"per_net": per_net(elements, constraints), "equal": equal(elements, constraints),
            "lp_sum": lp_sum(elements, constraints), "ours": dict(ours)}
    return {m: {"budgets": x, "score": score(x, elements, constraints, floors)} for m, x in sets.items()}
