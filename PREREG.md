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

- **2026-11-02, Plan v3 Phase A step 12: budgets at a bound (decided post hoc, after the step 12 results).**
  - **What was wrong.** G2.8's score counted "below floor" and "starved" when a budget was below floor or need ×
    (1 − 10⁻⁹). Phase 2 of the allocation (`budgets.refine`) leaves a pinned budget exactly that much room, xm ×
    (1 − 10⁻⁹). So a budget at its floor fell above or below the test by rounding.
  - **The change.** The tolerance is now 10⁻⁶ (`AT_BOUND_TOL` in `src/s2/baselines.py`), and the snapshots' starved
    count uses the same. The definitions of "infeasible" (a budget below the library floor) and "starved" (a budget
    below the expected need) are otherwise unchanged.
  - **Effect.** It changes one reported word, ours on LOADBench: "infeasible" at 10⁻⁹, "ok" at 10⁻⁶ (SPICE 1.007
    of allowed). Both are reported (flow record 7.13, row 60). No budget changes.
  - **Decision.** Imasha's, 2026-11-02. It was made after the step 12 results were seen, so it is post hoc.

- **2026-11-02, after review D (finding 1): G2.8 SPICE-checks PVT points again (decided after the Phase A results).**
  - **Why.** With `budget_corners: nominal`, S2's constraints are nominal only, so G2.8 simulated no PVT point. Its
    outcome words, and H1 (defined at every PVT corner where the schematic meets the spec), covered the nominal
    corner only. Plan v2's G2.8 also checked each rule's most-used PVT points (amendment of 2026-10-26, item 3).
  - **The change.**
    - G2.8 again SPICE-checks each rule's 5 most-used PVT points (first order, one common set), drawn from G2.9's
      PVT constraints.
    - The outcome word covers every simulated check, as in plan v2, and `outcome_nominal` gives the word from the
      nominal checks alone.
    - The PVT points are scored, not budgeted. G2.5, the gate on S2's own budgets, stays nominal, because its
      closure step would otherwise change the budgets.
  - **Decision.** Imasha's, 2026-11-02, choosing this over declaring G2.8 nominal-only. It was made after the
    Phase A results were seen.

- **2026-11-03, plan v4: S3 without guard rings and the new stages S4–S7, written before any S3 change or S4–S7
  code or run** (`docs/plan_v4_S4_S7.md`; branch `s4-s5` from tag `s0s3-reviewed`).
  - **S3 change (Imasha's decision).** S3's unit cells are drawn without a guard ring (`guard 0`); S4 draws one ring
    per block. S3's choice rule, modes, tolerance (`TOL_USE`) and the relaxed-type rule are unchanged.
    - Predicted: every chosen cell gets smaller, and the circuit with every chosen cell still meets every spec in
      SPICE (G3.3) on both designs.
    - The relaxed types may change; whatever they are is reported against the reviewed S3, not tuned.
  - **Gates** as listed in the plan, section 5 (G4.1–G4.6, G5.1–G5.5, G6.1–G6.3, G7.1–G7.4). The latch-up gate uses
    S2's `place.latchup_tap_distance` (15 µm). G7.2 uses the existing `TOL_USE` (0.02 of eta × margin).
  - **H4 (layout within budgets).** On the 5T, a layout that passes G6.2 (every extracted C, coupling and R within its
    S2 budget) also passes G7.1 and G7.2 at the nominal corner. A failure of G7.2 with G6.2 passing refutes H4.
  - **H5 (budgets in the placement cost).** The budget-aware placement cost gives a layout whose G6.2 violations are
    no more than those of the area-only cost, on both designs, at no more than 25 % more area. Reported per design.
  - **G2.0 validity** (hypothesis of 2026-10-26) is evaluated on these two designs: the post-layout use of each spec's
    margin (S7) against G2.0's prediction, within 25 % relative.
  - **Predictions per design.**
    - 5T: G6.2, G7.1 and G7.2 pass (G2.0 shares at most 0.13; every budget ≥ 3.73 × its expected need).
    - LOADBench: G7.2 fails on gain_db (G2.0 = 0.999 at eta 0.5, 29 of 40 budgets below need). That is a finding about
      its specs, reported as such.
  - **Constants still to fix** before the first S5 run, in a further amendment: routing layers and grid pitch, λ in
    the placement cost, and the area-only baseline's exact definition.

- **2026-11-03 (late evening), plan v4: S5's constants, fixed before any S5 code or run** (as the amendment above
  required).
  - **Placement.** Rows by device type: PMOS rows above NMOS rows. A package's designer rows are used when it has
    them. Rows are stacked 3.0 µm apart, and blocks in a row stand 3.0 µm apart (bounding boxes). A row with one
    symmetric block (a matched pair or mirror) puts that block's own axis at x = 0; a row without one is centred on
    x = 0; a row with two symmetric blocks is not allowed. Every row partition and order, every block variant and
    a vertical flip of every block are enumerated (up to 50 000 candidates; simulated annealing over a sequence pair
    beyond that, not needed for the 5T or LOADBench).
  - **Wire estimate.** Per net, the half-perimeter of the box around its pins; a block's track counts as a
    horizontal segment and a ring's body pin as a point of its body net.
  - **Budget-aware cost** = A / A_ref + λ Σ_n max(0, u_n − 1) + μ Σ_n u_n, with λ = 10 and μ = 1.
    - A is the placement's bounding-box area; A_ref is the sum, over the blocks, of their smallest variant's area.
    - u_n is net n's estimated length over S2's `route.max_length.<n>.metal3`, for every net that has one.
  - **Area-only baseline** (AICL-like, connectivity-agnostic): cost = A / A_ref; ties go to the first candidate in
    enumeration order.
  - **Routing (Phase 4):**
    - Top-level wires on metal3 (horizontal, outside the block footprints only) and metal4 (vertical, also over
      blocks, which have no metal4), joined by via3.
    - Width 0.4 µm on a 0.8 µm grid. Nets go in order of least budget slack first.
    - A ring's body pin is joined to its body net. Supply nets get the same width: EM is not evaluated, as in S2.
  - **H5** is read with these definitions: G6.2 violations and area, for the budget-aware and the area-only
    placements, each routed by the same router.

- **2026-11-04 (morning), plan v4 Phase 8 (`docs/plan_v5_ttsky25a.md`): S3–S7 on `ttsky25a_fd`, fixed before any
  Phase 8 code or run.** Imasha's decisions of 2026-11-04 (plan, section 0).
  - **Inputs.** The flow's DUT stays the schematic (`Opamp_with_bias`), specs as now (0.9 × the schematic,
    ASSUMPTION). S0–S3 are re-run with today's code before S4 (S3 with ringless cells); their verdicts are reported,
    not tuned.
  - **Hierarchy.** The design's own (`circuits/ttsky25a_fd/upstream/hierarchy.json`): `top`, `x1`, `x2`, and the two
    res_packs. Each is placed and routed as a macro; the five macros are then placed and routed. No designer
    floorplan: the code arranges the macros (Imasha).
  - **Matching and dummies** (package option, `ttsky25a_fd` only; the 5T's and LOADBench's blocks unchanged): matched
    transistor groups only as common centroid (ABBA) or interdigitated variants (AB not offered); groups of three or
    more, or of unequal m, in one row whose sequence keeps every device's centroid on the row's centre; the two
    res_packs in one block interleaved A B B A; one dummy unit at each end of every matched row, its terminals on the
    body net (resistor dummies on ground, ASSUMPTION), counted in LVS and in the extraction like any device.
  - **Search inside a macro.** Exhaustive enumeration up to 6 blocks (as now); beyond that, simulated annealing over
    row placements: seed 20261104; 40 000 moves per cost; moves (each equally likely): swap two blocks, move a block
    to another row, change a block's variant, flip a block (symmetric pairs move together); start temperature 0.05 ×
    the starting placement's cost, multiplied by 0.9998 after every move; the starting placement is the blocks in S0's
    order, PMOS rows above NMOS rows. The best placement seen is kept. Both costs (λ = 10, μ = 1, unchanged) run with
    the same seed.
  - **One symmetry axis.** Every P/N pair of the fully differential amplifier (blocks and macros) is mirrored about
    one vertical axis.
  - **Hard outline (G5.6).** The layout's bounding box at most 250 µm wide and 200 µm tall (Imasha; orientation
    ASSUMPTION). A placement outside it is rejected, never traded against wire length; if none fits, G5.6 fails with
    the smallest box found.
  - **Grid router** (where the spine router does not apply): metal3 horizontal, metal4 vertical, 0.4 µm wide on a
    0.8 µm grid; A* per net with cost = length + 2 µm per via; nets in order of least budget slack; a mirrored pair
    routed as mirror images; keep-outs as now.
  - **Predictions** (before any Phase 8 run): S2 still fails G2.7 at some PVT points (as on 2026-10-27); G6.2 fails
    (budgets below what a compact layout needs); the budget-aware layout has no more G6.2 violations than the
    area-only one (H5); the wiring loss drawn → R+C of GBW, as a share of margin, is below the hand layout's (51 %,
    C-only) — a prediction about this flow's compactness, reported either way.

- **2026-11-04 (10:03 CET), plan v4 Phase 8: two changes to S5's placement for `ttsky25a_fd`, after a dry run of the
  placement alone** (no layout drawn, nothing simulated; `runs/tmp/p8_place.py`). With one matched block per row and one
  shape per macro, the four macros (x1, x2, top, res_packs) came out 133 × 150, 133 × 62, 78 × 124 and 50 × 55 µm under
  the budget-aware cost, and no arrangement fit Imasha's hard outline of 250 × 200 µm.
  - **Shared rows inside a macro.** A row inside a macro may hold several matched blocks; such a row is centred, and
    each pair keeps its own symmetry (common centroid or mirror image inside its block) but not a shared axis. The
    outline is Imasha's hard constraint; the shared axis was this plan's own rule. Axes are reported, not gated.
  - **Three shapes per macro.** Each macro is placed (seed and schedule as above) under a width limit of 100 %, 65 %
    and 50 % of the outline's width (height: the outline's); the top level enumerates the macros' distinct shapes
    with every arrangement and keeps the best that fits. Same for both costs.
  - The predictions above stand.

- **2026-11-05 (10:10 CET), layout rule set v2 (`docs/rules_v2/ruleset_v2.md`, reviewed and answered by Imasha the
  same day), written before any v2 code or run.** v2 is opt-in per design (`ruleset: v2` in `inputs/<d>/layout.yaml`);
  every design without it runs v1 unchanged (the goldens must still match). First design: `iadc_ota_v2`, a GUI copy of
  `iadc_ota` (and a second copy once Imasha's hand-drawn hierarchy arrives).
  - **Spacing.** Every spacing and enclosure the generator chooses is the SKY130 Magic-deck minimum × 1.10, rounded up
    to 0.05 µm (Imasha, Q9, reading (a)); widths stay at the minimum or the current-based width; the latch-up limits
    keep `TAP_MARGIN` 0.5 µm. The unit cells' own geometry and S4's stub planner (already at the DRC minimum and signed
    off by DRC) are unchanged.
  - **Routing (R1, R2).** No wire of any net over a block's device area (metal3 and metal4), capacitors as before;
    channels between blocks and rows are as wide as routing needs: S5 tries the narrowest gap first and widens the
    gaps one router grid (0.8 µm) at a time until every net routes (phase 1: one width for all gaps).
  - **Patterns (M1-M9, phase 2).** Per matched group the patterns its matching level allows (1-D ABBA/ABAB, the
    cross-quad, 2-D common centroid with A/B swapped rows, clustered); a rough estimate (outline, internal wire length
    against S2's budgets, crossings) keeps a Pareto set of 2-3 per group, always including the best of the strictest
    pattern the level asks for; only those are signed off in S4; S5 chooses by its cost as before. If a survivor's
    signed-off area differs from its estimate by more than 15 % (ASSUMPTION), a third candidate is added.
  - **Rings (phase 3).** One ring per stack, shared edges between neighbouring stacks of one body net, one outer ring
    round the amplifier (Imasha, Q3); normal ring widths (Q10).
  - **Unchanged.** S0-S3, S2's budgets, every gate and negative control, S6/S7, the search settings (seed, moves,
    schedule, lambda, mu, shapes).
  - **Hypotheses.** H-v2a: with a hand layout to compare, the v2 layout's area is at most 1.3 × the hand layout's
    (target 1.2 ×; Imasha, Q7) with every spec met after layout; for `iadc_ota` both the raw ratio and the ratio
    against the hand area without its switched-capacitor CMFB (which the flow does not lay out) are reported.
    H-v2b: no-routing-over-devices does not raise the wiring's share of the GBW loss above v1's (12.0 %, C-only).
    Reported either way.

