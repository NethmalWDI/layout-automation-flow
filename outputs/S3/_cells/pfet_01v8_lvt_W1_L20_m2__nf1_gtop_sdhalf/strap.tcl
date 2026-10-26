drc off
gds read pfet_01v8_lvt_W1_L20_m2__nf1_gtop_sdhalf.gds
load pfet_01v8_lvt_W1_L20_m2__nf1_gtop_sdhalf
select top cell
box 0.455um 0.975um 0.685um 1.175um
paint metal1
label D c metal1
box 20.745um 0.975um 20.975um 1.175um
paint metal1
label S c metal1
box 0.735um 1.680um 20.695um 1.910um
paint metal1
label G c metal1
box 10.630um -0.085um 10.800um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W1_L20_m2__nf1_gtop_sdhalf
gds write pfet_01v8_lvt_W1_L20_m2__nf1_gtop_sdhalf
quit -noprompt
