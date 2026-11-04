drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_W24_L0p5_m1__nf2_gboth_sdfull_outS_ng/nfet_01v8_W24_L0p5_m1__nf2_gboth_sdfull_outS_ng.gds
load XM1__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_W24_L0p5_m1__nf2_gboth_sdfull_outS_ng
box 0.755um 12.630um 1.115um 12.990um
paint metal1
box 0.805um 12.650um 1.065um 12.970um
paint m2c
box 0.835um 12.810um 1.035um 14.820um
paint metal2
box 0.735um 14.620um 1.135um 15.020um
paint m3c
box 0.835um -1.000um 1.035um 0.590um
paint metal2
box 0.735um -1.200um 1.135um -0.800um
paint m3c
box 0.170um 12.290um 0.370um 13.920um
paint metal2
box 0.070um 13.720um 0.470um 14.120um
paint m3c
box -1.800um 13.720um 3.920um 14.120um
paint metal3
box -1.700um 13.870um -1.600um 13.970um
label net1 c metal3
box -1.800um 14.620um 3.920um 15.020um
paint metal3
box -1.700um 14.770um -1.600um 14.870um
label INP c metal3
box -1.800um -1.200um 3.920um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label net3 c metal3
box -0.800um -1.800um 2.920um 15.620um
sky130::guard_ring_draw psc psd
box 1.010um -1.850um 1.110um -1.750um
label VSS_body c locali
tech revert
save XM1__A
gds write XM1__A
quit -noprompt
