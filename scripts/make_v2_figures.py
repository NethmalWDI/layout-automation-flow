#!/usr/bin/env python3
"""Figures for flow record section 7 (plan v2), drawn only from the committed run outputs:
outputs/compare/<design>/<tag>.json (snapshots), outputs/S0/<design>/circuit_ir.json (spec limits, optional)
and outputs/reference_layout/<design>/reference_layout*.json. Nothing is simulated here.

  python3 scripts/make_v2_figures.py            -> docs/flow_record/img/v2_*.png

Documentation only (2026-10-27, Cowork): it does not change any flow result.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
CMP = REPO / "outputs" / "compare"
IMG = REPO / "docs" / "flow_record" / "img"
DESIGNS = ["example_ota_5t", "ota5t_stress", "loadbench_miller", "iadc_ota", "ttsky25a_fd"]
SHORT = {"example_ota_5t": "5T OTA", "ota5t_stress": "5T stress", "loadbench_miller": "LOADBench Miller",
         "iadc_ota": "iadc OTA", "ttsky25a_fd": "TTSKY25a FD"}
RULES = ["per_net", "equal", "lp_sum", "lp_floor", "ours"]
RULE_LABEL = {"per_net": "per-net", "equal": "equal split", "lp_sum": "plain LP", "lp_floor": "LP + floors",
              "ours": "ours (joint)"}
# a run whose snapshot is known not to be a result (flow record 7.1, row 40)
INVALID = {("ttsky25a_fd", "after_eta0.9"): "not valid:\nS2 crashed"}

# palette: dataviz reference instance (light), validated: categorical slots 1-3, status palette, text tokens
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
C_BEFORE, C_AFTER, C_POST = "#2a78d6", "#eb6834", "#1baf7a"
C_BLUE_LIGHT = "#9ec5f4"
ST_GOOD, ST_WARN, ST_SERIOUS, ST_CRIT, ST_NONE = "#0ca30c", "#fab219", "#ec835a", "#d03b3b", "#d9d8d3"

plt.rcParams.update({"font.family": ["DejaVu Sans"], "font.size": 10, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF})


def snap(d: str, tag: str):
    f = CMP / d / f"{tag}.json"
    return json.loads(f.read_text()) if f.exists() else None


def spec_limits(d: str) -> dict:
    f = REPO / "outputs" / "S0" / d / "circuit_ir.json"
    if not f.exists():
        return {}
    return {k: (v["kind"], v.get("limit")) for k, v in json.loads(f.read_text())["margins"].items()}


def clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def fig_gates():
    """Which stage gates failed, before (v1) and after (v2), per design."""
    fig, ax = plt.subplots(figsize=(11.5, 3.9))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, len(DESIGNS))
    ax.invert_yaxis()
    ax.axis("off")
    for j, st in enumerate(["S0", "S1", "S2", "S3"]):
        for k, tag in enumerate(["before", "after"]):
            x = 2 * j + k
            ax.text(x + 0.5, -0.12, f"{st} {tag}", ha="center", va="bottom", fontsize=9, color=INK2)
    for i, d in enumerate(DESIGNS):
        ax.text(-0.08, i + 0.5, SHORT[d], ha="right", va="center", fontsize=10)
        for j, st in enumerate(["S0", "S1", "S2", "S3"]):
            for k, tag in enumerate(["before", "after"]):
                r = snap(d, tag) or {}
                rec = r.get(st)
                x = 2 * j + k
                if not rec:
                    col, txt = ST_NONE, "not run"
                elif rec.get("failed"):
                    col = ST_CRIT
                    txt = "\n".join(g.split("_")[0] for g in rec["failed"])
                else:
                    col, txt = ST_GOOD, "PASS"
                ax.add_patch(Rectangle((x + 0.04, i + 0.06), 0.92, 0.88, facecolor=col, alpha=0.18,
                                       edgecolor=col, linewidth=1.2))
                ax.text(x + 0.5, i + 0.5, ("FAIL\n" + txt) if col == ST_CRIT else txt, ha="center",
                        va="center", fontsize=8.5, color=INK)
    ax.set_title("Stage gates before (v1) and after (v2): green = all gates pass, red = the gates listed failed",
                 fontsize=11, loc="left", pad=22)
    fig.tight_layout()
    fig.savefig(IMG / "v2_gates_before_after.png", dpi=160)
    plt.close(fig)


def fig_s3():
    """S3 total device area, before / after / post hoc, with whether every spec is met in the circuit."""
    fig, axs = plt.subplots(1, 5, figsize=(13, 3.6))
    for ax, d in zip(axs, DESIGNS):
        lim = spec_limits(d)
        tags = [("before", "before (v1)", C_BEFORE), ("after", "after (v2)", C_AFTER),
                ("after_posthoc_leastbad", "post hoc", C_POST)]
        xs, hs, cs, labs, notes = [], [], [], [], []
        for t, lab, c in tags:
            r = snap(d, t)
            s3 = (r or {}).get("S3") or {}
            if not s3.get("total_device_area_um2"):
                continue
            fin = s3.get("final") or {}
            miss = [k for k, (kind, l) in lim.items() if l is not None and fin.get(k) is not None
                    and ((fin[k] < l) if kind == "min" else (fin[k] > l))]
            xs.append(len(xs))
            hs.append(s3["total_device_area_um2"])
            cs.append(c)
            labs.append(lab)
            notes.append("specs met" if not miss else "misses " + ", ".join(
                f"{k.split('_')[0].upper()} {fin[k]:.1f}" for k in miss))
        ax.bar(xs, hs, color=cs, width=0.62, edgecolor=SURF, linewidth=2)
        for x, h, n in zip(xs, hs, notes):
            ax.text(x, h * 1.02, f"{h:,.0f}", ha="center", va="bottom", fontsize=8.5, color=INK)
            ax.text(x, h * 0.5, n.replace(", ", "\n"), ha="center", va="center", fontsize=7.5,
                    color="#ffffff" if "met" in n else INK, rotation=90)
        ax.set_xticks(xs, labs, fontsize=8)
        ax.set_title(SHORT[d], fontsize=10)
        ax.set_ylim(0, max(hs) * 1.18)
        clean(ax)
    axs[0].set_ylabel("S3 total device area (µm²)")
    fig.suptitle("S3: device area and whether the chosen cells meet every spec in the circuit (post hoc = "
                 "'least-bad' fallback, not plan v2)", fontsize=11, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(IMG / "v2_s3_area_specs.png", dpi=160)
    plt.close(fig)


def outcome_style(o: str | None):
    if o is None:
        return ST_NONE, "–"
    base = o.split(" (")[0]
    col = {"ok": ST_GOOD, "infeasible": ST_WARN, "unsafe": ST_SERIOUS, "unsafe + infeasible": ST_CRIT}.get(base, ST_NONE)
    short = {"ok": "ok", "infeasible": "infeasible", "unsafe": "unsafe", "unsafe + infeasible": "unsafe +\ninfeasible"}[base]
    return col, short + ("\n(unverified)" if "unverified" in o else "")


def fig_rules():
    """The five budget rules: outcome per design, at the design's own eta and at eta 0.9 (PREREG headline)."""
    fig, axs = plt.subplots(1, 2, figsize=(13.5, 4.6))
    for ax, tag, title in ((axs[0], "after", "at each design's own eta (0.5; stress 0.9)"),
                           (axs[1], "after_eta0.9", "at eta = 0.9 (PREREG headline)")):
        ax.set_xlim(0, len(RULES))
        ax.set_ylim(0, len(DESIGNS))
        ax.invert_yaxis()
        ax.axis("off")
        for j, m in enumerate(RULES):
            ax.text(j + 0.5, -0.1, RULE_LABEL[m], ha="center", va="bottom", fontsize=9, color=INK2)
        for i, d in enumerate(DESIGNS):
            ax.text(-0.06, i + 0.5, SHORT[d], ha="right", va="center", fontsize=9.5)
            r = snap(d, tag)
            if (d, tag) in INVALID or r is None:
                ax.add_patch(Rectangle((0.04, i + 0.06), len(RULES) - 0.08, 0.88, facecolor=SURF,
                                       edgecolor=INK2, hatch="//", linewidth=1))
                ax.text(len(RULES) / 2, i + 0.5, INVALID.get((d, tag), "no run").replace("\n", " ")
                        + " (see 7.1 row 40)", ha="center", va="center", fontsize=9,
                        bbox=dict(facecolor=SURF, edgecolor="none"))
                continue
            bl = (r.get("S2") or {}).get("baselines") or {}
            for j, m in enumerate(RULES):
                sc = bl.get(m) or {}
                col, txt = outcome_style(sc.get("outcome"))
                u = sc.get("spice_worst_use_of_allowed")
                ax.add_patch(Rectangle((j + 0.04, i + 0.06), 0.92, 0.88, facecolor=col, alpha=0.22,
                                       edgecolor=col, linewidth=1.4 if m == "ours" else 0.8))
                ax.text(j + 0.5, i + 0.42, txt, ha="center", va="center", fontsize=7.8, color=INK)
                if u is not None:
                    us = f"{u:.3g}" if u < 1000 else f"{u:.1e}".replace("e+0", "e").replace("e+", "e")
                    ax.text(j + 0.5, i + 0.84, f"SPICE use {us}", ha="center", va="center", fontsize=7,
                            color=INK2)
        ax.set_title(title, fontsize=10.5, loc="left", pad=18)
    fig.suptitle("Budget rules on the same sensitivities: unsafe = a spec violated or SPICE use > 1.02 x allowed; "
                 "infeasible = a budget below its library floor; (unverified) = some SPICE runs failed",
                 fontsize=9.5, x=0.01, ha="left", color=INK2)
    fig.tight_layout(rect=(0.04, 0, 1, 0.95))
    fig.savefig(IMG / "v2_budget_rules.png", dpi=160)
    plt.close(fig)


def fig_g20():
    """G2.0 (before layout) against the hand-drawn layouts (drawn devices -> extracted netlist)."""
    panels = [("iadc_ota", "gbw_mhz", "GBW loss (MHz)"), ("iadc_ota", "pm_deg", "PM loss (deg)"),
              ("ttsky25a_fd", "gbw_mhz", "GBW loss (MHz)"), ("ttsky25a_fd", "pm_deg", "PM loss (deg)")]
    fig, axs = plt.subplots(1, 4, figsize=(13.5, 3.8))
    for ax, (d, k, ylab) in zip(axs, panels):
        g = ((snap(d, "after") or {}).get("S2") or {}).get("g20_by_part", {}).get(k) or {}
        ref = json.loads((REPO / "outputs" / "reference_layout" / d / "reference_layout.json").read_text())
        rcf = REPO / "outputs" / "reference_layout" / d / "reference_layout_rc100s.json"
        rc = json.loads(rcf.read_text()) if rcf.exists() else None
        rc_ok = rc and rc.get("post_layout_rc") and not any(
            v.get("numerical_warnings") for kk, v in (rc.get("runs") or {}).items() if kk.startswith("pex_rc"))
        c_hand = (ref.get("lost_to_parasitics") or {}).get(k)
        r_hand = ((rc.get("lost_to_parasitics_rc") or {}).get(k) - c_hand) if rc_ok and c_hand is not None else None
        # capacitance group
        ax.bar(0, g.get("cap_wiring", 0), color=C_BEFORE, width=0.6, edgecolor=SURF, linewidth=2)
        ax.bar(0, g.get("cap_cells", 0), bottom=g.get("cap_wiring", 0), color=C_BLUE_LIGHT, width=0.6,
               edgecolor=SURF, linewidth=2)
        ax.bar(1, c_hand or 0, color=C_AFTER, width=0.6, edgecolor=SURF, linewidth=2)
        # resistance group
        ax.bar(2.6, g.get("r_wiring", 0) + g.get("r_access", 0), color=C_BEFORE, width=0.6, edgecolor=SURF,
               linewidth=2)
        top = max(g.get("cap_wiring", 0) + g.get("cap_cells", 0), c_hand or 0,
                  g.get("r_wiring", 0) + g.get("r_access", 0), r_hand or 0)
        if r_hand is not None:
            ax.bar(3.6, r_hand, color=C_AFTER, width=0.6, edgecolor=SURF, linewidth=2)
            ax.text(3.6, r_hand + top * 0.02, f"{r_hand:.3g}", ha="center", va="bottom", fontsize=8)
        else:
            ax.text(3.6, top * 0.05, "R+C run\nnot trusted\n(gmin\nstepping)", ha="center", va="bottom",
                    fontsize=7.5, color=INK2)
        for x, v in ((0, g.get("cap_wiring", 0) + g.get("cap_cells", 0)), (1, c_hand or 0),
                     (2.6, g.get("r_wiring", 0) + g.get("r_access", 0))):
            ax.text(x, v + top * 0.02, f"{v:.3g}", ha="center", va="bottom", fontsize=8)
        allowed = 0.5 * (g.get("margin") or 0)
        ax.axhline(allowed, color=INK2, linestyle=(0, (4, 3)), linewidth=1)
        ax.text(4.0, allowed, " eta x margin", va="bottom", ha="right", fontsize=7.5, color=INK2)
        ax.set_xticks([0, 1, 2.6, 3.6], ["G2.0\nC", "hand\nC only", "G2.0\nR", "hand\nR part"], fontsize=8)
        ax.set_ylim(0, max(top, allowed) * 1.25)
        ax.set_ylabel(ylab)
        ax.set_title(f"{SHORT[d]}: {k.split('_')[0].upper()}", fontsize=10)
        clean(ax)
    fig.suptitle("G2.0 'after' (S2's prediction before layout; dark blue = routes, light blue = inside the cells) "
                 "against the hand-drawn layouts' measured loss (orange)", fontsize=10.5, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(IMG / "v2_g20_vs_hand_layouts.png", dpi=160)
    plt.close(fig)


def fig_loadbench():
    """LOADBench: S3's relaxed-type fallback, plan v2 'after' against the post-hoc 'least-bad' rule."""
    d = "loadbench_miller"
    lim = spec_limits(d)
    tags = [("before", "before (v1)", C_BEFORE), ("after", "after (v2)", C_AFTER),
            ("after_posthoc_leastbad", "post hoc\nleast-bad", C_POST)]
    rows = [(lab, c, (snap(d, t) or {}).get("S3") or {}) for t, lab, c in tags]
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.4))
    for ax, key, ylab in ((axs[0], "pm_deg", "phase margin (deg)"), (axs[1], "power_uw", "power (µW)"),
                          (axs[2], None, "total device area (µm²)")):
        vals = [(s.get("final") or {}).get(key) if key else s.get("total_device_area_um2") for _, _, s in rows]
        ax.bar(range(3), vals, color=[c for _, c, _ in rows], width=0.6, edgecolor=SURF, linewidth=2)
        for x, v in enumerate(vals):
            ax.text(x, v * 1.02, f"{v:,.1f}" if key else f"{v:,.0f}", ha="center", va="bottom", fontsize=8.5)
        if key in lim and lim[key][1] is not None:
            ax.axhline(lim[key][1], color=ST_CRIT, linestyle=(0, (4, 3)), linewidth=1.2)
            ax.text(1.0, lim[key][1] + 0.01 * max(vals), ("spec ≥ " if lim[key][0] == "min" else "spec ≤ ")
                    + f"{lim[key][1]:g}", ha="center", va="bottom", fontsize=8, color=INK,
                    bbox=dict(facecolor=SURF, edgecolor="none", pad=1))
        ax.set_xticks(range(3), [lab for lab, _, _ in rows], fontsize=8.5)
        ax.set_ylabel(ylab)
        ax.set_ylim(0, max(vals + [lim.get(key, (None, 0))[1] or 0]) * 1.2)
        clean(ax)
    fig.suptitle("LOADBench Miller: all 6 device types relaxed in v2; the relaxed-type fallback decides the result",
                 fontsize=10.5, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(IMG / "v2_loadbench_fallback.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    for f in (fig_gates, fig_s3, fig_rules, fig_g20, fig_loadbench):
        f()
        print("wrote", f.__name__)
