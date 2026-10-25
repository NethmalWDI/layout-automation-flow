# Final plan: critical review, novelty, and the S0–S9 flow

**Date:** 2026-10-24
**Purpose:** a consolidated, critical re-analysis of the whole project. It covers:

- where we came from
- where we are now
- what the literature allows us to claim
- what each stage must do and why
- what can go wrong

This document **supersedes** the stage definitions in `03_plan_S0-S3.md` and refines the novelty in `05_literature_novelty_remap.md`. Literature evidence is in `05`, §1 and §11.

---

## Part A — Past and present

### A1. What was planned before (ChatGPT plan), and how it holds up

| Plan element | Verdict now | Reason (evidence from our runs or the literature) |
|---|---|---|
| ALIGN-SKY130 as the main physical engine | **Rejected as engine.** Kept only as a baseline on circuits with L = 0.15 µm. | Step 0: ALIGN-pdk-sky130 draws a **fixed 0.15 µm gate** and quantises W in 210 nm "fins". Our sized OTA came out DRC-clean, but **LVS shows L property errors**: it is not the designed circuit (`progress_log.md`). |
| MAGICAL as the reference engine | **Removed from the active plan.** Kept as a literature and algorithm reference. | It runs only on a TSMC40-style mock PDK, so its results cannot be compared with SKY130 post-layout results. It cost a 7.4 GB image and also contributed to the Docker lock-up. |
| gLayout for S3 | **Rejected as device generator.** | It re-implements transistors from generic rules; it is not the PDK PCell (`04_device_generation.md`). Its pinned dependencies (numpy ≤ 1.24, gdsfactory ≤ 7.7) also fail on the image's Python 3.12. |
| Budget = η·margin/\|S\| per node | **Kept, but made rigorous.** | Allocating the margin one node at a time double-counts it. A *joint* allocation is required (see B2). |
| LLM as constraint planner, not as layout engine | **Kept, and strengthened.** | Every positive result in the literature keeps a deterministic engine underneath (PANDA, ICPI, LayoutCopilot). LLM-written coordinates fail (ACDC). |
| Hard/soft/budget labels, provenance, independent verification, negative tests | **Kept.** | Vibe Tapeout's false passes. Our own Step 0 found false LVS failures from units and missing ports, which only showed up because we checked independently. |

### A2. What we have established (facts, not plans)

1. **Magic's SKY130 PDK PCells reproduce our devices exactly.** M1 extracts as `w=24 l=0.5 ad=6.96 pd=48.58`, identical to the xschem netlist. This is the right foundation for a PCell-exact flow.
2. Our verification scripts work on Magic DRC (`drc(full)`) and Netgen LVS. The DRC script includes a negative control that proves the checker is live.
3. **The upstream symbolic models have known gaps** (stage-1 README, our inventory):
   - differential mode only, with the tail treated as a virtual ground;
   - the level-2 amplifier template drops the mirror pole (Ioutn → Ioutp coupling);
   - matching is first-order in s;
   - there are no mismatch or noise sources.
4. **The sized 5T OTA has very large margins on the specs that layout affects:**

   | Spec | Achieved | Required |
   |---|---|---|
   | GBW | 104 MHz | 20 MHz |
   | PM | 81° | 60° |
   | Gain | 31.7 dB | 30 dB |

   Gain is the tight one, and gain is almost insensitive to layout capacitance. **Consequence:** this circuit cannot demonstrate the value of the method (see B6).
5. **Infrastructure:**
   - The container flow works.
   - Running several heavy jobs in parallel froze Docker Desktop.
   - The MCP bridge has a 60 s call limit, so long jobs must run in the background.

### A3. What the literature allows us to claim

This is summarised from `05`, §2.

**Already published (cannot be claimed):**
- spec → parasitic bounds through linearised sensitivities (Choudhury '93; Charbon '93/'94)
- mismatch bounds
- bound-driven shielding (Kirkpatrick '94)
- guard-ring need from substrate bounds (Miliozzi '96)
- EM-width routing (Martins '14; SAGERoute '23)
- topology-based symmetry extraction (ALIGN, GANA, AncstrGNN)
- CC/ID pattern choice (Madhusudan, Sharma '21)
- variant-selecting placement (Grus '23)
- per-net budgets in an open-PDK LLM flow, obtained by parasitic injection (Noori Zadeh et al., arXiv 2610.28677)
- LLM-generated constraints (PANDA, LayoutCopilot, ICPI)

**Gap.** No published flow does both of the following:
- (i) uses **hierarchical symbolic small-signal models** to decompose spec margins into **block-local budgets before layout**;
- (ii) uses those budgets to choose **PDK-PCell options** and to **pre-screen sub-block layout variants without full-circuit simulation**.

---

## Part B — Critical analysis (the professor's view)

### B1. Is "symbolic instead of numeric sensitivity" a real contribution?

**On its own, no.** A reviewer will say, correctly, that for a 6-transistor OTA a finite-difference sweep takes seconds, so the choice of method is an implementation detail.

The contribution has to come from what symbolic and *hierarchical* models enable that flat numerical ones do not:

1. **Hierarchical budget decomposition.**
   - The level maps in `equations.json` express each block's port elements in terms of the elements of the level below.
   - So a top-level margin can be pushed **down to per-block, per-port parasitic budgets**. Example: "the load-mirror block may add at most X fF at its Iref port and Y fF at its Iout port."
   - Each S4 variant is then judged **locally**, against its own budget.
   - Flat numerical methods give only per-net numbers for one assembled circuit.
2. **Recomposition for pre-screening.**
   - A variant's locally extracted parasitics can be inserted into the block's symbolic port model, and the spec recomputed **without a full-circuit post-layout simulation**.
   - This turns S4/S5 from "simulate every candidate" into "simulate only the finalists". It is measurable: prediction error, and simulations saved.
3. **Validity over ranges.** Closed forms can be evaluated over the variation ranges from your gm/ID–PSO stage cheaply. That gives worst-case budgets, not single-point ones.
4. **Attribution.** Each budget carries *which pole or zero* the node controls. This grounds both the LLM (B5) and the S8 diagnosis.

**Decision D1.** The primary claim is **hierarchical budget decomposition plus symbolic recomposition for variant pre-screening**, not "symbolic sensitivity" by itself.

### B2. The margin-allocation problem must be joint

Your PSO stage produces feasible ranges per node property. These are typically **one-factor-at-a-time**: each range assumes every other node stays nominal. If layout uses all of each node's range simultaneously, the spec fails.

**Decision D2.** Your variation ranges are treated as **feasibility limits** (inputs), not as budgets. S2 solves a small linear program:

- **Objective:** maximise the minimum weighted flexibility, maxₓ min_k (ΔC_k / w_k).
- **Subject to:**
  - Σ_k |S_ik| ΔC_k ≤ η_i · m_i for every spec i;
  - 0 ≤ ΔC_k ≤ range_k.
- **Weights** w_k come from geometric need: an estimate of the unavoidable C of a net, from its fan-out and the distance between blocks.

This is Charbon's 1993 formulation, but fed by hierarchical symbolic sensitivities and the upstream ranges. That makes it reproducible and explainable.

**Linearisation risk:** large parasitics break linearity. It is mitigated by the S7 closure check and one re-allocation iteration, the dynamic-bounds idea from Malavasi '95.

### B3. The symbolic models need to be "exact enough" where the budget lives

The level-2 template omits the mirror pole, and the matching is first-order in s. A budget for net3 (the mirror node) computed from level 2 would be **zero sensitivity**, which is wrong.

**Decision D3.** Budgets are computed from the **exact port admittance Y(s) of the lowest level that contains the node** (level 0/1). This Y(s) is built symbolically and evaluated numerically at the frequencies that define each spec:

| Spec | Evaluation frequency |
|---|---|
| Gain | DC |
| GBW | ≈ f_u |
| PM | f_u, together with the poles near it |

The reduced templates are used only where they have been verified to be exact.

**Requests to the O1 nodal analysis (for Monday and later):**

- **(a)** A net → symbol map for every physical net.
- **(b)** The Ioutn → Ioutp coupling term (the README already names the fix).
- **(c)** Common-mode models, required for CMFB and CMRR; essential for the FD OTA target.
- **(d)** Mismatch sources (ΔVth, Δβ) and noise sources as symbols.

Without (c) and (d), the CMFB, offset and noise budgets cannot be computed. For now S2 falls back to rule-based matching.

### B4. Electrical hierarchy is not physical hierarchy

**Example:** a bias mirror whose reference device sits in a bias block while its output devices feed several stages. If S4 builds sub-blocks strictly by electrical hierarchy, mirror matching across distant blocks is lost.

**Decision D4.** S2 derives a **physical clustering** from three inputs:
- the electrical hierarchy;
- matching criticality;
- proximity needs (high-sensitivity nets must be short).

Every hierarchy primitive maps to one cluster unless a matching or proximity rule forces devices to be split or merged. The rule is explicit and logged.

### B5. Where can an LLM add *measurable* value?

**Honest assessment.** Once sensitivities, budgets and a characterised PCell option table exist, most S1–S3 decisions are **deterministic optimisation**. An LLM making them would be slower and less reproducible than a solver.

The LLM is valuable where the information is *not formalised*:

1. **Intent completion.**
   - Classifying nets the models do not cover: clock or digital, ESD, test, reference.
   - Recognising unfamiliar topologies and mapping them to rule templates.
   - Reading designer notes.
2. **Conflict resolution and trade-off narration.** When the LP is infeasible or the rules conflict, propose which constraint to relax, with an equation-based justification.
3. **Generalisation to unseen circuits** without hand-writing rules for each topology.
4. **Tuning loops in S5 and S8** (the ICPI pattern), choosing *which* knob to change next.

**Decision D5.** The LLM is a **grounded copilot layer** with a strict JSON action space. Its contribution is reported as an **ablation**: rule-only vs. LLM-assisted, on **held-out** circuits.

The paper must stand without the LLM. If the LLM adds little, that is still a reportable finding, but it must not be the headline.

### B6. The evaluation circuits must be layout-sensitive, or nothing can be shown

**Rough estimate for our OTA.** Assumptions: Cox ≈ 8.3 fF/µm² for 4.15 nm oxide (an estimate; it should be read from the model card).

| Node | Existing C | Layout addition | Effect |
|---|---|---|---|
| OUTP | 1 pF load (CL) | a few fF | < 1 % on GBW |
| net3 (mirror node) | ≈ 100 fF from the M3/M4 gates | 5–20 fF | Moves a pole that lies well above GBW, so ≈ 1° of PM |

The method will "pass" trivially on this circuit and prove nothing.

**Decision D6.** The benchmark set must include circuits where layout consumes a large share of the margin:

- **(a)** The same 5T OTA re-run with a **small load** (e.g. CL = 50–100 fF) and specs tightened to the achieved values minus 10 %. Mark this clearly as a *stress variant*.
- **(b)** A **two-stage Miller OTA** with PM close to 60° and an internal high-impedance node. Source: LOADBench sized points.
- **(c)** A **fully differential OTA with CMFB**, your main target. It needs the common-mode models from B3(c).
- **(d)** One **clocked circuit**, a comparator, to exercise the analog/digital separation and shielding rules.

**Metric that proves sensitivity:** the fraction of the margin consumed by the baseline layout. Report it for every circuit.

### B7. PCell decisions must be quantitative, not rules of thumb

Choosing "double gate contacts" or "100 % via coverage" from heuristics is not research.

**Decision D7.** S3 builds an automatically **characterised option table**. For each device type, W/L/nf and PCell option set, Magic generates the cell and extracts it. Extraction uses `extract do resistance` for gate and source/drain access resistance, and `ext2spice cthresh 0` for junction and overlap capacitances. Measured per option:

| Quantity | Meaning |
|---|---|
| R_gate | Gate access resistance |
| R_s, R_d | Source/drain access resistance |
| C_db, C_sb | Junction capacitances (from AD/AS/PD/PS) |
| C_gd overlap | Gate–drain overlap capacitance |
| Area | Cell area |
| Pin positions | For S4/S5 routing |

These become **extra elements in the symbolic model**:
- gate resistance adds thermal noise and a pole;
- source resistance degenerates gm: gm_eff = gm / (1 + gm·R_s).

The option is then chosen by **budget slack per unit area**. The LLM explains and handles exceptions.

**Guard rings** are the exception: their benefit (substrate isolation) cannot be verified with Magic extraction or ngspice. They are decided by **rules**:
- SKY130 latch-up tap-distance rules;
- isolation of high-impedance or noise-critical devices that sit near aggressor (digital or clock) nets.

We state openly that this part is rule-based.

### B8. PnR: what to build, and what not to build

- **Not our contribution:** a new general analog placer or router. The literature is mature: SA or GA over sequence pair, MILP for small problems, SAGERoute-style routing.
- **What we need:** PCell-exact, DRC-clean SKY130 output with variant selection and our rules.

**Decision D8.**

**S4 — template-based procedural generators per primitive class.** Classes: differential pair, current mirror (ratioed), single device, cascode stack, capacitor.

- **Built from** unit PCells (Magic `gencell`, `guard 0`), plus dummies and a block-level substrate ring.
- **Internal routing** is drawn by the template, on a fixed track grid, so it is DRC-correct by construction.
- **Enumeration** covers arrangement (side-by-side / ABAB / ABBA / 2-D common-centroid), unit fold, orientation and pin side.

This is how BAG, ALIGN primitives and gLayout succeed: generator code, not search.

**S5 placement:** simulated annealing over sequence pair, with **symmetric-feasible moves** and a **variant gene** per block.
- Cost = area + λ · budget-violation estimate (from symbolic recomposition) + wirelength on critical nets.
- Followed by LP compaction.
- MILP is an option for top levels with ≤ ~40 blocks.
- We avoid re-implementing the patented HB\*-tree symmetry islands (US7873928, until 2027).

**S5 routing:** a **gridded maze router** on met2–met4. It handles:
- per-net width and via-count from current;
- mirrored routing for symmetric nets;
- shield tracks;
- forbidden crossings;
- max-length checks.

The top level has few nets, so this is tractable.

**RALF** (JKU, Apache-2.0, DATE'24; Magic-PCell-based placement, routing and Tcl output) is evaluated in week 1:
- **as the PCell-exact baseline A0**;
- **as a possible router donor.**

If its router handles our rules, reuse it instead of writing our own.

**LLM in S5:** sets cost weights and the variant shortlist, and chooses the next action in the tuning loop (ICPI pattern). **It never produces coordinates.**

### B9. Infrastructure decision

**Decision D9.** Two execution modes:

1. **Development mode in my cloud workspace.** Pinned installs of magic 8.3.685, netgen 1.5.324, ngspice-47 and `sky130A` (open_pdks 1689ac3f), plus a **private GitHub remote** for persistence. This needs your approval.
2. **Acceptance mode in your `layout-s0s3` container.**

Heavy jobs run **one at a time**, and Docker Desktop's memory limit is raised.

---

## Part C — Final novelty statement (for your defence)

**Title-level claim:**
*Hierarchical, analytically grounded layout-intent compilation for PCell-exact analog layout.*

| # | Contribution | Testable hypothesis | Measure |
|---|---|---|---|
| **N1** | **Hierarchical budget decomposition.** The top-level post-layout spec margin is decomposed into block-local, port-level parasitic budgets, by joint LP allocation over hierarchical symbolic sensitivities evaluated across the sizing-stage variation ranges. | **H1:** budgets from N1 bound the post-layout degradation, so that a layout meeting all budgets meets the specs. | Budget-compliance vs spec-pass agreement; worst-case error of the linear prediction |
| **N2** | **Symbolic recomposition for variant pre-screening.** Block-local extraction plus hierarchical port models predict full-circuit post-layout specs without full simulation. | **H2:** the prediction error on gain, GBW and PM is small enough to rank variants correctly. | Kendall τ against full PEX + SPICE ranking; simulations saved |
| **N3** | **Requirement-driven PDK-PCell parameterisation.** Device options are chosen from an automatically characterised option → parasitic table against the budgets. | **H3:** N3 reaches the same specs with less area, or fewer iterations, than default PCell options and than rule-of-thumb options. | Area; post-PEX spec retention |
| **N4** | **Budget-aware variant selection and PnR.** The S5 placer optimises area subject to recomposed budgets. | **H4:** fewer full PEX/SPICE loops to closure than (A1) topology-only constraints and (A3) injection-based budgets. | Loops to closure; final area |
| **N5** *(secondary)* | **Grounded LLM copilot**, ablated. | **H5:** on held-out topologies the LLM layer reduces manual rule authoring and/or improves N4 outcomes vs rule-only. | Decisions accepted by the validator; spec retention; human edits needed |

**Baselines (same circuits, same PEX flow):**

| ID | Baseline |
|---|---|
| A0 | RALF default (PCell-exact) |
| A1 | Topology-only constraints (symmetry and matching only) |
| A2 | LLM-labelled sensitive nets (PANDA/ICPI style) |
| A3 | Injection-based per-net budgets (2610.28677 style) |
| A4 | **Ours, rule and solver only** |
| A5 | **Ours + LLM** |

**Positioning against the most dangerous citation (2610.28677):**
- Their budgets come *after* sign-off, by injection into the full netlist.
- Ours are derived *before* layout, are **hierarchical** (per block and port), and are **reused** to pre-screen variants.
- Their symbolic analysis is used only for diagnosis; ours drives the constraints.

---

## Part D — The final flow, stage by stage

**Notation:** each stage lists its goal, inputs, method, deterministic/LLM split, outputs, gate, risks and effort.

### S0 — Ingest, freeze, bind to PCells

- **Goal:** one immutable, validated design package, with every device bound to its Magic PCell.
- **Inputs:** the design package.

  | File | Status |
  |---|---|
  | `netlist_sized.spice` | — |
  | `hierarchy.json` | — |
  | `nodal_analysis.json` | Per level: element maps, port Y(s), and the **net→symbol map** |
  | `specs.yaml` | — |
  | `achieved_specs.json` | — |
  | `operating_point.json` | Generated if missing |
  | `variation_ranges.json` | — |
  | `testbenches/` | — |

- **Method:**
  - Parse the netlist into a NetworkX graph.
  - Check consistency across files: every symbol maps to a net or device; hierarchy membership covers each device exactly once; achieved specs match a re-run of the testbenches within tolerance.
  - Bind each device to `sky130::<model>` with W/L/nf/m.
- **Split:** fully deterministic.
- **Outputs:** `circuit_ir.json`, `device_map.json`, `pdk_config.yaml`, `ref/*.spice` (µm units, ports explicit).
- **Gate:** the netlist round-trips through Netgen to "match uniquely" with no property errors; testbench re-run matches `achieved_specs`; negative tests are rejected.
- **Risks:** missing or inconsistent upstream files. Mitigation: a schema plus an explicit "missing" report; never guess.
- **Effort:** 0.5 day.

### S1 — Electrical intent (spec ↔ node map)

- **Goal:** know, quantitatively, which node affects which spec, why, and over what range.
- **Method:**
  1. **Operating point:** ngspice `.op` on the sized design, mapped onto the small-signal elements (C1..C5, G1, G2, R1 per device).
  2. **Sensitivity matrix:** S[spec][node] from the exact Y(s) of the lowest level containing the node (D3), evaluated at the spec frequencies, at nominal and at the corners of the variation ranges, giving min/max sensitivity.
  3. **Node classes:** dominant-pole, non-dominant/mirror-pole, high-Z, signal-path, bias, supply, digital/clock. Each class has a rule-defined detection, e.g. from impedance level and pole attribution.
  4. **Matching criticality:** from offset/CMRR sensitivity once mismatch symbols exist. Until then, from the hierarchy primitive class.
  5. **Branch currents** from the OP, for EM.
  6. **Coupling-sensitive net pairs:** pairs where ∂spec/∂C_coupling is large, e.g. the output-to-input Miller path.
- **Split:** deterministic. The LLM audits classifications and flags missing intent (e.g. "no CM model, so CMRR is not covered").
- **Outputs:** `sensitivity.json`, `node_classes.json`, `matching.json`, `currents.json`, `intent.json`.
- **Gate:**
  - Symbolic vs transistor-level ngspice perturbation (+δC at the node, two step sizes): sign agrees, and magnitude is within an agreed tolerance on the top-ranked nodes.
  - Predicted gain/GBW are close to `achieved_specs`.
- **Risks:** model gaps (B3). Mitigation: transistor-level finite differences as fallback, marked as such.
- **Effort:** 1–1.5 days.

### S2 — Requirement compiler (budgets and rules)

- **Goal:** turn intent into machine-checkable requirements.
- **Method:**
  1. **Joint budget LP** (D2), producing per-node ΔC (and ΔR where meaningful) budgets. Then **hierarchical decomposition** (N1): each block-port budget is derived through the level maps.
  2. **Routing rules:**
     - symmetric pairs (SymmetricNets);
     - **max length/C per net**, from the budget and the per-µm C of each layer, extracted from the PDK;
     - **min width and via count from current**, using SKY130 EM limits (*data still to be sourced from the SkyWater documentation; not invented*);
     - shielding for coupling-sensitive pairs near aggressors;
     - **no-cross rules** between digital/clock and high-Z analog nets;
     - layer preferences.
  3. **Placement rules:** symmetry axes, matched groups and pattern requirements (CC needed? ID enough?), proximity clusters (D4), orientation, guard-region needs.
- **Split:** solver and rules are deterministic. The LLM proposes relaxations when infeasible and explains each rule from its equation.
- **Outputs:**
  - `constraints.json`: the engine-neutral typed IR. Each entry carries id, class (hard/soft/budget), targets, value and units, `derived_from`, and status.
  - `budgets.json`, with per-block and per-port budgets.
- **Gate:** all names resolve; units present; LP feasible (or a documented relaxation); budgets reproducible; negative tests.
- **Risks:**
  - EM data unavailable: fall back to a conservative documented rule, flagged as ASSUMPTION.
  - Per-µm C unavailable: report length hints as `not_evaluated`.
- **Effort:** 1 day.

### S3 — Device design (PCell parameters)

- **Goal:** for each device, the PCell option set that meets its budgets at minimum area, with DRC/LVS sign-off.
- **Method:**
  1. **Characterised option table (D7)**, built once per device type and size class and cached. Options swept:
     - nf ∈ divisors preserving W_total;
     - `topc`/`botc` (gate contact top, bottom or both);
     - `diffcov`, `polycov`, `viasrc`, `viadrn`, `viagate`;
     - `guard` and `full_metal`.

     For each option, Magic extracts R_g, R_s, R_d, C_db, C_sb, the overlaps, area and pin positions.
  2. **Choose** the option that maximises budget slack per area, using the symbolic model extended with these elements.
  3. **Guard-ring rules (B7):** latch-up tap distance; isolation of sensitive devices.
  4. **Dummies:** placeholders, carried into the S4 templates.
- **Split:** deterministic choice. The LLM explains and handles exceptions, for example when a cheaper option is within ε of the best.
- **Outputs:** `device_decisions.json` (option, justification, predicted parasitics) and one PCell GDS per device.
- **Gate:** **every device has 0 DRC errors** (with negative control) and an **LVS match including W, L and nf**. Its extracted parasitics match the table entry.
- **Risks:**
  - Magic resistance extraction on small cells can be noisy. Mitigation: cross-check against analytical sheet- and contact-resistance estimates.
  - Option effects may be tiny for this OTA. **Report this honestly**; it is expected to matter more in larger and faster circuits.
- **Effort:** 1.5 days, including building the table.

### S4 — Sub-block variants

- **Goal:** a Pareto set of signed-off layout variants for each physical cluster.
- **Method:**
  - Template generators per primitive class (D8), built from S3 unit PCells.
  - Enumerate arrangement × fold × orientation × pin side.
  - Each variant gets local PEX, then **symbolic recomposition** (N2), which gives predicted spec contributions and budget slack.
- **Split:** deterministic enumeration. The LLM can prune the enumeration for large blocks.
- **Outputs:** `variants.json`. Per variant: GDS, bounding box, pins, symmetry error, extracted port parasitics, budget slack, predicted specs, DRC/LVS status.
- **Gate:** every listed variant is DRC 0 and LVS match. The recomposition error is validated on a sample by full simulation.
- **Risks:** template generators cost real development effort. Mitigation: start with the two classes the OTA needs (diff pair, mirror), then add classes per benchmark.
- **Effort:** 3–4 days for the first two classes.

### S5 — Variant selection, placement, routing

- **Goal:** the smallest top-level layout that meets all budgets and rules.
- **Method:**
  - SA over sequence pair with a variant gene and symmetric-feasible moves.
  - Cost = area + λ·(recomposed budget violation) + critical-net wirelength.
  - LP compaction.
  - Gridded router with the S2 rules (width, vias, mirrored routing, shields, no-cross, max length).
  - RALF is either the baseline or the router donor (B8).
- **Split:** deterministic engine. The LLM tunes weights and the shortlist, and picks the next action in the loop.
- **Outputs:** `placement.json`, `top.gds`, `routing_report.json` (with per-rule compliance).
- **Gate:** top-level DRC/LVS clean; every routing rule checked by script.
- **Risks:** the router is the highest engineering risk. Mitigation: gridded tracks, few top-level nets, RALF reuse.
- **Effort:** 4–6 days.

### S6–S9 — Verify, evaluate, repair, select

- **S6 Verify:**
  - Magic DRC plus the KLayout deck.
  - Netgen LVS, parsed.
  - PEX with coupling kept: `cthresh 0`, never the LVS preset, plus the sconnect well check.
- **S7 Evaluate:**
  - The same testbenches.
  - **Budget compliance per node:** extracted C vs budget.
  - H1/H2 data collection.
- **S8 Repair:**
  - Attribute failures with the symbolic sensitivities, then confirm with counterfactual SPICE.
  - Apply a local action: S3 option change, S4 variant swap, or an S5 reroute/move.
  - The ICPI-style loop is where the LLM is most useful.
- **S9 Select:** the smallest layout that passes everything.

---

## Part E — Risks and opportunities

### E1. Risk register

| # | Risk | P | I | Mitigation |
|---|---|---|---|---|
| R1 | Benchmarks not layout-sensitive, so no measurable benefit | High | High | D6 stress variants + two-stage + FD OTA. Report margin consumed. |
| R2 | Symbolic model gaps (mirror pole, CM, mismatch, noise) | High | High | D3 (exact Y(s) at low level); requests to O1; numerical fallback marked as such |
| R3 | Linear budgets optimistic for large parasitics | Med | Med | S7 closure check + one re-allocation (dynamic bounds) |
| R4 | Template generators and router effort exceed the schedule | High | High | Two primitive classes first; RALF reuse; small top levels |
| R5 | PCell option effects too small to show N3 on simple OTAs | Med | Med | Evaluate on faster/larger circuits; state it honestly |
| R6 | LLM adds no measurable value | Med | Low (by design) | Ablation framing (D5); report it either way |
| R7 | Missing PDK data (EM limits, per-µm C) | Med | Med | Source from SkyWater docs or PDK files; never invent; flag `not_evaluated` |
| R8 | Competing publication appears (2610.28677 follow-up) | Med | High | Publish N1+N2 early (workshop paper) |
| R9 | Infrastructure (Docker lock-ups, bridge time limit, PC availability) | High | Med | D9 cloud mode + sequential jobs + private remote |
| R10 | Netgen merging/property quirks give false LVS results | Med | Med | Explicit `device_map` and property checks; negative controls |
| R11 | IP: HB\*-tree symmetry-island patent | Low | Med | Use sequence-pair symmetric moves |

### E2. Opportunities

1. **Closing the loop to sizing (O3 → O2).**
   - The characterised PCell option table and the block budgets are exactly the parasitic models your PSO needs for **layout-aware sizing**: feasible ranges that already account for unavoidable layout C.
   - This is the "joint electrical–physical optimisation" in your project context. It is a natural second paper.
2. **Dataset contribution.** Every S4 variant comes with DRC/LVS status, local PEX and recomposition error. That is a SKY130 dataset in the spirit of OSIRIS (87,100 variants), but with **electrical budgets attached**, which OSIRIS lacks.
3. **Explainable layout review.** Every constraint is traceable to an equation. This is useful for teaching and for design reviews (it is what reviewers ask PANDA and ICPI for).
4. **Publication path:**
   - N1 + N2 on the OTA set: workshop or conference paper (ICLAD / MLCAD / SMACD / ISCAS).
   - Full flow + ablations: journal (TCAD / TCAS-I).

---

## Part F — Roadmap

| When | Deliverable | Gate |
|---|---|---|
| **Sun 25 Oct** (deadline) | S0 on the design-package contract (5T OTA + stress variant); S1 with real OP, sensitivities and ngspice validation; S2 joint-LP budgets + rule IR; S3 option table for the OTA's device sizes + decisions + per-device DRC/LVS | S0–S3 gates; handoff file |
| Mon 26 – Fri 30 Oct | Integrate your nodal-analysis outputs into S1; RALF evaluation (A0); S4 templates for diff pair and mirror; first **H1/H2 experiment** (recomposition vs full PEX) on the OTA | H2 ranking accuracy on ≥ 10 variants |
| 2–8 Nov | S5 placer + router (or RALF router); full flow on the 5T OTA (nominal + stress); two-stage Miller benchmark | Top-level DRC/LVS; S7 report |
| 9–15 Nov | S6–S8 loop; ablations A0–A5 on 2–3 circuits; LLM copilot layer | Ablation table |
| 16–22 Nov | FD OTA with CMFB (needs O1 CM models); write-up of N1+N2 | Draft paper |

---

## Part G — What you must do or decide

1. **Approve D1–D9**, or tell me which to change.
2. **Infrastructure (D9):**
   - Approve installing the pinned EDA tools in my cloud workspace.
   - Approve a **private GitHub remote** for the repo.
3. **Upstream requests (B3):**
   - net→symbol map;
   - the Ioutn→Ioutp coupling term;
   - common-mode models;
   - mismatch and noise symbols;
   - the format of `variation_ranges.json` (per node property: range and per-spec effect).
4. **Benchmarks (D6):**
   - Approve the 5T OTA stress variant (small CL, tightened specs), clearly labelled.
   - Approve LOADBench (~40 GB download) or pick 1–2 sized two-stage designs from your own PSO.
5. **Docker:** raise the memory limit in Docker Desktop and keep it running during acceptance runs. I will run jobs one at a time.

---

## References

All references were opened during the 2026-10-24 survey. Full list in `05`, §11.

**Newly checked for this document:**
- RALF (DATE 2024) — https://fodok.jku.at/fodok/vortrag.xsql?V_ID=40471 ; https://github.com/JakobRat/RALF
- Performance-driven analog layout survey (ASP-DAC 2024) — http://www.cse.cuhk.edu.hk/~byu/papers/C194-ASPDAC2024-AnalogPD.pdf
- Joint hierarchical placement (ICCAD 2024) — https://yibolin.com/publications/papers/ANALOG_ICCAD2024_Gao.pdf
- Layout-aware sizing with floorplans (DATE 2015) — https://past.date-conference.com/proceedings-archive/2015/pdf/0411.pdf
- LOADBench — https://arxiv.org/html/2610.21591
- OSIRIS — https://arxiv.org/pdf/2601.19439
- SKY130 BAG3 `tech_params.yaml` — checked: **contains no EM current limits** (only temperature scale factors), so EM data must come from elsewhere.
