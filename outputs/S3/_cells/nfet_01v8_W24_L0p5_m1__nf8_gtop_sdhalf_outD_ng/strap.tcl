drc off
gds read nfet_01v8_W24_L0p5_m1__nf8_gtop_sdhalf_outD_ng.gds
load nfet_01v8_W24_L0p5_m1__nf8_gtop_sdhalf_outD_ng
select top cell
box 0.805um 2.040um 1.065um 2.360um
paint m2c
box 2.385um 2.040um 2.645um 2.360um
paint m2c
box 3.965um 2.040um 4.225um 2.360um
paint m2c
box 5.545um 2.040um 5.805um 2.360um
paint m2c
box 0.010um 2.040um 6.600um 2.360um
paint metal2
label S c metal2
box 0.015um 0.900um 0.275um 1.220um
paint m2c
box 1.595um 0.900um 1.855um 1.220um
paint m2c
box 3.175um 0.900um 3.435um 1.220um
paint m2c
box 4.755um 0.900um 5.015um 1.220um
paint m2c
box 6.335um 0.900um 6.595um 1.220um
paint m2c
box 0.010um 0.900um 6.600um 1.220um
paint metal2
label D c metal2
box 0.145um 3.290um 6.465um 3.520um
paint metal1
label G c metal1
box 0.050um 1.580um 0.150um 1.680um
paint pwell
label B c pwell
save nfet_01v8_W24_L0p5_m1__nf8_gtop_sdhalf_outD_ng
gds write nfet_01v8_W24_L0p5_m1__nf8_gtop_sdhalf_outD_ng
quit -noprompt
