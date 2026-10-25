"""S1 step 2 — exact small-signal (linearised) model of the whole circuit at its operating point.

Each MOSFET is stamped with:
  * gm, gmbs, gds (VCCS + conductance, current defined into the drain),
  * the full BSIM4 intrinsic charge matrix C_ij = dQ_i/dV_j (non-reciprocal, quasi-static),
  * overlap caps cgso/cgdo/cgbo and junction caps capbd/capbs (reciprocal).
Nodes: supplies, ground, and nodes held by ideal bias sources are AC ground; inputs are driven
(INP = +0.5, INN = -0.5, as in the AC testbench); every other net is solved.
Metrics replicate the testbench definitions (diso_amp_AC): gain at 1 Hz, UGB where |H| = 1
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
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().lower()
    mult = {"f": 1e-15, "p": 1e-12, "n": 1e-9, "u": 1e-6, "m": 1e-3, "k": 1e3, "meg": 1e6, "g": 1e9}
    for suf in ("meg", "f", "p", "n", "u", "m", "k", "g"):
        if s.endswith(suf):
            return float(s[: -len(suf)]) * mult[suf]
    return float(s)


class LinearModel:
    def __init__(self, ir: dict, op: dict, drive: dict | None = None, extra_c: list | None = None):
        """ir: circuit_ir; op: per-device OP dict; drive: known AC node voltages;
        extra_c: [(netA, netB_or_None, farads)] added capacitors (None = to ground)."""
        roles = {p["name"]: p["role"] for p in ir["ports"]}
        ground = {n for n, r in roles.items() if r in ("ground", "supply")}
        for s in ir.get("internal_sources", []):
            ground.add(s["p"])
            ground.add(s["n"])
        self.drive = drive or {n: (0.5 if i == 0 else -0.5)
                               for i, n in enumerate([p["name"] for p in ir["ports"] if p["role"] == "input"])}
        nets = [n["name"] for n in ir["nets"]]
        self.unknown = [n for n in nets if n not in ground and n not in self.drive]
        self.known = list(self.drive)
        self.idx = {n: i for i, n in enumerate(self.unknown + self.known)}
        self.ground = ground
        n = len(self.idx)
        self.G = np.zeros((n, n))
        self.C = np.zeros((n, n))
        for d in ir["devices"]:
            o = op[d["name"]]
            t = d["terminals"]
            ix = {k: self.idx.get(t[k]) for k in TERMS}  # None = AC ground
            self._vccs(ix["d"], ix["s"], ix["g"], ix["s"], o["gm"])
            self._vccs(ix["d"], ix["s"], ix["b"], ix["s"], o["gmbs"])
            self._vccs(ix["d"], ix["s"], ix["d"], ix["s"], o["gds"])
            for (i, j), key in CMAT.items():
                if ix[i] is not None and ix[j] is not None:
                    self.C[ix[i], ix[j]] += o[key]
            for a, b, key in (("g", "s", "cgso"), ("g", "d", "cgdo"), ("g", "b", "cgbo"),
                              ("b", "d", "capbd"), ("b", "s", "capbs")):
                self._cap(ix[a], ix[b], o.get(key) or 0.0)  # missing optional param -> 0, reported by G1.1
        cl = parse_si(ir["conditions"].get("CL_F", 0))
        out = [p["name"] for p in ir["ports"] if p["role"] == "output"][0]
        self.out = out
        self._cap(self.idx.get(out), None, cl)
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

    def _cap(self, a, b, c):
        for i, j, s in ((a, a, 1), (b, b, 1), (a, b, -1), (b, a, -1)):
            if i is not None and j is not None:
                self.C[i, j] += s * c

    def response(self, f: np.ndarray) -> np.ndarray:
        nu = len(self.unknown)
        vk = np.array([self.drive[k] for k in self.known], dtype=complex)
        out_i = self.idx[self.out]
        H = np.empty(len(f), dtype=complex)
        for i, fi in enumerate(f):
            Y = self.G + 1j * 2 * np.pi * fi * self.C
            v = np.linalg.solve(Y[:nu, :nu], -Y[:nu, nu:] @ vk)
            H[i] = v[out_i]
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


def sensitivities(ir, op, nets_gnd: list, pairs: list, delta: float = 1e-15) -> dict:
    """Central differences on the linear model: dM/dC per fF for caps to ground and couplings."""
    base = metrics(LinearModel(ir, op).response(FREQ))
    out = {}
    for label, a, b in [(n, n, None) for n in nets_gnd] + [(f"{a}~{b}", a, b) for a, b in pairs]:
        mp = metrics(LinearModel(ir, op, extra_c=[(a, b, delta)]).response(FREQ))
        mm = metrics(LinearModel(ir, op, extra_c=[(a, b, -delta)]).response(FREQ))
        out[label] = {k: (None if mp[k] is None or mm[k] is None else (mp[k] - mm[k]) / 2)
                      for k in base}  # per fF (delta = 1 fF)
    return {"base": base, "per_fF": out}
