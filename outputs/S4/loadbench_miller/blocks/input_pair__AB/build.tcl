drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdfull_outS_ng/pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdfull_outS_ng.gds
load input_pair__AB -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdfull_outS_ng
box 3.610um 0.000um 3.610um 0.000um
getcell pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdfull_outS_ng h
box 1.325um 7.845um 1.685um 8.205um
paint metal1
box 1.375um 7.865um 1.635um 8.185um
paint m2c
box 1.405um 8.025um 1.605um 10.020um
paint metal2
box 1.305um 9.820um 1.705um 10.220um
paint m3c
box 1.405um -1.000um 1.605um 0.650um
paint metal2
box 1.305um -1.200um 1.705um -0.800um
paint m3c
box 0.350um 7.460um 0.550um 9.120um
paint metal2
box 0.250um 8.920um 0.650um 9.320um
paint m3c
box 4.935um 7.845um 5.295um 8.205um
paint metal1
box 4.985um 7.865um 5.245um 8.185um
paint m2c
box 5.015um 8.025um 5.215um 10.920um
paint metal2
box 4.915um 10.720um 5.315um 11.120um
paint m3c
box 5.015um -1.900um 5.215um 0.650um
paint metal2
box 4.915um -2.100um 5.315um -1.700um
paint m3c
box 6.070um 7.460um 6.270um 9.120um
paint metal2
box 5.970um 8.920um 6.370um 9.320um
paint m3c
box -1.800um 8.920um 8.420um 9.320um
paint metal3
box -1.700um 9.070um -1.600um 9.170um
label FirstStageYsourceTransconductance c metal3
box -1.800um 9.820um 8.420um 10.220um
paint metal3
box -1.700um 9.970um -1.600um 10.070um
label in1 c metal3
box -1.800um 10.720um 8.420um 11.120um
paint metal3
box -1.700um 10.870um -1.600um 10.970um
label in2 c metal3
box -1.800um -1.200um 8.420um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label FirstStageYout1 c metal3
box -1.800um -2.100um 8.420um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label outFirstStage c metal3
box -1.300um -3.200um 7.920um 12.220um
paint nwell
box -0.800um -2.700um 7.420um 11.720um
sky130::guard_ring_draw nsc nsd
box 3.260um -2.750um 3.360um -2.650um
label FirstStageYsourceTransconductance_body c locali
tech revert
save input_pair__AB
gds write input_pair__AB
quit -noprompt
