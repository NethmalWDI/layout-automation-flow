#!/usr/bin/env python3
"""Flatten a hierarchical xschem/SPICE netlist into one subcircuit the flow can ingest.

Instances of subcircuits defined in the file are expanded recursively; PDK devices (sky130_fd_pr__*)
and ideal elements are kept. Inside an instance, internal nets become '<inst>_<net>' and devices
'X<INST>_<dev>' (the X kept first so that SPICE still reads a subcircuit instance). xschem's
per-device expressions (ad, as, pd, ps, nrd, nrs as functions of W and nf) are evaluated to numbers,
so the flat netlist simulates identically and S0 can read every value. Nothing else is changed;
the instance multiplier m= and the PDK 'mult' are both kept.

usage: python3 scripts/flatten_spice.py <in.spice> <top subckt> <out.spice> [--name NEW]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PDK = re.compile(r"^sky130_fd_pr__\w+$", re.I)
PARAM = re.compile(r"(\w+)\s*=\s*('[^']*'|\S+)")


def logical(text: str) -> list[str]:
    out: list[str] = []
    for raw in text.splitlines():
        if raw.startswith("+") and out:
            out[-1] += " " + raw[1:].strip()
        else:
            out.append(raw.rstrip())
    return out


def read_subckts(text: str) -> dict:
    subs, cur = {}, None
    for ln in logical(text):
        s = ln.strip()
        m = re.match(r"^\*{0,2}\.subckt\s+(\S+)\s*(.*)$", s, re.I)
        if m:
            cur = {"name": m.group(1), "ports": [p for p in m.group(2).split() if "=" not in p], "lines": []}
            subs[cur["name"]] = cur
            continue
        if re.match(r"^\*{0,2}\.ends\b", s, re.I):
            cur = None
            continue
        if cur is not None and s and not s.startswith("*") and not s.startswith("."):
            cur["lines"].append(s)
    return subs


def eval_geom(params: dict) -> dict:
    """xschem sky130 MOSFET area/perimeter expressions -> numbers (same formulas, evaluated)."""
    W = float(params["W"])
    nf = int(float(params.get("nf", params.get("NF", 1))))
    env = {"W": W, "nf": nf, "int": int}
    out = {}
    for k, v in params.items():
        if isinstance(v, str) and v.startswith("'") and v.endswith("'"):
            out[k] = f"{eval(v.strip(chr(39)), {'__builtins__': {}}, env):.6g}"  # noqa: S307 (fixed formulas)
        else:
            out[k] = v
    return out


def expand(subs: dict, name: str, conn: dict, prefix: str, out: list, stats: dict) -> None:
    sc = subs[name]
    local = {}

    def net(n: str) -> str:
        if n in conn:
            return conn[n]
        if n.lower() in ("0", "gnd"):
            return n
        local.setdefault(n, f"{prefix}{n}" if prefix else n)
        return local[n]

    for ln in sc["lines"]:
        tok = ln.split()
        kind = tok[0][0].upper()
        if kind == "X":
            mi = next((i for i, t in enumerate(tok[1:], 1) if PDK.match(t) or t in subs), None)
            if mi is None:
                raise SystemExit(f"{name}: cannot resolve instance '{ln}'")
            model, nodes, rest = tok[mi], tok[1:mi], tok[mi + 1:]
            dev = tok[0]
            if model in subs:
                child = subs[model]
                if len(nodes) != len(child["ports"]):
                    raise SystemExit(f"{dev}: {len(nodes)} nodes for {model} with {len(child['ports'])} ports")
                cconn = {p: net(n) for p, n in zip(child["ports"], nodes)}
                expand(subs, model, cconn, f"{prefix}{dev.lower()}_", out, stats)
                stats["instances"] += 1
                continue
            params = dict(PARAM.findall(" ".join(rest)))
            if re.match(r"sky130_fd_pr__[np]fet", model):
                params = eval_geom(params)
            newname = f"X{prefix.upper()}{dev[1:]}" if prefix else dev
            out.append(f"{newname} {' '.join(net(n) for n in nodes)} {model} " +
                       " ".join(f"{k}={v}" for k, v in params.items()))
            stats["devices"] += 1
        elif kind in "RCVIL":
            newname = f"{tok[0][0]}{prefix.upper()}{tok[0][1:]}" if prefix else tok[0]
            out.append(f"{newname} {net(tok[1])} {net(tok[2])} {' '.join(tok[3:])}")
            stats["elements"] += 1
        else:
            raise SystemExit(f"{name}: unsupported element '{ln}'")


def flatten(src: Path, top: str, dst: Path, new_name: str | None = None) -> dict:
    text = src.read_text()
    subs = read_subckts(text)
    if top not in subs:
        raise SystemExit(f"top {top} not in {src} (found {sorted(subs)})")
    # xschem port directions of the top
    dirs = re.findall(r"^\*\.(ipin|opin|iopin)\s+(\S+)", text, re.M)
    top_dirs = []
    seen = set()
    for d, n in dirs:
        if n in subs[top]["ports"] and n not in seen:
            top_dirs.append(f"*.{d} {n}")
            seen.add(n)
    out: list[str] = []
    stats = {"devices": 0, "elements": 0, "instances": 0}
    expand(subs, top, {p: p for p in subs[top]["ports"]}, "", out, stats)
    name = new_name or top
    dst.write_text(f"* {name}: flat copy of subckt {top} from {src.name} (scripts/flatten_spice.py)\n"
                   f".subckt {name} {' '.join(subs[top]['ports'])}\n" + "\n".join(top_dirs) + "\n" +
                   "\n".join(out) + f"\n.ends {name}\n")
    return {"ports": subs[top]["ports"], **stats}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("top")
    ap.add_argument("dst")
    ap.add_argument("--name")
    a = ap.parse_args()
    print(flatten(Path(a.src), a.top, Path(a.dst), a.name))
    sys.exit(0)
