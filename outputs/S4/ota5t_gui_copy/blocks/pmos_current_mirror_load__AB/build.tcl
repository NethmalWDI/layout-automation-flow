drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/pfet_01v8_W8_L1_m1__nf1_gtop_sdfull_ng/pfet_01v8_W8_L1_m1__nf1_gtop_sdfull_ng.gds
load pmos_current_mirror_load__AB -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell pfet_01v8_W8_L1_m1__nf1_gtop_sdfull_ng
box 2.540um 0.000um 2.540um 0.000um
getcell pfet_01v8_W8_L1_m1__nf1_gtop_sdfull_ng
box 5.080um 0.000um 5.080um 0.000um
getcell pfet_01v8_W8_L1_m1__nf1_gtop_sdfull_ng h
box 7.620um 0.000um 7.620um 0.000um
getcell pfet_01v8_W8_L1_m1__nf1_gtop_sdfull_ng h
box 0.790um 8.545um 1.150um 8.905um
paint metal1
box 0.840um 8.565um 1.100um 8.885um
paint m2c
box 0.870um 8.725um 1.070um 9.815um
paint metal2
box 0.770um 9.615um 1.170um 10.015um
paint m3c
box 0.145um 0.310um 0.505um 0.670um
paint metal1
box 0.195um 0.330um 0.455um 0.650um
paint m2c
box 0.225um -1.000um 0.425um 0.490um
paint metal2
box 0.125um -1.200um 0.525um -0.800um
paint m3c
box 1.435um 0.310um 1.795um 0.670um
paint metal1
box 1.485um 0.330um 1.745um 0.650um
paint m2c
box 1.515um -1.000um 1.715um 0.490um
paint metal2
box 1.415um -1.200um 1.815um -0.800um
paint m3c
box 3.330um 8.545um 3.690um 8.905um
paint metal1
box 3.380um 8.565um 3.640um 8.885um
paint m2c
box 3.410um 8.725um 3.610um 10.715um
paint metal2
box 3.310um 10.515um 3.710um 10.915um
paint m3c
box 2.685um 0.310um 3.045um 0.670um
paint metal1
box 2.735um 0.330um 2.995um 0.650um
paint m2c
box 2.765um -1.900um 2.965um 0.490um
paint metal2
box 2.665um -2.100um 3.065um -1.700um
paint m3c
box 3.975um 0.310um 4.335um 0.670um
paint metal1
box 4.025um 0.330um 4.285um 0.650um
paint m2c
box 4.055um -1.000um 4.255um 0.490um
paint metal2
box 3.955um -1.200um 4.355um -0.800um
paint m3c
box 5.870um 8.545um 6.230um 8.905um
paint metal1
box 5.920um 8.565um 6.180um 8.885um
paint m2c
box 5.950um 8.725um 6.150um 10.715um
paint metal2
box 5.850um 10.515um 6.250um 10.915um
paint m3c
box 6.515um 0.310um 6.875um 0.670um
paint metal1
box 6.565um 0.330um 6.825um 0.650um
paint m2c
box 6.595um -2.800um 6.795um 0.490um
paint metal2
box 6.495um -3.000um 6.895um -2.600um
paint m3c
box 5.225um 0.310um 5.585um 0.670um
paint metal1
box 5.275um 0.330um 5.535um 0.650um
paint m2c
box 5.305um -1.000um 5.505um 0.490um
paint metal2
box 5.205um -1.200um 5.605um -0.800um
paint m3c
box 8.410um 8.545um 8.770um 8.905um
paint metal1
box 8.460um 8.565um 8.720um 8.885um
paint m2c
box 8.490um 8.725um 8.690um 9.815um
paint metal2
box 8.390um 9.615um 8.790um 10.015um
paint m3c
box 9.055um 0.310um 9.415um 0.670um
paint metal1
box 9.105um 0.330um 9.365um 0.650um
paint m2c
box 9.135um -1.000um 9.335um 0.490um
paint metal2
box 9.035um -1.200um 9.435um -0.800um
paint m3c
box 7.765um 0.310um 8.125um 0.670um
paint metal1
box 7.815um 0.330um 8.075um 0.650um
paint m2c
box 7.845um -1.000um 8.045um 0.490um
paint metal2
box 7.745um -1.200um 8.145um -0.800um
paint m3c
box 10.260um -1.000um 10.460um 9.815um
paint metal2
box 10.160um -1.200um 10.560um -0.800um
paint m3c
box 10.160um 9.615um 10.560um 10.015um
paint m3c
box 11.060um -1.900um 11.260um 10.715um
paint metal2
box 10.960um -2.100um 11.360um -1.700um
paint m3c
box 10.960um 10.515um 11.360um 10.915um
paint m3c
box -1.800um 9.615um 12.960um 10.015um
paint metal3
box -1.700um 9.765um -1.600um 9.865um
label VDD c metal3
box -1.800um 10.515um 12.960um 10.915um
paint metal3
box -1.700um 10.665um -1.600um 10.765um
label net3 c metal3
box -1.800um -1.200um 12.960um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label VDD c metal3
box -1.800um -2.100um 12.960um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label net3 c metal3
box -1.800um -3.000um 12.960um -2.600um
paint metal3
box -1.700um -2.850um -1.600um -2.750um
label OUTP c metal3
box -1.300um -4.100um 12.460um 12.015um
paint nwell
box -0.800um -3.600um 11.960um 11.515um
sky130::guard_ring_draw nsc nsd
box 5.530um -3.650um 5.630um -3.550um
label VDD_body c locali
tech revert
save pmos_current_mirror_load__AB
gds write pmos_current_mirror_load__AB
quit -noprompt
