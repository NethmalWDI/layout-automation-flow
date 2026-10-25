"""S3 step 2 — evaluate device options in the circuit, with the unchanged upstream testbenches.

A device line of the DUT is replaced by its option's extracted device cell (Magic, cthresh 0: finger
devices with their ad/as/pd/ps plus the capacitances drawn inside the cell), and the access resistance of
each terminal (options.access_resistance) is inserted in series:

    XM1 d g s b <model> ...   ->   XM1 d' g' s' b s3c_<cell>       (ports matched by name D/G/S/B)
                                   Rs3_XM1_d d' d R_d  (same for g, s)

Matched devices are replaced together with the same option. AC, NOISE and the OP (with one finger of
each replaced device probed for Vds - Vdsat) are run; results are compared with the S0 baseline.
"""
from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.common.tools import REPO, run_ngspice_text
from src.s1 import op as opmod, resistance

POS = {"d": 1, "g": 2, "s": 3, "b": 4}


def cell_subckt(rec: dict) -> tuple[str, str, list]:
    """Rename the extracted subcircuit to a unique name; return (name, text, ports).
    Magic names the substrate VSUBS; inside a subcircuit that node would float (only capacitors reach
    it), the DC matrix becomes singular and ngspice's gmin stepping can settle on a wrong operating
    point. VSUBS is therefore made a port ('SUB') and tied to the circuit's ground."""
    txt = (REPO / rec["pex"]["file"]).read_text()
    old = rec["pex"]["subckt"]
    name = f"s3c_{rec['cell']}".lower()
    body = re.search(rf"^\.subckt\s+{re.escape(old)}\b.*?^\.ends.*?$", txt, re.M | re.S | re.I).group(0)
    ports = list(rec["pex"]["ports"])
    head = f".subckt {name} " + " ".join(ports)
    if re.search(r"\bVSUBS\b", body):
        body = re.sub(r"\bVSUBS\b", "SUB", body)
        head += " SUB"
        ports.append("SUB")
    body = re.sub(rf"^\.subckt\s+{re.escape(old)}\b[^\n]*", head, body, count=1, flags=re.M | re.I)
    return name, body + "\n", ports


def replace_devices(deck: str, dut: str, repl: dict, gnd: str = "VSS") -> str:
    """repl: {device: (rec, R dict or None)}; rewrites those device lines inside the DUT subcircuit and
    appends the cell subcircuits before .end. R None = cell only, no access resistance."""
    lines = deck.splitlines(keepends=True)
    inside = False
    defs = {}
    for i, ln in enumerate(lines):
        low = ln.strip().lower()
        if low.startswith(".subckt") and len(low.split()) > 1 and low.split()[1] == dut.lower():
            inside = True
            continue
        if inside and low.startswith(".ends"):
            break
        tok = ln.split()
        if inside and tok and tok[0] in repl:
            rec, R = repl[tok[0]]
            name, body, ports = cell_subckt(rec)
            defs[name] = body
            net = {t: tok[POS[t]] for t in POS}
            if R is None:
                inner = dict(net)
                res = ""
            else:
                inner = {t: (f"s3_{tok[0]}_{t}" if t != "b" else net["b"]) for t in POS}
                res = "".join(f"Rs3_{tok[0]}_{t} {inner[t]} {net[t]} {R[t]:.6g}\n" for t in ("d", "g", "s"))
            inner["sub"] = gnd
            inst = f"{tok[0]} " + " ".join(inner[p.lower()] for p in ports) + f" {name}\n"
            lines[i] = inst + res
    if not inside:
        raise RuntimeError(f"DUT subcircuit {dut} not found in the testbench")
    done = {ln.split()[0] for ln in lines if ln.split() and ln.split()[1:2] and " s3c_" in ln}
    missing = [d for d in repl if d not in done]
    if missing:
        raise RuntimeError(f"devices not replaced: {missing}")
    txt = "".join(lines)
    extra = "".join(defs.values())
    m = re.search(r"^\.end\s*$", txt, re.M | re.I)
    return txt[:m.start()] + extra + txt[m.start():] if m else txt + extra


def finger_path(dev: str, rec: dict, model: str) -> str:
    first = rec["pex"]["fingers"] and re.search(r"^(X\S*)\s", (REPO / rec["pex"]["file"]).read_text(), re.M)
    x0 = first.group(1).lower() if first else "x0"
    return f"m.x1.xdut.{dev.lower()}.{x0}.m{model.lower()}"


def scenario_jobs(s0: Path, ir: dict, repl: dict, work: Path) -> list:
    tb = s0 / "tb"
    dut = ir["subckt"]
    gnd = next(p["name"] for p in ir["ports"] if p["role"] == "ground")
    devs = {d["name"]: d for d in ir["devices"]}
    paths = {d: finger_path(d, rec, devs[d]["model"]) for d, (rec, _) in repl.items()}
    ac = replace_devices((tb / "diso_amp_AC.spice").read_text(), dut, repl, gnd)
    nz = replace_devices((tb / "diso_amp_NOISE.spice").read_text(), dut, repl, gnd)
    work.mkdir(parents=True, exist_ok=True)
    opsrc = work / "op_src.spice"
    opsrc.write_text(replace_devices((tb / "diso_amp_OP.spice").read_text(), dut, repl, gnd))
    op = opmod.op_deck(opsrc, ir["devices"], paths)
    meas = (tb / "diso_amp_OP.spice").read_text()
    return [("ac", ac, work), ("noise", nz, work), ("op", op, work),
            ("opmeas", replace_devices(meas, dut, repl, gnd), work)]


def run_jobs(jobs: list, workers: int = 4) -> list:
    def one(j):
        tag, kind, txt, wd = j
        r = run_ngspice_text(txt, wd / kind, kind)
        if r["rc"] != 0 or r.get("numerical_warnings"):   # a doubtful operating point is a failed run
            return tag, kind, None
        if kind == "op":
            return tag, kind, resistance._sat_from_log((wd / kind / "op.log").read_text())
        return tag, kind, r["meas"] or None
    with ThreadPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(one, jobs))


def collect(results: list) -> dict:
    """{tag: merged measurements}; a failed run marks the tag with 'failed': [kinds]."""
    out: dict = {}
    for tag, kind, r in results:
        o = out.setdefault(tag, {})
        if r is None:
            o.setdefault("failed", []).append(kind)
            continue
        if kind == "op":
            o["sat_V"] = r["vds_minus_vdsat_V"]
            o["vout_V"] = r.get("vout_V")
            o["op_params"] = {d: {k: v.get(k) for k in ("id", "gm", "gds", "vth", "vdsat")}
                              for d, v in (r.get("params") or {}).items()}
        else:
            o.update(r)
    return out
