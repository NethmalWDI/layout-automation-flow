drc off
gds read nfet_01v8_W24_L0p5_m1__nf8_gboth_sdhalf_outD_ng.gds
load nfet_01v8_W24_L0p5_m1__nf8_gboth_sdhalf_outD_ng
select top cell
box 0.805um 2.350um 1.065um 2.670um
paint m2c
box 2.385um 2.350um 2.645um 2.670um
paint m2c
box 3.965um 2.350um 4.225um 2.670um
paint m2c
box 5.545um 2.350um 5.805um 2.670um
paint m2c
box 0.010um 2.350um 6.600um 2.670um
paint metal2
label S c metal2
box 0.015um 1.210um 0.275um 1.530um
paint m2c
box 1.595um 1.210um 1.855um 1.530um
paint m2c
box 3.175um 1.210um 3.435um 1.530um
paint m2c
box 4.755um 1.210um 5.015um 1.530um
paint m2c
box 6.335um 1.210um 6.595um 1.530um
paint m2c
box 0.010um 1.210um 6.600um 1.530um
paint metal2
label D c metal2
box 0.145um 3.600um 6.465um 3.830um
paint metal1
label G c metal1
box 0.050um 1.890um 0.150um 1.990um
paint pwell
label B c pwell
save nfet_01v8_W24_L0p5_m1__nf8_gboth_sdhalf_outD_ng
gds write nfet_01v8_W24_L0p5_m1__nf8_gboth_sdhalf_outD_ng
quit -noprompt
