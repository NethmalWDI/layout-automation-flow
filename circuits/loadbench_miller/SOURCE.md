# loadbench_miller: provenance

Generated 2026-10-26 by `scripts/make_loadbench_package.py circuits/loadbench/SimpleTwoStageOpAmp_SimpleOpAmp1_1 loadbench_miller --select`.

| Item | Origin | Status |
|---|---|---|
| Topology, device names, ad/as/pd/ps formulas | LOADBench `SimpleTwoStageOpAmp_SimpleOpAmp1_1` `example_run/CombinedTestBench.cir` | copied |
| Sizes W, L, Cc | `FinalPOFfull.csv` row 546 (0-based); tied sizes resolved through `params.cir` aliases | copied |
| Bias | ideal 10 uA sink, moved from LOADBench's testbench into the DUT as `Ibias` (bias source) | **adapted** |
| Miller capacitor | ideal capacitor `Capacitor2` (LOADBench has no PDK capacitor) | copied, **no layout device** |
| Reference metrics | `loadbench_reference.json` (LOADBench's simulation, reduced sky130 library) | copied |
| Testbenches | `diso_amp_AC/OP/NOISE`: this flow's convention, DC unity feedback through a 1 GH choke | **new** |
| Specs | `config.yaml`: **ASSUMPTION**, see `spec_notes` | **new** |
| Hierarchy / primitives | LOADBench `struct_recognition.xml` | converted |
| Symbolic equations | `upstream/equations.predicted.json`: textbook two-stage Miller model | **PREDICTED** |
| Operating point, variation ranges | not provided | S1 generates the OP; ranges pending |

Selection: --select: lowest area among 16 of 1024 rows meeting {'pm_deg': (55.0, 75.0), 'gain_db_min': 45.0, 'ft_hz_min': 10000000.0, 'p_w_max': 0.0015}.
LOADBench: Zenodo 10.5281/zenodo.21759759, licence CC BY 4.0 (attribution in THIRD_PARTY.md).
Devices not in any recognised structure: none.

SHA-256 of the generated upstream files:
- `upstream/primitives.json` 17988465b425f3a2bfd14222c590bc08a6a2af3c6cc804375b59b7dcebfa31b9
- `upstream/hierarchy.json` 27bf2eaa9b7eca3b5911b065bfce30686a69b359fe15a4b0f74f9c868eb88113
- `upstream/name_map.yaml` 0488fae444826e261943838a04fdb5c07b3afcf7d31cff2531a6f91fc09e8b34
- `upstream/equations.predicted.json` c2278f7982eaddc51fc96103e7f5d5beabce6cbdf02bdc99f315826021724d0e
