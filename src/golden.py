"""Golden-reference regression: the key results of each stage, snapshotted with tolerances.

A snapshot (tests/golden/<design>/<stage>.json) holds a flat {key: value} of what a stage must keep
producing: every gate's pass/fail, the simulated specs, the budgets, the chosen device options.
`compare` re-reads the current outputs and lists every key that moved beyond its tolerance.
Numbers use a relative tolerance (default 1e-3: same netlist, same tools) with an absolute floor;
booleans and strings must match exactly. A snapshot is rewritten only on purpose
(`python3 -m src.flow snapshot <design>`), and the git diff of the snapshot shows what changed.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from src.common.tools import REPO

GOLDEN = REPO / "tests" / "golden"
RTOL = 1e-3
ATOL = 1e-9
# looser where a result is legitimately noisy (fractions of a margin, SPICE step slopes)
TOL_OVERRIDES = {"verify.": (0.0, 0.005)}


def snapshot_path(design: str, stage: str) -> Path:
    return GOLDEN / design / f"{stage}.json"


def designs_with_snapshots() -> list[str]:
    return sorted(p.name for p in GOLDEN.glob("*") if p.is_dir())


def _load(stage: str, design: str, name: str):
    p = REPO / "outputs" / stage / design / name
    return json.loads(p.read_text()) if p.exists() else None


def _gates(rep: dict) -> dict:
    return {f"gate.{k}": (v.get("pass") if isinstance(v, dict) else v) for k, v in (rep.get("gates") or {}).items()}


def extract(design: str, stage: str) -> dict:
    out: dict = {}
    rep = _load(stage, design, f"{stage.lower()}_report.json")
    if rep is None:
        return out
    out.update(_gates(rep))
    if stage == "S0":
        for tb, r in (rep.get("testbenches") or {}).items():
            for k, v in (r.get("meas") or {}).items():
                out[f"tb.{tb}.{k}"] = v
    elif stage == "S1":
        g = rep["gates"].get("G1.2_linear_model_vs_spice") or {}
        for k, v in (g.get("linear") or {}).items():
            out[f"linear.{k}"] = v
        intent = _load("S1", design, "intent.json") or {}
        for n in intent.get("critical_nets", []):
            for k, v in (n.get("per_fF") or {}).items():
                out[f"per_fF.{n['net']}.{k}"] = v
    elif stage == "S2":
        out["eta"] = rep.get("eta")
        b = _load("S2", design, "budgets.json") or {}
        for e in b.get("elements", []):
            out[f"budget.{e['id']}"] = e.get("budget")
        v = rep["gates"].get("G2.5_spice_budget_verification") or {}
        for row in v.get("rows", []):
            out[f"verify.{row['check']}"] = row.get("spice_use_frac_of_margin")
    elif stage == "S3":
        d = _load("S3", design, "device_decisions.json") or {}
        if d:   # the relaxed-type rule (recorded since 2026-10-27; the runs before used 'default')
            out["relax_fallback"] = d.get("relax_fallback") or "default"
        for t, dec in (d.get("decisions") or {}).items():
            out[f"chosen.{t}"] = (dec.get("chosen") or {}).get("id")
            out[f"area.{t}"] = dec.get("area_um2")
        for k, v in (d.get("final_in_circuit") or {}).items():
            if isinstance(v, (int, float)):
                out[f"final.{k}"] = v
    return out


def write_snapshot(design: str, stage: str) -> Path:
    p = snapshot_path(design, stage)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"design": design, "stage": stage, "rtol": RTOL, "values": extract(design, stage)},
                            indent=1, sort_keys=True) + "\n")
    return p


def _tol(key: str, snap_rtol: float) -> tuple[float, float]:
    for prefix, t in TOL_OVERRIDES.items():
        if key.startswith(prefix):
            return t
    return snap_rtol, ATOL


def compare(design: str, stage: str) -> list[str]:
    snap = json.loads(snapshot_path(design, stage).read_text())
    now = extract(design, stage)
    diffs = []
    for k, ref in snap["values"].items():
        if k not in now:
            diffs.append(f"{k}: missing now (was {ref!r})")
            continue
        cur = now[k]
        if isinstance(ref, bool) or ref is None or isinstance(ref, str):
            if cur != ref:
                diffs.append(f"{k}: {ref!r} -> {cur!r}")
        elif isinstance(ref, (int, float)):
            if not isinstance(cur, (int, float)) or isinstance(cur, bool):
                diffs.append(f"{k}: {ref!r} -> {cur!r}")
                continue
            rtol, atol = _tol(k, snap.get("rtol", RTOL))
            if not math.isclose(cur, ref, rel_tol=rtol, abs_tol=max(atol, ATOL)):
                diffs.append(f"{k}: {ref:.6g} -> {cur:.6g}")
    for k in now.keys() - snap["values"].keys():
        if k.startswith("gate.") and now[k] is not None:   # a new information-only gate is not a change
            diffs.append(f"{k}: new gate (now {now[k]!r})")
    return diffs
