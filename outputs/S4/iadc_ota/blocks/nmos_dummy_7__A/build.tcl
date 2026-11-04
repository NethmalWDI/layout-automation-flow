drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdfull_ng/nfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdfull_ng.gds
load nmos_dummy_7__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdfull_ng
box 2.030um 0.000um 2.030um 0.000um
getcell nfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdfull_ng
box 4.060um 0.000um 4.060um 0.000um
getcell nfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdfull_ng
box 6.090um 0.000um 6.090um 0.000um
getcell nfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdfull_ng
box 0.535um 1.720um 0.895um 2.080um
paint metal1
box 0.585um 1.740um 0.845um 2.060um
paint m2c
box 0.615um 1.900um 0.815um 2.990um
paint metal2
box 0.515um 2.790um 0.915um 3.190um
paint m3c
box 0.090um 0.130um 0.450um 0.490um
paint metal1
box 0.140um 0.150um 0.400um 0.470um
paint m2c
box 0.170um -1.000um 0.370um 0.310um
paint metal2
box 0.070um -1.200um 0.470um -0.800um
paint m3c
box 0.980um 0.130um 1.340um 0.490um
paint metal1
box 1.030um 0.150um 1.290um 0.470um
paint m2c
box 1.060um -1.000um 1.260um 0.310um
paint metal2
box 0.960um -1.200um 1.360um -0.800um
paint m3c
box 2.565um 1.720um 2.925um 2.080um
paint metal1
box 2.615um 1.740um 2.875um 2.060um
paint m2c
box 2.645um 1.900um 2.845um 2.990um
paint metal2
box 2.545um 2.790um 2.945um 3.190um
paint m3c
box 2.120um 0.130um 2.480um 0.490um
paint metal1
box 2.170um 0.150um 2.430um 0.470um
paint m2c
box 2.200um -1.000um 2.400um 0.310um
paint metal2
box 2.100um -1.200um 2.500um -0.800um
paint m3c
box 3.010um 0.130um 3.370um 0.490um
paint metal1
box 3.060um 0.150um 3.320um 0.470um
paint m2c
box 3.090um -1.000um 3.290um 0.310um
paint metal2
box 2.990um -1.200um 3.390um -0.800um
paint m3c
box 4.595um 1.720um 4.955um 2.080um
paint metal1
box 4.645um 1.740um 4.905um 2.060um
paint m2c
box 4.675um 1.900um 4.875um 2.990um
paint metal2
box 4.575um 2.790um 4.975um 3.190um
paint m3c
box 4.150um 0.130um 4.510um 0.490um
paint metal1
box 4.200um 0.150um 4.460um 0.470um
paint m2c
box 4.230um -1.000um 4.430um 0.310um
paint metal2
box 4.130um -1.200um 4.530um -0.800um
paint m3c
box 5.040um 0.130um 5.400um 0.490um
paint metal1
box 5.090um 0.150um 5.350um 0.470um
paint m2c
box 5.120um -1.000um 5.320um 0.310um
paint metal2
box 5.020um -1.200um 5.420um -0.800um
paint m3c
box 6.625um 1.720um 6.985um 2.080um
paint metal1
box 6.675um 1.740um 6.935um 2.060um
paint m2c
box 6.705um 1.900um 6.905um 2.990um
paint metal2
box 6.605um 2.790um 7.005um 3.190um
paint m3c
box 6.180um 0.130um 6.540um 0.490um
paint metal1
box 6.230um 0.150um 6.490um 0.470um
paint m2c
box 6.260um -1.000um 6.460um 0.310um
paint metal2
box 6.160um -1.200um 6.560um -0.800um
paint m3c
box 7.070um 0.130um 7.430um 0.490um
paint metal1
box 7.120um 0.150um 7.380um 0.470um
paint m2c
box 7.150um -1.000um 7.350um 0.310um
paint metal2
box 7.050um -1.200um 7.450um -0.800um
paint m3c
box 8.220um -1.000um 8.420um 2.990um
paint metal2
box 8.120um -1.200um 8.520um -0.800um
paint m3c
box 8.120um 2.790um 8.520um 3.190um
paint m3c
box -1.800um 2.790um 10.120um 3.190um
paint metal3
box -1.700um 2.940um -1.600um 3.040um
label bias_a c metal3
box -1.800um -1.200um 10.120um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label bias_a c metal3
box -0.800um -1.800um 9.120um 3.790um
sky130::guard_ring_draw psc psd
box 4.110um -1.850um 4.210um -1.750um
label VSS_body c locali
tech revert
save nmos_dummy_7__A
gds write nmos_dummy_7__A
quit -noprompt
