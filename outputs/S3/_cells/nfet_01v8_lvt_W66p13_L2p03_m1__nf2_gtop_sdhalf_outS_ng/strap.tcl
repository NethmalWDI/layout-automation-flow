drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdhalf_outS_ng.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdhalf_outS_ng
select top cell
box 0.015um 24.590um 0.275um 24.910um
paint m2c
box 4.655um 24.590um 4.915um 24.910um
paint m2c
box 0.010um 24.590um 4.920um 24.910um
paint metal2
label S c metal2
box 2.335um 8.420um 2.595um 8.740um
paint m2c
box 0.010um 8.420um 4.920um 8.740um
paint metal2
label D c metal2
box 0.145um 33.360um 4.785um 33.590um
paint metal1
label G c metal1
box 0.050um 16.615um 0.150um 16.715um
paint pwell
label B c pwell
save nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdhalf_outS_ng
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gtop_sdhalf_outS_ng
quit -noprompt
