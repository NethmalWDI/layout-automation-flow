# Phase 3: Implementation plan for S0–S3

**Date:** 2026-10-23 (Fri, evening)
**Deadline:** S0–S3 final on Sunday 2026-10-25.
**What this plan builds on:**
- `docs/01_inventory.md`
- `docs/02_analysis.md` and Addendum A
- `docs/progress_log.md`, Step 0 (ALIGN flow verified)

This document covers the design under test, the engines and why, each stage S0–S3, the handoff to S4, the schedule, risks, and what you need to do.

---

## 0. Decisions already fixed, and why

| Decision | Choice | Why (evidence) |
|---|---|---|
| Design under test | **Sized `example_ota_5t`** (5 MOSFETs + V1 bias): M1/M2 24/0.5, M3/M4 8/1, M5 24/1. Specs: gain ≥ 30 dB, GBW ≥ 20 MHz, PM ≥ 60°, CL = 1 pF. | Your choice. It has real specs and measured pre-layout results (31.7 dB, 104 MHz, 81°). |
| Hierarchy and equations | Reused from `5t-ota` through an explicit, checked **name map** (Addendum A1) | The differential-mode equations are independent of tail biasing. The bias block is mapped manually (**ASSUMPTION**). |
| Execution | Everything runs in container `layout-s0s3` (iic-osic-tools 2026.10), driven through the `docker-eda` MCP server. MAGICAL runs in `magical-s0s3`. | Same environment as your work. Nothing is installed on the host. |
| Physical engines | **gLayout = S3 device generator** (pending your install approval). **ALIGN = automatic PnR baseline** and constraint consumer. **MAGICAL = mock-PDK constraint consumer.** | Step 0 showed that ALIGN-pdk-sky130 fixes L at 0.15 µm, so it cannot draw our devices correctly. gLayout handles L natively (`docs/02_analysis.md` §2). |
| Ground truth for "done" | Independent Magic DRC (with a negative control) and Netgen LVS against the *design* reference, with the report text parsed | Lesson from Vibe Tapeout and our own Step 0: units and port pitfalls produce false fails, and false passes are also possible. |

---

## 1. Data flow and interfaces

```
circuits/example_ota_5t/source/*        circuits/5t-ota/source/*      inputs/name_map.yaml
              │                                    │                          │
              ▼                                    │                          │
S0  ingest + freeze ──► outputs/S0/circuit_ir.json, device_map.json, pdk_config.yaml, ref/*.spice
              │                                    │
              ▼                                    ▼
S1  electrical intent ──► outputs/S1/intent.json, net_symbol_map.json, sensitivity.json, operating_values.json
              │            (import slot: inputs/operating_values.json, so Monday's nodal results replace ours)
              ▼
S2  constraint compiler ──► outputs/S2/constraints.json (engine-neutral IR)
              │                 ├─► engines/align/<subckt>.const.json
              │                 ├─► engines/magical/<top>.sym, <top>.symnet
              │                 └─► engines/glayout/params.json
              ▼
S3  device generation ──► outputs/S3/variants.json + primitives/<block>/<variant>/{.gds, .png, drc/, lvs/}
              │
              ▼
handoff/S3_to_S4.json   (one manifest pointing to everything S4+ needs)
```

**Rules that hold across every stage**

1. **No stage reads a later stage's outputs.**
2. **Every output file records its inputs.** It carries a `provenance` block with input file paths, their SHA-256 hashes, the tool versions and the git commit.
3. **Every number carries a status.** One of:
   - `verified`: checked by an independent tool
   - `estimated`: computed but not independently checked
   - `placeholder`
   - `assumption`
   - `not_evaluated`

   Each one also carries its units.
4. **Code layout.** Code lives in `src/s0` … `src/s3`, plus `src/common` for parsing, provenance and the container runner. Tests live in `tests/`, run with `pytest` inside the container.

---

## 2. Stage S0: ingest and freeze

**Goal:** a canonical, validated, immutable description of the circuit, plus the per-engine device mappings.

**Inputs**

| Input | Purpose |
|---|---|
| `circuits/example_ota_5t/source/example_ota_5t_sized.spice` | The netlist |
| `config.yaml` | Specs and conditions |
| `measurements.json` | Pre-layout reference values |
| `circuits/5t-ota/source/{hierarchy,primitives}.json` | Used only to check the name map |
| `inputs/name_map.yaml` | Written by me, reviewed by you |

**Outputs, in `outputs/S0/`**

- **`circuit_ir.json`**
  - `design`
  - `ports[]`: `{name, role ∈ supply|ground|input|output|bias}`
  - `nets[]`: `{name, kind ∈ port|internal}`
  - `devices[]`: `{name, type ∈ nmos|pmos, model, terminals{d,g,s,b}, W_um, L_um, nf, m, W_total_um, source_line}`
  - `removed_elements[]`: V1, with its reason
  - `specs`, `conditions`, `measured_prelayout`
  - `provenance`
- **`device_map.json`.** For each device and each engine (glayout, align, magical):
  - the parameters actually used
  - `deviation{W_rel, L_rel}`
  - `representable: bool`
  - `notes`

  This holds the ALIGN legalisation from Step 0 and its L limitation.
- **`pdk_config.yaml`**
  - `pdk: sky130A`, the open_pdks commit, tool versions
  - paths to `magicrc`, the netgen setup and the KLayout `lyp`
  - the rule values S2 needs: met1–met2 area and fringe capacitance per µm, read from the PDK files (§7, R3)
- **`ref/ota5t_design_ref.spice`**: the LVS reference in µm, with V1 removed and VBIAS as a port.

**Algorithm**

1. Parse the netlist with continuation lines.
2. Build a NetworkX bipartite graph of devices and nets.
3. Classify the ports.
4. Check the name map against the `5t-ota` primitives graph: same terminals, same roles.
5. Produce the per-engine mappings by reusing `make_align_input.py` and `make_magical_input.py` as library functions.

**Acceptance tests**

| ID | Test | Pass criterion |
|---|---|---|
| T0.1 | Device inventory | Exactly 5 MOSFETs; models ∈ {nfet_01v8, pfet_01v8} |
| T0.2 | Round trip | `circuit_ir` → SPICE matches the source in Netgen ("match uniquely", no property errors) |
| T0.3 | Name map | Pair M1/M2 ↔ XM3/XM4, load M3/M4 ↔ XM1/XM2, tail M5 ↔ XM5 (terminal-by-terminal); XM6 is reported "unmapped (bias reference absent)" |
| T0.4 | Hash freeze | Source hashes equal `circuits/SOURCE_SHA256.txt` |
| T0.5 | Negative tests | Unknown model, missing W, a dangling net and a duplicate name are each rejected with a clear error |

**Effort:** 0.5 day.

---

## 3. Stage S1: electrical intent

**Goal:** a quantitative statement of what matters electrically, and why.

**Inputs**

- `outputs/S0/circuit_ir.json`
- `circuits/5t-ota/source/5t-ota_differential_equations.json`, `hierarchy.json`
- `inputs/name_map.yaml`
- `inputs/operating_values.json`, **if present** (Monday slot)

**Outputs, in `outputs/S1/`**

- **`operating_values.json`.** For each transistor: gm, gmb, gds, cgs, cgd, cgb, cdb, csb, Id, Vgs, Vds, Vdsat, region.
  - Source: an ngspice `.op` of the sized design at the `config.yaml` conditions (tt, 27 °C, VCM 0.9 V), read from the BSIM4 instance parameters in the container.
  - These are mapped onto the `mosfet-ssm` elements: C1 = cgb, C2 = cgs, C3 = cgd, C4 = cdb, C5 = csb, G1 = gm, G2 = gmb, R1 = 1/gds.
  - **If `inputs/operating_values.json` exists, it replaces this file** (same schema). That is how Monday's nodal-analysis results plug in.
- **`intent.json`**
  - `blocks[]`: `{name, role, devices, from_hierarchy_path}`
  - `matching[]`: `{devices, kind ∈ diff_pair|mirror|ratio, purpose, evidence[], priority}`
  - `critical_nets[]`: `{net, rank, metrics_affected, score}`
- **`net_symbol_map.json`.** For each net, which equation symbols a layout capacitance or coupling on it adds to (table in Phase 2 §3, S1). It includes net0 → level-1 `C1_X1_X1` and marks net1 as "not observable in DM".
- **`sensitivity.json`.** For each net × metric (gain_db, gbw_mhz, pm_deg):
  - the symbolic ∂M/∂C, its numeric value, and the normalised Ŝ
  - **validation** against a transistor-level ngspice AC run with +δC at that net, for δ = 5 fF and 20 fF
  - status

**Algorithm**

1. Run the OP and map it to the small-signal elements.
2. Evaluate the equations bottom-up: level 0 → 1 → 2 → performance.
   - **Check:** the predicted gain, GBW and PM vs `measured_prelayout`. Agreement is expected within the known model limits: about 0.4 dB of gain, and PM overestimated by the missing mirror pole.
3. Compute `sympy.diff` with respect to each net's symbol.
   - For net0, use the level-1 model and a two-pole H(s), because level 2 drops the mirror pole.
4. Validate with transistor-level ngspice runs on the real sized netlist with an added capacitor (this was not possible with dummy data).
5. Rank nets by |Ŝ| weighted by spec tightness.

**Acceptance tests**

| ID | Test | Pass criterion |
|---|---|---|
| T1.1 | Matching | {M1, M2} diff_pair and {M3, M4} mirror are found with evidence; M5 is a single device |
| T1.2 | OP sanity | All devices in saturation; supply current within 1% of the measured 84.78 µA |
| T1.3 | Model vs measured | Gain within 1 dB and GBW within 15%. PM is **reported**, not gated (known bias) |
| T1.4 | Sensitivity validation | For OUTP and net3: sign agrees, and the magnitude is within 20% of the ngspice finite difference; the finite difference is stable across δ = 5 and 20 fF (within 10%) |
| T1.5 | Import slot | Dropping a test `inputs/operating_values.json` changes `sensitivity.json` and nothing else |
| T1.6 | Negative test | A net name that does not exist in the map is rejected |

**Effort:** 1 day. This is the riskiest stage numerically.

---

## 4. Stage S2: constraint compilation

**Goal:** turn intent and sensitivities into hard constraints, soft priorities and parasitic budgets, then compile them for each engine.

**Inputs:** the S0 and S1 outputs, and `pdk_config.yaml`.

**Outputs**

- **`outputs/S2/constraints.json`** (the engine-neutral IR). Each entry has:
  - `id`, `class ∈ hard|soft|budget|proposal`
  - `kind` (symmetry, same_template, group, net_priority, max_added_cap, max_wire_length_hint, port_side, …)
  - `targets`, `value`, `units`
  - `derived_from` (S1 ids)
  - `status`
- **Engine files:**
  - `engines/align/ota5t.const.json`
  - `engines/magical/ota5t.sym`, `ota5t.symnet`
  - `engines/glayout/params.json`

**Budget method**

- **Margin per metric:** `m = M_measured − M_min`. From the measured values:

  | Metric | Measured | Minimum | Margin | Note |
  |---|---|---|---|---|
  | Gain | 31.70 dB | 30 dB | 1.70 dB | Tight |
  | GBW | 104 MHz | 20 MHz | 84 MHz | Loose |
  | PM | 80.9° | 60° | 20.9° | |

- **Safety factor:** η = 0.5 (**ASSUMPTION**).
- **Split across nets.** Each net k gets `w_k = |Ŝ_k| / Σ|Ŝ|`, and then `ΔC_k,max = w_k · η · m / |S_k|`. The tightest metric across the three wins.
- **From budget to wire-length hint:** `L_max = ΔC_max / c_per_um(layer)`. The per-µm capacitance comes from `pdk_config.yaml`. If it is not found, the hint is marked `not_evaluated` and no value is invented.

**Engine compilation**

| Engine | What gets emitted |
|---|---|
| ALIGN | `SymmetricBlocks` (M1, M2) and (M3, M4); `SameTemplate`; `NetConst` criticality derived from the rank; `PowerPorts`/`GroundPorts` |
| MAGICAL | `.sym` lines `M1 M2`, `M3 M4`; `.symnet` `INP INN` |
| gLayout | Pattern choice per block and routing-priority order |

**Acceptance tests**

| ID | Test | Pass criterion |
|---|---|---|
| T2.1 | Names | Every target resolves in `circuit_ir` |
| T2.2 | Consistency | No two hard constraints conflict, and every value has units |
| T2.3 | Budget arithmetic | Recomputing from `sensitivity.json` reproduces the budgets; Σ allocated ≤ η·m |
| T2.4 | ALIGN consumes it | Run B1 (constraints) vs the A0 baseline finishes; a symmetry error is measured from the placement JSON |
| T2.5 | MAGICAL consumes it | Mock-PDK run with our `.sym` finishes |
| T2.6 | Negative tests | Unknown net, missing units, and a matching pair with unequal W/L (`SameTemplate` must be refused) are each rejected |

**Effort:** 0.75 day.

---

## 5. Stage S3: device and primitive generation

**Goal:** SKY130-legal layout variants for each hierarchy block, with the electrical identity of the devices preserved.

**Tool:** gLayout, installed in its own venv in `layout-s0s3` (**needs your approval**). Fallback: Magic's built-in sky130 device generators, scripted in Tcl.

**Blocks and variants**

| Block | V0 | V1 | V2 |
|---|---|---|---|
| Pair M1/M2 | Two separate FETs | Common-centroid `diff_pair` | Interdigitated |
| Load M3/M4 | Separate | Interdigitated | — |
| Tail M5 | Single FET | Fingered (nf = 2/4) | — |

Every variant has exactly W_total and L from `circuit_ir`.

**Outputs**

- `outputs/S3/variants.json`. For each variant:
  - `block`, `variant`, `gds`, `png`, `bbox_um`, `area_um2`
  - `pins[{name, layer, x, y}]`
  - `devices[{name, W_total, L, nf}]`
  - `drc{total, report}`, `lvs{result, report}`
  - `satisfies[constraint ids]`
  - `parasitic_estimate{AD, AS, PD, PS}` or `not_evaluated`
- The geometry files under `outputs/S3/primitives/…`

**Acceptance tests**

| ID | Test | Pass criterion |
|---|---|---|
| T3.1 | DRC | Magic `drc(full)` reports 0 errors, and the negative control is flagged |
| T3.2 | LVS | Netgen "match uniquely" against that block's slice of `ref/ota5t_design_ref.spice`, with **no property errors**. L and W must match, which ALIGN could not do |
| T3.3 | Pins | All block ports exist as labelled pins |
| T3.4 | Symmetry | For pair and mirror variants, the centroid offset between matched devices is ≤ 1 grid unit (measured) |
| T3.5 | Reproducibility | Regenerating gives an identical GDS hash for fixed parameters |
| T3.6 | Comparison column | ALIGN's A0 primitives are listed with their DRC/LVS status (L mismatch) |

**Effort:** 1 day. Fallback cost: +0.5 day.

---

## 6. Handoff from S3 to S4 (where Monday's inputs plug in)

**`handoff/S3_to_S4.json`** contains:

- `design`
- pointers to `circuit_ir`, `intent`, `sensitivity`, `constraints` and `variants`
- `budgets[]`: net, max_added_cap_fF, metric, status
- `engine_files`
- `open_issues[]`
- `provenance`

S4 (placement) consumes the variants and the constraints. S6/S7 later check the budgets against PEX.

**Monday's nodal-analysis results** go into `inputs/operating_values.json`, or a richer `inputs/nodal_analysis.json` whose adapter is defined on Monday. **Only S1 → S2 re-run. S0 and S3 are unchanged unless the sizes change.**

---

## 7. Schedule

| When | Work | Gate |
|---|---|---|
| Fri 23 (done) | Step 0: ALIGN flow, DRC/LVS scripts; MAGICAL build | Step-0 log |
| Sat 24, morning | S0 implementation and tests | T0.1–T0.5 |
| Sat 24, afternoon and evening | S1: OP extraction, equations, sensitivities, ngspice validation | T1.1–T1.6 |
| Sun 25, morning | S2 compiler, plus ALIGN B1 and MAGICAL runs | T2.1–T2.6 |
| Sun 25, afternoon | S3 with gLayout (or the fallback), DRC/LVS per variant | T3.1–T3.6 |
| Sun 25, evening | Handoff file, README end to end, final review | All gates, or blockers documented |

I stop for your review after each stage, as agreed.

---

## 8. Risks and fallbacks

| ID | Risk | Fallback |
|---|---|---|
| R1 | gLayout install conflicts with the container's gdsfactory 9.51 | Separate venv. If it is still broken, use Magic's Tcl device generator (ships with sky130A) for S3. |
| R2 | The OP → small-signal mapping disagrees with measured performance | Report the discrepancy. Use the transistor-level finite difference as the primary sensitivity and the symbolic one as the explanation. Flag it for your nodal analysis on Monday. |
| R3 | Per-µm wire capacitance not found in the PDK files | Do not invent it. Keep budgets in fF and mark the length hints `not_evaluated`. Ask you. |
| R4 | ALIGN ignores or rejects a constraint | Record "not consumed" (that is itself a result). Do not patch ALIGN. |
| R5 | The MAGICAL build or run fails on the old image | Record it. MAGICAL is not on the S0–S3 critical path. |
| R6 | Disk space on C: (about 20 GB free after the MAGICAL image) | Keep run outputs small, and do not commit large GDS variants beyond the ones that matter. |

---

## 9. What you must do or provide

1. **Approve installing gLayout** (`pip install glayout==0.2.0`) in a venv inside `layout-s0s3`. Nothing changes on the host or the image.
2. **Confirm or change the assumptions:**
   - η = 0.5
   - the bias-block name mapping
   - ALIGN width legalisation, including the +5 % on the load (ALIGN only)
3. **Monday:** the nodal-analysis results, or a sample of their format, so I can fix the adapter schema.
4. **Keep Docker Desktop and Claude Desktop running** while I work (the MCP bridge needs both).
