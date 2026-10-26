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

v2 (2026-10-26, findings R19 and cell floors):
  * floors f_k >= 0: no element is budgeted below what the cheapest cell of the device library already
    puts on it (S3 unit library, measured), because no layout could realise less. With floors an element
    gets max(t * w_k, f_k); if the floors alone break a constraint, the design is infeasible at this eta
    and that is reported (the allocation then runs without floors, flagged).
  * phase 2 never trims an element below min(its phase-1 budget, its expected need), nor below its floor
    (R19: the proportional-fairness step took 5 % from every binding element to inflate elements that did
    not need it).
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


def allocate(elements: list, constraints: list, kappa: float = KAPPA, floors: dict | None = None) -> dict:
    """elements: [{'id', 'w'}]; constraints: [{'id', 'b', 'a': {element_id: rate}}]; floors: {id: f}.
    Progressive filling of x_k = max(t * w_k, f_k) (numpy, bisection on t for all constraints at once).
    Returns {'x', 'rounds', 'unconstrained', 'floors_feasible', 'floors_used'}."""
    ids = [e["id"] for e in elements]
    idx = {k: i for i, k in enumerate(ids)}
    w = np.array([e["w"] for e in elements], dtype=float)
    f = np.array([float((floors or {}).get(k, 0.0)) for k in ids])
    A = np.zeros((len(constraints), len(ids)))
    for ci, c in enumerate(constraints):
        for k, v in c["a"].items():
            if k in idx and v > 0:
                A[ci, idx[k]] = v
    b = np.array([c["b"] for c in constraints], dtype=float)
    used = A.sum(axis=0) > 0
    unconstrained = [k for k in ids if not used[idx[k]]]
    feasible = bool(np.all(A @ np.where(used, f, 0.0) <= b * (1 + 1e-12) + 1e-30))
    if not feasible:
        f = np.zeros_like(f)
    x = np.zeros(len(ids))
    free = used.copy()
    frozen = np.zeros(len(ids), dtype=bool)
    rounds = []
    while free.any():
        active = (A[:, free] > 0).any(axis=1)
        if not active.any():
            break
        base_ = A[:, frozen] @ x[frozen] if frozen.any() else np.zeros(len(b))
        Af, wf, ff = A[:, free], w[free], f[free]

        def lhs(tv):  # tv: one t per constraint
            return base_ + np.einsum("cn,cn->c", Af, np.maximum(np.outer(tv, wf), ff[None, :]))
        lo_ = np.zeros(len(b))
        hi_ = np.full(len(b), kappa)
        ok_cap = lhs(hi_) <= b
        for _ in range(100):
            mid = 0.5 * (lo_ + hi_)
            good = lhs(mid) <= b
            lo_ = np.where(good, mid, lo_)
            hi_ = np.where(good, hi_, mid)
        tc = np.where(ok_cap | ~active, np.inf, lo_)
        best = float(tc.min())
        if not math.isfinite(best) or best >= kappa:     # the cap is reached before any spec binds
            fi = np.where(free)[0]
            x[fi] = np.maximum(kappa * w[fi], f[fi])
            rounds.append({"t": kappa, "binding": ["cap_kappa"], "frozen": [ids[i] for i in fi]})
            break
        bind = np.where(tc <= best * (1 + 1e-9) + 1e-15)[0]
        fz = free & (A[bind].sum(axis=0) > 0)
        fi = np.where(fz)[0]
        x[fi] = np.maximum(best * w[fi], f[fi])
        rounds.append({"t": best, "binding": [constraints[i]["id"] for i in bind], "frozen": [ids[i] for i in fi],
                       "at_floor": [ids[i] for i in fi if f[i] > best * w[i]]})
        frozen |= fz
        free &= ~fz
    xs = {ids[i]: float(x[i]) for i in range(len(ids)) if frozen[i] or (used[i] and x[i] > 0)}
    return {"x": xs, "rounds": rounds, "unconstrained": unconstrained, "floors_feasible": feasible,
            "floors_used": bool(floors) and feasible}


def lp_first_round(elements: list, constraints: list, floors: dict | None = None) -> dict:
    """Independent check of round 1: maximise t s.t. A x <= b, x_k >= t w_k, x_k >= f_k (HiGHS)."""
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
    fl = [float((floors or {}).get(k, 0.0)) for k in ids]
    r = linprog(cobj, A_ub=np.array(A), b_ub=np.array(b), bounds=[(v, None) for v in fl] + [(0, KAPPA)], method="highs")
    return {"status": r.message, "success": bool(r.success), "t": float(r.x[-1]) if r.success else None}


def check(x: dict, constraints: list) -> list:
    out = []
    for c in constraints:
        used = sum(c["a"].get(k, 0.0) * v for k, v in x.items())
        out.append({"constraint": c["id"], "allowed": c["b"], "used": used,
                    "ok": used <= c["b"] * (1 + 1e-9) + 1e-15})
    return out


SLSQP_MAX_VARS = 200   # above this many elements phase 2 uses an interior-point solver (same optimum, scales)


def _refine_large(A, b, w, lo, hi, x0):
    """Same phase-2 problem in x space for many elements: maximise sum log(x/w) s.t. A x <= b,
    lo <= x <= hi, with scipy's interior-point trust-constr (sparse A, diagonal Hessian). The result is
    clipped to the bounds and, if a constraint is still exceeded by rounding, moved back towards x0."""
    from scipy.optimize import Bounds, LinearConstraint, minimize
    from scipy.sparse import csr_matrix, diags
    sc = np.where(b > 0, b, 1.0)
    As, bs = csr_matrix(A / sc[:, None]), b / sc
    r = minimize(lambda x: -np.sum(np.log(x / w)), x0, jac=lambda x: -1.0 / x, hess=lambda x: diags(1.0 / x ** 2),
                 method="trust-constr", constraints=[LinearConstraint(As, -np.inf, bs * (1 - 1e-9))],
                 bounds=Bounds(lo, hi),
                 options={"maxiter": 3000, "gtol": 1e-10, "xtol": 1e-12, "verbose": 0})
    x = np.clip(r.x, lo, hi)
    over = As @ x - bs
    if over.max() > 1e-9:          # within check()'s tolerance is accepted (review item 2)
        d = x - x0
        ad = As @ d
        slack = bs - As @ x0
        with np.errstate(divide="ignore", invalid="ignore"):
            th = np.where(ad > 0, slack / ad, np.inf)
        x = x0 + max(0.0, min(1.0, float(th.min()))) * d
    return x, str(r.message)


def refine(elements: list, constraints: list, x_mm: dict, delta: float = 0.05, kappa: float = KAPPA,
           floors: dict | None = None, protect_need: bool = True) -> dict:
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
    xm = np.array([x_mm[k] for k in ids])
    lo_lin = xm * (1 - delta)
    if protect_need:   # R19: never below min(phase-1 budget, expected need)
        lo_lin = np.maximum(lo_lin, np.minimum(xm, w))
    if floors:
        lo_lin = np.maximum(lo_lin, np.array([float(floors.get(k, 0.0)) for k in ids]))
    # phase 2 may never ask for more than phase 1 gave as its floor; a pinned element keeps a hair of room
    # so that a tight constraint does not make the solver report the bounds as incompatible (review item 1)
    lo_lin = np.minimum(lo_lin, xm * (1 - 1e-9))
    lo = np.log(np.maximum(lo_lin, 1e-30))
    hi = np.log(kappa * w)
    hi = np.maximum(hi, lo)
    A = np.array([[c["a"].get(k, 0.0) for k in ids] for c in constraints])
    b = np.array([c["b"] for c in constraints])
    scale = np.where(b > 0, b, 1.0)

    def obj(y):
        return -np.sum(y - np.log(w))

    def jac(y):
        return -np.ones_like(y)

    if len(ids) > SLSQP_MAX_VARS:
        x, msg = _refine_large(A, b, w, np.exp(lo), np.exp(hi), xm)
        ok = all(c["ok"] for c in check(dict(zip(ids, x)), constraints))
        xd = {k: float(v) for k, v in zip(ids, x)}
        return {"x": xd if ok else dict(x_mm), "success": ok, "message": "trust-constr: " + msg,
                "delta": delta, "protect_need": protect_need, "floors_used": bool(floors)}
    cons = [{"type": "ineq", "fun": lambda y: (b - A @ np.exp(y)) / scale,
             "jac": lambda y: -(A * np.exp(y)) / scale[:, None]}]
    y0 = np.log(np.maximum(np.array([x_mm[k] for k in ids]), 1e-30))
    r = minimize(obj, y0, jac=jac, bounds=list(zip(lo, hi)), constraints=cons, method="SLSQP",
                 options={"maxiter": 500, "ftol": 1e-12})
    x = {k: float(np.exp(v)) for k, v in zip(ids, r.x)}
    ok = bool(r.success) and all(c["ok"] for c in check(x, constraints))
    return {"x": x if ok else dict(x_mm), "success": ok, "message": str(r.message), "delta": delta,
            "protect_need": protect_need, "floors_used": bool(floors)}
