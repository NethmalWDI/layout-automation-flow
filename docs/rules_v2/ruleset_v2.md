# Layout rule set v2 (S4 blocks, S5 placement and routing): draft for Imasha's review

Status: **REVIEWED by Imasha, 2026-11-05.** Rules accepted with the answers in section 7, which override the rule
tables where they differ. Two points are still open: Q9's exact reading, and the Q4 screening proposal (7.1). Branch
`rules-v2`.
- No code has changed. The flow keeps rule set v1 until the review is done.
- v2 will be opt-in per design (`ruleset: v2` in `inputs/<d>/layout.yaml`), so v1's results and goldens stay as they are.
- First use: a GUI copy of `iadc_ota`, following Imasha's hand-drawn hierarchy (to come).
- Every value below comes from one of four places:
  1. the SKY130 DRC deck, with its rule id;
  2. a source in `C:\Users\suind\Desktop\layout_books` (cited as [ICMD p.x] and so on);
  3. S2's budgets;
  4. an **ASSUMPTION** or a **QUESTION** for Imasha.
- Book content is paraphrased with page numbers. Nothing is quoted at length.

## 1. Sources

| Key | Source | What it gave |
|---|---|---|
| **ICMD** | C. Saint, J. Saint, *IC Mask Design: Essential Layout Techniques* (McGraw-Hill, 2002) (`ic-mask-design-essential-layout-techniques_compress.pdf`) | the main source for v2. Ch. 3 analog layout, Ch. 4 parasitics, Ch. 5 matching, Ch. 6 noise, Ch. 7 floorplanning, Ch. 8 general techniques; **Case Study 1, a CMOS differential amplifier (pp. 247–326)**; Case Study 2, a bipolar Gilbert-cell mixer (pp. 341–394) |
| DRC | SKY130A Magic DRC deck, `$PDK_ROOT/sky130A/libs.tech/magic/sky130A.tech` (image `hpretl/iic-osic-tools:2026.10`) | every minimum spacing, width and enclosure below |
| ASP22 | N. Karmokar et al., "Common-Centroid Layout for Active and Passive Devices: A Review and the Road Ahead", ASP-DAC 2022 | why CC works; 1-D and 2-D CC; layout-dependent effects; when CC is *not* best (its 5T OTA and StrongARM case studies, §V-B) |
| LONG05 | D. Long, X. Hong, S. Dong, "Optimal Two-Dimension Common Centroid Layout Generation for MOS Transistors Unit-Circuit", ISCAS 2005, pp. 2999–3002 | the four CC criteria, the even-finger theorem, orientation balance, the 2-D generation algorithm, routing in channels |
| CAD | M. Williams, "More Current Mirrors in Analog Layout", Cadence blog, 3 Aug 2023 | multi-leg mirrors; dummies at the row ends and extra dummy rows |
| WVU | D. W. Graham, "Analog IC Layout", lecture slides, West Virginia University | matching rules of thumb, CC examples, dummies, latch-up, an OTA with one ring per stack (slides 19–39) |
| TAMU | S. Palermo, J. Silva-Martinez, ECEN 474 Lecture 6 "Layout Techniques", Texas A&M | stacks, interdigitation, guard rings and latch-up, floorplanning, an industrial OTA with a ring per stack and an outer ring (slides 20–25, 48–50, 58–61) |
| LS | J. Lienig, J. Scheible, *Fundamentals of Layout Design for Electronic Circuits* | the PDF holds only the front matter and the start of chapter 1; nothing was taken from it |

## 2. What the sources teach (the intuition behind the rules)

### 2.1 Case Study 1 of *IC Mask Design*: a CMOS differential amplifier [ICMD pp. 247–326]

The circuit has five transistors: a PMOS active load (M1, M2), an NMOS input pair (M3, M4) and a current source (M5). Four copies sit on a test chip. The mask designer's layout is reviewed twice by the circuit designer. What the review taught, in order:

1. **Ask three questions first** (pp. 249–251; also pp. 54–55):
   - what does the circuit do?
   - how much current flows, and where?
   - what has to match, and how well?
   - Most of the later rework came from vague answers: 1–2 mA was quoted, and 5 mA was the real worst case over process and temperature.
2. **Reshape long, thin devices into fingers with the same total W** so the layout is compact. Agree the change with the designer (pp. 251–254).
3. **Keep every gate in one direction.** It helps matching and gives one metal direction (pp. 256–257).
4. **Keep an amplifier's input and output wires apart.** A space-saving flip put them side by side, which the designer rejected as a risk of oscillation (pp. 267–268, 275). Saving space is not always good.
5. **Cross-quad the input pair.** Split each device into two halves, place the halves diagonally, run the common (source) node through the centre and bring the inputs in symmetrically through the middle (pp. 275, 283–294).
   - A pair drawn as two devices cannot be cross-quaded. The schematic had to be split, so ask the designer to split it.
6. **Size current paths for the worst case.**
   - In a differential pair, the whole tail current can flow in one side. So each half of a split device must carry half of the maximum, and each wire is sized for that (pp. 284–289).
   - Use many vias on current paths (p. 294).
7. **Do not let current crowd at one corner.** The current source was rotated so its current leaves along the fingers into wide metal (pp. 276–277). It was later split in two for symmetry, so all the NFETs line up in one row (pp. 295–296).
8. **Taps:**
   - well and substrate ties at the far edges of each device, not only near one side (p. 277);
   - devices pulled apart slightly to fit substrate contacts close to the cross-quad (pp. 294–295);
   - the PMOS enclosed in n-well contacts (p. 300);
   - **the substrate contacts between two neighbouring devices merged into one, to save space** (p. 301).
9. **Align the centre lines** of the PMOS loads, the input pair and the current source (p. 302).
   - Differential input and output wires have equal lengths and leave symmetrically (pp. 302–303, 318).
10. **The layout hierarchy follows the schematic hierarchy,** so LVS can be checked level by level (p. 315).

### 2.2 Case Study 2 (bipolar Gilbert mixer) [ICMD pp. 341–394]

The lessons that carry over to CMOS:
- Stack the sections in the order of the schematic, with inputs on opposite sides and the output far from both (pp. 346–351).
- A block that is not on the signal path (the current source) does not need symmetry (p. 351).
- Draw a common node's current from its centre, so both halves see the same impedance (pp. 353–355).
- Connect wide devices at both ends, so the current exits through twice the width (pp. 363–364).
- Interdigitated, then **cross-quaded** pairs in the final version (pp. 379–391).
- Add dummies at the ends of the arrays (pp. 362, 370, 383).
- Stop when the returns diminish (p. 393).

### 2.3 Chapters 3–8 of *IC Mask Design*

**Matching (Ch. 5):**
- Matched devices go close together, in the same orientation (pp. 99–102).
- Matched devices share one unit device (pp. 103–105).
- In interdigitation, the reference device goes in the centre with the others wrapped around it (pp. 105–106).
- Common centroid cancels linear gradients and hot spots (pp. 109–110).
- The **cross-quad** is for two devices, each split in halves and placed diagonally. `ABBA` in a line is the cheaper version when area is tight (pp. 110–113).
- Matched devices have one common width, with only the length varied (p. 117).
- Dummies at the array ends, at the same pitch as the devices. A full dummy ring is for the strictest matching (pp. 108–109).
- Match the wiring as well: the same lengths, overlaps and metals (pp. 112–113, 115–116).
- The required matching level is an input from the designer, never guessed (pp. 64, 102, 169).

**Noise (Ch. 6):**
- Noisy and sensitive blocks go far apart (p. 129).
- Guard both the noisy and the quiet block (p. 128).
- Rings around noisy blocks are wide (not minimum), closed, and tied to ground with a wide strap (pp. 126–128).
- Differential wires run side by side over their whole length (pp. 132–134).

**Parasitics and floorplan (Ch. 4, 7, 8):**
- Do not route over other blocks or devices. In particular, nothing over the bias block or over capacitors; route sensitive nets around (pp. 84–86, 149–150, 169–170).
- When nothing may route over blocks, size each channel from the number of nets times the wire pitch (pp. 155–156).
- Symmetry outranks area; lay out half and mirror it (pp. 114, 149, 152–153).
- Size wires from current (pp. 56–62, 165–166).
- Pick the metal layer by its actual parasitics, which is not always the top metal (pp. 82–84, 165).
- Prefer rectangular blocks (p. 174).

**On minimum spacing (where the book and this plan differ):**
- The book tells analog designers not to use minimum rules out of habit: performance comes first (pp. 51, 58).
- It suggests routing on uniform, slightly-above-minimum widths and spacings, keeping the slack as reserve, and dropping to the true minimum only when stuck (pp. 162–165).
- Imasha's direction is DRC minimum "as the design and space allow". Rule D0 below keeps her direction, but makes it conditional on S2's budgets, the numbers that say where minimum is harmless. The book's reserve slack is offered as a choice (**QUESTION Q9**).

### 2.4 From the papers and slides

- **CC cancels a linear gradient**; 2-D CC cancels it in any direction [ASP22 p.1; WVU 24–25].
- **A good CC array** has coincident centroids, symmetry about both axes, dispersion, and a near-square outline [LONG05 Def. 1].
- **Orientation balance:** each device has equal left and right fingers [LONG05 Cond. 1].
- **Unit counts:** even for every device, with at most one odd [LONG05 Thm. 1].
- **Layout-dependent effects** (LOD, WPE) need matched devices with the same surroundings. Rows swapped A↔B fix LOD and routing mismatch [ASP22 pp. 2, 6].
- **ASP22's case studies:** large devices went to multi-row CC, small ones to clustered. A single-row CC of a small mirror was worse [ASP22 pp. 6–7].
- **Multi-leg mirrors:** the reference goes in the centre, critical legs nearest [CAD].
- **One ring per stack, an outer ring around the amplifier** [TAMU 50, 58–61; WVU 38].
- **Latch-up:** taps everywhere. The SKY130 limit is 15 µm (LU.2, LU.3).

## 3. The rules

`v1` is what the flow does now; `v2` is the proposal. "Source" is where the v2 value comes from.

### I: intent the layout needs first (the three questions)

| Id | Rule | v1 | v2 | Source |
|---|---|---|---|---|
| I1 | Matching level per group | S1 infers the matching groups (G1.4) | each group carries a level given by Imasha: *adjacent* / *interdigitated* / *common centroid (1-D or 2-D cross-quad)*; it chooses which M patterns are candidates. Taken from her hierarchy drawing; S1's groups stay as a cross-check | ICMD pp. 64, 102, 169; CS1 p. 275 |
| I2 | Worst-case current per branch | S2's `min_width_from_current` | unchanged, and for a differential pair each side is sized for the **whole** tail current (each half of a split device for half of it) | ICMD CS1 pp. 284–289 |
| I3 | Noisy and sensitive blocks | — | each block may be tagged *noisy* (e.g. clocked, like a switched-capacitor CMFB) or *sensitive* (input pair, bias); the tags drive T3, P3, R1 | ICMD pp. 122, 126–129, 149–150 |

### D: DRC-minimum spacing

**D0 (principle).** Every spacing is the DRC minimum for the two shapes that face each other. It is widened only when one of these asks, and each widening is recorded with its reason:
- an S2 budget: a coupling, or a parallel run at minimum spacing;
- a routing channel the router needs (R2);
- a tag (I3);
- a cited book rule.

The book's reserve slack (ICMD pp. 162–165) is QUESTION Q9.

DRC values used (Magic deck, µm):

| Rule | Value | Rule | Value |
|---|---|---|---|
| diff/tap.3 diffusion spacing | 0.27 | nwell.1 n-well width | 0.84 |
| diff/tap.8 n-well enclosure of p-diff | 0.18 | nwell.2a n-well spacing (wells may touch and merge) | 1.27 |
| diff/tap.9 n-diff to n-well | 0.34 | poly.1a / poly.2 width / spacing | 0.15 / 0.21 |
| diff/tap.10 n-well enclosure of n-tap | 0.18 | poly.4 poly (non-gate) to diffusion | 0.075 |
| diff/tap.11 p-tap to n-well | 0.13 | li.1 / li.3 width / spacing | 0.17 / 0.17 |
| met1.1 / met1.2, met2.1 / met2.2 | 0.14 / 0.14 | met3.1 / met3.2, met4.1 / met4.2 | 0.30 / 0.30 |
| capm.1 MIM width | 1.0 | capm.2a MIM spacing | 0.84 |
| capm.3 met3 enclosure of MIM | 0.14 | capm.11 MIM to unrelated met3 | 1.34 |
| LU.2 n-diff to p-tap, LU.3 p-diff to n-tap | < 15.0 | | |

| Id | Rule | v1 | v2 | Source |
|---|---|---|---|---|
| D1 | Unit to unit inside a block | `GAP` 0.6 µm fixed | the least distance at which the facing shapes are legal, measured from the cells' geometry; dummies at the same pitch as the devices | DRC; ICMD p. 108 |
| D2 | Metal3 tracks of a block | width 0.4, pitch 0.9 | width = max(0.30, the I2 width for the net); spacing 0.30, widened when two nets run side by side longer than S2's `max_parallel_run_at_min_spacing` | DRC; S2; ICMD pp. 56–62 |
| D3 | Units or tracks to the ring or tap strip | `RING_GAP`/`TAP_GAP` 0.8, `FIRST` 1.0, `EXT` 1.0, `NWELL_OVER` 0.5 | the least legal distance for the shapes present, computed | DRC |
| D4 | Block to block (S5) | `BLOCK_GAP` = `ROW_GAP` = 3.0 µm | facing shapes at the DRC minimum: blocks sharing a ring (T1) abut; separate n-wells of different nets 1.27; n-diff to n-well 0.34; plus the R2 channel where routes must pass | DRC; R2 |
| D5 | Routing margin round the placement | `MARGIN` 8.0 µm | only what the router uses; the outline is the drawn shapes' box | DRC |
| D6 | MIM | `CAPM_SPACE` 1.45 | 1.34 (capm.11) on the 0.005 µm grid; 0.84 between MIMs | DRC |
| D7 | Margin inside the latch-up distance | `TAP_MARGIN` 0.5 µm | **QUESTION Q6** | DRC LU.2/.3 |
| D8 | Values typed from DRC | constants in several files | one generated table with rule ids | DRC |

### T: taps and guard rings

| Id | Rule | v1 | v2 | Source |
|---|---|---|---|---|
| T1 | Rings | one per block | one ring per **stack** (blocks of one type and one body net placed together); neighbouring stacks with the same body net **share the ring edge between them** | ICMD CS1 p. 301; TAMU 50, 59–61; WVU 38 |
| T2 | Taps inside a stack | ring plus strips where S2 needs them | ties at the far edges of every device as well as near it, and strips wherever a diffusion would otherwise be beyond LU.2/LU.3 (S2's `max_diff_to_tap_distance`) | ICMD CS1 pp. 277, 294–295; DRC |
| T3 | Noisy and sensitive blocks (I3) | — | a sensitive block (the input pair) keeps a stack and ring of its own; a noisy block gets a wider (non-minimum) closed ring with a wide strap to ground; how wide is **QUESTION Q10** | ICMD pp. 126–128; TAMU 49, 61 |
| T4 | Outer ring round the whole amplifier | none | **QUESTION Q3** | TAMU 59 |
| T5 | Rings closed | yes | yes, checked | ICMD p. 128 |

### M: matching patterns (S4 variants), with the cross-quad and 2-D common centroid

| Id | Rule | v1 | v2 | Source |
|---|---|---|---|---|
| M1 | Candidate patterns | 1-D only: `AB`, `ABBA`, `ABAB`, palindromic rows; iadc's array folds one device | 1-D as now, **plus** the **cross-quad** (2 × 2: `AB/BA`, each device in two diagonal halves) for two devices; **2-D CC** with r rows (`ABBA/BAAB`, `AABB/BBAA`, …); 2-D interdigitated (`ABAB/BABA`); clustered for small groups. The matching level (I1) selects which are allowed | ICMD pp. 105–113, CS1 pp. 283–294, CS2 pp. 385–391; ASP22 §IV–V; LONG05; WVU 25 |
| M2 | Every 2-D candidate must meet | — | coincident centroids in x and y; symmetry about both axes; equal orientation balance per device; dispersion and squareness as scores | LONG05 Def. 1, Cond. 1 |
| M3 | Unit counts | half units when the finger count is even | a cross-quad or 2-D CC needs each device's units to divide into the pattern (even, at most one odd on the centre); otherwise the flow **proposes a split to the designer** (ICMD CS1 p. 283) and uses dummies or ID meanwhile. It never changes the schematic itself | LONG05 Thm. 1; ICMD p. 113 |
| M4 | Rows of a 2-D array | — | row k+1 swaps A and B, so LOD and routing match | ASP22 p. 6 |
| M5 | Choosing among allowed patterns | S5 cost (area + budgets); Imasha 2026-11-04: CC or interdigitated as needed | unchanged: every allowed candidate is signed off and S5 picks by cost. Order of trial: large groups 2-D CC first, small groups clustered or ID first. **QUESTION Q4** | ASP22 §V-B; ICMD p. 169 |
| M6 | Aspect ratio | rows only (iadc: up to 154 × 10.8 µm) | rows r chosen for a near-square array, or to fit the width S5 offers | ICMD p. 93; ASP22 p. 1; LONG05 Def. 1 |
| M7 | Multi-leg mirrors and interdigitation | — | the reference (diode) device in the centre, the others around it; the most critical legs (S1 sensitivity) nearest | ICMD pp. 105–106; CAD |
| M8 | Orientation and width | same orientation in a row | all gates in one direction everywhere; a matched group shares one finger width (S3 already uses identical options per group) | ICMD pp. 101–102, 117, 168–169, CS1 pp. 256–257; LONG05 |
| M9 | Wiring of a matched group | — | the same length, metals and crossings for each member, with dummy crossings added where one member would otherwise have fewer | ICMD pp. 112–113, 115–116, CS2 p. 379 |

### Y: dummies

| Id | Rule | v1 | v2 | Source |
|---|---|---|---|---|
| Y1 | Flow dummies | `dummies: true`: one at each row end | at both ends of every row of a matched array, same pitch as the devices; a full dummy ring when I1 asks for the strictest level | ICMD pp. 108–109; CAD; WVU 27 |
| Y2 | The designer's own dummy transistors (iadc: 38, e.g. `XM43`, `XX1_M46` … `XX2_M83`) | each a separate block with its own ring and 3 µm gaps | placed at the ends of the matched array they serve, inside its ring; the assignment comes from Imasha's hierarchy drawing, or else from their nets | ICMD pp. 108, 385; CAD; TAMU 60 |
| Y3 | No double dummies | — | a flow dummy only where no designer dummy is | — |

### P: placement (S5)

| Id | Rule | v1 | v2 | Source |
|---|---|---|---|---|
| P1 | Hierarchy | from the package (`hierarchy: upstream` for iadc) | Imasha's hand-drawn hierarchy: which blocks form a stack, the stacks' order, the macros | ICMD p. 315; TAMU 50 |
| P2 | Symmetry | matched blocks on a common axis | the centre lines of the stacked sections of one amplifier aligned (loads, input pair, tail); half laid out and mirrored where the circuit is symmetric; symmetry outranks area | ICMD CS1 p. 302, pp. 114, 149, 152–153 |
| P3 | Noisy vs sensitive | — | noisy and sensitive blocks placed as far apart as the outline allows; the inputs on opposite sides and the output away from both | ICMD p. 129, CS2 p. 351, CS1 pp. 268, 275 |
| P4 | Signal flow | cost = area + budgets | unchanged, with the order of stacks following the schematic (current source, pair, loads) | ICMD CS2 pp. 346–351 |

### R: routing

| Id | Rule | v1 | v2 | Source |
|---|---|---|---|---|
| R1 | Metal over devices | metal3 avoids only tracks and capacitor keep-outs; metal4 runs freely over devices | every block's device area is a keep-out for metal3/metal4 of *other* nets. Allowed: its own nets; a crossing **symmetric over a matched block** (the same wire over both halves). Never over a sensitive block (I3), the bias block, a capacitor, or a block whose net S2 marks `no_crossing_over_high_impedance` | Imasha 2026-11-05; ICMD pp. 84–86, 149–150, 169–170; ASP22 pp. 6–7; LONG05 p. 3002 |
| R2 | Channels | the fixed 3 µm gaps double as channels | a channel is as wide as the tracks that must pass (n × the D2 pitch): S5 places at the DRC minimum, routes, and opens a channel only where a net fails or a budget is exceeded, then repeats | ICMD pp. 155–156; D0 |
| R3 | Inputs and outputs | S2's coupling budgets | also a hard rule: an amplifier's input and output nets never run side by side (no shared channel at minimum spacing) | ICMD CS1 pp. 267–268, 275; CS2 p. 351 |
| R4 | Differential pairs | mirrored routing not attempted (G5.4 reports it) | the two nets routed side by side with equal length and the same layers, from a common centre point | ICMD pp. 115–116, 132–134, CS1 p. 318, CS2 pp. 353–355, 380 |
| R5 | Current paths | width from S2 | width from I2; vias as many as fit on current paths; current drawn from a device's centre or both ends, never one corner | ICMD pp. 165–166, CS1 pp. 276–277, 294, CS2 pp. 363–364 |

R1 and R2 pull against D4: routing off the blocks needs channels. The gaps become what the routes need, and the comparison shows the cost.

### S: shared diffusion (later)

- **S1.** Units of one type and body whose facing source/drain nets are equal may abut and share diffusion [ICMD p. 93; TAMU 21; WVU 34; LONG05 §II-B–C].
- This needs a DRC/LVS-signed abutment check first.
- **QUESTION Q5:** now, or after the first comparison?

### Unchanged

- S0–S3, S2's budgets, every DRC/LVS gate and negative control, S6/S7.
- The search settings.

## 4. Where iadc stands now (v1)

- **Blocks:** 67, of which **38** are the designer's dummies, each a single device with its own ring.
- **Area use:** the blocks fill 51 % of the budget-aware layout: 17,135 of 33,889 µm². The hand layout is 13,355 µm².
- **Block shapes:** long rows, up to 154.0 × 10.8 µm.
- **Rules that should shrink it:** Y2, T1, M1/M6, D1–D5.
- **Rules that may grow it back:** R1/R2, T3, and Q9 if the reserve slack is chosen.
- **No area is predicted here:** v2 is run and measured.

## 5. Plan after the review (branch `rules-v2`)

1. **PREREG amendment** with the accepted rules, the hypotheses and Imasha's thresholds (Q7).
2. **Code, opt-in under `ruleset: v2`.** v1 stays the default, and the goldens and tests must pass unchanged.
   1. DRC table;
   2. D;
   3. T;
   4. Y;
   5. M (cross-quad and 2-D generator);
   6. P;
   7. R;
   - each with tests.
3. **iadc v2:** a GUI copy of `iadc_ota` with `ruleset: v2` and Imasha's hierarchy (with I1/I3 annotations), run from the GUI.
4. **Comparison:** v1, v2 and the hand layout, side by side.
   - Area, block fill, DRC/LVS, G6.2 budget use, specs after layout, the wiring's GBW loss, and which pattern each group got.

## 6. Questions for Imasha

- **Q1.** Is the case study you meant *IC Mask Design*'s Case Study 1 (the CMOS amplifier)? Section 2.1 follows it.
- **Q2.** Accept or change each rule (I, D, T, M, Y, P, R, S).
- **Q3.** An outer guard ring round the whole OTA (T4)?
- **Q4.** Pattern choice (M5): score every allowed candidate, or also a size threshold?
- **Q5.** Shared diffusion (S1): now or later?
- **Q6.** `TAP_MARGIN` 0.5 µm inside the 15 µm latch-up limit: keep it (ASSUMPTION) or drop it?
- **Q7.** PREREG thresholds: what area reduction counts as success, and what loss is allowed?
- **Q8.** R1: any crossings besides symmetric ones over a matched block?
- **Q9.** Minimum vs reserve (D0): pure DRC minimum where S2 allows, or the book's slightly-above-minimum reserve? If reserve, how much?
- **Q10.** For iadc, which blocks are *noisy* and *sensitive* (I3)? Please put the matching level (I1) and the tags on the hierarchy drawing. How wide should a noisy block's ring be?

## 7. Imasha's answers (2026-11-05)

| Q | Answer | What it changes |
|---|---|---|
| Q1 | Yes: *IC Mask Design* Case Study 1 | section 2.1 stands |
| Q2 | The rules are good | rules I, D, T, M, Y, P, R, S accepted, as amended below |
| Q3 | Yes, keep an outer ring | T4: one outer guard ring round the whole amplifier |
| Q4 | Do not sign off every candidate: first estimate the area of about 4–5 placements roughly, then keep the best 2–3 for area and routing; brainstorm if this is not good | M5 becomes a two-stage screen, proposed in 7.1, **to agree** |
| Q5 | Allow shared diffusion for fingers, and where the specs allow | S1 enabled: within a device's fingers (as the PCell does) and between devices of one type and body whose facing source/drain are the same net, when S2's budget for that net's capacitance allows it |
| Q6 | Keep `TAP_MARGIN` as needed | D7: 0.5 µm stays (ASSUMPTION, as in v1) |
| Q7 | With a hand layout, the flow should reach **±20–30 %** of its area, not about 200 % as before | PREREG H-v2a: area ≤ 1.3 × the hand layout's (target 1.2 ×), with every spec still met after layout. Caveat: iadc's hand layout also holds its switched-capacitor CMFB, which the flow does not lay out (its bench keeps an ideal CMFB), so like-for-like is *flow area* against *hand area minus its CMFB*; both numbers will be reported |
| Q8 | If a crossing must happen it should be symmetric over every transistor of the block; VDD/VSS crossings are usual but add coupling, so it is a spec, area and routing decision; **for now, allow none** | R1: no other net crosses a block's device area, symmetric or not; a block's own nets only. The symmetric and supply crossings are a later option |
| Q9 | Spacing = DRC minimum plus 10 %, or the nearest larger value on a 0.05 µm grid | D0 reserve: see the two readings in 7.2, **to confirm** |
| Q10 | Normal rings for now; Imasha will upload the hierarchy drawings | T3 not used yet: every stack gets the normal ring (T1), plus the outer ring (T4). Which blocks form a stack, and the matching levels (I1), come from the drawings |

### 7.1 Q4: proposed screening of pattern candidates (to agree)

Agreed in principle: running every candidate through Magic, DRC and LVS is slow, and most are clearly worse. The
proposal, in three stages:

1. **Rough estimate (seconds, no Magic).**
   - For each matched group, the patterns its matching level allows (I1): typically 4–6. For example, for a pair: 1-D `ABBA`, 1-D `ABAB`, cross-quad 2 × 2, 2-row CC, 4-row CC, clustered.
   - Each is estimated from S3's unit-cell sizes and the v2 spacings:
     - outline (area and aspect, and whether it fits the width S5 can offer, e.g. the 161 µm tile);
     - internal routing: the number of tracks or channels, and each net's half-perimeter wire length against S2's budget;
     - the number of crossings;
     - centroid error and dispersion.
2. **Keep the best 2–3 per group.**
   - The cut is a Pareto front over (area, routing estimate), not one weighted sum, so the smallest and the best-routed both survive.
   - **The best candidate of the strictest pattern the matching level asks for is always kept,** even if it is not smallest, because the matching level is a requirement, not a preference.
3. **Sign off only the survivors in S4** (Magic, DRC, LVS, as now). S5 then chooses among them with its existing cost.

Two checks, so the screen cannot mislead silently:
- each survivor's estimated area is compared with its signed-off area, and the error is reported;
- if the estimate's error exceeds 15 %, a third candidate is added (ASSUMPTION: the 15 % is a proposal).

**Where this could be wrong:**
- The estimate is per group. The total area also depends on how S5 packs the groups. That is why 2–3 candidates, not one, go forward.
- The estimate cannot see parasitics. S6/S7 still measure them.

### 7.2 Q9: the two readings of "10 % more, or the nearest larger 0.05 µm"

| Rule | DRC min | DRC × 1.10 | (a) 1.10 × min, rounded up to 0.05 | (b) next 0.05 above min |
|---|---|---|---|---|
| diff/tap.3 diffusion spacing | 0.270 | 0.297 | 0.30 | 0.30 |
| diff/tap.8 n-well enclosure of p-diff | 0.180 | 0.198 | 0.20 | 0.20 |
| diff/tap.9 n-diff to n-well | 0.340 | 0.374 | 0.40 | 0.35 |
| diff/tap.10 n-well enclosure of n-tap | 0.180 | 0.198 | 0.20 | 0.20 |
| diff/tap.11 p-tap to n-well | 0.130 | 0.143 | 0.15 | 0.15 |
| nwell.2a n-well spacing | 1.270 | 1.397 | 1.40 | 1.30 |
| poly.2 poly spacing | 0.210 | 0.231 | 0.25 | 0.25 |
| poly.4 poly to diffusion | 0.075 | 0.083 | 0.10 | 0.10 |
| li.3 li spacing | 0.170 | 0.187 | 0.20 | 0.20 |
| met1.2 / met2.2 spacing | 0.140 | 0.154 | 0.20 | 0.15 |
| met3.2 / met4.2 spacing | 0.300 | 0.330 | 0.35 | 0.35 |
| capm.2a MIM spacing | 0.840 | 0.924 | 0.95 | 0.85 |
| capm.11 MIM to unrelated met3 | 1.340 | 1.474 | 1.50 | 1.35 |

- Reading (a) always keeps at least 10 %, and up to 43 % on met1/met2 (0.14 → 0.20).
- Reading (b) keeps less where the minimum is already near the grid (nwell 1.30, capm.11 1.35).
- The proposal is (a). Applied to spacings and enclosures only:
  - widths stay at the DRC minimum or the current-based width (I2);
  - the latch-up limits (LU.2/LU.3) are maxima, handled by `TAP_MARGIN`.
- **To confirm.**
