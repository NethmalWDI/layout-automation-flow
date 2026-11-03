drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdfull_outD_ng.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdfull_outD_ng
select top cell
box 2.335um 33.140um 2.595um 33.460um
paint m2c
box 0.010um 33.140um 4.920um 33.460um
paint metal2
label S c metal2
box 0.015um 0.490um 0.275um 0.810um
paint m2c
box 4.655um 0.490um 4.915um 0.810um
paint m2c
box 0.010um 0.490um 4.920um 0.810um
paint metal2
label D c metal2
box 0.145um 33.670um 4.785um 33.900um
paint metal1
label G c metal1
box 0.050um 16.925um 0.150um 17.025um
paint pwell
label B c pwell
save nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdfull_outD_ng
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdfull_outD_ng
quit -noprompt
