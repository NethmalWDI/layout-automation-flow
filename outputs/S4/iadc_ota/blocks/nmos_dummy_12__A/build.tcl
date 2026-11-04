drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng/nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng.gds
load nmos_dummy_12__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng
box 1.630um 0.000um 1.630um 0.000um
getcell nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull_ng
box 0.335um 1.570um 0.695um 1.930um
paint metal1
box 0.385um 1.590um 0.645um 1.910um
paint m2c
box 0.415um 1.750um 0.615um 2.840um
paint metal2
box 0.315um 2.640um 0.715um 3.040um
paint m3c
box 0.090um 0.180um 0.450um 0.540um
paint metal1
box 0.140um 0.200um 0.400um 0.520um
paint m2c
box 0.170um -1.000um 0.370um 0.360um
paint metal2
box 0.070um -1.200um 0.470um -0.800um
paint m3c
box 0.580um 0.680um 0.940um 1.040um
paint metal1
box 0.630um 0.700um 0.890um 1.020um
paint m2c
box 0.660um -1.000um 0.860um 0.860um
paint metal2
box 0.560um -1.200um 0.960um -0.800um
paint m3c
box 1.965um 1.570um 2.325um 1.930um
paint metal1
box 2.015um 1.590um 2.275um 1.910um
paint m2c
box 2.045um 1.750um 2.245um 2.840um
paint metal2
box 1.945um 2.640um 2.345um 3.040um
paint m3c
box 1.720um 0.180um 2.080um 0.540um
paint metal1
box 1.770um 0.200um 2.030um 0.520um
paint m2c
box 1.800um -1.000um 2.000um 0.360um
paint metal2
box 1.700um -1.200um 2.100um -0.800um
paint m3c
box 2.210um 0.680um 2.570um 1.040um
paint metal1
box 2.260um 0.700um 2.520um 1.020um
paint m2c
box 2.290um -1.000um 2.490um 0.860um
paint metal2
box 2.190um -1.200um 2.590um -0.800um
paint m3c
box 0.270um -1.200um 0.760um -0.800um
paint metal2
box 1.900um -1.200um 2.390um -0.800um
paint metal2
box 3.360um -1.000um 3.560um 2.840um
paint metal2
box 3.260um -1.200um 3.660um -0.800um
paint m3c
box 3.260um 2.640um 3.660um 3.040um
paint m3c
box -1.800um 2.640um 5.260um 3.040um
paint metal3
box -1.700um 2.790um -1.600um 2.890um
label x2_foldp c metal3
box -1.800um -1.200um 5.260um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label x2_foldp c metal3
box -0.800um -1.800um 4.260um 3.640um
sky130::guard_ring_draw psc psd
box 1.680um -1.850um 1.780um -1.750um
label VSS_body c locali
tech revert
save nmos_dummy_12__A
gds write nmos_dummy_12__A
quit -noprompt
