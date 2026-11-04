drc off
gds read nfet_01v8_lvt_W5_L20_m2__nf4_gboth_sdfull_outS_ng.gds
load nfet_01v8_lvt_W5_L20_m2__nf4_gboth_sdfull_outS_ng
select top cell
box 0.015um 1.320um 0.275um 1.640um
paint m2c
box 40.595um 1.320um 40.855um 1.640um
paint m2c
box 81.175um 1.320um 81.435um 1.640um
paint m2c
box 0.010um 1.320um 81.440um 1.640um
paint metal2
label S c metal2
box 20.305um 0.490um 20.565um 0.810um
paint m2c
box 60.885um 0.490um 61.145um 0.810um
paint m2c
box 0.010um 0.490um 81.440um 0.810um
paint metal2
label D c metal2
box 0.145um 1.850um 81.305um 2.080um
paint metal1
label G c metal1
box 0.050um 1.015um 0.150um 1.115um
paint pwell
label B c pwell
save nfet_01v8_lvt_W5_L20_m2__nf4_gboth_sdfull_outS_ng
gds write nfet_01v8_lvt_W5_L20_m2__nf4_gboth_sdfull_outS_ng
quit -noprompt
