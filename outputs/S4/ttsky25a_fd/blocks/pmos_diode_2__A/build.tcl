drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1p5_L10_m2__nf1_gboth_sdfull_ng/pfet_01v8_lvt_W1p5_L10_m2__nf1_gboth_sdfull_ng.gds
load pmos_diode_2__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell pfet_01v8_lvt_W1p5_L10_m2__nf1_gboth_sdfull_ng
box 11.540um 0.000um 11.540um 0.000um
getcell pfet_01v8_lvt_W1p5_L10_m2__nf1_gboth_sdfull_ng
box 5.290um 2.235um 5.650um 2.595um
paint metal1
box 5.340um 2.255um 5.600um 2.575um
paint m2c
box 5.370um 2.415um 5.570um 3.510um
paint metal2
box 5.270um 3.310um 5.670um 3.710um
paint m3c
box 0.145um 0.500um 0.505um 0.860um
paint metal1
box 0.195um 0.520um 0.455um 0.840um
paint m2c
box 0.225um -1.000um 0.425um 0.680um
paint metal2
box 0.125um -1.200um 0.525um -0.800um
paint m3c
box 10.435um 0.500um 10.795um 0.860um
paint metal1
box 10.485um 0.520um 10.745um 0.840um
paint m2c
box 10.515um -1.900um 10.715um 0.680um
paint metal2
box 10.415um -2.100um 10.815um -1.700um
paint m3c
box 16.830um 2.235um 17.190um 2.595um
paint metal1
box 16.880um 2.255um 17.140um 2.575um
paint m2c
box 16.910um 2.415um 17.110um 3.510um
paint metal2
box 16.810um 3.310um 17.210um 3.710um
paint m3c
box 11.685um 0.500um 12.045um 0.860um
paint metal1
box 11.735um 0.520um 11.995um 0.840um
paint m2c
box 11.765um -1.000um 11.965um 0.680um
paint metal2
box 11.665um -1.200um 12.065um -0.800um
paint m3c
box 21.975um 0.500um 22.335um 0.860um
paint metal1
box 22.025um 0.520um 22.285um 0.840um
paint m2c
box 22.055um -1.900um 22.255um 0.680um
paint metal2
box 21.955um -2.100um 22.355um -1.700um
paint m3c
box 23.180um -1.000um 23.380um 3.510um
paint metal2
box 23.080um -1.200um 23.480um -0.800um
paint m3c
box 23.080um 3.310um 23.480um 3.710um
paint m3c
box -1.800um 3.310um 25.080um 3.710um
paint metal3
box -1.700um 3.460um -1.600um 3.560um
label x1_Vbias c metal3
box -1.800um -1.200um 25.080um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label x1_Vbias c metal3
box -1.800um -2.100um 25.080um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label Vdd c metal3
box -1.300um -3.200um 24.580um 4.810um
paint nwell
box -0.800um -2.700um 24.080um 4.310um
sky130::guard_ring_draw nsc nsd
box 11.590um -2.750um 11.690um -2.650um
label Vdd_body c locali
tech revert
save pmos_diode_2__A
gds write pmos_diode_2__A
quit -noprompt
