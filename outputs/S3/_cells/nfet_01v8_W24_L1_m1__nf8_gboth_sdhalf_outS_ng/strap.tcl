drc off
gds read nfet_01v8_W24_L1_m1__nf8_gboth_sdhalf_outS_ng.gds
load nfet_01v8_W24_L1_m1__nf8_gboth_sdhalf_outS_ng
select top cell
box 0.015um 2.350um 0.275um 2.670um
paint m2c
box 2.595um 2.350um 2.855um 2.670um
paint m2c
box 5.175um 2.350um 5.435um 2.670um
paint m2c
box 7.755um 2.350um 8.015um 2.670um
paint m2c
box 10.335um 2.350um 10.595um 2.670um
paint m2c
box 0.010um 2.350um 10.600um 2.670um
paint metal2
label S c metal2
box 1.305um 1.210um 1.565um 1.530um
paint m2c
box 3.885um 1.210um 4.145um 1.530um
paint m2c
box 6.465um 1.210um 6.725um 1.530um
paint m2c
box 9.045um 1.210um 9.305um 1.530um
paint m2c
box 0.010um 1.210um 10.600um 1.530um
paint metal2
label D c metal2
box 0.145um 3.600um 10.465um 3.830um
paint metal1
label G c metal1
box 0.050um 1.890um 0.150um 1.990um
paint pwell
label B c pwell
save nfet_01v8_W24_L1_m1__nf8_gboth_sdhalf_outS_ng
gds write nfet_01v8_W24_L1_m1__nf8_gboth_sdhalf_outS_ng
quit -noprompt
