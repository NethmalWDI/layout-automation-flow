drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_W12_L0p5_m1__nf1_gtop_sdfull_ng/nfet_01v8_W12_L0p5_m1__nf1_gtop_sdfull_ng.gds
load nmos_differential_pair__ABBA -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_W12_L0p5_m1__nf1_gtop_sdfull_ng
box 1.930um 0.000um 1.930um 0.000um
getcell nfet_01v8_W12_L0p5_m1__nf1_gtop_sdfull_ng
box 3.860um 0.000um 3.860um 0.000um
getcell nfet_01v8_W12_L0p5_m1__nf1_gtop_sdfull_ng h
box 5.790um 0.000um 5.790um 0.000um
getcell nfet_01v8_W12_L0p5_m1__nf1_gtop_sdfull_ng h
box 0.360um 12.320um 0.720um 12.680um
paint metal1
box 0.410um 12.340um 0.670um 12.660um
paint m2c
box 0.440um 12.500um 0.640um 13.590um
paint metal2
box 0.340um 13.390um 0.740um 13.790um
paint m3c
box -0.035um 0.130um 0.325um 0.490um
paint metal1
box 0.015um 0.150um 0.275um 0.470um
paint m2c
box 0.045um -1.000um 0.245um 0.310um
paint metal2
box -0.055um -1.200um 0.345um -0.800um
paint m3c
box 0.755um 0.130um 1.115um 0.490um
paint metal1
box 0.805um 0.150um 1.065um 0.470um
paint m2c
box 0.835um -1.900um 1.035um 0.310um
paint metal2
box 0.735um -2.100um 1.135um -1.700um
paint m3c
box 2.290um 12.320um 2.650um 12.680um
paint metal1
box 2.340um 12.340um 2.600um 12.660um
paint m2c
box 2.370um 12.500um 2.570um 14.490um
paint metal2
box 2.270um 14.290um 2.670um 14.690um
paint m3c
box 1.895um 0.130um 2.255um 0.490um
paint metal1
box 1.945um 0.150um 2.205um 0.470um
paint m2c
box 1.975um -2.800um 2.175um 0.310um
paint metal2
box 1.875um -3.000um 2.275um -2.600um
paint m3c
box 2.685um 0.130um 3.045um 0.490um
paint metal1
box 2.735um 0.150um 2.995um 0.470um
paint m2c
box 2.765um -1.900um 2.965um 0.310um
paint metal2
box 2.665um -2.100um 3.065um -1.700um
paint m3c
box 4.470um 12.320um 4.830um 12.680um
paint metal1
box 4.520um 12.340um 4.780um 12.660um
paint m2c
box 4.550um 12.500um 4.750um 14.490um
paint metal2
box 4.450um 14.290um 4.850um 14.690um
paint m3c
box 4.865um 0.130um 5.225um 0.490um
paint metal1
box 4.915um 0.150um 5.175um 0.470um
paint m2c
box 4.945um -2.800um 5.145um 0.310um
paint metal2
box 4.845um -3.000um 5.245um -2.600um
paint m3c
box 4.075um 0.130um 4.435um 0.490um
paint metal1
box 4.125um 0.150um 4.385um 0.470um
paint m2c
box 4.155um -1.900um 4.355um 0.310um
paint metal2
box 4.055um -2.100um 4.455um -1.700um
paint m3c
box 6.400um 12.320um 6.760um 12.680um
paint metal1
box 6.450um 12.340um 6.710um 12.660um
paint m2c
box 6.480um 12.500um 6.680um 13.590um
paint metal2
box 6.380um 13.390um 6.780um 13.790um
paint m3c
box 6.795um 0.130um 7.155um 0.490um
paint metal1
box 6.845um 0.150um 7.105um 0.470um
paint m2c
box 6.875um -1.000um 7.075um 0.310um
paint metal2
box 6.775um -1.200um 7.175um -0.800um
paint m3c
box 6.005um 0.130um 6.365um 0.490um
paint metal1
box 6.055um 0.150um 6.315um 0.470um
paint m2c
box 6.085um -1.900um 6.285um 0.310um
paint metal2
box 5.985um -2.100um 6.385um -1.700um
paint m3c
box -1.800um 13.390um 8.920um 13.790um
paint metal3
box -1.700um 13.540um -1.600um 13.640um
label INP c metal3
box -1.800um 14.290um 8.920um 14.690um
paint metal3
box -1.700um 14.440um -1.600um 14.540um
label INN c metal3
box -1.800um -1.200um 8.920um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label net3 c metal3
box -1.800um -2.100um 8.920um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label net1 c metal3
box -1.800um -3.000um 8.920um -2.600um
paint metal3
box -1.700um -2.850um -1.600um -2.750um
label OUTP c metal3
box -0.800um -3.600um 7.920um 15.290um
sky130::guard_ring_draw psc psd
box 3.510um -3.650um 3.610um -3.550um
label VSS_body c locali
tech revert
save nmos_differential_pair__ABBA
gds write nmos_differential_pair__ABBA
quit -noprompt
