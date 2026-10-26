<!-- Copy of the claude.ai project doc `claude/11_external_review_papers_and_flow.md` (project "Layout automation"), mirrored on 2026-10-27 so that Claude Code can read it. The project copy is the original. -->

# External review: Noori Zadeh et al. (multi-agent nanowatt LPF), AICL Co-pilot, related work, and our flow

**Date:** 2026-10-25
**Living doc:** Claude Doc "External review: AI analog-layout papers vs. our PCell-exact flow" (the full version, with a 2x2 positioning diagram).
**Papers read in full** from `Layout_Automation_LLM\literature`: `2610.28677v1.pdf`, `AICL_Co-pilot_...pdf`, plus PANDA, ICPI, Vibe Tapeout, Open-ALOE and PAPlace.

## Verdicts (as a journal reviewer)

| Work | Recommendation | Main reason |
|---|---|---|
| Noori Zadeh, Prasad, Elamien, arXiv 2610.28677 (McMaster, 19 Oct 2026, 5 pp) | Major revision | See the five reasons below |
| AICL Co-pilot, Bio/Sondón/Sturm/Pretl, SMACD 2026 (JKU) | Tool demo; weak as research | See the four reasons below |
| Our S0–S3 flow (commit 8439ab3) | Not yet publishable | Strong verification; G2.0 is new. But N1 (hierarchical symbolic budgets) and N2 (recomposition) are not implemented, and there is one topology at one corner |

**Why major revision for Noori Zadeh et al.:**

- One design and one run, with no ablations or cost report.
- PEX moved fc by only 0.44 %, so the circuit is not layout-sensitive.
- The parasitic-budget agent is described in one sentence; its method is unstated.
- Only 16 of 45 PVT corners meet all specs.
- The comparison table mixes post-PEX simulation with measured silicon.

**Why AICL Co-pilot is weak as research:**

- There is no electrical evaluation at all.
- The area comparison is TSMC 180 nm manual against IHP SG13G2 automatic, and the 42 % stacking saving is an estimate.
- Symmetry and common-centroid are listed as future work.
- I found no code release.

## Related work map (2024–2026 plus classic)

**Agents decide, tools verify:**

- Noori Zadeh 2026
- Vibe Tapeout (arXiv 2610.15240; SKY130 SAR ADC; agents reported false passes)
- PANDA (DAC 2026; post-layout UGB fell from 10.84 to 4.19 MHz, missing its 8 MHz target)
- AnalogMaster (arXiv 2604.20916; no post-layout check)

**An LLM tunes a deterministic engine:**

- LayoutCopilot (TCAD 2025)
- ICPI (arXiv 2608.13767; GPT-5; 31 PEX runs per design; beats BO)
- LLANA (MAGICAL net weights)

**Generators and placers, no LLM:**

- AICL Co-pilot
- RALF (JKU, SKY130 Magic PCells)
- Open-ALOE (ISQED 2025, SKY130, silicon-measured bandgap)
- GLayout + LLM
- BAG3++
- PAPlace (TODAES 2026)
- Basso et al. (Infineon)

**Prior art for S2:** Choudhury & Sangiovanni-Vincentelli (UCB/ERL M92/38, TCAD 1993), Charbon/Malavasi, and Lampaert/Gielen/Sansen. They derived parasitic bounds from performance sensitivities before layout.

## Similar vs novel (claim verdicts)

**Drop as novelty:**

- Budgets from sensitivities. This is 1992/93 prior art.
- Per-net budgets inside an agentic open-PDK flow. This is Noori Zadeh.
- The LLM copilot as a headline.

**Keep, narrowed:**

- Joint budgets over nets, coupling pairs and terminal R, with DC headroom, all verified at once in SPICE. Must be shown against per-net injection (A3).
- G2.0, a pre-layout feasibility number. This is the strongest new item; it must be shown to predict the S7 outcome.
- PCell options from a measured option table. Needs a rule-of-thumb folding baseline, block area, and the W-bin re-sizing counted as a cost.

**Conditional:**

- Block-port budgets: keep only if S4 judges each variant against them.
- N2: rename it to port-model recomposition with numeric Y-parameters; keep the symbolic form for explanation only.

**Side result:** the upstream mirror-pole diagnosis and fix.

**Defensible thesis:** before any layout, compile margins into joint parasitic budgets that SPICE confirms. From them, predict whether a compact layout can fit. Then use them to choose PDK cells and to judge block variants, with fewer post-layout loops than per-net injection budgets or simulate-and-tune agents.

## Recommendations before S4

1. Rewrite the claims now.
2. Build baseline A3 (per-net injection, then all budgets inserted together, measured in SPICE) before S4. It needs only S0–S2 and is a possible first short paper.
3. Add corners and mismatch to S1–S2. Replace the fixed η with a reserve measured from the PVT spread, and report an η sweep.
4. Add real circuits: two-stage Miller (LOADBench), an FD OTA with CMFB, and a comparator.
5. Fix R19 and add cell floors.
6. Strengthen N3 or drop it.
7. Validate access R by extraction.
8. Design S4 around H2. Use AICL's S-Cell/M-Cell idea, and add symmetry, common-centroid and dummies. Give every variant local PEX, a port-budget check and a full simulation.
9. Add baselines A0 (RALF) and A_gen (a parameterized generator plus a black-box area optimizer, as in Paper 1).
10. Keep independent verification.
11. Ask JKU and McMaster for their code.
