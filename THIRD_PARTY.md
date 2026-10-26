# Third-party material

| Material | Where | Licence | How it is used |
|---|---|---|---|
| SkyWater SKY130 PDK (open_pdks 1689ac3f) | inside the image `hpretl/iic-osic-tools:2026.10` | Apache-2.0 | Device models, Magic PCells, DRC/LVS decks; not committed |
| IIC-OSIC-TOOLS image | Docker Hub `hpretl/iic-osic-tools:2026.10` | Apache-2.0 (image scripts); tools under their own licences | Runs Magic, Netgen, ngspice, KLayout, xschem |
| Upstream 5T OTA design (`circuits/5t-ota/`, `circuits/example_ota_5t/`) | committed, read-only copies | Project-internal (llm-analog-sizing team) | Inputs; never modified |
| LOADBench two-stage op-amps (`circuits/loadbench/`) | committed subset | CC BY 4.0, Zenodo 10.5281/zenodo.21759759 (Azevedo et al., MLCAD'26) | Benchmark inputs; attribution kept here and in the flow record |
| Stanford iadc (`r09g/iadc`) OTA | vendored read-only in `circuits/iadc_ota/upstream_src/` (schematics, netlists, OTA layout, licence, commit id) | MIT | Fully differential benchmark with a hand-drawn reference layout |
| TTSKY25a fully differential op-amp (`NethmalWDI/Fully_differential_opamp`) | vendored read-only in `circuits/ttsky25a_fd/upstream_src/` (schematics, testbenches, GDS, licence, commit id) | Apache-2.0 | Fully differential benchmark with a fabricated reference layout |
| SpiceXplorer (`MacAnalog/spicexplorer-release`) | not vendored; its per-net budget rule (budget = margin fraction x margin / per-unit rate, `postlayout.score_c_budgets`) is re-implemented in `src/s2/baselines.py` | PolyForm Noncommercial 1.0.0 | Per-net injection budget baseline (research use) |

Material without a licence (for example `wulffern/cnr_ota_sky130nm`) is not committed and not redistributed.
