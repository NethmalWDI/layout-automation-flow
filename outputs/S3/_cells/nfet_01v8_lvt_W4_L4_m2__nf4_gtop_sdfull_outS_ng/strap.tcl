drc off
gds read nfet_01v8_lvt_W4_L4_m2__nf4_gtop_sdfull_outS_ng.gds
load nfet_01v8_lvt_W4_L4_m2__nf4_gtop_sdfull_outS_ng
select top cell
box 0.015um 0.760um 0.275um 1.080um
paint m2c
box 8.595um 0.760um 8.855um 1.080um
paint m2c
box 17.175um 0.760um 17.435um 1.080um
paint m2c
box 0.010um 0.760um 17.440um 1.080um
paint metal2
label S c metal2
box 4.305um 0.180um 4.565um 0.500um
paint m2c
box 12.885um 0.180um 13.145um 0.500um
paint m2c
box 0.010um 0.180um 17.440um 0.500um
paint metal2
label D c metal2
box 0.145um 1.290um 17.305um 1.520um
paint metal1
label G c metal1
box 0.050um 0.580um 0.150um 0.680um
paint pwell
label B c pwell
save nfet_01v8_lvt_W4_L4_m2__nf4_gtop_sdfull_outS_ng
gds write nfet_01v8_lvt_W4_L4_m2__nf4_gtop_sdfull_outS_ng
quit -noprompt
