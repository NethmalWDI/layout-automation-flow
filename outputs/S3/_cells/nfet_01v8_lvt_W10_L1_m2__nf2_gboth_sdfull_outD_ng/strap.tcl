drc off
gds read nfet_01v8_lvt_W10_L1_m2__nf2_gboth_sdfull_outD_ng.gds
load nfet_01v8_lvt_W10_L1_m2__nf2_gboth_sdfull_outD_ng
select top cell
box 1.305um 5.070um 1.565um 5.390um
paint m2c
box 0.010um 5.070um 2.860um 5.390um
paint metal2
label S c metal2
box 0.015um 0.490um 0.275um 0.810um
paint m2c
box 2.595um 0.490um 2.855um 0.810um
paint m2c
box 0.010um 0.490um 2.860um 0.810um
paint metal2
label D c metal2
box 0.145um 5.600um 2.725um 5.830um
paint metal1
label G c metal1
box 0.050um 2.890um 0.150um 2.990um
paint pwell
label B c pwell
save nfet_01v8_lvt_W10_L1_m2__nf2_gboth_sdfull_outD_ng
gds write nfet_01v8_lvt_W10_L1_m2__nf2_gboth_sdfull_outD_ng
quit -noprompt
