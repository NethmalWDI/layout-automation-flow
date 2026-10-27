# Plan v2 slides (2026-10-27)

The slide deck "PCell-Exact Analog Layout Flow S0–S9" is a claude.ai artifact (private to Imasha; Cowork publishes
it). Version 7 (2026-10-27) adds the section **Plan v2** (15 slides) after the earlier 19. Claude Code cannot open
it, so the slide titles and their one-line messages are listed here. The figures are the `docs/flow_record/img/v2_*.png`
files and `ttsky25a_fd_groups_Diff_opamp` (rendered from the SVG).

| Slide id | Title | Message |
|---|---|---|
| v2-circuits | Three new circuits and what we predicted | LOADBench, TTSKY25a and iadc; predicted inputs labelled; testbenches reproduced |
| v2-groups | The flow's matching groups on your schematic | 23 predicted groups on Diff_opamp; L-ratioed mirrors checked as equal-L subsets |
| v2-generality | Six findings, each now fixed or gated | what the new circuits exposed in S0/S1 (2026-10-26) |
| v2-changes | What v2 changes, stage by stage | PVT and Monte Carlo, floors, R19, PVT constraints, baselines, S3 modes |
| v2-bugs | Six more bugs, found by gates and review | MIM x M, S3 m > 1, triode limits, negative control, solver, scoring |
| v2-gates | Which checks fail, before and after | S0/S1 unchanged; v2's S2 says "does not fit" on 4 of 5; only the 5T passes all |
| v2-s3 | Device area and specs, before, after and post hoc | all specs met except LOADBench 'after'; iadc's S3 is a code artefact |
| v2-loadbench | The rule for relaxed types decided the result | PM 48.1 deg with the old rule, 64.7 deg post hoc (not plan v2) |
| v2-baselines | Five budget rules, scored in SPICE | per-net unsafe everywhere; held out: all infeasible, equal split = ours; TTSKY25a eta 0.9 not valid |
| v2-margins | What binds: corners that barely meet the spec | binding margins 0.014 dB, 0.26 deg, 0.093 dB; 5T corner contradicted by SPICE |
| v2-hypotheses | What the pre-registration asked, and what we found | H1 not in full; H1b half, by construction; H1c holds but tests nothing |
| v2-handlayout | The hand layout, measured the flow's way | TTSKY25a tile: drawn → PEX −6.8 % GBW, −3 deg; the paper's numbers not reproduced |
| v2-g20 | S2's prediction against two hand-drawn layouts | iadc: none within 25 %; TTSKY25a tile: related circuit; G2.0 not calibrated |
| v2-review | What an independent reader found | review C's six main findings; write-up corrected, code fixes open |
| v2-next | Before S4: five things to settle | fix and re-run; margin rule; fair re-scoring; S3 options; G2.0 on own layouts |
