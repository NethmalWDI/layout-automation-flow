drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gtop_sdhalf_outD_ng.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gtop_sdhalf_outD_ng
select top cell
box 2.335um 12.190um 2.595um 12.510um
paint m2c
box 6.975um 12.190um 7.235um 12.510um
paint m2c
box 0.010um 12.190um 9.560um 12.510um
paint metal2
label S c metal2
box 0.015um 4.280um 0.275um 4.600um
paint m2c
box 4.655um 4.280um 4.915um 4.600um
paint m2c
box 9.295um 4.280um 9.555um 4.600um
paint m2c
box 0.010um 4.280um 9.560um 4.600um
paint metal2
label D c metal2
box 0.145um 16.820um 9.425um 17.050um
paint metal1
label G c metal1
box 0.050um 8.345um 0.150um 8.445um
paint pwell
label B c pwell
save nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gtop_sdhalf_outD_ng
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gtop_sdhalf_outD_ng
quit -noprompt
