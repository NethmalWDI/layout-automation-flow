drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gboth_sdhalf_outD.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gboth_sdhalf_outD
select top cell
box 0.970um 182.020um 1.230um 182.340um
paint m2c
box 0.435um 182.020um 1.765um 182.340um
paint metal2
label S c metal2
box 0.440um 61.330um 0.700um 61.650um
paint m2c
box 1.500um 61.330um 1.760um 61.650um
paint m2c
box 0.435um 61.330um 1.765um 61.650um
paint metal2
label D c metal2
box 0.570um 243.045um 1.630um 243.275um
paint metal1
label G c metal1
box 1.015um -0.085um 1.185um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gboth_sdhalf_outD
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gboth_sdhalf_outD
quit -noprompt
