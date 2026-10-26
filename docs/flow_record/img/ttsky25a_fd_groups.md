| G | kind | devices (SPICE name -> schematic instance) | sheet |
|---|---|---|---|
| G1 | nmos-differential-pair | XX1_M5 -> M5, XX1_M6 -> M6 | Diff_opamp |
| G2 | nmos-differential-pair | XX1_M18 -> M18, XX1_M16 -> M16 | Diff_opamp |
| G3 | nmos-differential-pair | XX1_M10 -> M10, XX1_M17 -> M17 | Diff_opamp |
| G4 | pmos-differential-pair | XX2_M7 -> M7, XX2_M8 -> M8 | Common_source_stage |
| G5 | nmos-current-mirror | XM33 -> M33, XM37 -> M37, XM41 -> M41 | Opamp_with_bias |
| G6 | nmos-current-mirror ratioed by L, subset 1 (single device: nothing to match) | XX1_M46 -> M46 | Diff_opamp |
| G7 | nmos-current-mirror ratioed by L, subset 2 | XX1_M1 -> M1, XX1_M2 -> M2, XX1_M7 -> M7, XX1_M9 -> M9 | Diff_opamp |
| G8 | nmos-current-mirror ratioed by L, subset 3 | XX1_M22 -> M22, XX1_M15 -> M15 | Diff_opamp |
| G9 | nmos-current-mirror | XX1_M23 -> M23, XX1_M24 -> M24 | Diff_opamp |
| G10 | nmos-current-mirror | XX2_M10 -> M10, XX2_M11 -> M11 | Common_source_stage |
| G11 | nmos-current-mirror-load | XX2_M5 -> M5, XX2_M6 -> M6 | Common_source_stage |
| G12 | pmos-current-mirror | XM39 -> M39, XM38 -> M38 | Opamp_with_bias |
| G13 | pmos-current-mirror-load | XX1_M20 -> M20, XX1_M21 -> M21 | Diff_opamp |
| G14 | pmos-current-mirror ratioed by L, subset 1 (single device: nothing to match) | XX2_M12 -> M12 | Common_source_stage |
| G15 | pmos-current-mirror ratioed by L, subset 2 (single device: nothing to match) | XX2_M3 -> M3 | Common_source_stage |
| G16 | nmos-matched-cascode-pair | XX1_M19 -> M19, XX1_M4 -> M4 | Diff_opamp |
| G17 | nmos-matched-cascode-pair | XX1_M3 -> M3, XX1_M8 -> M8 | Diff_opamp |
| G18 | nmos-matched-current-source-pair | XX2_M2 -> M2, XX2_M1 -> M1 | Common_source_stage |
| G19 | pmos-matched-current-source-pair | XM32 -> M32, XM34 -> M34 | Opamp_with_bias |
| G20 | pmos-matched-current-source-pair | XM43 -> M43, XM44 -> M44 | Opamp_with_bias |
| G21 | pmos-matched-current-source-pair | XM45 -> M45, XM54 -> M54 | Opamp_with_bias |
| G22 | pmos-matched-cascode-pair | XX1_M11 -> M11, XX1_M12 -> M12 | Diff_opamp |
| G23 | pmos-matched-current-source-pair | XX1_M13 -> M13, XX1_M14 -> M14 | Diff_opamp |
