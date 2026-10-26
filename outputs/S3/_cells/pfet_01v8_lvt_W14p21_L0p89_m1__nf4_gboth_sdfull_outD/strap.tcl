drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gboth_sdfull_outD.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gboth_sdfull_outD
select top cell
box 1.620um 4.010um 1.880um 4.330um
paint m2c
box 3.980um 4.010um 4.240um 4.330um
paint m2c
box 0.435um 4.010um 5.425um 4.330um
paint metal2
label S c metal2
box 0.440um 0.880um 0.700um 1.200um
paint m2c
box 2.800um 0.880um 3.060um 1.200um
paint m2c
box 5.160um 0.880um 5.420um 1.200um
paint m2c
box 0.435um 0.880um 5.425um 1.200um
paint metal2
label D c metal2
box 0.570um 4.585um 5.290um 4.815um
paint metal1
label G c metal1
box 2.845um -0.085um 3.015um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gboth_sdfull_outD
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gboth_sdfull_outD
quit -noprompt
