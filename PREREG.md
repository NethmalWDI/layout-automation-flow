# Pre-registration (DRAFT, not yet frozen)

This file is committed and tagged (`prereg-v1`) **before** any baseline is run on the held-out circuits.
After the tag, changes are allowed only as dated amendments at the end, with the reason.

## Hypotheses

- **H1 (soundness).** Inserting all of a method's budgets together at their full value uses at most
  eta × margin of every spec, at every PVT corner where the schematic meets the spec.
- **H1b (per-net vs joint).** Per-net injection budgets (baseline A3, run with the authors' code)
  violate H1 on at least one spec for at least 2 of the 3 benchmark circuits; joint budgets do not.
- **H1c (feasibility).** The equal-split baseline gives at least one critical element a budget below
  the parasitics of the default device cells (infeasible) on at least 2 of 3 circuits.
- **H2 (pre-screening).** The S4a planner's predicted ranking of block variants agrees with the
  realized (extracted + simulated) ranking with Kendall tau >= 0.7, top-3 recall >= 2/3, and zero
  false accepts.
- **H3 (device decomposition).** At equal verified margin, S4a in mode A-bin gives smaller block area
  than the rule-of-thumb folding baseline; the model change stays below 10 % of eta × margin.
- **G2.0 validity.** G2.0 (fraction of the margin a compact layout would use) predicts the
  post-layout margin used within 25 % (relative) on every circuit once S5–S7 exist.

## Metrics, thresholds, circuits

- Circuits: example_ota_5t (development), ota5t_stress (development), loadbench_miller,
  iadc_ota, ttsky25a_fd (held out: the rules and constants are frozen before they are run).
  Note (honest record): loadbench_miller and ttsky25a_fd were already run once on 2026-10-26 with the v1 flow,
  to measure the "before" state; the v2 rules below were written before their v2 ("after") runs.
- Corners: tt/ss/ff/sf/fs x VDD +-10 % x {-40, 27, 85} C.
- eta sweep: 0.3, 0.5, 0.7, 0.9, 1.0. Headline numbers are reported at eta = 0.9 and at the sweep.
- Every method gets the same SPICE/PEX budget; counts and wall time are logged.

## Frozen constants (set 2026-10-26, before the v2 runs)

- Rule-of-thumb target finger width: 4.0 um (`src/s3/options.py`, RULE_OF_THUMB_WF); nf = the grid value
  nearest W / 4 um, default contacts and coverage.
- nf grid: 1, 2, 4, 8; plus 16, 32, 64 only when the finger stays >= 7 um (the lower W edge of the wide
  SKY130 bins).
- S2 phase-2 floor rule (R19 fix): an element is never trimmed below min(phase-1 budget, expected need),
  nor below its library floor (the least any library cell puts on it).
- S3 resistance allowance v2: a cell may use max(its share of the budget, the library's lowest access R of
  that terminal), never more than the budget.
- Model-change cap: 10 % of eta × margin per spec (to be applied in S4a).
- PVT: 5 corners x VDD x {0.9, 1.0, 1.1} x {-40, 27, 85} C = 45 points; Monte Carlo: 200 runs of tt_mm.

## Amendments

- **2026-10-26, after the first v2 runs of the two development designs (5T), before any v2 run of the
  held-out designs.** Following an independent review (flow record 7.7, review B): (1) a SPICE run that fails
  (timeout, no DC solution, numerical warnings) is a failed run, never a violation; (2) a fifth budget rule,
  `lp_floor` (the LP with the library floors and budgets capped at need), is added next to the plain LP,
  which is kept; (3) every method's own most-used PVT points are checked in SPICE (one common set);
  (4) outcomes are defined as: unsafe = a spec violated in SPICE or use / (eta x margin) > 1.02; infeasible =
  some budget below its library floor; ok = neither. H1b and H1c are read with these definitions. The
  development designs were re-run with them; their first numbers are kept in the flow record as superseded.
- **2026-10-26, ttsky25a_fd specs.** At the designer's request the specs are the schematic's own simulated
  performance (gain -1 dB, GBW x 0.9, power x 1.1, PM >= 60 deg), the same rule as loadbench_miller, set
  before its v2 run.
- **2026-10-26, eta of the SPICE-scored comparison.** The SPICE-scored baseline comparison (G2.8) runs at each
  design's own eta (0.5 unless the package sets it; ota5t_stress 0.9), not at 0.9 as written above; the
  eta sweep (first order) covers 0.3 to 1.0 for every design. A SPICE-scored run at eta = 0.9 for every design
  is still to do.
- **2026-10-27, after all plan-v2 runs: the S3 rule for relaxed device types (decided post hoc).**
  - When no option of a device type stays within its allowance, S3 still keeps one and flags the type (G3.5).
    It now keeps the option whose worst check, the access R of d, g and s included, is broken least
    (`--relax-fallback least-bad`, the largest min_slack). Until now it kept the default PCell, the device as
    sized, when that cell was built (`--relax-fallback default`).
  - Reason: in plan v2's LOADBench 'after' run all six types were relaxed. The old rule drew the 484 um and 887 um
    devices as single fingers with 8.2 and 4.9 kohm of gate resistance, and PM fell to 48.1 deg (spec >= 60).
  - On the same inputs the least-bad rule gave 64.7 deg and half the device area. ota5t_stress improved
    slightly, and iadc_ota and ttsky25a_fd did not change.
  - This was decided after seeing plan v2's results, so it is not part of plan v2. Every plan-v2 result
    ('before', 'after', the no-PVT ablation, eta 0.9 and its re-run) used the old rule and stands as recorded.
    The least-bad results for plan v2 are reported only as post hoc (snapshot tag 'after_posthoc_leastbad';
    flow record 7.1, row 38).
  - Runs from now on use least-bad. The v1 variant, plan v2's scripts and golden re-runs of plan-v2 snapshots
    keep the old rule, and `--relax-fallback default` reproduces plan v2's S3.
- **2026-11-01, Plan v3 Phase A (5T and LOADBench), written before any Phase A code change or run.**
  - **Context.** This file was tagged `prereg-v1` on 2026-11-01, on commit `a8c6f7d3`, after plan v2's runs. The
    "DRAFT" heading above predates the tag. This amendment is the first dated change on top of the tag. The plan is
    `docs/plan_v3_phaseA.md`, and decisions D-a to D-f in it are Imasha's (2026-11-01).
  - **Scope (D-a).** `example_ota_5t` and `loadbench_miller` only. `ota5t_stress`, `iadc_ota` and `ttsky25a_fd`
    are frozen: their outputs, snapshots and golden files stay as they are, the rules below must leave them
    running, and their plan-v2 results stand as recorded.
  - **1. Budgets use nominal constraints only (D-b).** For the two designs (package key `budget_corners:
    nominal`), S2 allocates with the nominal constraints only. S0 still simulates the 45 PVT points. In G2.9, S2
    reports first-order use at each point, as a fraction of eta × that point's margin, plus the worst point and the
    points where a spec was not met before layout. This is reported, not gated. Designs without the key keep the
    plan-v2 behaviour, where all 45 points constrain the budgets.
  - **2. Allowance = share of nominal margin, eta = 0.5 (D-c).** For each spec at nominal, allowance = 0.5 ×
    (achieved − spec). This is S2's default (`ETA_DEFAULT`), so the packages need no `eta` key. The eta sweep
    (0.3–1.0) stays as a report. Phase A's runs use eta = 0.5; the plan-v2 SPICE-scored comparison at eta = 0.9 is
    not repeated in Phase A.
  - **3. One tolerance, `TOL_USE` = 0.02 of the allowed use, eta × margin (Q3).** It has one definition and is used
    by G2.5, `outcome()` and S3.
    - G2.5's gate moves from 10 % (`TOL_VERIFY`) to 2 %. The 10 % figure stays only as a reported column, "within
      first-order model error", not as a gate. More G2.5 checks may then fail.
    - S3's tolerance, 1 % of the margin until now (`TOL`), becomes `TOL_USE` × eta × margin: the same 1 % at
      eta = 0.5.
    - `outcome()`'s "unsafe" threshold, use / (eta × margin) > 1.02 (amendment of 2026-10-26), is this same
      tolerance.
  - **4. S3 saturation check: do no harm below vdsat.**
    - For a device already below vdsat in the schematic (its schematic vds − vdsat ≤ 0), S3's check becomes "do no
      harm": an option may lower that value by at most `TOL_USE` × |schematic value|.
    - Its slack is measured against |schematic value|, and the check is marked as this rule.
    - Saturated devices keep the plan-v2 rule.
    - ASSUMPTION: the further-drop tolerance, `TOL_USE` × |vds − vdsat|, comes from no upstream source.
  - **5. `lp_floor_k`.** The `lp_floor` baseline is also scored with the upper bound ours uses, KAPPA × need
    (KAPPA = 10, `src/s2/budgets.py`), as `lp_floor_k`. The plan-v2 `lp_floor`, capped at need, is kept, and both
    are reported.
  - **6. G2.0's route part uses the representative cells.**
    - Route lengths use the half-perimeter of the bounding box of the representative S3 cell of the device's type,
      instead of S0's as-sized PCell.
    - A type with no representative cell falls back to the as-sized PCell and is listed as such.
    - m > 1 is scaled as S3 does (ASSUMPTION; both designs have m = 1 everywhere). The as-sized value stays as a
      second column.
    - G2.0 is information only, so no budget changes.
  - **7. The PM reference phase is rounded to the nearest 180°.** PM = 180 + (phase at the unity-gain frequency −
    reference), where the reference is the 1 Hz phase rounded to the nearest multiple of 180°.
    - This applies in the S1 linear model and in the bench template for new designs.
    - The frozen testbenches of the two designs are not changed. Their 1 Hz phase's distance from the nearest
      multiple of 180° is measured and recorded; it is expected below 0.01°.
  - **8. Designer groups (D-e) and the mirror-bank rule.**
    - Mirror blocks of the same polarity whose devices share the gate net and the source net, with at least one
      diode-connected, are merged into one mirror bank, ratioed by W × m to the diode device.
    - LOADBench's designer groups (Imasha's review, 2026-11-01) are read from
      `inputs/loadbench_miller/designer_groups.yaml`, outside the hash-frozen folders:
      - P2, P8 and P5 form one PMOS mirror bank;
      - the input pair P6/P7;
      - the NMOS mirror load N1/N4;
      - the CS stage, N3 with P5 as its load: a functional group with no N3–P5 matching.
    - Where the designer's groups and the automatic blocks disagree, the designer's groups win, and the agreement
      is reported.
    - The floorplan rows are recorded for S4 and not used in S0–S3.
    - LOADBench's PMOS bank keeps its sizes (D-d): W = 37.3, 90.63 and 887.03 µm at L = 0.74 µm, ratio
      1 : 2.43 : 23.8.
  - **Unchanged:**
    - S3's relaxed-type fallback stays `least-bad` (amendment of 2026-10-27).
    - The nf grid, the representative-cell floors and the frozen constants stay as they are.
    - No LLM runs inside the flow (D-f).
  - **Changes that alter no rule or constant** (plan steps 2, 5a, 9 and 10):
    - run hygiene: exit codes, clean output folders, the snapshot identity check;
    - the dummy-aware S1 tagger;
    - the SPICE vs first-order report;
    - LOADBench's hand model, labelled PREDICTED (patched, post hoc) and report-only.
  - **9. Predictions, written before the runs.** Section 4 of the plan, copied unchanged below. "Expected" means a
    prediction, not a result. Every prediction that fails gets one line of explanation, and no rule is changed to
    make a prediction come true.

  | Step | example_ota_5t | loadbench_miller |
  |---|---|---|
  | 2 hygiene | no number changes | no number changes |
  | 3 nominal budgets | allocation identical to the `after_nopvt` snapshot (t_round1 3.401, 21 elements, min ratio to need 3.23; regression check) | budgets larger than plan-v2 'after' (no longer starved at the PVT points). The PVT use table shows points above 1.0 (reported, not gated) |
  | 4 S3 do-no-harm | no change if every functional device is saturated (check G1.1) | same |
  | 5 grouping | blocks unchanged | one bank {P2, P8, P5}, consistent in G1.4; the CS stage is not matched; designer file and automatic rule agree |
  | 6 tolerance, lp_floor_k | G2.5 may report more checks over 1.02. Outcome words for ours unchanged at eta 0.5; lp_floor_k gets more room than lp_floor | same |
  | 7 PM reference | about 2e-5° (pole at about 2.7 MHz) | about 2e-3° (pole at about 29 kHz) |
  | 8 G2.0 route | small change | route part of G2.0 drops a lot (no 484 and 887 µm single fingers) |
  | 9 model agreement | the row-42 corner appears in the PVT report, no longer binding | listed checks, if any |
  | 10 hand model | — | hand PM gap falls from about 17° to a few degrees (G1.5, report only) |
  | 12 S3 and SPICE | area and relaxed types close to `after_nopvt` | fewer relaxed types than plan-v2 'after' (all 6 were relaxed). PM after S3 at or above plan-v2 post hoc 64.7° |

- **2026-11-01, Plan v3 Phase A step 8: G2.0's route part is part of the expected need (Imasha's decision (b),
  before any step 8 run).**
  - Item 6 assumed G2.0 is information only and said "no budget changes". In the code, the route lengths are the
    wiring part of every element's expected need. G2.0 is rate × that need, and the allocation shares the margin
    in units of the same need.
  - Imasha chose (b): the representative cells' route lengths set the need everywhere, for G2.0 and the
    allocation, as the cell part already did in plan v2. 'Ours' budgets therefore change, and so do the scores of
    the other budget rules, which share the need. The alternative was to change G2.0 only and keep the as-sized
    need in the allocation.
  - G2.0 keeps the as-sized route as a second column (`fraction_of_margin_route_as_sized_pcell`).
  - Item 6's other points, and the step 8 predictions in item 9, are unchanged.
