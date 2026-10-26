drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdfull_outS.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdfull_outS
select top cell
box 0.440um 3.655um 0.700um 3.975um
paint m2c
box 2.800um 3.655um 3.060um 3.975um
paint m2c
box 5.160um 3.655um 5.420um 3.975um
paint m2c
box 0.435um 3.655um 5.425um 3.975um
paint metal2
label S c metal2
box 1.620um 0.525um 1.880um 0.845um
paint m2c
box 3.980um 0.525um 4.240um 0.845um
paint m2c
box 0.435um 0.525um 5.425um 0.845um
paint metal2
label D c metal2
box 0.570um 4.230um 5.290um 4.460um
paint metal1
label G c metal1
box 2.845um -0.085um 3.015um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdfull_outS
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gtop_sdfull_outS
quit -noprompt
