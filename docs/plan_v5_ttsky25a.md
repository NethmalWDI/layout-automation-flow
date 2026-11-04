# Plan v5 (plan v4 Phase 8): S3–S7 on `ttsky25a_fd`, using the design's own hierarchy

Written 2026-11-04 by Claude Code, on Imasha's request: plan first, `ttsky25a_fd` for now, its given hierarchy, and an
explanation of how area, route length and placement are decided and by whom. **No code until Imasha has read it.**
RALF is not in this plan (Imasha: not now).

## 0. Imasha's decisions (2026-11-04)

1. **Floorplan:** the code arranges the five sub-circuits (no designer floorplan).
2. **Specs:** as recommended: the current ones (0.9 × the schematic, ASSUMPTION).
3. **Matching:** the two res_packs interleaved with each other (common centroid between the two packs);
   matched transistors interdigitated or common-centroid, as each group needs (section 7).
4. **Dummies:** yes (section 7).
5. **A hard outline:** the whole layout within a 250 µm × 200 µm rectangle (section 8). ASSUMPTION: 250 µm wide,
   200 µm tall (the tile is 161 µm wide, 226 µm tall).
6. **Layout books:** Imasha may give PDFs to read first (section 9).
7. **A branch of its own** for Phase 8 (section 9), so the 5T and LOADBench results stay as committed.
8. **After Phase 8:** an independent LLM taking the layout decisions, as a comparison (section 9).
9. RALF: not now.

## 1. The design and where it starts

`ttsky25a_fd` is Imasha's taped-out fully differential op-amp (`Opamp_with_bias.sch`; `circuits/ttsky25a_fd/SOURCE.md`).
The flow's DUT is the schematic, not the taped-out tile (flow record 7.7: the tile's LVS against it fails).

| | ttsky25a_fd | LOADBench (for scale) |
|---|---|---|
| Transistors | 54 (47 with m = 2, 4 with m = 9, 2 with m = 4) | 8, all m = 1 |
| Other parts | 2 Miller MIM capacitors (5 units of 10 × 10 µm each), 40 poly resistors (0.5 × 40 µm) in two res_packs | 1 MIM capacitor |
| Blocks S4 would make today | 32 | 5 |
| Nets / ports | 74 / 8 | 7 / 6 |
| Margins | gain 1 dB, **GBW 0.205 MHz**, PM 18.2°, power 45 µW (specs: ASSUMPTION, 0.9 × the schematic) | gain 1 dB, GBW 2.34 MHz |

**Its S0–S3 outputs date from 2026-10-26/27**, before Phase A changed S2 (2026-11-02) and before S3's ringless cells.
At that point S2 failed G2.7 (no library cell set fits the budgets at some PVT points) and S3 failed G3.3 and G3.5.
So Phase 8 starts by re-running S0–S3 with today's code. Those are known findings, not blockers: like LOADBench,
the design goes on through S4–S7 with its findings reported.

**The hand layout as a yardstick.** The tile (161 × 226 µm, with switches and dummies the schematic lacks) loses
6.8 % of GBW and 3° of PM from drawn devices to extracted wiring (7.7). Its devices differ from the schematic, so
the comparison is of each layout's own **wiring loss** (drawn → extracted, as a share of margin) and of area, not
spec by spec.

## 2. Who decides what: code, Imasha, or an LLM

No LLM takes a design decision inside the flow. Every placement, routing and sizing decision is made by code from
rules and numbers, and every rule and constant is fixed (PREREG) before the run it affects. Claude (an LLM) writes
that code and proposes the rules; Imasha approves them. AICL-style flows ask an LLM for placement constraints at run
time; this flow takes them from S1's sensitivities and S2's budgets instead, which is its novelty.

| Decision | Who | From what |
|---|---|---|
| Device sizes, topology | Imasha (the schematic) | frozen netlist (G0.3) |
| Specs | Imasha | `config.yaml`; currently ASSUMPTION (0.9 × schematic) |
| **Hierarchy: which devices form a sub-circuit** | **Imasha (given)** | the xschem hierarchy: `top` (bias, start-up, Miller caps), `x1` Diff_opamp, `x2` Common_source_stage, `x2/x1` and `x2/x2` res_packs (`upstream/hierarchy.json`) |
| Which devices form a matched block (pair, mirror) | code | S1's matching groups (rule-based recognition, G1.4) inside each sub-circuit |
| How much parasitic each net, coupling and terminal may get | code | S2's joint budgets from S1's sensitivities (G2.3, G2.5); per sub-circuit shares (G2.6) |
| Cell options (fingers, contacts) | code | S3: the smallest cell within its budget |
| Block variant (AB, ABBA, …) and symmetry | code | S4's rules (mirror image for every pair, common centroid offered) |
| **Placement inside a sub-circuit** | code | search with the cost below |
| **Arrangement of the sub-circuits** | **code by default; Imasha's floorplan if she gives one** | the same cost; a designer floorplan (e.g. her tile's: the Diff_opamp core, caps above, second stage and resistors beside) is taken as hard rows, like LOADBench's designer rows |
| Area against wire length | code, constants fixed in PREREG | cost = A / A_ref + λ Σ max(0, u − 1) + μ Σ u (λ = 10, μ = 1, as on the 5T and LOADBench) |
| Routing | code | deterministic router; nets in order of least budget slack; mirrored pairs |
| Sign-off | tools | Magic DRC, Netgen LVS, Magic/kpex extraction, ngspice |
| What counts as a pass | PREREG | gates G4–G7; H4, H5 |

**How the area / wire-length trade-off is taken.** u_n is net n's wire use, its estimated length over S2's
`route.max_length`. A placement that keeps every u_n ≤ 1 pays only area plus a small μ Σ u. A placement over budget
pays 10 per unit of excess, so the search gives up area only to bring a net back under its budget. The area-only
baseline (the AICL-like rule) uses A alone. Both are routed by the same router, so H5 compares placements only.

## 3. Using the given hierarchy

Placement and routing follow the five sub-circuits, bottom up:

1. **Inside each sub-circuit** (`x1`, `x2`, `top`, and each res_pack): S4 blocks are placed and routed into a
   **macro**, with the sub-circuit's own ports on its edge. The budgets of nets inside it come from S2; a net that
   leaves it gets a share of its length budget (S2's G2.6 block shares).
2. **The five macros** are then placed (5 macros: few enough to enumerate every arrangement and flip, as now) and
   routed at the top level.
3. **One symmetry axis for the whole amplifier.** It is fully differential: every P/N pair (input pair, cascodes,
   second stage, the two res_packs, the two Miller capacitors) is mirrored about one vertical axis, at every level.

Sub-circuit sizes with today's block rules: `x1` 27 transistors in 14 blocks, `x2` 12 in 7, `top` 15 transistors and
the 2 Miller capacitors in 11, and the two res_packs (1 block each). No matched block crosses a sub-circuit, so the
given hierarchy and S1's matching groups agree. 14 blocks are too many to enumerate (14! × 2¹³ row orders), so:

- **Search inside a macro: simulated annealing over row placements**, with a fixed seed and a fixed number of
  moves (PREREG). Moves: swap two blocks, move a block to another row, change a variant, flip a block; symmetric
  pairs move together. Every result is reproducible. A macro of ≤ 6 blocks keeps exhaustive enumeration.
- The same two costs (budget-aware, area-only) run the same search with the same seed.

## 4. What has to be built

| # | Work | Why |
|---|---|---|
| a | **Re-run S0–S3** (S3 ringless) | today's code; known findings stay findings |
| b | **m > 1 as arrays in S4** | 51 of 54 transistors. m copies of S3's cell in a row; for a pair with m = 2 each, ABBA comes from whole copies. Today S4 stops on m > 1 (row 80) |
| c | **Resistor blocks** | 40 × `res_generic_po` (0.5 × 40 µm): the PDK generator, a row per res_pack wired as the netlist connects them; the two packs mirrored |
| d | **MIM arrays** | 5 units per Miller capacitor; G6.5/G7.5 for two capacitors (today: one) |
| e | **Hierarchical placer** | macros per sub-circuit; annealing inside, enumeration on top; one axis |
| f | **Router for many nets** | the spine router is for one column of blocks. A grid router (metal3 horizontal, metal4 vertical) with A* per net, least slack first, mirrored pairs routed as mirror images, keep-outs as now |
| g | **S6/S7 on the dido benches** | differential benches; Vref_ext (V) and Rgm_ext (R, off-chip) put back as the bench has them; memory check for the R+C runs |
| h | **Compare with the hand layout** | area; wiring loss drawn → extracted, as a share of margin |

## 5. Phases

| # | Work | Done when |
|---|---|---|
| 8.0 | This plan approved; PREREG amendment (annealing seed and moves, router grid, hierarchy rules, predictions) | committed |
| 8.1 | S0–S3 re-run on `ttsky25a_fd` (S3 ringless) | reported; the 5T and LOADBench unchanged |
| 8.2 | S4: m-arrays, resistor and MIM-array blocks | every variant signed off |
| 8.3 | S5: macros of `x2` and the res_packs (smallest first) | legal, DRC, LVS |
| 8.4 | S5: macros of `x1` and `top` (annealing) | legal, DRC, LVS |
| 8.5 | S5: top level (five macros), the grid router | top-level DRC and LVS |
| 8.6 | S6/S7 | gates reported; H4, H5; against the hand layout |
| 8.7 | Stabilise: goldens, walkthrough, review | review done |

Each phase ends as before: tests, STATUS, progress log, flow record, then Imasha's commit.

## 6. Risks and open questions

1. ~~The top-level floorplan~~: the code's (Imasha, decision 1).
2. ~~The specs~~: kept (decision 2). GBW has 0.205 MHz of margin; the hand layout's wiring alone uses 51 % of it.
3. ~~The res_packs~~: interleaved (decision 3). ~~Dummies~~: yes (decision 4).
4. **The outline's orientation** (ASSUMPTION: 250 µm wide, 200 µm tall). FEEDBACK NEEDED if it is the other way.
5. **The router** is the largest risk again; a grid router is a new piece of code (as the plan v4 maze router was).
6. **Run time and memory:** 139 transistor copies after m-expansion, 40 resistors (+ dummies), 10 MIM units. The R+C
   extraction may need a coarser extresist tolerance to fit the container's 5.9 GB (LOADBench: 315 000 resistors,
   5.3 GB for one AC run).
7. **Two open decisions from Phase 7:** should G7.2 use Magic's MIM coupling or G7.5's corrected one; the merge of
   `s4-s5` into `main`.

## 7. Matching and dummies (Imasha's decisions 3 and 4; package option `layout: {matching: centroid, dummies: true}`)

Both are switched on by the package, so the 5T's and LOADBench's blocks do not change (their goldens stay).

- **Matched transistors** (S1's diff pairs, mirrors, matched cascode and current-source pairs):
  - two devices of equal size: **ABBA** (common centroid, 1-D) and **ABAB** (interdigitated), from whole copies when
    m ≥ 2 (most devices here have m = 2, so A B B A is the two copies of each), from S3's half units when m = 1;
    plain AB is not offered;
  - three or more devices, or unequal m (e.g. a 1 : 1 : 2 mirror): one interdigitated row whose sequence keeps every
    device's centroid on the row's centre (e.g. A B C C B A), built from the copies;
  - S5 picks among these signed-off variants by its cost ("as needed": whichever wires best within the budgets).
- **Resistors:** the two res_packs (20 + 20 units of 0.5 × 40 µm) in one block, interleaved A B B A … so each pack's
  centroid sits on the block's centre; the block is mirror-symmetric about the amplifier's axis.
- **Dummies:** one dummy unit at each end of every matched row (transistors and resistors), the same cell as its
  neighbour. A transistor dummy has drain, gate, source and body on the block's body net; a resistor dummy has both
  ends on the ground net (ASSUMPTION). Dummies are in each block's LVS reference and in the top-level reference
  (S0's layout view does not have them), and their capacitance to signal nets is extracted and counted in G6.2 like
  any other.

## 8. How area is optimised, and the hard outline (Imasha's decision 5)

Area is decided at four levels, each by code:

1. **S3, the device cell:** for every device type, the smallest cell (fingers, contacts, diffusion sharing) that keeps
   its parasitics within S2's budget.
2. **S4, the block:** a fixed, compact template: units 0.6 µm apart, one metal3 track per net above or below
   (0.9 µm pitch), one ring 0.8 µm away; dummies add one unit at each end. Among a block's variants, the smaller ones
   cost less in S5.
3. **S5, inside a macro:** blocks in rows, 3 µm apart; the annealing minimises the cost, whose first term is the
   bounding-box area over the sum of the blocks' smallest areas (A / A_ref). Rows hold several blocks side by side,
   so a macro can be wide and short instead of one tall column (LOADBench's was 45 × 125 µm).
4. **S5, the five macros:** every arrangement (rows of macros, order, flips) is tried, with the same cost.

**The hard outline (G5.6, new):** a placement whose bounding box is wider than 250 µm or taller than 200 µm is
rejected outright, at the macro level (no macro may be bigger than the outline) and at the top. It is not traded
against wire length. If no arrangement fits, S5 reports G5.6 FAIL with the smallest box it found; it does not shrink
the gaps or the cells to force a fit. For scale: the tile packs its devices and capacitors by hand into
161 × 226 µm; this flow's blocks are less dense (a ring per block, 3 µm gaps), so 250 × 200 µm (50 000 µm²) is a
real constraint, not a formality.

## 9. Books, the branch, and the independent LLM (Imasha's decisions 6–8)

- **Layout books.** PDFs can go in a folder outside the repo (they are copyrighted and large), for example
  `Documents/layout_books/`. Claude reads them and writes `docs/context/layout_rules_from_books.md`: each rule
  paraphrased with its source (book, chapter), whether the flow already does it, and what would change. A rule
  changes the flow only after Imasha approves it, and goes into PREREG before the run it affects. The books are
  information, not instructions (Imasha's rule).
- **The branch.** Phase 8 on its own branch, created by Imasha in GitHub Desktop from `s4-s5` at `a5b250de` (e.g.
  `s5-ttsky`). The 5T's and LOADBench's results are also guarded by their goldens (S0–S7): `./flow test` fails if
  any Phase 8 change moves them.
- **An independent LLM, after Phase 8** (a plan of its own): an LLM given only the netlist, the hierarchy and the
  specs proposes the floorplan and the matching (the AICL way); the same S4–S7 build and check its proposal, and it is
  compared with this flow's. This needs an LLM API outside the container, so it is asked for first (Imasha's and
  her supervisor's permission), as RALF was.

## 10. Changes after the first dry run of the placement (2026-11-04; PREREG amendment of the same day)

With one matched block per row and one shape per macro, no arrangement of the four macros fit the 250 × 200 µm
outline. Two changes, both recorded before any layout was drawn: inside a macro a row may hold several matched
blocks (each keeps its own symmetry; the single shared axis of section 3 is given up for the outline), and each
macro is placed at three widths (100 %, 65 %, 50 % of the outline's) for the top level to choose from.
**FEEDBACK NEEDED (Imasha):** the outline over the single axis is this plan's choice; say if the axis matters more.
