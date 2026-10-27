# 14. Plan v3: circuit review pack and implementation plan (2026-10-27, evening)

Live document: Claude Doc "Plan v3: circuit review pack and implementation plan"
(https://claude.ai/artifact/R15Aj6FzDVKxcYwLT1WAr5). Repo copy: `docs/plan_v3_review_pack.md`, figures in
`docs/plan_v3/img/`. Flow record 7.12 and journey rows 46–50. Documentation only: no runs, no code changed.

## Imasha's direction (after plan v2)

Budget at middle corners and report the extremes; release the schematic-to-layout allowance realistically (sizing
owns robustness); predict the layout's problems, then diagnose after one extraction; budget only critical nets
and nodes; S3 finds a good candidate primitive (a "suspect" when only least-bad) and the combination search moves
to S4; any LLM decision needs guardrails against invented values and endless search.

## Assessment (supervisor view)

- Adopt all six; the two that matter most are the released allowance (Option B: eta × nominal margin per corner,
  with each corner's own sensitivities) and predict-then-diagnose.
- Proposed thesis claim: a pre-layout contract between sizing and layout. (1) S2 states before layout whether the
  schematic leaves layout a realistic allowance, else returns a quantified request to sizing ("schematic-owned").
  (2) A frozen, scored suspect list of nets and net pairs. (3) After one extraction, attribution to the suspects,
  confirmation by selective back-annotation, iterations to closure counted. The budget-allocation rule becomes an
  implementation detail (plan v2: equal split ≈ ours on held-out designs). Needs a literature check (Choudhury and
  Sangiovanni-Vincentelli 1992/93, Charbon/Malavasi 1994–96, Lourenço DATE 2015, ALIGN, MAGICAL, ParaGraph DAC 2020,
  commercial parasitic-contribution reports).
- LLM: defer until a deterministic S4 works; closed candidate lists, deterministic checks, fixed budgets, ablation.

## Plan v3

A clean the evidence (S3 saturation check relative to the schematic; stale files; dummy tags; recognition
pairings; fair re-scoring; corrected hand models; PM measurement) → B the sizing–layout contract (PREREG amendment
v3: middle-9 set, extremes reported, allowance table, schematic-owned verdict) → C frozen suspect list (topology
tags + top S1 nets and pairs; budgets on suspects only; calibration on the two existing hand layouts, post hoc) →
D S3 ≤ 3 good cells per device, bounded block search in S4 → E one extraction, attribution, at most one fix
iteration; scored by suspect recall at k (ground truth: remove each net's extracted parasitics), prediction error,
iterations, run time.

## Circuit findings

| | LOADBench | iadc | TTSKY25a |
|---|---|---|---|
| Hand model misses | mirror doublet (pole ≈ 33 MHz, whole 17° PM gap) | fold current split (M11/M12 in triode, ro ≈ 1/gm cascode) | fold-node pole (≈ fT of L = 5 µm cascode, ≈ 10°) |
| Hand model vs SPICE (GBW, PM) | +29 %, +17° | +98 %, −20° | +14 %, +9° |
| Most critical parasitic (S1) | in2 ↔ outFirstStage 59 fF (PM) | op ↔ on 27 fF (GBW) | fold ↔ fold 108 fF (PM) |
| Middle corners the schematic misses (package rule) | 2 of 9 | 2 of 9 | 6 of 9 |
| Recognition | fine | dummy tags; `cm` stacks read as pairs | cascode pairs swapped; CS pair missing |

Also: PM is measured from the 1 Hz phase, so TTSKY25a reads 2.3° high (≈ 75.9°, margin ≈ 16°). iadc's upstream
schematic has a Performance Summary (53.7 dB, 70°, 344 MHz) that our operating point reproduces without C3/C4.
The TTSKY25a tile's own capacitance-only extraction loses ≈ 3° of PM; the paper's 52° is unexplained.

## Decisions waiting (D1–D10)

Corner set; allowance rule; allowance values and eta; specs for designs without upstream specs; suspect selection
rule (share, k); iadc reference (with or without C3/C4); TTSKY25a calibration now; CMFB loop check; Phase A fixes;
LLM deferral. Details: `docs/STATUS.md`, Open questions.
