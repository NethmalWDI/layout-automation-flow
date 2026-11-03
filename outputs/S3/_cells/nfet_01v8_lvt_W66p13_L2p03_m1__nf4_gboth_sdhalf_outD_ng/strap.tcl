drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gboth_sdhalf_outD_ng.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gboth_sdhalf_outD_ng
select top cell
box 2.335um 12.500um 2.595um 12.820um
paint m2c
box 6.975um 12.500um 7.235um 12.820um
paint m2c
box 0.010um 12.500um 9.560um 12.820um
paint metal2
label S c metal2
box 0.015um 4.590um 0.275um 4.910um
paint m2c
box 4.655um 4.590um 4.915um 4.910um
paint m2c
box 9.295um 4.590um 9.555um 4.910um
paint m2c
box 0.010um 4.590um 9.560um 4.910um
paint metal2
label D c metal2
box 0.145um 17.130um 9.425um 17.360um
paint metal1
label G c metal1
box 0.050um 8.655um 0.150um 8.755um
paint pwell
label B c pwell
save nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gboth_sdhalf_outD_ng
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gboth_sdhalf_outD_ng
quit -noprompt
