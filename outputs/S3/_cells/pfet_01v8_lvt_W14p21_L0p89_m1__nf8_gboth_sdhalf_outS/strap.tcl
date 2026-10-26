drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdhalf_outS.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdhalf_outS
select top cell
box 0.440um 1.825um 0.700um 2.145um
paint m2c
box 2.800um 1.825um 3.060um 2.145um
paint m2c
box 5.160um 1.825um 5.420um 2.145um
paint m2c
box 7.520um 1.825um 7.780um 2.145um
paint m2c
box 9.880um 1.825um 10.140um 2.145um
paint m2c
box 0.435um 1.825um 10.145um 2.145um
paint metal2
label S c metal2
box 1.620um 1.295um 1.880um 1.615um
paint m2c
box 3.980um 1.295um 4.240um 1.615um
paint m2c
box 6.340um 1.295um 6.600um 1.615um
paint m2c
box 8.700um 1.295um 8.960um 1.615um
paint m2c
box 0.435um 1.295um 10.145um 1.615um
paint metal2
label D c metal2
box 0.570um 2.815um 10.010um 3.045um
paint metal1
label G c metal1
box 5.205um -0.085um 5.375um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdhalf_outS
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdhalf_outS
quit -noprompt
