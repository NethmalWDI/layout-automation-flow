"""S2 step 1 — joint budget allocation (decision D2 / novelty N1).

Every layout parasitic k (capacitance of a net to ground, coupling between two nets, series
resistance at a device terminal) consumes spec margin at a rate a_ik (from S1). A parasitic can only
add, so only the harmful direction counts (a_ik = max(0, -dM_i/dx_k) for a 'min' spec, max(0, +dM_i/dx_k)
for a 'max' spec); a parasitic that helps a spec is given no credit for it.

    find x >= 0   with   sum_k a_ik x_k <= eta_i * m_i     for every spec / DC headroom i

Giving each element the whole margin would double-count it. The allocation is max-min fair in units of
'expected need' w_k (an estimate of what a reasonable layout puts there):
    maximise t  such that  x_k = t * w_k  for all elements, then freeze the elements of the binding
    constraint(s) and keep raising t for the rest (progressive filling), until every element is frozen.
The first round is also solved as a linear program (scipy linprog, HiGHS) as an independent check.
Elements that consume no margin in any constraint get no budget ('unconstrained by the specs').
No element is given more than KAPPA times its expected need: far beyond the expected value a
first-order rate means little, and effects that are not modelled (slew, CMRR, PSRR, settling) would
take over (KAPPA is an ASSUMPTION).
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import linprog

KAPPA = 10.0


def harmful_rate(kind: str, slope: float | None) -> float:
    if slope is None:
        return 0.0
    return max(0.0, -slope) if kind == "min" else max(0.0, slope)


def allocate(elements: list, constraints: list, kappa: float = KAPPA) -> dict:
    """elements: [{'id', 'w'}]; constraints: [{'id', 'b', 'a': {element_id: rate}}].
    Returns {'x': {id: value}, 'rounds': [...], 'unconstrained': [...]}."""
    ids = [e["id"] for e in elements]
    w = {e["id"]: e["w"] for e in elements}
    used = {k for c in constraints for k, v in c["a"].items() if v > 0}
    unconstrained = [k for k in ids if k not in used]
    free = [k for k in ids if k in used]
    x: dict = {}
    rounds = []
    while free:
        best, binding = math.inf, []
        for c in constraints:
            slack = c["b"] - sum(c["a"].get(k, 0.0) * x[k] for k in x)
            denom = sum(c["a"].get(k, 0.0) * w[k] for k in free)
            if denom <= 0:
                continue
            t = slack / denom
            if t < best * (1 - 1e-12):
                best, binding = t, [c["id"]]
            elif abs(t - best) <= 1e-12 * max(1.0, abs(best)):
                binding.append(c["id"])
        if best is math.inf:  # remaining elements only appear in constraints with zero rate
            break
        if best >= kappa:      # the cap is reached before any spec binds
            for k in free:
                x[k] = kappa * w[k]
            rounds.append({"t": kappa, "binding": ["cap_kappa"], "frozen": list(free)})
            break
        frozen_now = [k for k in free if any(next(c for c in constraints if c["id"] == cid)["a"].get(k, 0.0) > 0
                                             for cid in binding)]
        for k in frozen_now:
            x[k] = best * w[k]
        rounds.append({"t": best, "binding": binding, "frozen": frozen_now})
        free = [k for k in free if k not in frozen_now]
    return {"x": x, "rounds": rounds, "unconstrained": unconstrained}


def lp_first_round(elements: list, constraints: list) -> dict:
    """Independent check of round 1: maximise t s.t. A x <= b, x_k >= t w_k, x >= 0 (HiGHS)."""
    ids = [e["id"] for e in elements if any(c["a"].get(e["id"], 0) > 0 for c in constraints)]
    n = len(ids)
    if n == 0:
        return {"status": "no constrained elements"}
    w = np.array([next(e["w"] for e in elements if e["id"] == k) for k in ids])
    # variables: x_1..x_n, t ; objective: maximise t
    cobj = np.zeros(n + 1)
    cobj[-1] = -1.0
    A, b = [], []
    for c in constraints:
        A.append([c["a"].get(k, 0.0) for k in ids] + [0.0])
        b.append(c["b"])
    for i in range(n):  # t*w_i - x_i <= 0
        row = [0.0] * (n + 1)
        row[i] = -1.0
        row[-1] = w[i]
        A.append(row)
        b.append(0.0)
    r = linprog(cobj, A_ub=np.array(A), b_ub=np.array(b), bounds=[(0, None)] * (n + 1), method="highs")
    return {"status": r.message, "success": bool(r.success), "t": float(r.x[-1]) if r.success else None}


def check(x: dict, constraints: list) -> list:
    out = []
    for c in constraints:
        used = sum(c["a"].get(k, 0.0) * v for k, v in x.items())
        out.append({"constraint": c["id"], "allowed": c["b"], "used": used,
                    "ok": used <= c["b"] * (1 + 1e-9) + 1e-15})
    return out


def refine(elements: list, constraints: list, x_mm: dict, delta: float = 0.05, kappa: float = KAPPA) -> dict:
    """Phase 2. Max-min fairness freezes every element that appears in a binding constraint, even when
    its rate there is negligible (e.g. 1.5e-4 deg/ohm), so such elements end up with budgets no larger
    than the critical ones. Phase 2 keeps at least (1 - delta) of every max-min budget and maximises
    sum_k log(x_k / w_k) (proportional fairness) over what is left, so the margin freed by the small
    sacrifice goes where it buys the most budget. Capped at kappa * w_k. delta is an ASSUMPTION.
    Solved in log space with SLSQP; returns the max-min budgets unchanged if it does not converge."""
    from scipy.optimize import minimize
    ids = [k for k in x_mm]
    if not ids:
        return {"x": dict(x_mm), "success": True, "note": "nothing to refine"}
    w = np.array([next(e["w"] for e in elements if e["id"] == k) for k in ids])
    lo = np.log(np.maximum(np.array([x_mm[k] for k in ids]) * (1 - delta), 1e-30))
    hi = np.log(kappa * w)
    hi = np.maximum(hi, lo)
    A = np.array([[c["a"].get(k, 0.0) for k in ids] for c in constraints])
    b = np.array([c["b"] for c in constraints])
    scale = np.where(b > 0, b, 1.0)

    def obj(y):
        return -np.sum(y - np.log(w))

    def jac(y):
        return -np.ones_like(y)

    cons = [{"type": "ineq", "fun": lambda y: (b - A @ np.exp(y)) / scale,
             "jac": lambda y: -(A * np.exp(y)) / scale[:, None]}]
    y0 = np.log(np.maximum(np.array([x_mm[k] for k in ids]), 1e-30))
    r = minimize(obj, y0, jac=jac, bounds=list(zip(lo, hi)), constraints=cons, method="SLSQP",
                 options={"maxiter": 500, "ftol": 1e-12})
    x = {k: float(np.exp(v)) for k, v in zip(ids, r.x)}
    ok = bool(r.success) and all(c["ok"] for c in check(x, constraints))
    return {"x": x if ok else dict(x_mm), "success": ok, "message": str(r.message), "delta": delta}
