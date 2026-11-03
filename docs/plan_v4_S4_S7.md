# Plan v4: block generation, placement, routing and verification (S4–S7) on the 5T and LOADBench

**Branch:** `s4-s5`, from `main` at tag `s0s3-reviewed` (`ec359567`). `main` keeps the reviewed S0–S3 state until a
review like the S0–S3 one merges this branch. **Started:** 2026-11-03.

**Imasha's decisions (2026-11-03):**
- Implement our own engine, keeping the flow's novelty, as decision D8 (`docs/06_final_plan_critical_review.md` B8)
  set out.
- S3's unit cells lose their guard rings; every S4 block gets one ring.
- Work on branch `s4-s5`: first S4–S7 on the 5T and LOADBench, then stabilise, then a more complex design.

Still open (section 8): RALF as a baseline (needs a download), and which harder design.

## 1. The stages

| Stage | Does | Writes (`outputs/<stage>/<design>/`) |
|---|---|---|
| S3 (changed) | Same choice of cells as now, but each unit cell is drawn **without a guard ring** (`guard 0`). The body pin becomes a label on the n-well (PMOS) or the substrate (NMOS) | as now |
| S4 | **Block generation.** One block per matched group or single device: units from S3, placed in an arrangement, wired inside, with **one guard ring**. Several variants per block, each signed off and extracted | `blocks.json`, `blocks/<block>__<variant>/`, `s4_report.json` |
| S5 | **Placement and routing.** Picks one variant per block, places the blocks, and routes the nets between them | `placement.json`, `top.gds`, `routing_report.json`, `s5_report.json` |
| S6 | **Sign-off and extraction** of the top level: DRC, LVS, PEX with Magic, and kpex as a cross-check. Every net's C and R is compared with its S2 budget | `parasitics_vs_budgets.json`, `s6_report.json` |
| S7 | **Post-layout evaluation** in the flow's own benches (the code of `scripts/reference_layout.py`): specs, and each margin's use against eta | `metrics.json`, `s7_report.json` |

S8 (repair) and S9 (selection) come after these work.

## 2. How the decisions are taken

**Hard rules, from S0's IR** (device model, body net, supplies):
1. A block holds **one device type with one body net**. Mixed groups are split; LOADBench's `cs_stage` gives N3 a
   block of its own, and P5 sits in the bias bank, as in the designer rows.
2. Blocks with the same well potential may share a well. Different wells keep SKY130's well-to-well spacing.
   LOADBench's P6/P7 have their own body net, so they get their own n-well.
3. **PMOS on the supply side (top), NMOS on the ground side (bottom)**: an ordering constraint in placement.
4. **Symmetry.** S2's `place.symmetry.*` and `route.symmetric.*` put matched blocks on one vertical axis and mirror
   their routes.

**Groups stay together.** S1's matching groups (G1.4) and S0's blocks become one S4 block each, built as one unit,
so its devices cannot end up apart.

**Order (what is on top, what is left).**
- Rows come from rule 3. Designer rows are used when the package gives them; LOADBench's
  `inputs/loadbench_miller/designer_groups.yaml` does: bias bank, then the input pair, then the NMOS mirror and N3.
- Within a row, the order, orientation and variant are chosen by the cost below.
- With 3 to 6 blocks every candidate can be enumerated, so the result is exact and explainable. Simulated
  annealing over a sequence pair (D8) is kept for larger designs.

**Cost and order of work.**
1. **S4:** variants per block (arrangement side-by-side / ABAB / ABBA, orientation, pin side; end dummies as an
   option). Each is DRC/LVS-checked and extracted, so its area and internal C are measured. Variants beaten on
   every count are dropped.
2. **S5 placement:** cost = area + λ × predicted budget violation + penalties.
   - The predicted violation, for every budgeted net: the estimated wire length × C per µm (S2's `parasitics.json`)
     plus the block's port C, against the net's S2 budget. The same for coupling (the side-by-side run of critical
     pairs) and for R (length × R per µm, against the R that S3 left for routing).
   - Budgets act as constraints: the smallest placement that meets them wins.
   - An **area-only cost**, as in AICL's packer, runs as the baseline.
3. **S5 routing:**
   - Nets go in order, least budget slack first, on a grid A* with each layer's preferred direction.
   - Width comes from the R budget. `route.max_parallel` keeps critical pairs apart. Symmetric nets are routed
     mirrored.
   - A net that misses its budget is re-routed, then sent back to placement.
4. **S6/S7:** extracted C and R against the budgets; post-layout SPICE. The smallest passing layout wins.

**What is new against the literature:** S2's joint budgets drive placement and routing; every extracted parasitic is
checked against its own budget; G2.0's prediction is tested on a real layout; the output is PCell-exact SKY130.
AICL packs for area without connectivity; the McMaster flow checks per-net budgets after an area optimisation.

## 3. Inputs S4–S7 read (frozen: `tests/frozen/s0_s2_outputs.json`)

| From | File | Used for |
|---|---|---|
| S0 | `circuit_ir.json` | devices (type, W, L, nf, body net), nets, blocks, designer rows |
| S0 | `ref/<d>_layout.spice`, `tb/` | LVS reference; the benches for S7 |
| S1 | `s1_report.json` (G1.4), `sensitivity.json` | matching groups; which nets are critical |
| S2 | `budgets.json` | C per net, coupling per pair, R per terminal |
| S2 | `constraints.json` | `route.max_length.*`, `route.max_parallel.*`, `route.max_series_R.*`, `place.symmetry.*`, `route.symmetric.*`, `place.proximity.*`, `place.latchup_tap_distance` (15 µm) |
| S2 | `hierarchy.json` | each budget split into the part inside a block and the top-level part |
| S2 | `outputs/S2/pdk/parasitics.json` | C and R per µm per layer |
| S3 | `device_decisions.json`, `_cells/<cell>/` | chosen option per type, geometry, pins (the `.mag` labels), access R |

## 4. The blocks of the two designs

**5T (3 blocks):**
- `pmos_current_mirror_load`: XM3, XM4; PMOS, body VDD; n-well with an n-tap ring.
- `nmos_differential_pair`: XM1, XM2; NMOS, body VSS; p-tap ring; arrangements AABB / ABAB / ABBA at the level of
  S3's units.
- `nmos_current_mirror_bias`: XM5; NMOS, body VSS.

**LOADBench (5 blocks):**
- `pmos_bias_bank`: P2, P8, P5; body `sourcePmos`. The width ratio is 1 : 2.43 : 23.8, not an integer, so the
  devices sit side by side, not interdigitated (open question 3).
- `input_pair`: P6, P7; body `FirstStageYsourceTransconductance`, its own n-well.
- `nmos_mirror_load`: N1, N4; body `sourceNmos`.
- N3 alone; body `sourceNmos`.
- `Capacitor2`: ideal 0.5 pF in the netlist (open question 4).

## 5. Gates

- **S3 (changed):** as now. In addition, every unit cell has no guard ring and its body pin is labelled.
- **S4:**
  - G4.1: one type and one body net per block; ring present.
  - G4.2: DRC 0 for every variant, with a negative control.
  - G4.3: LVS for every variant (W, L, nf and the block's connectivity), with a negative control.
  - G4.4: matched devices' centroids mirror about the block's axis.
  - G4.5: every diffusion within 15 µm of a tap (S2's latch-up rule).
  - G4.6 (info): port C against `hierarchy.json`.
- **S5:**
  - G5.1: the placement is legal (no overlap, well spacing, PMOS above NMOS, symmetric blocks on the axis).
  - G5.2: top-level DRC 0.
  - G5.3: top-level LVS against `ref/<d>_layout.spice`.
  - G5.4: every `route.*` rule in `constraints.json` checked by script.
  - G5.5 (info): area against the area-only baseline.
- **S6:**
  - G6.1: PEX done.
  - G6.2: every net's extracted C, every coupling and every terminal R within its S2 budget.
  - G6.3 (info): kpex against Magic.
- **S7:**
  - G7.1: every spec met post-layout (nominal).
  - G7.2: every check uses at most eta × margin × (1 + `TOL_USE`).
  - G7.3 (info): G2.0's prediction against the post-layout use (PREREG: within 25 %).
  - G7.4 (info): PVT points.

PREREG's amendment of 2026-11-03 states the predictions.

## 6. Keeping the reviewed state safe

- `tests/test_s4s5.py` hashes the S0–S2 files later stages read (75 files, `scripts/freeze_outputs.py`) and fails if
  any changes. A deliberate change re-runs the script and is logged.
- S4–S7 read S0–S3 and write only their own folders. `./flow run <d> --from S4` re-runs them alone.
- The existing tests and the 20 goldens pass on every commit. S3's goldens change once, in Phase 1, on purpose.
  S4–S7 get goldens in Phase 7.
- Merging into `main` waits for a review.

## 7. Phases

| # | Work | Done when |
|---|---|---|
| 0 | Freeze test; this plan; PREREG amendment; STATUS | tests pass; committed |
| 1 | S3 without guard rings; re-run the 5T and LOADBench; compare with the reviewed S3 | S3 gates as before; changes explained (flow record) |
| 2 | S4 on the 5T: pair, mirror and single device; rings; variants | G4.1–G4.5 pass |
| 3 | S5 placement on the 5T; area-only baseline | G5.1 passes |
| 4 | S5 router on the 5T | G5.2–G5.4 pass |
| 5 | S6/S7 on the 5T | G6/G7 reported; the 5T expected to pass |
| 6 | LOADBench through S4–S7 | reported; gain over eta expected (G2.0 = 0.999) |
| 7 | Stabilise: goldens, walkthrough to S7, review, merge | review done |
| 8 | Harder design | open |

## 8. Risks and open questions (FEEDBACK NEEDED, Imasha)

1. **The router** is the largest risk (D8). Mitigation: a grid, few top-level nets, and RALF's router if allowed.
2. **The body pin without a ring.** S3's LVS and in-circuit simulations need the body labelled on the n-well or the
   substrate. First thing to settle in Phase 1.
3. **LOADBench's PMOS bank** (1 : 2.43 : 23.8): side by side as S3 sized them (proposed), or units rounded to an
   integer ratio (changes the sizing, needs a decision).
4. **The Miller capacitor** is ideal in the netlist. Draw it as a SKY130 MIM capacitor (PREDICTED), or leave it out of
   the layout and keep it ideal in S7?
5. **Dummies** at row ends: in the first variants or later? They add C to the nets they touch, charged to the budgets.
6. **RALF** as a baseline: needs the download from GitHub (Imasha, and the supervisor if it counts as a connection).
7. **The harder design:** `ttsky25a_fd` (hand layout measured) or `iadc_ota`.
