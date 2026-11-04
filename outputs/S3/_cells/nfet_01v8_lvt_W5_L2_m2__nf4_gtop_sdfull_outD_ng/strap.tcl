drc off
gds read nfet_01v8_lvt_W5_L2_m2__nf4_gtop_sdfull_outD_ng.gds
load nfet_01v8_lvt_W5_L2_m2__nf4_gtop_sdfull_outD_ng
select top cell
box 2.305um 1.010um 2.565um 1.330um
paint m2c
box 6.885um 1.010um 7.145um 1.330um
paint m2c
box 0.010um 1.010um 9.440um 1.330um
paint metal2
label S c metal2
box 0.015um 0.180um 0.275um 0.500um
paint m2c
box 4.595um 0.180um 4.855um 0.500um
paint m2c
box 9.175um 0.180um 9.435um 0.500um
paint m2c
box 0.010um 0.180um 9.440um 0.500um
paint metal2
label D c metal2
box 0.145um 1.540um 9.305um 1.770um
paint metal1
label G c metal1
box 0.050um 0.705um 0.150um 0.805um
paint pwell
label B c pwell
save nfet_01v8_lvt_W5_L2_m2__nf4_gtop_sdfull_outD_ng
gds write nfet_01v8_lvt_W5_L2_m2__nf4_gtop_sdfull_outD_ng
quit -noprompt
