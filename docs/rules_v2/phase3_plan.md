# Rule set v2, phase 3: plan (on hold from 2026-11-06)

Phases 1–2 of rule set v2 are built and run; see `ruleset_v2.md` sections 3 and 7, PREREG 2026-11-05, and flow record
section 7.26. On `iadc_ota_v2` they gave:
- budget-aware: 22,142 µm²;
- area-only: 17,901 µm²;
- that is 1.34–1.66 × the hand layout, or 1.77–2.19 × it without its CMFB, against a target of 1.3 ×;
- the wiring takes 13.7 % of GBW, against v1's 12.0 %.

Phase 3 attacks the remaining area. Work was put on hold here by Imasha (token budget). Nothing below is coded yet.

**Write a PREREG amendment before any phase 3 run.**

## Where the area goes (iadc_ota_v2, area-only)

| Level | Area | Overhead |
|---|---|---|
| The 19 blocks themselves (smallest signed-off variants) | 10,658 µm² | – |
| The three macros (x1, x2, top) as placed | 13,947 µm² | +31 % (channels, arrangement inside a macro) |
| The whole layout (macros stacked in a column, the capacitors in a row of their own) | 17,901 µm² | +28 % |

## Step 1: macro packing (largest gain expected)

A dry run (placement only, nothing drawn) compares five ways of packing at a 1.6 µm channel:
- **V0:** today's method;
- **V1:** more macro widths (1.0, 0.8, 0.65, 0.5, 0.4, 0.3 × the outline, so macros can sit side by side);
- **V2:** the top-level capacitors and rail dummies placed inside x2;
- **V3:** V1 and V2 together;
- **V4:** flat, all 19 blocks annealed as one macro.

Files:
- script: `runs/tmp/books/p3_dry.py` (git-ignored; copy it to `scripts/` if it is kept);
- log: `runs/logs/p3_dry.log`;
- results: `runs/tmp/books/p3_dry.json`.

Results (finished 2026-11-05, 19:30 CET; placement only, not routed):

| Variant | Area-only | Budget-aware |
|---|---|---|
| V0 now | 84.7 × 211.2 = 17,901 µm² | 160.2 × 150.7 = 24,134 µm² |
| V1 more shapes | 17,901 µm² | 128.9 × 190.2 = 24,529 µm² |
| V2 top into x2 | 126.5 × 127.1 = 16,077 µm² (−10 %) | 144.2 × 180.6 = 26,040 µm² |
| V3 both | 16,077 µm² | 144.2 × 165.8 = 23,909 µm² |
| **V4 flat** | **80.4 × 181.6 = 14,594 µm² (−18 %)** | 132.6 × 183.4 = 24,317 µm² |

**Area-only:** V4 (flat) gives 1.09 × the whole hand layout and 1.45 × it without its CMFB.

**Budget-aware:** the layout hardly moves (23.9–26.0 k µm²). Its wire-budget term outweighs the area term, as on v1
(flow record row 99), so packing alone will not shrink it. The budget-aware cost's balance (λ, μ, or budgets that a
compact layout can meet) is its own question for Imasha.

**Step 1 run (2026-11-06, `packing: flat` on iadc_ota_v2; PREREG amendment of that date):**
- **Area-only:** 79.6 × 175.8 = 13,983 µm² (1.05 × the hand layout, 1.39 × it without its CMFB), routed with a 0.8 µm channel. It has **8 DRC errors** (nwell.2a): same-body PMOS blocks 0.8 µm apart.
  - Fixed in `src/common/ruleset.py`: n-wells touch or keep nwell.2a's reserve, 1.40 µm (flow record row 107; test).
  - **Re-run needed** (about 1.5 h): `docker exec -d layout-s0s3 bash -lc "cd /foss/designs && source scripts/env.sh && python3 -u -m src.flow run iadc_ota_v2 --from S5 > runs/logs/gui_iadc_ota_v2_S5S7.log 2>&1"`, then `python3 scripts/make_design_report.py iadc_ota_v2` and `python3 scripts/make_readme_figures.py`.
- **Budget-aware:** flat is worse (29,442 µm², DRC 0, LVS match), so keep sub-circuit macros for it. That means making `packing: flat` apply to the area-only cost alone, or tuning the budget-aware cost.

**Originally next:** route V4 and V2 at their channel widths. A flat placement loses the sub-circuit grouping, so check that the
matched pairs and the routing still behave. Then implement the winner:
- `src/s5/macro.py`: `SHAPES` and `macro_of`, or a flat mode;
- switched on only under `ruleset: v2` (see `src/common/ruleset.py`), so v1 stays unchanged.

## Step 2: channels only where routing needs them (R2, refined)

Today S5 adds one channel width to every gap and re-anneals the whole placement for each width
(`src/s5/run.py`, the `v2` branch in `main`; `RS.CHANNEL`). Instead:

1. **Keep the arrangement S5 found:** each macro's rows and each block's variant and flip; the top level's macro
   rows and shapes. Add a function that re-runs `place.realise` on that arrangement with per-pair extra gaps
   (`extra[(a, b)]`), with no new search.
2. **Route** (`src/s5/grid.py`). For each failed net, widen by one router grid (0.8 µm) every gap inside the box of
   its pins, re-space, and route again.
3. **Repeat** until every net routes, or for at most 20 rounds. If it never converges, fall back to today's
   uniform channel.

Gaps that never need a channel stay at their DRC minimum. Same-body blocks then abut, which step 3 needs.

## Step 3: one ring per stack, shared edges, and the outer ring (T1, T4)

- **Shared edges:** where two same-body blocks abut with no channel, overlap their rings so the centre lines
  coincide. The gap is −2 × (bbox margin to the ring centre): −0.42 µm for NMOS, −0.60 µm for PMOS.
  - Tracks must then stop short of the ring: `EXT` = −(met3.2 reserve / 2 + track width / 2). Otherwise two blocks'
    tracks meet end to end.
  - Check it with S5's assembled DRC.
- **Outer ring (Imasha, Q3: yes):** one guard ring around the whole amplifier, drawn by S5's assembly
  (`assemble` in `src/s5/run.py`), tied to VSS, inside the outline.
- The flow's own ring width stays normal (Q10).

## Step 4: wiring loss

v2's route is 44 % shorter than v1's, yet it loses more GBW, so the extra coupling is probably inside the denser
blocks (track pitch 0.75 µm, units 0.05 µm apart). To find it:
- compare S6's per-net capacitances (`outputs/S6/<d>/*/`) between `iadc_ota` and `iadc_ota_v2` for the nets with the
  highest GBW sensitivity (S1);
- widen only those nets' track spacing (a per-net D0 widening, as `ruleset_v2.md` D2 allows).

## Then

- `ttsky25a_fd_v2`: compare it with the hand layout. It was started 2026-11-05; `scripts/finish_ttsky_v2.sh` finishes
  it and refreshes the reports.
- Imasha's drawn hierarchy for ttsky, if she makes one.
- v2 on the 5T and LOADBench: they use the spine router, and v2 needs the grid router. Either move them to
  `hierarchy: upstream` or teach the spine router the device keep-outs.
