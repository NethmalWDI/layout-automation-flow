#!/usr/bin/env python3
"""The local GUI's helper (gui/gui.ps1 calls it through docker exec; it never calls an LLM).

usage (inside layout-s0s3, repo root):
  python3 scripts/gui_backend.py list                    designs with their stage results
  python3 scripts/gui_backend.py get <design>            the editable texts of a design (netlist, hierarchy, specs,
                                                         layout instructions) and its element names
  python3 scripts/gui_backend.py save <request.json>     save edits as a NEW design copy (Imasha, 2026-11-04): the
                                                         original's frozen sources and results stay untouched
  python3 scripts/gui_backend.py status <design>         stage results, whether a GUI run is going, its log's tail
  python3 scripts/gui_backend.py template <request.json> a starting config.yaml for a new netlist (ports by name;
                                                         every value the design must give left null: FILL IN)
  python3 scripts/gui_backend.py new <request.json>      a brand-new design from uploaded files (netlist, config,
                                                         optional benches, hierarchy, measurements, layout
                                                         instructions, other files kept in extra/)
Each prints one JSON object.

A copy gets circuits/<new>/{source,testbenches,upstream}/ and inputs/<new>/ from the base design, with the edited
texts written over the copied ones, every path in its package re-pointed to the copy, a SOURCE.md saying where it
came from and what was edited, and the SHA-256 of its netlist, config and measurements appended to
circuits/SOURCE_SHA256.txt (S0's gate G0.3 checks them).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from src.common import spice  # noqa: E402

NAME = re.compile(r"^[a-z][a-z0-9_]{1,40}$")
STAGES = ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7"]


def out(obj) -> None:
    print(json.dumps(obj))


def package(design: str) -> dict:
    return yaml.safe_load((REPO / "inputs" / design / "package.yaml").read_text())


def designs() -> list:
    return sorted(p.parent.name for p in (REPO / "inputs").glob("*/package.yaml") if not p.parent.name.startswith("_"))


def hierarchy_path(pkg: dict) -> str | None:
    return (pkg.get("upstream") or {}).get("hierarchy")


def elements(netlist: Path) -> list:
    try:
        nl = spice.parse(netlist)
    except Exception as e:   # the GUI shows the parser's message
        return [f"(netlist does not parse: {e})"]
    return sorted([m.name for m in nl.mosfets] + [p.name for p in nl.passives] + [s.name for s in nl.sources])


def hier_elements(h: dict) -> set:
    """Every element a hierarchy file names: the upstream 'levels' format, or any 'elements'/'devices' lists."""
    found = set()

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in ("elements", "devices") and isinstance(v, list):
                    found.update(e for e in v if isinstance(e, str))
                else:
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(h)
    return found


def stage_table(design: str) -> dict:
    f = REPO / "outputs" / "flow" / design / "flow_summary.json"
    st = json.loads(f.read_text()).get("stages", {}) if f.exists() else {}
    return {s: {"status": st.get(s, {}).get("status"), "failed": st.get(s, {}).get("failed_gates") or [],
                "started": st.get(s, {}).get("started")} for s in STAGES}


def cmd_list() -> None:
    res = []
    for d in designs():
        pkg = package(d)
        res.append({"design": d, "description": " ".join((pkg.get("description") or "").split())[:240],
                    "layout_yaml": (REPO / "inputs" / d / "layout.yaml").exists(), "stages": stage_table(d),
                    "report": (REPO / "docs" / "reports" / f"{d}_report.html").exists()})
    out({"designs": res})


def read(rel: str | None) -> str:
    return (REPO / rel).read_text() if rel and (REPO / rel).exists() else ""


def cmd_get(design: str) -> None:
    pkg = package(design)
    lay = REPO / "inputs" / design / "layout.yaml"
    out({"design": design, "package": (REPO / "inputs" / design / "package.yaml").read_text(),
         "netlist_path": pkg["netlist"], "netlist": read(pkg["netlist"]),
         "hierarchy_path": hierarchy_path(pkg), "hierarchy": read(hierarchy_path(pkg)),
         "config_path": pkg["config"], "config": read(pkg["config"]),
         "layout": lay.read_text() if lay.exists() else "", "elements": elements(REPO / pkg["netlist"])})


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check(req: dict, base_pkg: dict) -> tuple[list, list]:
    """(errors, warnings) for the edited texts; errors stop the save."""
    errs, warns = [], []
    if req.get("hierarchy"):
        try:
            h = json.loads(req["hierarchy"])
        except json.JSONDecodeError as e:
            errs.append(f"hierarchy: not valid JSON ({e})")
            h = None
    else:
        h = None
    for key in ("config", "layout"):
        if req.get(key):
            try:
                yaml.safe_load(req[key])
            except yaml.YAMLError as e:
                errs.append(f"{key}: not valid YAML ({str(e).splitlines()[0]})")
    if h is not None:
        tmp = REPO / "runs" / "tmp" / "gui" / "check.spice"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(req.get("netlist") or read(base_pkg["netlist"]))
        names = set(elements(tmp))
        missing = sorted(hier_elements(h) - names)
        if missing:
            warns.append(f"hierarchy names {len(missing)} element(s) not in the netlist: {missing[:12]}")
    return errs, warns


def cmd_save(reqfile: str) -> None:
    req = json.loads(Path(reqfile).read_text())
    base, new = req.get("base", ""), req.get("new", "")
    if base not in designs():
        return out({"ok": False, "errors": [f"unknown base design {base!r}"]})
    if not NAME.match(new):
        return out({"ok": False, "errors": ["the new name: lower-case letters, digits and _, starting with a letter"]})
    if new in designs() or (REPO / "circuits" / new).exists():
        return out({"ok": False, "errors": [f"{new} exists already; choose another name"]})
    bpkg = package(base)
    errs, warns = check(req, bpkg)
    if errs:
        return out({"ok": False, "errors": errs, "warnings": warns})
    src_c, dst_c = REPO / "circuits" / base, REPO / "circuits" / new
    for sub in ("source", "testbenches", "upstream"):
        if (src_c / sub).is_dir():
            shutil.copytree(src_c / sub, dst_c / sub)
    dst_i = REPO / "inputs" / new
    shutil.copytree(REPO / "inputs" / base, dst_i)
    text = (REPO / "inputs" / base / "package.yaml").read_text()
    text = text.replace(f"circuits/{base}/", f"circuits/{new}/").replace(f"inputs/{base}/", f"inputs/{new}/")
    text = re.sub(rf"^design:\s*{re.escape(base)}\s*$", f"design: {new}", text, flags=re.M)
    pkg = yaml.safe_load(text)
    edited = []
    # the hierarchy always lives in the copy, so the copy owns what it was given (S5 reads circuits/<d>/upstream/)
    hp = hierarchy_path(pkg)
    new_hp = f"circuits/{new}/upstream/hierarchy.json"
    if hp and hp != new_hp:
        (dst_c / "upstream").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO / hp, REPO / new_hp)
        text = text.replace(f"hierarchy: {hp}", f"hierarchy: {new_hp}")
        pkg = yaml.safe_load(text)
    for key, rel in (("netlist", pkg["netlist"]), ("hierarchy", hierarchy_path(pkg)), ("config", pkg["config"])):
        if req.get(key):
            if not rel or not rel.startswith(f"circuits/{new}/"):
                return out({"ok": False, "errors": [f"{key}: the base design keeps it outside circuits/{base}/"]})
            (REPO / rel).write_text(req[key] if req[key].endswith("\n") else req[key] + "\n")
            edited.append(key)
    if req.get("layout") is not None:
        lay = dst_i / "layout.yaml"
        if req["layout"].strip():
            lay.write_text(req["layout"] if req["layout"].endswith("\n") else req["layout"] + "\n")
            edited.append("layout instructions")
        elif lay.exists():
            lay.unlink()
            edited.append("layout instructions (removed)")
    (dst_i / "package.yaml").write_text(f"# Copy of {base}, made with the local GUI on {dt.date.today()} "
                                        f"(edited: {', '.join(edited) or 'nothing'}).\n" + text)
    note = (req.get("note") or "").strip()
    sha_lines, rec = [], []
    for key in ("netlist", "config", "achieved"):
        if pkg.get(key) and str(pkg[key]).startswith(f"circuits/{new}/"):
            f = REPO / pkg[key]
            sha_lines.append(f"{sha256(f)}  {pkg[key].replace('circuits/', '', 1)}")
            rec.append(f"- `{pkg[key].replace(f'circuits/{new}/', '')}` {sha256(f)}")
    with open(REPO / "circuits" / "SOURCE_SHA256.txt", "a") as fh:
        fh.write("\n".join(sha_lines) + "\n")
    (dst_c / "SOURCE.md").write_text(
        f"# {new}: provenance\n\nA copy of `{base}` made with the local GUI (`gui/gui.ps1`) on {dt.date.today()}.\n\n"
        f"- **Edited:** {', '.join(edited) or 'nothing'}.\n"
        f"- **Unchanged from {base}:** everything else (see `circuits/{base}/SOURCE.md` for their origin).\n"
        + (f"- **Note from the GUI:** {note}\n" if note else "")
        + "\nSHA-256 recorded in `circuits/SOURCE_SHA256.txt` (S0 gate G0.3):\n" + "\n".join(rec) + "\n")
    out({"ok": True, "design": new, "edited": edited, "warnings": warns})


# ------------------------------------------------------------------------------------------- a brand-new design
STD_PORTS = {"INP": ["inp", "ip", "vp", "vinp", "in_p", "inplus", "vin_p"], "INN": ["inn", "in", "vm", "vinn", "in_n",
             "inminus", "vin_n"], "OUTP": ["outp", "op", "vop", "out_p", "voutp"], "OUTN": ["outn", "on", "vom", "out_n",
             "voutn"], "OUT": ["out", "vout", "output"], "VDD": ["vdd", "vdpwr", "avdd", "vcc"], "VSS": ["vss", "gnd",
             "vgnd", "avss", "0"]}


def _netlist_from(req: dict, work: Path) -> tuple[Path | None, str | None]:
    """The request's netlist, flattened from `flatten_top` when given; (path, error)."""
    work.mkdir(parents=True, exist_ok=True)
    raw = work / "raw.spice"
    raw.write_text(req.get("netlist") or "")
    if not (req.get("netlist") or "").strip():
        return None, "a netlist is required"
    top = (req.get("flatten_top") or "").strip()
    if not top:
        return raw, None
    sys.path.insert(0, str(REPO / "scripts"))
    import flatten_spice
    flat = work / "flat.spice"
    try:
        flatten_spice.flatten(raw, top, flat, req.get("name") or top)
    except SystemExit as e:
        return None, f"flattening failed: {e}"
    return flat, None


def cmd_template(reqfile: str) -> None:
    """A starting config.yaml for a new netlist: its ports mapped to the bench's by name where the name is a usual
    one; every value the design must give is left null with FILL IN (nothing is guessed)."""
    req = json.loads(Path(reqfile).read_text())
    path, err = _netlist_from(req, REPO / "runs" / "tmp" / "gui" / "new")
    if err:
        return out({"ok": False, "errors": [err]})
    try:
        nl = spice.parse(path)
    except Exception as e:
        return out({"ok": False, "errors": [f"the netlist does not parse: {e}"]})
    ports, used = {}, set()
    for tb, cands in STD_PORTS.items():
        hit = next((p for p in nl.ports if p.lower() in cands and p not in used), None)
        if hit:
            ports[tb] = hit
            used.add(hit)
    diff = "OUTP" in ports and "OUTN" in ports
    if not diff and "OUT" in ports:
        ports["OUTP"] = ports.pop("OUT")
    lines = [f"# config.yaml for {req.get('name') or nl.name}: written by the GUI from the netlist's ports. Fill in every",
             "# null (FILL IN). Values that are not the design's own are marked ASSUMPTION in spec_notes.",
             f"name: {req.get('name') or nl.name}", "interface:", "  input: differential",
             f"  output: {'differential' if diff else 'single_ended'}", "  kind: amp", "  dut_symbol: dut_amp",
             "  ports:                  # bench port: the netlist's port"]
    for tb in ("INP", "INN", "OUTP", "OUTN", "VDD", "VSS"):
        if tb == "OUTN" and not diff:
            continue
        lines.append(f"    {tb}: {ports[tb]}" if tb in ports else f"    {tb}: null       # FILL IN: which port is {tb}?")
    others = [p for p in nl.ports if p not in ports.values()]
    if others:
        lines.append(f"  # other ports ({', '.join(others)}): declare them under bias_sources or port_roles below the "
                     "form, or drive them in the bench wrapper lines")
    lines += ["analyses: [AC, OP, NOISE]", "conditions:", "  VDD_V: null      # FILL IN (V)",
              "  VCM_V: null      # FILL IN (V)", "  CL_F: null       # FILL IN (load per output, e.g. 0.5p)",
              "  temp: 27", "  corner: tt", "specs: {}           # FILL IN: min/max per measurement, for example",
              "#  pm_deg: {min: ...}", "#  gain_db: {min: ...}", "#  gbw_mhz: {min: ...}", "#  power_uw: {max: ...}",
              "spec_notes: {}      # say here which values are ASSUMPTIONs"]
    out({"ok": True, "config": "\n".join(lines) + "\n", "ports": nl.ports, "subckt": nl.name, "differential": diff,
         "elements": len(nl.mosfets) + len(nl.passives) + len(nl.sources)})


def _benches(nl, cfg: dict, design: str, dut_sub: str, wrapper: str) -> tuple[dict, list]:
    sys.path.insert(0, str(REPO / "scripts"))
    import benchlib
    iface = (cfg.get("interface") or {})
    ports = {k: v for k, v in (iface.get("ports") or {}).items() if v not in (None, "NC")}
    inv = {v: k for k, v in ports.items()}
    diff = iface.get("output") == "differential"
    warns = []
    nodes = []
    for p in nl.ports:
        tb = inv.get(p)
        if tb == "OUT":
            tb = "OUTP"
        if tb in ("INP", "INN", "OUTP", "OUTN", "VDD", "VSS"):
            nodes.append(tb)
        else:
            nodes.append(f"{p}_w")
            warns.append(f"port {p} is not a bench port: it is node {p}_w in the bench wrapper; drive it in the "
                         "wrapper lines or declare it under bias_sources / port_roles")
    xdut = "XDUT " + " ".join(nodes) + f" {nl.name}"
    out_ = {}
    for kind in ("AC", "OP", "NOISE"):
        name = f"{'dido' if diff else 'diso'}_amp_{kind}.spice"
        out_[name] = benchlib.bench(design, kind, dut_sub, xdut, differential_output=diff,
                                    wrapper_extra=(wrapper.strip() + "\n") if wrapper.strip() else "")
    return out_, warns


def cmd_new(reqfile: str) -> None:
    """A brand-new design from the GUI's uploads: circuits/<d>/{source,testbenches,upstream,extra}/ and
    inputs/<d>/package.yaml; the benches are generated with scripts/benchlib.py unless uploaded."""
    import base64
    req = json.loads(Path(reqfile).read_text())
    d = (req.get("name") or "").strip()
    if not NAME.match(d):
        return out({"ok": False, "errors": ["the name: lower-case letters, digits and _, starting with a letter"]})
    if d in designs() or (REPO / "circuits" / d).exists() or (REPO / "inputs" / d).exists():
        return out({"ok": False, "errors": [f"{d} exists already; choose another name"]})
    errs, warns = [], []
    path, err = _netlist_from(req, REPO / "runs" / "tmp" / "gui" / "new")
    if err:
        return out({"ok": False, "errors": [err]})
    try:
        nl = spice.parse(path)
    except Exception as e:
        return out({"ok": False, "errors": [f"the netlist does not parse: {e}"]})
    from src.s0.ingest import ALLOWED_MODELS
    errs += [f"netlist: {e}" for e in spice.validate(nl, ALLOWED_MODELS)]
    try:
        cfg = yaml.safe_load(req.get("config") or "") or {}
    except yaml.YAMLError as e:
        cfg = {}
        errs.append(f"config: not valid YAML ({str(e).splitlines()[0]})")
    if not cfg.get("interface", {}).get("ports"):
        errs.append("config: interface.ports is missing (use 'Make a starting config')")
    nulls = [k for k, v in (cfg.get("conditions") or {}).items() if v is None]
    if nulls:
        errs.append(f"config: conditions still null: {nulls}")
    if not cfg.get("specs"):
        errs.append("config: no specs")
    opt = {}
    for key in ("bias_sources", "port_roles"):
        try:
            opt[key] = yaml.safe_load(req.get(key) or "") or {}
        except yaml.YAMLError as e:
            errs.append(f"{key}: not valid YAML ({str(e).splitlines()[0]})")
    for key, parse in (("hierarchy", json.loads), ("measurements", json.loads), ("layout", yaml.safe_load)):
        if (req.get(key) or "").strip():
            try:
                parse(req[key])
            except Exception as e:
                errs.append(f"{key}: does not parse ({str(e).splitlines()[0]})")
    if not (req.get("measurements") or "").strip() and not req.get("derive_specs"):
        errs.append("S0 needs the schematic's own results to know each spec's margin: upload measurements made with "
                    "these benches, or tick 'Specs from the schematic's own results'")
    if errs:
        return out({"ok": False, "errors": errs})
    if req.get("hierarchy"):
        missing = sorted(hier_elements(json.loads(req["hierarchy"])) - set(elements(path)))
        if missing:
            warns.append(f"hierarchy names {len(missing)} element(s) not in the netlist: {missing[:12]}")
    base = REPO / "circuits" / d
    for sub in ("source", "testbenches", "upstream", "extra"):
        (base / sub).mkdir(parents=True, exist_ok=True)
    net_rel = f"circuits/{d}/source/{d}.spice"
    text = path.read_text()
    (REPO / net_rel).write_text(text if text.rstrip().endswith(".end") else text.rstrip() + "\n.end\n")
    cfg_rel = f"circuits/{d}/source/config.yaml"
    (REPO / cfg_rel).write_text(req["config"] if req["config"].endswith("\n") else req["config"] + "\n")
    ach_rel = None
    if (req.get("measurements") or "").strip():
        ach_rel = f"circuits/{d}/source/measurements.json"
        (REPO / ach_rel).write_text(req["measurements"])
    tbs = {t["name"]: t["text"] for t in (req.get("testbenches") or []) if t.get("name") and t.get("text")}
    generated = not tbs
    if generated:
        # the DUT subckt as S0 writes it from the parsed netlist (xschem comments the top header out: '**.subckt')
        from src.s0.ingest import write_full
        tbs, w = _benches(nl, cfg, d, write_full(nl, nl.name), req.get("wrapper") or "")
        warns += w
    tb_rel = []
    for name, t in tbs.items():
        safe = re.sub(r"[^A-Za-z0-9_.-]", "_", Path(name).name)
        (base / "testbenches" / safe).write_text(t)
        tb_rel.append(f"circuits/{d}/testbenches/{safe}")
    hier_rel = None
    if (req.get("hierarchy") or "").strip():
        hier_rel = f"circuits/{d}/upstream/hierarchy.json"
        (REPO / hier_rel).write_text(req["hierarchy"])
    kept = []
    for x in req.get("extras") or []:
        safe = re.sub(r"[^A-Za-z0-9_.-]", "_", Path(x.get("name", "file")).name)
        (base / "extra" / safe).write_bytes(base64.b64decode(x.get("b64") or ""))
        kept.append(safe)
    (REPO / "inputs" / d).mkdir(parents=True, exist_ok=True)
    if (req.get("layout") or "").strip():
        (REPO / "inputs" / d / "layout.yaml").write_text(req["layout"] if req["layout"].endswith("\n") else req["layout"] + "\n")
    pkg = {"design": d, "description": (req.get("description") or f"{d}, made with the local GUI").strip(),
           "netlist": net_rel, "config": cfg_rel, "achieved": ach_rel, "testbenches": tb_rel,
           "dut_subckt_in_testbench": nl.name,
           "upstream": {"netlist": net_rel if hier_rel else None, "hierarchy": hier_rel, "primitives": None,
                        "equations": None, "name_map": None},
           "predicted": [], "bias_sources": opt.get("bias_sources") or {}, "operating_point": None,
           "variation_ranges": None, "conditions_override": {}}
    if opt.get("port_roles"):
        pkg["port_roles"] = opt["port_roles"]
    if generated:   # the generated benches drive through couplers, so S1 is told the AC drive (as LOADBench, ttsky)
        diff = (cfg.get("interface") or {}).get("output") == "differential"
        pkg["ac_drive"] = {"INP": 0.5, "INN": -0.5} if diff else {"INP": 1.0, "INN": 0.0}
        if ach_rel:
            warns.append("the uploaded measurements come from other benches than the generated ones, so S0's G0.6 "
                         "(reproduce the measurements) will most likely fail; leave them out to use S0's own results")
    if req.get("derive_specs"):
        pkg["specs_from_achieved"] = {"gain_db": {"min_delta": -1.0}, "gbw_mhz": {"min_factor": 0.9},
                                      "power_uw": {"max_factor": 1.1}}
    (REPO / "inputs" / d / "package.yaml").write_text(
        f"# New design made with the local GUI on {dt.date.today()} (gui/gui.ps1). Field reference: docs/INPUTS.md.\n"
        + yaml.safe_dump(pkg, sort_keys=False))
    sha_lines, rec = [], []
    for rel in [net_rel, cfg_rel] + ([ach_rel] if ach_rel else []):
        h = sha256(REPO / rel)
        sha_lines.append(f"{h}  {rel.replace('circuits/', '', 1)}")
        rec.append(f"- `{rel.replace(f'circuits/{d}/', '')}` {h}")
    with open(REPO / "circuits" / "SOURCE_SHA256.txt", "a") as fh:
        fh.write("\n".join(sha_lines) + "\n")
    note = (req.get("note") or "").strip()
    (base / "SOURCE.md").write_text(
        f"# {d}: provenance\n\nA new design made with the local GUI (`gui/gui.ps1`) on {dt.date.today()}.\n\n"
        f"| Item | Origin |\n|---|---|\n"
        f"| Netlist | uploaded{' and flattened from ' + req['flatten_top'] if req.get('flatten_top') else ''} |\n"
        f"| Specs and conditions (`config.yaml`) | uploaded / written in the GUI (ASSUMPTIONs as marked inside) |\n"
        f"| Measurements | {'uploaded' if ach_rel else 'none (S0 simulates the schematic itself)'} |\n"
        f"| Testbenches | {'generated by scripts/benchlib.py (DC-closed through chokes)' if generated else 'uploaded'} |\n"
        f"| Hierarchy | {'uploaded' if hier_rel else 'none'} |\n"
        f"| Layout instructions | {'uploaded' if (req.get('layout') or '').strip() else 'none (defaults)'} |\n"
        f"| Other files kept (`extra/`, not read by the flow) | {', '.join(kept) or 'none'} |\n"
        + (f"\nNote from the GUI: {note}\n" if note else "")
        + "\nSHA-256 recorded in `circuits/SOURCE_SHA256.txt` (S0 gate G0.3):\n" + "\n".join(rec) + "\n")
    out({"ok": True, "design": d, "testbenches": [Path(r).name for r in tb_rel], "generated_benches": generated,
         "extras": kept, "warnings": warns})


def cmd_status(design: str) -> None:
    log = REPO / "runs" / "logs" / f"gui_{design}.log"
    ex = REPO / "runs" / "logs" / f"gui_{design}.log.exit"
    rlog = REPO / "runs" / "logs" / f"gui_{design}_report.log"
    rex = REPO / "runs" / "logs" / f"gui_{design}_report.log.exit"
    tail = log.read_text(errors="replace").splitlines()[-25:] if log.exists() else []
    rtail = rlog.read_text(errors="replace").splitlines()[-8:] if rlog.exists() else []
    out({"design": design, "stages": stage_table(design),
         "running": log.exists() and not ex.exists(), "exit": ex.read_text().strip() if ex.exists() else None,
         "log": tail, "report_running": rlog.exists() and not rex.exists(),
         "report_exit": rex.read_text().strip() if rex.exists() else None, "report_log": rtail,
         "report": f"docs/reports/{design}_report.html" if (REPO / "docs" / "reports" / f"{design}_report.html").exists()
         else None})


def main(argv: list) -> int:
    if not argv:
        print(__doc__)
        return 2
    cmd, args = argv[0], argv[1:]
    if cmd == "list":
        cmd_list()
    elif cmd in ("get", "status") and args and args[0] in designs():
        {"get": cmd_get, "status": cmd_status}[cmd](args[0])
    elif cmd == "save" and args:
        cmd_save(args[0])
    elif cmd == "new" and args:
        cmd_new(args[0])
    elif cmd == "template" and args:
        cmd_template(args[0])
    else:
        out({"ok": False, "errors": [f"bad command or unknown design: {argv}"]})
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
