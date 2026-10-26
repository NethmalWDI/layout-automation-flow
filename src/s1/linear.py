"""S1 step 2 — exact small-signal (linearised) model of the whole circuit at its operating point.

Each MOSFET is stamped with:
  * gm, gmbs, gds (VCCS + conductance, current defined into the drain),
  * the full BSIM4 intrinsic charge matrix C_ij = dQ_i/dV_j (non-reciprocal, quasi-static),
  * overlap caps cgso/cgdo/cgbo and junction caps capbd/capbs (reciprocal).
Netlist passives are stamped too (ideal R/C, and PDK capacitors/resistors at their nominal value).
Nodes: supplies, ground, and nodes held by ideal VOLTAGE sources are AC ground; an ideal current
source is an open circuit in AC (its nodes are solved); inputs are driven as in the AC testbench;
every other net is solved.
Metrics replicate the testbench definitions (diso/dido_amp_AC): gain at 1 Hz, UGB where |H| = 1
(linear interpolation on a 40 points/decade grid), PM = 180 + (phase(UGB) - phase(1 Hz)).
"""
from __future__ import annotations

import numpy as np

TERMS = "dgsb"
CMAT = {("d", "d"): "cdd", ("d", "g"): "cdg", ("d", "s"): "cds", ("d", "b"): "cdb",
        ("g", "d"): "cgd", ("g", "g"): "cgg", ("g", "s"): "cgs", ("g", "b"): "cgb",
        ("s", "d"): "csd", ("s", "g"): "csg", ("s", "s"): "css", ("s", "b"): "csb",
        ("b", "d"): "cbd", ("b", "g"): "cbg", ("b", "s"): "cbs", ("b", "b"): "cbb"}


def parse_si(v) -> float:
    """'1p', '1pF', '200f', '200fF', '1e-12' -> farads etc. A trailing unit letter after a prefix is dropped."""
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().lower()
    import re as _re
    m = _re.fullmatch(r"([-+0-9.e]+)(meg|[fpnumkg])?[a-z]*", s)
    if m and m.group(2):
        s = m.group(1) + m.group(2)
    elif m:
        s = m.group(1)
    mult = {"f": 1e-15, "p": 1e-12, "n": 1e-9, "u": 1e-6, "m": 1e-3, "k": 1e3, "meg": 1e6, "g": 1e9}
    for suf in ("meg", "f", "p", "n", "u", "m", "k", "g"):
        if s.endswith(suf):
            return float(s[: -len(suf)]) * mult[suf]
    return float(s)


class LinearModel:
    def __init__(self, ir: dict, op: dict, drive: dict | None = None, extra_c: list | None = None,
                 extra_r: list | None = None):
        """ir: circuit_ir; op: per-device OP dict; drive: known AC node voltages;
        extra_c: [(netA, netB_or_None, farads)] added capacitors (None = to ground);
        extra_r: [(device, terminal, ohms)] series resistance between a device terminal and its net.
        A series resistor splits the terminal off its net onto a new internal node '<dev>.<t>'."""
        for c in ir.get("passives", []):
            if c.get("value") is None:
                raise NotImplementedError(f"passive {c['name']} ({c.get('model')}) has no nominal value for the linear model")
        roles = {p["name"]: p["role"] for p in ir["ports"]}
        ground = {n for n, r in roles.items() if r in ("ground", "supply", "bias_ac_ground")}
        # ASSUMPTION (testbench): nodes held by ideal internal VOLTAGE sources (bias) are AC ground; a real
        # bias generator has finite impedance, so couplings onto VBIAS are not budgeted from this model.
        # An ideal current source has infinite impedance: it adds nothing to the small-signal circuit.
        for s in ir.get("internal_sources", []):
            if s.get("kind", "V") == "V":
                ground.add(s["p"])
                ground.add(s["n"])
        known_nets = {n["name"] for n in ir["nets"]}
        for a_, b_, _ in (extra_c or []):
            for n_ in (a_, b_):
                if n_ is not None and n_ not in known_nets:
                    raise KeyError(f"extra_c on unknown net {n_}")
        devnames = {d["name"] for d in ir["devices"]}
        for d_, t_, _ in (extra_r or []):
            if d_ not in devnames or t_ not in TERMS:
                raise KeyError(f"extra_r on unknown terminal {d_}.{t_}")
        self.drive = drive or {n: (0.5 if i == 0 else -0.5)
                               for i, n in enumerate([p["name"] for p in ir["ports"] if p["role"] == "input"])}
        nets = [n["name"] for n in ir["nets"]]
        split = {(d, t): r for d, t, r in (extra_r or [])}
        self.unknown = [n for n in nets if n not in ground and n not in self.drive] + [f"{d}.{t}" for d, t in split]
        self.known = list(self.drive)
        self.idx = {n: i for i, n in enumerate(self.unknown + self.known)}
        self.ground = ground
        n = len(self.idx)
        self.G = np.zeros((n, n))
        self.C = np.zeros((n, n))
        for (d, t), r in split.items():  # series resistor: internal node <-> original net
            net = next(x for x in ir["devices"] if x["name"] == d)["terminals"][t]
            self._cond(self.idx[f"{d}.{t}"], self.idx.get(net), 1.0 / r)
        for d in ir["devices"]:
            o = op[d["name"]]
            t = d["terminals"]
            ix = {k: (self.idx[f"{d['name']}.{k}"] if (d["name"], k) in split else self.idx.get(t[k]))
                  for k in TERMS}  # None = AC ground
            self._vccs(ix["d"], ix["s"], ix["g"], ix["s"], o["gm"])
            self._vccs(ix["d"], ix["s"], ix["b"], ix["s"], o["gmbs"])
            self._vccs(ix["d"], ix["s"], ix["d"], ix["s"], o["gds"])
            for (i, j), key in CMAT.items():
                if ix[i] is not None and ix[j] is not None:
                    self.C[ix[i], ix[j]] += o[key]
            for a, b, key in (("g", "s", "cgso"), ("g", "d", "cgdo"), ("g", "b", "cgbo"),
                              ("b", "d", "capbd"), ("b", "s", "capbs")):
                self._cap(ix[a], ix[b], o.get(key) or 0.0)  # missing optional param -> 0, reported by G1.1
        for c in ir.get("passives", []):
            a_, b_ = self.idx.get(c["a"]), self.idx.get(c["b"])
            if c["kind"] == "C":
                self._cap(a_, b_, c["value"])
            else:
                self._cond(a_, b_, 1.0 / c["value"])
        cl = parse_si(ir["conditions"].get("CL_F", 0))
        outs = [p for p in ir["ports"] if p["role"] == "output"]
        # single-ended output: H = v(out); differential output (dido): H = v(OUTP) - v(OUTN), CL on each
        self.out = outs[0]["name"]
        self.out_sign = {p["name"]: (-1.0 if p.get("testbench_port") == "OUTN" else 1.0) for p in outs}
        for o in outs:
            self._cap(self.idx.get(o["name"]), None, cl)
        for a, b, c in (extra_c or []):
            self._cap(self.idx.get(a), self.idx.get(b) if b else None, c)

    def _vccs(self, p, n, cp, cn, g):
        for row, sr in ((p, 1.0), (n, -1.0)):
            if row is None:
                continue
            if cp is not None:
                self.G[row, cp] += sr * g
            if cn is not None:
                self.G[row, cn] -= sr * g

    def _cond(self, a, b, g):
        for i, j, sg in ((a, a, 1), (b, b, 1), (a, b, -1), (b, a, -1)):
            if i is not None and j is not None:
                self.G[i, j] += sg * g

    def _cap(self, a, b, c):
        for i, j, s in ((a, a, 1), (b, b, 1), (a, b, -1), (b, a, -1)):
            if i is not None and j is not None:
                self.C[i, j] += s * c

    def response(self, f: np.ndarray) -> np.ndarray:
        nu = len(self.unknown)
        vk = np.array([self.drive[k] for k in self.known], dtype=complex)
        outs = [(self.idx[o], sg) for o, sg in self.out_sign.items()]
        H = np.empty(len(f), dtype=complex)
        for i, fi in enumerate(f):
            Y = self.G + 1j * 2 * np.pi * fi * self.C
            v = np.linalg.solve(Y[:nu, :nu], -Y[:nu, nu:] @ vk)
            H[i] = sum(sg * v[k] for k, sg in outs)
        return H

    def dc_node_resistance(self) -> dict:
        nu = len(self.unknown)
        Rm = np.linalg.inv(self.G[:nu, :nu])
        return {n: float(Rm[i, i]) for i, n in enumerate(self.unknown)}

    def node_capacitance(self) -> dict:
        nu = len(self.unknown)
        return {n: float(self.C[i, i]) for i, n in enumerate(self.unknown[:nu])}


FREQ = np.logspace(0, 9, 9 * 40 + 1)  # dec 40 from 1 Hz to 1 GHz, as the AC testbench


def metrics(H: np.ndarray, f: np.ndarray = FREQ) -> dict:
    db = 20 * np.log10(np.abs(H))
    ph = np.degrees(np.unwrap(np.angle(H)))
    gain = float(db[0])
    k = np.where((db[:-1] > 0) & (db[1:] <= 0))[0]
    if len(k) == 0:
        return {"gain_db": gain, "gbw_mhz": None, "pm_deg": None}
    k = k[0]
    t = db[k] / (db[k] - db[k + 1])
    fu = f[k] + t * (f[k + 1] - f[k])
    ph_u = ph[k] + t * (ph[k + 1] - ph[k])
    return {"gain_db": gain, "gbw_mhz": float(fu / 1e6), "pm_deg": float(180 + (ph_u - ph[0]))}


def sensitivities(ir, op, nets_gnd: list, pairs: list, delta: float = 1e-15, drive: dict | None = None) -> dict:
    """Central differences on the linear model: dM/dC per fF for caps to ground and couplings."""
    base = metrics(LinearModel(ir, op, drive=drive).response(FREQ))
    out = {}
    for label, a, b in [(n, n, None) for n in nets_gnd] + [(f"{a}~{b}", a, b) for a, b in pairs]:
        mp = metrics(LinearModel(ir, op, drive=drive, extra_c=[(a, b, delta)]).response(FREQ))
        mm = metrics(LinearModel(ir, op, drive=drive, extra_c=[(a, b, -delta)]).response(FREQ))
        out[label] = {k: (None if mp[k] is None or mm[k] is None else (mp[k] - mm[k]) / (2 * delta / 1e-15))
                      for k in base}  # per fF
    return {"base": base, "per_fF": out}


def sensitivities_r(ir, op, groups: list, delta: float = 5.0, drive: dict | None = None) -> dict:
    """Central differences on the linear model: dM/dR per ohm of series resistance at device
    terminals. groups: [(id, [(device, terminal), ...])]; every member of a group gets the same
    resistor (matched devices are wired symmetrically, so their parasitics are varied together).
    The response is analytic in the conductance, so -delta (a negative resistor) is a valid step."""
    base = metrics(LinearModel(ir, op, drive=drive).response(FREQ))
    out = {}
    for gid, members in groups:
        mp = metrics(LinearModel(ir, op, drive=drive, extra_r=[(d, t, delta) for d, t in members]).response(FREQ))
        mm = metrics(LinearModel(ir, op, drive=drive, extra_r=[(d, t, -delta) for d, t in members]).response(FREQ))
        out[gid] = {k: (None if mp[k] is None or mm[k] is None else (mp[k] - mm[k]) / (2 * delta)) for k in base}
    return {"base": base, "per_ohm": out}


def evaluate(ir, op, extra_c=None, extra_r=None, drive=None) -> dict:
    """Metrics with a set of parasitics inserted at once (used by S2 to check a whole budget)."""
    return metrics(LinearModel(ir, op, drive=drive, extra_c=extra_c, extra_r=extra_r).response(FREQ))


# ---------------------------------------------------------------- fast, exact metric changes (plan v2, PVT)
def _h(G, C, nu, vk, outs, f):
    Y = G + 1j * 2 * np.pi * f * C
    v = np.linalg.solve(Y[:nu, :nu], -Y[:nu, nu:] @ vk)
    return sum(sg * v[k] for k, sg in outs)


class FastModel:
    """The linear model's matrices kept, so that one capacitor can be added without rebuilding it, and the
    metrics found by root finding at the unity-gain frequency instead of a 361-point sweep. Used for the
    many per-corner sensitivities S2 needs; agrees with metrics() to its grid interpolation error."""

    def __init__(self, lm: "LinearModel"):
        self.lm = lm
        self.sys = self._sys(lm)
        self.G, self.C = lm.G, lm.C
        m = metrics(lm.response(FREQ))
        self.base = m
        self.fu = None if m["gbw_mhz"] is None else m["gbw_mhz"] * 1e6
        self.h1 = _h(self.G, self.C, *self.sys, 1.0)
        self.hu = None if self.fu is None else self._root(self.G, self.C, self.sys)[1]

    @staticmethod
    def _sys(lm):
        return (len(lm.unknown), np.array([lm.drive[k] for k in lm.known], dtype=complex),
                [(lm.idx[o], sg) for o, sg in lm.out_sign.items()])

    def _root(self, G, C, sys_):
        from scipy.optimize import brentq
        g = lambda lf: np.log(abs(_h(G, C, *sys_, 10 ** lf)))  # noqa: E731
        a, b = np.log10(self.fu) - 0.15, np.log10(self.fu) + 0.15
        ga, gb = g(a), g(b)
        k = 0
        while ga * gb > 0 and k < 8:
            a, b = a - 0.3, b + 0.3
            ga, gb = g(a), g(b)
            k += 1
        lf = brentq(g, a, b, xtol=1e-10)
        return 10 ** lf, _h(G, C, *sys_, 10 ** lf)

    def delta(self, G, C, sys_=None) -> dict:
        """Change of gain_db, gbw_mhz, pm_deg from the base for modified matrices (same nodes unless sys_)."""
        sys_ = sys_ or self.sys
        h1 = _h(G, C, *sys_, 1.0)
        out = {"gain_db": float(20 * np.log10(abs(h1) / abs(self.h1)))}
        if self.fu is None:
            return {**out, "gbw_mhz": None, "pm_deg": None}
        fu, hu = self._root(G, C, sys_)
        out["gbw_mhz"] = (fu - self.fu) / 1e6
        out["pm_deg"] = float(np.degrees(np.angle(hu / self.hu)) - np.degrees(np.angle(h1 / self.h1)))
        return out

    def delta_lm(self, lm2: "LinearModel") -> dict:
        return self.delta(lm2.G, lm2.C, self._sys(lm2))

    def cap_matrices(self, a, b, c: float):
        C = self.C.copy()
        ia = self.lm.idx.get(a) if a else None
        ib = self.lm.idx.get(b) if b else None
        for i, j, s_ in ((ia, ia, 1), (ib, ib, 1), (ia, ib, -1), (ib, ia, -1)):
            if i is not None and j is not None:
                C[i, j] += s_ * c
        return self.G, C

    def rates_c(self, a, b, delta=1e-15) -> dict:
        p = self.delta(*self.cap_matrices(a, b, delta))
        m = self.delta(*self.cap_matrices(a, b, -delta))
        return {k: (None if p[k] is None or m[k] is None else (p[k] - m[k]) / (2 * delta / 1e-15)) for k in p}
