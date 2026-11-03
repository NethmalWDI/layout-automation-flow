drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_W24_L0p5_m1__nf2_gtop_sdfull_outS_ng/nfet_01v8_W24_L0p5_m1__nf2_gtop_sdfull_outS_ng.gds
load nmos_differential_pair__AB -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_W24_L0p5_m1__nf2_gtop_sdfull_outS_ng
box 2.720um 0.000um 2.720um 0.000um
getcell nfet_01v8_W24_L0p5_m1__nf2_gtop_sdfull_outS_ng h
box 0.755um 12.320um 1.115um 12.680um
paint metal1
box 0.805um 12.340um 1.065um 12.660um
paint m2c
box 0.835um 12.500um 1.035um 14.490um
paint metal2
box 0.735um 14.290um 1.135um 14.690um
paint m3c
box 0.835um -1.000um 1.035um 0.280um
paint metal2
box 0.735um -1.200um 1.135um -0.800um
paint m3c
box 0.170um 11.980um 0.370um 13.590um
paint metal2
box 0.070um 13.390um 0.470um 13.790um
paint m3c
box 3.725um 12.320um 4.085um 12.680um
paint metal1
box 3.775um 12.340um 4.035um 12.660um
paint m2c
box 3.805um 12.500um 4.005um 15.390um
paint metal2
box 3.705um 15.190um 4.105um 15.590um
paint m3c
box 3.805um -1.900um 4.005um 0.280um
paint metal2
box 3.705um -2.100um 4.105um -1.700um
paint m3c
box 4.470um 11.980um 4.670um 13.590um
paint metal2
box 4.370um 13.390um 4.770um 13.790um
paint m3c
box -1.800um 13.390um 6.640um 13.790um
paint metal3
box -1.700um 13.540um -1.600um 13.640um
label net1 c metal3
box -1.800um 14.290um 6.640um 14.690um
paint metal3
box -1.700um 14.440um -1.600um 14.540um
label INP c metal3
box -1.800um 15.190um 6.640um 15.590um
paint metal3
box -1.700um 15.340um -1.600um 15.440um
label INN c metal3
box -1.800um -1.200um 6.640um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label net3 c metal3
box -1.800um -2.100um 6.640um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label OUTP c metal3
box -0.800um -2.700um 5.640um 16.190um
sky130::guard_ring_draw psc psd
box 2.370um -2.750um 2.470um -2.650um
label VSS_body c locali
tech revert
save nmos_differential_pair__AB
gds write nmos_differential_pair__AB
quit -noprompt
