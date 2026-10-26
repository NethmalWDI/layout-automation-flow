drc off
gds read pfet_01v8_lvt_W1_L10_m2__nf1_gboth_sdfull.gds
load pfet_01v8_lvt_W1_L10_m2__nf1_gboth_sdfull
select top cell
box 0.455um 1.330um 0.685um 1.530um
paint metal1
label D c metal1
box 10.745um 1.330um 10.975um 1.530um
paint metal1
label S c metal1
box 0.735um 2.035um 10.695um 2.265um
paint metal1
label G c metal1
box 5.630um -0.085um 5.800um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W1_L10_m2__nf1_gboth_sdfull
gds write pfet_01v8_lvt_W1_L10_m2__nf1_gboth_sdfull
quit -noprompt
