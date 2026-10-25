# How each tool creates transistors: PDK PCell or its own geometry?

**Date:** 2026-10-24
**Question (yours):** Do ALIGN, MAGICAL and gLayout place the PDK's transistor PCells, or do they draw transistors themselves from layer rules? You want the flow to use the SKY130 PDK's own transistor PCells exactly.

## 1. Short answer

**None of the three engines uses the SKY130 PDK's PCells.** Each one draws its transistors itself, rectangle by rectangle, from its own description of the design rules.

| Tool | How it creates a MOSFET | Evidence (source code) | What that means for SKY130 |
|---|---|---|---|
| **ALIGN** (`ALIGN-pdk-sky130`) | Its own generator class, `MOSGenerator(DefaultCanvas)`. It draws grid-based "wires" for each layer (`Poly`, `Fin`, `Diff`, `M1` …) from `layers.json` pitches and widths. | `SKY130_PDK/mos.py` lines 10–60 (`self.addGen(Wire('pl','Poly',...))`). `layers.json` begins: *"rules … discussed in FinFET_MOCK_PDK.ppt"*. Poly `Width: 150`. | It inherits a FinFET-style abstraction: widths are quantised to 210 nm "fins", **L is fixed at 0.15 µm**, and NF must be even. These constraints are not SKY130's; they come from ALIGN. Step 0 confirmed it: LVS shows L = 0.15 against 0.5 and 1.0 µm. |
| **MAGICAL** | Its own `device_generation` Python package draws rectangles with `gdspy.Rectangle(...)`. | `device_generation/glovar.py`: `class tsmc40_glovar`, with hard-coded TSMC 40 nm layer numbers (`VIA8=58`, …). `Mosfet.py` / `Capacitor.py` use `gdspy.Rectangle`. | Written for TSMC 40 nm and a mock PDK. **No SKY130 description exists.** Porting means writing a new rule set and layer map. It would still be MAGICAL's geometry, not the PDK's PCell. |
| **gLayout** | Its own generator: `glayout/primitives/fet.py` builds fingers, diffusion, contacts and taps from `rectangle(...)` and `via_array(...)`, sized by generic rules (`pdk.get_grule("poly","mcon")…`) from `sky130_mapped`. | `fet.py` lines 45–120 (`__gen_fingers_macro`, `multiplier`, `nmos`). No call to Magic `gencell` anywhere in the package. | Real SKY130 layers and real L, so it is far closer than ALIGN. It is still a re-implementation, not the PDK PCell. Extracted AD/AS/PD/PS and well and tap structure can differ from the PDK cell. |

## 2. Where the PDK's own PCells actually are

The SKY130 PDK installed in your container (open_pdks 1689ac3f) ships parameterised device generators in two places:

1. **Magic: `$PDK_ROOT/sky130A/libs.tech/magic/sky130A.tcl`**
   - It defines `sky130::sky130_fd_pr__nfet_01v8_draw`, `…_defaults`, `…_check` and so on, for every primitive device. Examples: `sky130_fd_pr__nfet_01v8`, `pfet_01v8`, `*_lvt`, resistors, MIM caps.
   - You call it with `magic::gencell sky130::sky130_fd_pr__nfet_01v8 <name> w <W/finger> l <L> nf <n> m <m> guard 1 …`.
   - **This is the same generator xschem/Magic users get from the "Devices" menu.**
2. **KLayout:** the open_pdks KLayout tech folder (`libs.tech/klayout/pymacros`) also carries a sky130 PCell library. It is not yet evaluated here.

**Evidence this is the right path (run on 2026-10-24).** `scripts/magic_pcell_devices.py` generated all five OTA devices with the Magic PDK generator, at **exactly** the netlist values with no legalisation:

| Device | PCell | W (µm) | L (µm) | nf |
|---|---|---|---|---|
| M1, M2 | `sky130::sky130_fd_pr__nfet_01v8` | 24 | 0.5 | 1 |
| M5 | `sky130::sky130_fd_pr__nfet_01v8` | 24 | 1.0 | 1 |
| M3, M4 | `sky130::sky130_fd_pr__pfet_01v8` | 8 | 1.0 | 1 |

Magic's extraction of M1 gives:

`X0 S G D B sky130_fd_pr__nfet_01v8 ad=6.96 pd=48.58 as=6.96 ps=48.58 w=24 l=0.5`

That is **identical** to the xschem pre-layout netlist values (`ad=6.96 as=6.96 pd=48.58 ps=48.58`). The pre-layout simulation and the layout therefore describe the same device. Per-device DRC and LVS for all five are being run (`runs/pcell/ota5t_devices/pcell_check.json`).

## 3. What this means for our flow

The placer and router must **treat transistors (or matched groups) as black-box PDK PCell instances.** They place and connect them, but never redraw them. Options:

| Option | How it works | PCell-exact? | Effort and risk | Recommendation |
|---|---|---|---|---|
| **A. Magic PCells, then our own S4/S5** (Python placement, Magic Tcl routing) | S3 produces the PCell instances, plus `variants.json` with pins and bboxes read from the generated cells. S4/S5 place them and draw routes in Magic. | **Yes** | Medium. This is the core of your own O3 plan ("custom constrained placement/routing"). | **Primary path** |
| **B. Magic PCells, then gLayout routing** | Import each PCell GDS into gdsfactory (`import_gds`), attach ports at the D/G/S/B labels, then use gLayout `smart_route` / `c_route`. | **Yes** for devices. Routes come from gLayout. | Medium. gLayout must run in a Python 3.10/3.11 venv, because it pins numpy ≤ 1.24 and gdsfactory ≤ 7.7. | Strong secondary path |
| **C. RALF** (JKU, Apache-2.0, github.com/JakobRat/RALF, "IIC-RALF") | A published SKY130 flow that builds primitives **with Magic's PCell generator**, places them with RL or simulated annealing, and routes in Magic. Recognises diff pairs. | **Yes** | Needs evaluation: it is research code, and the only example given is a diff amp. | **Evaluate as the S4/S5 baseline**, in place of, or next to, ALIGN |
| **D. ALIGN with external primitives** | ALIGN can take user or blackbox primitives (`-b/--blackbox_dir`), so in principle PCell GDS/LEF could replace its MOS generator. | Possibly | High. Unverified on SKY130; its grid abstraction still applies to routing. | Not this week |
| **E. Port MAGICAL to SKY130** | Rewrite `glovar`, LEF and techfiles, and swap `device_generation` for PCell GDS. | Yes, if the device generator is replaced | Very high | Not this week. Keep MAGICAL as the algorithm and constraint reference. |

**How this changes the S3 plan (`docs/03_plan_S0-S3.md` §5)**

- The **S3 generator becomes the Magic PDK PCell** (`magic::gencell`). gLayout is kept as a comparison column (its own geometry).
- Variants are PCell parameter choices only: `nf` folding with W_total preserved, `guard`, contact coverage, and gate-contact options. Every variant must pass the same DRC/LVS gate.
- Matched groups (common-centroid, interdigitated) cannot be expressed *inside* a single PDK PCell. The PDK generator draws one transistor, with fingers and multipliers, per call. Matching therefore becomes an **S4 placement constraint over PCell instances**, for example ABBA ordering of multiplier units.

**What "MAGICAL mapped to SKY130" would mean:** keep MAGICAL's placement ideas (symmetry-aware analytical placement) but feed it PDK PCell abstracts. That is option E above, and a later-stage task.

## 4. Status of items you asked about

| Item | Status |
|---|---|
| ALIGN examples (all 5 in ALIGN-pdk-sky130) | Running (batch). Gallery to follow. |
| MAGICAL examples | ota1, ota2, ota3 and comp routed (exit 0). adc1 was running when Docker stopped responding. |
| gLayout install | Failed on Python 3.12: it pins `numpy<=1.24.0`, which has no 3.12 wheel. Next attempt: a Python 3.10/3.11 venv via `uv`. |
| Magic PDK PCells for our OTA | All 5 generated at the exact sizes. Extraction confirmed for M1. Full DRC/LVS was running. |
