# Rule set v2, phase 3: plan (on hold since 2026-11-05)

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

V0 reproduced the committed run (area-only 84.7 × 211.2 = 17,901 µm²; budget-aware 160.2 × 150.7 at 1.6 µm). The
other four were still running when work stopped; read their numbers from the log.

Pick the variant with the smallest area that still fits the tile, then implement it:
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
