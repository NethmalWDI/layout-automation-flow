drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W7p105_L0p89_m1__nf1_gboth_sdfull_ng/pfet_01v8_lvt_W7p105_L0p89_m1__nf1_gboth_sdfull_ng.gds
load input_pair__ABAB -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell pfet_01v8_lvt_W7p105_L0p89_m1__nf1_gboth_sdfull_ng
box 2.430um 0.000um 2.430um 0.000um
getcell pfet_01v8_lvt_W7p105_L0p89_m1__nf1_gboth_sdfull_ng
box 4.860um 0.000um 4.860um 0.000um
getcell pfet_01v8_lvt_W7p105_L0p89_m1__nf1_gboth_sdfull_ng
box 7.290um 0.000um 7.290um 0.000um
getcell pfet_01v8_lvt_W7p105_L0p89_m1__nf1_gboth_sdfull_ng
box 0.735um 7.845um 1.095um 8.205um
paint metal1
box 0.785um 7.865um 1.045um 8.185um
paint m2c
box 0.815um 8.025um 1.015um 9.120um
paint metal2
box 0.715um 8.920um 1.115um 9.320um
paint m3c
box 0.145um 0.500um 0.505um 0.860um
paint metal1
box 0.195um 0.520um 0.455um 0.840um
paint m2c
box 0.225um -1.000um 0.425um 0.680um
paint metal2
box 0.125um -1.200um 0.525um -0.800um
paint m3c
box 1.325um 0.500um 1.685um 0.860um
paint metal1
box 1.375um 0.520um 1.635um 0.840um
paint m2c
box 1.405um -1.900um 1.605um 0.680um
paint metal2
box 1.305um -2.100um 1.705um -1.700um
paint m3c
box 3.165um 7.845um 3.525um 8.205um
paint metal1
box 3.215um 7.865um 3.475um 8.185um
paint m2c
box 3.245um 8.025um 3.445um 10.020um
paint metal2
box 3.145um 9.820um 3.545um 10.220um
paint m3c
box 2.575um 0.500um 2.935um 0.860um
paint metal1
box 2.625um 0.520um 2.885um 0.840um
paint m2c
box 2.655um -2.800um 2.855um 0.680um
paint metal2
box 2.555um -3.000um 2.955um -2.600um
paint m3c
box 3.755um 0.500um 4.115um 0.860um
paint metal1
box 3.805um 0.520um 4.065um 0.840um
paint m2c
box 3.835um -1.900um 4.035um 0.680um
paint metal2
box 3.735um -2.100um 4.135um -1.700um
paint m3c
box 5.595um 7.845um 5.955um 8.205um
paint metal1
box 5.645um 7.865um 5.905um 8.185um
paint m2c
box 5.675um 8.025um 5.875um 9.120um
paint metal2
box 5.575um 8.920um 5.975um 9.320um
paint m3c
box 5.005um 0.500um 5.365um 0.860um
paint metal1
box 5.055um 0.520um 5.315um 0.840um
paint m2c
box 5.085um -1.000um 5.285um 0.680um
paint metal2
box 4.985um -1.200um 5.385um -0.800um
paint m3c
box 6.185um 0.500um 6.545um 0.860um
paint metal1
box 6.235um 0.520um 6.495um 0.840um
paint m2c
box 6.265um -1.900um 6.465um 0.680um
paint metal2
box 6.165um -2.100um 6.565um -1.700um
paint m3c
box 8.025um 7.845um 8.385um 8.205um
paint metal1
box 8.075um 7.865um 8.335um 8.185um
paint m2c
box 8.105um 8.025um 8.305um 10.020um
paint metal2
box 8.005um 9.820um 8.405um 10.220um
paint m3c
box 7.435um 0.500um 7.795um 0.860um
paint metal1
box 7.485um 0.520um 7.745um 0.840um
paint m2c
box 7.515um -2.800um 7.715um 0.680um
paint metal2
box 7.415um -3.000um 7.815um -2.600um
paint m3c
box 8.615um 0.500um 8.975um 0.860um
paint metal1
box 8.665um 0.520um 8.925um 0.840um
paint m2c
box 8.695um -1.900um 8.895um 0.680um
paint metal2
box 8.595um -2.100um 8.995um -1.700um
paint m3c
box -1.800um 8.920um 10.920um 9.320um
paint metal3
box -1.700um 9.070um -1.600um 9.170um
label in1 c metal3
box -1.800um 9.820um 10.920um 10.220um
paint metal3
box -1.700um 9.970um -1.600um 10.070um
label in2 c metal3
box -1.800um -1.200um 10.920um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label FirstStageYout1 c metal3
box -1.800um -2.100um 10.920um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label FirstStageYsourceTransconductance c metal3
box -1.800um -3.000um 10.920um -2.600um
paint metal3
box -1.700um -2.850um -1.600um -2.750um
label outFirstStage c metal3
box -1.300um -4.100um 10.420um 11.320um
paint nwell
box -0.800um -3.600um 9.920um 10.820um
sky130::guard_ring_draw nsc nsd
box 4.510um -3.650um 4.610um -3.550um
label FirstStageYsourceTransconductance_body c locali
tech revert
save input_pair__ABAB
gds write input_pair__ABAB
quit -noprompt
