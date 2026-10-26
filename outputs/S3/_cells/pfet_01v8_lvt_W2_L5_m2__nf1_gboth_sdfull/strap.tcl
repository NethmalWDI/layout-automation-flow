drc off
gds read pfet_01v8_lvt_W2_L5_m2__nf1_gboth_sdfull.gds
load pfet_01v8_lvt_W2_L5_m2__nf1_gboth_sdfull
select top cell
box 0.455um 1.830um 0.685um 2.030um
paint metal1
label D c metal1
box 5.745um 1.830um 5.975um 2.030um
paint metal1
label S c metal1
box 0.735um 3.035um 5.695um 3.265um
paint metal1
label G c metal1
box 3.130um -0.085um 3.300um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W2_L5_m2__nf1_gboth_sdfull
gds write pfet_01v8_lvt_W2_L5_m2__nf1_gboth_sdfull
quit -noprompt
