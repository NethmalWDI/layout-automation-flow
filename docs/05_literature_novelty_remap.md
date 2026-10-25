# Literature review, novelty, and remapped flow (S0–S9)

**Date:** 2026-10-24

**How this was produced.** Five parallel literature tracks searched arXiv, IEEE/ACM proceedings pages, university reports, GitHub and Hugging Face/Zenodo. I spot-checked the critical items myself: 2610.28677, LOADBench (2610.21591) and OSIRIS (2601.19439).

- **Citation rule:** every cited item was opened unless it is marked *UNVERIFIED*.
- **LinkedIn:** no LinkedIn post could be opened and verified, so none is cited.
- **Builds on:** `01_inventory`, `02_analysis`, `03_plan`, `04_device_generation`.

---

## 0. Answers in one page

| Your question | Answer |
|---|---|
| **What is the novelty?** | Turning **hierarchical, symbolic, per-node small-signal models**, plus the spec margins and the variation ranges from your gm/ID–PSO front end, into a **typed set of layout requirements before any layout exists**. These are per-node parasitic budgets, routing rules (symmetry, max length/C, shielding, EM width, A/D separation) and **SKY130 PDK-PCell parameter decisions** (fingers, gate-contact side, contact/via coverage, guard rings). Each decision is traceable to an equation. These then drive hierarchical variant generation (S4) and variant selection with PnR (S5). **No work we found does this.** Every prior constraint generator uses *numerical* sensitivities (simulation, parasitic injection or ML surrogates), *topology-only* rules, or *LLM intuition*. See §2. |
| **Closest competitors a reviewer will cite** | **Noori Zadeh et al., arXiv 2610.28677 (19 Oct 2026).** An open-PDK multi-agent flow with a *parasitic-budget agent*. Its budgets come from parasitic **injection plus re-simulation**; its symbolic analysis was used only for diagnosis after sign-off. Others: **PANDA** (LLM writes constraints; post-layout UGB fails), **ICPI** (LLM tunes MAGICAL knobs), **LLANA**, **LayoutCopilot**, and the classic **Charbon/Malavasi/Choudhury 1993–97** and **Miliozzi DAC'96** sensitivity→bound work. |
| **Should PnR be done by an LLM?** | **No, not the coordinates.** Every positive result keeps a deterministic placer and router underneath and uses the LLM as **planner and parameter tuner**: PANDA, ICPI, LayoutCopilot, AnalogMaster. LLMs writing coordinates directly produce overlaps and broken symmetry (ACDC, 2512.09199). **Recommendation:** S4 enumerates variants deterministically. S5 uses a classical placer with a variant-selection variable (SA or GA over sequence pair, or MILP for small top levels) and a constraint-aware router. The LLM plans, prunes and tunes, ICPI-style. |
| **PCell-based flow: yes or no?** | **Yes. Use the open_pdks Magic generator (`magic::gencell sky130::…`) as the single canonical device generator.** It is exact for LVS and PEX (verified: extracted AD/PD equal the xschem netlist). Its main limit: one PCell holds one device, so matched structures (ABBA, common-centroid) must be **assembled in S4 from unit PCells**. Pros and cons are in §6. |
| **"Analog size bench" dataset** | This is **AMS-SizingBench** (AutoSizer, ICML'26): 24 SKY130 circuits, but **unsized** (W = null) and with spec/testbench caveats. The better source of *sized* SKY130 op-amps is **LOADBench** (MLCAD'26, CC BY 4.0). It has 100+ op-amp topologies, ~10³ Pareto sizings each, and structural/functional XML annotations (mirrors, diff pairs, stages, matching), which are close to the hierarchy you would otherwise prepare by hand. Ladder in §8. |
| **Can I work in the cloud with your PC off?** | **Partly, yes** (§10). Research, code, unit tests, SymPy and the docs all run in my cloud workspace. EDA runs (Magic, Netgen, ngspice, `sky130A`) need either your PC's Docker or an install of those tools in my cloud workspace. The install is a few GB, without the 17 GB image, and needs your approval. |

---

## 1. Literature map (condensed)

### 1.1 LLM / agentic analog layout, 2024–2026

| Work | What the LLM decides | Engine underneath | Uses node sensitivities? | PCell options by LLM? | PDK / evaluation |
|---|---|---|---|---|---|
| **Multi-agent nanowatt LPF**, Noori Zadeh, Prasad, Elamien, arXiv 2610.28677 | Writes a GDSFactory generator; picks routing layers; a parasitic-budget agent converts margin to per-net budgets | Nevergrad (25 params, min area); mirror-symmetry check | **Numeric injection** (symbolic used only in post-sign-off review) | Dummy rows (human reverted) | IHP SG13G2; KLayout DRC/LVS, kpex, MC |
| **PANDA**, Zhang et al., arXiv 2606.15052 | Placement/routing constraint plans; picks best attempt after PEX | Constraint placer + SAGERoute; MOSTAR BO sizing | No ("sensitive nets" are labels) | No | Proprietary; UGB 10.84 → 4.19 MHz (fails 8 MHz) |
| **ICPI**, Liu, Wei, Gao, Pan, arXiv 2608.13767 | Analyzer gives importance scores; Supervisor/Executor tune 5 knob families | MAGICAL-derived kernel | No (LLM judgement) | No | 65/40 nm; FoM 1.104 vs BO 0.979 |
| **LayoutCopilot**, arXiv 2406.18873 | NL → layout commands (symAdd, netPriority, wireWidth) | MAGICAL + editor | No | No | TSMC 40/28; CMRR 27.3 → 58.7 dB |
| **LLANA**, arXiv 2406.05250 | LLM as BO surrogate over 14 net weights | MAGICAL | No (rejects analytical) | No | — |
| **Vibe Tapeout**, Yoshioka, arXiv 2610.15240 | Agents write Python/Tcl generators and routers | Magic/netgen | No | Implicit (wrote generators) | **SKY130**; false passes found; −8 to −13 dB SNDR after PEX |
| **Glayout NL→layout** (MLCAD'24, *UNVERIFIED venue*) | Fine-tuned LLM writes gLayout code | gLayout | No | Can call guard-ring/via cells, no rationale | SKY130/GF180; 70% task completion |
| **LAYGO2 + GPT-4**, arXiv 2408.07279 (+ SKY130 reproduction) | Writes placement/routing code | laygo2 grids | No | No | DRC/LVS clean, with tool feedback |
| **AnalogMaster**, arXiv 2604.20916 | Image → netlist, sizing | SA placer, A* router with an "electrical sensitivity" cost | Not explained | No | — |
| **ACDC**, arXiv 2512.09199 | **Direct coordinates** | none | No | No | Overlaps, broken symmetry |
| aispice PR #38 (GitHub, MIT) | Edits generator params after DRC/LVS failure | Rust generators (CC/ID, dummies, guard ring) | No | Only as repair | IHP; 5T OTA GBW 113.7 → 105.2 MHz |

### 1.2 Sensitivity / parasitic / EM-driven constraint generation (what is **already** done)

| Idea | Prior art | Sensitivity source |
|---|---|---|
| Specs → per-parasitic bounds via linearised ΔP = Σ S·Δp | Choudhury & Sangiovanni-Vincentelli, TCAD 1993 (*venue UNVERIFIED*); Charbon et al., ICCAD 1993 | **Numerical** |
| Bounds on parasitic *mismatch*; topological constraints from sensitivity | Charbon ICCAD'93 | Numerical |
| Bounds become router cost weights; reroute violators | Charbon et al., ERL M94/40 (CICC'95) | Numerical (augmented-schematic simulation) |
| Dynamic re-allocation of bounds during routing | Malavasi CICC'95 | Numerical |
| Statistical treatment of parasitics | Charbon et al., IEICE 1997 | Numerical / statistical |
| Per-node noise bounds that drive **shield insertion** | Kirkpatrick & Sangiovanni-Vincentelli, ICCAD'94 | Simulation |
| Whether a **guard ring** is needed, A/D separation, width/length limits | Miliozzi et al., DAC'96 | Finite differences |
| Performance-driven placement with sensitivities | Lampaert, Gielen, Sansen, DAC'95 | Precomputed numeric |
| **EM width** from current; IR-drop → max length | Martins et al., DATE'14; **SAGERoute** DATE'23 (LP sizing); MagicalRoute ICCAD'20 | Schematic simulation currents |
| Symmetry / matching extraction | ALIGN/GANA, Kunal ICCAD'20, AncstrGNN DAC'21 | **Topology only** (they explicitly avoid sensitivities as too costly) |
| Device pattern selection (CC/ID/clustered, fins × fingers) | Madhusudan DATE'21, Sharma DATE'21, Maji 2407.00817 | SPICE deviation or geometric proxies |
| Post-layout-predicted guidance | AnalogFold/PARoute DAC'24 (3D GNN), GeniusRoute | Learned surrogate |
| Symbolic sensitivities | Yang & Vemuri, DATE'06 | **Symbolic, but sizing only** |

### 1.3 Symbolic and hierarchical front ends

- **Symbolic tools:** SymMNA, SLiCAP, SymXplorer, SapWin, and approximate pole/zero methods (Gheorghe 2025; Fathi 2026).
- **LLMs reasoning over symbolic models:** White-Op (2601.21321), AmpAgent (2409.14739), Bujana & Karsilayan (2604.07387). **All stop at sizing.** None hands node-level knowledge to layout.

### 1.4 PnR methods with variants

- **Variant selection as an ILP binary:** Grus et al., ICORES'23. Exact ILP stalls at about 100 rectangles; a GA/CMA-ES heuristic scales to about 200 devices.
- **HB\*-tree symmetry islands:** **Synopsys patent US7873928**, estimated expiry 2027. This is an IP caution.
- **RL placement:** about ties SA zero-shot and needs hours of training (Basso et al.; 2405.16951).
- **Router choices:** SAGERoute and RALF's gridless Magic router.
- **RALF (JKU, Apache-2.0, DATE'24):**
  - **Instantiates the Magic sky130 gencells.**
  - Places with RL or SA and routes with a gridless router that **outputs Magic Tcl**.
  - The authors' own assessment (Pretl, ESSERC'24) lists missing symmetry, dummies and power routing.

---

## 2. Novelty

### 2.1 What we must NOT claim

These are already published:
- spec → parasitic-bound mapping
- mismatch bounds
- shield insertion from noise bounds
- guard-ring need from substrate bounds
- EM-width routing
- graph-based symmetry extraction
- CC/ID pattern selection
- per-net budgets in an open-PDK agent flow (2610.28677)
- LLM-generated constraints (PANDA, LayoutCopilot)

### 2.2 Defensible contributions (proposed wording)

**C1 — Symbolic-hierarchical intent compilation.**
A method that propagates **closed-form, frequency-resolved, hierarchical** small-signal models into layout requirements:

- **Inputs:** ∂spec/∂C_node, ∂spec/∂R_branch, ∂spec/∂(mismatch), computed per hierarchy level.
- **Range, not a point:** the models are evaluated over the **variation ranges** produced by the gm/ID–PSO sizing front end, not at a single operating point.
- **Outputs, before layout:**
  - per-node parasitic budgets
  - routing rules
  - placement and matching rules
- **Explanation:** each output carries **pole/zero attribution**, i.e. *why* the node matters.

*Differentiators:*
- **Vs. Charbon/Choudhury/Miliozzi:** symbolic and hierarchical instead of flat finite differences; no per-point re-simulation; valid over ranges.
- **Vs. 2610.28677:** budgets are derived *before* layout from equations, not by injection after sign-off.
- **Vs. ALIGN/GANA:** quantitative, not topology-only.

**C2 — Requirement-driven PDK-PCell parameterisation.**
A rule base, auditable by an LLM, that maps node requirements to **exact SKY130 PDK PCell parameters**:

- nf/m split at constant W_total
- gate-contact side (`topc`/`botc`)
- contact and via coverage (`diffcov`, `polycov`, `viasrc`, `viadrn`, `viagate`)
- guard-ring presence and type, plus block-level substrate rings
- dummies

*No prior work* derives these from per-node budgets. The closest do something else:
- Madhusudan: SPICE deviation
- OSIRIS / gLayout: RL after extraction
- Miliozzi: ring yes/no only

**C3 — Budget-aware hierarchical variant generation and selection.**
- **S4:** produces a Pareto set of DRC/LVS-clean variants for each sub-block, assembled from PCells, scored against **its own node budgets** (local PEX).
- **S5:** chooses variants and places and routes them to **minimise area subject to the budgets**.
- *Prior art:* variant-selecting placers exist (Grus), but none tie the choice to electrical budgets. LLM flows select only whole-flow snapshots (PANDA).

**C4 — Equation-grounded LLM decisions, with ablation.**
- The LLM proposes, explains and resolves conflicts *over explicit expressions and budgets*. It does not rely on pretrained intuition (ICPI, PANDA) or black-box BO (LLANA).
- Every decision is schema-validated and checked independently.
- We **measure** what the LLM adds versus a rule-only baseline.

**C5 — Fully open, reproducible SKY130 reference flow.**
- Every sub-block is DRC/LVS clean, verified with Magic, Netgen and ngspice.
- Benchmarks are public: own OTA, AMS-SizingBench, LOADBench.
- The only open-PDK precedent is 2610.28677, on IHP.

### 2.3 Required evidence (otherwise the claim is weak)

Run ablations on the same circuits and PEX flow:

| Variant | Constraints / decisions |
|---|---|
| A0 | Default engine |
| A1 | Topology-only constraints (ALIGN-style) |
| A2 | LLM-labelled sensitive nets (PANDA/ICPI-style) |
| A3 | Injection-based budgets (2610.28677-style) |
| **A4** | **Ours, symbolic (no LLM)** |
| **A5** | **Ours + LLM** |

**Metrics:**
- post-PEX spec retention
- area
- number of PEX/SPICE runs
- **budget-prediction accuracy** (predicted vs extracted degradation per node)
- Monte Carlo offset

**Known risk:** linearised budgets are optimistic for large parasitics (the reason for Malavasi's dynamic bounds). Close the loop with the PEX check in S7/S8.

---

## 3. Remapped flow S0–S9 (your vision, aligned to the novelty)

### 3.0 The input contract (the "design package" given to S0)

| File | Content | Source |
|---|---|---|
| `netlist_sized.spice` | Optimised, sized netlist | O2 (PSO) |
| `hierarchy.json` | Levels, primitives (diff pair, mirror …), stage membership | O1 (or prepared by hand for benchmarks) |
| `nodal_analysis.json` | Per level and per node: the symbolic element map (as `equations.json` today), TFs, poles/zeros, and **which symbols each physical node contributes to** | O1 (SymMNA) |
| `specs.yaml` | Targets (min/max), conditions (VDD, CL, temperature, corner) | Designer |
| `achieved_specs.json` | Schematic-simulated values: gain, GBW, PM, noise, power, … | Testbench run |
| `operating_point.json` | Per device: Id, gm, gds, Cxx, Vdsat, region | ngspice `.op` |
| `variation_ranges.json` | Per node property (C, R, gm, gds …): feasible or allowed range and its effect on each spec, from the gm/ID–PSO range stage | O2 |
| `testbenches/` | The AC/OP/noise decks that produced `achieved_specs` | Repo |

### 3.1 Stage definitions

| Stage | Responsibility (new emphasis in **bold**) | Main outputs | LLM role | Gate |
|---|---|---|---|---|
| **S0 Ingest & bind** | Parse and freeze the design package; check every node and symbol maps to a real net/device; bind devices to **Magic PDK PCells** | `circuit_ir.json`, `device_map.json`, `pdk_config.yaml`, `ref/*.spice` | none (deterministic) | Round-trip LVS; schema checks; negative tests |
| **S1 Electrical intent** | **Spec→node map**: sensitivity matrix S[spec][node] over the variation ranges; node classes (dominant-pole, mirror-pole, high-Z, signal, bias, supply, digital/clock); matching criticality (offset/CMRR sensitivity); **branch currents** (EM); coupling-sensitive net pairs | `intent.json`, `sensitivity.json`, `node_classes.json` | Explains and audits classifications; flags gaps (e.g. "CM model missing") | Symbolic vs SPICE perturbation agreement |
| **S2 Requirement compiler** | Typed requirements: **per-node C/R budgets** (margin split across nodes), **routing rules** (differential/symmetric pairs, max length/C, shielding, A/D crossing ban, **min width and vias from current**), **placement rules** (symmetry axis, proximity, CC/ID need, orientation, guard regions) | `constraints.json` (IR), `budgets.json` | Proposes rules and resolves conflicts; every proposal is validated | Names resolve; units; budget arithmetic; no hard conflicts |
| **S3 Device design (PCell parameters)** | Per device: **nf/m at constant W_total; `topc`/`botc` (gate R for high-gm/noise nodes); `diffcov`/`viasrc`/`viadrn` (contact R on high-current S/D); `polycov`/`viagate`; `guard`; dummies; `conn_gates`**. Each choice is justified from S1/S2 | `device_decisions.json`; PCell GDS per device | Picks options from a rule-bounded menu, with written justification | **Every device DRC 0 + LVS match** (including W, L, nf) |
| **S4 Sub-block variants** | For each hierarchical element (diff pair, mirror, tail, cascode stack …): enumerate arrangements from **unit PCells** (side-by-side, ABAB, ABBA, 2-D CC; mirror ratio interdigitation; dummies; block guard ring), plus local routing that obeys S2 rules; local PEX → **node C against budget** | `variants.json` (Pareto: area, aspect, pins, symmetry error, budget slack) + GDS | Prunes the variant space; ranks trade-offs | **Every variant DRC 0 + LVS match + budget report** |
| **S5 Global selection + PnR** | Choose one variant per block, then place (min area subject to symmetry, proximity, A/D separation), then route (EM width, symmetric routing, shields, max length) | `placement.json`, `top.gds`, `routing_report.json` | **Planner/tuner only:** weights, priorities, variant shortlist (ICPI-style loop) | Top-level DRC/LVS |
| **S6 Physical verification** | DRC (Magic `drc(full)` + KLayout deck), LVS (Netgen, parsed), PEX (Magic with **coupling caps kept**: `cthresh 0`, not the LVS preset) | reports, `extracted_rc.spice` | none (independent) | Negative controls |
| **S7 Post-layout evaluation** | Same testbenches; **per-node budget compliance** (extracted C vs budget); spec deltas | `metrics.json`, `budget_compliance.json` | Summarises | — |
| **S8 Diagnosis & repair** | Attribute failures with the symbolic sensitivities, confirm by counterfactual SPICE, then a **local** fix back in S3/S4/S5 | `repair_plan.json` | Hypothesis ranking; picks a repair from the allowed actions | Re-run S6/S7 |
| **S9 Selection** | Smallest layout meeting all verified specs | final GDS + history | — | — |

**Hierarchical sign-off rule (your requirement):** nothing moves up a level unless it is DRC- and LVS-clean.
- S3 devices → S4 variants → S5 top level.
- PEX budgets are checked at S4 (local) and S7 (global).

### 3.2 Example of the S2/S3 rule base (for the 5T OTA)

These rules are illustrative. The actual numbers come from S1.

| Requirement (from S1) | Rule | Effect in S2/S3 |
|---|---|---|
| OUTP is the dominant-pole node; ∂GBW/∂C_OUTP large | budget ΔC_OUTP ≤ x fF | max length/C on OUTP; prefer low-C metal; no dummy/guard coupling |
| net3 is the mirror-pole node; affects PM | budget ΔC_net3 | M3/M4 placed adjacent; short net3; `doverlap` shared diffusion |
| M1/M2 offset/CMRR sensitivity high | matching critical | S4 offers ABBA / 2-D CC variants; same orientation; dummies |
| INP/INN are a differential pair | symmetric routing | SymmetricNets; matched lengths and vias |
| Tail current Id = 85 µA | EM / IR | min width and number of vias on net1 and VSS from the SKY130 EM table |
| M1/M2 high gm; input-referred noise matters | gate resistance | nf ≥ k, and `topc=1 botc=1` (double-sided gate contact) |
| Bias node VBIAS (high-Z, noise-sensitive) | isolation | guard ring around M5 / block substrate ring; shield VBIAS if it runs near switching nets |

---

## 4. Who decides what (LLM vs deterministic)

| Decision | Deterministic engine | LLM | Why |
|---|---|---|---|
| Sensitivities, budgets | ✔ (SymPy + ngspice) | explain only | Must be exact and reproducible |
| Constraint proposals / conflicts | rule base + validator | ✔ proposes, explains | Literature: LLMs work at the constraint level |
| PCell options (S3) | menu + DRC/LVS | ✔ chooses with justification | Novel (C2); measured against a rule-only baseline |
| Variant enumeration (S4) | ✔ | prune / rank | Enumeration is cheap; legality must be exact |
| Placement / routing coordinates (S5) | ✔ SA/GA/MILP + router | **no** | ACDC shows LLM coordinates fail |
| PnR tuning loop | engine | ✔ ICPI-style | ICPI beat BO with about 11 post-layout sims |
| Verification | ✔ independent | none | Vibe Tapeout false passes |

**LLM access:** Claude Code / Codex CLI with JSON schemas (`claude -p --json-schema`) and a provider-neutral client.
- Every call is journaled: inputs hash, prompt version, output, validation result.

---

## 5. PnR recommendation

1. **Week 1 after S3: evaluate RALF** on our 5T OTA.
   - It already uses the Magic PDK PCells and emits Magic Tcl routing.
   - Apache-2.0, so we can reuse and extend it.
   - If it works: use it as the S5 baseline (A0) and add a variant gene plus our S2 rules.
2. **Own engine, if RALF is unusable.** Python sequence-pair with symmetric-feasible moves, SA or GA with a **variant-selection gene** (Grus-style), then LP compaction. Routing as Magic Tcl: A* with per-net width and mirrored routes for symmetric nets.
   - Avoid reimplementing the patented HB\*-tree symmetry islands until 2027.
3. **ALIGN** stays as an external comparison (A0'), noting it is not PCell-exact on SKY130 (fixed L).
4. **MAGICAL** stays as an algorithm reference: its mock PDK cannot produce SKY130 output.

---

## 6. PCell-based flow: pros and cons, and decision

| Pros | Cons / limits | Mitigation |
|---|---|---|
| Exact device geometry, so LVS and PEX match the PDK models. Verified: `ad=6.96 pd=48.58` identical to the xschem netlist. | **One device per Magic PCell:** no CC/ID or shared diffusion *between* devices | Assemble matched structures in S4 from unit PCells (nf=1/2, `guard 0`) plus a block-level ring |
| Device-level DRC correct by construction (including SKY130 quirks such as NPC) | Dummy option disabled | Dummies as separate instances |
| No re-encoding of design rules (ALIGN / gLayout / MAGICAL all do this) | More area than row-based styles (spacing between instances) | S4 searches abutment-friendly variants; S5 compaction |
| Small, meaningful S3 parameter space (exactly the knobs you listed) | Tcl generation is slow | Cache cells by parameter hash |
| Portable: GF180 and IHP ship equivalent generators | KLayout sky130 PCells differ geometrically (but support interdigitation) | **Use Magic as the single canonical generator.** KLayout only for checks |
| Fits the sign-off tools (Magic extract, Netgen) | netgen m vs nf merging needs care | Explicit device_map and LVS property checks |

**Decision:** PCell-exact flow with the Magic generator as canonical. gLayout, ALIGN and MAGICAL serve as comparisons.

---

## 7. What changes from `03_plan_S0-S3.md`

| Item | Change |
|---|---|
| S0 | Input becomes the **design package** (§3.0). Device binding is to Magic PCells. |
| S1 | Adds node classes, **branch currents** (EM) and variation ranges (`variation_ranges.json` slot) |
| S2 | Adds routing-rule classes: EM width/vias, A/D separation, shielding, max length/C |
| S3 | **Was** "gLayout variants". **Now** "PCell parameter decisions per device + DRC/LVS". Matched-structure variants move to S4. |
| S4/S5 | Redefined as variant generation, then selection plus PnR (§3.1) |

---

## 8. Benchmarks and test ladder

The manual work per circuit is `hierarchy.json`, `nodal_analysis.json` and `variation_ranges.json`.

| # | Circuit | Source | Sized? | Notes |
|---|---|---|---|---|
| 1 | 5T OTA (5 FET + bias) | your `example_ota_5t` | yes | Current DUT; hierarchy and equations exist |
| 2 | 5T / current-mirror OTA | ALIGN-pdk-sky130 examples + AMS-SizingBench YAML testbenches | ALIGN: yes | Cross-tool comparison |
| 3 | Two-stage Miller | **LOADBench** (sized Pareto points + XML annotations) | yes | Annotations reduce the manual hierarchy work |
| 4 | Folded cascode | AMS-SizingBench `folded_cascode_ota` | **no** (W null) | Size it with your PSO first |
| 5 | FD OTA with CMFB | wulffern `cnr_ota_sky130nm` (no licence file) / LOADBench | partly | Your main target class |
| 6 | LDO | AnalogGym `ldo_simple` / efabless `sky130_am_ip__ldo_01v8` | AnalogGym: initial sizes | Large pass device, EM rules |
| 7 | Comparator | efabless `sky130_icrg_ip__ulpcomp` | yes | Clocked: A/D separation rules |

**AMS-SizingBench caveats:** no licence file; some unit inconsistencies; the LDO testbench runs only `.op`; `fdgb` has no CMFB.

---

## 9. Revised near-term schedule

| When | Work |
|---|---|
| Sun 25 Oct | S0 on the design-package contract (5T OTA); S1 symbolic sensitivities + OP + ngspice validation; S2 requirement compiler (budgets, routing rules, EM widths); S3 PCell decisions + per-device DRC/LVS (generator already working) |
| Mon 26 Oct | Plug your nodal-analysis results into S1; re-run S1 → S3 |
| Week of 26 Oct | RALF evaluation; S4 variant generator (diff pair, mirror); S5 baseline |

---

## 10. Working with your PC off

| Works in my cloud workspace | Needs EDA tools |
|---|---|
| Literature, docs, all Python (parsers, SymPy sensitivities, constraint compiler, PCell decision logic), unit tests, LLM decision loop | Magic (PCell generation, DRC, extraction), Netgen (LVS), ngspice with `sky130A` models |

**Option A (default): your PC.** You keep your PC and Docker on during work sessions, and the code lives in your repo.

**Option B (needs your approval):** I install magic, netgen, ngspice and the `sky130A` PDK in my cloud workspace, pinned to the same versions as your container:
- magic 8.3.685, netgen 1.5.324, ngspice-47, open_pdks 1689ac3f
- Installed via conda-eda or source builds, plus ciel for the PDK
- About 3–5 GB; 2 CPUs and 7 GB RAM are available

Caveats for Option B:
- The cloud workspace is reclaimed after a period of inactivity, so the work must be saved somewhere durable: your repo when the PC is on, or a **private GitHub remote** if you allow one.
- **Acceptance runs still go through your container**, so results stay reproducible on your side.

---

## 11. Key references (opened)

**Closest competitors and LLM layout work**
- 2610.28677 — https://arxiv.org/html/2610.28677
- PANDA — https://arxiv.org/html/2606.15052v1
- ICPI — https://arxiv.org/pdf/2608.13767
- LayoutCopilot — https://arxiv.org/html/2406.18873v3
- LLANA — https://arxiv.org/html/2406.05250v3
- Vibe Tapeout — https://arxiv.org/html/2610.15240v1
- ACDC — https://arxiv.org/pdf/2512.09199
- AnalogMaster — https://arxiv.org/html/2604.20916
- LAYGO2 + LLM — https://export.arxiv.org/pdf/2408.07279
- aispice — https://github.com/danieltyukov/aispice/pull/38

**Classic sensitivity → constraint work**
- Charbon ICCAD'93 — https://ptolemy.berkeley.edu/projects/embedded/research/analog-cad/publications/abstracts/CharbonICCAD93.html
- ERL M94/40 — https://www2.eecs.berkeley.edu/Pubs/TechRpts/1994/ERL-94-40.pdf
- Miliozzi DAC'96 — https://websrv.cecs.uci.edu/~papers/compendium94-03/papers/1996/dac96/pdffiles/16_2.pdf
- Kirkpatrick ICCAD'94 — https://cecs.uci.edu/~papers/compendium94-03/papers/1994/iccad94/pdffiles/09d_3.pdf
- Malavasi TCAD'96 — https://infoscience.epfl.ch/record/85458

**EM-aware routing, device patterns, learned guidance**
- SAGERoute — https://past.date-conference.com/proceedings-archive/2023/DATA/623.pdf
- Martins DATE'14 — https://past.date-conference.com/date17/files/proceedings/2014/pdffiles/02.4_1.pdf
- Madhusudan DATE'21 — https://past.date-conference.com/proceedings-archive/2021/pdf/1837.pdf
- Sharma DATE'21 — https://past.date-conference.com/proceedings-archive/2021/pdf/1829.pdf
- AnalogFold — https://www.cse.cuhk.edu.hk/~byu/papers/C223-DAC2024-PARoute.pdf
- Kunal ICCAD'20 — https://arxiv.org/pdf/2010.00051
- Yang & Vemuri DATE'06 — https://past.date-conference.com/proceedings-archive/2017/pyear/PAPERS/2006/DATE06/PDFFILES/03B_6.PDF

**Symbolic and LLM-assisted sizing**
- White-Op — https://arxiv.org/pdf/2601.21321
- AmpAgent — https://arxiv.org/html/2409.14739v1
- LLM-derived equations — https://arxiv.org/abs/2604.07387
- SymXplorer — https://github.com/NooriDan/SymXplorer
- SLiCAP — https://analog-electronics.tudelft.nl/slicap/SLiCAP_python/slicap_python.html

**PCells, placement and routing tools**
- RALF — https://github.com/JakobRat/RALF
- Pretl ESSERC'24 — https://mos-ak.org/bruges_2024/publication/7_Pretl_ESSERC_2024_openAnalogRF.pdf
- Magic sky130 PCells — https://raw.githubusercontent.com/RTimothyEdwards/open_pdks/master/sky130/magic/sky130.tcl
- KLayout sky130 PCells — https://github.com/fossi-foundation/sky130_klayout_pdk
- Grus ILP variants — https://www.scitepress.org/Papers/2023/117893/117893.pdf
- HB\* patent — https://patents.google.com/patent/US7873928
- OSIRIS — https://arxiv.org/pdf/2601.19439

**Datasets and benchmarks**
- AMS-SizingBench — https://github.com/yuxi120407/AutoSizer
- LOADBench — https://arxiv.org/html/2610.21591
- AnalogGym — https://github.com/CODA-Team/AnalogGym
