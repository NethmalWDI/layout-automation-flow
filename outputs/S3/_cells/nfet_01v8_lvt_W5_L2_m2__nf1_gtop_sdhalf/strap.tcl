drc off
gds read nfet_01v8_lvt_W5_L2_m2__nf1_gtop_sdhalf.gds
load nfet_01v8_lvt_W5_L2_m2__nf1_gtop_sdhalf
select top cell
box 0.455um 2.975um 0.685um 3.175um
paint metal1
label D c metal1
box 2.745um 2.975um 2.975um 3.175um
paint metal1
label S c metal1
box 0.735um 5.635um 2.695um 5.865um
paint metal1
label G c metal1
box 1.630um -0.085um 1.800um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W5_L2_m2__nf1_gtop_sdhalf
gds write nfet_01v8_lvt_W5_L2_m2__nf1_gtop_sdhalf
quit -noprompt
