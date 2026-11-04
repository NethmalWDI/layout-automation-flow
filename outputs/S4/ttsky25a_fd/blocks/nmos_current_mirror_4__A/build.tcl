drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W1_L2_m2__nf1_gboth_sdfull_ng/nfet_01v8_lvt_W1_L2_m2__nf1_gboth_sdfull_ng.gds
load nmos_current_mirror_4__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_lvt_W1_L2_m2__nf1_gboth_sdfull_ng
box 3.430um 0.000um 3.430um 0.000um
getcell nfet_01v8_lvt_W1_L2_m2__nf1_gboth_sdfull_ng
box 1.110um 1.630um 1.470um 1.990um
paint metal1
box 1.160um 1.650um 1.420um 1.970um
paint m2c
box 1.190um 1.810um 1.390um 2.920um
paint metal2
box 1.090um 2.720um 1.490um 3.120um
paint m3c
box -0.035um 0.440um 0.325um 0.800um
paint metal1
box 0.015um 0.460um 0.275um 0.780um
paint m2c
box 0.045um -1.000um 0.245um 0.620um
paint metal2
box -0.055um -1.200um 0.345um -0.800um
paint m3c
box 2.255um 0.440um 2.615um 0.800um
paint metal1
box 2.305um 0.460um 2.565um 0.780um
paint m2c
box 2.335um -1.900um 2.535um 0.620um
paint metal2
box 2.235um -2.100um 2.635um -1.700um
paint m3c
box 4.540um 1.630um 4.900um 1.990um
paint metal1
box 4.590um 1.650um 4.850um 1.970um
paint m2c
box 4.620um 1.810um 4.820um 2.920um
paint metal2
box 4.520um 2.720um 4.920um 3.120um
paint m3c
box 3.395um 0.440um 3.755um 0.800um
paint metal1
box 3.445um 0.460um 3.705um 0.780um
paint m2c
box 3.475um -1.000um 3.675um 0.620um
paint metal2
box 3.375um -1.200um 3.775um -0.800um
paint m3c
box 5.685um 0.440um 6.045um 0.800um
paint metal1
box 5.735um 0.460um 5.995um 0.780um
paint m2c
box 5.765um -1.900um 5.965um 0.620um
paint metal2
box 5.665um -2.100um 6.065um -1.700um
paint m3c
box 6.960um -1.000um 7.160um 2.920um
paint metal2
box 6.860um -1.200um 7.260um -0.800um
paint m3c
box 6.860um 2.720um 7.260um 3.120um
paint m3c
box -1.800um 2.720um 8.860um 3.120um
paint metal3
box -1.700um 2.870um -1.600um 2.970um
label net4 c metal3
box -1.800um -1.200um 8.860um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label net4 c metal3
box -1.800um -2.100um 8.860um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label Vss c metal3
box -0.800um -2.700um 7.860um 3.720um
sky130::guard_ring_draw psc psd
box 3.480um -2.750um 3.580um -2.650um
label Vss_body c locali
tech revert
save nmos_current_mirror_4__A
gds write nmos_current_mirror_4__A
quit -noprompt
