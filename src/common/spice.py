"""Minimal, strict SPICE reader/writer for sized SKY130 transistor netlists (xschem style).

Supported elements: X<name> MOSFET instances of sky130_fd_pr__{n,p}fet_* models,
X<name> PDK passives (sky130_fd_pr__cap_* / sky130_fd_pr__res_*), V<name> and I<name> independent
sources, R/C ideal passives. Anything else raises SpiceError, because silently skipping an element
would change the circuit.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

MOS_MODEL_RE = re.compile(r"^sky130_fd_pr__([np])fet_\w+$", re.I)
PDK_PASSIVE_RE = re.compile(r"^sky130_fd_pr__(cap|res)_\w+$", re.I)
SI = {"t": 1e12, "g": 1e9, "meg": 1e6, "k": 1e3, "m": 1e-3, "u": 1e-6, "n": 1e-9, "p": 1e-12, "f": 1e-15}


def si(text) -> float:
    """SPICE number with an optional scale suffix ('10u', '1e-05', '0.5p', '2meg', '200fF')."""
    if isinstance(text, (int, float)):
        return float(text)
    s_ = str(text).strip().strip("'").lower()
    m = re.fullmatch(r"([-+]?(?:\d+\.?\d*|\.\d+)(?:e[-+]?\d+)?)(meg|[tgkmunpf])?[a-z]*", s_)
    if not m:
        raise SpiceError(f"not a number: {text!r}")
    return float(f"{float(m.group(1)) * (SI[m.group(2)] if m.group(2) else 1.0):.15g}")
PARAM_RE = re.compile(r"(\w+)\s*=\s*('[^']*'|\S+)")


class SpiceError(ValueError):
    """Raised for anything the reader refuses to interpret."""


@dataclass
class Mosfet:
    name: str
    d: str
    g: str
    s: str
    b: str
    model: str
    params: dict  # UPPER-case keys, raw string values
    line_no: int

    @property
    def polarity(self) -> str:
        m = MOS_MODEL_RE.match(self.model)
        return "nmos" if m and m.group(1).lower() == "n" else "pmos"

    def num(self, key: str, default=None) -> float:
        v = self.params.get(key.upper(), default)
        if v is None:
            raise SpiceError(f"{self.name}: parameter {key} missing (line {self.line_no})")
        return float(v)

    @property
    def terminals(self) -> dict:
        return {"d": self.d, "g": self.g, "s": self.s, "b": self.b}


@dataclass
class Source:
    name: str
    p: str
    n: str
    value: str
    line_no: int

    @property
    def kind(self) -> str:
        """'V' (voltage) or 'I' (current; flows from p through the source to n)."""
        return self.name[0].upper()

    @property
    def dc(self) -> float | None:
        """The DC value: 'DC 10u', '0.75', 'dc 0.9 ac 1' -> number; None if there is none."""
        tok = self.value.replace("=", " ").split()
        for i, t in enumerate(tok):
            if t.lower() == "dc" and i + 1 < len(tok):
                return si(tok[i + 1])
        try:
            return si(tok[0]) if tok else None
        except SpiceError:
            return None


@dataclass
class Passive:
    name: str
    a: str
    b: str
    value: str
    line_no: int
    model: str = "ideal"        # 'ideal' (R/C element) or a PDK model (sky130_fd_pr__cap_mim_m3_1, ...)
    params: dict = field(default_factory=dict)   # PDK device parameters (UPPER-case keys)
    body: str | None = None     # third terminal of a PDK resistor

    @property
    def kind(self) -> str:
        """'C' or 'R'."""
        if self.model == "ideal":
            return self.name[0].upper()
        return "C" if "__cap_" in self.model.lower() else "R"

    @property
    def nominal(self) -> float | None:
        """Value in F or ohm. Ideal: the number on the line. PDK MIM capacitor: the tt model's area term
        (sw_cap_mim_ca = 2 fF/um^2 on (W + 0.15 um)(L + 0.15 um), models_capacitors.spice). Other PDK
        devices: None (S1 reads the simulator's value)."""
        if self.model == "ideal":
            return si(self.value.split()[0])
        if re.match(r"sky130_fd_pr__cap_mim_m[34]_[12]$", self.model, re.I):
            w, l_ = float(self.params["W"]), float(self.params["L"])
            mult = float(self.params.get("MF", self.params.get("MULT", self.params.get("M", 1))))
            return 2e-15 * (w + 0.15) * (l_ + 0.15) * mult
        return None

    def line(self) -> str:
        if self.model == "ideal":
            return f"{self.name} {self.a} {self.b} {self.value}"
        nodes = [self.a, self.b] + ([self.body] if self.body else [])
        return f"{self.name} {' '.join(nodes)} {self.model} " + " ".join(f"{k}={v}" for k, v in self.params.items())


@dataclass
class Netlist:
    name: str
    ports: list
    port_dirs: dict = field(default_factory=dict)  # from xschem *.ipin/*.opin/*.iopin
    mosfets: list = field(default_factory=list)
    sources: list = field(default_factory=list)
    passives: list = field(default_factory=list)

    def nets(self) -> dict:
        """net -> list of (element, terminal)."""
        out: dict = {}
        for m in self.mosfets:
            for t, n in m.terminals.items():
                out.setdefault(n, []).append((m.name, t))
        for s in self.sources:
            out.setdefault(s.p, []).append((s.name, "p"))
            out.setdefault(s.n, []).append((s.name, "n"))
        for p in self.passives:
            out.setdefault(p.a, []).append((p.name, "a"))
            out.setdefault(p.b, []).append((p.name, "b"))
            if p.body:
                out.setdefault(p.body, []).append((p.name, "body"))
        return out


def logical_lines(text: str):
    """Yield (line_no, text) with '+' continuations joined."""
    cur, cur_no = None, 0
    for i, raw in enumerate(text.splitlines(), start=1):
        if raw.startswith("+"):
            if cur is None:
                raise SpiceError(f"continuation without a line at {i}")
            cur += " " + raw[1:].strip()
            continue
        if cur is not None:
            yield cur_no, cur
        cur, cur_no = raw.strip(), i
    if cur is not None:
        yield cur_no, cur


def parse(path: Path, subckt: str | None = None) -> Netlist:
    """Parse the first (or the named) subcircuit; xschem's commented '**.subckt' header is accepted."""
    text = Path(path).read_text()
    nl: Netlist | None = None
    port_dirs: dict = {}
    inside = False
    for no, ln in logical_lines(text):
        if not ln:
            continue
        hdr = re.match(r"^\*{0,2}\.subckt\s+(\S+)\s*(.*)$", ln, re.I)
        if hdr and nl is None and (subckt is None or hdr.group(1) == subckt):
            nl = Netlist(name=hdr.group(1), ports=hdr.group(2).split())
            inside = True
            continue
        if re.match(r"^\*{0,2}\.ends\b", ln, re.I):
            if inside:
                break
            continue
        pin = re.match(r"^\*\.(ipin|opin|iopin)\s+(\S+)", ln, re.I)
        if pin:
            port_dirs[pin.group(2)] = {"ipin": "input", "opin": "output", "iopin": "inout"}[pin.group(1).lower()]
            continue
        if ln.startswith("*") or ln.startswith("."):
            continue
        if not inside:
            continue
        tok = ln.split()
        kind = tok[0][0].upper()
        if kind == "X":
            if len(tok) >= 6 and MOS_MODEL_RE.match(tok[5]):
                params = {k.upper(): v for k, v in PARAM_RE.findall(" ".join(tok[6:]))}
                nl.mosfets.append(Mosfet(tok[0], tok[1], tok[2], tok[3], tok[4], tok[5], params, no))
                continue
            mi = next((i for i, t in enumerate(tok) if PDK_PASSIVE_RE.match(t)), None)
            if mi is None or mi not in (3, 4):
                raise SpiceError(f"line {no}: unsupported subcircuit instance '{ln}'")
            params = {k.upper(): v for k, v in PARAM_RE.findall(" ".join(tok[mi + 1:]))}
            nl.passives.append(Passive(tok[0], tok[1], tok[2], "", no, model=tok[mi], params=params,
                                       body=tok[3] if mi == 4 else None))
        elif kind in "VI":
            nl.sources.append(Source(tok[0], tok[1], tok[2], " ".join(tok[3:]), no))
        elif kind in "RC":
            nl.passives.append(Passive(tok[0], tok[1], tok[2], " ".join(tok[3:]), no))
        else:
            raise SpiceError(f"line {no}: unsupported element '{tok[0]}'")
    if nl is None:
        raise SpiceError(f"{path}: no subckt{' ' + subckt if subckt else ''} found")
    nl.port_dirs = port_dirs
    return nl


def validate(nl: Netlist, allowed_models: list) -> list:
    """Return a list of problems (empty = valid)."""
    errs = []
    names = [e.name for e in nl.mosfets + nl.sources + nl.passives]
    for n in sorted({x for x in names if names.count(x) > 1}):
        errs.append(f"duplicate element name {n}")
    for m in nl.mosfets:
        if m.model not in allowed_models:
            errs.append(f"{m.name}: model {m.model} not in allowed set {allowed_models}")
        for key in ("W", "L"):
            if key not in m.params:
                errs.append(f"{m.name}: {key} missing")
            else:
                try:
                    if float(m.params[key]) <= 0:
                        errs.append(f"{m.name}: {key} must be > 0")
                except ValueError:
                    errs.append(f"{m.name}: {key}={m.params[key]} is not a number")
    nets = nl.nets()
    for p in nl.ports:
        if p not in nets:
            errs.append(f"port {p} is not connected to any element")
    for n, conns in nets.items():
        if n not in nl.ports and len(conns) < 2:
            errs.append(f"net {n} is dangling (only {conns})")
    return errs


def mos_line(name: str, t: dict, model: str, params: dict) -> str:
    ps = " ".join(f"{k}={v}" for k, v in params.items())
    return f"{name} {t['d']} {t['g']} {t['s']} {t['b']} {model} {ps}"
