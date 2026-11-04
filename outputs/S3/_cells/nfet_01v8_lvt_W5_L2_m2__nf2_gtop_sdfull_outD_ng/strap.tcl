drc off
gds read nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdfull_outD_ng.gds
load nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdfull_outD_ng
select top cell
box 2.305um 2.260um 2.565um 2.580um
paint m2c
box 0.010um 2.260um 4.860um 2.580um
paint metal2
label S c metal2
box 0.015um 0.180um 0.275um 0.500um
paint m2c
box 4.595um 0.180um 4.855um 0.500um
paint m2c
box 0.010um 0.180um 4.860um 0.500um
paint metal2
label D c metal2
box 0.145um 2.790um 4.725um 3.020um
paint metal1
label G c metal1
box 0.050um 1.330um 0.150um 1.430um
paint pwell
label B c pwell
save nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdfull_outD_ng
gds write nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdfull_outD_ng
quit -noprompt
