drc off
gds read pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf.gds
load pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf
select top cell
box 0.455um 1.225um 0.685um 1.425um
paint metal1
label D c metal1
box 10.745um 1.225um 10.975um 1.425um
paint metal1
label S c metal1
box 0.735um 2.180um 10.695um 2.410um
paint metal1
label G c metal1
box 5.630um -0.085um 5.800um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf
gds write pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf
quit -noprompt
