<!-- Copy of the claude.ai project doc `claude/08_status_S0_S1.md` (project "Layout automation"), mirrored on 2026-10-27 so that Claude Code can read it. The project copy is the original. -->

# Status after S0 + S1 (2026-10-25)

**Repo:** `layout-automation-s0-s3`, local only, at `C:\Users\suind\Documents\GitHub\`.

- **Commits:** `a12ba26` (S0 G0.7 + S1 + flow record), then `7505908`.
- **Living record:** `docs/flow_record.md`, with pictures in `docs/flow_record/img/`. For each stage it gives the inputs and outputs, JSON excerpts, DRC/LVS evidence and the problems met. Update it at every stage.

## Gates

| Stage | example_ota_5t | ota5t_stress (CL 200 fF, tight margins) |
|---|---|---|
| S0, G0.1–G0.6 (ingest, freeze, round-trip LVS, exact testbench reproduction) | PASS | PASS |
| S0, G0.7: each device drawn by its SKY130 Magic PCell at exact W/L/nf/m; DRC 0; LVS match, no property errors; both negative controls behave | PASS (5/5) | PASS (5/5) |
| S1, G1.1–G1.4 | PASS | PASS |

## S1 key numbers

- **Linear model vs SPICE:**
  - gain −0.004 dB;
  - GBW +0.5 %;
  - PM +0.01° (example) / +0.02° (stress).
- **Sensitivities vs SPICE finite differences (derivative compared with the zero-step extrapolated slope):** worst 1.0 % for the example. For the stress design all are ≤ 2.4 %, except one near-zero slope (net3 → PM) at 17.6 %.
- **Stress budgets, first-order fF that use up a margin:**

  | Element | fF |
  |---|---|
  | OUTP~net3 | 12 |
  | OUTP~INP | 25 |
  | OUTP to ground | 30 |
  | net3~INP | 35 |
  | net3 to ground | 43 |

  All of these are limited by GBW.
- **Tail headroom:** XM5 is 19.6 mV inside saturation at 84.8 µA. S2 needs an IR-drop budget for net1 and for XM5's VSS connection.
- **Upstream symbolic model:** PM optimistic by +10° (example) and +25° (stress), because the mirror node is missing; d(GBW)/dCL is −2.19 against an actual −1.24 MHz/fF. This is the measured cost of the missing Ioutn→Ioutp term (needed for N2).

## G1.3 criterion change, made openly

- **Before:** the slope had to be within 20 % of the secant slope at +20 fF.
- **Now:**
  - the derivative is compared with the SPICE slope extrapolated to zero step, (4·s5 − s20)/3;
  - the first-order prediction error at +20 fF is reported as a fraction of the margin (≤ 5 %).
- **Reason:** curvature dominates near-zero slopes.

## Next

1. **S2:** joint LP budgets (N1) from `intent.json` / `sensitivity.json` / `currents.json`. Verify the joint budget with SPICE, with all budget capacitances inserted at once. Add an IR budget for the tail. Add EM widths (the EM limit source is still pending from Imasha).
2. **S3:** PCell option table (guard, contact coverage, …) and per-device decisions, each device redone with DRC/LVS evidence.

## Working notes

- Committing a file to the PC does not overwrite an existing file, and re-sending a reused name delivered a stale copy. Always upload under a new name to `.incoming/`, check the md5, then move it inside the container.
- git runs inside the container as root, followed by `chown 1000:1000`.
- One Docker job at a time.
