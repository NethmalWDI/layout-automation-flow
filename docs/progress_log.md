# Progress log

## 2026-10-23 — Step 0: full ALIGN flow on SKY130 (before S0–S3 code)

**Environment**

- **Container:** `layout-s0s3`, created from `hpretl/iic-osic-tools:2026.10` (ID 306585de35d1).
  - Created through the `docker-eda` MCP server.
  - The repo is mounted at `/foss/designs`.
  - No ports are published.
- **Tool versions** (from `runs/env/tool_versions.txt`):

  | Tool | Version |
  |---|---|
  | magic | 8.3.685 |
  | netgen | 1.5.324 |
  | klayout | 0.30.12 |
  | ngspice | ngspice-47 |
  | sky130A (open_pdks) | 1689ac3f |
  | Python | 3.12.3 |

- **ALIGN install:** `align-analoglayout==0.9.8`, in its own venv at `/opt/venv-align` (inside the container only; the image is untouched).
  - The full freeze is in `runs/env/requirements-align.lock.txt`.
  - It needed apt packages `coinor-libcgl1`, `coinor-libcbc3.1` and `coinor-libosi1v5`, plus **`python3-dev`**.
  - Issue: gdspy has no cp312 wheel and needs `Python.h`. The first install attempt failed on this; it is fixed in `scripts/setup_align.sh`.
- **ALIGN-pdk-sky130:** commit `3da43f0c22a4d6e2314a6bd4682ff938bb01a0ea`, cloned to `external/` (git-ignored).

**Smoke test: ALIGN's own `five_transistor_ota` (unmodified example)**

- **ALIGN run:** exit 0. Output `FIVE_TRANSISTOR_OTA_0.gds` is 36.5 × 43.0 µm (1571 µm²) and has 3 primitives: DP_NMOS_B, SCM_NMOS, SCM_PMOS.
- **Magic DRC** (`sky130A.magicrc`, `drc(full)`, euclidean, run on the flattened layout): **0 errors.**
  - Negative control: a 0.05 µm met1 sliver is flagged (1 error), so the checker is live.
  - The GDS layers 100/5, 235/5 and 104/0 that ALIGN writes are unknown to Magic and are skipped (boundary/annotation layers).
- **Netgen LVS** (`sky130A_setup.tcl`): **"Circuits match uniquely"**, with 300 devices and 208 nets.
  - The reference was expanded to explicit series and finger devices, because ALIGN realises `stack=3` as 3 series transistors per finger (`ref/five_transistor_ota_ref_expanded.spice`).
  - Two fixes were needed:
    - **Units:** the reference must be in µm (xschem/sky130 convention). In metres, netgen reports 200 % property errors.
    - **Ports:** Magic needs `port makeall`, otherwise the extracted cell has no pins.

**Our design: sized `example_ota_5t`**

- **Source:** copied from `llm-analog-sizing-hierarchical-optimization/results/example_ota_5t/`. SHA-256 hashes are in `circuits/SOURCE_SHA256.txt`.
- **Conversion** (`scripts/make_align_input.py`; report in `runs/align/inputs/ota5t/conversion_report.json`):
  - V1 (0.75 V) was removed, and its node is exposed as port `vbias`.
  - **ASSUMPTION, ALIGN only:** widths are legalised to an even NF × k fins × 0.21 µm, with 2 ≤ k ≤ 12. The limit is ALIGN `mos.py`: `(28 − k)/2 ≥ 8`, `k > 1`. Results:

    | Device | Reference W | ALIGN W | NF × fins | Error |
    |---|---|---|---|---|
    | M1, M2, M5 | 24 µm | 23.94 µm | 38 × 3 | −0.25 % |
    | M3, M4 | 8 µm | 8.40 µm | 4 × 10 | **+5.0 %** |

  - **Deviation from what was approved:** the approved values 24.15 µm and 8.19 µm are **not legal** in ALIGN. 115 and 39 fins are odd numbers, but ALIGN asserts an even NF. A first try at 19 fins per finger failed the `mos.py` height assertion.
  - **Limitation:** ALIGN-pdk-sky130 draws a **fixed 0.15 µm gate** (`layers.json` Poly Width = 150 nm). L = 0.5 and 1.0 µm **cannot be represented.**
- **ALIGN run:** exit 0. Output `OTA5T_0.gds` is 46.8 × 23.7 µm (1110 µm²) and has 3 primitives: DP_NMOS_B (M1/M2), NMOS_S (M5), SCM_PMOS (M3/M4). Picture: `runs/align/A0_ota5t_baseline/OTA5T_0.png`.
- **Magic DRC:** **0 errors** (negative control flagged).
- **Netgen LVS against the original sized design** (`ref/ota5t_design_ref.spice`):
  - **Topology and pins match uniquely** (5 devices, 8 nets).
  - **Property errors:**
    - **L:** 0.15 µm drawn, against 0.5 µm (pair) and 1.0 µm (load and tail).
    - **W:** the load is 8.4 µm against 8 µm (+4.9 %).

**Conclusion**

- The open ALIGN → SKY130 → Magic/Netgen flow works end to end. It is DRC-clean and LVS topology-clean on both circuits.
- For our sized OTA, however, the layout is **not electrically equivalent**: every gate length is wrong.
- **Decision input for S3:** stock ALIGN-pdk-sky130 cannot be the device generator for designs with L ≠ 0.15 µm. This confirms the Phase 2 recommendation of gLayout for S3. Alternatively, ALIGN's MOS generator would need an L-aware patch.

**Open issue**

- **MAGICAL image pull:** `jayl940712/magical:latest` did not complete through MCP. The `docker run` call blocks for longer than the 60 s bridge timeout.

**MAGICAL (in parallel)**

- **Source:** cloned into `external/MAGICAL` (git-ignored) at commit `199ab0719f85f74c79bf85a556118b132988a5fe`. Submodules:

  | Submodule | Commit |
  |---|---|
  | ConstGen | 6e1532d |
  | IdeaPlaceEx | a727c34 |
  | anaroute | 9ef33c2 |
  | device_generation | 4b4bd1f |

- **Image:** `jayl940712/magical:latest` is **not pulled yet**. The MCP `container_create` call blocks during the pull and times out at the bridge's 60 s limit.
- **Action needed from you:** run `docker pull jayl940712/magical:latest` once in PowerShell.
- **Next steps once the image is there:** create `magical-s0s3` → run `build.sh` (pip-builds the C++ components) → `examples/ota1/run.sh` on the mock PDK.

## 2026-10-23 (late): MAGICAL running on its mock PDK

**Setup**

- **Image:** `jayl940712/magical:latest`, ID f5e8909673c9, **7.38 GB**. This is larger than the earlier estimate.
- **Container:** `magical-s0s3`, with the repo mounted at `/work`. The image is Debian 8.
  - `python` is Python 2.7; MAGICAL needs `python3`, which is 3.7.
  - Note: the upstream `run.sh` calls `python`, so it fails here with `No module named magicalFlow`. Use `python3 ../../flow/python/Magical.py <cfg>.json` instead.
- **Build:** `build.sh` (pip-builds device_generation, ConstGen, IdeaPlaceEx, anaroute and magicalFlow) runs on a copy in `/opt/MAGICAL` and took about 10 minutes. The package freeze is in `runs/env/requirements-magical.lock.txt`.

**ota1 (upstream example, mock PDK)**

- MAGICAL finished with exit 0 in 31 s.
- Output: `Core_test_flow.route.gds`, 75.0 × 30.7 µm. Copied to `runs/magical/ota1_mock/`.

**Our sized OTA (mock PDK)**

- **Input:** generated by `scripts/make_magical_input.py`. Spectre syntax; nch/pch; W/L/nf exactly as in the design (24u/500n, 8u/1u, 24u/1u); V1 removed, with VBIAS made a port.
- **Run:** MAGICAL finished with exit 0 in 4 s.
- **Output:** `ota5t.route.gds`, 13.4 × 30.9 µm. Picture: `runs/magical/A0_ota5t_mock/ota5t.route.png`.
- **Constraints MAGICAL generated automatically:**

  | File | Content |
  |---|---|
  | `ota5t.sym` | {M1, M2}, {M3, M4}, M5 self-symmetric |
  | `ota5t.symnet` | {INP, INN}, net1 and VBIAS self-symmetric |

  This independently agrees with the matching groups our hierarchy implies, and is a useful cross-check for S1 (T1.1).
- **Caveat:** mock-PDK geometry. It is **not** SKY130, and no DRC or LVS is possible on it.

**Plan:** `docs/03_plan_S0-S3.md` is written and awaiting approval.

## 2026-10-25 — S0 implemented and passing (example_ota_5t + stress variant)

**Folder move.** The source folder moved to `Desktop\01_Research_Projects\Layout_Automation_LLM`. Access was granted again. The SHA-256 hashes of the sources match the copies in `circuits/`.

**ALIGN example batch (from 23 Oct, now committed):**

| Example | Result |
|---|---|
| five_transistor_ota | DRC 0 |
| current_mirror_ota | **DRC 50** |
| telescopic_ota | **DRC 8** |
| buffer, inverter | killed by out-of-memory (exit 137) |
| umich_test_case | failed |

This is more evidence against ALIGN as our SKY130 engine.

**Code**

| Path | What it does |
|---|---|
| `src/common/spice.py` | Strict parser/writer. Supported elements: X-MOSFET (sky130 models), V, R, C. Anything else raises an error. |
| `src/common/tools.py` | ngspice/netgen runners and provenance |
| `src/s0/ingest.py` | The S0 stage |
| `inputs/<design>/package.yaml` | Design-package contract |
| `inputs/example_ota_5t/name_map.yaml` | Name map onto the 5t-ota hierarchy |

**Tests**

- `tests/test_s0.py`: 11 unit tests, including negative ones. Rejected inputs: unknown model, missing W, dangling net, duplicate name, unsupported element, wrong name map.
- `tests/test_s0_integration.py`: LVS round-trip, which must also *detect* a rewiring and a W change.

**Results** (`outputs/S0/<design>/s0_report.json`)

| Gate | example_ota_5t | ota5t_stress |
|---|---|---|
| G0.1 inventory (5 FETs + V1) | PASS | PASS |
| G0.2 validation | PASS | PASS |
| G0.3 hash freeze | PASS | PASS |
| G0.4 name map (3 blocks; bias block flagged as manual ASSUMPTION) | PASS | PASS |
| G0.5 round-trip LVS (IR-written netlist vs original, 6 devices / 8 nets, "match uniquely") | PASS | PASS |
| G0.6 testbench reproduction (IR netlist in the upstream AC/OP/NOISE decks) | PASS, exact to all digits: 31.697 dB, 104.455 MHz, 80.9348°, 84.7774 µA, 339.064 nV/√Hz | PASS (generated) |

**Negative control.** Rewiring XM4's gate to INP makes the round-trip LVS FAIL (`runs/S0_negctl`), so the checker is live.

**Stress variant** (CL = 200 fF, ASSUMPTION-labelled specs):

| Spec | Achieved | Margin |
|---|---|---|
| Gain | 31.697 dB | 0.5 dB |
| GBW | 373.65 MHz | 37.4 MHz (spec ≥ 336.3) |
| PM | 65.08° | 5.0° (spec ≥ 60.08) |

Layout parasitics will now consume a visible share of the margin, which is the purpose of this variant.

**LOADBench, fetched without the 15 GB download**

- `scripts/loadbench_fetch.py` uses `remotezip` 0.12.3 in `/opt/venv-tools` (container only) with HTTP range requests.
- **Index:** `TwoStageOpAmps.zip` has 554 entries and is 14.97 GB, of which about 350 MB per topology is `all_sims.zip`.
- **Fetched:** only the small files for 4 two-stage topologies (1_1, 5_2, 33_7, 72_1), **3.8 MB in total**, into `circuits/loadbench/`:
  - parameterised netlist + testbench (`example_run/CombinedTestBench.cir`, `params.cir`);
  - 1024 Pareto sizings (`FinalPOFfull.csv`);
  - hierarchy: `struct_recognition.xml` (diff pairs, mirrors, arrays) and `partitioning.xml` (stages, load, bias).
- **Notes:**
  - The devices use `*_lvt` models and `m=` multipliers.
  - Some Pareto widths reach hundreds of µm.
  - Turning these into design packages (parameter substitution plus hierarchy from the XML) is the next S0 extension.

## 2026-10-25 (afternoon) — G0.7 PCell binding, S1 implemented and passing, living flow record

**G0.7: every device drawn by its SKY130 PCell (both designs)**

- `src/s0/pcell_binding.py` and `src/common/pcell.py` draw each device with `magic::gencell sky130::sky130_fd_pr__{n,p}fet_01v8` at its exact W/L/nf/m (default options).
- Each device is then checked:
  - Magic DRC: 0 errors on XM1–XM5. The met1-sliver negative control is flagged each time.
  - Netgen LVS against the device's own netlist line: "Circuits match uniquely", no property errors. A reference with L + 0.1 µm is rejected each time.
- The extracted AD/PD/AS/PS equal the values in the sized netlist.
- Fix: device-level LVS uses `LVS_MODE=subcell` in `scripts/magic_lvs.sh`. In top-cell mode Magic prefixes the pins (`M1_pc.D`), which gave a false failure.

**S1 (`src/s1/`): operating point, exact linear model, sensitivities, intent**

| Gate | example_ota_5t | ota5t_stress |
|---|---|---|
| G1.1 operating point: all saturated, Isup 84.777 µA; charge matrix conserves charge within 3e-6 | PASS | PASS |
| G1.2 linear model vs SPICE: gain −0.004 dB, GBW +0.5 %, PM +0.01° / +0.02° | PASS | PASS |
| G1.3 sensitivities vs SPICE finite differences, 10 measurable checks per design, worst 1.0 % / 2.4 % (one near-zero slope 17.6 %) | PASS | PASS |
| G1.4 matching groups {XM1, XM2} and {XM3, XM4}, equal size | PASS | PASS |
| G1.5 upstream symbolic vs SPICE (info): PM optimistic by +10.4° / **+25.5°**; mirror node missing | INFO | INFO |

**Findings for S2**

- **Stress-design budgets, first-order fF that use up a margin:**

  | Element | fF |
  |---|---|
  | OUTP~net3 | **12** |
  | OUTP~INP | 25 |
  | OUTP to ground | 30 |
  | net3~INP | 35 |
  | net3 to ground | 43 |

  All of these draw on the GBW margin, so they must be shared out jointly.
- **Tail headroom:** XM5 is only 19.6 mV inside saturation at 84.8 µA, so an IR-drop budget is needed for net1 and for XM5's VSS connection.
- **Non-linearity:** the first-order prediction is conservative for the tightest pair (−3.15 against −2.59 MHz/fF at +20 fF). S2 will verify the joint budget with SPICE.

**Gate criterion change (G1.3), recorded openly**

- **Before:** the linear slope had to be within 20 % of the SPICE secant slope at +20 fF.
- **What failed:** one case in the stress design, net3 → PM. Linear 0.0040 °/fF; SPICE 0.0112 °/fF (+20 fF) and 0.0064 °/fF (+5 fF). The near-zero slope is dominated by curvature.
- **Now:**
  - the linear slope is compared with the SPICE slope extrapolated to zero step, s0 = (4·s5 − s20)/3;
  - a margin-relative criterion is reported alongside: the first-order prediction error at +20 fF must be within 5 % of the margin.

**Other fixes**

- BSIM4 values are read via `let` + `echo`.
- PMOS values come in the device frame; magnitudes are used for saturation.
- A missing work folder for the Bode plot was fixed.
- Coupling pairs for the SPICE cross-check are now picked by the fF that would use up a margin. The earlier choice by |dPM/dC| missed OUTP~net3.
- A file sent to the PC under a reused name arrived as the old version. Uploads now use new names and are md5-checked.

**Documentation**

- `docs/flow_record.md` is the living record: inputs/outputs per stage, JSON excerpts, DRC/LVS pictures, problems.
- Pictures are in `docs/flow_record/img/`, made by `scripts/make_record_figures.py`.

## 2026-10-25 (evening) — S1 resistance extension, supervisor review 1, S2 and S3 implemented

**Where the repo is.** `C:\Users\suind\Documents\GitHub\layout-automation-s0-s3`. The Explorer "Documents" shortcut may open OneDrive\Documents instead. Shortcuts are in `Desktop\Layout_automation`.

**S1 extension: series resistance at device terminals**

- Terminal groups are matched-pair variables, e.g. `XM1+XM2.s`.
- Linear model with node splitting, and SPICE at 20 and 100 Ω for AC, NOISE and DC headroom.
- G1.6 passes on both designs (16/16 and 20/20 checks):
  - 4–5 effects are small-signal;
  - 12–15 are bias shifts, each confirmed by re-solving the linear model at the operating point SPICE finds with the resistor in place.
- Offset of a one-sided resistor, measured in a follower bench: about 50 µV/Ω at the pair sources, about 15 µV/Ω at the mirror sources.

**Supervisor review 1.** I reviewed my own work, then had an independent agent review the code; the full table is in `docs/flow_record.md`. Main fixes:

- Gates that could pass when a simulation failed.
- S2 verification now uses harmful parasitics only, per check, against η·margin, with a closure iteration.
- The S3 allowance is now expressed in S2's own terms.
- The offset/gain artefact of the open-loop bench.
- Silent zeros.
- Supply trunk currents.
- Conservative per-µm capacitance.
- κ cap on budgets.
- A phase-2 proportional-fairness refinement of the budgets.

**S2** (`src/s2/`):

- **PDK parasitics measured with Magic test wires.** For met1: 0.893 Ω/µm; 84.8 aF/µm over field, 158 aF/µm over li1; 56 aF/µm coupling at min spacing.
- **Allocation.** 21 elements, constraints on gain, GBW, PM, noise and DC headroom, η = 0.5.
- **SPICE verification.** Every check was within η·margin (+10 %) on both designs, with no closure needed. Stress design: GBW used 0.49 of its margin, PM 0.48.
- **Stress budgets are about 1× expected need.** For example OUTP~net3 coupling 0.24 fF, about 4 µm of parallel met1.

**S3** (`src/s3/`):

- 84 option cells: 3 device types × nf, gate contacts, contact coverage and source side.
- Each option cell is a Magic PCell plus met2 finger straps (`strap.py`).
- 80 cells signed off with DRC 0 and LVS match on W/L/nf, each with negative controls. 4 PMOS nf=8 cells with half contact coverage do not pass and are recorded.
- In-circuit evaluation with the cell's own extraction and access R.

**Bug found by checking a suspicious number.** A PMOS cell raised the supply current by 10 µA. The cause: Magic's substrate node VSUBS floats inside the subcircuit, ngspice's gmin stepping then converged to a wrong operating point. Fixed: VSUBS is tied to ground, and every run whose log reports numerical trouble now counts as failed in S1–S3.
- **S2 ↔ S3 consistency (finding R16).** The S3 option library is now built before S2. S2's expected need includes the measured default cells. S3's share of every budget follows that split.
- **G2.0** reports, before any layout, how much of each margin a compact default layout would use:

  | Check | example_ota_5t | ota5t_stress |
  |---|---|---|
  | GBW | 0.06 | **0.90** |
  | PM | 0.08 | **0.66** |

**S3 results**

- **example_ota_5t: PASS.** All gates, all chosen cells DRC/LVS clean with negative controls.

  | Devices | Chosen option | Area (µm²) |
  |---|---|---|
  | PMOS mirror | nf2, gate top | 30.2 → 24.8 |
  | Input pair | nf2, gate top | 61.1 → 43.0 |
  | Tail | nf4, gate top, 50 % coverage | 74.1 → 51.6 |

  - In the circuit with access R: gain 32.88 dB, GBW 101.9 MHz, PM 79.84°, all within the allowances.
  - Device area −27 %.
  - The tail cell changes XM5's current by −3 % (another SKY130 W bin). This is reported in `device_model_change`.
- **ota5t_stress: FAIL, flagged (as S2's G2.0 predicted).**
  - No option fits η = 0.5. The default cells are kept, and the specs are still met: GBW 356.3 MHz (limit 336.3), PM 62.4° (limit 60.08).
  - The cells alone use 46 % of the GBW margin and 53 % of the PM margin, before any wiring.
  - Decision needed: η about 0.9, relaxed stress specs, or layout-aware re-sizing.
- **Other S3 fixes:**
  - via1 enclosure in the straps;
  - label patches;
  - a "strap does not fit" check (4 PMOS nf = 8, 50 % cells; LVS had caught the S–D short);
  - the relaxation case keeps the default PCell.
- **Tests:** 37 pass (S0 14, S1 11, S2 8, S3 4).
