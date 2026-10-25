drc off
gds read nfet_01v8_W24_L1_m1__nf4_gboth_sdfull_outD.gds
load nfet_01v8_W24_L1_m1__nf4_gboth_sdfull_outD
select top cell
box 1.730um 6.415um 1.990um 6.735um
paint m2c
box 4.310um 6.415um 4.570um 6.735um
paint m2c
box 0.435um 6.415um 5.865um 6.735um
paint metal2
label S c metal2
box 0.440um 0.835um 0.700um 1.155um
paint m2c
box 3.020um 0.835um 3.280um 1.155um
paint m2c
box 5.600um 0.835um 5.860um 1.155um
paint m2c
box 0.435um 0.835um 5.865um 1.155um
paint metal2
label D c metal2
box 0.570um 6.945um 5.730um 7.175um
paint metal1
label G c metal1
box 3.065um -0.085um 3.235um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L1_m1__nf4_gboth_sdfull_outD
gds write nfet_01v8_W24_L1_m1__nf4_gboth_sdfull_outD
quit -noprompt
