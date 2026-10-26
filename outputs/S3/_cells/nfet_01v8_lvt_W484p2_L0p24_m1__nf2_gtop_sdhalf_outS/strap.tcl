drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gtop_sdhalf_outS.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gtop_sdhalf_outS
select top cell
box 0.440um 181.710um 0.700um 182.030um
paint m2c
box 1.500um 181.710um 1.760um 182.030um
paint m2c
box 0.435um 181.710um 1.765um 182.030um
paint metal2
label S c metal2
box 0.970um 61.020um 1.230um 61.340um
paint m2c
box 0.435um 61.020um 1.765um 61.340um
paint metal2
label D c metal2
box 0.570um 242.735um 1.630um 242.965um
paint metal1
label G c metal1
box 1.015um -0.085um 1.185um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gtop_sdhalf_outS
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gtop_sdhalf_outS
quit -noprompt
