drc off
gds read nfet_01v8_lvt_W5_L20_m2__nf4_gtop_sdfull_outS_ng.gds
load nfet_01v8_lvt_W5_L20_m2__nf4_gtop_sdfull_outS_ng
select top cell
box 0.015um 1.010um 0.275um 1.330um
paint m2c
box 40.595um 1.010um 40.855um 1.330um
paint m2c
box 81.175um 1.010um 81.435um 1.330um
paint m2c
box 0.010um 1.010um 81.440um 1.330um
paint metal2
label S c metal2
box 20.305um 0.180um 20.565um 0.500um
paint m2c
box 60.885um 0.180um 61.145um 0.500um
paint m2c
box 0.010um 0.180um 81.440um 0.500um
paint metal2
label D c metal2
box 0.145um 1.540um 81.305um 1.770um
paint metal1
label G c metal1
box 0.050um 0.705um 0.150um 0.805um
paint pwell
label B c pwell
save nfet_01v8_lvt_W5_L20_m2__nf4_gtop_sdfull_outS_ng
gds write nfet_01v8_lvt_W5_L20_m2__nf4_gtop_sdfull_outS_ng
quit -noprompt
