drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W2_L5_m2__nf2_gboth_sdfull_outS_ng/pfet_01v8_lvt_W2_L5_m2__nf2_gboth_sdfull_outS_ng.gds
load pmos_matched_cascode_pair__ABAB -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell pfet_01v8_lvt_W2_L5_m2__nf2_gboth_sdfull_outS_ng
box 11.830um 0.000um 11.830um 0.000um
getcell pfet_01v8_lvt_W2_L5_m2__nf2_gboth_sdfull_outS_ng
box 23.660um 0.000um 23.660um 0.000um
getcell pfet_01v8_lvt_W2_L5_m2__nf2_gboth_sdfull_outS_ng
box 35.490um 0.000um 35.490um 0.000um
getcell pfet_01v8_lvt_W2_L5_m2__nf2_gboth_sdfull_outS_ng
box 47.320um 0.000um 47.320um 0.000um
getcell pfet_01v8_lvt_W2_L5_m2__nf2_gboth_sdfull_outS_ng
box 59.150um 0.000um 59.150um 0.000um
getcell pfet_01v8_lvt_W2_L5_m2__nf2_gboth_sdfull_outS_ng
box 5.435um 1.735um 5.795um 2.095um
paint metal1
box 5.485um 1.755um 5.745um 2.075um
paint m2c
box 5.515um 1.915um 5.715um 3.010um
paint metal2
box 5.415um 2.810um 5.815um 3.210um
paint m3c
box 5.515um -1.000um 5.715um 0.650um
paint metal2
box 5.415um -1.200um 5.815um -0.800um
paint m3c
box 0.350um 1.350um 0.550um 3.010um
paint metal2
box 0.250um 2.810um 0.650um 3.210um
paint m3c
box 17.265um 1.735um 17.625um 2.095um
paint metal1
box 17.315um 1.755um 17.575um 2.075um
paint m2c
box 17.345um 1.915um 17.545um 4.810um
paint metal2
box 17.245um 4.610um 17.645um 5.010um
paint m3c
box 17.345um -1.900um 17.545um 0.650um
paint metal2
box 17.245um -2.100um 17.645um -1.700um
paint m3c
box 12.180um 1.350um 12.380um 3.910um
paint metal2
box 12.080um 3.710um 12.480um 4.110um
paint m3c
box 29.095um 1.735um 29.455um 2.095um
paint metal1
box 29.145um 1.755um 29.405um 2.075um
paint m2c
box 29.175um 1.915um 29.375um 4.810um
paint metal2
box 29.075um 4.610um 29.475um 5.010um
paint m3c
box 29.175um -2.800um 29.375um 0.650um
paint metal2
box 29.075um -3.000um 29.475um -2.600um
paint m3c
box 24.010um 1.350um 24.210um 5.710um
paint metal2
box 23.910um 5.510um 24.310um 5.910um
paint m3c
box 40.925um 1.735um 41.285um 2.095um
paint metal1
box 40.975um 1.755um 41.235um 2.075um
paint m2c
box 41.005um 1.915um 41.205um 4.810um
paint metal2
box 40.905um 4.610um 41.305um 5.010um
paint m3c
box 41.005um -1.900um 41.205um 0.650um
paint metal2
box 40.905um -2.100um 41.305um -1.700um
paint m3c
box 35.840um 1.350um 36.040um 3.910um
paint metal2
box 35.740um 3.710um 36.140um 4.110um
paint m3c
box 52.755um 1.735um 53.115um 2.095um
paint metal1
box 52.805um 1.755um 53.065um 2.075um
paint m2c
box 52.835um 1.915um 53.035um 4.810um
paint metal2
box 52.735um 4.610um 53.135um 5.010um
paint m3c
box 52.835um -2.800um 53.035um 0.650um
paint metal2
box 52.735um -3.000um 53.135um -2.600um
paint m3c
box 47.670um 1.350um 47.870um 5.710um
paint metal2
box 47.570um 5.510um 47.970um 5.910um
paint m3c
box 64.585um 1.735um 64.945um 2.095um
paint metal1
box 64.635um 1.755um 64.895um 2.075um
paint m2c
box 64.665um 1.915um 64.865um 3.010um
paint metal2
box 64.565um 2.810um 64.965um 3.210um
paint m3c
box 64.665um -1.000um 64.865um 0.650um
paint metal2
box 64.565um -1.200um 64.965um -0.800um
paint m3c
box 59.500um 1.350um 59.700um 3.010um
paint metal2
box 59.400um 2.810um 59.800um 3.210um
paint m3c
box 71.080um -1.000um 71.280um 3.010um
paint metal2
box 70.980um -1.200um 71.380um -0.800um
paint m3c
box 70.980um 2.810um 71.380um 3.210um
paint m3c
box -1.800um 2.810um 72.980um 3.210um
paint metal3
box -1.700um 2.960um -1.600um 3.060um
label Vdd c metal3
box -1.800um 3.710um 72.980um 4.110um
paint metal3
box -1.700um 3.860um -1.600um 3.960um
label x1_Vtest2 c metal3
box -1.800um 4.610um 72.980um 5.010um
paint metal3
box -1.700um 4.760um -1.600um 4.860um
label x1_Vbias c metal3
box -1.800um 5.510um 72.980um 5.910um
paint metal3
box -1.700um 5.660um -1.600um 5.760um
label x1_net1 c metal3
box -1.800um -1.200um 72.980um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label Vdd c metal3
box -1.800um -2.100um 72.980um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label Vop1 c metal3
box -1.800um -3.000um 72.980um -2.600um
paint metal3
box -1.700um -2.850um -1.600um -2.750um
label Vom1 c metal3
box -1.300um -4.100um 72.480um 7.010um
paint nwell
box -0.800um -3.600um 71.980um 6.510um
sky130::guard_ring_draw nsc nsd
box 35.540um -3.650um 35.640um -3.550um
label Vdd_body c locali
tech revert
save pmos_matched_cascode_pair__ABAB
gds write pmos_matched_cascode_pair__ABAB
quit -noprompt
