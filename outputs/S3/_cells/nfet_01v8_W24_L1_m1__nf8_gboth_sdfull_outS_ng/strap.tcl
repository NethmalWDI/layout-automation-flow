drc off
gds read nfet_01v8_W24_L1_m1__nf8_gboth_sdfull_outS_ng.gds
load nfet_01v8_W24_L1_m1__nf8_gboth_sdfull_outS_ng
select top cell
box 0.015um 3.070um 0.275um 3.390um
paint m2c
box 2.595um 3.070um 2.855um 3.390um
paint m2c
box 5.175um 3.070um 5.435um 3.390um
paint m2c
box 7.755um 3.070um 8.015um 3.390um
paint m2c
box 10.335um 3.070um 10.595um 3.390um
paint m2c
box 0.010um 3.070um 10.600um 3.390um
paint metal2
label S c metal2
box 1.305um 0.490um 1.565um 0.810um
paint m2c
box 3.885um 0.490um 4.145um 0.810um
paint m2c
box 6.465um 0.490um 6.725um 0.810um
paint m2c
box 9.045um 0.490um 9.305um 0.810um
paint m2c
box 0.010um 0.490um 10.600um 0.810um
paint metal2
label D c metal2
box 0.145um 3.600um 10.465um 3.830um
paint metal1
label G c metal1
box 0.050um 1.890um 0.150um 1.990um
paint pwell
label B c pwell
save nfet_01v8_W24_L1_m1__nf8_gboth_sdfull_outS_ng
gds write nfet_01v8_W24_L1_m1__nf8_gboth_sdfull_outS_ng
quit -noprompt
