drc off
gds read nfet_01v8_lvt_W5_L20_m2__nf2_gboth_sdfull_outS_ng.gds
load nfet_01v8_lvt_W5_L20_m2__nf2_gboth_sdfull_outS_ng
select top cell
box 0.015um 2.570um 0.275um 2.890um
paint m2c
box 40.595um 2.570um 40.855um 2.890um
paint m2c
box 0.010um 2.570um 40.860um 2.890um
paint metal2
label S c metal2
box 20.305um 0.490um 20.565um 0.810um
paint m2c
box 0.010um 0.490um 40.860um 0.810um
paint metal2
label D c metal2
box 0.145um 3.100um 40.725um 3.330um
paint metal1
label G c metal1
box 0.050um 1.640um 0.150um 1.740um
paint pwell
label B c pwell
save nfet_01v8_lvt_W5_L20_m2__nf2_gboth_sdfull_outS_ng
gds write nfet_01v8_lvt_W5_L20_m2__nf2_gboth_sdfull_outS_ng
quit -noprompt
