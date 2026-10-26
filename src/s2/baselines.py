"""S2 baselines (plan v2, recommendation A3): other ways to turn the same S1 sensitivities into budgets.

All methods get exactly the same inputs: the elements (expected need w_k), the harmful rates a_ik and the
allowed use b_i = eta * m_i of every check i. They differ only in how b_i is shared.

  per_net   each element alone may use the whole allowed use of its most limiting check:
            x_k = min_i b_i / a_ik  ("budget = margin_fraction x margin / per_unit", the rule of SpiceXplorer's
            postlayout.score_c_budgets, re-implemented here; their code is PolyForm-NC and is not vendored).
            It ignores that the other elements consume the same margin.
  equal     every element of a check gets an equal share of it: x_k = min_i b_i / (N_i a_ik), N_i = number of
            elements with a_ik > 0. Safe by construction, blind to what a layout needs.
  lp_sum    linear program: maximise sum_k x_k / w_k subject to A x <= b, 0 <= x_k <= kappa w_k (HiGHS). Its
            optimum is a vertex: many budgets at 0 or at kappa x need, i.e. far outside the range where the
            first-order model holds. Kept as the plain LP; not a reproduction of any published method.
  lp_floor  the same LP made fair to the library: maximise sum_k min(x_k / w_k, 1) (a budget above its need
            earns nothing) with x_k >= f_k, the library floor ours also gets (bounds [f_k, w_k]; [0, w_k] when
            the floors alone are infeasible). It differs from ours only in max-sum vs max-min sharing.
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


def lp_floor(elements, constraints, floors: dict | None = None):
    ids = [e["id"] for e in elements if any(c["a"].get(e["id"], 0) > 0 for c in constraints)]
    if not ids:
        return {}, None
    w = {e["id"]: e["w"] for e in elements}
    fl = floors or {}
    A = np.array([[c["a"].get(k, 0.0) for k in ids] for c in constraints])
    b = np.array([c["b"] for c in constraints])
    cobj = -np.array([1.0 / w[k] for k in ids])

    def solve(lo):
        return linprog(cobj, A_ub=A, b_ub=b, bounds=[(lo(k), w[k]) for k in ids], method="highs")
    r = solve(lambda k: min(fl.get(k, 0.0), w[k]))
    floored = True
    if not r.success:
        r, floored = solve(lambda k: 0.0), False
    if not r.success:
        return {}, None
    return {k: float(v) for k, v in zip(ids, r.x)}, floored


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
    xf, floored = lp_floor(elements, constraints, floors)
    sets = {"per_net": per_net(elements, constraints), "equal": equal(elements, constraints),
            "lp_sum": lp_sum(elements, constraints), "lp_floor": xf, "ours": dict(ours)}
    res = {m: {"budgets": x, "score": score(x, elements, constraints, floors)} for m, x in sets.items()}
    res["lp_floor"]["score"]["floors_applied"] = floored
    return res


def outcome(sc: dict, tol: float = 0.02) -> str:
    """One word per method, from its scores (SPICE where available, else first order):
    'unsafe'      a spec is violated in SPICE, or the layout would use more than eta x margin (use/allowed > 1);
    'infeasible'  some budget is below what the cheapest library cell already adds (no layout can meet it);
    'ok'          neither; 'unverified' is appended when some SPICE runs failed (no value, not a violation)."""
    use = sc.get("spice_worst_use_of_allowed")
    use = sc.get("worst_use_of_allowed") if use is None else use
    words = []
    if sc.get("spice_specs_violated") or (use is not None and use > 1 + tol):
        words.append("unsafe")
    if sc.get("below_floor"):
        words.append("infeasible")
    w = " + ".join(words) or "ok"
    return w + (" (unverified: failed runs)" if sc.get("spice_failed_runs") else "")
