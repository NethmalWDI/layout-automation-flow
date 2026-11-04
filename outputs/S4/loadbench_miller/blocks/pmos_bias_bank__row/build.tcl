drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W37p3_L0p74_m1__nf1_gboth_sdhalf_ng/pfet_01v8_lvt_W37p3_L0p74_m1__nf1_gboth_sdhalf_ng.gds
gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdhalf_outS_ng/pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdhalf_outS_ng.gds
gds read /foss/designs/outputs/S3/_cells/pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdfull_outS_ng/pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdfull_outS_ng.gds
load pmos_bias_bank__row -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell pfet_01v8_lvt_W37p3_L0p74_m1__nf1_gboth_sdhalf_ng
box 2.280um 0.000um 2.280um 0.000um
getcell pfet_01v8_lvt_W90p63_L0p74_m1__nf8_gboth_sdfull_outS_ng
box 12.770um 0.000um 12.770um 0.000um
getcell pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gboth_sdhalf_outS_ng
box 0.660um 38.035um 1.020um 38.395um
paint metal1
box 0.710um 38.055um 0.970um 38.375um
paint m2c
box 0.740um 38.215um 0.940um 57.450um
paint metal2
box 0.640um 57.250um 1.040um 57.650um
paint m3c
box 0.145um 9.795um 0.505um 10.155um
paint metal1
box 0.195um 9.815um 0.455um 10.135um
paint m2c
box 0.225um -1.000um 0.425um 9.975um
paint metal2
box 0.125um -1.200um 0.525um -0.800um
paint m3c
box 1.175um 9.795um 1.535um 10.155um
paint metal1
box 1.225um 9.815um 1.485um 10.135um
paint m2c
box 1.255um -1.900um 1.455um 9.975um
paint metal2
box 1.155um -2.100um 1.555um -1.700um
paint m3c
box 6.545um 12.065um 6.905um 12.425um
paint metal1
box 6.595um 12.085um 6.855um 12.405um
paint m2c
box 6.625um 12.245um 6.825um 57.450um
paint metal2
box 6.525um 57.250um 6.925um 57.650um
paint m3c
box 6.625um -2.800um 6.825um 0.650um
paint metal2
box 6.525um -3.000um 6.925um -2.600um
paint m3c
box 2.630um 11.680um 2.830um 58.350um
paint metal2
box 2.530um 58.150um 2.930um 58.550um
paint m3c
box 21.155um 56.175um 21.515um 56.535um
paint metal1
box 21.205um 56.195um 21.465um 56.515um
paint m2c
box 21.235um 56.355um 21.435um 57.450um
paint metal2
box 21.135um 57.250um 21.535um 57.650um
paint m3c
box 21.235um -3.700um 21.435um 14.480um
paint metal2
box 21.135um -3.900um 21.535um -3.500um
paint m3c
box 13.120um 41.960um 13.320um 58.350um
paint metal2
box 13.020um 58.150um 13.420um 58.550um
paint m3c
box 30.600um -1.000um 30.800um 57.450um
paint metal2
box 30.500um -1.200um 30.900um -0.800um
paint m3c
box 30.500um 57.250um 30.900um 57.650um
paint m3c
box 31.400um -1.900um 31.600um 58.350um
paint metal2
box 31.300um -2.100um 31.700um -1.700um
paint m3c
box 31.300um 58.150um 31.700um 58.550um
paint m3c
box -1.800um 57.250um 33.300um 57.650um
paint metal3
box -1.700um 57.400um -1.600um 57.500um
label ibias c metal3
box -1.800um 58.150um 33.300um 58.550um
paint metal3
box -1.700um 58.300um -1.600um 58.400um
label sourcePmos c metal3
box -1.800um -1.200um 33.300um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label ibias c metal3
box -1.800um -2.100um 33.300um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label sourcePmos c metal3
box -1.800um -3.000um 33.300um -2.600um
paint metal3
box -1.700um -2.850um -1.600um -2.750um
label FirstStageYsourceTransconductance c metal3
box -1.800um -3.900um 33.300um -3.500um
paint metal3
box -1.700um -3.750um -1.600um -3.650um
label out c metal3
box -1.300um -5.000um 32.800um 59.650um
paint nwell
box -0.800um -4.500um 32.300um 59.150um
sky130::guard_ring_draw nsc nsd
box 11.885um -4.585um 12.055um 59.235um
paint li
box 11.885um -4.285um 12.055um 58.935um
paint nsc
box 11.885um -4.585um 12.055um 59.235um
paint nsd
box 15.700um -4.550um 15.800um -4.450um
label sourcePmos_body c locali
tech revert
save pmos_bias_bank__row
gds write pmos_bias_bank__row
quit -noprompt
