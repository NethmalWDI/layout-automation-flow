<!-- Copy of the claude.ai project doc `claude/09_status_S2_S3.md` (project "Layout automation"), mirrored on 2026-10-27 so that Claude Code can read it. The project copy is the original. -->

# Status after S1-ext, S2 and S3 (2026-10-25 evening)

**Repo:** `C:\Users\suind\Documents\GitHub\layout-automation-s0-s3`, local only.

- **Commit:** `4cf69ba`, followed by a trivial `6aca6a3`.
- **Living record:** `docs/flow_record.md`.
- **Pipeline order:** S0 → S1 → S3 `--cells-only` (option library, design independent) → S2 → S3 decisions.

## Gates

| Stage | example_ota_5t | ota5t_stress |
|---|---|---|
| S1 (G1.1–G1.6, incl. resistance) | PASS | PASS |
| S2 (G2.1–G2.6) | PASS | PASS; G2.0: a compact layout with the default cells would use 90 % of the GBW margin and 66 % of the PM margin |
| S3 | PASS | FAIL, flagged: no option fits η = 0.5; specs still met with the default cells; the cells alone use 46 % of the GBW margin and 53 % of the PM margin |

## Key results

**Resistance (S1).** Half of the series-R effects are bias shifts I·R. They are confirmed by re-solving the linear model at the operating point SPICE finds with the resistor. S2 therefore takes R rates from SPICE.

**PDK interconnect (measured with Magic):**

| Quantity | Value |
|---|---|
| met1 resistance | 0.893 Ω/µm |
| met1 capacitance, over field | 84.8 aF/µm |
| met1 capacitance, over li1 | 158 aF/µm |
| met1 coupling at min spacing | 56 aF/µm |
| pdiff licon | 585 Ω per contact |
| ndiff licon | 185 Ω per contact |

**S3 option library.** 84 cells: Magic PCell plus our met2 finger straps. 80 pass DRC and LVS (W/L/nf) with negative controls. 4 PMOS nf = 8 cells with 50 % coverage: "strap does not fit".

**Example design decisions:**

| Devices | Chosen | Area (µm²) |
|---|---|---|
| PMOS mirror | nf2, gate top | 30 → 25 |
| Input pair | nf2, gate top | 61 → 43 |
| Tail | nf4, gate top, 50 % coverage | 74 → 52 |

- Device area −27 %.
- In-circuit with access R: GBW −2.6 MHz, PM −1.1°, within the allowances.
- The tail at nf = 4 changes XM5's current by −3 %, through the SKY130 W bin. This is a re-sizing effect, reported in `device_model_change`.

## Bugs found by supervisor review

- A floating Magic VSUBS node caused a wrong operating point via gmin stepping. Now caught: any ngspice numerical warning fails the run.
- Gates could pass on missing data.
- The S2/S3 allocation was inconsistent: the expected need now includes the measured default cells.

## Open items

**Waiting on you:**

- EM data;
- an offset spec;
- variation ranges;
- the bias impedance;
- the decision on η for the stress variant (about 0.9, or relaxed specs, or layout-aware re-sizing).

**Next:**

- S4 templates (diff pair, mirror) from the S3 cells;
- LOADBench packages;
- an η sweep;
- a limit on device-model changes in S3.
