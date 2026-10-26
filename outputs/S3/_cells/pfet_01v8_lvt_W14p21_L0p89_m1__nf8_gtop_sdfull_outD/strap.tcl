drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gtop_sdfull_outD.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gtop_sdfull_outD
select top cell
box 1.620um 1.885um 1.880um 2.205um
paint m2c
box 3.980um 1.885um 4.240um 2.205um
paint m2c
box 6.340um 1.885um 6.600um 2.205um
paint m2c
box 8.700um 1.885um 8.960um 2.205um
paint m2c
box 0.435um 1.885um 10.145um 2.205um
paint metal2
label S c metal2
box 0.440um 0.525um 0.700um 0.845um
paint m2c
box 2.800um 0.525um 3.060um 0.845um
paint m2c
box 5.160um 0.525um 5.420um 0.845um
paint m2c
box 7.520um 0.525um 7.780um 0.845um
paint m2c
box 9.880um 0.525um 10.140um 0.845um
paint m2c
box 0.435um 0.525um 10.145um 0.845um
paint metal2
label D c metal2
box 0.570um 2.460um 10.010um 2.690um
paint metal1
label G c metal1
box 5.205um -0.085um 5.375um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gtop_sdfull_outD
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gtop_sdfull_outD
quit -noprompt
