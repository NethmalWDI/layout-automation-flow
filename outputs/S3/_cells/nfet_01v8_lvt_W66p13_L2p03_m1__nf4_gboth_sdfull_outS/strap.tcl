drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gboth_sdfull_outS.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gboth_sdfull_outS
select top cell
box 0.440um 16.945um 0.700um 17.265um
paint m2c
box 5.080um 16.945um 5.340um 17.265um
paint m2c
box 9.720um 16.945um 9.980um 17.265um
paint m2c
box 0.435um 16.945um 9.985um 17.265um
paint metal2
label S c metal2
box 2.760um 0.835um 3.020um 1.155um
paint m2c
box 7.400um 0.835um 7.660um 1.155um
paint m2c
box 0.435um 0.835um 9.985um 1.155um
paint metal2
label D c metal2
box 0.570um 17.475um 9.850um 17.705um
paint metal1
label G c metal1
box 5.125um -0.085um 5.295um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gboth_sdfull_outS
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf4_gboth_sdfull_outS
quit -noprompt
