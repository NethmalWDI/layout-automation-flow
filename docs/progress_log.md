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

## 2026-10-25 (night): stress at η = 0.9, pole drop-out study, decisions

**Your decisions:**

- the stress variant gives layout 90 % of each margin (η = 0.9);
- EM is ignored for now;
- S3 is on hold;
- S4 starts on Monday, 2026-10-26.

**η as a package input.** `inputs/ota5t_stress/package.yaml` now has `eta: 0.9`. `src/s2/run.py` takes η from `--eta`, else from the package, else 0.5, and records the value and its source in `budgets.json`. A unit test was added.

**Stress rerun at η = 0.9:**

- **S2: PASS.**
  - Budgets ≈ 0.95 × need (0.998 after phase 1).
  - SPICE verification: GBW 0.84 and PM 0.74 of the margin, both within η.
  - Rules: OUTP met1 ≤ 9.1 µm; net3 proximity 9.3 µm; OUTP~net3 parallel run 12.2 µm.
- **S3: G3.3 PASS, G3.5 FAIL** (PMOS mirror and tail keep the default cell).
  - Input pair: nf4 (61.1 → 36.3 µm²).
  - In the circuit: GBW 369.2 MHz, PM 63.65°, gain 32.22 dB; all specs met, within the allowances.
  - Cause of the FAIL:
    - S2's phase-2 trim (R19);
    - the tail's lower-R options would re-size it.

**Pole drop-out study** (`src/s1/symbolic_patch.py`). Patched copies of the upstream equations are written to `inputs/example_ota_5t/upstream_patched/`; the original is unchanged.

| Variant | Stress PM / GBW | Example PM / GBW |
|---|---|---|
| SPICE | 65.1° / 373.7 MHz | 80.9° / 104.5 MHz |
| Upstream original | 90.6° / 493.7 MHz | 91.3° / 108.4 MHz |
| P1 (mirror doublet) | 73.2° / 373.6 MHz | 82.8° / 104.4 MHz |
| P2 (+ transcapacitance) | 65.2° / 363.7 MHz | 80.2° / 104.0 MHz |

- The mirror pole is ≈ 313 MHz. The earlier figure of 614 MHz was wrong (R20).
- Tests: 40 pass.

**Supervisor review 3** (R19–R24) is in the flow record.

## 2026-10-26: plan v2 (new designs, generality fixes, PVT, baselines, before/after)

The full account is section 7 of `docs/flow_record.md` (draft in `docs/flow_record_section7_draft.md` until the
runs finish). Log of the day:

- **New designs:** `loadbench_miller` (LOADBench two-stage Miller), `ttsky25a_fd` (the TTSKY25a fully
  differential op-amp, with the taped-out tile as layout reference), `iadc_ota` (r09g/iadc folded cascode, with a
  hand-drawn layout). Missing upstream inputs predicted and labelled PREDICTED / ASSUMPTION in each `SOURCE.md`.
- **v1 switch** (`--variant v1`) reproduces the old example_ota_5t golden exactly: the "before" side of every
  comparison.
- **Your decisions:** keep `Opamp_with_bias.sch` as the TTSKY25a DUT (the tile's bias switch block hardly changes
  the area); the ICM 2026 paper figures (~100 dB, 2.3 MHz, 52 deg, CMRR ~91 dB at 1 kHz, post-layout) are the
  reported reference (`circuits/ttsky25a_fd/source/paper_post_layout.json`).
- **Hand-drawn TTSKY25a tile** (`scripts/reference_ttsky25a.sh`): drawn -> PEX costs GBW -6.8 %, PM -3.0 deg at
  every condition set. The tile already differs from the schematic without parasitics (+9.7 dB, -25 % GBW).
  The paper's 2.3 MHz / 52 deg is not reproduced at the designers' own bench conditions (ff, 20 C, 100 MIM
  loads): 1.43 MHz / 78.5 deg. Open question: how the paper's post-layout run was set up.
- **Fixes during the runs:**
  - S2 crashed when a baseline rule's budget left the circuit with no DC solution and ngspice hung: a run
    that times out is now a failed run (`tools.run_ngspice`), budget scenarios time out after 180 s.
  - The structure recogniser put dummies into mirrors (iadc: 24 of 38 dummies in 6 false blocks; S1 divided by
    their zero gm). Dummies are assigned first; iadc package regenerated; S1 reports an off device in a
    matched group instead of crashing.
  - iadc S0 G0.7 FAIL is real: 4 LVT devices (W 1.2, L 0.2 um) give met1.6 minimum-area errors in the default
    PCell, as LOADBench's 484 um single finger does.
- **Git:** GitHub's repository had its own two commits (Initial commit, Delete README.md; no files), so GitHub
  Desktop could not combine the histories and stashed the uncommitted work while trying. Fixed locally without
  force-push: `git merge --allow-unrelated-histories origin/main` (no file changed), then the stash restored into
  the working tree. The interrupted runs were restarted (`runs/tmp/queue_v2c.sh`, log `runs/logs/queue_v2c.log`).
- **Two agents, one repo (20:15):** Imasha may also work with Claude Code on the laptop. The agents share no
  conversation memory, so the shared state now lives in the repo: `CLAUDE.md` (rules verbatim, environment, how
  to run, git policy, coordination protocol; Claude Code reads it at start) and `docs/STATUS.md` (running jobs,
  claims, pending tasks, open questions; updated at the start and end of every work session). Cowork's deploys
  now go through `.incoming/apply.sh`, which refuses to overwrite a file changed since Cowork last synced
  (CONFLICT) instead of silently replacing someone else's edit.
- **Baselines re-scored (20:15):** 5T and ota5t_stress 'after' re-run with review B's scoring. 5T: the LP with
  floors and ours are both safe and feasible, so the table now also reports budget / need: the LP with floors
  gives every element exactly its need (geomean 1.00), ours 3.19. Stress: only ours stays inside the allowance
  in SPICE (0.98) and it reports the design infeasible (G2.7). Snapshots now keep G2.0's split into route C,
  cell C and resistance (`g20_by_part`) and each rule's budget / need.
- **iadc hand layout, R+C (20:20):** the first R+C run was invalid (19.4 dB, gmin stepping failed): the R+C
  netlist exposes the CMFB sub-cell's clock ports separately and they floated. `--map-shorted` ties them; the
  re-run is clean. Wire resistance costs GBW 2.5 MHz and PM 2.5 deg beyond the capacitance, and shifts the
  operating point (output CM -68 mV, gain +3.6 dB). G2.0 'before' predicted the PM part well (2.53 deg) and the
  GBW part 25 x too high (62 MHz, mostly the access resistance of v1's single-finger default cells).
- **Overnight stop and the move to Claude Code (2026-10-27 01:10 Sri Lanka time):** the PC goes off at 01:30,
  about 6 h of runs short. All runs were stopped cleanly (`scripts/plan_v2_stop.sh`) right after loadbench's
  45 PVT points finished. The remaining runs are one resumable script, `scripts/plan_v2_resume.sh`: finished
  steps are marked in `runs/state/plan_v2/`, an interrupted step re-runs, and outputs set aside are restored.
  `docs/HANDOFF.md` is the plan for continuing with Claude Code: setup, first prompt, daily routine, remaining
  work in order, and what each agent can and cannot do. Copies of the claude.ai project docs 08–12 are in
  `docs/context/project_docs/`.

## 2026-10-27: plan-v2 runs resumed; S3 gate-pad met1.6 patch for short-L devices (Claude Code)

- **Runs resumed (05:30 CET):** `scripts/plan_v2_resume.sh` was started with the command in its header (two lanes,
  logs `runs/logs/plan_v2_resume.log`, `plan_v2_lane_A.log`, `plan_v2_lane_B.log`).
- **Lane A stopped at 05:55:** iadc 'before' S3 (v1) raised `mode A-free: no built option for
  ['nfet_01v8_lvt_W1p2_L0p2_m6', 'nfet_01v8_lvt_W1p2_L0p2_m2']`. Lane B (TTSKY) was not affected and kept running.
  - **Why no option:** every built option of these two types failed DRC with met1.6 (Metal1 minimum area
    < 0.083 um2); LVS passed. iadc builds only the options in the sized W bin (`s3_build_mode: A-bin`), so for
    W = 1.2 um only the 4 nf = 1 options exist per type, and all of them failed.
  - **Which shape:** measuring every merged met1 island of the failing cells (KLayout) showed that only the gate
    contact pad is too small: 0.290 x 0.230 um = 0.0667 um2. The PCell's pad does not grow at short L
    (here L = 0.2 um). gtop cells have one pad (3 errors), gboth cells two (6 errors). The S/D strips
    (0.28 um2) are fine, and there is no met2 error. LOADBench's 484/0.24 um nf = 1 cells fail for the same
    reason (same pad, L = 0.24 um). This is journey row 7 (S0 G0.7, open since 2026-10-26).
- **Fix (Imasha's suggestion: a small met1 stripe on the gate):**
  - `src/s3/strap.py` (`pad_patch`): a gate pad below 0.083 um2 is widened symmetrically along the gate (x) to
    the minimum area, on the 5 nm grid. 0.290 x 0.230 becomes 0.370 x 0.230 = 0.0851 um2. Widening in x keeps
    the pad's 0.16 um gap to the S/D strips and leaves the cell's bounding box unchanged. The PCell itself is
    not changed; the patch is drawn in the wrapper, next to the straps and labels. The record keeps the patch
    (`strap.gate_pad_patch`).
  - `src/s3/run.py`: a cached cell that failed DRC before this patch is rebuilt. Signed-off cells are never
    rebuilt, so no earlier result changes.
- **Check:** `src.s3.run inputs/iadc_ota/package.yaml --cells-only --rules v1` (log
  `runs/logs/s3_cells_iadc_gatepad.log`, 65 s): 88 of 88 iadc options signed off (was 80). All 8 rebuilt cells
  have DRC 0 with the negative control still flagged, an LVS match and 1 device. `tests/test_v2.py`: 24 passed.
- **Not covered by this patch (different cause):** `nfet_01v8_lvt_W0p5_L20_m2` (TTSKY), sdhalf options only:
  the S/D strip is 0.230 x 0.355 um = 0.0817 um2 (narrow W with 50 % via coverage). The sdfull options of that
  type pass, so nothing is blocked. These 2 cells are rebuilt once by the cache rule above and still fail.
- **Before/after caveat:** LOADBench 'before' ran with its 4 nf = 1 options unsigned; its 'after' run will have
  them signed off. Check in 7.5 whether S3 picks any of them (unlikely for a 484 um finger).
- **Lane A restarted as a side run (06:27 CET):** `scripts/plan_v2_laneA_now.sh` runs lane A's steps (iadc 'before'
  S3, loadbench 'after', iadc 'after', iadc hand layout) with the same `.done` markers, next to the resume
  script's lane B. The main resume script is paused (`kill -STOP`), so that its final part (eta 0.9 sets
  `outputs/S2/<design>` aside and overwrites it) cannot run while the side lane uses iadc's S2 outputs. After both
  have ended, the resume script is restarted: it runs the no-PVT ablation, eta 0.9, the golden snapshots and the report.
- **Run check (08:16 CET):** 8 steps finished today. Details are in `docs/STATUS.md`, *Recent results*.
  - iadc 'before' S3 (v1) and TTSKY 'before' S3 (v1): FAIL G3.3, G3.5, with every spec met. iadc's G3.3
    failure is the 45 devices that S1 G1.1 already flags below vdsat.
  - **LOADBench 'after' (v2): PM 48.1°, below the ≥ 60° spec ('before' 64.9°).**
    - S2 fails G2.7: the cheapest cells use up to 2.8 × eta × margin at the sf/ss PVT points. It also fails
      G2.3: t = 0.00094, and phase 2 did not converge, so the max-min budgets are kept.
    - So S3 relaxes all 6 types, and each one keeps its nf = 1 default PCell. Two of them have kΩ gate
      resistance: 8.2 kΩ for 484.2/0.24 and 4.9 kΩ for 887.03/0.74. 'Before' had nf = 8 for both.
    - The cells alone, without their access resistance, cost about 1° of PM. All cells together, with access
      resistance, cost 17.3°.
  - **Correction to the caveat above:** I wrote that S3 was unlikely to pick a 484 µm nf = 1 cell. It did, through
    the relaxation fallback. Before the gate-pad patch that cell was not DRC-clean, so the fallback took the
    option with the most slack (nf = 8).
  - Whether to change the fallback is a FEEDBACK NEEDED question in STATUS.md. Nothing is changed until Imasha
    decides.
- **Post-hoc 'least-bad' fallback test (08:40 CET; Imasha's decision):** keep LOADBench's 'after' result as it is.
  After the queue, test a fallback for relaxed types that keeps the least-bad option, gate R included, as a
  separately labelled post-hoc S3 run. Not pre-registered, and reported as such.
  - `src/s3/options.py` `relaxed_pick`: 'default' is the rule every run used, unchanged. 'least-bad' always keeps
    the option with the largest min_slack: the option whose worst check (cell margin use, or the access R of d,
    g or s, each as a fraction of what it may use) is broken least.
  - `src/s3/run.py`: `--relax-fallback` (default 'default') and `--out` (default `outputs/S3/<design>`). Both are
    opt-in, so the queued runs behave exactly as before. The fallback is recorded in G3.5 and
    `device_decisions.json`; the golden comparison does not read those fields.
  - `scripts/compare_before_after.py`: `snap` takes an optional S3 folder. Its record of LOADBench 'after' without
    the folder is identical to the 07:27 snapshot (checked). The report's intro explains the new tag.
  - `scripts/plan_v2_after_queue.sh` (started 08:40:33) waits for both lanes and stops the paused first pass of
    the resume script. It keeps that pass's logs as `*_pass1.log`, because the second pass would overwrite them.
    Then it runs the resume script again. Last, it re-runs S3 with `--relax-fallback least-bad --out
    outputs/posthoc/least_bad/<design>` for every design whose 'after' S3 relaxed a type, snaps it as
    `after_posthoc_leastbad` and writes the report again. Its pieces were dry-checked before launch: syntax, the
    lane and PID detection, the relaxed-type counts and the input-hash check.
  - Before any run, a dry check on LOADBench's existing option table: least-bad keeps nf = 64 for the 484 and 887 um
    devices (gate R 3 and 2 ohm), nf = 8 for 66.13 and 90.63 um, nf = 2 for 37.3 um, and nf = 1 for 14.21 um.
    For ota5t_stress it changes 2 of its 3 relaxed types (nf = 1 to nf = 2). Whether PM recovers is for the
    SPICE run to show.
  - Also: `.gitignore` ignores `outputs/posthoc/*/*/sim/`; README, S3 section; `tests/test_s3.py` covers
    `relaxed_pick` (5 passed); flow record 7.1, row 38.
- **Run check (11:50 CET):** details are in `docs/STATUS.md`, *Recent results*.
  - The side lane ended at 09:25 (exit 0) and lane B at 10:08. The after-queue script stopped the paused first
    pass at 10:08:47, kept its logs (`*_pass1.log`) and started the second pass. By 11:20 that pass had run the
    no-PVT ablation and S2 at eta 0.9 for the 5T designs and LOADBench.
  - iadc 'after' relaxes all 22 types on saturation checks (G1.1's devices), exactly as 'before', so the final
    specs are identical. TTSKY 'after' relaxes 10 of 22 types, mostly on S/D access R; its final specs equal
    'before'.
  - The no-PVT ablation of ota5t_stress passes S2 and S3 with no relaxed type ('after' relaxed 3 of 3).
  - The TTSKY tile's R+C runs warn "Dynamic gmin stepping failed", so they are not trusted yet.
  - **Standby:** the Windows event log shows the PC in Modern Standby (idle timeout) five times between 06:59 and
    11:16 CET. The container's processes slowed or paused then; their run times are 28–32 min shorter than the
    wall clock.
    - Of the logs still on disk, 8 SPICE runs timed out today. 7 are TTSKY 'after' S2 baseline runs at
      08:26–08:43, before any standby.
    - The eighth, an iadc 'after' lp_floor check (started 08:51:13, 28 s into a standby; 180 s limit), may be a
      standby artefact. It changes no outcome: 8 other failed runs already mark lp_floor "unverified".
    - No timeout appears in today's PVT sweeps or S3 simulations.
    - The eta 0.9 S2 runs of example_ota_5t and LOADBench ran almost entirely in standby, and their logs were
      removed when the 'after' outputs were put back. Whether to re-run them is a FEEDBACK NEEDED question in
      STATUS.md.
  - The post-hoc folders of TTSKY, LOADBench and ota5t_stress were seeded with copies of the 'after' `sim/`
    folders (11:41–11:48; file counts checked). S3's cache reuses a run only for identical deck text with exit
    code 0, so the post-hoc results equal a fresh run's, but take minutes instead of about an hour.
- **eta 0.9 re-run queued (12:00 CET; Imasha's decision):** after the post-hoc test, re-run S2 at eta 0.9 for
  example_ota_5t and loadbench_miller with the PC awake, and compare with the first runs.
  - `scripts/plan_v2_eta09_rerun.sh` (started 11:59:41) waits for `scripts/plan_v2_after_queue.sh` to finish. It
    then repeats the resume script's eta 0.9 step for the two designs, with snapshot tag `after_eta0.9_rerun`.
  - It keeps the re-run's S2 folder in `outputs/posthoc/eta09_rerun/<design>/S2/`, so failed runs can be traced
    this time.
  - It records wall-clock time against container uptime over each run (`clock.json`), so a standby shows as a
    jump.
  - The S2 run carries no `.done` marker. That avoids a latent problem of the resume script's eta step: after
    an interruption between S2 and its snapshot, the restored 'after' S2 would be snapped as eta 0.9. That
    problem is noted in STATUS.md, not fixed, because that script is running.
  - `scripts/compare_eta09_rerun.py` compares any two snapshot tags of a design rule by rule: outcome, failed
    SPICE runs, worst use, gates. Tried on ota5t_stress 'after' against 'after_eta0.9', both at eta 0.9 and
    neither in standby: the same gates and failed-run counts, but 'ours' SPICE worst use 0.984 → 1.11, which turns
    "infeasible" into "unsafe + infeasible". So some drift exists without standby; its source is still to be found.
  - Keep-awake: since 12:00 the Claude Code session holds the PC awake (app keep-awake). A background watcher
    waits for the re-run. The Windows sleep setting is the sure way.
- **All runs finished (13:04 CET).**
  - The resume script's second pass ended at 12:36 with 33 steps done: eta 0.9 for all 5 designs, golden
    snapshots, report. The post-hoc test ran 12:36–12:40 and the eta 0.9 re-run 12:41–13:04.
  - No standby after 11:16 (Windows event log).
  - **Post-hoc 'least-bad' fallback** (not pre-registered; same inputs as 'after', checked by hash):
    - LOADBench PM 48.1° → 64.7° (spec ≥ 60°; 'before' 64.9°). G3.3 now passes. Area 4396 → 2142 µm²
      ('before' 2342). Power 361 → 555 µW ('before' 551, limit 614).
    - 5 of 6 types change. The 484/0.24 and 887/0.74 devices go to nf = 64, gate R 3 and 2 Ω instead of 8184
      and 4855 Ω.
    - ota5t_stress: area 257 → 206 µm², GBW 356.3 → 370.2 MHz, PM 62.4 → 63.8°.
    - iadc and TTSKY: no type changes. iadc's relaxed types have only nf = 1 options under A-bin. For TTSKY's 10,
      the least-bad option is the default cell itself.
    - The power numbers suggest that LOADBench's nf = 1 fallback also moved the bias point: 88–161 Ω of S/D
      access R in the sources of large, weakly inverted devices. That is an inference, not a separate run.
  - **eta 0.9 re-run with the PC awake:** example_ota_5t and loadbench_miller reproduce their first runs exactly:
    gates, outcomes, failed-run counts, worst use and verification. So the morning's standby changed nothing
    there.
    - The 5T re-run again has 4 ngspice timeouts in lp_sum, with the PC awake, so those runs really hang.
    - The re-runs are bit-for-bit reproductions on the same day. So the ota5t_stress 'after' (2026-10-26) vs
      'after_eta0.9' (today) difference comes from something that changed in between, not from noise. It is
      still to be found.
  - TTSKY at eta 0.9: every budget rule's outcome is as at eta 0.5. The eta 0.9 table (PREREG headline) is
    complete in `docs/before_after.md`.
  - `clock.json`: with the PC awake, the wall clock still ran 5 % ahead of container uptime (25–32 s per run).
    That is the VM's normal drift, so the measure needs that baseline.
- **S3 relaxed-type rule: 'least-bad' is now the default for future runs (13:30 CET; Imasha's decision).**
  - Plan v2's 'after' results and the post-hoc label stay as they are. PREREG.md has a dated amendment saying the
    change was decided after seeing plan v2's results.
  - `src/s3/options.py` (`relaxed_pick`) and `src/s3/run.py`: the default is `least-bad`; `--relax-fallback
    default` is the old rule, kept for reproducing plan v2.
  - `src/flow.py`: the v1 variant pins `--relax-fallback default`, so 'before' stays reproducible. `./flow run`
    and `./flow test` take `--relax-fallback`.
  - Golden S3 re-runs (`./flow test --rerun`) use the rule recorded in the snapshot. `src/golden.py` now records
    it; snapshots taken before today count as 'default'.
  - `scripts/plan_v2_resume.sh` and `scripts/plan_v2_laneA_now.sh`: their 'after' S3 and ablation S3 pin
    `--relax-fallback default`, so plan v2's scripts still reproduce plan v2.
  - Tests: `tests/test_s3.py` covers the default and the flow's pass-through. `tests/test_s3.py`,
    `tests/test_v2.py` and `tests/test_golden.py`: 51 passed (the golden comparison of every committed output
    included).
  - Docs: README (S3, "Relaxed types"), the report intro (`docs/before_after.md` regenerated) and flow record
    7.1 row 38.
- **Work stopped here for a handoff to Cowork (13:35 CET).** Imasha will run Cowork on this folder for the
  documentation. Nothing is running in the container, nothing is set aside, and nothing is committed.
  STATUS.md has the handoff notes.

## 2026-10-27 (afternoon): documentation pass and independent review C (Cowork)

Imasha handed the write-up to Cowork after Claude Code finished the runs. No run was started and no flow code was
changed in this pass.

- **Catch-up findings before writing:**
  - The TTSKY25a S2 run at eta 0.9 crashed (`OSError: [Errno 22] Invalid argument` writing an ngspice log in the
    mounted folder, 12:36). The resume script snapped it anyway, because a crash and a gate FAIL both exit with
    code 1. The snapshot mixes that run's `budgets.json` with the eta 0.5 report, so it is not a result. Flow record
    row 40.
  - `docs/before_after.md` has budget-rule tables for the 'after' runs only (each design's own eta). The eta 0.9
    table was built from the snapshots for flow record 7.6.
  - Today's work was committed by Imasha as `1aa7f791` (17:54 Sri Lanka time).
- **Written:** flow record section 7 completed.
  - 7.5: LOADBench, iadc and TTSKY25a before/after, with the post-hoc column labelled.
  - 7.6: held-out designs at eta 0.5, the eta 0.9 headline, a binding-margin table and the hypothesis reading.
  - 7.7, 7.8: against the 'after' G2.0.
  - 7.9: review C. 7.10: limitations. New 7.11: assessment.
  - Journey rows 40–44.
  - Outside section 7: the record's header, status at a glance, problems log and changelog.
- **Figures:** five `docs/flow_record/img/v2_*.png`, drawn from the snapshots by `scripts/make_v2_figures.py`. They
  are rendered in the container (DejaVu Sans), so they can be regenerated there.
- **Independent review C:** an agent that had not seen our notes read the write-up against the snapshots, the run
  outputs and the code. It made 14 findings, each checked against the files before acting.
  - **Corrected in the text:**
    - equal split matches or beats ours on every pre-registered outcome on the held-out designs;
    - H1 has no tolerance (3 exceedances in 8 pairs);
    - H1c is guaranteed when the floors exceed the allowance;
    - per-net's overshoot is by construction;
    - the G2.0 vs hand-layout comparison must include the cell part (no like-for-like number within 25 %);
    - the claim that G2.0 "flagged" LOADBench is withdrawn;
    - the 5T gate-resistance sentence contradicted row 20;
    - several number and label errors.
  - **Confirmed and open (technical):**
    - S3's saturation check gives devices below vdsat a negative margin, so every option fails; iadc's S3 results
      are artefacts (row 41).
    - The 5T's binding PVT corner is contradicted by SPICE, and G2.5 cannot see it (row 42).
    - Variant S2 runs leave stale files in the S2 folder (row 43).
    - G2.0's route lengths still come from the as-sized PCells (row 44).
    - The binding PVT points have margins of 0.014 dB, 0.093 dB and 0.26 deg, at or below the model error.
    - The LP with floors is capped at the need while ours may reach 10 x.
    - Phase 2 above 200 elements stops on wall-clock time.
    - The ota5t_stress drift is in the PVT-point inputs, not in the cell cache, which contradicts the earlier
      hypothesis.
- **Slides:** deck version 7, with the section "Plan v2" (15 slides; titles in `docs/slides_v2.md`).
- **claude.ai project doc 13:** `claude/13_plan_v2_results_and_review.md` (copy in `docs/context/project_docs/`).
- **STATUS.md:** claim released; pending tasks 1d–1i added; one FEEDBACK NEEDED list.
- **Deploy incident (14:19 CET), fixed:** a deploy archive reused an old name (`docs_c`), the bridge delivered the
  2026-10-26 archive of that name, and `apply.sh` extracted it because it had no `__prev_md5.txt` to check. That
  overwrote `PREREG.md` and `docs/flow_record_section7_draft.md` with their 2026-10-26 18:22 versions for about
  5 minutes. Found from the archive md5 that `apply.sh` prints. Both files were restored from Cowork's copy, with the
  md5s checked. `apply.sh` now requires the expected archive md5 and the `__prev_md5.txt` file, and archive names
  carry a timestamp (flow record row 45).
