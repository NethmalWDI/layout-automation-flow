drc off
gds read pfet_01v8_lvt_W1p5_L10_m2__nf1_gboth_sdhalf.gds
load pfet_01v8_lvt_W1p5_L10_m2__nf1_gboth_sdhalf
select top cell
box 0.455um 1.580um 0.685um 1.780um
paint metal1
label D c metal1
box 10.745um 1.580um 10.975um 1.780um
paint metal1
label S c metal1
box 0.735um 2.535um 10.695um 2.765um
paint metal1
label G c metal1
box 5.630um -0.085um 5.800um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W1p5_L10_m2__nf1_gboth_sdhalf
gds write pfet_01v8_lvt_W1p5_L10_m2__nf1_gboth_sdhalf
quit -noprompt
