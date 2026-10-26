"""Generate devices with the SKY130 PDK's own Magic PCells and sign each one off (DRC + LVS).

Used by S0 (binding check with default options) and S3 (option sweeps).
Every verdict is parsed from tool reports; each check carries a negative control:
  - DRC: magic_drc.sh paints a 0.05 um met1 sliver after the real check and must see it flagged;
  - LVS: the same layout is compared against a reference with a wrong L and must FAIL.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

from src.common.tools import PDK_ROOT, REPO, TOOL_ENV, rel

SCRIPTS = REPO / "scripts"
MAGICRC = f"{PDK_ROOT}/sky130A/libs.tech/magic/sky130A.magicrc"


def gencell_tcl(cell: str, model: str, params: dict) -> str:
    p = " ".join(f"{k} {v}" for k, v in params.items())
    return "\n".join([
        f"cellname delete {cell}", f"load {cell} -silent", "box 0 0 0 0",
        f"magic::gencell sky130::{model} {cell}_pc {p}",
        "select top cell", "expand", f"save {cell}", f"gds write {cell}",
    ])


def generate(devices: list, out: Path, timeout: int = 900) -> dict:
    """devices: [{'cell','model','params'}]. One Magic batch run; returns {'rc','log','gds':{cell:path}}."""
    out.mkdir(parents=True, exist_ok=True)
    tcl = ["drc off", "snap internal"] + [gencell_tcl(d["cell"], d["model"], d["params"]) for d in devices]
    tcl.append("quit -noprompt")
    (out / "gen.tcl").write_text("\n".join(tcl) + "\n")
    r = subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", MAGICRC, str(out / "gen.tcl")],
                       cwd=out, env=TOOL_ENV, capture_output=True, text=True, timeout=timeout)
    (out / "gen_magic.log").write_text(r.stdout + r.stderr)
    return {"rc": r.returncode, "log": rel(out / "gen_magic.log"),
            "gds": {d["cell"]: str(out / f"{d['cell']}.gds") for d in devices if (out / f"{d['cell']}.gds").exists()}}


def _run(cmd: list, env_extra: dict | None = None, timeout: int = 300) -> str:
    r = subprocess.run(cmd, env={**TOOL_ENV, **(env_extra or {})}, capture_output=True, text=True, timeout=timeout)
    return r.stdout + r.stderr


def drc(gds: Path, cell: str, out: Path) -> dict:
    txt = _run(["bash", str(SCRIPTS / "magic_drc.sh"), str(gds), cell, str(out)])
    tot = re.search(r"^DRC_TOTAL (\d+)", txt, re.M)
    neg = re.search(r"^NEG_CONTROL_TOTAL (\d+)", txt, re.M)
    total = int(tot.group(1)) if tot else None
    neg_n = int(neg.group(1)) if neg else None
    return {"errors": total, "neg_control_flagged": bool(neg_n and neg_n > (total or 0)),
            "pass": total == 0 and bool(neg_n and neg_n > 0), "report": rel(out / "drc_report.txt")}


def lvs_device(gds: Path, cell: str, model: str, W: float, L: float, nf: int, m: int, out: Path,
               mode: str = "subcell") -> dict:
    """Device-level LVS against the netlist values (um). mode 'subcell' compares the PCell inside its
    wrapper (S0); mode 'top' compares the wrapper, whose own labels D/G/S/B are the ports (S3 device
    cells with finger straps)."""
    out.mkdir(parents=True, exist_ok=True)
    if m != 1 and mode == "subcell":   # the PCell's m copies are drawn unconnected: check them as drawn
        return lvs_by_extraction(gds, cell, model, {"W": W / nf if nf > 1 else W, "L": L, "nf": nf}, m, out,
                                 neg_key="L", neg_delta=0.1)
    mpart = f" m={m}" if m != 1 else ""
    ref = out / "ref.spice"
    ref.write_text(f".subckt {cell} D G S B\nX{cell} D G S B {model} L={L:g} W={W:g} nf={nf}{mpart}\n.ends\n")
    txt = _run(["bash", str(SCRIPTS / "magic_lvs.sh"), str(gds), cell, str(ref), cell, str(out / "lvs")],
               {"LVS_MODE": mode})
    ok = "LVS_RESULT MATCH" in txt
    # negative control: same layout, reference with L + 0.1 um must not match
    bad = out / "ref_wrongL.spice"
    bad.write_text(ref.read_text().replace(f"L={L:g}", f"L={L + 0.1:g}"))
    txt2 = _run(["bash", str(SCRIPTS / "magic_lvs.sh"), str(gds), cell, str(bad), cell, str(out / "lvs_negctl")],
                {"LVS_MODE": mode})
    neg_ok = "LVS_RESULT FAIL" in txt2
    m_cell = re.search(r"cell=(\S+)", txt)
    return {"match": ok, "neg_control_rejected": neg_ok, "pass": ok and neg_ok,
            "pcell_instance": m_cell.group(1) if m_cell else None,
            "report": rel(out / "lvs" / "lvs_report.txt"), "extracted": rel(out / "lvs" / "extracted.spice")}


def _extracted(ext: Path) -> tuple[list, list]:
    """(ports, devices) of a Magic ext2spice subcircuit; a device is (name, nodes, model)."""
    txt = ext.read_text()
    lines, cur = [], ""
    for ln in txt.splitlines():
        if ln.startswith("+"):
            cur += " " + ln[1:].strip()
        else:
            if cur:
                lines.append(cur)
            cur = ln.strip()
    if cur:
        lines.append(cur)
    ports, devs = [], []
    for ln in lines:
        if ln.lower().startswith(".subckt"):
            ports = ln.split()[2:]
        elif ln[:1] in "Xx":
            tok = ln.split()
            mi = next((i for i, t in enumerate(tok) if t.startswith("sky130_fd_pr__")), None)
            if mi:
                devs.append((tok[0], tok[1:mi], tok[mi]))
    return ports, devs


def lvs_by_extraction(gds: Path, cell: str, model: str, props: dict, expected_devices: int, out: Path,
                      neg_key: str = "L", neg_delta: float = 1.0) -> dict:
    """Binding check for a PCell whose copies are not wired together (m > 1 MOSFETs, MF > 1 capacitors,
    resistors with an unconnected body pin): the reference is written with the extracted connectivity
    (ports and nodes as the PCell draws them) and the NETLIST's properties (W, L, nf), so netgen checks
    the device count, the model and every property; negative control: the same with L changed."""
    out.mkdir(parents=True, exist_ok=True)

    def run(ref_text, tag):
        ref = out / f"ref_{tag}.spice"
        ref.write_text(ref_text)
        return _run(["bash", str(SCRIPTS / "magic_lvs.sh"), str(gds), cell, str(ref), cell, str(out / tag)],
                    {"LVS_MODE": "subcell"})
    first = run(f".subckt {cell} A B\n.ends\n", "probe")
    ext = out / "probe" / "extracted.spice"
    if not ext.exists():
        return {"match": False, "neg_control_rejected": False, "pass": False, "error": "extraction failed: " + first[-300:]}
    ports, devs = _extracted(ext)

    def ref_text(pr):
        pp = " ".join(f"{k}={v:g}" if isinstance(v, (int, float)) else f"{k}={v}" for k, v in pr.items())
        body = "\n".join(f"X{i} {' '.join(n)} {model} {pp}" for i, (_, n, _) in enumerate(devs))
        return f".subckt {cell} {' '.join(ports)}\n{body}\n.ends\n"
    count_ok = len(devs) == expected_devices and all(m_ == model for _, _, m_ in devs)
    txt = run(ref_text(props), "lvs")
    ok = "LVS_RESULT MATCH" in txt and count_ok
    bad = dict(props)
    bad[neg_key] = float(props[neg_key]) + neg_delta
    neg_ok = "LVS_RESULT FAIL" in run(ref_text(bad), "lvs_negctl")
    return {"match": ok, "neg_control_rejected": neg_ok, "pass": ok and neg_ok, "ports": ports,
            "devices_extracted": len(devs), "devices_expected": expected_devices, "count_ok": count_ok,
            "report": rel(out / "lvs" / "lvs_report.txt"), "extracted": rel(ext)}


def lvs_passive(gds: Path, cell: str, model: str, params: dict, out: Path) -> dict:
    """PDK passive (MIM capacitor array of MF cells, poly resistor): see lvs_by_extraction."""
    mf = int(params.get("MF", 1))
    return lvs_by_extraction(gds, cell, model, {"W": float(params["W"]), "L": float(params["L"])}, mf, out)


def png(gds: Path, out_png: Path) -> str:
    _run(["klayout", "-zz", "-rd", f"gds={gds}", "-rd", f"png={out_png}", "-r", str(SCRIPTS / "gds_to_png.py")])
    return rel(out_png) if out_png.exists() else None


def extracted_params(lvs_dir: Path) -> dict:
    f = lvs_dir / "lvs" / "extracted.spice"
    if not f.exists():
        return {}
    m = re.search(r"^X\S*\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(.*)$", f.read_text(), re.M)
    return dict(re.findall(r"(\w+)=(\S+)", m.group(1))) if m else {}
