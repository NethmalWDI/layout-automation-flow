drc off
gds read nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS_ng.gds
load nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS_ng
select top cell
box 0.015um 5.760um 0.275um 6.080um
paint m2c
box 2.595um 5.760um 2.855um 6.080um
paint m2c
box 5.175um 5.760um 5.435um 6.080um
paint m2c
box 0.010um 5.760um 5.440um 6.080um
paint metal2
label S c metal2
box 1.305um 0.180um 1.565um 0.500um
paint m2c
box 3.885um 0.180um 4.145um 0.500um
paint m2c
box 0.010um 0.180um 5.440um 0.500um
paint metal2
label D c metal2
box 0.145um 6.290um 5.305um 6.520um
paint metal1
label G c metal1
box 0.050um 3.080um 0.150um 3.180um
paint pwell
label B c pwell
save nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS_ng
gds write nfet_01v8_W24_L1_m1__nf4_gtop_sdfull_outS_ng
quit -noprompt
