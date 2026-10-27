<!-- Copy of the claude.ai project doc `claude/13_plan_v2_results_and_review.md` (project "Layout automation"), written 2026-10-27 by Cowork. The project copy is the original. -->

# 13. Plan v2: results, review C and where the flow stands (2026-10-27)

This is a durable summary of plan v2. The full record is flow record section 7 (`docs/flow_record.md`; source
`docs/flow_record_section7_draft.md`). Every number comes from `outputs/compare/<design>/<tag>.json` or from the run
outputs named in section 7.

## What plan v2 did

- **Designs:** five, in two groups.
  - Development: `example_ota_5t` and `ota5t_stress`.
  - Held out: `loadbench_miller`, `iadc_ota` (with a hand layout) and `ttsky25a_fd` (Imasha's taped-out tile).
- **Runs:** every design ran 'before' (v1, the old flow) and 'after' (v2).
- **What v2 changed:**
  - 45 PVT points and a 200-run Monte Carlo in S0;
  - in S2, library floors (G2.7), the R19 fix, one constraint per PVT point and five budget rules scored in SPICE;
  - S3 option modes.
- **Extra runs:** a no-PVT ablation (the two 5T designs), S2 at eta 0.9 for all five (the PREREG headline), and
  hand-layout comparisons against G2.0.

## Results in one table ('after', v2)

| Design | S2 | S3 | Final specs |
|---|---|---|---|
| example_ota_5t | PASS | PASS; area 187 → 237 um2 | met |
| ota5t_stress | G2.7 FAIL (binding: GBW at ss, 1.1 V, 85 C, margin 7.8 MHz) | 3 types relaxed; area 207 → 257 um2 | met |
| loadbench_miller | G2.7, G2.3 FAIL (binding: gain at sf, 0.9 V, −40 C, margin 0.014 dB) | all 6 relaxed; area 4396 um2 | **PM 48.1 deg (spec >= 60)**; post-hoc least-bad 64.7 deg |
| iadc_ota | G2.7 FAIL (binding: PM at ss, 0.9 V, −40 C, margin 0.26 deg) | 22/22 relaxed: an artefact of S3's saturation check (row 41) | met |
| ttsky25a_fd | G2.7 FAIL (one corner: gain at ff, 1.0 V, 27 C, margin 0.093 dB) | 10/22 relaxed | met |

## Budget rules and hypotheses

- **Per-net budgets are unsafe on every design:** 1.7 to 65 x the allowance in SPICE.
- **Held-out designs:** every rule is infeasible, because the cheapest cells already exceed the allowance.
  - Equal split matches or beats ours on every pre-registered outcome.
  - Ours is "safe, feasible, with room" on the 5T only. There the LP with floors is also safe and feasible, with
    zero room.
- **H1:** not supported in full. There are 3 exceedances in 8 design–eta pairs:
  - TTSKY25a at 1.035;
  - LOADBench at 1.008, one resolution step on a 0.014 dB margin;
  - stress at 1.11, which is not reproduced by the previous day's 0.98.
- **H1b:** the first half holds, as expected by construction. The second half fails on TTSKY25a. The per-net rule
  is our re-implementation, not the authors' code.
- **H1c:** holds, but is uninformative here, because the floors exceed the allowance.
- **The PREREG headline at eta 0.9 is missing TTSKY25a.** Its S2 crashed (`OSError [Errno 22]` on the mounted
  folder), and the snapshot mixed two runs (row 40). Not re-run yet.
- **The 5T and LOADBench eta 0.9 runs** were repeated with the PC awake: identical.

## G2.0 against the hand layouts

- **iadc (same circuit):** none of the four comparable numbers is within PREREG's 25 % (they are off by 1.35 to 7 x).
- **TTSKY25a tile (a later circuit):** PM is 21 % high and GBW 2.2 x low.
- **TTSKY25a tile R+C run:** not trusted (gmin stepping).
- **G2.0's route part** still uses the as-sized PCell geometry (row 44).

## Decisions of 2026-10-27 (Imasha)

- The S3 gate-pad met1.6 patch (row 37).
- The lane A side run.
- LOADBench 'after' is kept. The post-hoc 'least-bad' test was run and adopted as the S3 default for future runs
  (PREREG amendment); plan v2's results keep the old rule.
- The eta 0.9 re-run with the PC awake.

## Review C (independent, 2026-10-27): 14 findings

All were checked against the files.

**Corrected in the write-up:**

- equal split vs ours;
- the hypothesis reading;
- the G2.0 like-for-like comparison;
- the 5T gate-R story;
- the number errors.

**Open (technical, waiting for Imasha):**

- the S3 saturation defect (row 41);
- the 5T binding corner contradicted by SPICE (row 42);
- stale files in variant runs (row 43);
- G2.0 route geometry (row 44);
- the fairness of the LP-with-floors bound;
- the near-zero-margin corners;
- the phase-2 wall-clock cap;
- the stress drift, which lies in the PVT-point inputs and not in the cell cache.

## Assessment

**What works:**

- S0/S1 generalise to five designs (model vs SPICE within 0.09 dB, 2.8 %, 0.2 deg).
- S2 now reports misfit before layout, with the binding corner.
- Per-net budgets are shown unsafe in SPICE.

**What does not work yet:**

- On real circuits the joint budgets are infeasible and no better than equal split.
- The verdicts hinge on corners with near-zero margin.
- S3 says little: one defect, one fallback rule decided post hoc.
- G2.0 is not calibrated.
- Infrastructure (standby, stale files, a crash snapped as a result) caused several problems.

**Before S4:**

1. Fix the defects and re-run.
2. Decide and pre-register how near-zero-margin corners count.
3. Re-score the baselines fairly.
4. Give S3 options that can lower the floors.
5. Test G2.0 on the flow's own layouts (S5–S7).
