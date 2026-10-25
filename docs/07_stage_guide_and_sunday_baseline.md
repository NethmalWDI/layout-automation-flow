# Stage guide: what each stage takes in, does and produces, plus Sunday's baseline

**Date:** 2026-10-24
**Companion to:** `06_final_plan_critical_review.md` and the slide deck.
**Running example:** the sized 5T OTA (`example_ota_5t`). Every stage below is illustrated on it.

---

## 1. The 5T OTA we use as the running example

| Device | Role | Model | W/L (µm) |
|---|---|---|---|
| M1, M2 | input differential pair | nfet_01v8 | 24 / 0.5 |
| M3, M4 | PMOS current-mirror load | pfet_01v8 | 8 / 1 |
| M5 | tail current source, gate at V1 = 0.75 V | nfet_01v8 | 24 / 1 |

**Nets:**

| Net | What it is |
|---|---|
| INP, INN | inputs |
| OUTP | output, loaded by CL = 1 pF |
| net3 | mirror gate / M1 drain |
| net1 | tail |
| VBIAS | M5 gate |
| VDD, VSS | supplies |

**Specs** (required → achieved in schematic simulation):

| Spec | Required | Achieved |
|---|---|---|
| Gain | ≥ 30 dB | 31.7 dB |
| GBW | ≥ 20 MHz | 104 MHz |
| PM | ≥ 60° | 81° |
| Power | ≤ 1000 µW | 153 µW |
| Input noise | ≤ 400 nV/√Hz | 339 nV/√Hz |

---

## 2. What we need for S0, against what we have today

| Input | Why S0 needs it | Status today | Where it is / what to request |
|---|---|---|---|
| **Sized netlist** | The circuit to lay out | **Have** | `circuits/example_ota_5t/source/example_ota_5t_sized.spice` |
| **Specs and conditions** | Defines margins | **Have** | `config.yaml`: specs, VDD 1.8 V, VCM 0.9 V, CL 1 pF, tt, 27 °C |
| **Achieved (schematic) specs** | Margin = achieved − required | **Have** | `measurements.json` |
| **Testbenches** | Re-run to confirm, and later reused for post-layout | **Have** | `diso_amp_AC/OP/NOISE.spice` decks in the upstream results |
| **Hierarchy** | Matching groups, sub-blocks | **Partial** | `5t-ota/hierarchy.json` describes the 6-transistor variant. We map it by hand: M1/M2 = diff pair, M3/M4 = load mirror, M5 = tail (no reference device). **Request:** stage-1 support for a voltage-biased tail, so the hierarchy is generated rather than mapped |
| **Nodal analysis (symbolic)** | The sensitivities | **Partial** | `5t-ota_differential_equations.json`: level maps plus level-2 gain/GBW/PM. **Request:** (a) a net-to-symbol map listing which symbols sit on which physical net; (b) the Ioutn→Ioutp coupling term (the mirror pole); later (c) common-mode, (d) mismatch and noise symbols |
| **Operating point** (gm, gds, C per device) | Turns symbols into numbers | **Missing, but we generate it** | ngspice `.op` in the container on the sized netlist |
| **Variation ranges** | Feasible range per node property | **Missing** | **Request** the format from your PSO stage: per node or device property, the min/max allowed and its effect on each spec. Sunday's baseline works without it and marks it `not_provided` |
| **More designs** | Layout-sensitive tests | **Missing** | **Request:** 3–4 sized two-stage designs from your PSO. Alternative: pull 3–4 LOADBench op-amps without downloading the 15 GB archive (§5) |

---

## 3. Each stage in plain terms

Each stage lists its input, method, output and the check that must pass. It then shows what the result looks like on the 5T OTA.

### S0 — Ingest and bind

- **Purpose.** Make one frozen, self-consistent description of the design, so nothing later works on a wrong or changed input.
- **Input:** the files in §2.
- **Method:**
  1. Read the netlist into a graph: devices as nodes, nets as edges, each with W, L, nf, m and model.
  2. Cross-check the files:
     - every device in the hierarchy exists in the netlist;
     - every symbol in the nodal analysis belongs to a real device or net;
     - specs and achieved specs use the same names and units.
  3. Re-run the testbenches in the container and confirm the achieved specs within a small tolerance.
  4. **Bind each transistor to its PDK PCell**: write down the exact generator call that will later draw it, `magic::gencell sky130::sky130_fd_pr__nfet_01v8 … w 24 l 0.5 nf 1 m 1`.
- **Output:**
  - `circuit_ir.json`: the cleaned description;
  - `device_map.json`: device → PCell call;
  - `ref/ota5t_ref.spice`: the netlist LVS compares against, in µm, with ports explicit.
- **Check:** the netlist written back out matches the original in Netgen ("match uniquely", no property errors); the re-run testbench reproduces 31.7 dB / 104 MHz / 81°.
- **Example result:** 5 devices; 8 nets; V1 recorded as an internal bias source; M1/M2/M5 bound to nfet PCells, M3/M4 to pfet PCells.

### S1 — Electrical intent (which node affects which spec)

- **Purpose.** Before any layout, know where extra capacitance or resistance hurts, how much, and why.
- **Input:** `circuit_ir.json`, the nodal-analysis equations, the operating point.
- **Method:**
  1. **Operating point.** Run ngspice `.op` and read each transistor's gm, gds, gmb, Cgs, Cgd, Cdb, Csb and Id.
  2. **Fill the symbolic model.** Map those values onto the small-signal elements of your stage-1 models (C1–C5, G1, G2, R1 per device). Evaluate the level maps upwards. Compare predicted gain and GBW with the measured values: this checks both the model and the mapping.
  3. **Sensitivities.** For each net, compute how much gain, GBW and PM change per added fF of capacitance at that net.
     - It uses the exact lower-level model where the top-level one is incomplete (e.g. net3, because the level-2 model drops the mirror pole).
     - Resistance is handled the same way for series wires where it matters.
  4. **Ground-truth check.** Add a small capacitor, e.g. 5 fF and 20 fF, at the net in the real transistor netlist and re-simulate. The symbolic and SPICE sensitivities must agree in sign and roughly in size.
  5. **Classify every net:**
     - dominant-pole node (OUTP);
     - non-dominant / mirror-pole node (net3);
     - tail / common-mode node (net1);
     - input pair (INP/INN);
     - bias (VBIAS);
     - supply (VDD/VSS).
  6. **Branch currents** from the operating point. In this circuit about 42 µA flows in each branch and 85 µA in the tail.
  7. **Matching groups:** {M1, M2} differential pair; {M3, M4} mirror. Taken from the hierarchy, and later strengthened by offset sensitivity when mismatch symbols exist.
- **Output:** `sensitivity.json` (net × spec table with units), `node_classes.json`, `currents.json`, `matching.json`, `intent.json`.
- **Check:** symbolic vs SPICE agreement on the top-ranked nets; predicted gain and GBW close to the measured values.
- **Example result (expected, not yet measured):**
  - OUTP is the dominant node, but its sensitivity per fF is tiny, because CL = 1 pF already sits there.
  - net3 matters most for PM.
  - Gain is almost insensitive to capacitance.
  - This is why we add the stress variant.

### S2 — Requirement compiler (budgets and rules)

- **Purpose.** Turn "this node matters" into numbers and rules a layout tool can obey and a checker can verify.
- **Input:** S1 outputs, the margins (achieved − required), variation ranges if provided.
- **Method:**
  1. **Margins.** Each spec has a required value. Its margin is how far the achieved value is from it.

     | Spec | Achieved | Required | Margin |
     |---|---|---|---|
     | Gain | 31.7 dB | 30 dB | 1.7 dB |
     | GBW | 104 MHz | 20 MHz | 84 MHz |
     | PM | 80.9° | 60° | 20.9° |

     A safety factor η = 0.5 reserves half of each margin.
  2. **Joint budget.** A small linear program chooses how much extra capacitance each net may receive, ΔC_k.
     - For every spec, the summed predicted degradation Σ |S_ik|·ΔC_k must stay within η × margin.
     - It maximises the smallest weighted allowance.
     - This avoids the trap of giving every node the whole margin.
  3. **Push budgets down the hierarchy.** Express the net budgets as limits at sub-block ports. Example: "the diff-pair block may add at most X fF at its output port." S4 can then judge each sub-block layout on its own.
  4. **Rules** (each one carries units and the equation that justifies it):
     - **Symmetric routing:** INP/INN and the two pair drains.
     - **Max length / capacitance per net:** budget ÷ capacitance per µm of the chosen metal. The per-µm values are read from the PDK; if absent, the rule is marked `not_evaluated`.
     - **Minimum width and number of vias from current:** needs SKY130 EM limits from the SkyWater documentation, *not yet sourced; never invented*.
     - **Shielding** for coupling-sensitive pairs that run near aggressors.
     - **No crossing** of digital or clock nets over high-impedance analog nets. Not applicable to this OTA, but the rule type exists.
     - **Placement:** symmetry axis for M1/M2, adjacency for M3/M4, common-centroid needed or not.
- **Output:** `budgets.json`, `constraints.json`.
- **Check:** every name resolves; units present; the LP is feasible, or the relaxation is documented; recomputing from `sensitivity.json` gives the same budgets.

### S3 — Device design (PCell options per transistor)

- **Purpose.** Make the device-level choices you listed, quantitatively. Then sign off each transistor before any assembly.
- **Input:** budgets, device list, the Magic PCell generator.
- **Method:**
  1. **Build an option table** for each device type (3 for this OTA). The Magic PCell options swept:

     | Option | Values |
     |---|---|
     | Fingers nf | 1, 2, 4, 8 — total width kept constant |
     | Gate contacts | top only / bottom only / both (`topc`, `botc`) |
     | Contact coverage | `diffcov`, `polycov` |
     | Via coverage | `viasrc`, `viadrn`, `viagate` |
     | Guard ring | `guard`, `full_metal` |

  2. **Extract each option.** Magic extraction with resistance turned on measures:
     - gate resistance;
     - source and drain access resistance;
     - drain and source junction capacitance;
     - area;
     - pin positions.

     **No value is assumed; each is measured.**
  3. **Choose per device.** Insert those parasitics into the S1 model and pick the option with the most budget slack per unit area. Examples of how the physics shows up:
     - **double gate contacts** lower gate resistance, and so its noise and pole, for the high-gm input pair;
     - **full source via coverage** lowers source resistance, which otherwise degenerates gm;
     - **more fingers** shrink the drain junction capacitance on a sensitive node such as net3.
  4. **Guard rings by rule:**
     - SKY130 latch-up tap distance;
     - isolation for high-impedance or noise-critical devices near aggressors.

     Their benefit cannot be verified with open tools, so this is stated openly.
- **Output:** `device_decisions.json` (option, measured parasitics, justification) and one PCell layout per device.
- **Check:** every device has 0 DRC errors (with the negative control) and an LVS match including W, L and nf.

### S4 — Sub-block variants

- **Purpose.** Several good, signed-off layouts for each building block, so the global step can choose.
- **Input:** S3 devices, the matching and budget rules.
- **Method:**
  - One template generator per block type, assembled from unit PCells.
  - Diff pair arrangements: side by side, ABAB, ABBA, 2-D common centroid, with dummies and a block guard ring.
  - Mirror arrangements: interdigitated by ratio.
  - Internal wiring is drawn by the template on a fixed track grid, so it is correct by construction.
  - Each variant is extracted locally, and its parasitics are inserted into the block's symbolic port model to predict its effect on the specs.
- **Output:** `variants.json`, a Pareto set per block (area, aspect ratio, pins, symmetry error, budget slack, predicted specs).
- **Check:** every variant is DRC- and LVS-clean; on a sample, the predicted effect is confirmed by full simulation (hypothesis H2).

### S5 — Selection, placement, routing

- **Purpose.** The smallest full layout that respects all budgets and rules.
- **Method:**
  - **Placement:** simulated annealing over a sequence pair. Each block also carries a "which variant" choice. Moves keep symmetric pairs mirrored.
  - **Cost:** area + predicted budget violation + critical-net length. Then compaction.
  - **Routing:** on a track grid, with width and via count from current, mirrored routes for symmetric nets, shield tracks, banned crossings and length limits.
  - **LLM role:** adjusts weights and shortlists; it never writes coordinates.
  - **Baseline:** RALF.
- **Output:** placement, top-level GDS, routing report.
- **Check:** top-level DRC and LVS clean; every routing rule verified by script.

### S6–S9

| Stage | What it does |
|---|---|
| **S6 Verify** | DRC (Magic plus the KLayout deck); LVS (Netgen); extraction that keeps coupling capacitance |
| **S7 Evaluate** | The same testbenches on the extracted netlist; compare the extracted capacitance at each node with its budget |
| **S8 Repair** | The sensitivities rank suspects; a counterfactual simulation confirms the cause; a local fix follows (option, variant or route); then S6 again |
| **S9 Select** | The smallest layout passing all specs |

---

## 4. Sunday's baseline: concrete steps (container, one job at a time)

| # | Time | Step | Output | Done when |
|---|---|---|---|---|
| 1 | Morning | Bring Docker up. Rename the stress copy: same OTA, CL = 50 fF, specs = achieved − 10 %, labelled `ota5t_stress` | — | Both designs listed in `circuits/` |
| 2 | Morning | `src/s0/ingest.py` + tests: parse, cross-check, bind to PCells, write the reference netlist; re-run AC/OP/NOISE testbenches for both designs | `outputs/S0/{circuit_ir,device_map}.json`, `ref/` | T0 gates pass |
| 3 | Midday | `src/s1/op_extract.py`: ngspice `.op` → per-device small-signal values. `src/s1/sensitivity.py`: symbolic model filled and evaluated, sensitivities per net. `src/s1/spice_check.py`: δC finite differences in transistor-level SPICE | `outputs/S1/*.json` + comparison plot | Agreement on OUTP and net3 |
| 4 | Afternoon | `src/s2/budgets.py` (LP with scipy `linprog`) + `src/s2/rules.py` | `outputs/S2/{budgets,constraints}.json` | T2 gates pass |
| 5 | Evening | `src/s3/option_table.py`: sweep PCell options for the 3 device types (≈ 50–100 small cells, run sequentially). `src/s3/decide.py`. Per-device DRC/LVS | `outputs/S3/{option_table,device_decisions}.json`, device GDS + PNG | Every chosen device DRC 0 and LVS match |
| 6 | Evening | Handoff file + progress log + commit | `handoff/S3_to_S4.json` | — |

**What you need to do on Sunday:**
1. Start Docker Desktop before I begin, with the memory limit raised.
2. Keep no other heavy container running, e.g. Monte Carlo.
3. Keep Claude Desktop open (it carries the bridge).
4. If possible, send the variation-range format and the net-to-symbol map.

**What the baseline will not have yet:**
- variation ranges, unless provided;
- common-mode, mismatch and noise budgets;
- EM-based widths (until the SkyWater EM data is sourced);
- S4 and S5.

Each missing item is marked in the outputs, not filled in.

---

## 5. Notes on your questions

### Token usage if the EDA tools were installed in my cloud workspace

- **Tokens are spent on text I read and write, not on compute time.** A simulation that runs for ten minutes costs nothing until I read its output.
- **The install itself:** a one-off cost of a few thousand tokens, with logs kept quiet.
- **After that:** running in the cloud or on your PC costs about the same. The PC route adds a little overhead from polling background jobs, because of the 60-second bridge limit.
- **So the choice is about reliability and availability, not tokens.** Staying on your PC, as you decided, is fine.

### Only 3–4 LOADBench designs

- **No per-design download exists.** LOADBench is split into category archives on Zenodo (two-stage: 15 GB).
- **Proposed approach:** read only the wanted folders out of the remote zip using HTTP range requests (e.g. the Python `remotezip` package). This transfers just the zip index plus the few designs: a few MB, not 15 GB.
- This needs one small pip install in the container, which I'll ask before doing.
- The 330 kB `AllCombinedTestbenches.zip` and the 0.6 MB reduced SKY130 library can be downloaded whole.

### Docker

**Agreed:** one heavy job at a time. Yesterday's lock-up came from:
- the ALIGN example batch;
- the MAGICAL adc1 run;
- Magic checks;
- your Monte Carlo run in another container.

All of these ran at the same time.
