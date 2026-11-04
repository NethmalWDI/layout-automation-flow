drc off
gds read nfet_01v8_lvt_W4_L4_m2__nf2_gboth_sdfull_outD_ng.gds
load nfet_01v8_lvt_W4_L4_m2__nf2_gboth_sdfull_outD_ng
select top cell
box 4.305um 2.070um 4.565um 2.390um
paint m2c
box 0.010um 2.070um 8.860um 2.390um
paint metal2
label S c metal2
box 0.015um 0.490um 0.275um 0.810um
paint m2c
box 8.595um 0.490um 8.855um 0.810um
paint m2c
box 0.010um 0.490um 8.860um 0.810um
paint metal2
label D c metal2
box 0.145um 2.600um 8.725um 2.830um
paint metal1
label G c metal1
box 0.050um 1.390um 0.150um 1.490um
paint pwell
label B c pwell
save nfet_01v8_lvt_W4_L4_m2__nf2_gboth_sdfull_outD_ng
gds write nfet_01v8_lvt_W4_L4_m2__nf2_gboth_sdfull_outD_ng
quit -noprompt
