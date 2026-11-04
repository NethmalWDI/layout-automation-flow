drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gtop_sdhalf_outS_ng/nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gtop_sdhalf_outS_ng.gds
load cs_stage__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gtop_sdhalf_outS_ng
box 8.445um 15.450um 8.805um 15.810um
paint metal1
box 8.495um 15.470um 8.755um 15.790um
paint m2c
box 8.525um 15.630um 8.725um 17.670um
paint metal2
box 8.425um 17.470um 8.825um 17.870um
paint m3c
box 8.525um -1.000um 8.725um 4.030um
paint metal2
box 8.425um -1.200um 8.825um -0.800um
paint m3c
box 0.170um 11.360um 0.370um 16.770um
paint metal2
box 0.070um 16.570um 0.470um 16.970um
paint m3c
box -1.800um 16.570um 19.300um 16.970um
paint metal3
box -1.700um 16.720um -1.600um 16.820um
label sourceNmos c metal3
box -1.800um 17.470um 19.300um 17.870um
paint metal3
box -1.700um 17.620um -1.600um 17.720um
label outFirstStage c metal3
box -1.800um -1.200um 19.300um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label out c metal3
box -0.800um -1.800um 18.300um 18.470um
sky130::guard_ring_draw psc psd
box 8.700um -1.850um 8.800um -1.750um
label sourceNmos_body c locali
tech revert
save cs_stage__A
gds write cs_stage__A
quit -noprompt
