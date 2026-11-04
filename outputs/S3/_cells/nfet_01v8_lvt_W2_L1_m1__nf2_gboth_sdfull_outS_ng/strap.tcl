drc off
gds read nfet_01v8_lvt_W2_L1_m1__nf2_gboth_sdfull_outS_ng.gds
load nfet_01v8_lvt_W2_L1_m1__nf2_gboth_sdfull_outS_ng
select top cell
box 0.015um 1.070um 0.275um 1.390um
paint m2c
box 2.595um 1.070um 2.855um 1.390um
paint m2c
box 0.010um 1.070um 2.860um 1.390um
paint metal2
label S c metal2
box 1.305um 0.490um 1.565um 0.810um
paint m2c
box 0.010um 0.490um 2.860um 0.810um
paint metal2
label D c metal2
box 0.145um 1.600um 2.725um 1.830um
paint metal1
label G c metal1
box 0.050um 0.890um 0.150um 0.990um
paint pwell
label B c pwell
save nfet_01v8_lvt_W2_L1_m1__nf2_gboth_sdfull_outS_ng
gds write nfet_01v8_lvt_W2_L1_m1__nf2_gboth_sdfull_outS_ng
quit -noprompt
