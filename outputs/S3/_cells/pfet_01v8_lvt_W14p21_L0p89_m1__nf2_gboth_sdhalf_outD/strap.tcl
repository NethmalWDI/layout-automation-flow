drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdhalf_outD.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdhalf_outD
select top cell
box 1.620um 5.820um 1.880um 6.140um
paint m2c
box 0.435um 5.820um 3.065um 6.140um
paint metal2
label S c metal2
box 0.440um 2.630um 0.700um 2.950um
paint m2c
box 2.800um 2.630um 3.060um 2.950um
paint m2c
box 0.435um 2.630um 3.065um 2.950um
paint metal2
label D c metal2
box 0.570um 8.145um 2.930um 8.375um
paint metal1
label G c metal1
box 1.665um -0.085um 1.835um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdhalf_outD
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf2_gboth_sdhalf_outD
quit -noprompt
