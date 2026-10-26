drc off
gds read nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gboth_sdhalf.gds
load nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gboth_sdhalf
select top cell
box 0.455um 1.385um 0.685um 1.585um
paint metal1
label D c metal1
box 0.945um 1.385um 1.175um 1.585um
paint metal1
label S c metal1
box 0.670um 2.145um 0.960um 2.375um
paint metal1
label G c metal1
box 0.730um -0.085um 0.900um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gboth_sdhalf
gds write nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gboth_sdhalf
quit -noprompt
