drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W33p065_L2p03_m1__nf4_gboth_sdfull_outS_ng/nfet_01v8_lvt_W33p065_L2p03_m1__nf4_gboth_sdfull_outS_ng.gds
load nmos_mirror_load__ABAB -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_lvt_W33p065_L2p03_m1__nf4_gboth_sdfull_outS_ng
box 10.420um 0.000um 10.420um 0.000um
getcell nfet_01v8_lvt_W33p065_L2p03_m1__nf4_gboth_sdfull_outS_ng
box 20.840um 0.000um 20.840um 0.000um
getcell nfet_01v8_lvt_W33p065_L2p03_m1__nf4_gboth_sdfull_outS_ng
box 31.260um 0.000um 31.260um 0.000um
getcell nfet_01v8_lvt_W33p065_L2p03_m1__nf4_gboth_sdfull_outS_ng
box 4.605um 8.900um 4.965um 9.260um
paint metal1
box 4.655um 8.920um 4.915um 9.240um
paint m2c
box 4.685um 9.080um 4.885um 11.090um
paint metal2
box 4.585um 10.890um 4.985um 11.290um
paint m3c
box 4.685um -1.000um 4.885um 0.590um
paint metal2
box 4.585um -1.200um 4.985um -0.800um
paint m3c
box 0.170um 8.560um 0.370um 10.190um
paint metal2
box 0.070um 9.990um 0.470um 10.390um
paint m3c
box 15.025um 8.900um 15.385um 9.260um
paint metal1
box 15.075um 8.920um 15.335um 9.240um
paint m2c
box 15.105um 9.080um 15.305um 11.090um
paint metal2
box 15.005um 10.890um 15.405um 11.290um
paint m3c
box 15.105um -1.900um 15.305um 0.590um
paint metal2
box 15.005um -2.100um 15.405um -1.700um
paint m3c
box 10.590um 8.560um 10.790um 10.190um
paint metal2
box 10.490um 9.990um 10.890um 10.390um
paint m3c
box 25.445um 8.900um 25.805um 9.260um
paint metal1
box 25.495um 8.920um 25.755um 9.240um
paint m2c
box 25.525um 9.080um 25.725um 11.090um
paint metal2
box 25.425um 10.890um 25.825um 11.290um
paint m3c
box 25.525um -1.000um 25.725um 0.590um
paint metal2
box 25.425um -1.200um 25.825um -0.800um
paint m3c
box 21.010um 8.560um 21.210um 10.190um
paint metal2
box 20.910um 9.990um 21.310um 10.390um
paint m3c
box 35.865um 8.900um 36.225um 9.260um
paint metal1
box 35.915um 8.920um 36.175um 9.240um
paint m2c
box 35.945um 9.080um 36.145um 11.090um
paint metal2
box 35.845um 10.890um 36.245um 11.290um
paint m3c
box 35.945um -1.900um 36.145um 0.590um
paint metal2
box 35.845um -2.100um 36.245um -1.700um
paint m3c
box 31.430um 8.560um 31.630um 10.190um
paint metal2
box 31.330um 9.990um 31.730um 10.390um
paint m3c
box 41.780um -1.000um 41.980um 11.090um
paint metal2
box 41.680um -1.200um 42.080um -0.800um
paint m3c
box 41.680um 10.890um 42.080um 11.290um
paint m3c
box -1.800um 9.990um 43.680um 10.390um
paint metal3
box -1.700um 10.140um -1.600um 10.240um
label sourceNmos c metal3
box -1.800um 10.890um 43.680um 11.290um
paint metal3
box -1.700um 11.040um -1.600um 11.140um
label FirstStageYout1 c metal3
box -1.800um -1.200um 43.680um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label FirstStageYout1 c metal3
box -1.800um -2.100um 43.680um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label outFirstStage c metal3
box -0.800um -2.700um 42.680um 11.890um
sky130::guard_ring_draw psc psd
box 20.890um -2.750um 20.990um -2.650um
label sourceNmos_body c locali
tech revert
save nmos_mirror_load__ABAB
gds write nmos_mirror_load__ABAB
quit -noprompt
