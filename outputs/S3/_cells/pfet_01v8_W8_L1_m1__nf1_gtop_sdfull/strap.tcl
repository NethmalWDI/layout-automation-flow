drc off
gds read pfet_01v8_W8_L1_m1__nf1_gtop_sdfull.gds
load pfet_01v8_W8_L1_m1__nf1_gtop_sdfull
select top cell
box 0.455um 4.475um 0.685um 4.675um
paint metal1
label D c metal1
box 1.745um 4.475um 1.975um 4.675um
paint metal1
label S c metal1
box 0.735um 8.680um 1.695um 8.910um
paint metal1
label G c metal1
box 1.130um -0.085um 1.300um 0.085um
paint locali
label B c locali
save pfet_01v8_W8_L1_m1__nf1_gtop_sdfull
gds write pfet_01v8_W8_L1_m1__nf1_gtop_sdfull
quit -noprompt
