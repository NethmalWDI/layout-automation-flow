drc off
gds read pfet_01v8_lvt_W1_L5_m2__nf1_gtop_sdhalf.gds
load pfet_01v8_lvt_W1_L5_m2__nf1_gtop_sdhalf
select top cell
box 0.455um 0.975um 0.685um 1.175um
paint metal1
label D c metal1
box 5.745um 0.975um 5.975um 1.175um
paint metal1
label S c metal1
box 0.735um 1.680um 5.695um 1.910um
paint metal1
label G c metal1
box 3.130um -0.085um 3.300um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W1_L5_m2__nf1_gtop_sdhalf
gds write pfet_01v8_lvt_W1_L5_m2__nf1_gtop_sdhalf
quit -noprompt
