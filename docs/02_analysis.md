# Phase 2: Critical analysis and research

**Project:** Analog layout automation, S0–S3
**Date:** 2026-10-23
**Inputs:** `docs/01_inventory.md` and its addendum, `docs/context/project_context_S0-S9.md` (your stage definitions), the ChatGPT plan, the 7 papers, and a web and GitHub survey done today.

**Ground rules for this document**
- Every factual claim about an external tool or paper is cited (see §7).
- Anything I could not verify is marked **UNVERIFIED**.
- My recommendations are marked **REC**.

---

## 0. Summary

1. **The ChatGPT plan's overall structure is sound and I keep it.**
   - It separates a tool-independent research IR from tool-specific syntax.
   - It separates hard constraints from soft priorities.
   - It labels every number as *verified*, *estimated* or *not evaluated*.
   - It sets up A/B/C comparison branches and requires negative tests.

   What I change is the toolchain and the scope, because three of its assumptions do not hold for us (items 2–4).

2. **The plan made ALIGN-SKY130 the main platform. That is too risky as the *only* physical engine.**
   - ALIGN is installable: there is a PyPI wheel, `align-analoglayout 0.9.8`, for Python 3.10–3.13 [A1].
   - ALIGN-pdk-sky130 maps ALIGN's "M1" layer onto SKY130 `li1`. It ships dummy `.model` cards. It has open issues on off-grid, spacing and elongated-transistor DRC errors [A2].
   - ALIGN's own SKY130 CI step runs Magic with a simplified tech file whose DRC section is empty [A3].
   - I found **no public evidence of DRC- or LVS-clean ALIGN SKY130 output** checked against the real `sky130A` decks (UNVERIFIED either way).

   **REC:** keep ALIGN as the *automatic place-and-route baseline* (branch A) and as one constraint consumer. Do not make it the only route to a legal SKY130 layout.

3. **Add gLayout as the SKY130 device and primitive generator for S3.** This is what your own project context already prefers ("GLayout/gdsfactory: physical device and geometry generation").
   - MIT licence, `pip install glayout` (0.2.0) [G1].
   - Natively supports `sky130A` and `gf180mcuD`.
   - Has `nmos`/`pmos` cells with fingers and multipliers, a common-centroid `diff_pair`, interdigitated two-transistor cells, current mirrors and tap rings [G2].
   - Ships its own Magic/KLayout DRC and Netgen LVS hooks [G3].

4. **MAGICAL: start it in parallel as you asked, with a realistic expectation.**
   - It has been dormant since September 2021 and needs Python 3.7, gcc 6 and Boost 1.62 [M1].
   - Its device generator is hard-wired to TSMC 40 nm layers and rules [M2]. No SKY130 port exists publicly (UNVERIFIED, since GitHub code search was unavailable).
   - ICPI's "MAGICAL with extended PDK support" is not public. Its repository is a PDK-free synthetic demo [I1].

   **REC:** run MAGICAL's `ota1` on its mock PDK in its own Docker image, and run *our* OTA through it on the mock PDK. This proves that our S2 compiler can drive a second engine (`.sym` and `.symnet` files). A SKY130 port is out of scope this week.

5. **The input data force a change to S1.**
   - The plan's S1 needs a DC operating point, specs and transistor-model SPICE perturbations. We have none of these: you confirmed dummy sizes and no specs.
   - What we *do* have, and the plan does not use, is a set of exact symbolic equations that map level 2 down to level 0.

   **REC:** compute sensitivities **analytically** by differentiating those equations with SymPy. Validate them by **perturbing the linear small-signal netlists** in ngspice; these netlists need no PDK models. Add a fixed **import slot** so Monday's nodal-analysis results replace the placeholder values without any code change.

6. **The novelty claim needs one new citation.**
   - arXiv 2610.28677 (19 Oct 2026, McMaster) has a "parasitic-budget agent". It converts pre-layout margin into per-net budgets, but by *numerical parasitic injection and re-simulation*. Its symbolic analysis (SLiCAP and SymXplorer) is used separately, for transfer functions, and is not used to set budgets [P1].
   - The classic work, Charbon et al. 1994 and Malavasi et al., already bounds parasitics from performance sensitivities [P2, P3].

   **Defensible novelty:** *hierarchical, symbolic* sensitivities that are traceable to primitive-level elements. These are compiled automatically into engine-independent constraints and budgets in an open SKY130 flow.

7. **Scope for Sunday.** The ChatGPT S0–S3 plan budgets 7 development days; we have about 2.5. The plan in Phase 3 keeps every stage, but each with a minimum viable acceptance gate. The LLM branch C becomes a defined hook with a validator, not a critical-path experiment.

---

## 1. How the ChatGPT plan compares with the literature and current tools

| Plan element | Literature / state of the art | Verdict |
|---|---|---|
| Research IR (intent, budgets, constraints_ir) kept separate from tool syntax | PANDA writes per-stage JSON artefacts [PANDA §4.1]. ICPI uses a structured layout state [ICPI §III-B]. ALIGN abstracts the PDK to JSON [ALIGN §2.2]. | **Keep.** This is what lets ALIGN, MAGICAL and gLayout share one S2. |
| Hard/soft split, plus verified/estimated/not-evaluated labels | Vibe Tapeout found agents reporting *false passes*: LVS passing with missing connections, and Magic extraction lumping coupling capacitance to ground [VT §III-D, §VI-E]. | **Keep and strengthen.** Each acceptance check runs as code, independently of the generator that produced the result. |
| Budget = η·margin / \|S\| | Charbon '94 [P2] and ALIGN's "electrical constraints" [ALIGN §2.3] use the same idea. ALIGN translated budgets into wire length, track count and via count, but left it work in progress. | **Modify** (§3.3). We have no margins yet, so use normalised sensitivities and relative budgets. Allocate one *shared* margin across nets instead of giving each net the full margin. Keep the per-unit wire parasitics needed to convert a budget into a length. |
| Sensitivities by central finite difference on the transistor-level SPICE | — | **Replace for now.** Without an operating point this is impossible. Use analytic SymPy derivatives plus linear-netlist perturbation (§3.2). Keep the transistor-level method for when real sizing arrives. |
| ALIGN-SKY130 as the main engine | Facts in §2.1. | **Modify.** ALIGN becomes branch A and a constraint consumer. gLayout becomes the S3 generator. |
| "Do not write a new MOSFET generator; characterise ALIGN's first" | gLayout already provides verified SKY130 generators [G2]. Open-ALOE's SKY130 stem cells show the same "PDK-correct cells first" approach [ALOE §III.A]. | **Keep the principle, change the generator.** Characterise *both*, and gate on real `sky130A` Magic DRC. |
| A/B/C branches (default / analytical / LLM) | ICPI shows its LLM agents beating BO and heuristics only with a carefully *controlled* evaluation budget [ICPI Table II]. | **Keep A and B as experiments in S0–S3.** **Defer C's experiment** and implement only its validated interface. |
| 10-day and 7-day schedules | — | **Replace** with the 2.5-day schedule in Phase 3. |
| LLM via Codex or Claude CLI with JSON schemas | The Vibe Tapeout agents and ICPI both use fixed schemas [ICPI §III, VT §III-B]. | **Keep** for branch C later. Nothing in S0–S3 depends on an LLM. |

---

## 2. Tool survey and reuse recommendations

### 2.1 Comparison table

| Tool | Licence | State (2026-10) | SKY130 status | Role for us | Risks |
|---|---|---|---|---|---|
| **IIC-OSIC-TOOLS `2026.10`** | Apache-2.0 | Tag published 2026-10-15 [T1] | `sky130A` via open_pdks, plus magic, netgen, klayout, ngspice, gdsfactory, cace, ciel [T2] | **The execution environment.** A separate container from the same image, as you asked. | Exact tool versions in 2026.10 are UNVERIFIED; capture them in S0. No ALIGN (removed in 2024.05) and no gLayout [T3]. |
| **gLayout** | MIT | Active, v0.2.0 (2026-05) [G1] | Native (`sky130_mapped_pdk`) | **S3 device and primitive generator.** Optionally a simple S4 placer later. | gdsfactory version pin vs. the image's system gdsfactory (UNVERIFIED), so use a venv. Open issues: c_route via regression (#93), dummy transistor layout (#79) [G4]. |
| **ALIGN-public + ALIGN-pdk-sky130** | BSD-3 | 0.9.8 on PyPI (2026-06-18); public commits through 2026-09 [A1] | Abstraction exists, but "M1" is `li1`, the `.model` cards are dummies, and DRC issues #10–#12 are open [A2] | **Branch A baseline** (automatic topology recognition and PnR). **Constraint consumer** (`.const.json`). | Pins `pydantic<2` (use a venv). Needs COIN-OR libraries on Ubuntu 24.04. Its netlists require W to be a multiple of 210 nm [A2]. Real-deck DRC/LVS is unproven. |
| **MAGICAL** | BSD-3 | Dormant since 2021-09 [M1] | None. TSMC40 layers are hard-coded [M2]. | **Algorithm reference** and **second constraint consumer** (`.sym`/`.symnet`) on its mock PDK. | Docker image `jayl940712/magical` is about 5 years old. Needs Spectre-syntax netlists. Device names must be `nch`/`pch` [M2]. |
| **BAG3/BAG3++** | Apache/BSD | Tied to Cadence Virtuoso; the SKY130 primitive library was archived in 2026-04 and targets the NDA S8 PDK [B1] | — | **Reject** | Needs Cadence. |
| **PANDA code** | PolyForm Noncommercial | Single commit; needs Virtuoso, Spectre and Calibre plus a T65 PDK [PA1] | — | **Ideas only:** per-stage JSON, pin-list sync. | Licence and proprietary tools. |
| **ICPI demo** | Not stated | Synthetic, PDK-free [I1] | — | **Ideas for S4/S8:** five action families, design journal, rollback. | No real engine. |
| **Magic / Netgen / KLayout** | GPL / GPL / GPL | Inside the image | Official `sky130A` decks | **Independent verification** in S3 and later S6 | Known pitfalls in §2.3. |
| **SymPy (+ SymMNA)** | BSD / — | Already used by your stage 1 | n/a | **S1 sensitivities** | Expression growth on larger circuits. Fine for the 5T OTA. |

### 2.2 What I recommend reusing, and why

- **Reuse your own stage-1 outputs as the S1 source of truth:** `hierarchy.json`, `primitives.json` and `equations.json`.
  - They already contain the block structure that ALIGN and MAGICAL try to *infer*, using a GCN, graph isomorphism or spectral similarity [ALIGN §2.1, MAGICAL].
  - Re-inferring them would throw away your strongest asset.
  - ALIGN's own auto-annotation then becomes a *comparison* in branch A: does ALIGN recognise the same blocks?
- **Reuse your repo's container pattern:** Python on the host, tools through `docker exec` into IIC-OSIC-TOOLS (`src/analog_sizing/container.py`, Apache-2.0).
  - I will either import it or follow the same pattern for a container named `layout-s0s3`, so the two projects behave the same way.
- **Reuse gLayout's generators.** Do not write MOSFET polygons ourselves.
- **Reuse ALIGN's `.const.json` schema** as one compiler target. Its constraint types map one-to-one onto what S1 produces:
  - `SymmetricBlocks`, `SameTemplate`, `GroupBlocks`, `NetConst`/`NetPriority`, `PortLocation`, `Order` [A4]
- **Reuse ICPI's five knob families** (net weights, placement bias, symmetry, routing priority, wire widths) as the vocabulary for the *engine-neutral* constraint IR [ICPI Table I]. This is what S4+ will tune.

### 2.3 Licensing and compatibility risks

| Risk | Impact | Mitigation |
|---|---|---|
| PANDA is PolyForm Noncommercial | We cannot copy its code into an Apache or MIT project | Ideas only. Copy no code. |
| ALIGN pins `pydantic<2`; gLayout and the image have their own pins | Dependency conflicts | **One venv per engine** inside the container (`/foss/designs/.venv-align`, `.venv-glayout`), versions pinned in `requirements-*.txt`. |
| MAGICAL needs Python 3.7 and gcc 6 | Cannot share the image | Use its own Docker image, run only on the mock PDK, and label results "mock PDK, not SKY130". |
| ALIGN's SKY130 layer mapping (`li1` as M1) | GDS may fail real DRC | Gate *every* GDS on `sky130A` Magic DRC with `drc(full)`. Record failures; do not fix ALIGN this week. |
| Magic extraction false passes | Wrong parasitics later | Not an S0–S3 issue. Noted in the S3→S4 handoff: when extracting, use `ext2spice cthresh 0 rthresh 0` and `extract do coupling`, never the `lvs` preset [X1]. Add the sconnect check for well and tap connectivity [X2]. |
| I cannot reach your Docker from my side | I cannot run container steps myself | See §5. This decision belongs to Phase 3. |

---

## 3. Stage-by-stage verdicts

Each stage is compared with your definitions in the project context (§4) and the ChatGPT S0–S3 plan.

### S0: Input and PDK integration → **MODIFY**

**Keep:**
- freeze the reference netlist with a hash
- a device and parameter manifest
- `circuit_ir.json`, `device_map.json`, `pdk_config.yaml` (your names)
- a tool-version manifest
- negative tests

**Change:**
1. **Ingest from your stage-1 outputs, not from ALIGN's example.**
   - Source: `5t-ota_primitives.spice` plus `primitives.json`, cross-checked against `topologies/5t-ota/circuit.spice`.
   - The ChatGPT examples use ALIGN's circuit (M0–M5, VOUT, NET8), which differs from ours (XM1–XM6, Voutp, net0) [Inventory §0.4].
2. **Make S0 engine-independent.** Engine adapters translate `circuit_ir.json` into:
   - ALIGN SPICE: W as a multiple of 0.21 µm, `nf`, X-instances [A2]. Our W = 1 µm is *not* a multiple of 0.21 µm, so S0 must **flag this, not silently round it**. **ASSUMPTION** to confirm with you: for ALIGN only, we round to 1.05 µm and record the deviation.
   - MAGICAL Spectre: `nch`/`pch`.
   - gLayout parameters.
3. **The environment check is part of S0.** Record the versions of the image, magic, netgen, klayout, ngspice and `sky130A`, then run a DRC/LVS smoke test on one gLayout `nmos`. Without this, nothing downstream is trustworthy.
4. **Drop "reproduce ALIGN's own OTA" as the S0 gate.** It becomes a smoke test of the ALIGN install. It does not test our flow.

### S1: Electrical intent → **MODIFY substantially**

**Keep:**
- block, matching and critical-net outputs with evidence
- `intent.json` and `sensitivity.json`
- symbolic-vs-SPICE validation
- the rule "S1 must compute the ranks, not assume them"

**Change:**

1. **Structural intent is deterministic and comes from your hierarchy.** For example:
   - Diff pair X2 {XM3, XM4} is a symmetric pair because its model has mirror-image twins ("twins must be identical transistors", stage-1 README).
   - Mirrors X1 {XM1, XM2} and X3 {XM6, XM5} form ratio groups.

   Each matching record carries its evidence (primitive class, twin rule, equal W/L/nf/m) and a matching purpose. Your project context defines matching as part of S1.

2. **Quantitative intent uses analytic sensitivities from `equations.json`.** We map each *physical net* to the *symbols* that a layout parasitic on that net adds to. This **net→symbol parasitic map** is the new artefact that connects electrical and physical design:

   | Net | Where layout capacitance lands | Metrics affected |
   |---|---|---|
   | Voutp | C to ground → `CL` (equivalently C4_X1) | GBW, PM (output pole) |
   | Voutp–Vinn coupling | Adds to C6 (feed-forward zero G2/C6) | PM |
   | net0 | C to ground → `C1_X1_X1` (mirror gate node) | **Mirror pole, so PM.** This is *not visible at level 2* (Inventory §0.3, stage-1 README), so it is evaluated from the level-1 model. |
   | Vinp/Vinn | Input capacitance: C1/C3 | Visible only with a source impedance. Flagged. |
   | net1 (tail) | Common-mode only; a virtual ground in DM | **Not observable** in the current models. Flagged as a gap (needs a CM model). |
   | Iref, VDD, VSS | Bias and supply | Out of scope for the DM model. Rails get low-impedance routing by rule. |

   - Sensitivities are `S = ∂M/∂C` and the normalised `Ŝ = (∂M/∂C)·(C_ref/M)`, for M in {A0, GBW, PM}, computed with `sympy.diff` and evaluated at the operating values.
   - **Validation:** perturb the same linear netlists in ngspice (these are the decks `verify.py` already builds) with +δC on the net, for at least two δ values, and compare the sign and magnitude. This needs no PDK models, so it works today.

3. **Operating values are placeholders now and real later.**
   - Today: the dummy values `verify.py` uses (C 1–10 fF, G 50–500 µS, R 20–200 kΩ, CL = 1 pF), each tagged `PLACEHOLDER`.
   - Monday: your nodal-analysis results are loaded through one documented input file, `inputs/operating_values.json`, with the schema fixed in Phase 3. Nothing else changes.

4. **Drop for now:** DC-operating-point extraction from transistor-level ngspice. There is no sized design, and the plan's own S1.1 inputs list it as coming from "O1/O2 or fixed OTA example".

### S2: Constraint generation → **MODIFY**

**Keep:**
- hard/soft/budget/LLM-proposal classes
- three output layers: budgets, engine-neutral IR, engine files
- incremental B1/B2/B3 experiments
- three-level validation: correctness, effectiveness, usefulness
- negative tests

**Change:**

1. **One IR file using your name, `constraints.json`.** It contains the hard constraints, soft priorities and budgets, each with provenance and status. Engine files are *derived* from it:
   - `5t_ota.const.json` for ALIGN
   - `.sym`/`.symnet` for MAGICAL
   - a gLayout parameter file
2. **Budgets without specs.**
   - Each metric gets a relative degradation allowance, ε_M. **ASSUMPTION**, placeholder: GBW 10%, PM 5°, A0 0.5 dB.
   - That allowance is split across nets in proportion to their sensitivity: `ΔC_k = w_k·ε_M/|S_k|`, with Σ w_k = 1. This replaces giving each net the full margin, which the plan itself warns against.
   - When Monday brings specs, ε_M becomes `η·(M_nominal − M_min)`.
3. **Budget → geometry hint.**
   - Using `sky130A` per-unit wire capacitance (area plus fringe for met1/met2, from the PDK's Magic tech or capacitance tables), translate each ΔC budget into a **max wire-length hint** per layer. This is the step ALIGN described but did not implement [ALIGN §2.3].
   - **If per-unit capacitance values are missing or uncertain, they are flagged; I will not invent them** (§6).
4. **Criticality is derived from the sensitivity ranking:**
   - ALIGN: `NetConst.criticality` / `NetPriority.weight`
   - ICPI-style: `net_weight`
5. **What is checked at S2:**
   - **Correctness:** every name resolves, no conflicts, units are present.
   - **Consumption:** ALIGN parses the file and runs `--flow_stop 2_primitives` without error; MAGICAL reads the `.sym` files.
   - Geometric *effectiveness* is checked only where an engine actually places devices (ALIGN full flow, MAGICAL mock PDK). These are reported as diagnostics, not gates.

### S3: Device generation → **REPLACE the generator, keep the gate**

**Keep:**
- device-equivalence report
- variants V0/V1/V2
- per-primitive DRC/LVS
- pins and bounding boxes
- "retain several candidates, not just the smallest"

**Change:**

1. **Generator: gLayout, per hierarchy block.**

   | Block | Variants |
   |---|---|
   | X2 diff pair | V0 = simple two-device; V1 = common-centroid `diff_pair`; V2 = interdigitated |
   | X1 PMOS mirror, X3 NMOS mirror | V0 = side by side; V1 = interdigitated |

   Fingers are explored *only* where the W/L/nf/m equivalence holds. With nf = 1 and W = 1 µm, the legal finger set is {1} unless we interpret W as total width. **ASSUMPTION:** W is total width, as in the sky130 `nfet_01v8` symbol convention. Flagged for you to confirm.

2. **Gate: real `sky130A` checks for every variant.**
   - Magic DRC with `drc(full)` and 0 errors.
   - Netgen LVS of the primitive against its slice of `circuit_ir.json` reports "match uniquely" with no property errors. **I parse the report text, not the exit code** (lesson from Vibe Tapeout).
3. **ALIGN's `2_primitives` is kept as a comparison column.** Its GDS also goes through Magic DRC, and the results are recorded honestly.
4. **Output:** `variants.json` (your name). Each variant records:
   - cell name, GDS path
   - bounding box and area
   - pin coordinates and layers
   - device-equivalence status
   - DRC/LVS verdicts with log paths
   - a rough parasitic estimate (diffusion area AD/AS/PD/PS from gLayout geometry, or "not evaluated")
   - which S1 constraint each variant satisfies

   This is exactly what S4 needs to choose among variants.

---

## 4. What I am deliberately *not* doing in S0–S3

- Porting MAGICAL to SKY130. That is infrastructure work, not your contribution, and the ChatGPT plan agrees.
- Fixing ALIGN's SKY130 DRC issues.
- Running the LLM branch C experiment. Only the interface and validator are built.
- Common-mode, PSRR or noise sensitivities. These need models that do not exist yet.
- Full-circuit PnR as a deliverable. ALIGN and MAGICAL full runs appear only as diagnostics.

---

## 5. One open infrastructure decision (needed before Phase 3 is final)

My shell on your PC is an isolated Linux VM. It sees the connected folders but **cannot reach Docker Desktop**. Three options:

| Option | How it works | Pros | Cons |
|---|---|---|---|
| **(a) You run, I read.** | I write `scripts/run_stage.ps1 S<n>`, which uses `docker exec` into container `layout-s0s3`, created from `hpretl/iic-osic-tools:2026.10` with the repo mounted. You run one command per stage; the outputs land in the repo, where I read and verify them. | Exactly your environment; reproducible for you later | Every tool run needs you |
| **(b) I mirror the tools.** | With your approval, I install the same tool set in my cloud workspace (ngspice, magic, netgen, klayout, the `sky130A` PDK via ciel at the same open_pdks version, gLayout, ALIGN), develop and test there, and you do the final acceptance run in your container through (a). | I can iterate on my own; fastest for Sunday | Possible version drift, so S0 records both version sets and the acceptance run in your container is what counts |
| **(c) Install in the VM.** | Same as (b), but inside the VM on your PC | Files are local | Heavy (PDK is several GB); egress rules unknown |

**REC: (b) + (a).** I develop in the cloud with pinned versions, and the acceptance gates run in your `layout-s0s3` container. I will ask for approval before installing anything.

---

## 6. Data I still need, or will mark as ASSUMPTION

| Item | Needed by | Default if you don't provide it |
|---|---|---|
| Relative degradation allowances ε (GBW, PM, A0) | S2 | GBW 10%, PM 5°, A0 0.5 dB (**ASSUMPTION**) |
| W convention (total vs per-finger) | S0, S3 | Total width (**ASSUMPTION**) |
| ALIGN W rounding (1 µm → 1.05 µm, ALIGN only) | S0 | Round and log it (**ASSUMPTION**) |
| `sky130A` per-unit wire capacitance | S2 | Read from the PDK inside the container. If not found, flag it and do not guess. |
| Monday's nodal-analysis format | S1 import slot | I define the schema; you map to it |

---

## 7. Citations

**Papers in your folder**
- **[ALIGN]** Dhar et al., *ALIGN: A System for Automating Analog Layout*, arXiv:2008.10682 (§2.1 annotation, §2.2 PDK abstraction, §2.3 electrical constraints).
- **[MAGICAL]** Chen et al., IEEE D&T 38(2), 2021.
- **[ALOE]** Li et al., *Open-ALOE*, ISQED 2025.
- **[AICL]** Bio et al., *AICL Co-pilot*, SMACD 2026 (Listing 1: 5T-OTA relative placement).
- **[PANDA]** Zhang et al., arXiv:2606.15052 (Table 2: UGB 10.84 → 4.19 MHz after layout).
- **[ICPI]** Liu et al., arXiv:2608.13767 (Table I action families; Table II results).
- **[VT]** Yoshioka, arXiv:2610.15240 (§III-D, §VI-E false passes).

**Web, checked 2026-10-23**
- **[P1]** Noori Zadeh et al., *Multi-Agent AI Design of a Nanowatt Biomedical Low-Pass Filter*, arXiv:2610.28677 — https://arxiv.org/html/2610.28677
- **[P2]** Charbon et al., ERL M94/40, 1994 — https://www2.eecs.berkeley.edu/Pubs/TechRpts/1994/ERL-94-40.pdf
- **[P3]** Malavasi et al., *Automation of IC Layout with Analog Constraints* — https://infoscience.epfl.ch/record/85458
- **[A1]** https://pypi.org/project/align-analoglayout/ (0.9.8, 2026-06-18, Py ≥ 3.10, BSD-3); https://github.com/ALIGN-analoglayout/ALIGN-public
- **[A2]** https://github.com/ALIGN-analoglayout/ALIGN-pdk-sky130 (`layers.json`, `gen_param.py`, `models.sp`; issues #8, #10, #11, #12)
- **[A3]** https://github.com/ALIGN-analoglayout/ALIGN-public/blob/master/.github/workflows/benchmark.yml and `benchmarks/magic_tech/SKY130_PDK`
- **[A4]** https://github.com/ALIGN-analoglayout/ALIGN-public/blob/master/align/schema/constraint.py
- **[M1]** https://github.com/magical-eda/MAGICAL (last commit 2021-09-10; Dockerfile)
- **[M2]** https://github.com/magical-eda/MAGICAL/blob/master/flow/python/DesignDB.py ; https://github.com/jayl940712/device_generation
- **[I1]** https://github.com/bingyang1132/ICLAD2026-demo-sim-aware-in-context
- **[G1]** https://pypi.org/project/glayout/
- **[G2]** https://raw.githubusercontent.com/idea-fasoc/OpenFASoC/main/openfasoc/generators/glayout/README.md
- **[G3]** https://raw.githubusercontent.com/ReaLLMASIC/gLayout/main/src/glayout/pdk/mappedpdk.py
- **[G4]** https://github.com/ReaLLMASIC/gLayout/issues
- **[T1]** https://hub.docker.com/r/hpretl/iic-osic-tools/tags
- **[T2]** https://github.com/iic-jku/IIC-OSIC-TOOLS
- **[T3]** https://raw.githubusercontent.com/iic-jku/IIC-OSIC-TOOLS/main/RELEASE_NOTES.md
- **[B1]** https://bag3-readthedocs.readthedocs.io/en/latest/new_pdk_setup/ ; https://github.com/google/skywater-pdk-libs-sky130_bag3_pr
- **[PA1]** https://github.com/PKU-IDEA/PANDA
- **[X1]** http://opencircuitdesign.com/magic/commandref/ext2spice.html ; http://opencircuitdesign.com/magic/commandref/extract.html
- **[X2]** https://github.com/d-m-bailey/sconnect_for_sky130_magic

---

## Addendum A (2026-10-23): Switching to the sized OTA, Docker access, ALIGN-first, and ALIGN+LLM prior art

### A1. Can we use the sized `example_ota_5t` with the `5t-ota` hierarchy?

The two circuits are **not identical**. Here is how they line up.

**Device mapping**

| Role | `5t-ota` (dummy) | `example_ota_5t` (sized) |
|---|---|---|
| Diff pair | XM3/XM4: 1/0.15 | M1/M2: 24/0.5 |
| PMOS mirror load | XM1/XM2: 1/0.15 | M3/M4: 8/1 |
| Tail | XM5, mirrored from diode XM6 with port Iref | M5: 24/1, gate held by internal source V1 = 0.75 V |
| Bias reference | XM6 | **none** |

**Net mapping**

| `5t-ota` | `example_ota_5t` |
|---|---|
| Vinp / Vinn / Voutp | INP / INN / OUTP |
| net0 | net3 |
| net1 | net1 |

**What carries over**

- The **differential-mode equations carry over exactly.**
  - In DM the bias block X3 sits entirely on GND. Its Iout is the tail, and the tail is a virtual ground.
  - So A0, GBW, PM and the net→symbol map do not depend on how the tail is biased.
- The **structural hierarchy carries over** for the pair and the load mirror.
- The **bias block does not carry over.** It becomes a single-device "tail source" block with an external bias.

**What does not work directly**

Running stage 1 itself on `example_ota_5t` would fail as it stands, for two reasons:
- `extract-primitives.py` rejects a voltage source.
- It has no single-transistor bias primitive to match M5.

**REC: use the sized netlist, with its specs, as the S0–S3 design.**

- Reuse `hierarchy.json` and `equations.json` through an explicit, checked **name map**. Mark the bias block as `manual-mapping (ASSUMPTION)`.
- This gives us real specs: gain ≥ 30 dB, GBW ≥ 20 MHz, PM ≥ 60°, CL = 1 pF.
- It also gives real measured pre-layout values: 31.7 dB, 104 MHz, 81°.
- A `.op` run with sky130 models gives the real gm, gds and capacitances. That replaces the dummy values.

### A2. Why I cannot reach Docker, and what would fix it

My shell on your PC is an isolated Linux VM. It can see only the connected folders, and it has no path to the Docker Desktop daemon (a Windows named pipe) or to WSL.

| Option | What you do | Notes |
|---|---|---|
| **1. Local shell MCP server in Claude Desktop** | Add a local MCP server that can run commands on Windows (for example, a "desktop commander"-type server), restricted to `docker` if the server supports an allow-list | Claude Desktop proxies local MCP servers into this session. I could then run `docker exec layout-s0s3 ...` myself. Security: this grants command execution on your PC, so restrict it. |
| **2. Docker MCP Toolkit** | Docker Desktop → MCP Toolkit → Clients → Connect Claude Desktop | Officially supports Claude Desktop. I found **no catalog server that runs `docker exec` on your own containers** (UNVERIFIED). |
| **3. You run, I read** | Run one PowerShell line per step that I give you | Always works. Outputs land in the repo, where I verify them. |

**Cloud mirror.** I would *not* pull the 17 GB image. I would install only ALIGN (pip), magic, netgen, ngspice and `sky130A` via ciel, which is a few GB. It is still a version-drift risk and setup time, so it becomes **unnecessary if option 1 works**.

### A3. Is there prior work that wraps ALIGN with an LLM, the way ICPI wraps MAGICAL?

Searched 2026-10-23. **None found** in which LLM agents tune ALIGN's constraints or placer knobs from post-layout feedback.

**Closest work that uses ALIGN**

- **AutoSizer** (arXiv 2602.02849, BNL; https://github.com/yuxi120407/AutoSizer).
  - Its LLM loop tunes *sizing*.
  - Its optional full-flow mode runs ALIGN `schematic2layout.py` with ALIGN-pdk-sky130, then Magic PEX and ngspice.
  - Its README notes that ALIGN works for "a subset of circuits (simple OTAs and amplifiers)".

**LLM layout-refinement works that use MAGICAL as the engine, not ALIGN**

- ICPI (2608.13767)
- LLANA (2406.05250; LLM-enhanced BO over net weights)
- LayoutCopilot (2406.18873)
- Post-layout-simulation-driven sizing (2310.14049)

**ML on ALIGN without an LLM**

- GNN hierarchical annotation (Kunal et al., TCAD 2023)
- The UMN parasitics-aware OTA sizing and layout work (ISQED 2026). That it uses ALIGN is UNVERIFIED.

**ICPI's own related work** groups ALIGN with MAGICAL as wirelength-centric generators and does not use it.

**Opportunity:** an ICPI-style act–observe–reflect loop over ALIGN's `.const.json` and placer options, on SKY130 with open Magic/Netgen/ngspice verification, appears **unclaimed**. This fits S4+ naturally.

### A4. Revised first step, as you asked

Before S0–S3 code, run **the complete ALIGN flow** and confirm it works.

1. Create container `layout-s0s3` from `hpretl/iic-osic-tools:2026.10`, with this repo mounted at `/foss/designs`.
2. Inside it, set up venv `.venv-align` with `align-analoglayout==0.9.8` (pinned) and clone ALIGN-pdk-sky130 at a pinned commit.
3. **Smoke test:** run ALIGN's own `five_transistor_ota`, all the way to a GDS.
4. **Our circuit:** convert the sized `example_ota_5t` to ALIGN SPICE.
   - W must be a multiple of 0.21 µm: 24 → 24.15 and 8 → 8.19 (**ASSUMPTION**, logged).
   - Add the PowerPorts/GroundPorts constraints.
   - Run the full flow to a GDS.
5. **View the result:** a KLayout PNG rendered in the container, plus the GDS opened in KLayout on Windows.
6. **Define "working":**
   - ALIGN exits with code 0, and the GDS is non-empty with the expected devices.
   - Then report Magic `sky130A` DRC and Netgen LVS **as status**. Failures are recorded, not hidden.
