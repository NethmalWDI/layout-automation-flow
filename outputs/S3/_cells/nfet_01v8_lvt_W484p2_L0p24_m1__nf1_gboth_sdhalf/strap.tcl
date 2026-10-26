drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf1_gboth_sdhalf.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf1_gboth_sdhalf
select top cell
box 0.455um 242.885um 0.685um 243.085um
paint metal1
label D c metal1
box 0.985um 242.885um 1.215um 243.085um
paint metal1
label S c metal1
box 0.690um 485.145um 0.980um 485.375um
paint metal1
label G c metal1
box 0.750um -0.085um 0.920um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W484p2_L0p24_m1__nf1_gboth_sdhalf
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf1_gboth_sdhalf
quit -noprompt
