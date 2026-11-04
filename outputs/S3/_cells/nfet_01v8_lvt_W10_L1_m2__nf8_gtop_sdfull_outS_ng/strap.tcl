drc off
gds read nfet_01v8_lvt_W10_L1_m2__nf8_gtop_sdfull_outS_ng.gds
load nfet_01v8_lvt_W10_L1_m2__nf8_gtop_sdfull_outS_ng
select top cell
box 0.015um 1.010um 0.275um 1.330um
paint m2c
box 2.595um 1.010um 2.855um 1.330um
paint m2c
box 5.175um 1.010um 5.435um 1.330um
paint m2c
box 7.755um 1.010um 8.015um 1.330um
paint m2c
box 10.335um 1.010um 10.595um 1.330um
paint m2c
box 0.010um 1.010um 10.600um 1.330um
paint metal2
label S c metal2
box 1.305um 0.180um 1.565um 0.500um
paint m2c
box 3.885um 0.180um 4.145um 0.500um
paint m2c
box 6.465um 0.180um 6.725um 0.500um
paint m2c
box 9.045um 0.180um 9.305um 0.500um
paint m2c
box 0.010um 0.180um 10.600um 0.500um
paint metal2
label D c metal2
box 0.145um 1.540um 10.465um 1.770um
paint metal1
label G c metal1
box 0.050um 0.705um 0.150um 0.805um
paint pwell
label B c pwell
save nfet_01v8_lvt_W10_L1_m2__nf8_gtop_sdfull_outS_ng
gds write nfet_01v8_lvt_W10_L1_m2__nf8_gtop_sdfull_outS_ng
quit -noprompt
