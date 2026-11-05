"""S5 grid router (plan v4 Phase 8.5, docs/plan_v5_ttsky25a.md; PREREG amendment of 2026-11-04 morning).

For layouts the spine router cannot serve (several blocks side by side, many nets). On a GRID of points:
  * metal3 runs horizontally and metal4 vertically, WIRE wide; via3 joins them at a grid point. Wires on neighbouring
    grid lines stand GRID - WIRE = 0.4 um apart (met3.2/met4.2 ask 0.3), so the grid alone keeps them legal;
  * every pin is a horizontal metal3 segment off the grid: a block's track (as placed by S4), or a ring's bottom edge
    (a contact stack li-met3 is drawn where it is used). A net reaches a pin from a metal4 grid point in a column
    over the segment, with a short metal4 stub down (or up) to the segment and a via3 on it; the three grid points of
    that column around the stub are reserved for the net;
  * obstacles: every block track and keep-out (S4: a capacitor's plates, short internal tracks), every placed contact
    stack, grown by WIRE/2 + SPACE, for every net, its own included (Magic checks spacing by geometry);
  * each net is routed as a tree: A* from the tree (its grid points and its pins' access points) to the nearest pin
    not yet joined, cost = length + VIA_COST per via, until every pin is joined; nets in order of least budget slack;
  * a wire piece that is a single grid point is drawn as a SQUARE (area at least 0.24 um2).
A net it cannot finish is listed in the result's `failed`, never left silently unconnected. Mirrored routing of a
symmetric pair is not attempted (G5.4 reports it). All lengths in um.
"""
from __future__ import annotations

import heapq
import math

GRID = 0.8
WIRE = 0.4
SPACE = 0.3
VIA3 = 0.4
VIA_COST = 2.0
MARGIN = 8.0          # routing room around the placement
SQUARE = 0.5          # a single-point wire piece: 0.25 um2
STUB_EXT = 0.31       # a stub reaches past its ends so its metal4 is at least 0.62 um long (area 0.248 um2)
STACK = {"locali": 0.5, "mcon": 0.34, "m2c": 0.34, "m3c": 0.4}
STACK_M3 = 0.5
GROW = WIRE / 2 + SPACE
RING_IN = 0.6         # a contact stack's centre this far in from a ring's corners: 0.25 (half the stack's li)
                      # + 0.085 (half the ring's li) + 0.17 (li.3) = 0.505 um


def _i(x):
    return int(math.floor(x / GRID + 0.5))


class Grid:
    def __init__(self, bbox, outline=None):
        x0, y0, x1, y1 = bbox
        mx = MARGIN if not outline else max(0.0, (outline[0] - (x1 - x0)) / 2 - SQUARE)
        my = MARGIN if not outline else max(0.0, (outline[1] - (y1 - y0)) / 2 - SQUARE)
        self.i0, self.i1 = math.ceil((x0 - mx) / GRID), math.floor((x1 + mx) / GRID)
        self.j0, self.j1 = math.ceil((y0 - my) / GRID), math.floor((y1 + my) / GRID)
        self.own = {}          # (layer, i, j) -> net, or '#' (nobody)
        self.soft = set()      # rule set v2: points closed only by a device area (no metal there), see access()

    def inside(self, i, j):
        return self.i0 <= i <= self.i1 and self.j0 <= j <= self.j1

    def block(self, layer, x0, y0, x1, y1, owner="#", soft=False):
        """Every grid point whose wire would come within SPACE of the rectangle. soft: the rectangle holds no metal
        (a device area, rule set v2 R1), so a wire only has to stay off it, not SPACE away: the caller shrinks it."""
        for i in range(math.ceil((x0 - GROW) / GRID - 1e-9), math.floor((x1 + GROW) / GRID + 1e-9) + 1):
            for j in range(math.ceil((y0 - GROW) / GRID - 1e-9), math.floor((y1 + GROW) / GRID + 1e-9) + 1):
                x, y = i * GRID, j * GRID
                if x0 - GROW < x < x1 + GROW and y0 - GROW < y < y1 + GROW:
                    k = (layer, i, j)
                    cur = self.own.get(k)
                    if soft and cur is None:
                        self.soft.add(k)
                    self.own[k] = owner if cur in (None, owner) else "#"

    def free(self, k, net):
        o = self.own.get(k)
        return o is None or o == net


def access(pin, grid, net):
    """The metal4 grid points from which `net` reaches `pin` (a horizontal metal3 segment at an off-grid y): a column
    over the segment (a via's width in from its ends) with its three points around the segment's y free."""
    y = pin["y"]
    a, b = (pin["rx0"] + RING_IN, pin["rx1"] - RING_IN) if pin["kind"] == "body" and "rx0" in pin else (pin["x0"], pin["x1"])
    if pin["kind"] == "body" and "rx0" not in pin:
        a, b = pin["x0"] - 2.0, pin["x0"] + 2.0
    j = _i(y)
    out = []
    m = 0.0 if pin["kind"] == "body" and "rx0" in pin else VIA3      # a track: a via's width in from its ends
    if not grid.soft:                                                 # v1: exactly as before
        for i in range(math.ceil((a + m) / GRID - 1e-9), math.floor((b - m) / GRID + 1e-9) + 1):
            if grid.inside(i, j) and all(grid.free((4, i, jj), net) for jj in (j - 1, j, j + 1)):
                out.append((4, i, j))
        return out
    # rule set v2 (flow record row 104): a track 0.55 um from its devices has the grid point beside it inside the
    # device area. A neighbour closed only by a device area holds no metal, so it does not stop the stub; and the stub
    # may start one grid point further out (its three points reserved around that point, which still cover the
    # track's own row of the grid)
    for i in range(math.ceil((a + m) / GRID - 1e-9), math.floor((b - m) / GRID + 1e-9) + 1):
        for jc in (j, j + 1, j - 1):
            if grid.inside(i, jc) and grid.free((4, i, jc), net) and \
                    all(grid.free((4, i, jj), net) or (4, i, jj) in grid.soft for jj in (jc - 1, jc + 1)):
                out.append((4, i, jc))
                break
    return out


def astar(grid, net, sources, targets):
    """Cheapest path from any source to any target (layer, i, j); None if there is none."""
    tset = set(targets)
    if not tset:
        return None
    ti = [t[1] for t in tset]
    tj = [t[2] for t in tset]
    bi0, bi1, bj0, bj1 = min(ti), max(ti), min(tj), max(tj)

    def h(k):
        _, i, j = k
        return GRID * (max(0, bi0 - i, i - bi1) + max(0, bj0 - j, j - bj1))
    dist, prev, pq = {}, {}, []
    for s in sources:
        dist[s] = 0.0
        heapq.heappush(pq, (h(s), 0.0, s))
    while pq:
        f, g, k = heapq.heappop(pq)
        if g > dist.get(k, 1e18) + 1e-9:
            continue
        if k in tset:
            path = [k]
            while path[-1] in prev:
                path.append(prev[path[-1]])
            return path[::-1]
        layer, i, j = k
        nbrs = [((3, i - 1, j), GRID), ((3, i + 1, j), GRID)] if layer == 3 else [((4, i, j - 1), GRID), ((4, i, j + 1), GRID)]
        nbrs.append(((7 - layer, i, j), VIA_COST))
        for n, c in nbrs:
            if not grid.inside(n[1], n[2]) or not grid.free(n, net):
                continue
            ng = g + c
            if ng < dist.get(n, 1e18) - 1e-9:
                dist[n], prev[n] = ng, k
                heapq.heappush(pq, (ng + h(n), ng, n))
    return None


def route(pl: dict, nmap: dict, ports: list, order: list, outline: list | None = None) -> dict:
    """pl: a flattened placement. Returns {'routes': {net: {...}}, 'failed': [net, ...]}. With an outline the routing
    stays inside it, centred on the placement (the hard outline holds for the routed layout too)."""
    from src.s5.place import joined_once
    every, pins = {}, {}
    for b, p in pl["blocks"].items():
        for q in p["pins"]:
            n = nmap.get(q["net"], q["net"])
            every.setdefault(n, []).append({**q, "block": q.get("inner") or b})
    for n, qs in every.items():
        pins[n] = joined_once(qs)
    grid = Grid(pl["bbox"], outline)
    for n, qs in every.items():                       # every track of every block, for every net
        for q in qs:
            if q["kind"] == "track":
                grid.block(3, q["x0"], q["y"] - WIRE / 2, q["x1"], q["y"] + WIRE / 2)
    v2 = any(k.get("kind") == "device_area" for p in pl["blocks"].values() for k in p.get("keepouts", []))
    for b, p in pl["blocks"].items():                 # capacitor plates, internal tracks
        for k in p.get("keepouts", []):
            if k.get("kind") != "device_area":
                x0, y0, x1, y1 = k["box"]
                if v2 and k["layer"] == "metal4" and min(x1 - x0, y1 - y0) > 3.005:
                    # rule set v2 (flow record row 106): metal4 wider than 3 um wants met4.5b's spacing, not met4.2's
                    from src.common import drc_rules as D
                    e = D.reserve("met4.5b") - SPACE
                    x0, y0, x1, y1 = x0 - e, y0 - e, x1 + e, y1 + e
                grid.block(3 if k["layer"] == "metal3" else 4, x0, y0, x1, y1)
    for n, qs in every.items():                       # a band along every ring's bottom edge, kept for the stacks
        for q in qs:
            if q["kind"] == "body" and "rx0" in q:
                grid.block(3, q["rx0"], q["y"] - STACK_M3 / 2, q["rx1"], q["y"] + STACK_M3 / 2)
    for b, p in pl["blocks"].items():                 # rule set v2, R1: device areas last, so only points nothing
        for k in p.get("keepouts", []):               # else closes are 'soft'; no metal there, so a wire's edge may
            if k.get("kind") == "device_area":        # reach the area's edge (shrunk by SPACE: GROW less SPACE)
                x0, y0, x1, y1 = k["box"]
                grid.block(3 if k["layer"] == "metal3" else 4, x0 + SPACE, y0 + SPACE, x1 - SPACE, y1 - SPACE,
                           soft=True)
    nets = [n for n in pins if len(pins[n]) > 1 or n in ports]
    nets.sort(key=lambda n: (order.index(n) if n in order else len(order), n))
    routes, failed = {}, []
    for net in nets:
        qs = pins[net]
        first = min(range(len(qs)), key=lambda k: (qs[k]["y"], qs[k]["x0"]))
        acc0 = access(qs[first], grid, net)
        if not acc0:
            failed.append(net)
            continue
        tree, used = set(), []                       # used: (access point, pin) where a stub goes down to a pin
        starts = {a: first for a in acc0}            # access points of the pins joined so far
        todo = [k for k in range(len(qs)) if k != first]
        if not todo:                                  # a port with one pin: a stub and a via for its label
            used.append((acc0[0], qs[first]))
        ok = True
        while todo:
            cand = {}
            for k in todo:
                for a in access(qs[k], grid, net):
                    cand.setdefault(a, k)
            path = astar(grid, net, list(tree | set(starts)), list(cand))
            if path is None:
                ok = False
                break
            if path[0] not in tree:                   # it leaves from a joined pin: a stub there
                used.append((path[0], qs[starts[path[0]]]))
            k_end = cand[path[-1]]
            used.append((path[-1], qs[k_end]))
            for node in path:
                tree.add(node)
                grid.own[node] = net
            todo.remove(k_end)
            for a in access(qs[k_end], grid, net):
                starts.setdefault(a, k_end)
        if not ok:
            failed.append(net)
            for node in tree:
                if grid.own.get(node) == net:
                    del grid.own[node]
            continue
        stacks = []                                   # reserve the stubs' columns; a ring pin gets its contact stack
        for (layer, i, j), q in used:
            for jj in (j - 1, j, j + 1):
                if (4, i, jj) not in grid.soft:      # a device area stays closed to this net too
                    grid.own[(4, i, jj)] = net
            tree.add((4, i, j))
            if q["kind"] == "body":
                x, y = i * GRID, q["y"]
                if (x, y) not in stacks:
                    stacks.append((x, y))
                    grid.block(3, x - STACK_M3 / 2, y - STACK_M3 / 2, x + STACK_M3 / 2, y + STACK_M3 / 2)
        routes[net] = {"nodes": sorted(tree), "stubs": [[i * GRID, j * GRID, q["y"]] for (l, i, j), q in used],
                       "stacks": stacks, "port": net in ports, "n_pins": len(qs)}
    return {"routes": routes, "failed": failed}


def segments(r: dict) -> dict:
    """The route's wires as segments: metal3 (y, x0, x1), metal4 (x, y0, y1), single points, and its vias."""
    nodes = set(map(tuple, r["nodes"]))
    m3 = sorted((i, j) for l, i, j in nodes if l == 3)
    m4 = sorted((j, i) for l, i, j in nodes if l == 4)

    def runs(pts):
        out, cur = [], None
        for a, b in pts:
            if cur and cur[0] == a and b == cur[2] + 1:
                cur[2] = b
            else:
                if cur:
                    out.append(tuple(cur))
                cur = [a, b, b]
        if cur:
            out.append(tuple(cur))
        return out
    seg3 = [(j * GRID, i0 * GRID, i1 * GRID) for j, i0, i1 in runs(sorted((j, i) for i, j in m3))]
    seg4 = [(i * GRID, j0 * GRID, j1 * GRID) for i, j0, j1 in runs(sorted((i, j) for j, i in m4))]
    vias = [(i * GRID, j * GRID) for l, i, j in nodes if l == 3 and (4, i, j) in nodes]
    return {"metal3": seg3, "metal4": seg4, "vias": vias}


def lengths(r: dict) -> dict:
    s = segments(r)
    stub = sum(abs(y - yg) for _, yg, y in r["stubs"])
    return {"metal4": round(sum(y1 - y0 for _, y0, y1 in s["metal4"]) + stub, 4),
            "metal3": round(sum(x1 - x0 for _, x0, x1 in s["metal3"]), 4)}


def tcl(routes: dict) -> list:
    """Magic commands that draw the routes and port labels in the current (top) cell."""
    def box(x0, y0, x1, y1):
        return f"box {x0:.4f}um {y0:.4f}um {x1:.4f}um {y1:.4f}um"
    c = []
    for net, r in routes.items():
        s = segments(r)
        for y, x0, x1 in s["metal3"]:
            if x1 - x0 < 1e-9:
                c += [box(x0 - SQUARE / 2, y - SQUARE / 2, x0 + SQUARE / 2, y + SQUARE / 2), "paint metal3"]
            else:
                c += [box(x0 - WIRE / 2, y - WIRE / 2, x1 + WIRE / 2, y + WIRE / 2), "paint metal3"]
        for x, y0, y1 in s["metal4"]:
            if y1 - y0 < 1e-9:
                c += [box(x - SQUARE / 2, y0 - SQUARE / 2, x + SQUARE / 2, y0 + SQUARE / 2), "paint metal4"]
            else:
                c += [box(x - WIRE / 2, y0 - WIRE / 2, x + WIRE / 2, y1 + WIRE / 2), "paint metal4"]
        for x, y in s["vias"]:
            c += [box(x - VIA3 / 2, y - VIA3 / 2, x + VIA3 / 2, y + VIA3 / 2), "paint via3"]
        for x, yg, y in r["stubs"]:                    # metal4 from the grid point to the pin, a via3 on the pin
            lo, hi = min(yg, y) - STUB_EXT, max(yg, y) + STUB_EXT
            c += [box(x - WIRE / 2, lo, x + WIRE / 2, hi), "paint metal4",
                  box(x - VIA3 / 2, y - VIA3 / 2, x + VIA3 / 2, y + VIA3 / 2), "paint via3"]
        for sx, sy in r["stacks"]:
            for layer, w in STACK.items():
                c += [box(sx - w / 2, sy - w / 2, sx + w / 2, sy + w / 2), f"paint {layer}"]
            c += [box(sx - STACK_M3 / 2, sy - STACK_M3 / 2, sx + STACK_M3 / 2, sy + STACK_M3 / 2), "paint metal3"]
        if r["port"] and r["stubs"]:
            x, yg, _ = r["stubs"][0]
            c += [box(x - 0.05, yg - 0.05, x + 0.05, yg + 0.05), f"label {net} c metal4"]
    return c


def rules_view(r: dict) -> dict:
    """The route as S5's G5.4 reads it: metal3 runs (y, x0, x1), metal4 runs (x, y0, y1) including the stubs, and
    every via3 (the stubs' included)."""
    s = segments(r)
    stubs4 = [(x, min(yg, y), max(yg, y)) for x, yg, y in r["stubs"]]
    return {"met3": s["metal3"], "m4segs": s["metal4"] + stubs4, "vias": s["vias"] + [(x, y) for x, _, y in r["stubs"]],
            "port": r["port"], "n_pins": r["n_pins"], "grid": True}
