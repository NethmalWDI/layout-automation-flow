drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdhalf_outS_ng.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdhalf_outS_ng
select top cell
box 0.015um 24.900um 0.275um 25.220um
paint m2c
box 4.655um 24.900um 4.915um 25.220um
paint m2c
box 0.010um 24.900um 4.920um 25.220um
paint metal2
label S c metal2
box 2.335um 8.730um 2.595um 9.050um
paint m2c
box 0.010um 8.730um 4.920um 9.050um
paint metal2
label D c metal2
box 0.145um 33.670um 4.785um 33.900um
paint metal1
label G c metal1
box 0.050um 16.925um 0.150um 17.025um
paint pwell
label B c pwell
save nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdhalf_outS_ng
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdhalf_outS_ng
quit -noprompt
