<!-- Copy of the claude.ai project doc `claude/10_status_eta09_pole_fix.md` (project "Layout automation"), mirrored on 2026-10-27 so that Claude Code can read it. The project copy is the original. -->

# Status: stress at η = 0.9, the pole drop-out fix, and decisions (2026-10-25, night)

**Repository:** `C:\Users\suind\Documents\GitHub\layout-automation-s0-s3`, commit **8439ab3**.
**Living record:** `docs/flow_record.md`, with sections 3.9, 4.5, 5.5, Supervisor review 3 and 6.
**Slides:** the deck artifact "PCell-Exact Analog Layout Flow S0–S9", version 6. It now has 19 slides, including a results section.

## Decisions (from Imasha)

- The stress variant uses **η = 0.9**: package key `eta: 0.9` in `inputs/ota5t_stress/package.yaml`.
  - `src/s2/run.py` reads η in this order: the `--eta` flag, then the package key, then the default 0.5.
  - It records `eta` and `eta_source` in `budgets.json`.
- **EM is ignored for now.** The EM rules stay `not_evaluated`.
- **S3 is on hold** as it is.
- **S4 starts Monday 2026-10-26.**

## Stress design at η = 0.9

**S2: PASS.**

- Budgets ≈ 0.948 × need: phase 1 gives 0.998, then phase 2 trims 5 %.
- SPICE verification uses 0.84 of the GBW margin and 0.74 of the PM margin.
- Rules: OUTP met1 ≤ 9.1 µm; net3 proximity 9.3 µm; OUTP~net3 parallel run ≤ 12.2 µm.

**S3: G3.3 PASS, G3.5 FAIL.**

- **Input pair:** nf4_gtop_sdfull_outS, 61.1 → 36.3 µm².
- **PMOS mirror:** keeps the default cell. Its source R is 27.3 Ω against 25.9 Ω allowed. No option has a lower source R; R19 (below) is the cause.
- **Tail:** keeps the default cell. The nf4 options have a lower source R, but they re-size the tail (W bin, about −3 % Id) and cost 6.7 MHz of GBW against a 0.12 MHz allowance.
- **In the circuit:** GBW 369.2 MHz, PM 63.65°, gain 32.22 dB. Device area 256.6 → 206.9 µm².

**R19 (open; decide before S4 uses budgets).** S2's phase-2 proportional fairness takes budget from the binding elements to inflate negligible-rate elements up to κ. Proposed fix:

- (a) a phase-2 floor at min(phase-1 budget, need);
- (b) lower bounds per element from the option library's minimum achievable cell value.

## The pole drop-out problem and the input-side fix

**The problem.** The upstream level-2 template keeps the DC value of the mirrored path but drops its dynamics; Ioutn→Ioutp is listed as "missing" in the file. The mirror pole is ≈ 313 MHz: R1_X1 = 4.36 kΩ, C2_X1 + C5_X1 = 116.5 fF.

- **Correction:** the earlier 614 MHz figure was wrong (R20). It came from the DC driving-point R, which includes the loop through the output.

**The fix** is in `src/s1/symbolic_patch.py`. It writes patched **copies** to `inputs/example_ota_5t/upstream_patched/`; the original is unchanged.

- **P1, mirror doublet**, using only symbols already in the file:
  - `Gm(s) = G2_X1_X2 + (G2_X1 − G2_X1_X2)/(1 + s·τm)`
  - `τm = R1_X1·(C2_X1 + C5_X1)`
- **P2:** P1 plus the transcapacitance `gm(s) = gm − s·Cm`, with `Cm ≈ (2/5)·Cgs`.

**Results** (PM / GBW):

| Model | Stress | Example |
|---|---|---|
| Upstream original | 90.6° / 493.7 MHz | 91.3° / 108.4 MHz |
| P1 | 73.2° / 373.6 MHz | 82.8° / 104.4 MHz |
| P2 | 65.2° / 363.7 MHz | 80.2° / 104.0 MHz |
| SPICE | 65.1° / 373.7 MHz | 80.9° / 104.5 MHz |

- The CL and net3 sensitivities now match the SPICE finite differences.
- **Fair accuracy of P2:** about ±1.5° in PM. With Cm taken from the OP instead, the stress PM is 66.3°.
- The S1 gates still use the original file.

## Open items for Monday

1. Apply the R19 fix?
2. An offset spec.
3. The variation-range format.
4. The S4 template generators: diff pair (ABAB, ABBA, common centroid, dummies), mirror, tail.

Also open: the symbolic gain is 0.33 dB low (R22, not diagnosed).
