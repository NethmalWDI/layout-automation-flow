<!-- Copy of the claude.ai project doc `claude/12_flow_v2_decisions.md` (project "Layout automation"), mirrored on 2026-10-27 so that Claude Code can read it. The project copy is the original. -->

# Flow v2: decisions after the external review (2026-10-26)

Living doc: "Flow v2: decisions after the external review" (Claude Doc). This file is the durable summary.

## Imasha's answers to the 11 recommendations of doc 11

1. **Rewrite the claims.** Yes. The LLM's role is now defined per stage (table below).
2. **A3 per-net injection baseline.** Yes. The explanation is under "Why joint vs per-net".
3. **Corners and mismatch.** Yes.
4. **Real circuits.** Run fully differential OTAs plus the existing 5T OTA. Run S0–S3 unchanged first ("before"), then apply the updates, then re-run ("after").
5. **R19 fix and cell floors.** Implement.
6. **Merge S3 and S4?** Analysed critically by an independent supervisor agent. Decision: **restructure, don't merge** (see below).
7. **Strengthen N3.** Do it, with the reasons, pros and cons stated.
8. **Validate access R by extraction.** Agreed.
9. **Baselines.** Agreed, and find other easy ones (see below).
10. **Independent verification.** Keep it and add more practices (see below).
11. **Ask other groups for code.** Not answered.

## LLM role, S0–S4

The LLM proposes; deterministic checks accept or reject; every stage also runs with the LLM off.

| Stage | LLM proposes | Never |
|---|---|---|
| S0 | Name maps, port roles, draft upstream files | Changes the netlist, specs or sizes |
| S1 | Mechanism explanations, classes for nets without a model, textbook equations (scored against SPICE) | Computes sensitivities |
| S2 | Relaxations when infeasible, plain-language rules | Sets budgets or η |
| S3 | Nothing | — |
| S4a | Matching policy when there is no offset spec; pruning | Ranks candidates |
| S4b | Generator code | Signs off its own output |

Every LLM call is logged with model, date, temperature and prompt hash. Each call is repeated at least 3 times. The LLM is evaluated on held-out circuits.

## Why joint vs per-net budgets

**The problem with per-net budgets.** A per-net budget assumes every other net gets nothing.

- On the stress design, five per-net budgets at η = 0.9 together use about 4.5 GBW margins (first-order estimate).
- Joint budgets use at most 0.9 of the margin; SPICE measured 0.84.
- An equal split is safe but starves the critical nets: OUTP would get 1.3 fF against the 2.8 fF the default cells already add.

**The experiment.** A three-outcome figure: unsafe / infeasible / joint.

- The per-net baseline is run with Paper 1's own code (SpiceXplorer `score_c_budgets`, PolyForm-NC licence).
- It needs at least 3 circuits and the PVT corners.
- It is a short-paper result, not a paper on its own, because superposition of degradations is textbook (Choudhury 1992).

## S3/S4: restructure

| Stage | Role |
|---|---|
| S3 Unit library | Design-independent: signed unit cells (with and without guard ring), fitted C/R/area models, W-bin table, LVS negative controls for nf/m/dummies |
| S4a Block planning | Device decomposition (nf, m) and pattern chosen jointly; every candidate scored analytically against the block-port budgets; top-K list |
| S4b Block realization | Generate the top-K plus about 30 random candidates; DRC, two LVS checks (same circuit; as-built), PEX, in-circuit simulation; measure prediction error |

**Modes.**

- **B:** nf and m from the netlist. Degenerate for our nf = m = 1 netlists.
- **B+:** total units fixed, the split is free.
- **A-bin:** free, but the finger width stays in the sized device's W-bin. This is the main research mode.
- **A-free:** ablation only.

**Search size, 5T OTA** (pair / mirror / tail):

| Mode | Candidates |
|---|---|
| A-free | ~1240 / 850 / 380 |
| A-bin | 132 / 12 / 60 |
| B | 12 each |

**Reverse to the PI's full merge if** calibration reaches τ ≥ 0.9, top-3 recall of 100 % and zero false accepts on 3 circuits.

**Checks to add:**

- Netgen nf merging (negative controls).
- ngspice `wnflag` binning.
- A matching policy, since with no offset spec and no LOD/WPE the planner would always pick side-by-side without dummies.

**Effort:** about 4–5 weeks for the library changes, the planner, 3 generators and calibration.

## N3 strengthening

**Changes:**

- A rule-of-thumb folding baseline, with the target finger width fixed before running.
- Block area instead of isolated-cell area.
- A W-bin/model-change cap as a fraction of η × margin.

**Pro:** a fair claim. **Con:** it may shrink to single digits and become a supporting result.

## Corners, mismatch, η

| Stage | Change |
|---|---|
| S0 | 45 PVT points: 5 process corners × VDD ±10 % × −40/27/85 °C |
| S1 | Sensitivities per corner |
| S2 | One constraint per spec and corner. η becomes a model-error reserve, swept from 0.3 to 1.0 |
| Mismatch | 200-run Monte Carlo. Offset rules stay `not_evaluated` until there is an offset spec |

## New circuits (Imasha chose both fully differential designs and LOADBench)

**LOADBench `SimpleTwoStageOpAmp_SimpleOpAmp1_1`** (CC BY 4.0, held-out split).

- Two-stage Miller, PMOS input, LVT devices, PMOS bodies tied to source.
- Has: about 1000 Pareto sizings, OP/AC/DC/tran testbenches, structure/partition XML.
- Missing: specs, noise testbench, symbolic model.
- Testbench conditions: 1.8 V, 1 pF load, 10 µA bias.

**Stanford iadc OTA** (github.com/r09g/iadc, MIT).

- Fully differential folded cascode with switched-capacitor CMFB.
- Built from 1.4/0.6 µm unit transistors.
- Hand-drawn Magic layout with common centroid and dummies; LVS and PEX netlists included.
- AC analysis uses an ideal-CMFB testbench.

**Imasha's TTSKY25a fully differential op-amp** (NethmalWDI/Fully_differential_opamp, Apache-2.0).

- Two-stage fully differential: folded cascode plus a common-source stage, one CMFB per stage, beta-multiplier bias, about 80 devices.
- Layout is in GDS only, inside the Tiny Tapeout tile. Fabricated.
- Post-layout values: ≈ 100 dB, 2.3 MHz, PM ≥ 52°, CMRR ≈ 91 dB, ≈ 500 µW.

**Rejected:**

- CNR_OTA (wulffern): no layout, no licence.
- AMS-SizingBench: unsized, no CMFB, no licence.

**Predicted inputs.** Hierarchy, primitives, name map and textbook symbolic models are built by us, labelled `provenance: predicted`. G1.5 scores them against SPICE.

## Baselines, ranked by value / effort

1. Per-net injection budgets (SpiceXplorer code).
2. Ablations of our own flow.
3. Choudhury/Charbon LP/QP on our sensitivities.
4. Equal split.
5. Topology-only constraints.
6. RALF (SKY130 Magic PCells).
7. gLayout (MIT; blocks with common centroid and interdigitation).
8. The hand-drawn reference layouts (iadc, TTSKY25a).

**Lower priority:**

- PANDA-style LLM labelling.
- ALIGN, only for L = 0.15 µm designs.

**Not runnable:** MAGICAL, BAG3, Open-ALOE, AICL.

## Practices to add

1. PREREG.md, tagged before the baselines run.
2. A held-out circuit split.
3. Equal simulation budget for every method.
4. Golden regression tests.
5. Cross-tool sign-off: KLayout DRC/LVS and kpex next to Magic/Netgen.
6. PVT corners and Monte Carlo.
7. An ablation matrix.
8. 10 or more seeds, with confidence intervals.
9. Cost reporting.
10. LLM hygiene and leakage control.
11. Licence hygiene (THIRD_PARTY.md) and a threats-to-validity section.
12. Our own budget-soundness test: random parasitic sets up to the budgets at the worst corners.

## Repo

**Location:** github.com/NethmalWDI/layout-automation-flow (private). Pushed through the GitHub connector, never force-pushed.

**Usage:**

- `./flow run <design> [--stage Sx]` runs a design, or one stage.
- `./flow test [--stage Sx]` runs the unit and golden tests.
- `inputs/_template` plus `docs/INPUTS.md` describe how to add a new design.

**Content and licensing:**

- Everything is committed: code, tests, inputs, outputs, logs and docs.
- Unlicensed sources are fetched at run time, never committed.
