# Design package reference (inputs/<design>/package.yaml)

A design enters the flow as one YAML file plus the files it points to. Start from
`inputs/_template/`. S0 checks every field; anything missing is reported as *pending* and never
filled in by guesswork. Files that we predicted ourselves (because the sizing stage has not delivered
them yet) carry `provenance: PREDICTED` inside and are listed in the design's `circuits/<design>/SOURCE.md`.

## Fields

| Field | Required | Meaning |
|---|---|---|
| `design` | yes | Name; used for `outputs/<stage>/<design>/` |
| `description` | no | Free text |
| `inherit` | no | Path of another package; this one overrides its keys (used by stress variants) |
| `netlist` | yes | Sized netlist: one flat `.subckt` (hierarchical netlists: `scripts/flatten_spice.py`). Elements: SKY130 MOSFETs `sky130_fd_pr__{n,p}fet_01v8[_lvt]` (`W`, `L`, `nf`, `mult`, `m`), PDK passives (`sky130_fd_pr__cap_mim_m3_1`, `sky130_fd_pr__res_generic_po`), ideal `R`/`C`, ideal `V`/`I` sources. Anything else is refused, never skipped |
| `config` | yes | `interface` (testbench port -> DUT port; `NC` for unused), `analyses`, `conditions` (`VDD_V`, `VCM_V`, `CL_F`, `temp`, `corner`), `specs` (`min`/`max` per measurement) |
| `achieved` | yes, or `null` | `measurements.json` from the upstream schematic simulation, which S0 must reproduce within 0.1 %. `null` together with `specs_from_achieved`: the achieved values are this flow's own S0 simulation |
| `reference` | no | External reference metrics (`{"metrics": {...}, "source": ..., "simulator_setup": ...}`), compared by gate G0.8 with the tolerances in `src/s0/ingest.py` (`REF_TOL`) |
| `testbenches` | yes | ngspice decks (below), one per analysis |
| `dut_subckt_in_testbench` | yes | Name of the DUT `.subckt` inside the decks |
| `upstream.*` | no | Sizing-stage hierarchy, primitives, symbolic equations and name map |
| `bias_sources` | no | `{element: PORT}`: ideal sources **and off-chip passives** inside the DUT (bias current, CM reference, an off-chip bias resistor): kept for simulation, removed in the layout view, the node they drive exposed as `PORT` |
| `port_roles` | no | Roles of DUT ports outside the six standard ones: `bias_ac_ground` (held by an ideal source in the testbench wrapper, e.g. a CMFB control driven by an ideal CMFB: AC ground in differential mode), `bias_monitor` / `bias_current` (solved in AC) |
| `ac_drive` | no | `{INP: 0.5, INN: -0.5}`: the AC drive of each input in the AC bench, when it is not read from plain `V` sources (benches with DC-feedback chokes) |
| `conditions_override` | no | Overrides of `config.conditions` (e.g. a smaller load) |
| `specs_from_achieved` | no | Derive specs from the achieved values: `min_delta`, `min_factor`, `max_factor` per spec (labelled ASSUMPTION) |
| `eta` | no | Fraction of each margin given to layout in S2 (default 0.5); `--eta` on the command line wins |
| `mc_runs` | no | Monte Carlo runs of the S0 mismatch step (default 200) |
| `s3_build_mode` | no | Which S3 options to build: `A-free` (default), `A-bin` or `B` (large designs) |
| `s1_extras` | no | Optional S1 add-ons (`symbolic_patch`) |

## Testbenches

- Decks are plain ngspice files that include the SKY130 library (`.lib $PDK_ROOT/sky130A/libs.tech/combined/sky130.lib.spice tt`) and set `.param VDD_V=... VCM_V=... CL_F=...`.
- The DUT is reached as `x1` (a wrapper `dut_amp` with ports `INP INN OUTN VDD VSS OUTP`) containing `XDUT` (the design's `.subckt`). Device operating points are read as `@m.x1.xdut.<device>.m<model>[param]`. The wrapper may also hold testbench-only elements (an ideal CMFB).
- Each measurement is printed as `echo MEAS <name> <value>`; names carry their unit (`gain_db`, `gbw_mhz`, `pm_deg`, `isup_ua`, `power_uw`, `vout_v`, `voutcm_v`, `vnoise_nv_rthz`, ...).
- Naming: `<io>_amp_<ANALYSIS>.spice`, where `<io>` is `diso` (differential in, single-ended out `OUT`) or `dido` (differential in and out `OUTP`/`OUTN`, `CL_F` on each output, signal `v(OUTP) - v(OUTN)`).
- New packages should use `scripts/benchlib.py`: the loop is closed at DC through 1 GH chokes from the output(s) to the inverting input(s) and open from 1 Hz up, so high-gain amplifiers sit at their follower operating point (as in an offset-corrected open-loop bench) and a one-sided parasitic cannot rail the output.

## Package generators (examples)

| Design | Script | What is predicted |
|---|---|---|
| `loadbench_miller` | `scripts/make_loadbench_package.py <LOADBench folder> loadbench_miller --select` | specs, noise bench, symbolic model |
| `ttsky25a_fd` | `scripts/make_ttsky25a_package.py` | specs, primitives, symbolic model |
| `iadc_ota` | `scripts/make_iadc_package.py` | specs, primitives, symbolic model, the CMFB's AC model |

## What each stage produces

| Stage | Main outputs (`outputs/<stage>/<design>/`) |
|---|---|
| S0 | `circuit_ir.json`, `device_map.json`, `ref/` LVS references, `pcell/` per-device GDS + DRC/LVS, `pvt.json` (45 PVT points), `mc.json` (mismatch Monte Carlo), `s0_report.json` |
| S1 | `operating_point.json`, `linear_model.json`, `symbolic_check.json`, `sensitivity.json`, `sensitivity_r.json`, `intent.json`, `s1_report.json` |
| S2 | `budgets.json`, `baselines.json`, `eta_sweep.json`, `hierarchy.json`, `constraints.json`, `verification.json`, `s2_report.json` |
| S3 | `option_table.json`, `device_decisions.json` (main mode + every mode), `s3_report.json`; cells in `outputs/S3/_cells/` |
