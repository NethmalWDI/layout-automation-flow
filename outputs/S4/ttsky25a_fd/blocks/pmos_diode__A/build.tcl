drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W1_L20_m2__nf1_gtop_sdfull_ng/pfet_01v8_lvt_W1_L20_m2__nf1_gtop_sdfull_ng.gds
load pmos_diode__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell pfet_01v8_lvt_W1_L20_m2__nf1_gtop_sdfull_ng
box 21.540um 0.000um 21.540um 0.000um
getcell pfet_01v8_lvt_W1_L20_m2__nf1_gtop_sdfull_ng
box 10.290um 1.545um 10.650um 1.905um
paint metal1
box 10.340um 1.565um 10.600um 1.885um
paint m2c
box 10.370um 1.725um 10.570um 2.815um
paint metal2
box 10.270um 2.615um 10.670um 3.015um
paint m3c
box 0.145um 0.310um 0.505um 0.670um
paint metal1
box 0.195um 0.330um 0.455um 0.650um
paint m2c
box 0.225um -1.000um 0.425um 0.490um
paint metal2
box 0.125um -1.200um 0.525um -0.800um
paint m3c
box 20.435um 0.310um 20.795um 0.670um
paint metal1
box 20.485um 0.330um 20.745um 0.650um
paint m2c
box 20.515um -1.900um 20.715um 0.490um
paint metal2
box 20.415um -2.100um 20.815um -1.700um
paint m3c
box 31.830um 1.545um 32.190um 1.905um
paint metal1
box 31.880um 1.565um 32.140um 1.885um
paint m2c
box 31.910um 1.725um 32.110um 2.815um
paint metal2
box 31.810um 2.615um 32.210um 3.015um
paint m3c
box 21.685um 0.310um 22.045um 0.670um
paint metal1
box 21.735um 0.330um 21.995um 0.650um
paint m2c
box 21.765um -1.000um 21.965um 0.490um
paint metal2
box 21.665um -1.200um 22.065um -0.800um
paint m3c
box 41.975um 0.310um 42.335um 0.670um
paint metal1
box 42.025um 0.330um 42.285um 0.650um
paint m2c
box 42.055um -1.900um 42.255um 0.490um
paint metal2
box 41.955um -2.100um 42.355um -1.700um
paint m3c
box 43.180um -1.000um 43.380um 2.815um
paint metal2
box 43.080um -1.200um 43.480um -0.800um
paint m3c
box 43.080um 2.615um 43.480um 3.015um
paint m3c
box -1.800um 2.615um 45.080um 3.015um
paint metal3
box -1.700um 2.765um -1.600um 2.865um
label net3 c metal3
box -1.800um -1.200um 45.080um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label net3 c metal3
box -1.800um -2.100um 45.080um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label Vdd c metal3
box -1.300um -3.200um 44.580um 4.115um
paint nwell
box -0.800um -2.700um 44.080um 3.615um
sky130::guard_ring_draw nsc nsd
box 21.590um -2.750um 21.690um -2.650um
label Vdd_body c locali
tech revert
save pmos_diode__A
gds write pmos_diode__A
quit -noprompt
