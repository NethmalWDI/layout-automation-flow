drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/pfet_01v8_W8_L1_m1__nf1_gboth_sdfull_ng/pfet_01v8_W8_L1_m1__nf1_gboth_sdfull_ng.gds
load XM4__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell pfet_01v8_W8_L1_m1__nf1_gboth_sdfull_ng
box 0.790um 8.735um 1.150um 9.095um
paint metal1
box 0.840um 8.755um 1.100um 9.075um
paint m2c
box 0.870um 8.915um 1.070um 10.010um
paint metal2
box 0.770um 9.810um 1.170um 10.210um
paint m3c
box 0.145um 0.500um 0.505um 0.860um
paint metal1
box 0.195um 0.520um 0.455um 0.840um
paint m2c
box 0.225um -1.000um 0.425um 0.680um
paint metal2
box 0.125um -1.200um 0.525um -0.800um
paint m3c
box 1.435um 0.500um 1.795um 0.860um
paint metal1
box 1.485um 0.520um 1.745um 0.840um
paint m2c
box 1.515um -1.900um 1.715um 0.680um
paint metal2
box 1.415um -2.100um 1.815um -1.700um
paint m3c
box -1.800um 9.810um 3.740um 10.210um
paint metal3
box -1.700um 9.960um -1.600um 10.060um
label net3 c metal3
box -1.800um -1.200um 3.740um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label OUTP c metal3
box -1.800um -2.100um 3.740um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label VDD c metal3
box -1.300um -3.200um 3.240um 11.310um
paint nwell
box -0.800um -2.700um 2.740um 10.810um
sky130::guard_ring_draw nsc nsd
box 0.920um -2.750um 1.020um -2.650um
label VDD_body c locali
tech revert
save XM4__A
gds write XM4__A
quit -noprompt
