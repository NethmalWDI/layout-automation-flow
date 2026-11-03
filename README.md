# layout-automation-flow

An electrically informed analog layout flow for the SkyWater SKY130 open PDK, stages S0–S3:

- **S0 Ingest:** freeze a sized netlist, its specs and testbenches; bind every transistor to its exact SKY130 PCell (DRC/LVS-checked).
- **S1 Intent:** operating point, exact small-signal model, sensitivity of every spec to capacitance at each net and resistance at each terminal (checked against SPICE).
- **S2 Budgets:** joint parasitic budgets (fF, Ω) and layout rules, verified all at once in SPICE; G2.0 says before layout whether a compact layout can fit.
- **S3 Devices:** PCell options per device, chosen against the budgets, each cell DRC/LVS-signed.

Designs (`./flow list`):

| Design | What | Source |
|---|---|---|
| `example_ota_5t` | sized 5T OTA (development) | upstream sizing team |
| `ota5t_stress` | the same, 200 fF load, tight specs (development) | derived |
| `loadbench_miller` | two-stage Miller op-amp, one Pareto point | LOADBench (CC BY 4.0) |
| `ttsky25a_fd` | two-stage fully differential op-amp, taped out on TTSKY25a | NethmalWDI/Fully_differential_opamp (Apache-2.0) |
| `iadc_ota` | fully differential folded-cascode OTA with a hand-drawn layout | r09g/iadc (MIT) |

Inputs the upstream stages did not provide are predicted by the package scripts and labelled PREDICTED
(`circuits/<design>/SOURCE.md`). The before/after comparison of the plan-v2 updates is in `docs/before_after.md`.

## For reviewers: S0–S3 on the 5T OTA and LOADBench

**What to read first:** `docs/s0_s3_walkthrough.html` (open it in a browser; `.md` for the same text). It shows,
for `example_ota_5t` and `loadbench_miller`, what each stage did and what came out: every gate, the main numbers
and plots, and an explanation of each failed gate. It opens with a short guide to the ideas it uses (margin, eta,
expected need). Every table and plot has a *How to read it* note and, where the numbers allow, a *What it shows here*
line built from that design's results. It is generated from the committed outputs.

**Expected result.** FAIL means a gate reported a finding, but the stage finished and wrote its report. ERROR
(a crash) does not occur.

| Design | S0 | S1 | S2 | S3 | Run time |
|---|---|---|---|---|---|
| `example_ota_5t` | PASS | PASS | PASS | PASS | about 30 min (20 of them S0's 45 PVT points and Monte Carlo) |
| `loadbench_miller` | FAIL (G0.7) | FAIL (G1.6) | PASS | FAIL (G3.5) | about 20 min |

LOADBench's three FAILs are findings, not flow errors:
- **G0.7:** the SKY130 PCell drawn at the netlist's exact size for one device (`XNormalTransistorNmos3`, one
  484 µm finger) breaks the PDK's metal-area rule met1.6 at its gate pad. The other 8 devices pass DRC and LVS.
  S3 draws its own cells and widens that pad, so every cell it chooses is DRC-clean (G3.1).
- **G1.6:** 1 of 54 resistance-sensitivity checks. A resistor at P5's source shifts the bias point, which a
  small-signal model at a fixed operating point cannot predict within the limit. The flow passes on the
  transistor-level SPICE rate, which includes the shift.
- **G3.5:** 3 of 6 device types have no cell within their S2 allowance (LOADBench's gain margin is 1 dB). S3
  keeps the least-bad cell and flags the type. The circuit with every chosen cell still meets every spec in SPICE
  (G3.3).

**Run it** (Windows PowerShell, Docker Desktop running). On this PC the container `layout-s0s3` already mounts the
repository (`docker start layout-s0s3` if it is stopped). Without `FLOW_CONTAINER`, `flow.ps1` starts a
throwaway container from the pinned image instead.

```powershell
$env:FLOW_CONTAINER="layout-s0s3"
.\flow.ps1 status example_ota_5t           # gate verdicts of the committed run, per stage
.\flow.ps1 status loadbench_miller
.\flow.ps1 run example_ota_5t              # S0 -> S3, about 30 min
.\flow.ps1 run loadbench_miller            # S0 -> S3, about 20 min
.\flow.ps1 run example_ota_5t --stage S1   # one stage, from the earlier stages' outputs (S1 or S3: under a minute)
.\flow.ps1 test                            # 138 unit tests + golden comparison with the committed outputs (~15 s)
```

The same inside the container: `docker exec -e IIC_OSIC_TOOLS_QUIET=1 layout-s0s3 bash -lc "cd /foss/designs &&
source scripts/env.sh && python3 -u -m src.flow run example_ota_5t"`. The variable stops the image's login
profile from printing its `[INFO]` lines. `-u` makes each step's line appear as it finishes; without it, Python
holds its output until the run ends. The launchers set both. `status all` also lists the three other designs. Their outputs are the
plan-v2 runs of 25–27 October and are not part of this review; flow record 7.5 gives their results.

**Where the outputs go:**
- each stage: `outputs/<stage>/<design>/`, with its gates in `<stage>_report.json` (e.g. `outputs/S2/loadbench_miller/s2_report.json`);
- per-step logs: `runs/logs/flow/<design>/`;
- the run summary: `outputs/flow/<design>/flow_summary.json`.

A run rewrites these folders. The results reproduce (the review's clean runs matched Phase A's exactly), but run
ids and timestamps change. Discarding the changes in GitHub Desktop returns to the committed run.
`python3 scripts/make_s0s3_walkthrough.py` regenerates the walkthrough from a new run.

**Further reading:** `docs/flow_record.md` (the journey: what was built, what went wrong and how it was found;
section 7.13 is the current version, 7.14 this review), `docs/progress_log.md`, and `PREREG.md` (hypotheses and
thresholds, with dated amendments).

## Quick start (anyone, any OS)

You need Docker (Docker Desktop on Windows/macOS) and about 20 GB of disk for the EDA image.
Nothing else is installed on your machine: the launchers run everything inside the pinned image
`hpretl/iic-osic-tools:2026.10` with this repository mounted at `/foss/designs`.

```bash
git clone <this repo> && cd layout-automation-flow
./flow list                              # designs found in inputs/        (Windows: .\flow.ps1 list)
./flow run example_ota_5t                # S0 -> S3 for one design (about 10 min the first time)
./flow run example_ota_5t --stage S2     # one stage; it reads only the earlier stages' outputs
./flow status all                        # gate table per design and stage
./flow test                              # unit tests + golden comparison of the committed outputs
./flow test --stage S1 --rerun           # re-run S1 for the golden designs, then compare (overwrites outputs/S1/<design>/)
./flow run loadbench_miller --variant v1 # the flow as it was before the plan-v2 updates (ablation)
./flow run ttsky25a_fd --no-pvt          # skip the 45-point PVT sweep and Monte Carlo in S0
```

Inside the container you can also call the stages directly, e.g. `python3 -m src.s2.run inputs/<d>/package.yaml
--alloc v1|v2 --no-pvt --no-baselines --eta 0.9` or `python3 -m src.s3.run inputs/<d>/package.yaml --mode B|A-bin|A-free
--rules v1|v2`; `python3 scripts/compare_before_after.py snap <design> <tag> [<S3 folder>]` and `... report` keep and
compare runs.

Plan v3 Phase A's runs of `example_ota_5t` and `loadbench_miller` have the snapshot tag `after_v3a` (2026-11-02;
flow record 7.13). `python3 scripts/compare_eta09_rerun.py <design> --first <tag> --rerun after_v3a --json
outputs/phaseA/<design>/<name>.json` compares any two tags. Always give `--json`: the default path is the eta 0.9
re-run's committed comparison.

**Hand-drawn reference layouts** (plan v2, baseline 8): `python3 scripts/reference_layout.py <design> <gds> <cell>
--ports "<pin>=<bench node>,..." [--bias "<off-chip element>;..."] [--corner ff --temp 20 --mim-load 1,1,100 --tag <name>]`
extracts a layout with Magic (LVS netlist and a capacitance-only PEX), runs LVS against the flow's layout view and
simulates the schematic, the drawn devices and the PEX in the flow's own benches
(`outputs/reference_layout/<design>/reference_layout[_<tag>].json`; `--rc` adds a Magic extresist R+C extraction,
`--map-shorted` ties ports that Magic reports as electrically shorted, e.g. a sub-cell's copy of a clock pin).
`scripts/reference_ttsky25a.sh` runs it for the taped-out TTSKY25a tile at the flow's conditions and at the
designers' `gain_and_phase.sch` conditions; `scripts/reference_iadc.sh` for the hand-drawn iadc OTA (CMFB clocks
held in phase 1, cmc driven by the flow's ideal CMFB law).

Each stage writes to `outputs/<stage>/<design>/` and logs to `runs/logs/flow/<design>/`; the run summary is
`outputs/flow/<design>/flow_summary.json`. A stage's status comes from the exit codes of its commands
(`src/common/hygiene.py`):

| Status | Exit code | Meaning |
|---|---|---|
| **PASS** | 0 | every gate passed |
| **FAIL** | 3 | a gate failed, but the stage finished and wrote its report (e.g. S3 flags a device type that does not fit) |
| **ERROR** | anything else, e.g. 1 from a crash; or no fresh report | the stage did not finish; it stops at that command |

The committed outputs are the reference results; `./flow test` fails if a re-run moves any of them beyond its
tolerance (`tests/golden/`).

**Clean runs.**
- S2 starts from an empty `outputs/S2/<design>/`. The run before moves to `outputs/S2/<design>.prev/`
  (git-ignored), replacing an earlier `.prev`.
- S3 does the same with its report files. It keeps `sim/`, its simulation cache, which is reused only for an
  identical deck, and `outputs/S3/_cells/`, the cell cache.
- Every S2 JSON carries the run's `run_id` and `eta`. The S3 files carry their own `run_id` and the `s2_run_id`
  they were made from.
- `compare_before_after.py snap` refuses (exit 2) when `budgets.json`, `s2_report.json` and `baselines.json`
  disagree on `run_id` or `eta`, when `budgets.json` has no `s2_report.json`, or when any of them is older than the
  S2 start in `flow_summary.json`.

**Your own design:** copy `inputs/_template/` to `inputs/<name>/`, fill in `package.yaml` (every field is
explained in `docs/INPUTS.md`), and run `./flow run <name>`. Missing upstream files are reported as pending,
never invented.

**What changed in plan v2 (2026-10-26):**

- S0 handles current sources, ideal and PDK passives (MIM, poly resistors), differential outputs, off-chip test elements and an external-reference gate (G0.8), and runs 45 PVT points plus a mismatch Monte Carlo (G0.9, G0.10).
- S2 floors every budget at what the cheapest library cell already puts there (G2.7), no longer trims binding elements in phase 2 (finding R19), adds a constraint per spec and PVT point (G2.9), and scores four other budget rules on the same sensitivities (G2.8: per-net, equal split, a plain LP, the LP with floors), each in SPICE at its own worst PVT points, with outcomes unsafe / infeasible / ok, plus an eta sweep.
- S3 decides in three option modes (B: nf as in the netlist; A-bin: the finger stays in the sized device's SKY130 model bin; A-free) plus a rule-of-thumb folding baseline, and a cell may always use the library's lowest access resistance (G3.7).

**Plan v3 Phase A (from 2026-11-01; `docs/plan_v3_phaseA.md`, PREREG amendment of that date):** the package key
`budget_corners: nominal` (set for `example_ota_5t` and `loadbench_miller`) makes S2 budget at the nominal corner
only. S2 still computes the PVT points' constraints and reports, in G2.9, what the final budgets use at each of the
45 points as a fraction of eta × that point's margin. That is reported, not gated. Without the key, S2 budgets at
every PVT point, as in plan v2.

- **One tolerance** (`src/common/tolerance.py`, `TOL_USE` = 0.02 of the allowed use, eta × margin). It is used by:
  - G2.5's gate and its closure step;
  - `baselines.outcome()` (the "unsafe" line);
  - S3, as `TOL_USE` × eta of the margin.

  G2.5's old 10 % stays only as a reported column, `within_first_order_error_10pct`.
- **G2.8 and the PVT points.** With `budget_corners: nominal`, G2.8 still SPICE-checks each rule's 5 most-used PVT
  points from G2.9; they are scored, not budgeted, and G2.5 stays nominal.
  - `outcome` covers every simulated check, as in plan v2; `outcome_nominal` gives the nominal checks alone.
  - The PREREG note of 2026-11-02 records this, after review D.
- **At a bound.** G2.8 counts a budget within 10⁻⁶ below its floor or need as at it, not below it
  (`baselines.AT_BOUND_TOL`). Phase 2 leaves pinned budgets 10⁻⁹ of room.
- **`lp_floor_k`.** G2.8 also scores `lp_floor_k`: `lp_floor` with ours' upper bound, 10 × need, so six rules are
  compared in all. With that room the max-sum LP may starve some elements to give others more; that is a result,
  not an error.
- **Saturation do-no-harm.** For a device already below vdsat in the schematic, S3 allows a further drop of at
  most `TOL_USE` × |vds − vdsat|.
- **Mirror banks and designer groups.** S0 merges mirror blocks that share their gate and source nets into one
  bank. It reads the designer's groups from `designer_groups:` (see `docs/INPUTS.md`).
- **Route lengths from the representative cells.** The wiring part of each element's expected need (one stub
  across each pin's device) uses the bounding box of the representative S3 cell of the device's type. Before, it
  used S0's as-sized PCell. A type without a library cell, and every passive, keeps the as-sized PCell.
  - This is the need both G2.0 and the allocation use (PREREG amendment 2026-11-01, step 8), so budgets move with
    it.
  - G2.0 lists `route_lengths` per device and keeps the as-sized route as a second column,
    `fraction_of_margin_route_as_sized_pcell`.
- **PM reference.** PM = 180 + phase at the UGB − the 1 Hz phase rounded to the nearest multiple of 180°. The S1
  linear model and new benches (`scripts/benchlib.py`) use it. The frozen benches keep the unrounded 1 Hz phase;
  for the 5T and LOADBench that is 0.00002° and 0.0016° away.
- **PDK environment.** The iic-osic-tools image starts on its default PDK, IHP-SG13G2, so ngspice would read IHP's
  init file. `scripts/env.sh` switches to sky130A with the image's own command (`sak-pdk sky130A`, sourced as
  `sak-pdk-script.sh`), which ends up loading sky130's ngspice settings (`ngbehavior=hsa`, `enable_noisy_r`). Source
  it before every flow command; `./flow` and `flow.ps1` already do. `TOOL_ENV` (`src/common/tools.py`) pins the
  same variables for every tool the flow starts.
- **Running the tests.** `./flow test`, or `.\flow.ps1 test` from PowerShell, works from any shell. The image's
  login profile sets `USER` to "1000\ndesigner"; `scripts/env.sh` keeps the part after the newline, because a
  newline in pytest's temp folder name made Netgen fail the S0 round-trip test.
- **Line endings.** `.gitattributes` checks every text file out with LF, on Windows too. With Git for Windows'
  default `core.autocrlf=true` and no attributes, a checkout wrote CRLF, and bash could not parse `scripts/env.sh`
  (flow record row 66).

**Repository rules:** third-party material and licences are listed in `THIRD_PARTY.md`; hypotheses and
thresholds for the experiments are fixed in `PREREG.md` before baselines run.

## Documents

- **`docs/flow_record.md`**: the living record of the flow. For each stage it gives the inputs and outputs, JSON excerpts, DRC/LVS pictures and the problems met. It is updated at every stage.
- **`docs/s0_s3_walkthrough.md`** (and `docs/s0_s3_walkthrough.html`, self-contained, images embedded): what S0–S3 did on `example_ota_5t` and `loadbench_miller` and what came out: each gate, the main numbers and plots, an explanation of every failed gate, and for each table and plot how to read it and what it shows for that design. Every number is read from `outputs/`; the "How to read it" notes are the only typed explanations besides the gate meanings and the known findings. Regenerate it after a run, inside the container: `python3 scripts/make_s0s3_walkthrough.py [design ...] [--no-html] [--out FILE.md]` (pandoc writes the HTML).
- `docs/progress_log.md`: chronological log.
- `docs/01_inventory.md`, `docs/02_analysis.md`, `docs/03_plan_S0-S3.md`: inventory, analysis and plan.
- `docs/04_device_generation.md` … `docs/07_stage_guide_and_sunday_baseline.md`: device generation, literature, final plan and stage guide.
- `docs/context/project_context_S0-S9.md`

## Environment (development setup used so far)

1. **Docker MCP server.** Set it up once by following `tools/mcp-docker-eda/README.md`.
2. **Container.** `layout-s0s3`, from `hpretl/iic-osic-tools:2026.10`, with this repo mounted at `/foss/designs`.
3. **ALIGN.** Install it into the container, as root:

   ```bash
   docker exec -u 0 layout-s0s3 bash /foss/designs/scripts/setup_align.sh
   ```

## Step 0: run ALIGN end to end

Run these inside `layout-s0s3`, from `/foss/designs`:

```bash
# convert the sized netlist to ALIGN input; deviations are logged to conversion_report.json
python3 scripts/make_align_input.py circuits/example_ota_5t/source/example_ota_5t_sized.spice runs/align/inputs/ota5t --subckt ota5t

# place and route with ALIGN -> GDS
bash scripts/run_align.sh runs/align/inputs/ota5t runs/align/A0_ota5t_baseline -n 1

# render the layout to PNG
klayout -zz -rd gds=runs/align/A0_ota5t_baseline/OTA5T_0.gds -rd png=runs/align/A0_ota5t_baseline/OTA5T_0.png -r scripts/gds_to_png.py

# Magic DRC (with a negative control)
bash scripts/magic_drc.sh runs/align/A0_ota5t_baseline/OTA5T_0.gds OTA5T_0 runs/align/A0_ota5t_baseline/drc

# Magic extraction + Netgen LVS against the design reference
bash scripts/magic_lvs.sh runs/align/A0_ota5t_baseline/OTA5T_0.gds OTA5T_0 runs/align/A0_ota5t_baseline/ref/ota5t_design_ref.spice ota5t runs/align/A0_ota5t_baseline/lvs_vs_design
```

## S0 — ingest and freeze a design package

Run inside `layout-s0s3`, from `/foss/designs`:

```bash
python3 -m pytest -q tests/test_s0.py tests/test_s0_integration.py   # unit + LVS negative-control tests
python3 -m src.s0.ingest inputs/example_ota_5t/package.yaml        # outputs/S0/example_ota_5t/
python3 -m src.s0.ingest inputs/ota5t_stress/package.yaml          # stress variant (CL = 200 fF)
python3 -m src.s0.pcell_binding outputs/S0/example_ota_5t          # G0.7: each device drawn by its SKY130 PCell, DRC + LVS
python3 -m src.s0.pcell_binding outputs/S0/ota5t_stress
```

G0.7 draws every device with `magic::gencell sky130::sky130_fd_pr__{n,p}fet_01v8` at its exact W/L/nf/m. It then runs Magic DRC (0 errors required; a met1 sliver must be flagged) and Netgen LVS against the device's own netlist line (match with no property errors required; a reference with L + 0.1 µm must be rejected).

**Outputs:**

| File | Contents |
|---|---|
| `circuit_ir.json` | Devices, nets, port roles, hierarchy blocks, specs, achieved values, margins, pending inputs |
| `device_map.json` | Exact Magic PCell call per device |
| `pdk_config.yaml` | PDK and tool configuration |
| `ref/*_full.spice` | Simulation view |
| `ref/*_layout.spice` | LVS reference |
| `pcell/XM*.gds`, `pcell/XM*.png`, `pcell/drc_*`, `pcell/lvs_*` | PCell devices, renders, and DRC/LVS runs (including the negative controls) |
| `pcell_binding.json` | G0.7 per-device verdicts |
| `s0_report.json` | Every gate, with its evidence |

## S1 — electrical intent (operating point, exact linear model, sensitivities)

Run inside `layout-s0s3`, from `/foss/designs`, after S0:

```bash
python3 -m src.s1.run inputs/example_ota_5t/package.yaml   # outputs/S1/example_ota_5t/ (about 2 min, 15 ngspice runs, sequential)
python3 -m src.s1.run inputs/ota5t_stress/package.yaml
python3 -m src.s1.run inputs/ota5t_stress/package.yaml --no-fd   # skip the transistor-level cross-check (seconds)
python3 scripts/make_record_figures.py example_ota_5t ota5t_stress  # refresh the pictures in docs/flow_record/img/
```

**Gates:**

| Gate | Check |
|---|---|
| G1.1 | Operating point: all devices saturated, supply current within 1 %, charge-matrix conservation |
| G1.2 | Linear model vs SPICE: within 0.2 dB / 3 % / 2°. PM's reference is the 1 Hz phase rounded to a multiple of 180°; the 1 Hz phases of both are recorded (`pm_reference`) |
| G1.3 | Linear-model sensitivities vs SPICE finite differences (5 and 20 fF): derivative within 20 %, or first-order prediction at +20 fF within 5 % of the margin |
| G1.4 | Matching groups (diff pair, mirror) present and equal-sized |
| G1.5 | Upstream symbolic model vs SPICE; reported, not gated |

**Outputs:**

| File | Contents |
|---|---|
| `operating_point.json` | Per-device operating-point values |
| `linear_model.json` | Linear model vs SPICE |
| `sensitivity.json` | Per net and pair: linear, SPICE and symbolic slopes, and the fF that would use up the margin |
| `node_classes.json` | Dominant and non-dominant pole nodes, mirror node, tail, bias, supplies |
| `currents.json` | Branch currents per net |
| `intent.json` | Matching groups; nets and coupling pairs ranked by criticality |
| `symbolic_check.json` | Upstream equations evaluated at this operating point |
| `plots/` | Bode and sensitivity plots |
| `s1_report.json` | All gates, with their evidence |

## LOADBench subset (no full download)

```bash
/opt/venv-tools/bin/python scripts/loadbench_fetch.py index TwoStageOpAmps.zip
/opt/venv-tools/bin/python scripts/loadbench_fetch.py fetch TwoStageOpAmps.zip SimpleTwoStageOpAmp_SimpleOpAmp1_1/
```

## S1 extension: series resistance at device terminals

`python3 -m src.s1.run ...` (same command as above) also writes `sensitivity_r.json`:

- per terminal group (matched pairs varied together): dSpec/dR from transistor-level SPICE (AC, NOISE, DC headroom) and from the linear model;
- the mechanism, with gate G1.6: small-signal, or a bias shift confirmed by re-solving the linear model at the shifted operating point;
- the systematic offset of a one-sided resistor, measured in a unity-gain follower.

## S1 add-on: pole drop-out study (patched copies of the upstream equations)

```bash
python3 -m src.s1.symbolic_patch inputs/example_ota_5t/package.yaml inputs/ota5t_stress/package.yaml
```

- Writes two patched **copies** of `circuits/5t-ota/source/5t-ota_differential_equations.json` to `inputs/example_ota_5t/upstream_patched/` (the original is never modified):
  - `P1`: the mirror pole-zero doublet, using only symbols the file already defines;
  - `P2`: P1 plus the transcapacitance gm(s) = gm - s*Cm, Cm ~= (2/5)*Cgs.
- Evaluates the original, P1 and P2 with the S1 evaluator against SPICE: `outputs/S1/<design>/symbolic_patch_check.json` and `plots/symbolic_patch.png`.
- Explained in `docs/flow_record.md`, section 3.9.

**Two-stage Miller (LOADBench), Plan v3 Phase A step 10:**

```bash
python3 -m src.s1.symbolic_patch_miller inputs/loadbench_miller/package.yaml
```

It also runs inside `./flow run loadbench_miller --stage S1`, through `s1_extras: [symbolic_patch_miller]`.

- It writes `inputs/loadbench_miller/upstream_patched/equations.predicted.P1.json`, a patched copy of the
  PREDICTED textbook file, which stays unchanged in `circuits/`.
- The copy adds the NMOS-mirror pole-zero doublet: Gm(s) = gm1/2·(1 + 1/(1 + s·τm)).
  - τm = C(FirstStageYout1) / (gm + gds of the diode device + gds of the mirror-side input device).
  - C is the S1 linear model's capacitance at that node.
- It is labelled **PREDICTED (patched, post hoc)**, because it was written after this circuit's PM gap was seen.
  G1.5 still reports the unpatched file, not gated.
- Results go to `outputs/S1/loadbench_miller/symbolic_patch_check.json` and `plots/symbolic_patch.png`.

## S2: requirement compiler (budgets, rules, verification)

Run inside `layout-s0s3`, from `/foss/designs`, after S1:

```bash
python3 -m src.s2.pdk_parasitics                         # once: per-um R/C of li1..met4 measured with Magic
python3 -m src.s2.run inputs/ota5t_stress/package.yaml   # outputs/S2/ota5t_stress/  (eta 0.9 from the package)
python3 -m src.s2.run inputs/example_ota_5t/package.yaml # eta 0.5 (default)
python3 -m src.s2.run inputs/<design>/package.yaml --eta 0.7   # override for one run
```

**eta** (the fraction of each margin given to layout) comes from `--eta` if given, else the package key `eta`, else 0.5. `budgets.json` records the value used (`eta`) and where it came from (`eta_source`). The stress variant sets `eta: 0.9` (decision of 2026-10-25).

**Gates:**

| Gate | Check |
|---|---|
| G2.1 | Every target resolves |
| G2.2 | Units and provenance on every rule |
| G2.3 | Allocation: max-min plus refinement; LP cross-check; reproducible |
| G2.4 | Linear model at the budget point (info) |
| G2.5 | SPICE verification: per check, its harmful budgets inserted at once; use <= eta x margin (+2 %, `TOL_USE`; +10 % before Phase A); spec met |
| G2.6 | Hierarchy shares sum to the budgets |
| G2.10 | SPICE vs first order, per simulated check (G2.5, G2.8): checks with a sign disagreement or a difference above 0.25 of the margin (ASSUMPTION, for review); with nominal budgets, each spec's worst PVT point beside the nominal result (info) |

**Outputs:**

| File | Contents |
|---|---|
| `budgets.json` | Every budget, with its expected need, binding check and margin used |
| `hierarchy.json` | Block-port and top-level shares of every net budget |
| `constraints.json` | Typed rule IR |
| `verification.json` | SPICE results of the budget verification |
| `plots/` | Budget and verification plots |
| `s2_report.json` | All gates, with their evidence |

## S3: device design (PCell options, decisions, sign-off)

Run after S2:

```bash
python3 -m src.s3.run inputs/ota5t_stress/package.yaml --workers 4   # builds/uses outputs/S3/_cells (cached)
python3 -m src.s3.run inputs/example_ota_5t/package.yaml
python3 -m src.s3.run inputs/ota5t_stress/package.yaml --cells-only   # only build/measure the option cells
python3 -m src.s3.run inputs/loadbench_miller/package.yaml --relax-fallback default \
    --out runs/tmp/s3_planv2_rule                                     # plan v2's relaxed-type rule, beside the results
```

**Relaxed types.** When no option of a device type stays within its allowance, S3 still keeps one and flags the
type (G3.5).
- **The rule since 2026-10-27** (PREREG amendment): S3 keeps the option whose worst check, access resistance of d, g
  and s included, is broken least (`--relax-fallback least-bad`, the default).
- **Plan v2's rule** (`--relax-fallback default`) kept the default PCell, i.e. the device as sized, or the option
  with the largest slack if that cell was not built. Every plan-v2 result used it, and so do the v1 variant
  (`--variant v1`) and plan v2's scripts.
- `./flow run <design> --relax-fallback default` reproduces plan v2's S3.
- `./flow test --rerun` re-runs S3 with the rule recorded in each golden snapshot; plan v2's snapshots record the
  old rule.
- `--out <folder>` writes S3 beside the main results.

Plan v2 tested the new rule post hoc on its 'after' runs (`scripts/plan_v2_after_queue.sh`): every design whose
'after' S3 relaxed a type, in `outputs/posthoc/least_bad/<design>/`, snapshot tag `after_posthoc_leastbad`.
`scripts/plan_v2_eta09_rerun.sh` then runs S2 at eta 0.9 again for example_ota_5t and loadbench_miller, because
their first runs overlapped a Windows standby. It uses snapshot tag `after_eta0.9_rerun` and keeps the S2 folder
and a clock record in `outputs/posthoc/eta09_rerun/<design>/`. `python3 scripts/compare_eta09_rerun.py <design>...`
compares each first run with its re-run.

Each option cell is a SKY130 Magic PCell (exact W/L), plus met2 finger straps and D/G/S/B labels. Each cell gets:

- DRC (with a negative control);
- LVS against the sized netlist line, checking W, L and nf (with a negative control);
- a Magic cell extraction;
- access resistances.

**Gates:**

| Gate | Check |
|---|---|
| G3.1 | DRC of the chosen cells |
| G3.2 | LVS of the chosen cells |
| G3.3 | All chosen cells and their access R in the circuit: specs met, margin use within the allowance |
| G3.4 | Option table complete |
| G3.5 | No relaxation |
| G3.6 | The model cards add no gate resistance of their own (rgatemod = 0) |

**Outputs:**

| File | Contents |
|---|---|
| `option_table.json` | Every option |
| `device_decisions.json` | The chosen option per device type and why |
| `plots/option_space.png` | Area against slack for every option; filled: the main mode's options, which S3 chooses from; hollow: the other modes'. `python3 scripts/replot_s3_options.py [design ...]` redraws it from a run's saved tables |
| `s3_report.json` | All gates, with their evidence |

S4 onward will be added here as it is implemented.
