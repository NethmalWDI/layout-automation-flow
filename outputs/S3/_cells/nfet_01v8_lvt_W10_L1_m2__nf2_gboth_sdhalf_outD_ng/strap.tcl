drc off
gds read nfet_01v8_lvt_W10_L1_m2__nf2_gboth_sdhalf_outD_ng.gds
load nfet_01v8_lvt_W10_L1_m2__nf2_gboth_sdhalf_outD_ng
select top cell
box 1.305um 3.850um 1.565um 4.170um
paint m2c
box 0.010um 3.850um 2.860um 4.170um
paint metal2
label S c metal2
box 0.015um 1.710um 0.275um 2.030um
paint m2c
box 2.595um 1.710um 2.855um 2.030um
paint m2c
box 0.010um 1.710um 2.860um 2.030um
paint metal2
label D c metal2
box 0.145um 5.600um 2.725um 5.830um
paint metal1
label G c metal1
box 0.050um 2.890um 0.150um 2.990um
paint pwell
label B c pwell
save nfet_01v8_lvt_W10_L1_m2__nf2_gboth_sdhalf_outD_ng
gds write nfet_01v8_lvt_W10_L1_m2__nf2_gboth_sdhalf_outD_ng
quit -noprompt
