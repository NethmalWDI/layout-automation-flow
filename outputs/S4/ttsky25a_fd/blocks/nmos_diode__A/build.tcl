drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W10_L1_m2__nf1_gtop_sdfull_ng/nfet_01v8_lvt_W10_L1_m2__nf1_gtop_sdfull_ng.gds
load nmos_diode__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_lvt_W10_L1_m2__nf1_gtop_sdfull_ng
box 2.430um 0.000um 2.430um 0.000um
getcell nfet_01v8_lvt_W10_L1_m2__nf1_gtop_sdfull_ng
box 0.610um 10.320um 0.970um 10.680um
paint metal1
box 0.660um 10.340um 0.920um 10.660um
paint m2c
box 0.690um 10.500um 0.890um 11.640um
paint metal2
box 0.590um 11.440um 0.990um 11.840um
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
box 3.040um 10.320um 3.400um 10.680um
paint metal1
box 3.090um 10.340um 3.350um 10.660um
paint m2c
box 3.120um 10.500um 3.320um 11.640um
paint metal2
box 3.020um 11.440um 3.420um 11.840um
paint m3c
box 2.395um 0.130um 2.755um 0.490um
paint metal1
box 2.445um 0.150um 2.705um 0.470um
paint m2c
box 2.475um -1.000um 2.675um 0.310um
paint metal2
box 2.375um -1.200um 2.775um -0.800um
paint m3c
box 3.685um 0.130um 4.045um 0.490um
paint metal1
box 3.735um 0.150um 3.995um 0.470um
paint m2c
box 3.765um -1.900um 3.965um 0.310um
paint metal2
box 3.665um -2.100um 4.065um -1.700um
paint m3c
box 4.960um -1.000um 5.160um 11.640um
paint metal2
box 4.860um -1.200um 5.260um -0.800um
paint m3c
box 4.860um 11.440um 5.260um 11.840um
paint m3c
box -1.800um 11.440um 6.860um 11.840um
paint metal3
box -1.700um 11.590um -1.600um 11.690um
label net1 c metal3
box -1.800um -1.200um 6.860um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label net1 c metal3
box -1.800um -2.100um 6.860um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label Rgm c metal3
box -0.800um -2.700um 5.860um 12.440um
sky130::guard_ring_draw psc psd
box 2.480um -2.750um 2.580um -2.650um
label Vss_body c locali
tech revert
save nmos_diode__A
gds write nmos_diode__A
quit -noprompt
