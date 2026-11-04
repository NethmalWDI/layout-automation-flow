drc off
gds read nfet_01v8_lvt_W33p065_L2p03_m1__nf4_gboth_sdfull_outS_ng.gds
load nfet_01v8_lvt_W33p065_L2p03_m1__nf4_gboth_sdfull_outS_ng
select top cell
box 0.015um 8.340um 0.275um 8.660um
paint m2c
box 4.655um 8.340um 4.915um 8.660um
paint m2c
box 9.295um 8.340um 9.555um 8.660um
paint m2c
box 0.010um 8.340um 9.560um 8.660um
paint metal2
label S c metal2
box 2.335um 0.490um 2.595um 0.810um
paint m2c
box 6.975um 0.490um 7.235um 0.810um
paint m2c
box 0.010um 0.490um 9.560um 0.810um
paint metal2
label D c metal2
box 0.145um 8.870um 9.425um 9.100um
paint metal1
label G c metal1
box 0.050um 4.525um 0.150um 4.625um
paint pwell
label B c pwell
save nfet_01v8_lvt_W33p065_L2p03_m1__nf4_gboth_sdfull_outS_ng
gds write nfet_01v8_lvt_W33p065_L2p03_m1__nf4_gboth_sdfull_outS_ng
quit -noprompt
