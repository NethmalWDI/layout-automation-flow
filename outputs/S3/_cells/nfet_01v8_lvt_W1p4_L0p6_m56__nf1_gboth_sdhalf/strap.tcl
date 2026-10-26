drc off
gds read nfet_01v8_lvt_W1p4_L0p6_m56__nf1_gboth_sdhalf.gds
load nfet_01v8_lvt_W1p4_L0p6_m56__nf1_gboth_sdhalf
select top cell
box 0.455um 1.485um 0.685um 1.685um
paint metal1
label D c metal1
box 1.345um 1.485um 1.575um 1.685um
paint metal1
label S c metal1
box 0.735um 2.345um 1.295um 2.575um
paint metal1
label G c metal1
box 0.930um -0.085um 1.100um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W1p4_L0p6_m56__nf1_gboth_sdhalf
gds write nfet_01v8_lvt_W1p4_L0p6_m56__nf1_gboth_sdhalf
quit -noprompt
