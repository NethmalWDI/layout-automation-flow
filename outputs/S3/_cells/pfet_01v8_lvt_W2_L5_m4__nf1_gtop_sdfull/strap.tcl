drc off
gds read pfet_01v8_lvt_W2_L5_m4__nf1_gtop_sdfull.gds
load pfet_01v8_lvt_W2_L5_m4__nf1_gtop_sdfull
select top cell
box 0.455um 1.475um 0.685um 1.675um
paint metal1
label D c metal1
box 5.745um 1.475um 5.975um 1.675um
paint metal1
label S c metal1
box 0.735um 2.680um 5.695um 2.910um
paint metal1
label G c metal1
box 3.130um -0.085um 3.300um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W2_L5_m4__nf1_gtop_sdfull
gds write pfet_01v8_lvt_W2_L5_m4__nf1_gtop_sdfull
quit -noprompt
