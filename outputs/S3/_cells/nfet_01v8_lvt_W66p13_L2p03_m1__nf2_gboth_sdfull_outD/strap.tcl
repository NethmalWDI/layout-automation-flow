drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdfull_outD.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdfull_outD
select top cell
box 2.760um 33.485um 3.020um 33.805um
paint m2c
box 0.435um 33.485um 5.345um 33.805um
paint metal2
label S c metal2
box 0.440um 0.835um 0.700um 1.155um
paint m2c
box 5.080um 0.835um 5.340um 1.155um
paint m2c
box 0.435um 0.835um 5.345um 1.155um
paint metal2
label D c metal2
box 0.570um 34.015um 5.210um 34.245um
paint metal1
label G c metal1
box 2.805um -0.085um 2.975um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdfull_outD
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf2_gboth_sdfull_outD
quit -noprompt
