"""S1 extension — series resistance at device terminals.

Wiring and PCell access resistance sit between a transistor terminal and its net. For every
device terminal (d, g, s) this computes
  * dM/dR per ohm for gain/GBW/PM from the exact linear model (node splitting, linear.py), and
  * transistor-level SPICE finite differences at two resistor values for
      - AC  (gain, GBW, PM),
      - NOISE (spot noise at 1 kHz and integrated noise; resistor thermal noise is included by ngspice),
      - DC operating point (every device's Vds - Vdsat, supply current): the DC effect I*R that a
        small-signal model cannot show.
DC slopes are measured for every terminal (cheap OP runs); AC/NOISE slopes for the terminals that
the linear model ranks as most margin-consuming. Runs are independent and use a thread pool.
"""
from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.common.tools import bench, run_ngspice_text
from src.s1 import op as opmod

POS = {"d": 1, "g": 2, "s": 3, "b": 4}  # token index on an X-MOSFET line: Xname d g s b model ...


def deck_with_res(deck_txt: str, dut: str, dev: str, term: str, ohms: float) -> str:
    """Insert a series resistor between <dev>.<term> and its net inside the DUT subcircuit."""
    lines = deck_txt.splitlines(keepends=True)
    inside, done = False, False
    for i, ln in enumerate(lines):
        low = ln.strip().lower()
        if low.startswith(".subckt") and low.split()[1] == dut.lower():
            inside = True
            continue
        if inside and low.startswith(".ends"):
            break
        if inside and ln.split() and ln.split()[0].lower() == dev.lower():
            tok = ln.split()
            net = tok[POS[term]]
            new = f"s1r_{dev}_{term}"
            tok[POS[term]] = new
            lines[i] = " ".join(tok) + "\n" + f"Rpar_s1_{dev}_{term} {new} {net} {ohms:g}\n"
            done = True
            break
    if not done:
        raise RuntimeError(f"device {dev} not found inside .subckt {dut}")
    return "".join(lines)


def _sat_from_log(log: str) -> dict:
    """Saturation headroom, supply current, output voltage, and every probed device parameter."""
    vals: dict = {}
    for m in re.finditer(r"^OPV (\S+) (\S+) (\S+)", log, re.M):
        try:
            vals.setdefault(m.group(1), {})[m.group(2)] = float(m.group(3))
        except ValueError:
            pass
    sat = {d: abs(v["vds"]) - abs(v["vdsat"]) for d, v in vals.items() if "vds" in v and "vdsat" in v}
    isup = re.search(r"^OPI isup (\S+)", log, re.M)
    vout = re.search(r"^OPI vout (\S+)", log, re.M)
    return {"vds_minus_vdsat_V": sat, "isup_A": abs(float(isup.group(1))) if isup else None,
            "vout_V": float(vout.group(1)) if vout else None, "params": vals}


def _one(job):
    kind, deck_txt, work, name = job
    work = work / kind  # one folder per run: ngspice writes rawspice.raw into its cwd
    r = run_ngspice_text(deck_txt, work, name)
    if r["rc"] != 0 or r.get("numerical_warnings"):
        raise RuntimeError(f"ngspice run in {work} failed or reported numerical trouble: {r.get('numerical_warnings')}")
    if kind == "op":
        return _sat_from_log((work / f"{name}.log").read_text())
    return r["meas"]


def _with_res(txt: str, dut: str, members: list, ohms: float) -> str:
    for d, t in members:
        txt = deck_with_res(txt, dut, d, t, ohms)
    return txt


def dc_and_ac(s0_dir: Path, ir: dict, groups_dc: list, groups_ac: list, values: list, work: Path,
              workers: int = 4) -> dict:
    """groups_*: [(id, [(dev, term), ...])], every member gets the same resistor; values in ohms."""
    dut = ir["subckt"]
    tb = s0_dir / "tb"
    ac0 = bench(tb, "AC").read_text()
    nz0 = bench(tb, "NOISE").read_text()
    op_path = bench(tb, "OP")
    jobs = [("ac", ac0, work / "base", "ac"), ("noise", nz0, work / "base", "noise"),
            ("op", opmod.op_deck(op_path, ir["devices"]), work / "base", "op")]
    keys = [("base", "ac"), ("base", "noise"), ("base", "op")]
    tmp = work / "tmp_op"
    tmp.mkdir(parents=True, exist_ok=True)
    for gid, members in groups_dc:
        for v in values:
            mod = tmp / f"op_{gid.replace('+', '_')}_{v:g}.spice"
            mod.write_text(_with_res(op_path.read_text(), dut, members, v))
            jobs.append(("op", opmod.op_deck(mod, ir["devices"]), work / gid / f"{v:g}", "op"))
            keys.append((f"{gid}|{v:g}", "op"))
    for gid, members in groups_ac:
        for v in values:
            jobs.append(("ac", _with_res(ac0, dut, members, v), work / gid / f"{v:g}", "ac"))
            keys.append((f"{gid}|{v:g}", "ac"))
            jobs.append(("noise", _with_res(nz0, dut, members, v), work / gid / f"{v:g}", "noise"))
            keys.append((f"{gid}|{v:g}", "noise"))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        res = list(ex.map(_one, jobs))
    out: dict = {"base": {}, "cases": {}}
    for (case, kind), r in zip(keys, res):
        if case == "base":
            out["base"][kind] = r
        else:
            gid, v = case.split("|")
            out["cases"].setdefault(gid, {}).setdefault(f"{v}ohm", {})[kind] = r
    return out


def follower_deck(op_txt: str) -> str:
    """Unity-gain follower from the open-loop OP bench: the inverting input source is replaced by a
    0 V connection to the output, so V(OUT) - VCM is the input-referred offset (diso bench names)."""
    if re.search(r"^L\S*\s+OUT\S*\s+IN[NP]\s", op_txt, re.M | re.I):
        return op_txt   # the bench already closes the loop at DC (choke from the output to the input)
    out, n = re.subn(r"^Vinn\s+INN\s+0\s+.*$", "Vinn INN OUT 0", op_txt, count=1, flags=re.M | re.I)
    if n != 1:
        raise RuntimeError("follower: no 'Vinn INN 0 ...' line and no DC-feedback choke in the OP bench")
    return out


def offset_follower(s0_dir: Path, ir: dict, singles: list, values: list, work: Path, workers: int = 4) -> dict:
    """Systematic input offset of a one-sided series resistor, measured in a unity-gain follower
    (the output stays at its operating point, unlike in the open-loop bench)."""
    dut = ir["subckt"]
    base_txt = follower_deck(bench(s0_dir / "tb", "OP").read_text())
    tmp = work / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    (tmp / "base.spice").write_text(base_txt)
    jobs = [("op", opmod.op_deck(tmp / "base.spice", ir["devices"]), work / "base", "op")]
    keys = ["base"]
    for gid, members in singles:
        for v in values:
            f = tmp / f"{gid}_{v:g}.spice"
            f.write_text(_with_res(base_txt, dut, members, v))
            jobs.append(("op", opmod.op_deck(f, ir["devices"]), work / gid / f"{v:g}", "op"))
            keys.append(f"{gid}|{v:g}")
    with ThreadPoolExecutor(max_workers=workers) as ex:
        res = list(ex.map(_one, jobs))
    b = res[0]["vout_V"]
    out = {"base_vout_V": b, "terminals": {}}
    for k, r in zip(keys[1:], res[1:]):
        gid, v = k.split("|")
        out["terminals"].setdefault(gid, {})[f"{v}ohm"] = None if r["vout_V"] is None or b is None else \
            (r["vout_V"] - b) / float(v)
    return out


def slopes(fd: dict, values: list) -> dict:
    """Per terminal: slope per ohm at each resistor value for every measured quantity, plus the
    zero-step extrapolation from the two values (slope linear in R)."""
    b = fd["base"]
    res = {}
    for term, by_v in fd["cases"].items():
        row: dict = {}
        for kind in ("ac", "noise", "op"):
            if kind not in b:
                continue
            per_v = {}
            for v in values:
                r = by_v.get(f"{v:g}ohm", {}).get(kind)
                if r is None:
                    continue
                if kind == "op":
                    per_v[v] = {**{f"sat_{d}": (r["vds_minus_vdsat_V"][d] - b["op"]["vds_minus_vdsat_V"][d]) / v
                                   for d in r["vds_minus_vdsat_V"]},
                                "isup_ua": (r["isup_A"] - b["op"]["isup_A"]) * 1e6 / v,
                                "vout_V": (None if r.get("vout_V") is None or b["op"].get("vout_V") is None
                                           else (r["vout_V"] - b["op"]["vout_V"]) / v)}
                else:
                    per_v[v] = {k: (None if r.get(k) is None or b[kind].get(k) is None else (r[k] - b[kind][k]) / v)
                                for k in b[kind]}
            if not per_v:  # this quantity was not simulated for this terminal
                continue
            if len(per_v) == 2:
                v1, v2 = sorted(per_v)
                ext = {k: (None if per_v[v1][k] is None or per_v[v2][k] is None
                           else per_v[v1][k] - v1 * (per_v[v2][k] - per_v[v1][k]) / (v2 - v1))
                       for k in per_v[v1]}
            else:
                ext = None
            row[kind] = {"per_ohm": {f"{v:g}ohm": s for v, s in per_v.items()}, "extrapolated_0": ext}
        res[term] = row
    return res
