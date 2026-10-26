"""S3 step 1 — the characterised PCell option table (decision D7).

For each device type (model, W, L, m) the SKY130 Magic PCell is generated for a grid of options,
completed into a device cell (finger straps + D/G/S/B labels, strap.py), and every cell is measured:
  * DRC (Magic drc(full), negative control) and LVS of the whole device cell against the sized
    netlist line (Netgen; W, L and nf; negative control with L + 0.1 um);
  * the cell's own extraction (Magic, cthresh 0): the finger devices with their ad/as/pd/ps and the
    capacitances drawn inside the cell (straps over gates, contacts). This subcircuit is used verbatim
    by the in-circuit simulation (evaluate.py);
  * area and per-terminal contact counts from the GDS (KLayout);
  * access resistance per terminal (the extraction above has no resistance):
      gate : BSIM4 distributed gate resistance Rgeltd = Rsh_poly * W_f / (3 * ngcon^2 * L * nf)
             (BSIM4 manual, XGW = XGL = 0; ngcon = number of contacted gate ends), plus the measured
             poly contacts and gate mcons in parallel. The sky130 model cards set rgatemod = 0, so the
             simulator adds no gate resistance of its own.
      s, d : per strip of the terminal: licon and mcon contacts in parallel (counted on the GDS), the
             met1 strip as a distributed resistor fed uniformly and tapped at one end (1/3 of its
             end-to-end value; width measured on the GDS) and the strap via; strips in parallel.
    Contact and sheet resistances come from the extract section of sky130A.tech (S2 pdk rules).
    For the default option Magic's lumped extresist value is kept as a cross-check.
"""
from __future__ import annotations

import itertools
import re
import subprocess
from pathlib import Path

from src.common import pcell
from src.common.tools import TOOL_ENV, rel
from src.s3 import strap, wbins

L_DIFF, L_POLY, L_LICON, L_LI, L_MCON, L_M1 = (65, 20), (66, 20), (66, 44), (67, 20), (67, 44), (68, 20)
NF_GRID = (1, 2, 4, 8)
NF_GRID_WIDE = (16, 32, 64)   # only for wide devices: used when the finger stays >= WIDE_MIN_WF
WIDE_MIN_WF = 7.0             # um, the lower W edge of the wide SKY130 model bins
GATE_GRID = {"both": (1, 1), "top": (1, 0)}
SD_GRID = {"full": (100, 100), "half": (50, 50)}   # (diffcov %, viasrc/viadrn %)
MIN_WF = 0.42                                       # sky130 minimum finger width (PCell wmin)


def device_types(ir: dict) -> dict:
    types: dict = {}
    for d in ir["devices"]:
        key = f"{d['model'].replace('sky130_fd_pr__', '')}_W{d['W_um']:g}_L{d['L_um']:g}_m{d['m']}".replace(".", "p")
        t = types.setdefault(key, {"model": d["model"], "W": d["W_um"], "L": d["L_um"], "m": d["m"],
                                   "nf": d.get("nf", 1), "type": d["type"], "devices": []})
        t["devices"].append(d["name"])
    return types


def grid(W: float, wide: bool = True) -> list:
    """wide=False: the v1 grid (nf <= 8), for the 'before' variant"""
    out = []
    nfs = NF_GRID + (tuple(n for n in NF_GRID_WIDE if W / n >= WIDE_MIN_WF) if wide else ())
    for nf, (g, gc), (s, sc) in itertools.product(nfs, GATE_GRID.items(), SD_GRID.items()):
        if W / nf < MIN_WF:
            continue
        for outer in (("S", "D") if nf % 2 == 0 else ("D",)):
            out.append({"id": f"nf{nf}_g{g}_sd{s}" + (f"_out{outer}" if nf % 2 == 0 else ""), "nf": nf,
                        "gate_contacts": g, "sd_cov": s, "outer": outer,
                        "magic": {"topc": gc[0], "botc": gc[1], "diffcov": sc[0], "viasrc": sc[1], "viadrn": sc[1],
                                  "guard": 1, "conn_gates": 1 if nf > 1 else 0}})
    return out


# Option modes (plan v2, S3/S4 decision): how far the drawn device may depart from the netlist line
#   B      nf and m exactly as in the netlist (only contact and coverage options vary)
#   A-bin  nf free as long as the finger width W/nf stays in the sized device's SKY130 model bin (main mode)
#   A-free every nf of the grid (ablation; the drawn device may fall into another model bin)
#   RoT    rule-of-thumb baseline (N3): nf = the grid value nearest W / RULE_OF_THUMB_WF, default contacts
MODES = ("B", "A-bin", "A-free")
RULE_OF_THUMB_WF = 4.0   # um, fixed before any run that uses it (PREREG.md)


def in_mode(t: dict, opt: dict, mode: str) -> bool:
    if mode == "A-free":
        return True
    if mode == "B":
        return opt["nf"] == t.get("nf", 1)
    if mode == "A-bin":
        return opt["nf"] == t.get("nf", 1) or wbins.same_bin(t["model"], t["W"], t["L"], t["W"] / opt["nf"])
    raise ValueError(mode)


def rule_of_thumb_id(t: dict) -> str:
    nfs = [n for n in NF_GRID + NF_GRID_WIDE if t["W"] / n >= MIN_WF and (n in NF_GRID or t["W"] / n >= WIDE_MIN_WF)]
    nf = min(nfs, key=lambda n: (abs(t["W"] / n - RULE_OF_THUMB_WF), n))
    return f"nf{nf}_gboth_sdfull" + ("_outD" if nf % 2 == 0 else "")


def default_option_id() -> str:
    return "nf1_gboth_sdfull"


def magic_params(t: dict, opt: dict) -> dict:
    p = {"w": round(t["W"] / opt["nf"], 4), "l": t["L"], "nf": opt["nf"], "m": t["m"]}
    p.update(opt["magic"])
    return p


def geometry(gds: Path, roles_plan: dict) -> dict:
    import klayout.db as kdb
    ly = kdb.Layout()
    ly.read(str(gds))
    top = ly.top_cell()
    dbu = ly.dbu

    def region(lp):
        li = ly.find_layer(*lp)
        return kdb.Region(top.begin_shapes_rec(li)) if li is not None else kdb.Region()
    diff, poly, licon, mcon, li = (region(x) for x in (L_DIFF, L_POLY, L_LICON, L_MCON, L_LI))
    lic_poly, lic_diff = licon & poly, licon & diff
    mcon_diff = mcon.interacting(diff)
    mcon_gate = mcon.interacting(lic_poly.sized(int(0.2 / dbu))).not_interacting(diff) \
        if not lic_poly.is_empty() else kdb.Region()
    per_strip = []
    for s in roles_plan["strips"]:
        box = kdb.Region(kdb.Box(int(s["x0"] / dbu), int(s["y0"] / dbu) - 500, int(s["x1"] / dbu), int(s["y1"] / dbu) + 500))
        li_s = [q.bbox() for q in (li & diff).interacting(box).each()]
        li_len = max((b.height() * dbu for b in li_s), default=None)
        li_w = min((b.width() * dbu for b in li_s), default=None)
        per_strip.append({**s, "n_licon": (lic_diff & box).count(), "n_mcon": mcon_diff.interacting(box).count(),
                          "width_um": s["x1"] - s["x0"], "length_um": s["y1"] - s["y0"],
                          "li_length_um": li_len, "li_width_um": li_w})
    bb = top.dbbox()
    return {"bbox_um": [round(bb.width(), 3), round(bb.height(), 3)], "area_um2": round(bb.width() * bb.height(), 3),
            "n_licon_poly": lic_poly.count(), "n_licon_diff": lic_diff.count(), "n_mcon_diff": mcon_diff.count(),
            "n_mcon_gate": mcon_gate.count(), "strips": per_strip}


def pex(gds: Path, cell: str, out: Path) -> dict:
    """Cell-level extraction with all capacitances (cthresh 0), ports = the wrapper labels."""
    out.mkdir(parents=True, exist_ok=True)
    (out / "pex.tcl").write_text("\n".join([
        f"gds read {gds}", f"load {cell}", "select top cell", "port makeall", f"extract path {out}",
        "extract all", "ext2spice hierarchy off", "ext2spice subcircuit top on", "ext2spice cthresh 0",
        "ext2spice format ngspice",
        f"ext2spice -o {out}/pex.spice", "quit -noprompt"]) + "\n")
    r = subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", str(pcell.MAGICRC), str(out / "pex.tcl")],
                       cwd=out, env=TOOL_ENV, capture_output=True, text=True, timeout=300)
    (out / "pex_magic.log").write_text(r.stdout + r.stderr)
    f = out / "pex.spice"
    txt = f.read_text() if f.exists() else ""
    sub = re.search(r"^\.subckt\s+(\S+)\s+(.*)$", txt, re.M)
    devs = [dict(re.findall(r"(\w+)=(\S+)", m.group(1))) for m in re.finditer(r"^X\S*\s+(?:\S+\s+){5}(.*)$", txt, re.M)]
    caps = [float(m.group(1)) * {"a": 1e-18, "f": 1e-15, "p": 1e-12}.get(m.group(2), 1.0)
            for m in re.finditer(r"^C\S*\s+\S+\s+\S+\s+([0-9.eE+-]+)([afp]?)", txt, re.M)]
    return {"file": rel(f), "subckt": sub.group(1) if sub else None, "ports": sub.group(2).split() if sub else [],
            "n_devices": len(devs), "fingers": devs, "n_caps": len(caps), "sum_caps_F": sum(caps)}


def magic_lumped_r(gds: Path, cell: str, out: Path) -> dict:
    """Magic extresist on the device cell: label-to-device lumped resistance (cross-check only)."""
    out.mkdir(parents=True, exist_ok=True)
    (out / "rx.tcl").write_text("\n".join([
        f"gds read {gds}", f"load {cell}", "select top cell", "port makeall", "extract do resistance",
        "extract all", "ext2sim labels on", "ext2sim", "extresist tolerance 1", "extresist all",
        "ext2spice extresist on", "ext2spice cthresh 0", "ext2spice format ngspice", f"ext2spice -o {out}/rx.spice",
        "quit -noprompt"]) + "\n")
    r = subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", str(pcell.MAGICRC), str(out / "rx.tcl")],
                       cwd=out, env=TOOL_ENV, capture_output=True, text=True, timeout=300)
    (out / "rx_magic.log").write_text(r.stdout + r.stderr)
    txt = (out / "rx.spice").read_text() if (out / "rx.spice").exists() else ""
    res = {}
    for t in ("G", "D", "S"):
        vals = [float(m.group(1)) for m in re.finditer(rf"^R\S*\s+{t}(?:\.\S+)?\s+{t}\.\S+\s+([0-9.eE+-]+)", txt, re.M)]
        res[t] = max(vals) if vals else None
    return {"largest_resistor_on_net_ohm": res, "file": rel(out / "rx.spice"),
            "note": "Magic lumps each net to a point; None = net below extresist tolerance"}


def access_resistance(t: dict, opt: dict, geo: dict, rules: dict) -> dict:
    W, L, nf = t["W"], t["L"], opt["nf"]
    wf = W / nf
    rc = rules["contacts"]
    ngcon = 2 if opt["gate_contacts"] == "both" else 1
    r_poly = rules["poly_sheet_res_ohm_sq"] * wf / (3 * ngcon ** 2 * L * nf)
    n_pc, n_mg = max(geo["n_licon_poly"], 1), max(geo["n_mcon_gate"], 1)
    out = {"g": r_poly + rc["licon_poly"]["ohm_per_contact"] / n_pc + rc["mcon"]["ohm_per_contact"] / n_mg,
           "g_parts": {"poly_distributed": r_poly, "ngcon": ngcon, "poly_contacts": n_pc, "gate_mcons": n_mg}}
    licon = rc["licon_pdiff" if t["type"] == "pmos" else "licon_ndiff"]["ohm_per_contact"]
    mc, via = rc["mcon"]["ohm_per_contact"], rc["via1"]["ohm_per_contact"]
    rsh_m1 = rules["layers"]["metal1"]["sheet_res_ohm_sq"]
    strapped = len(geo["strips"]) > 2
    for term in ("d", "s"):
        g_tot, parts = 0.0, []
        for s in geo["strips"]:
            if s["role"] != term.upper():
                continue
            r = licon / max(s["n_licon"], 1) + mc / max(s["n_mcon"], 1) + rsh_m1 * s["length_um"] / s["width_um"] / 3
            # li strip beyond the met1 strip (reduced via coverage): two uncovered ends, current entering
            # uniformly along them -> Rsh_li * L_uncovered / (12 * w_li)
            if s.get("li_length_um") and s.get("li_width_um"):
                l_unc = max(0.0, s["li_length_um"] - s["length_um"])
                r += rules["layers"]["locali"]["sheet_res_ohm_sq"] * l_unc / (12 * s["li_width_um"])
            if strapped:
                r += via
            parts.append(round(r, 4))
            g_tot += 1.0 / r
        out[term] = 1.0 / g_tot if g_tot else None
        out[f"{term}_strips_ohm"] = parts
    return out


def build_one(t: dict, tid: str, opt: dict, out: Path, rules: dict, cross_check: bool = False) -> dict:
    cell = f"{tid}__{opt['id']}"
    d = out / cell
    gen = pcell.generate([{"cell": cell, "model": t["model"], "params": magic_params(t, opt)}], d)
    gds = d / f"{cell}.gds"
    rec = {"type": tid, "option": opt, "cell": cell, "gds": rel(gds), "gen_rc": gen["rc"]}
    if not gds.exists():
        rec.update({"ok": False, "error": "PCell generation failed", "log": gen["log"]})
        return rec
    try:
        st = strap.apply(d, cell, opt["outer"])
    except strap.StrapDoesNotFit as e:
        rec.update({"ok": False, "error": f"strap does not fit: {e}"})
        return rec
    rec["strap"] = {k: st[k] for k in ("rc", "strapped", "roles")}
    rec["drc"] = pcell.drc(gds, cell, d / "drc")
    rec["lvs"] = pcell.lvs_device(gds, cell, t["model"], t["W"], t["L"], opt["nf"], t["m"], d / "lvs", mode="top")
    geo = geometry(gds, st["plan"])
    rec["geometry"] = geo
    rec["pex"] = pex(gds, cell, d / "pex")
    rec["access_resistance_ohm"] = access_resistance(t, opt, geo, rules)
    if cross_check:
        rec["magic_extresist"] = magic_lumped_r(gds, cell, d / "rx")
    rec["png"] = pcell.png(gds, d / f"{cell}.png")
    rec["ok"] = bool(rec["drc"]["pass"] and rec["lvs"]["pass"] and rec["pex"]["n_devices"] == opt["nf"] * t["m"])
    return rec
