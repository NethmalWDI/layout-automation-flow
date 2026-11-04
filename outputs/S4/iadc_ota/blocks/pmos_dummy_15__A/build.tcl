drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/pfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdhalf_ng/pfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdhalf_ng.gds
load pmos_dummy_15__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell pfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdhalf_ng
box 2.140um 0.000um 2.140um 0.000um
getcell pfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdhalf_ng
box 4.280um 0.000um 4.280um 0.000um
getcell pfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdhalf_ng
box 6.420um 0.000um 6.420um 0.000um
getcell pfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdhalf_ng
box 0.590um 1.945um 0.950um 2.305um
paint metal1
box 0.640um 1.965um 0.900um 2.285um
paint m2c
box 0.670um 2.125um 0.870um 3.215um
paint metal2
box 0.570um 3.015um 0.970um 3.415um
paint m3c
box 0.145um 0.630um 0.505um 0.990um
paint metal1
box 0.195um 0.650um 0.455um 0.970um
paint m2c
box 0.225um -1.000um 0.425um 0.810um
paint metal2
box 0.125um -1.200um 0.525um -0.800um
paint m3c
box 1.035um 0.630um 1.395um 0.990um
paint metal1
box 1.085um 0.650um 1.345um 0.970um
paint m2c
box 1.115um -1.900um 1.315um 0.810um
paint metal2
box 1.015um -2.100um 1.415um -1.700um
paint m3c
box 2.730um 1.945um 3.090um 2.305um
paint metal1
box 2.780um 1.965um 3.040um 2.285um
paint m2c
box 2.810um 2.125um 3.010um 3.215um
paint metal2
box 2.710um 3.015um 3.110um 3.415um
paint m3c
box 2.285um 0.630um 2.645um 0.990um
paint metal1
box 2.335um 0.650um 2.595um 0.970um
paint m2c
box 2.365um -1.000um 2.565um 0.810um
paint metal2
box 2.265um -1.200um 2.665um -0.800um
paint m3c
box 3.175um 0.630um 3.535um 0.990um
paint metal1
box 3.225um 0.650um 3.485um 0.970um
paint m2c
box 3.255um -1.900um 3.455um 0.810um
paint metal2
box 3.155um -2.100um 3.555um -1.700um
paint m3c
box 4.870um 1.945um 5.230um 2.305um
paint metal1
box 4.920um 1.965um 5.180um 2.285um
paint m2c
box 4.950um 2.125um 5.150um 3.215um
paint metal2
box 4.850um 3.015um 5.250um 3.415um
paint m3c
box 4.425um 0.630um 4.785um 0.990um
paint metal1
box 4.475um 0.650um 4.735um 0.970um
paint m2c
box 4.505um -1.000um 4.705um 0.810um
paint metal2
box 4.405um -1.200um 4.805um -0.800um
paint m3c
box 5.315um 0.630um 5.675um 0.990um
paint metal1
box 5.365um 0.650um 5.625um 0.970um
paint m2c
box 5.395um -1.900um 5.595um 0.810um
paint metal2
box 5.295um -2.100um 5.695um -1.700um
paint m3c
box 7.010um 1.945um 7.370um 2.305um
paint metal1
box 7.060um 1.965um 7.320um 2.285um
paint m2c
box 7.090um 2.125um 7.290um 3.215um
paint metal2
box 6.990um 3.015um 7.390um 3.415um
paint m3c
box 6.565um 0.630um 6.925um 0.990um
paint metal1
box 6.615um 0.650um 6.875um 0.970um
paint m2c
box 6.645um -1.000um 6.845um 0.810um
paint metal2
box 6.545um -1.200um 6.945um -0.800um
paint m3c
box 7.455um 0.630um 7.815um 0.990um
paint metal1
box 7.505um 0.650um 7.765um 0.970um
paint m2c
box 7.535um -1.900um 7.735um 0.810um
paint metal2
box 7.435um -2.100um 7.835um -1.700um
paint m3c
box 8.660um -1.900um 8.860um 3.215um
paint metal2
box 8.560um -2.100um 8.960um -1.700um
paint m3c
box 8.560um 3.015um 8.960um 3.415um
paint m3c
box -1.800um 3.015um 10.560um 3.415um
paint metal3
box -1.700um 3.165um -1.600um 3.265um
label VDD c metal3
box -1.800um -1.200um 10.560um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label on c metal3
box -1.800um -2.100um 10.560um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label VDD c metal3
box -1.300um -3.200um 10.060um 4.515um
paint nwell
box -0.800um -2.700um 9.560um 4.015um
sky130::guard_ring_draw nsc nsd
box 4.330um -2.750um 4.430um -2.650um
label VDD_body c locali
tech revert
save pmos_dummy_15__A
gds write pmos_dummy_15__A
quit -noprompt
