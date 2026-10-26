# iadc_ota: provenance

Generated 2026-10-26 by `scripts/make_iadc_package.py` from `upstream_src/` (r09g/iadc, commit b8c2c4006a0091d6bbcb35d19028b0b4c1393bf4 Sat May 13 02:11:09 2023 -0700, MIT).

| Item | Origin | Status |
|---|---|---|
| Core and bias | `netlist/ota.spice`: folded_cascode_3_core, folded_cascode_3_bias, top-level dummies; flattened (85 devices) | copied, flattened |
| CMFB | switched-capacitor CMFB: its output capacitors C3/C4 kept; the switches and C1/C2/C5/C6 removed; an ideal CMFB with the SC steady-state law in the testbench wrapper | **ASSUMPTION** (AC model) |
| Bias current | 30 uA ideal source inside the DUT (`Ibias_ext`, bias_sources), from ota_tb_tran_ideal_clock | adapted |
| Load | 0.3 pF per output, from the same testbench | copied |
| Testbenches | `dido_amp_AC/OP/NOISE` (scripts/benchlib.py) | **new** |
| Specs | `config.yaml`: **ASSUMPTION**; upstream gives none | **new** |
| Primitives | rule-based recognition | **PREDICTED** |
| Symbolic equations | textbook folded-cascode model | **PREDICTED** |
| Layout reference | `upstream_src/layout/ota/` (hand-drawn Magic layout), `upstream_src/netlist/ota_layout_pex.spice` | copied |

SHA-256 of the generated files:
- `source/iadc_ota.spice` 963013b9ae2879c02942dddadd6db6ce6a1871616fdc733ca98d0b93377c97e2
- `source/config.yaml` 6157953331649721aa901d2166cfacee5166f6e019fa66473b0625ebea909bb5
- `testbenches/dido_amp_AC.spice` ff8e244b5460a67f3578ff76daf1f36f8d41ba76dc846f75f057e9edb0bf90d4
- `testbenches/dido_amp_NOISE.spice` c2f5434cd6f5bdacf2adf51665229ec5045f9a36e98fbc9c0fe3d0584bb6b45f
- `testbenches/dido_amp_OP.spice` fb2164cd1fe7749371997044d5605280d40e4c07771f5d1806334900f0268ebe
- `upstream/equations.predicted.json` b6d04c5fc0892008b87ead8b67ae4952a235de1e9f74a2fd0a15c7b175ab37ee
- `upstream/hierarchy.json` 4472c469c9d24a218832d14a69256270afe90582803aad3cfcafc11add54f608
- `upstream/name_map.yaml` cb8604994fbbab953ecfa6070133005fce9b3b4df812757fd1e4c45a0d4081e4
- `upstream/primitives.json` 84c106a25c3e29d28e5f416d62a7d61bc31fb4a282af29342c4fb7fd1e5cbb4f
