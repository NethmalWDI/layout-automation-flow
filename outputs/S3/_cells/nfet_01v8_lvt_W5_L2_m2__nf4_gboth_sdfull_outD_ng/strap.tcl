drc off
gds read nfet_01v8_lvt_W5_L2_m2__nf4_gboth_sdfull_outD_ng.gds
load nfet_01v8_lvt_W5_L2_m2__nf4_gboth_sdfull_outD_ng
select top cell
box 2.305um 1.320um 2.565um 1.640um
paint m2c
box 6.885um 1.320um 7.145um 1.640um
paint m2c
box 0.010um 1.320um 9.440um 1.640um
paint metal2
label S c metal2
box 0.015um 0.490um 0.275um 0.810um
paint m2c
box 4.595um 0.490um 4.855um 0.810um
paint m2c
box 9.175um 0.490um 9.435um 0.810um
paint m2c
box 0.010um 0.490um 9.440um 0.810um
paint metal2
label D c metal2
box 0.145um 1.850um 9.305um 2.080um
paint metal1
label G c metal1
box 0.050um 1.015um 0.150um 1.115um
paint pwell
label B c pwell
save nfet_01v8_lvt_W5_L2_m2__nf4_gboth_sdfull_outD_ng
gds write nfet_01v8_lvt_W5_L2_m2__nf4_gboth_sdfull_outD_ng
quit -noprompt
