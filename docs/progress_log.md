# Progress log

## 2026-10-23 — Step 0: full ALIGN flow on SKY130 (before S0–S3 code)

**Environment**

- **Container:** `layout-s0s3`, created from `hpretl/iic-osic-tools:2026.10` (ID 306585de35d1).
  - Created through the `docker-eda` MCP server.
  - The repo is mounted at `/foss/designs`.
  - No ports are published.
- **Tool versions** (from `runs/env/tool_versions.txt`):

  | Tool | Version |
  |---|---|
  | magic | 8.3.685 |
  | netgen | 1.5.324 |
  | klayout | 0.30.12 |
  | ngspice | ngspice-47 |
  | sky130A (open_pdks) | 1689ac3f |
  | Python | 3.12.3 |

- **ALIGN install:** `align-analoglayout==0.9.8`, in its own venv at `/opt/venv-align` (inside the container only; the image is untouched).
  - The full freeze is in `runs/env/requirements-align.lock.txt`.
  - It needed apt packages `coinor-libcgl1`, `coinor-libcbc3.1` and `coinor-libosi1v5`, plus **`python3-dev`**.
  - Issue: gdspy has no cp312 wheel and needs `Python.h`. The first install attempt failed on this; it is fixed in `scripts/setup_align.sh`.
- **ALIGN-pdk-sky130:** commit `3da43f0c22a4d6e2314a6bd4682ff938bb01a0ea`, cloned to `external/` (git-ignored).

**Smoke test: ALIGN's own `five_transistor_ota` (unmodified example)**

- **ALIGN run:** exit 0. Output `FIVE_TRANSISTOR_OTA_0.gds` is 36.5 × 43.0 µm (1571 µm²) and has 3 primitives: DP_NMOS_B, SCM_NMOS, SCM_PMOS.
- **Magic DRC** (`sky130A.magicrc`, `drc(full)`, euclidean, run on the flattened layout): **0 errors.**
  - Negative control: a 0.05 µm met1 sliver is flagged (1 error), so the checker is live.
  - The GDS layers 100/5, 235/5 and 104/0 that ALIGN writes are unknown to Magic and are skipped (boundary/annotation layers).
- **Netgen LVS** (`sky130A_setup.tcl`): **"Circuits match uniquely"**, with 300 devices and 208 nets.
  - The reference was expanded to explicit series and finger devices, because ALIGN realises `stack=3` as 3 series transistors per finger (`ref/five_transistor_ota_ref_expanded.spice`).
  - Two fixes were needed:
    - **Units:** the reference must be in µm (xschem/sky130 convention). In metres, netgen reports 200 % property errors.
    - **Ports:** Magic needs `port makeall`, otherwise the extracted cell has no pins.

**Our design: sized `example_ota_5t`**

- **Source:** copied from `llm-analog-sizing-hierarchical-optimization/results/example_ota_5t/`. SHA-256 hashes are in `circuits/SOURCE_SHA256.txt`.
- **Conversion** (`scripts/make_align_input.py`; report in `runs/align/inputs/ota5t/conversion_report.json`):
  - V1 (0.75 V) was removed, and its node is exposed as port `vbias`.
  - **ASSUMPTION, ALIGN only:** widths are legalised to an even NF × k fins × 0.21 µm, with 2 ≤ k ≤ 12. The limit is ALIGN `mos.py`: `(28 − k)/2 ≥ 8`, `k > 1`. Results:

    | Device | Reference W | ALIGN W | NF × fins | Error |
    |---|---|---|---|---|
    | M1, M2, M5 | 24 µm | 23.94 µm | 38 × 3 | −0.25 % |
    | M3, M4 | 8 µm | 8.40 µm | 4 × 10 | **+5.0 %** |

  - **Deviation from what was approved:** the approved values 24.15 µm and 8.19 µm are **not legal** in ALIGN. 115 and 39 fins are odd numbers, but ALIGN asserts an even NF. A first try at 19 fins per finger failed the `mos.py` height assertion.
  - **Limitation:** ALIGN-pdk-sky130 draws a **fixed 0.15 µm gate** (`layers.json` Poly Width = 150 nm). L = 0.5 and 1.0 µm **cannot be represented.**
- **ALIGN run:** exit 0. Output `OTA5T_0.gds` is 46.8 × 23.7 µm (1110 µm²) and has 3 primitives: DP_NMOS_B (M1/M2), NMOS_S (M5), SCM_PMOS (M3/M4). Picture: `runs/align/A0_ota5t_baseline/OTA5T_0.png`.
- **Magic DRC:** **0 errors** (negative control flagged).
- **Netgen LVS against the original sized design** (`ref/ota5t_design_ref.spice`):
  - **Topology and pins match uniquely** (5 devices, 8 nets).
  - **Property errors:**
    - **L:** 0.15 µm drawn, against 0.5 µm (pair) and 1.0 µm (load and tail).
    - **W:** the load is 8.4 µm against 8 µm (+4.9 %).

**Conclusion**

- The open ALIGN → SKY130 → Magic/Netgen flow works end to end. It is DRC-clean and LVS topology-clean on both circuits.
- For our sized OTA, however, the layout is **not electrically equivalent**: every gate length is wrong.
- **Decision input for S3:** stock ALIGN-pdk-sky130 cannot be the device generator for designs with L ≠ 0.15 µm. This confirms the Phase 2 recommendation of gLayout for S3. Alternatively, ALIGN's MOS generator would need an L-aware patch.

**Open issue**

- **MAGICAL image pull:** `jayl940712/magical:latest` did not complete through MCP. The `docker run` call blocks for longer than the 60 s bridge timeout.

**MAGICAL (in parallel)**

- **Source:** cloned into `external/MAGICAL` (git-ignored) at commit `199ab0719f85f74c79bf85a556118b132988a5fe`. Submodules:

  | Submodule | Commit |
  |---|---|
  | ConstGen | 6e1532d |
  | IdeaPlaceEx | a727c34 |
  | anaroute | 9ef33c2 |
  | device_generation | 4b4bd1f |

- **Image:** `jayl940712/magical:latest` is **not pulled yet**. The MCP `container_create` call blocks during the pull and times out at the bridge's 60 s limit.
- **Action needed from you:** run `docker pull jayl940712/magical:latest` once in PowerShell.
- **Next steps once the image is there:** create `magical-s0s3` → run `build.sh` (pip-builds the C++ components) → `examples/ota1/run.sh` on the mock PDK.
