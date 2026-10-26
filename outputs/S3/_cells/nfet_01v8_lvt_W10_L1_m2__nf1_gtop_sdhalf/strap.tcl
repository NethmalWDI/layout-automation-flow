drc off
gds read nfet_01v8_lvt_W10_L1_m2__nf1_gtop_sdhalf.gds
load nfet_01v8_lvt_W10_L1_m2__nf1_gtop_sdhalf
select top cell
box 0.455um 5.475um 0.685um 5.675um
paint metal1
label D c metal1
box 1.745um 5.475um 1.975um 5.675um
paint metal1
label S c metal1
box 0.735um 10.635um 1.695um 10.865um
paint metal1
label G c metal1
box 1.130um -0.085um 1.300um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W10_L1_m2__nf1_gtop_sdhalf
gds write nfet_01v8_lvt_W10_L1_m2__nf1_gtop_sdhalf
quit -noprompt
