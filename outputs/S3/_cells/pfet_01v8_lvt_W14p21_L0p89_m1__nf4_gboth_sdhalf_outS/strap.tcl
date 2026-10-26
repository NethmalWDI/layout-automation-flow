drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gboth_sdhalf_outS.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gboth_sdhalf_outS
select top cell
box 0.440um 3.155um 0.700um 3.475um
paint m2c
box 2.800um 3.155um 3.060um 3.475um
paint m2c
box 5.160um 3.155um 5.420um 3.475um
paint m2c
box 0.435um 3.155um 5.425um 3.475um
paint metal2
label S c metal2
box 1.620um 1.735um 1.880um 2.055um
paint m2c
box 3.980um 1.735um 4.240um 2.055um
paint m2c
box 0.435um 1.735um 5.425um 2.055um
paint metal2
label D c metal2
box 0.570um 4.585um 5.290um 4.815um
paint metal1
label G c metal1
box 2.845um -0.085um 3.015um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gboth_sdhalf_outS
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf4_gboth_sdhalf_outS
quit -noprompt
