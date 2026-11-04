"""S5 routing (plan v4, Phase 4; layers, width and grid fixed in the PREREG amendment of 2026-11-03, late evening).

A spine router for row placements, where the blocks of one design stand centred on one axis and the tracks of
connected blocks overlap in x:
  * every net gets one vertical metal4 SPINE (width WIRE, on the GRID; metal4 may pass over blocks, which have none);
  * each of the net's block tracks (metal3) meets the spine with a via3, or, if the track does not reach the spine,
    with a metal3 extension along the track's line;
  * each ring body pin (local interconnect, `<body>_body`) gets a contact stack up to metal3 and a metal3 run to the
    spine at the ring's line, which no block track uses;
  * spines are GRID apart wherever their heights overlap and keep clear of other nets' stacks and vias; the nets of a
    `route.symmetric.*` pair get spines mirrored about the axis (only that position for a hard rule; tried first for
    a soft one, whose miss G5.4 reports); nets go in order of least budget slack first;
  * a port net gets its port label (the layout view's name) on its spine; a port net with a single pin gets a
    one-via pad;
  * a block's keep-outs (a capacitor's met3 plate and met4; plan v4 Phase 6) are kept MET3_SPACE clear by every
    spine and met3 run, except a keep-out that belongs to the net itself (a plate's neck);
  * a net's two tracks that one block already joins (src/s5/place.joined_once) get one connection, the nearer;
  * a spine within two pitches of another net's spine runs beside it no longer than S2's
    route.max_parallel.<a>~<b>.metal4 allows (the length G5.4 measures); a met3 run keeps MET3_SPACE from every
    met3 shape it does not overlap, its own net's included (Magic checks spacing by geometry, not by net).
A net the router cannot place raises, so a failure is never silent. This is not a general maze router: it covers
the row placements S5 makes, and the plan's maze router stays open for layouts that need detours (plan, section 8).
All lengths in um.
"""
from __future__ import annotations

import re

GRID = 0.8
WIRE = 0.4
VIA3 = 0.4          # via3 with its metal3/metal4 surround
STACK = {"locali": 0.5, "mcon": 0.34, "m2c": 0.34, "m3c": 0.4}
STACK_M3 = 0.5      # the stack's metal3 square: 0.25 um2 (met3.6 needs 0.24) and 0.35 um from a track 0.8 um away
MIN_LEN = 0.7       # every metal3/metal4 piece at least 0.4 x 0.7 um: 0.28 um2, above the 0.24 um2 minimum area
MET3_SPACE = 0.3
Y_CLEAR = 1.2       # two spines on one column need this much between their via centres (two grown ends + spacing)


def net_map(ir: dict, ref_spice: str) -> dict:
    """IR net -> the layout view's net, from each device's terminals in both (e.g. net2 -> VBIAS)."""
    ref = {}
    for ln in ref_spice.splitlines():
        t = ln.split()
        if t and t[0][:1] in "Xx" and len(t) > 5:
            ref[t[0]] = t[1:5]
    out = {}
    for d in ir["devices"]:
        r = ref.get(d["name"]) or ref.get("X" + d["name"])   # the layout view keeps the instance name (XM5)
        if r:
            for k, rn in zip("dgsb", r):
                out[d["terminals"][k]] = rn
    return out


def ports_of(ref_spice: str) -> list:
    m = re.search(r"^\.subckt\s+\S+\s+(.*)$", ref_spice, re.M)
    return m.group(1).split() if m else []


def drawn(x0: float, x1: float) -> tuple:
    """The x extent Magic draws for a met3 run from x0 to x1: WIRE/2 past each end, lengthened about its middle to
    at least MIN_LEN."""
    a, b = x0 - WIRE / 2, x1 + WIRE / 2
    pad = max(0.0, (MIN_LEN - (b - a)) / 2)
    return a - pad, b + pad


def _snap(x: float) -> float:
    return round(round(x / GRID) * GRID, 4)


def plan_routes(pl: dict, nmap: dict, ports: list, order: list, mirrored: list, par_limit: dict | None = None) -> dict:
    """pl: a placement (src/s5/place.realise); par_limit: {frozenset({a, b}): um} from S2's metal4 parallel rules.
    Returns {net: route} with the spine, vias, extensions and stacks."""
    from src.s5.place import joined_once
    pins = {}
    for b, p in pl["blocks"].items():
        for q in p["pins"]:
            pins.setdefault(nmap.get(q["net"], q["net"]), []).append({**q, "block": b})
    every = pins                                      # all tracks are drawn, the joined ones too
    pins = {n: joined_once(qs) for n, qs in pins.items()}
    par_limit = par_limit or {}
    nets = [n for n in pins if len(pins[n]) > 1 or n in ports]
    nets.sort(key=lambda n: (order.index(n) if n in order else len(order), n))
    tracks = [(n, q) for n, qs in every.items() for q in qs if q["kind"] == "track"]
    keep = [{**k, "net": nmap.get(k["net"], k["net"]) if k["net"] else None}
            for p in pl["blocks"].values() for k in p.get("keepouts", [])]

    def kept_out(layer, net, x0, y0, x1, y1):
        """True if the box [x0, y0, x1, y1] comes within MET3_SPACE of another net's keep-out on the layer."""
        return any(k["layer"] == layer and k["net"] != net and x0 < k["box"][2] + MET3_SPACE and
                   x1 > k["box"][0] - MET3_SPACE and y0 < k["box"][3] + MET3_SPACE and y1 > k["box"][1] - MET3_SPACE
                   for k in keep)
    spines, routes = {}, {}
    pair_of = {a: (b, cls) for a, b, cls in mirrored} | {b: (a, cls) for a, b, cls in mirrored}

    def y_range(qs):
        ys = [q["y"] for q in qs]
        return min(ys), max(ys)

    def free(x, net, lo, hi):
        pad = max(VIA3, MIN_LEN) / 2
        if kept_out("metal4", net, x - WIRE / 2, lo - pad, x + WIRE / 2, hi + pad):
            return False
        for m, s in spines.items():
            if m != net and abs(s["x"] - x) < GRID - 1e-6 and not (hi < s["y"][0] - Y_CLEAR or lo > s["y"][1] + Y_CLEAR):
                return False
            lim = par_limit.get(frozenset((m, net)))
            if m != net and lim is not None and abs(s["x"] - x) <= 2 * GRID + 1e-6 and \
                    min(hi, s["y"][1]) - max(lo, s["y"][0]) > lim:
                return False
        for m, r in routes.items():   # other nets' stacks and vias
            if m != net and any(abs(px - x) < GRID - 1e-6 and lo - GRID <= py <= hi + GRID for px, py in r["points"]):
                return False
        for m, qs in pins.items():    # other nets' body pins (their stacks come later)
            if m != net and any(q["kind"] == "body" and abs(q["x0"] - x) < GRID - 1e-6 and lo - GRID <= q["y"] <= hi + GRID
                                for q in qs):
                return False
        return True

    def ext_ok(y, xa, xb, net, mine=()):
        """None if a met3 run at y from xa to xb comes within MET3_SPACE of another net's met3 (or a keep-out); else
        the met3 fills that merge it with its own net's shapes it passes closer than that without touching (Magic
        checks spacing by geometry). mine: the runs this attempt has already planned."""
        lo, hi = drawn(min(xa, xb), max(xa, xb))
        if kept_out("metal3", net, lo, y - WIRE / 2, hi, y + WIRE / 2):
            return None
        shapes = [(m, q["y"], q["x0"], q["x1"]) for m, q in tracks]
        shapes += [(m, ey, *drawn(ex0, ex1)) for m, r in routes.items() for ey, ex0, ex1 in r["met3"]]
        shapes += [(net, ey, *drawn(ex0, ex1)) for ey, ex0, ex1 in mine]
        fills = []
        for m, oy, ox0, ox1 in shapes:
            dy = abs(oy - y)
            if dy >= WIRE + MET3_SPACE or hi < ox0 or lo > ox1:
                continue
            if m != net:
                return None
            if dy > 1e-6:
                a, b = max(lo, ox0), min(hi, ox1)
                c = (a + b) / 2
                a, b = min(a, c - WIRE / 2), max(b, c + WIRE / 2)
                fills.append((round(a, 4), round(min(y, oy) - WIRE / 2, 4), round(b, 4), round(max(y, oy) + WIRE / 2, 4)))
        return fills

    def cost_of(x, qs):
        c = 0.0
        for q in qs:
            if q["kind"] == "track" and not (q["x0"] + VIA3 <= x <= q["x1"] - VIA3):
                c += min(abs(x - q["x0"]), abs(x - q["x1"]))
            elif q["kind"] == "body":
                c += abs(x - q["x0"])
        return c

    def attempt(net, x):
        """The met3 runs net needs with its spine at x, or None if x is taken or a run would touch another net."""
        qs = pins[net]
        lo, hi = y_range(qs)
        if not free(x, net, lo, hi):
            return None
        met3, fills = [], []
        for q in qs:
            if q["kind"] == "track" and not (q["x0"] + VIA3 <= x <= q["x1"] - VIA3):
                end = q["x1"] - VIA3 if x > q["x1"] else q["x0"] + VIA3
                run = (q["y"], min(end, x), max(end, x))
            elif q["kind"] == "body":
                run = (q["y"], min(q["x0"], x), max(q["x0"], x))
            else:
                continue
            f = ext_ok(run[0], run[1], run[2], net, met3)
            if f is None:
                return None
            met3.append(run)
            fills += f
        return met3, fills

    def commit(net, x, plan):
        met3, fills = plan
        qs = pins[net]
        lo, hi = y_range(qs)
        vias = [(x, q["y"]) for q in qs]
        stacks = [(q["x0"], q["y"]) for q in qs if q["kind"] == "body"]
        spines[net] = {"x": x, "y": [round(lo, 4), round(hi, 4)]}
        routes[net] = {"spine": spines[net], "vias": vias, "met3": [m for m in met3 if m[2] - m[1] > 1e-6],
                       "fills": fills, "stacks": stacks, "points": vias + stacks, "port": net in ports,
                       "n_pins": len(qs)}

    def candidates(net):
        qs = pins[net]
        span = [min(q["x0"] for q in qs) - 10 * GRID, max(q["x1"] for q in qs) + 10 * GRID]
        cands = [_snap(span[0] + k * GRID) for k in range(int((span[1] - span[0]) / GRID) + 1)]
        return sorted(cands, key=lambda x: (cost_of(x, qs), abs(x)))

    for net in nets:
        if net in routes:
            continue
        partner, cls = pair_of.get(net, (None, None))
        if cls == "hard" and partner in pins and partner not in routes:
            # a hard mirrored pair is placed together: x for net, -x for its partner, each free of the other
            pq = pins[partner]
            for x in candidates(net):
                if abs(x) < GRID / 2 and not (y_range(pq)[1] < y_range(pins[net])[0] - Y_CLEAR or
                                              y_range(pq)[0] > y_range(pins[net])[1] + Y_CLEAR):
                    continue                     # both on the axis would share one column
                m1 = attempt(net, x)
                if m1 is None:
                    continue
                commit(net, x, m1)
                m2 = attempt(partner, _snap(-x))
                if m2 is not None:
                    commit(partner, _snap(-x), m2)
                    break
                del spines[net], routes[net]
            else:
                raise RuntimeError(f"no mirrored spines for the hard pair {net}/{partner}")
            continue
        mirror_x = _snap(-spines[partner]["x"]) if partner in spines else None
        ordered = candidates(net)
        if mirror_x is not None:   # a soft pair: the partner's spine mirrored is tried first
            ordered = [mirror_x] + [x for x in ordered if x != mirror_x]
        for x in ordered:
            m = attempt(net, x)
            if m is not None:
                commit(net, x, m)
                break
        else:
            raise RuntimeError(f"no spine for net {net}")
    return routes


def lengths(r: dict) -> dict:
    return {"metal4": round(r["spine"]["y"][1] - r["spine"]["y"][0], 4),
            "metal3": round(sum(x1 - x0 for _, x0, x1 in r["met3"]), 4)}


def tcl(routes: dict) -> list:
    """Magic commands that draw the routes and port labels in the current (top) cell."""
    def box(x0, y0, x1, y1):
        return f"box {x0:.4f}um {y0:.4f}um {x1:.4f}um {y1:.4f}um"
    def grow(a, b):   # a segment [a, b] lengthened about its middle to at least MIN_LEN
        pad = max(0.0, (MIN_LEN - (b - a)) / 2)
        return a - pad, b + pad
    c = []
    for net, r in routes.items():
        x, (y0, y1) = r["spine"]["x"], r["spine"]["y"]
        ya, yb = grow(y0 - VIA3 / 2, y1 + VIA3 / 2)
        c += [box(x - WIRE / 2, ya, x + WIRE / 2, yb), "paint metal4"]
        for vx, vy in r["vias"]:
            c += [box(vx - VIA3 / 2, vy - VIA3 / 2, vx + VIA3 / 2, vy + VIA3 / 2), "paint via3"]
        for y, x0, x1 in r["met3"]:
            xa, xb = drawn(x0, x1)
            c += [box(xa, y - WIRE / 2, xb, y + WIRE / 2), "paint metal3"]
        for f in r.get("fills", []):
            c += [box(*f), "paint metal3"]
        for sx, sy in r["stacks"]:
            for layer, s in STACK.items():
                c += [box(sx - s / 2, sy - s / 2, sx + s / 2, sy + s / 2), f"paint {layer}"]
            c += [box(sx - STACK_M3 / 2, sy - STACK_M3 / 2, sx + STACK_M3 / 2, sy + STACK_M3 / 2), "paint metal3"]
        if r["port"]:
            c += [box(x - 0.05, y0 - 0.05, x + 0.05, y0 + 0.05), f"label {net} c metal4"]
    return c
