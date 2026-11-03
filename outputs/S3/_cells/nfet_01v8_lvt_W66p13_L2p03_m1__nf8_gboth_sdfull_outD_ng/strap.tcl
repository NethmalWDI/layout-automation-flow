drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdfull_outD_ng.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdfull_outD_ng
select top cell
box 2.335um 8.340um 2.595um 8.660um
paint m2c
box 6.975um 8.340um 7.235um 8.660um
paint m2c
box 11.615um 8.340um 11.875um 8.660um
paint m2c
box 16.255um 8.340um 16.515um 8.660um
paint m2c
box 0.010um 8.340um 18.840um 8.660um
paint metal2
label S c metal2
box 0.015um 0.490um 0.275um 0.810um
paint m2c
box 4.655um 0.490um 4.915um 0.810um
paint m2c
box 9.295um 0.490um 9.555um 0.810um
paint m2c
box 13.935um 0.490um 14.195um 0.810um
paint m2c
box 18.575um 0.490um 18.835um 0.810um
paint m2c
box 0.010um 0.490um 18.840um 0.810um
paint metal2
label D c metal2
box 0.145um 8.870um 18.705um 9.100um
paint metal1
label G c metal1
box 0.050um 4.525um 0.150um 4.625um
paint pwell
label B c pwell
save nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdfull_outD_ng
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gboth_sdfull_outD_ng
quit -noprompt
