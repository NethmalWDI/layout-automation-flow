drc off
gds read pfet_01v8_lvt_W1_L5_m2__nf1_gboth_sdfull.gds
load pfet_01v8_lvt_W1_L5_m2__nf1_gboth_sdfull
select top cell
box 0.455um 1.330um 0.685um 1.530um
paint metal1
label D c metal1
box 5.745um 1.330um 5.975um 1.530um
paint metal1
label S c metal1
box 0.735um 2.035um 5.695um 2.265um
paint metal1
label G c metal1
box 3.130um -0.085um 3.300um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W1_L5_m2__nf1_gboth_sdfull
gds write pfet_01v8_lvt_W1_L5_m2__nf1_gboth_sdfull
quit -noprompt
