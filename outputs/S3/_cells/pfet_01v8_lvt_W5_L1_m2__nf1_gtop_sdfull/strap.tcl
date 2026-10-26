drc off
gds read pfet_01v8_lvt_W5_L1_m2__nf1_gtop_sdfull.gds
load pfet_01v8_lvt_W5_L1_m2__nf1_gtop_sdfull
select top cell
box 0.455um 2.975um 0.685um 3.175um
paint metal1
label D c metal1
box 1.745um 2.975um 1.975um 3.175um
paint metal1
label S c metal1
box 0.735um 5.680um 1.695um 5.910um
paint metal1
label G c metal1
box 1.130um -0.085um 1.300um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W5_L1_m2__nf1_gtop_sdfull
gds write pfet_01v8_lvt_W5_L1_m2__nf1_gtop_sdfull
quit -noprompt
