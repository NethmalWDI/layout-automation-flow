drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W0p6_L5_m2__nf1_gboth_sdfull_ng/nfet_01v8_lvt_W0p6_L5_m2__nf1_gboth_sdfull_ng.gds
load nmos_diode_2__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_lvt_W0p6_L5_m2__nf1_gboth_sdfull_ng
box 6.430um 0.000um 6.430um 0.000um
getcell nfet_01v8_lvt_W0p6_L5_m2__nf1_gboth_sdfull_ng
box 2.610um 1.230um 2.970um 1.590um
paint metal1
box 2.660um 1.250um 2.920um 1.570um
paint m2c
box 2.690um 1.410um 2.890um 2.520um
paint metal2
box 2.590um 2.320um 2.990um 2.720um
paint m3c
box -0.035um 0.440um 0.325um 0.800um
paint metal1
box 0.015um 0.460um 0.275um 0.780um
paint m2c
box 0.045um -1.000um 0.245um 0.620um
paint metal2
box -0.055um -1.200um 0.345um -0.800um
paint m3c
box 5.255um 0.440um 5.615um 0.800um
paint metal1
box 5.305um 0.460um 5.565um 0.780um
paint m2c
box 5.335um -1.900um 5.535um 0.620um
paint metal2
box 5.235um -2.100um 5.635um -1.700um
paint m3c
box 9.040um 1.230um 9.400um 1.590um
paint metal1
box 9.090um 1.250um 9.350um 1.570um
paint m2c
box 9.120um 1.410um 9.320um 2.520um
paint metal2
box 9.020um 2.320um 9.420um 2.720um
paint m3c
box 6.395um 0.440um 6.755um 0.800um
paint metal1
box 6.445um 0.460um 6.705um 0.780um
paint m2c
box 6.475um -1.000um 6.675um 0.620um
paint metal2
box 6.375um -1.200um 6.775um -0.800um
paint m3c
box 11.685um 0.440um 12.045um 0.800um
paint metal1
box 11.735um 0.460um 11.995um 0.780um
paint m2c
box 11.765um -1.900um 11.965um 0.620um
paint metal2
box 11.665um -2.100um 12.065um -1.700um
paint m3c
box 12.960um -1.000um 13.160um 2.520um
paint metal2
box 12.860um -1.200um 13.260um -0.800um
paint m3c
box 12.860um 2.320um 13.260um 2.720um
paint m3c
box -1.800um 2.320um 14.860um 2.720um
paint metal3
box -1.700um 2.470um -1.600um 2.570um
label net5 c metal3
box -1.800um -1.200um 14.860um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label net5 c metal3
box -1.800um -2.100um 14.860um -1.700um
paint metal3
box -1.700um -1.950um -1.600um -1.850um
label Vss c metal3
box -0.800um -2.700um 13.860um 3.320um
sky130::guard_ring_draw psc psd
box 6.480um -2.750um 6.580um -2.650um
label Vss_body c locali
tech revert
save nmos_diode_2__A
gds write nmos_diode_2__A
quit -noprompt
