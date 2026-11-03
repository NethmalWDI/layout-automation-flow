drc off
gds read nfet_01v8_W24_L0p5_m1__nf8_gtop_sdfull_outS_ng.gds
load nfet_01v8_W24_L0p5_m1__nf8_gtop_sdfull_outS_ng
select top cell
box 0.015um 2.760um 0.275um 3.080um
paint m2c
box 1.595um 2.760um 1.855um 3.080um
paint m2c
box 3.175um 2.760um 3.435um 3.080um
paint m2c
box 4.755um 2.760um 5.015um 3.080um
paint m2c
box 6.335um 2.760um 6.595um 3.080um
paint m2c
box 0.010um 2.760um 6.600um 3.080um
paint metal2
label S c metal2
box 0.805um 0.180um 1.065um 0.500um
paint m2c
box 2.385um 0.180um 2.645um 0.500um
paint m2c
box 3.965um 0.180um 4.225um 0.500um
paint m2c
box 5.545um 0.180um 5.805um 0.500um
paint m2c
box 0.010um 0.180um 6.600um 0.500um
paint metal2
label D c metal2
box 0.145um 3.290um 6.465um 3.520um
paint metal1
label G c metal1
box 0.050um 1.580um 0.150um 1.680um
paint pwell
label B c pwell
save nfet_01v8_W24_L0p5_m1__nf8_gtop_sdfull_outS_ng
gds write nfet_01v8_W24_L0p5_m1__nf8_gtop_sdfull_outS_ng
quit -noprompt
