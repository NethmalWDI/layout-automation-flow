drc off
gds read pfet_01v8_lvt_W5_L1_m2__nf1_gboth_sdfull.gds
load pfet_01v8_lvt_W5_L1_m2__nf1_gboth_sdfull
select top cell
box 0.455um 3.330um 0.685um 3.530um
paint metal1
label D c metal1
box 1.745um 3.330um 1.975um 3.530um
paint metal1
label S c metal1
box 0.735um 6.035um 1.695um 6.265um
paint metal1
label G c metal1
box 1.130um -0.085um 1.300um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W5_L1_m2__nf1_gboth_sdfull
gds write pfet_01v8_lvt_W5_L1_m2__nf1_gboth_sdfull
quit -noprompt
