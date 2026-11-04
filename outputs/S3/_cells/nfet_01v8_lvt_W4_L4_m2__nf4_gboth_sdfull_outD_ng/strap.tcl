drc off
gds read nfet_01v8_lvt_W4_L4_m2__nf4_gboth_sdfull_outD_ng.gds
load nfet_01v8_lvt_W4_L4_m2__nf4_gboth_sdfull_outD_ng
select top cell
box 4.305um 1.070um 4.565um 1.390um
paint m2c
box 12.885um 1.070um 13.145um 1.390um
paint m2c
box 0.010um 1.070um 17.440um 1.390um
paint metal2
label S c metal2
box 0.015um 0.490um 0.275um 0.810um
paint m2c
box 8.595um 0.490um 8.855um 0.810um
paint m2c
box 17.175um 0.490um 17.435um 0.810um
paint m2c
box 0.010um 0.490um 17.440um 0.810um
paint metal2
label D c metal2
box 0.145um 1.600um 17.305um 1.830um
paint metal1
label G c metal1
box 0.050um 0.890um 0.150um 0.990um
paint pwell
label B c pwell
save nfet_01v8_lvt_W4_L4_m2__nf4_gboth_sdfull_outD_ng
gds write nfet_01v8_lvt_W4_L4_m2__nf4_gboth_sdfull_outD_ng
quit -noprompt
