# Project Context: Hierarchical LLM-Assisted Analog Netlist-to-GDS Automation

## 1. Overall research objective

We are developing a fully automated, open-source analog IC design framework with two connected research branches.

**O1/O2 — Automated electrical circuit design (separate ongoing project):**
- Automatic circuit hierarchy and building-block extraction.
- Bottom-up symbolic small-signal modeling using SymMNA and SymPy.
- SPICE validation of the analytical models.
- Inverse design to identify feasible ranges of gm/ID, channel length (L), and drain current (ID).
- Mixed-variable PSO for optimized transistor sizing and netlist generation.

Hierarchy extraction and symbolic modeling have already been developed. The feasible-range inverse-design stage remains a bottleneck.

**O3 — Our proposed physical-design research:**

Accept the optimized transistor-level SPICE netlist and automatically generate the smallest physically legal GDS layout that satisfies the electrical specifications **after parasitic extraction**.

Initially, O3 must preserve the optimized netlist without changing transistor sizing. Eventually, physical feedback may be returned to O1/O2 for joint electrical–physical optimization.

## 2. Main research direction and proposed novelty

Existing tools already perform automatic netlist-to-GDS generation, geometric area optimization, hierarchical placement, and post-layout optimization.

Therefore, simply combining an LLM with a placer/router or adding PEX feedback is not sufficiently novel.

Our main proposed contribution is:

**A hierarchical, electrically informed physical-design framework that automatically transforms symbolic circuit models and specification margins into quantitative physical constraints, then uses extracted parasitic information to diagnose and selectively correct physical structures responsible for post-layout performance degradation.**

We are investigating three connected contributions:

1. **Analytical-to-physical constraint compilation:** Automatically derive matching requirements, critical-net priorities, and parasitic budgets from validated hierarchical circuit equations and sensitivities.
2. **Hierarchical, specification-aware layout optimization:** Generate multiple local physical variants of circuit subblocks, coordinate their interface budgets, and optimize their global placement and routing.
3. **Targeted post-layout repair:** When a specification fails, use analytical sensitivities, PEX data, and counterfactual SPICE tests to identify likely responsible nets/subblocks and modify the relevant layout region instead of blindly regenerating everything.

These are research hypotheses that must be experimentally validated against existing methods. Sensitivity-based layout constraints, hierarchical optimization, and LLM refinement already have significant prior art.

## 3. Closely related existing frameworks

| Framework | Main contribution | Limitations relative to our goal |
|---|---|---|
| **MAGICAL (ICCAD 2019; IEEE D&T 2021)** | Automatic constraint extraction, device generation, analytical placement, geometric compaction, symmetry-aware routing, and GDS generation | Optimizes area, wirelength and geometric constraints, but its default flow does not implement our proposed symbolic-model-guided post-layout failure attribution |
| **ALIGN (DAC 2019; IEEE D&T 2021)** | Automatic SPICE hierarchy recognition, PDK abstraction, primitive generation, hierarchical constraint-driven placement/routing, and GDS | Strong existing analog PnR baseline; full real-PDK integration and comprehensive post-layout optimization depend on the configured flow |
| **PANDA (DAC 2026)** | LLM-coordinated topology generation (AnalogXpert), hierarchical Bayesian sizing (MOSTAR), LLM placement/routing planning, physical implementation, LVS/PEX and post-layout feedback | Closest system-level competitor; post-layout specification closure remains challenging in its published OTA demonstration |
| **BAG3++ (IEEE OJCAS 2025)** | Parameterized Python schematic/layout generators, hierarchical physical implementation and partial-layout extraction | Requires appropriate circuit-specific generators and practical EDA integration |
| **GLayout (MLCAD 2024 and open-source project)** | Python-based, PDK-aware analog layout primitives and generators, including SKY130/GF180 support | Not a universal autonomous netlist-to-GDS optimizer for arbitrary complex circuits |
| **ICPI (ICLAD 2026)** | LLM act–observe–reflect optimization of layout-generator parameters using simulation feedback | Strong competitor for our S8 repair agent; we need to demonstrate the additional value of verified physical-cause attribution |

Useful references:

- MAGICAL: https://github.com/magical-eda/MAGICAL
- ALIGN: https://github.com/ALIGN-analoglayout/ALIGN-public
- PANDA paper: https://arxiv.org/abs/2606.15052
- PANDA code: https://github.com/PKU-IDEA/PANDA
- BAG3++: https://doi.org/10.1109/OJCAS.2024.3502641
- GLayout: https://github.com/ReaLLMASIC/gLayout
- ICPI: https://arxiv.org/abs/2608.13767

## 4. Proposed architecture: S0–S9

| Stage | Responsibility | Main output |
|---|---|---|
| **S0 — Input and PDK integration** | Parse optimized SPICE, preserve hierarchy/connectivity, resolve transistor parameters, map devices to PDK generators | `circuit_ir.json`, `device_map.json`, `pdk_config.yaml` |
| **S1 — Electrical intent** | Import hierarchy, operating points and symbolic models; identify blocks, critical nets, matching requirements and sensitivities | `intent.json`, `sensitivity.json` |
| **S2 — Constraint generation** | Create hard physical constraints, soft priorities and quantitative parasitic budgets | `constraints.json` |
| **S3 — Device generation** | Produce legal physical transistor/passive variants with different finger and contact arrangements | Primitive GDS cells, `variants.json` |
| **S4 — Hierarchical placement** | Optimize local subblock layouts and select compatible global arrangements | `placements.json`, layout variants |
| **S5 — Performance-aware routing** | Connect devices and blocks, considering matching, critical-net parasitics, supplies, and routing legality | `candidate.gds`, `routing_report.json` |
| **S6 — Physical verification** | Run DRC, LVS and parasitic extraction in sequence | Verification reports, `extracted_rc.spice` |
| **S7 — Post-layout evaluation** | Evaluate gain, GBW, PM, power, noise, CMRR/PSRR, and applicable PVT/mismatch requirements | `metrics.json`, `feasibility.json` |
| **S8 — Optimization and repair** | Diagnose failed specifications, select bounded physical modifications, and generate improved candidates | `repair_plan.json`, updated candidates |
| **S9 — Final selection** | Select the smallest layout satisfying all required verified specifications | Final GDS, extracted netlist, results and optimization history |

## 5. Physical implementation and software

**Initial PDK:** SKY130A.

**Preferred implementation:**
- Python: central orchestrator and data handling.
- NetworkX: circuit hierarchy/connectivity graph.
- SymMNA/SymPy: electrical models and sensitivity information.
- GLayout/gdsfactory: physical device and geometry generation.
- Custom constrained placement/routing logic, borrowing ideas from ALIGN and MAGICAL.
- Magic or KLayout: geometric verification.
- Netgen: LVS.
- Magic: RC extraction.
- Ngspice/CACE: post-layout electrical characterization.
- Numerical optimizers: simulated annealing, NSGA-II or Bayesian optimization.
- LLM: selective reasoning and planning, not numerical geometry execution.

The main original engineering work is in S2, general hierarchical placement/routing coordination, and S8.

## 6. Hierarchical and parallel subblock optimization

A fully differential two-stage OTA is our main complex example.

It contains:

- Bias generation.
- First gain stage.
- First-stage CMFB.
- Second gain stage.
- Second-stage CMFB.
- Shared compensation and interstage connections.

Local workers can generate several layout alternatives independently for each block.

Each returns a GDS cell, area, pin coordinates, local verification results and parasitic estimates.

A global coordinator selects compatible variants, places the blocks, routes their shared connections and evaluates the completed circuit.

A local minimum-area layout is not necessarily globally optimal because external pin locations and interstage parasitics can degrade overall performance.

Separate LLM models are not required for every block. Logical agents may share one LLM while deterministic geometry-generation and evaluation workers run in parallel.

## 7. Failure handling and feedback loops

**DRC failure:** Stop before PEX. Repair illegal geometry by revisiting routing (S5), placement (S4), primitives (S3), or constraints (S2), depending on the cause.

**LVS failure:** Stop before electrical evaluation. Identify device/parameter or connectivity mismatches and repair the appropriate earlier stage. Keep the reference optimized netlist immutable.

**PEX/tool execution failure:** Classify separately from electrical specification failure and correct the extraction or simulation configuration.

**Electrical specification failure:** Use extracted RC information and circuit sensitivities to identify suspected critical parasitics or subblocks. Test hypotheses through counterfactual simulations, then propose legal local repairs. Reverify the assembled design.

**No feasible physical solution:** Escalate to the upstream O1/O2 sizing system and create a new netlist revision.

A local physical repair can reuse unaffected subblocks, but the complete modified design must undergo relevant top-level verification.

## 8. LLM contributions

The LLM has three main responsibilities:

1. **S1–S2:** Interpret circuit structure and help propose validated analog placement/routing constraints.
2. **S3–S5:** Propose subblock-specific physical strategies and coordinate local versus global design priorities.
3. **S8:** Interpret structured failure evidence and propose targeted physical repair actions.

The LLM does **not** directly perform SPICE calculations, numerical sensitivity derivation, transistor polygon generation, DRC, LVS, PEX or final feasibility verification.

The system must compare LLM decisions against non-LLM numerical and rule-based baselines to establish whether the LLM adds measurable value.

## 9. Research validation

Begin with a five-transistor OTA, progress to a two-stage OTA with CMFB, then an FDDA-based INA or another complex analog block.

Compare:

- Fixed conventional layout constraints.
- Area/wirelength-driven numerical optimization.
- LLM-guided constraints.
- Analytical sensitivity-guided constraints.
- Hierarchical electrical-budget coordination.
- Targeted post-layout repair.
- Additional LLM-assisted repair.

Main metrics are DRC/LVS pass rate, complete post-layout specification pass rate, minimum feasible physical area, number of PEX/SPICE evaluations, runtime, and performance on unseen circuit structures.

## 10. Implementation status and immediate next milestone

The architecture, research comparisons, stage definitions, implementation prompts, and illustrative OTA case-study presentations have been developed conceptually.

**There is not yet evidence in this discussion that the complete proposed physical automation system has been implemented or verified.**

Development should proceed through:

1. Verify the SKY130 open-source EDA environment.
2. Reproduce DRC/LVS/PEX/SPICE on a known OTA.
3. Implement deterministic fixed-netlist-to-GDS generation.
4. Add automatic analytical physical constraints.
5. Introduce hierarchical layout optimization.
6. Add PEX-based diagnosis and targeted repair.
7. Add bounded LLM planning and evaluate its benefit.
8. Integrate feedback with the upstream gm/ID–PSO optimizer.

**Immediate priority:** Establish a real, DRC/LVS-clean, extracted-SPICE-validated SKY130 OTA layout before developing the complete LLM-agent system.

The overarching goal is not merely automated GDS generation, but achieving **minimum-area post-layout specification closure through electrically informed physical decisions and efficient targeted repairs**.
