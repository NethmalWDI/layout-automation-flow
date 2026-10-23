# Phase 1: Inventory

- **Project:** Analog layout automation, stages S0–S3
- **Author:** Claude (research engineer), for Imasha
- **Date:** 2026-10-23 (Fri)
- **Status:** Phase 1 deliverable. No code was written and no source files were changed.
- **Source folder (read-only):** `C:\Users\suind\Desktop\Layout_automation`

---

## 0. The five things you need to know first

1. **The folder has no sizing results. It has a hierarchy decomposition.**
   - All six transistors in `5t-ota/` have the same size: `w=1 l=0.15 nf=1 m=1`. These are template defaults; nothing was sized.
   - No operating point, no specs and no measured performance exist.
   - Every numeric value in `verification/` is labelled *"dummy values"* by the generator itself.
   - What the folder does contain:
     - a correct primitive hierarchy
     - small-signal netlists
     - symbolic equations that map each level onto the level below it
2. **The code that produced `5t-ota/` is not in the folder.**
   - These scripts are named in file headers but missing: `extract-primitives.py`, `build-hierarchy.py`, `netlist-gen.py`, `verify.py`.
   - These inputs are also missing: `topologies/5t-ota/circuit.spice`, `primitives/*/circuit_model.spice`, `mosfet-ssm.spice`, `transconductance-amplifier-ssm.spice`.
   - I could not find `llm-analog-sizing` publicly on GitHub, so I assume it is private.
3. **The level-2 model is not exact.**
   - `equations.json` sets `"exact": false` for `diso_amplifier`.
   - It lists three "missing" terms, all at **net0**, the mirror node: G12 and C12 of the load mirror.
   - So the top-level transfer function is single-pole and does not contain the mirror pole/zero.
   - Consequence: S1 must look at net0 sensitivity using level 1 or level 0, not level 2.
4. **The ChatGPT plan's worked examples use a different circuit.**
   - The plan uses ALIGN's own `five_transistor_ota`, with devices M0–M5 and nets VOUT, NET8, SOURCE, ID.
   - Our circuit has XM1–XM6 and nets Voutp, net0, net1, Iref.
   - Every example in the plan needs a name mapping before we can use it.
5. **The toolchain is the IIC-OSIC-TOOLS Docker image on SKY130.**
   - The logs show paths under `/foss/designs/...` and ngspice output.
   - Docker Desktop, WSL, VcXsrv and KLayout are present on Windows.
   - I could not run tools inside the computer's Linux shell yet, because it was still downloading (§4).

---

## 1. File list

### 1.1 Top level

| File | Size | Description |
|---|---|---|
| `Implementation plan feedback_chatgpt.pdf` | 1.3 MB, 80 pp | Export of the ChatGPT conversation. It has three turns: (1) a 10-day S0–S9 roadmap built on MAGICAL; (2) a revision that switches to ALIGN + ALIGN-pdk-sky130, and covers using Codex or Claude Code as the LLM; (3) a detailed S0–S3 plan. The "Pasted text.txt" project summary it refers to is **not** included. |

### 1.2 `literature/` (7 papers)

| File | Paper |
|---|---|
| `10356330.pdf` | MAGICAL: open-source automated analog layout, netlist to GDSII. Chen et al., IEEE D&T 2021. |
| `2008.10682v1 (1).pdf` | ALIGN: A System for Automating Analog Layout. Dhar et al., arXiv 2020. |
| `4A-3-117.pdf` | Open-ALOE: analog layout automation flow for the open-source ecosystem. Li et al., ISQED 2025. Uses SKY130. |
| `AICL_Co-pilot_….pdf` | AICL Co-pilot: hybrid hierarchical analog layout. Bio et al. (JKU, Pretl), SMACD 2026. |
| `2606.15052v1.pdf` | PANDA: LLM-enhanced performance-driven analog design to layout. Zhang et al. (PKU), DAC 2026. |
| `2608.13767v1.pdf` | ICPI: simulation-aware in-context policy improvement for LLM-aided layout refinement. Liu et al. (UT Austin), 2026. |
| `2610.15240v1.pdf` | The Era of Vibe Tapeout. Yoshioka (Keio), 2026. LLM agents doing a SKY130 SAR ADC with Magic and Netgen. |

### 1.3 `5t-ota/` (read-only)

**Netlists**

| File | Format | Description |
|---|---|---|
| `5t-ota_primitives.spice` | SPICE subckt | **Transistor-level reference.** One subckt per primitive instance, plus `.subckt 5t-ota VDD VSS Vinp Vinn Voutp Iref`. Contains the six `sky130_fd_pr` MOSFETs. Written by `extract-primitives.py`. |
| `5t-ota_differential_primitives.spice` | SPICE subckt (linear) | Level 0 in differential mode. Each MOSFET is replaced by its small-signal C/G/R stamp (`C1..C4`, `G1`, `R1` per transistor). Rails and the tail node net1 are tied to GND (virtual ground). Written by `build-hierarchy.py`. |
| `5t-ota_differential.spice` | SPICE subckt (linear) | Level 1, where each primitive is an abstract 2- or 4-port model, and level 2, where the whole amplifier is one `diso_amplifier` transconductance model. |
| `primitive-models/*_DM.spice` (3 files) | SPICE | Generic differential-mode small-signal models for each primitive class (M1, M2 naming). Written by `netlist-gen.py`. |

**JSON metadata**

| File | Description |
|---|---|
| `primitives.json` | Instance → primitive class, category, library path and port→net map. Also the transistor rename map (e.g. M1→XM3) and the list of rail names. |
| `hierarchy.json` | The tree: level 1 (load, gm and bias structures) → level 2 (`diso_amplifier`). Lists nodes, inputs and outputs per block, plus the differential-mode block table (path, parent, ports, open ports). |
| `5t-ota_differential_equations.json` | Symbolic value maps from each level to the one below. For example `G2_X1 = G12_X1_X1*G1_X1_X2*R1_X1_X1*R1_X1_X2/(R1_X1_X1+R1_X1_X2) + G2_X1_X2`. Also holds symbolic performance (transfer function, A0, GBW, PM and a zero) and the exactness flags `free`, `unmatched`, `missing` and `exact`. |

**`verification/` (20 files)**

| Files | Description |
|---|---|
| `*_level-N.spice` (10) | ngspice AC benches written by `verify.py`. Step 1 compares each primitive at level 0 against level 1. Step 2 compares the amplifier at level 1 against level 2. Step 3 runs the whole circuit at level 0. All use **dummy** parameter values. Sweep is AC from 1 kHz to 100 GHz, 20 points per decade. |
| `*_level-N.log` (10) | ngspice stdout. Each shows the run finished (161 points) and nothing else. **There is no pass/fail record. The `.raw` waveform files were not copied.** |

---

## 2. What the ChatGPT plan defines

### 2.1 Overall structure

The conversation names stages S0–S9, plus O1, O2 and O3 for the upstream and orchestration layers. Only S0–S3 are defined in detail.

| Stage | Plan's definition |
|---|---|
| O1/O2 | Upstream topology/sizing: the "existing inverse-design optimizer". O3 is "your framework": hierarchy → budgets → physical controls → verification → diagnosis → repair. |
| S0 | Baseline and netlist integration |
| S1 | Electrical intent extraction |
| S2 | Physical constraint compilation |
| S3 | PDK-aware primitive / device generation |
| S4–S5 | Placement and routing. Branch A: an existing engine plus LLM-chosen constraints, ICPI-style. Branch B: the LLM writes layout code with no optimizer. |
| S6–S8 | DRC → LVS → PEX → SPICE, then pre-simulation parasitic diagnosis, counterfactual tests and targeted repair (return-stage table in Turn 1 §5) |
| S9 | Not defined |

**How the plan changed between turns.**
- **Turn 1:** MAGICAL is the baseline. ALIGN-SKY130 is run in parallel as the "real PDK" track.
- **Turn 2:** ALIGN + ALIGN-pdk-sky130 becomes the main platform. MAGICAL is kept only to study its algorithms.
- **Turn 3:** keeps ALIGN.

**Three experiment branches run throughout:**
- **A:** ALIGN defaults
- **B:** analytical constraints (our hierarchy plus SymMNA)
- **C:** B plus constraints proposed by the LLM and then validated

### 2.2 S0–S3 in detail (Turn 3)

| | S0: Baseline and netlist freeze | S1: Electrical intent | S2: Constraint compilation | S3: Primitive generation |
|---|---|---|---|---|
| **Goal** | Make ALIGN-SKY130 work and freeze the reference netlist | Find which devices must match, which nodes matter, and why, *quantitatively* | Turn intent into budgets and constraints that ALIGN accepts | Generate SKY130 primitives without changing the circuit |
| **Inputs** | ALIGN-public, ALIGN-pdk-sky130, the `five_transistor_ota` example, the reference SPICE | Sized netlist, hierarchy, **DC operating points (ngspice)**, SymMNA models, **spec file**, SKY130 device map, optional human annotation | S1 outputs and specs | Reference netlist, S2 `.const.json`, ALIGN-SKY130 generators |
| **Outputs** | Run directory (`1_topology`, `2_primitives`, `3_pnr`), GDS, logs, pinned commits, `reference_manifest` (hash, pins, devices, models, params) | `hierarchy`, `matching.json`, critical-node table, **`sensitivity.json`** (central or forward finite difference S = ∂M/∂C, with units and testbench), `intent.json` | `parasitic_budgets.json` (C_budget ≈ η·margin/\|S\|), `constraints_ir.json` (tool-neutral), `<subckt>.const.json` (SameTemplate, SymmetricBlocks, GroupBlocks, NetConst, PortLocation, Order …) | `__primitives__.json` from `--flow_stop 2_primitives`, a device-equivalence report, variants V0, V1, V2, primitive DRC/LVS, pins, bounding boxes |
| **Success criteria** | `schematic2layout.py -h` works; the example runs; 6 devices recorded; GDS is non-empty; repeat run is consistent; DRC/LVS status *known* | 100% match on connectivity, device inventory and pair identity; sensitivities converge across step sizes; symbolic and SPICE agree in sign and magnitude; negative tests reject bad input | Every name resolves; 0 hard conflicts; incremental B1/B2/B3 experiments; constraints are *consumed* by ALIGN; negative tests | The default primitive is generated; electrical identity is preserved; geometry and pins are recorded; DRC/LVS results are clear; provenance is saved |
| **Effort** | 1–2 days | 2 days | 2 days | 2 days or more |

**Turn 3 schedule:** 7 development days for S0–S3, plus a 16-item checklist in §11.

**My early read.** The plan is sound on separation of concerns:
- the research IR stays separate from tool syntax
- hard constraints are kept apart from soft ones
- every value is marked verified, estimated or not evaluated
- negative tests are included

It is weak on three points:
- it assumes a sized netlist and an operating point that we do not have
- it is anchored to ALIGN's example circuit rather than ours
- it does not budget for ALIGN's SKY130 maturity issues, which it acknowledges itself

The full critique belongs to Phase 2.

---

## 3. The literature: method, I/O and what we can reuse

| Paper | Method | Inputs → outputs | Reusable for us | Limits for us |
|---|---|---|---|---|
| **MAGICAL** (D&T'21) | Bottom-up hierarchy. Parametric device generators. Symmetry found by graph isomorphism against a pattern library, plus spectral similarity at system level. Analytical global placement with LP legalisation. Symmetry-aware A* routing. | Unannotated Spectre/HSPICE netlist plus design rules → GDSII | S1: pattern-based symmetry extraction. S3: generator concept. Net-criticality and spacing constraints (Liu et al. extension). | Demonstrated in TSMC 40 nm; the public examples use a mock PDK; **no SKY130**. No parasitic budgets. |
| **ALIGN** (arXiv'20) | GCN plus subgraph-isomorphism annotation. Design rules abstracted to a JSON grid that includes **per-unit parasitics**. Constraint generation. Parameterised primitives (CC/ID, aspect ratio). Sequence-pair placement. Constructive or SAT routing. | Sized SPICE, specs and PDK JSON → GDS. Designer annotation can override. | Closest match to our S1/S2/S3 split. Its "max node parasitic → wire length / tracks / vias" electrical constraint is our budget concept. Has a `.const.json` interface. | Electrical constraints were work-in-progress. The paper does not show SKY130. |
| **Open-ALOE** (ISQED'25) | Magic-generated **SKY130 stem cells** (LEF/LIB/GDS). Digital PnR with net weights. NSGA-II over net weights, with wire-length objectives on critical nets. Magic DRC and Netgen LVS. | SPICE plus user objectives → multiple GDS candidates | The only paper here with **SKY130 silicon** (a bandgap). Its Magic/Netgen checking is directly reusable. Our S1 sensitivities could weight its objective. | Needs **Cadence Innovus**. Has no explicit symmetry or matching constraints. |
| **AICL Co-pilot** (SMACD'26) | Attribute-aware subgraph matching to S-cells and M-cells. Relative or abutment placement. RSMT routing. | Netlist plus a Python placement-constraint structure → DRC/LVS-clean layout | Listing 1 is **a 5T-OTA placement constraint set** (tail → pair on top → load on top). A simple, tool-neutral relative-placement schema. | No SKY130 (uses IHP and TSMC). No electrical results. No code. Symmetry is listed as future work. |
| **PANDA** (DAC'26) | LLM as planner and constraint writer. Deterministic sizing (MOSTAR BO), placement and routing (SAGERoute). JSON artefacts per stage. PEX feedback used to choose among attempts. | Intent and spec → `topology.json`, `placement_constraints.json`, `routing_rules.json`, `pl.json`, `rt.json` | Per-stage JSON handoff and snapshot discipline. Pin lists synced from the netlist. | Critical nets are chosen by the LLM, with no sensitivity analysis. **Post-layout UGB 4.19 MHz against an 8 MHz target.** PDK and tools not stated. |
| **ICPI** (2026) | A modified MAGICAL kernel. Five action families: net weights, placement bias, symmetry, routing priority, wire widths. A one-time LLM Analyzer, then Supervisor, Executor and Reflector agents with a design journal and rollback. | Netlist and tech → parameters → PEX → simulation, with FoM = geometric mean of scores × PM factor | S2 can compile into the same five action families. Our SymMNA sensitivities can **replace the LLM Analyzer** with a deterministic prior. The journal design suits S4+. | Uses Calibre, Spectre and commercial 65/40 nm processes. The public code is synthetic only. |
| **Vibe Tapeout** (2026) | General coding agents write Python/Tcl that emits SPICE and Magic layout. Includes a supervising verifier, checkpoints and one-factor-at-a-time PEX ablation. | Spec → GDS, `DECISIONS.md`, `iterations.jsonl` | Same PDK and same open tools. Turns acceptance criteria into code. Uses an **independent verifier**. Its benchmark task T1 is a 5T OTA. | Found **false passes**, including the Magic extraction lumping coupling C to ground and LVS passing with missing nets. Results come from a single run. |

**What none of the seven papers does:** derive layout constraints or parasitic budgets from *symbolic* small-signal sensitivities. That remains the defensible novelty for S1/S2, consistent with the ChatGPT plan's own repositioning after the Vibe Tapeout paper.

---

## 4. The 5T-OTA data in detail

### 4.1 Circuit (from `5t-ota_primitives.spice`)

| Instance | Primitive (category) | Device | Model | W (µm) | L (µm) | nf | m | D / G / S / B |
|---|---|---|---|---|---|---|---|---|
| XM1 | pmos_current_mirror_load (load), M1 diode | pfet | `sky130_fd_pr__pfet_01v8` | 1 | 0.15 | 1 | 1 | net0 / net0 / VDD / VDD |
| XM2 | pmos_current_mirror_load, M2 | pfet | same | 1 | 0.15 | 1 | 1 | Voutp / net0 / VDD / VDD |
| XM3 | nmos_differential_pair (gm), M1 | nfet | `sky130_fd_pr__nfet_01v8` | 1 | 0.15 | 1 | 1 | net0 / Vinp / net1 / VSS |
| XM4 | nmos_differential_pair, M2 | nfet | same | 1 | 0.15 | 1 | 1 | Voutp / Vinn / net1 / VSS |
| XM6 | nmos_current_mirror_bias (bias), M1 diode | nfet | same | 1 | 0.15 | 1 | 1 | Iref / Iref / VSS / VSS |
| XM5 | nmos_current_mirror_bias, M2 | nfet | same | 1 | 0.15 | 1 | 1 | net1 / Iref / VSS / VSS |

- **Ports:** VDD, VSS, Vinp, Vinn, Voutp, Iref.
- **Internal nets:**
  - net0: mirror gate / XM3 drain
  - net1: tail
- **Bodies:** NMOS bodies are on VSS, so the input pair has body effect when net1 > VSS. PMOS bodies are on VDD.

**Flag: no sizing.** All six devices share the same template defaults, and L = 0.15 µm is the SKY130 minimum. That is unrealistic for an OTA input pair or mirror. **ASSUMPTION needed:** either (a) you give me the sized netlist, or (b) we run S0–S3 on these placeholder sizes and label every number as placeholder.

### 4.2 Hierarchy

| Level | Content |
|---|---|
| 0 | 6 transistors |
| 1 | X1 load-structure {XM1, XM2}; X2 gm-structure {XM3, XM4}, inputs Vinp/Vinn, outputs net0/Voutp; X3 bias-structure {XM6, XM5} |
| 2 | X1 `diso_amplifier` (differential-input, single-output), members {load, gm, bias} |

This lines up directly with layout groups: three matched pairs.

### 4.3 Electrical data

| Item | Exists? | Notes |
|---|---|---|
| Small-signal topology per level | Yes | DM only, so tail and rails are AC ground. **No common-mode model**, which means no CMRR or PSRR view of net1 or the rails. |
| Symbolic level-to-level maps | Yes | `equations.json`. Primitives are exact. The amplifier is `exact:false`, with net0 terms missing (§0.3). |
| Symbolic performance | Yes, level 2 | A0 = G2·R2/2; ω_GBW = G2 / (2(C4+C6+CL)); zero at G2/C6; PM formula. **CL is a free symbol with no value.** |
| Numeric parameter values (gm, gds, C) | **Dummy only** | For example G1_XM3 = 263 µS, R1_XM3 = 33.9 kΩ, caps 1–9 fF. These give A0 ≈ 4.98 (13.9 dB), which I recomputed. They are not operating-point values. |
| DC operating point, bias current, VDD, input CM | **No** | |
| Specs (gain, GBW, PM, CL, power) | **No** | |
| Verification verdicts | **No** | The logs show only that runs completed; there are no `.raw` files and no comparison metric. |
| Layout data (GDS, LEF, constraints) | **No** | As expected, since this is upstream of layout. |

### 4.4 Technology

- **PDK:** SkyWater SKY130 (`sky130_fd_pr__{n,p}fet_01v8`, 1.8 V devices). The PDK version or commit is **not recorded**.
- **Simulator:** ngspice, in HSPICE-compatible mode `hs a`. The version string was not captured.
- **Environment:** the log paths `/foss/designs/PROJECTS/llm-analog-sizing/...` match the **IIC-OSIC-TOOLS** Docker image (JKU, Pretl), which bundles magic, netgen, klayout, ngspice, xschem, open_pdks, OpenROAD and gLayout.

---

## 5. Toolchain on this machine

| Item | Status | How I know |
|---|---|---|
| Windows host | `imasha-pc` | Device info |
| Docker Desktop | Installed | `C:\Program Files\Docker` |
| WSL | Installed | `C:\Program Files\WSL`, `~/vscode-remote-wsl` |
| VcXsrv (X server, needed for GUI tools from Docker) | Installed | Program Files |
| KLayout | Probably installed on Windows | `~/KLayout` config folder exists. Version unknown. |
| Git for Windows | Installed | Program Files |
| Node.js | Installed | Program Files |
| Codex CLI | Has been used | `~/.codex` |
| IIC-OSIC-TOOLS image, magic, netgen, ngspice, sky130 PDK | **Probably inside Docker. Not yet verified.** | Inferred from the log paths. I need `docker images` and an in-container version check. |
| ALIGN-public, ALIGN-pdk-sky130, MAGICAL, gLayout | **Not found** in the visible folders | Desktop, Documents and GitHub (empty) |
| `llm-analog-sizing` repo | **Not found locally** | Only the copied `5t-ota/` results are here |
| Linux shell for Claude on this PC | **Not ready**: "workspace still downloading" | I will re-check before Phase 4 |

**Constraint I need to tell you about.** The shell I can run on your PC is an isolated Linux VM that only sees the connected folders. It **cannot reach Docker Desktop or WSL**. So anything that has to run in IIC-OSIC-TOOLS (Magic DRC, Netgen LVS, primitive generation in SKY130) means either:
- you run a script I give you inside the container, or
- I install the same tools myself (in my cloud workspace or the VM), which needs your approval.

This is a planning decision for Phase 3.

---

## 6. Gaps: what S0–S3 need against what exists

Legend: ✅ have it · ⚠️ partial or placeholder · ❌ missing

| Stage | Need | Status | Gap or action |
|---|---|---|---|
| **S0** | Transistor-level reference netlist | ✅ | `5t-ota_primitives.spice`. Freeze it with a hash. |
| | Real device sizes (W/L/nf/m) | ⚠️ | All placeholders. **Ask you.** |
| | Pin roles: supply, ground, input, output, bias | ⚠️ | Derivable from `primitives.json`. Needs confirming. |
| | Consistency across the three netlists and the JSONs | ✅ data, ❌ check | Write a cross-checker. |
| | PDK version and tool versions | ❌ | Need `open_pdks` commit and tool versions from your container. |
| | Layout engine installed (ALIGN, gLayout or other) | ❌ | Decide in Phase 2. Needs an install. |
| **S1** | Hierarchy and grouping | ✅ | `hierarchy.json`, `primitives.json`. |
| | Matching pairs with evidence | ⚠️ | Implied by primitive class. Formalise it. |
| | Symbolic transfer functions and performance | ✅ DM level 2, ⚠️ net0 | Rebuild net0 sensitivity from level 1 (the mirror pole). |
| | Numeric small-signal values at the operating point | ❌ | Dummy only. Need an OP sim of the real sizing (sky130 models, `.op` with gm/gds/cgs/cgd/cdb). |
| | Specs and margins (gain, GBW, PM, CL) | ❌ | **Ask you.** Without them, budgets can only be relative. |
| | Common-mode / CMRR model (net1, rails) | ❌ | Not in the data. Mark as out of scope or add a CM bench. |
| | SPICE validation of sensitivities | ❌ | Need ngspice with sky130 models, or at least the linear netlists (I can do those with ngspice on the given C/G/R models). |
| **S2** | Budget method and safety factor η | ⚠️ | Formula exists in the plan. η is your choice. |
| | Target tool constraint schema | ❌ | Depends on the Phase 2 tool choice: ALIGN `.const.json`, gLayout params, or MAGICAL `.sym`. |
| | Per-unit wire parasitics for SKY130 metals | ❌ | Available from the PDK or ALIGN's `layers.json`, once installed. |
| **S3** | SKY130 device generator | ❌ | ALIGN-pdk-sky130 or gLayout, depending on Phase 2. |
| | DRC/LVS decks (magic tech, netgen setup) | ❌ here, probably ✅ in your Docker | Confirm. |
| | Device-equivalence rules (meaning of nf and m in sky130 models) | ❌ | Get from PDK docs and the generator source. |
| **S3→S4 handoff** | Defined format for Monday's inputs | ❌ | Design in Phase 3. I need to know roughly what arrives Monday. |

---

## 7. Questions for you

These are blocking, or nearly blocking, for Phase 3.

1. **Sizes.** Is there a *sized* 5T-OTA output from `hierarchical-optimization` that is not in this folder, perhaps in another results subfolder? Or are S0–S3 meant to run on the placeholder sizes?
2. **Specs and operating point.** What are VDD, Iref (or the tail current), input common-mode, CL, and the gain/GBW/PM targets?
3. **Code access.** Can you give me the `llm-analog-sizing` repo, or at least the scripts named in §0.2 plus `topologies/` and `primitives/`? That lets me regenerate the equations with numeric values instead of reverse-engineering them.
4. **Docker.** Is the IIC-OSIC-TOOLS image what you use, and which tag? Are you willing to run short scripts in it, or do you prefer that I install the tools (with your approval)?
5. **Monday's inputs.** What roughly are they? For example, real sizing, more circuits, or PEX? This shapes the S3→S4 handoff.
6. **The S0–S9 project summary.** The "Pasted text.txt" summary the ChatGPT chat started from is not in the PDF. Can you share it, so I use your own stage definitions?
7. **GitHub remote.** I will create the local repo at `Documents\GitHub\layout-automation-s0-s3`. Should it also have a remote on your GitHub account, private by default? I will never push without your OK.

---

## Addendum (2026-10-23, after your answers)

| # | Your answer | Effect on the plan |
|---|---|---|
| 1, 2, 5 | Use the dummy-sized `5t-ota` as it is. The goal is a working S0–S3 flow by Sunday. Nodal-analysis results arrive Monday or next week. | All numeric values are **PLACEHOLDER**. S1/S2 must accept the nodal-analysis results later through a defined import slot, with no code change. |
| 3 | You uploaded the full `llm-analog-sizing-hierarchical-optimization` repo (154 files, Apache-2.0 `LICENSE`). | The generator scripts (`src/stage1_hierarchy/*.py`), `topologies/5t-ota/circuit.spice` and `primitives/` are now available. Its `container.py` already drives IIC-OSIC-TOOLS from Python with `docker exec`. |
| 4 | Docker image `hpretl/iic-osic-tools:2026.10` (ID 306585de35d1). You want a separate container from the same image. | Feasible. Phase 3 will specify a container named `layout-s0s3` with the repo mounted at `/foss/designs`. |
| 6 | Project context uploaded. | Saved as `docs/context/project_context_S0-S9.md`. Your own S0–S9 definitions and output names (`circuit_ir.json`, `device_map.json`, `pdk_config.yaml`, `intent.json`, `sensitivity.json`, `constraints.json`, `variants.json`) take precedence over the ChatGPT wording. |
| 7 | Keep the repo local. Start MAGICAL alongside ALIGN. | No remote. Both engines are evaluated in Phase 2. |

**Two new findings from the full repo**

1. **`results/example_ota_5t/` is a *real sized and simulated* 5T OTA.**
   - **Sizes:** M1/M2 = 24/0.5, M3/M4 = 8/1, M5 = 24/1, with a 0.75 V tail-bias source.
   - **Measured:** 31.7 dB gain, 104 MHz GBW, 81° PM, 153 µW.
   - **Specs:** gain ≥ 30 dB, GBW ≥ 20 MHz, PM ≥ 60°, CL = 1 pF, VDD = 1.8 V.

   This is a different netlist from the dummy `5t-ota`: it has no Iref mirror, and its tail is biased by a voltage. It is **not** used for the Sunday flow, per your answer. It is the obvious second test case once the flow works, because it gives us real specs to budget against.

2. **The stage-1 README documents two model limitations itself:**
   - the tail is treated as a virtual ground (about 0.4 dB gain error);
   - there is no Ioutn→Ioutp coupling, so the mirror pole is missing and PM is overestimated by about 29° × (f_u / f_mirror).

   This confirms §0.3. S1 must read the net0 sensitivity from level 0/1, not from the level-2 transfer function.
