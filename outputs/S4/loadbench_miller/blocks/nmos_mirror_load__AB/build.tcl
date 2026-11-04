drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdfull_outS_ng/nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdfull_outS_ng.gds
load nmos_mirror_load__AB -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdfull_outS_ng
box 19.700um 0.000um 19.700um 0.000um
getcell nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdfull_outS_ng h
box 9.245um 8.900um 9.605um 9.260um
paint metal1
box 9.295um 8.920um 9.555um 9.240um
paint m2c
box 9.325um 9.080um 9.525um 11.090um
paint metal2
box 9.225um 10.890um 9.625um 11.290um
paint m3c
box 9.325um -1.000um 9.525um 0.590um
paint metal2
box 9.225um -1.200um 9.625um -0.800um
paint m3c
box 0.170um 8.560um 0.370um 10.190um
paint metal2
box 0.070um 9.990um 0.470um 10.390um
paint m3c
box 29.195um 8.900um 29.555um 9.260um
paint metal1
box 29.245um 8.920um 29.505um 9.240um
paint m2c
box 29.275um 9.080um 29.475um 11.090um
paint metal2
box 29.175um 10.890um 29.575um 11.290um
paint m3c
box 29.275um -1.900um 29.475um 0.590um
paint metal2
box 29.175um -2.100um 29.575um -1.700um
paint m3c
box 38.430um 8.560um 38.630um 10.190um
paint metal2
box 38.330um 9.990um 38.730um 10.390um
paint m3c
box 39.500um -1.000um 39.700um 11.090um
paint metal2
box 39.400um -1.200um 39.800um -0.800um
paint m3c
box 39.400um 10.890um 39.800um 11.290um
paint m3c
box -1.800um 9.990um 41.400um 10.390um
paint metal3
box -1.700um 10.140um -1.600um 10.240um
label sourceNmos c metal3
box -1.800um 10.890um 41.400um 11.290um
paint metal3
box -1.700um 11.040um -1.600um 11.140um
label FirstStageYout1 c metal3
box -1.800um -1.200um 41.400um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label FirstStageYout1 c metal3
box -1.800um -2.100um 41.400um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label outFirstStage c metal3
box -0.800um -2.700um 40.400um 11.890um
sky130::guard_ring_draw psc psd
box 19.750um -2.750um 19.850um -2.650um
label sourceNmos_body c locali
tech revert
save nmos_mirror_load__AB
gds write nmos_mirror_load__AB
quit -noprompt
