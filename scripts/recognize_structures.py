#!/usr/bin/env python3
"""A small rule-based structure recogniser: groups the transistors of a flat netlist into the building
blocks the flow's S0/S1 expect from the upstream hierarchy stage (primitives.json format).

It is a stand-in for the upstream hierarchy when a design comes without one, so its output is
labelled PREDICTED. Rules, in this order, each device assigned once:
  0. dummy: an off device (gate tied to source, or gate on the rail that turns it off) -> 'dummy';
     drain = source otherwise -> 'mos-capacitor'
  1. differential pair: two devices of one polarity on the same non-rail source net, different gates
     and drains, identical size -> 'differential-pair' (gm-structure)
  2. current mirror: devices of one polarity sharing gate and source nets, one diode-connected
     -> 'current-mirror' (load-structure when a drain is a pair drain, else bias-structure)
  3. matched pair: two devices of one polarity sharing the gate net, identical size, sources on
     the same net or on mirrored nets -> 'matched-current-source-pair' / 'matched-cascode-pair'
  4. anything left: a one-device block named after its role (diode, switch-like, common-source...)
Passives: capacitors -> 'capacitor' blocks, resistors chained through internal nets -> 'resistor-string'.

usage: python3 scripts/recognize_structures.py <netlist> [--rails VDD,VSS] [--out primitives.json]
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.common import spice  # noqa: E402


def size(m) -> tuple:
    return (m.model, m.num("W"), m.num("L"), int(m.num("NF", 1)), int(m.num("MULT", m.params.get("M", 1))))


def rail_kind(net: str) -> str | None:
    """'high' / 'low' from the usual SKY130 / xschem supply names (case-insensitive), else None."""
    n = net.lower()
    if n in ("0", "gnd") or any(n.startswith(p) for p in ("vss", "vgnd", "agnd", "dgnd", "gnd")):
        return "low"
    if any(n.startswith(p) for p in ("vdd", "vcc", "vpwr", "vdpwr", "avdd", "dvdd")):
        return "high"
    return None


def recognize(nl: spice.Netlist, rails: set) -> list:
    devs = {m.name: m for m in nl.mosfets}
    left = dict(devs)
    blocks = []
    rails_l = {r.lower() for r in rails}
    on_rail = lambda n: n.lower() in rails_l  # noqa: E731

    def add(kind, cat, members, note=""):
        blocks.append({"primitive": kind, "category": cat, "devices": members, "note": note})
        for d in members:
            left.pop(d, None)

    # 0. dummies and MOS capacitors first. Without this step a dummy with d = g = s looks diode-connected
    #    and joins a "mirror" with the other dummies of its net (found on iadc_ota: 24 of its 38 dummies were
    #    in 6 false blocks). Off device = dummy (enhancement models only; native / zero-Vt devices conduct at
    #    Vgs = 0): gate tied to source, or gate on the rail that turns it off (nmos: low rail, pmos: high
    #    rail), whatever its drain and source. A device with drain = source whose gate is on the other rail
    #    or on a signal net is a MOS capacitor, not a dummy.
    for name, m in sorted(devs.items()):
        native = any(s_ in m.model.lower() for s_ in ("nvt", "native", "zvt"))
        g_off = on_rail(m.g) and rail_kind(m.g) == ("low" if m.polarity == "nmos" else "high")
        if not native and (m.g == m.s or g_off):
            add(f"{m.polarity}-dummy", "dummy", [name])
        elif m.d == m.s and m.g != m.d:
            add(f"{m.polarity}-mos-capacitor", "other", [name], f"gate {m.g}, drain = source {m.d}")
    # 1. differential pairs (never a device whose gate sits on a rail)
    by_src: dict = {}
    for m in devs.values():
        if not on_rail(m.s) and not on_rail(m.g):
            by_src.setdefault((m.polarity, m.s), []).append(m)
    pair_drains = set()
    for (pol, src), ms in sorted(by_src.items()):
        for a, b in itertools.combinations(ms, 2):
            if a.name in left and b.name in left and a.g != b.g and a.d != b.d and size(a) == size(b) \
                    and a.d != a.g and b.d != b.g:
                add(f"{pol}-differential-pair", "gm-structure", [a.name, b.name], f"common source {src}")
                pair_drains |= {a.d, b.d}
    # 2. current mirrors (shared gate and source, one diode)
    by_gs: dict = {}
    for m in devs.values():
        by_gs.setdefault((m.polarity, m.g, m.s), []).append(m)
    for (pol, g, s), ms in sorted(by_gs.items()):
        ms = [m for m in ms if m.name in left]
        if len(ms) >= 2 and any(m.d == m.g for m in ms):
            diode = [m for m in ms if m.d == m.g]
            ordered = diode + [m for m in ms if m.d != m.g]
            load = any(m.d in pair_drains for m in ms)
            add(f"{pol}-current-mirror" + ("-load" if load else ""), "load-structure" if load else "bias-structure",
                [m.name for m in ordered], f"gate {g}, source {s}")
    # 3. matched pairs sharing a gate
    by_g: dict = {}
    for m in devs.values():
        if m.name in left:
            by_g.setdefault((m.polarity, m.g), []).append(m)
    for (pol, g), ms in sorted(by_g.items()):
        for a, b in itertools.combinations(ms, 2):
            if a.name in left and b.name in left and size(a) == size(b) and a.d != b.d:
                kind = "matched-current-source-pair" if (a.s == b.s and on_rail(a.s)) else "matched-cascode-pair"
                add(f"{pol}-{kind}", "load-structure" if kind.endswith("source-pair") else "gm-structure",
                    [a.name, b.name], f"gate {g}")
    # 4. single devices
    for name, m in sorted(left.items()):
        role = "diode" if m.d == m.g else "single"
        add(f"{m.polarity}-{role}", "bias-structure" if role == "diode" else "other", [name])
    # passives
    caps = [p for p in nl.passives if p.kind == "C"]
    for c in caps:
        blocks.append({"primitive": "capacitor", "category": "passive", "devices": [c.name], "note": f"{c.a}-{c.b}"})
    res = [p for p in nl.passives if p.kind == "R"]
    if res:
        # resistors connected through nets that touch only resistors form one string
        nets = nl.nets()
        parent = {r.name: r.name for r in res}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for n, conns in nets.items():
            rs = [e for e, _ in conns if e in parent]
            if rs and len(rs) == len(conns):
                for r in rs[1:]:
                    parent[find(r)] = find(rs[0])
        groups: dict = {}
        for r in res:
            groups.setdefault(find(r.name), []).append(r.name)
        for g in groups.values():
            blocks.append({"primitive": "resistor-string", "category": "passive", "devices": sorted(g),
                           "note": f"{len(g)} resistors"})
    return blocks


def to_primitives(blocks: list, nl: spice.Netlist, design: str) -> dict:
    inst = []
    for i, b in enumerate(blocks, start=1):
        inst.append({"instance": f"X{i}", "subckt": b["primitive"].replace("-", "_"), "primitive": b["primitive"],
                     "category": b["category"], "library": "scripts/recognize_structures.py (rule-based, PREDICTED)",
                     "transistors": {f"M{j}": d for j, d in enumerate(b["devices"], start=1)
                                     if any(m.name == d for m in nl.mosfets)},
                     "passives": [d for d in b["devices"] if any(p.name == d for p in nl.passives)],
                     "note": b["note"]})
    return {"design": design, "provenance": "PREDICTED (rule-based structure recognition, scripts/recognize_structures.py)",
            "subckt": nl.name, "ports": nl.ports, "instances": [x for x in inst if x["transistors"] or x["passives"]]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("netlist")
    ap.add_argument("--rails", default="")
    ap.add_argument("--out")
    a = ap.parse_args()
    nl = spice.parse(Path(a.netlist))
    rails = set(filter(None, a.rails.split(",")))
    prim = to_primitives(recognize(nl, rails), nl, nl.name)
    txt = json.dumps(prim, indent=1)
    if a.out:
        Path(a.out).write_text(txt + "\n")
    for x in prim["instances"]:
        print(x["instance"], x["primitive"], list(x["transistors"].values()) + x["passives"])
