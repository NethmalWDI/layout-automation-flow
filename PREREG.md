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
