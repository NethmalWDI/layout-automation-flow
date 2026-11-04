drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_W1p4_L0p6_m1__nf1_gboth_sdfull_ng/nfet_01v8_W1p4_L0p6_m1__nf1_gboth_sdfull_ng.gds
load nmos_matched_cascode_pair_11__AB -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_W1p4_L0p6_m1__nf1_gboth_sdfull_ng
box 2.030um 0.000um 2.030um 0.000um
getcell nfet_01v8_W1p4_L0p6_m1__nf1_gboth_sdfull_ng
box 4.060um 0.000um 4.060um 0.000um
getcell nfet_01v8_W1p4_L0p6_m1__nf1_gboth_sdfull_ng h
box 6.090um 0.000um 6.090um 0.000um
getcell nfet_01v8_W1p4_L0p6_m1__nf1_gboth_sdfull_ng h
box 0.535um 2.050um 0.895um 2.410um
paint metal1
box 0.585um 2.070um 0.845um 2.390um
paint m2c
box 0.615um 2.230um 0.815um 3.320um
paint metal2
box 0.515um 3.120um 0.915um 3.520um
paint m3c
box 0.090um 0.460um 0.450um 0.820um
paint metal1
box 0.140um 0.480um 0.400um 0.800um
paint m2c
box 0.170um -1.900um 0.370um 0.640um
paint metal2
box 0.070um -2.100um 0.470um -1.700um
paint m3c
box 0.980um 0.460um 1.340um 0.820um
paint metal1
box 1.030um 0.480um 1.290um 0.800um
paint m2c
box 1.060um -1.900um 1.260um 0.640um
paint metal2
box 0.960um -2.100um 1.360um -1.700um
paint m3c
box 2.565um 2.050um 2.925um 2.410um
paint metal1
box 2.615um 2.070um 2.875um 2.390um
paint m2c
box 2.645um 2.230um 2.845um 4.220um
paint metal2
box 2.545um 4.020um 2.945um 4.420um
paint m3c
box 2.120um 0.460um 2.480um 0.820um
paint metal1
box 2.170um 0.480um 2.430um 0.800um
paint m2c
box 2.200um -2.800um 2.400um 0.640um
paint metal2
box 2.100um -3.000um 2.500um -2.600um
paint m3c
box 3.010um 0.460um 3.370um 0.820um
paint metal1
box 3.060um 0.480um 3.320um 0.800um
paint m2c
box 3.090um -1.000um 3.290um 0.640um
paint metal2
box 2.990um -1.200um 3.390um -0.800um
paint m3c
box 4.595um 2.050um 4.955um 2.410um
paint metal1
box 4.645um 2.070um 4.905um 2.390um
paint m2c
box 4.675um 2.230um 4.875um 4.220um
paint metal2
box 4.575um 4.020um 4.975um 4.420um
paint m3c
box 5.040um 0.460um 5.400um 0.820um
paint metal1
box 5.090um 0.480um 5.350um 0.800um
paint m2c
box 5.120um -1.000um 5.320um 0.640um
paint metal2
box 5.020um -1.200um 5.420um -0.800um
paint m3c
box 4.150um 0.460um 4.510um 0.820um
paint metal1
box 4.200um 0.480um 4.460um 0.800um
paint m2c
box 4.230um -1.900um 4.430um 0.640um
paint metal2
box 4.130um -2.100um 4.530um -1.700um
paint m3c
box 6.625um 2.050um 6.985um 2.410um
paint metal1
box 6.675um 2.070um 6.935um 2.390um
paint m2c
box 6.705um 2.230um 6.905um 3.320um
paint metal2
box 6.605um 3.120um 7.005um 3.520um
paint m3c
box 7.070um 0.460um 7.430um 0.820um
paint metal1
box 7.120um 0.480um 7.380um 0.800um
paint m2c
box 7.150um -1.900um 7.350um 0.640um
paint metal2
box 7.050um -2.100um 7.450um -1.700um
paint m3c
box 6.180um 0.460um 6.540um 0.820um
paint metal1
box 6.230um 0.480um 6.490um 0.800um
paint m2c
box 6.260um -1.900um 6.460um 0.640um
paint metal2
box 6.160um -2.100um 6.560um -1.700um
paint m3c
box 8.220um -1.900um 8.420um 3.320um
paint metal2
box 8.120um -2.100um 8.520um -1.700um
paint m3c
box 8.120um 3.120um 8.520um 3.520um
paint m3c
box -1.800um 3.120um 10.120um 3.520um
paint metal3
box -1.700um 3.270um -1.600um 3.370um
label VSS c metal3
box -1.800um 4.020um 10.120um 4.420um
paint metal3
box -1.700um 4.170um -1.600um 4.270um
label cm c metal3
box -1.800um -2.100um 10.120um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label VSS c metal3
box -1.800um -3.000um 10.120um -2.600um
paint metal3
box -1.700um -2.850um -1.600um -2.750um
label x1_net14 c metal3
box 2.690um -1.200um 5.720um -0.800um
paint metal3
box 2.790um -1.050um 2.890um -0.950um
label x1_net15 c metal3
box -0.800um -3.600um 9.120um 5.020um
sky130::guard_ring_draw psc psd
box 4.110um -3.650um 4.210um -3.550um
label VSS_body c locali
tech revert
save nmos_matched_cascode_pair_11__AB
gds write nmos_matched_cascode_pair_11__AB
quit -noprompt
