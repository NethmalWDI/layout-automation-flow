drc off
gds read nfet_01v8_lvt_W1_L1_m9__nf1_gboth_sdhalf.gds
load nfet_01v8_lvt_W1_L1_m9__nf1_gboth_sdhalf
select top cell
box 0.455um 1.285um 0.685um 1.485um
paint metal1
label D c metal1
box 1.745um 1.285um 1.975um 1.485um
paint metal1
label S c metal1
box 0.735um 1.945um 1.695um 2.175um
paint metal1
label G c metal1
box 1.130um -0.085um 1.300um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W1_L1_m9__nf1_gboth_sdhalf
gds write nfet_01v8_lvt_W1_L1_m9__nf1_gboth_sdhalf
quit -noprompt
