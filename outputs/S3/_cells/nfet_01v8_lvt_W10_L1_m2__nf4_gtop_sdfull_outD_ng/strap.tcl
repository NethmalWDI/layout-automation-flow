drc off
gds read nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdfull_outD_ng.gds
load nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdfull_outD_ng
select top cell
box 1.305um 2.260um 1.565um 2.580um
paint m2c
box 3.885um 2.260um 4.145um 2.580um
paint m2c
box 0.010um 2.260um 5.440um 2.580um
paint metal2
label S c metal2
box 0.015um 0.180um 0.275um 0.500um
paint m2c
box 2.595um 0.180um 2.855um 0.500um
paint m2c
box 5.175um 0.180um 5.435um 0.500um
paint m2c
box 0.010um 0.180um 5.440um 0.500um
paint metal2
label D c metal2
box 0.145um 2.790um 5.305um 3.020um
paint metal1
label G c metal1
box 0.050um 1.330um 0.150um 1.430um
paint pwell
label B c pwell
save nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdfull_outD_ng
gds write nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdfull_outD_ng
quit -noprompt
