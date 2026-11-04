drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_W24_L1_m1__nf1_gboth_sdfull_ng/nfet_01v8_W24_L1_m1__nf1_gboth_sdfull_ng.gds
load XM5__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_W24_L1_m1__nf1_gboth_sdfull_ng
box 0.610um 24.630um 0.970um 24.990um
paint metal1
box 0.660um 24.650um 0.920um 24.970um
paint m2c
box 0.690um 24.810um 0.890um 25.920um
paint metal2
box 0.590um 25.720um 0.990um 26.120um
paint m3c
box -0.035um 0.440um 0.325um 0.800um
paint metal1
box 0.015um 0.460um 0.275um 0.780um
paint m2c
box 0.045um -1.000um 0.245um 0.620um
paint metal2
box -0.055um -1.200um 0.345um -0.800um
paint m3c
box 1.255um 0.440um 1.615um 0.800um
paint metal1
box 1.305um 0.460um 1.565um 0.780um
paint m2c
box 1.335um -1.900um 1.535um 0.620um
paint metal2
box 1.235um -2.100um 1.635um -1.700um
paint m3c
box -1.800um 25.720um 3.630um 26.120um
paint metal3
box -1.700um 25.870um -1.600um 25.970um
label net2 c metal3
box -1.800um -1.200um 3.630um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label net1 c metal3
box -1.800um -2.100um 3.630um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label VSS c metal3
box -0.800um -2.700um 2.630um 26.720um
sky130::guard_ring_draw psc psd
box 0.865um -2.750um 0.965um -2.650um
label VSS_body c locali
tech revert
save XM5__A
gds write XM5__A
quit -noprompt
