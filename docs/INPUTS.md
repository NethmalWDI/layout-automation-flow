# Design package reference (inputs/<design>/package.yaml)

A design enters the flow as one YAML file plus the files it points to. Start from
`inputs/_template/`. S0 checks every field; anything missing is reported as *pending* and never
filled in by guesswork. Files that we predicted ourselves (because the sizing stage has not delivered
them yet) are listed under `predicted:` and carry `provenance: predicted` inside.

## Fields

| Field | Required | Meaning |
|---|---|---|
| `design` | yes | Name; used for `outputs/<stage>/<design>/` |
| `description` | no | Free text |
| `inherit` | no | Path of another package; this one overrides its keys (used by stress variants) |
| `netlist` | yes | Sized netlist: one `.subckt` with SKY130 `sky130_fd_pr__{n,p}fet_01v8[_lvt]` devices (`W`, `L`, `nf`, `mult`), optional ideal sources for bias |
| `config` | yes | `interface` (testbench port -> DUT port; `NC` for unused), `analyses`, `conditions` (`VDD_V`, `VCM_V`, `CL_F`, `temp`, `corner`), `specs` (`min`/`max` per measurement) |
| `achieved` | yes | `measurements.json`: `{"measurements": {"<testbench>": {"<meas>": value}}}` from the schematic simulation that S0 must reproduce within 0.1 % |
| `testbenches` | yes | ngspice decks (below) |
| `dut_subckt_in_testbench` | yes | Name of the DUT `.subckt` inside the decks |
| `upstream.*` | no | Sizing-stage hierarchy, primitives, symbolic equations and name map |
| `predicted` | no | Which upstream files are our predictions |
| `bias_sources` | no | Ideal sources inside the DUT: kept for simulation, removed in the layout view, their node exposed as a port |
| `conditions_override` | no | Overrides of `config.conditions` (e.g. a smaller load) |
| `specs_from_achieved` | no | Derive specs from the achieved values (stress variants only; labelled ASSUMPTION) |
| `eta` | no | Fraction of each margin given to layout in S2 (default 0.5); `--eta` on the command line wins |
| `s1_extras` | no | Optional S1 add-ons |

## Testbenches

- Decks are plain ngspice files that include the SKY130 library (`.lib $PDK_ROOT/sky130A/libs.tech/combined/sky130.lib.spice tt`) and set `.param VDD_V=... VCM_V=... CL_F=...`.
- The DUT is reached as `x1` (a wrapper `dut_amp` with ports `INP INN OUTN VDD VSS OUTP`) containing `XDUT` (the design's `.subckt`). Device operating points are read as `@m.x1.xdut.<device>.m<model>[param]`.
- Each measurement is printed as `echo MEAS <name> <value>`; names carry their unit (`gain_db`, `gbw_mhz`, `pm_deg`, `isup_ua`, `power_uw`, `vnoise_nv_rthz`, ...).
- Naming: `<io>_amp_<ANALYSIS>.spice`, where `<io>` is `diso` (differential in, single-ended out) or `dido` (differential in and out; support for `dido` is being added with the fully differential benchmarks).

## What each stage produces

| Stage | Main outputs (`outputs/<stage>/<design>/`) |
|---|---|
| S0 | `circuit_ir.json`, `device_map.json`, `ref/` LVS references, `pcell/` per-device GDS + DRC/LVS, `s0_report.json` |
| S1 | `operating_point.json`, `linear_model.json`, `sensitivity.json`, `sensitivity_r.json`, `intent.json`, `s1_report.json` |
| S2 | `budgets.json`, `hierarchy.json`, `constraints.json`, `verification.json`, `s2_report.json` |
| S3 | `option_table.json`, `device_decisions.json`, `s3_report.json`; cells in `outputs/S3/_cells/` |
