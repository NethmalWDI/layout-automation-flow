drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gtop_sdhalf_outD_ng.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gtop_sdhalf_outD_ng
select top cell
box 2.335um 5.990um 2.595um 6.310um
paint m2c
box 6.975um 5.990um 7.235um 6.310um
paint m2c
box 11.615um 5.990um 11.875um 6.310um
paint m2c
box 16.255um 5.990um 16.515um 6.310um
paint m2c
box 0.010um 5.990um 18.840um 6.310um
paint metal2
label S c metal2
box 0.015um 2.220um 0.275um 2.540um
paint m2c
box 4.655um 2.220um 4.915um 2.540um
paint m2c
box 9.295um 2.220um 9.555um 2.540um
paint m2c
box 13.935um 2.220um 14.195um 2.540um
paint m2c
box 18.575um 2.220um 18.835um 2.540um
paint m2c
box 0.010um 2.220um 18.840um 2.540um
paint metal2
label D c metal2
box 0.145um 8.560um 18.705um 8.790um
paint metal1
label G c metal1
box 0.050um 4.215um 0.150um 4.315um
paint pwell
label B c pwell
save nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gtop_sdhalf_outD_ng
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf8_gtop_sdhalf_outD_ng
quit -noprompt
