drc off
gds read nfet_01v8_lvt_W1_L1_m9__nf1_gtop_sdhalf.gds
load nfet_01v8_lvt_W1_L1_m9__nf1_gtop_sdhalf
select top cell
box 0.455um 0.975um 0.685um 1.175um
paint metal1
label D c metal1
box 1.745um 0.975um 1.975um 1.175um
paint metal1
label S c metal1
box 0.735um 1.635um 1.695um 1.865um
paint metal1
label G c metal1
box 1.130um -0.085um 1.300um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W1_L1_m9__nf1_gtop_sdhalf
gds write nfet_01v8_lvt_W1_L1_m9__nf1_gtop_sdhalf
quit -noprompt
