# layout-automation-s0-s3

An electrically informed analog layout flow for SKY130, covering stages S0–S3. The first test case is a sized 5T OTA.

## Documents

- **`docs/flow_record.md`**: the living record of the flow. For each stage it gives the inputs and outputs, JSON excerpts, DRC/LVS pictures and the problems met. It is updated at every stage.
- `docs/progress_log.md`: chronological log.
- `docs/01_inventory.md`, `docs/02_analysis.md`, `docs/03_plan_S0-S3.md`: inventory, analysis and plan.
- `docs/04_device_generation.md` … `docs/07_stage_guide_and_sunday_baseline.md`: device generation, literature, final plan and stage guide.
- `docs/context/project_context_S0-S9.md`

## Environment

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
| G1.2 | Linear model vs SPICE: within 0.2 dB / 3 % / 2° |
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

S2 and S3 will be added here as they are implemented.
