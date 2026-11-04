drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W2_L1_m1__nf1_gtop_sdfull_ng/nfet_01v8_lvt_W2_L1_m1__nf1_gtop_sdfull_ng.gds
load nmos_single_2__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_lvt_W2_L1_m1__nf1_gtop_sdfull_ng
box 0.610um 2.320um 0.970um 2.680um
paint metal1
box 0.660um 2.340um 0.920um 2.660um
paint m2c
box 0.690um 2.500um 0.890um 3.640um
paint metal2
box 0.590um 3.440um 0.990um 3.840um
paint m3c
box -0.035um 0.130um 0.325um 0.490um
paint metal1
box 0.015um 0.150um 0.275um 0.470um
paint m2c
box 0.045um -1.000um 0.245um 0.310um
paint metal2
box -0.055um -1.200um 0.345um -0.800um
paint m3c
box 1.255um 0.130um 1.615um 0.490um
paint metal1
box 1.305um 0.150um 1.565um 0.470um
paint m2c
box 1.335um -1.900um 1.535um 0.310um
paint metal2
box 1.235um -2.100um 1.635um -1.700um
paint m3c
box -1.800um 3.440um 3.630um 3.840um
paint metal3
box -1.700um 3.590um -1.600um 3.690um
label net3 c metal3
box -1.800um -1.200um 3.630um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label PBias c metal3
box -1.800um -2.100um 3.630um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label NBias c metal3
box -0.800um -2.700um 2.630um 4.440um
sky130::guard_ring_draw psc psd
box 0.865um -2.750um 0.965um -2.650um
label Vss_body c locali
tech revert
save nmos_single_2__A
gds write nmos_single_2__A
quit -noprompt
