drc off
gds read nfet_01v8_W24_L0p5_m1__nf4_gtop_sdfull_outD_ng.gds
load nfet_01v8_W24_L0p5_m1__nf4_gtop_sdfull_outD_ng
select top cell
box 0.805um 5.760um 1.065um 6.080um
paint m2c
box 2.385um 5.760um 2.645um 6.080um
paint m2c
box 0.010um 5.760um 3.440um 6.080um
paint metal2
label S c metal2
box 0.015um 0.180um 0.275um 0.500um
paint m2c
box 1.595um 0.180um 1.855um 0.500um
paint m2c
box 3.175um 0.180um 3.435um 0.500um
paint m2c
box 0.010um 0.180um 3.440um 0.500um
paint metal2
label D c metal2
box 0.145um 6.290um 3.305um 6.520um
paint metal1
label G c metal1
box 0.050um 3.080um 0.150um 3.180um
paint pwell
label B c pwell
save nfet_01v8_W24_L0p5_m1__nf4_gtop_sdfull_outD_ng
gds write nfet_01v8_W24_L0p5_m1__nf4_gtop_sdfull_outD_ng
quit -noprompt
