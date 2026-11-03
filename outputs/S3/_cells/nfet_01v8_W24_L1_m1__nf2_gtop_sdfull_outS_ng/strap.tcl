drc off
gds read nfet_01v8_W24_L1_m1__nf2_gtop_sdfull_outS_ng.gds
load nfet_01v8_W24_L1_m1__nf2_gtop_sdfull_outS_ng
select top cell
box 0.015um 11.760um 0.275um 12.080um
paint m2c
box 2.595um 11.760um 2.855um 12.080um
paint m2c
box 0.010um 11.760um 2.860um 12.080um
paint metal2
label S c metal2
box 1.305um 0.180um 1.565um 0.500um
paint m2c
box 0.010um 0.180um 2.860um 0.500um
paint metal2
label D c metal2
box 0.145um 12.290um 2.725um 12.520um
paint metal1
label G c metal1
box 0.050um 6.080um 0.150um 6.180um
paint pwell
label B c pwell
save nfet_01v8_W24_L1_m1__nf2_gtop_sdfull_outS_ng
gds write nfet_01v8_W24_L1_m1__nf2_gtop_sdfull_outS_ng
quit -noprompt
