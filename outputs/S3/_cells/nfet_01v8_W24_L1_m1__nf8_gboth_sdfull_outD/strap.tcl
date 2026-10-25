drc off
gds read nfet_01v8_W24_L1_m1__nf8_gboth_sdfull_outD.gds
load nfet_01v8_W24_L1_m1__nf8_gboth_sdfull_outD
select top cell
box 1.730um 3.415um 1.990um 3.735um
paint m2c
box 4.310um 3.415um 4.570um 3.735um
paint m2c
box 6.890um 3.415um 7.150um 3.735um
paint m2c
box 9.470um 3.415um 9.730um 3.735um
paint m2c
box 0.435um 3.415um 11.025um 3.735um
paint metal2
label S c metal2
box 0.440um 0.835um 0.700um 1.155um
paint m2c
box 3.020um 0.835um 3.280um 1.155um
paint m2c
box 5.600um 0.835um 5.860um 1.155um
paint m2c
box 8.180um 0.835um 8.440um 1.155um
paint m2c
box 10.760um 0.835um 11.020um 1.155um
paint m2c
box 0.435um 0.835um 11.025um 1.155um
paint metal2
label D c metal2
box 0.570um 3.945um 10.890um 4.175um
paint metal1
label G c metal1
box 5.645um -0.085um 5.815um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L1_m1__nf8_gboth_sdfull_outD
gds write nfet_01v8_W24_L1_m1__nf8_gboth_sdfull_outD
quit -noprompt
