# layout-automation-s0-s3

An electrically informed analog layout flow for SKY130, covering stages S0–S3. The first test case is a sized 5T OTA.

## Documents

- `docs/01_inventory.md`
- `docs/02_analysis.md`
- `docs/progress_log.md`
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

Stages S0–S3 will be added here as they are implemented.
