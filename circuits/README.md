# circuits/

Read-only **copies** of upstream inputs. The originals in `Layout_automation/` are never modified.
`SOURCE_SHA256.txt` records the hashes taken at copy time.

| Folder | Origin | Use |
|---|---|---|
| `example_ota_5t/source/` | `llm-analog-sizing-hierarchical-optimization/results/example_ota_5t/` + `topologies/example_ota_5t/config.yaml` | **Design under test**: sized 5T OTA with specs and measured pre-layout performance |
| `5t-ota/source/` | `.../topologies/5t-ota/circuit.spice` + `.../results/5t-ota/*.json` | Hierarchy and symbolic equations, reused through a name map |
