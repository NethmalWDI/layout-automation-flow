drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/pfet_01v8_W1p4_L0p6_m2__nf1_gtop_sdfull_ng/pfet_01v8_W1p4_L0p6_m2__nf1_gtop_sdfull_ng.gds
load pmos_dummy_6__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell pfet_01v8_W1p4_L0p6_m2__nf1_gtop_sdfull_ng
box 2.140um 0.000um 2.140um 0.000um
getcell pfet_01v8_W1p4_L0p6_m2__nf1_gtop_sdfull_ng
box 0.590um 1.945um 0.950um 2.305um
paint metal1
box 0.640um 1.965um 0.900um 2.285um
paint m2c
box 0.670um 2.125um 0.870um 3.215um
paint metal2
box 0.570um 3.015um 0.970um 3.415um
paint m3c
box 0.145um 0.310um 0.505um 0.670um
paint metal1
box 0.195um 0.330um 0.455um 0.650um
paint m2c
box 0.225um -1.000um 0.425um 0.490um
paint metal2
box 0.125um -1.200um 0.525um -0.800um
paint m3c
box 1.035um 0.310um 1.395um 0.670um
paint metal1
box 1.085um 0.330um 1.345um 0.650um
paint m2c
box 1.115um -1.000um 1.315um 0.490um
paint metal2
box 1.015um -1.200um 1.415um -0.800um
paint m3c
box 2.730um 1.945um 3.090um 2.305um
paint metal1
box 2.780um 1.965um 3.040um 2.285um
paint m2c
box 2.810um 2.125um 3.010um 3.215um
paint metal2
box 2.710um 3.015um 3.110um 3.415um
paint m3c
box 2.285um 0.310um 2.645um 0.670um
paint metal1
box 2.335um 0.330um 2.595um 0.650um
paint m2c
box 2.365um -1.000um 2.565um 0.490um
paint metal2
box 2.265um -1.200um 2.665um -0.800um
paint m3c
box 3.175um 0.310um 3.535um 0.670um
paint metal1
box 3.225um 0.330um 3.485um 0.650um
paint m2c
box 3.255um -1.000um 3.455um 0.490um
paint metal2
box 3.155um -1.200um 3.555um -0.800um
paint m3c
box 4.380um -1.000um 4.580um 3.215um
paint metal2
box 4.280um -1.200um 4.680um -0.800um
paint m3c
box 4.280um 3.015um 4.680um 3.415um
paint m3c
box -1.800um 3.015um 6.280um 3.415um
paint metal3
box -1.700um 3.165um -1.600um 3.265um
label x1_m21d c metal3
box -1.800um -1.200um 6.280um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label x1_m21d c metal3
box -1.300um -2.300um 5.780um 4.515um
paint nwell
box -0.800um -1.800um 5.280um 4.015um
sky130::guard_ring_draw nsc nsd
box 2.190um -1.850um 2.290um -1.750um
label VDD_body c locali
tech revert
save pmos_dummy_6__A
gds write pmos_dummy_6__A
quit -noprompt
