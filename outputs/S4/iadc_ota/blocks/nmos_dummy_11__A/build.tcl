drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_W1p4_L0p6_m2__nf1_gboth_sdfull_ng/nfet_01v8_W1p4_L0p6_m2__nf1_gboth_sdfull_ng.gds
load nmos_dummy_11__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_W1p4_L0p6_m2__nf1_gboth_sdfull_ng
box 2.030um 0.000um 2.030um 0.000um
getcell nfet_01v8_W1p4_L0p6_m2__nf1_gboth_sdfull_ng
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
box 0.170um -1.000um 0.370um 0.640um
paint metal2
box 0.070um -1.200um 0.470um -0.800um
paint m3c
box 0.980um 0.460um 1.340um 0.820um
paint metal1
box 1.030um 0.480um 1.290um 0.800um
paint m2c
box 1.060um -1.000um 1.260um 0.640um
paint metal2
box 0.960um -1.200um 1.360um -0.800um
paint m3c
box 2.565um 2.050um 2.925um 2.410um
paint metal1
box 2.615um 2.070um 2.875um 2.390um
paint m2c
box 2.645um 2.230um 2.845um 3.320um
paint metal2
box 2.545um 3.120um 2.945um 3.520um
paint m3c
box 2.120um 0.460um 2.480um 0.820um
paint metal1
box 2.170um 0.480um 2.430um 0.800um
paint m2c
box 2.200um -1.000um 2.400um 0.640um
paint metal2
box 2.100um -1.200um 2.500um -0.800um
paint m3c
box 3.010um 0.460um 3.370um 0.820um
paint metal1
box 3.060um 0.480um 3.320um 0.800um
paint m2c
box 3.090um -1.000um 3.290um 0.640um
paint metal2
box 2.990um -1.200um 3.390um -0.800um
paint m3c
box 4.160um -1.000um 4.360um 3.320um
paint metal2
box 4.060um -1.200um 4.460um -0.800um
paint m3c
box 4.060um 3.120um 4.460um 3.520um
paint m3c
box -1.800um 3.120um 6.060um 3.520um
paint metal3
box -1.700um 3.270um -1.600um 3.370um
label i_bias c metal3
box -1.800um -1.200um 6.060um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label i_bias c metal3
box -0.800um -1.800um 5.060um 4.120um
sky130::guard_ring_draw psc psd
box 2.080um -1.850um 2.180um -1.750um
label VSS_body c locali
tech revert
save nmos_dummy_11__A
gds write nmos_dummy_11__A
quit -noprompt
