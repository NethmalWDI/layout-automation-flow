drc off
gds read pfet_01v8_W8_L1_m1__nf8_gtop_sdfull_outS.gds
load pfet_01v8_W8_L1_m1__nf8_gtop_sdfull_outS
select top cell
box 0.440um 1.105um 0.700um 1.425um
paint m2c
box 3.020um 1.105um 3.280um 1.425um
paint m2c
box 5.600um 1.105um 5.860um 1.425um
paint m2c
box 8.180um 1.105um 8.440um 1.425um
paint m2c
box 10.760um 1.105um 11.020um 1.425um
paint m2c
box 0.435um 1.105um 11.025um 1.425um
paint metal2
label S c metal2
box 1.730um 0.525um 1.990um 0.845um
paint m2c
box 4.310um 0.525um 4.570um 0.845um
paint m2c
box 6.890um 0.525um 7.150um 0.845um
paint m2c
box 9.470um 0.525um 9.730um 0.845um
paint m2c
box 0.435um 0.525um 11.025um 0.845um
paint metal2
label D c metal2
box 0.570um 1.680um 10.890um 1.910um
paint metal1
label G c metal1
box 5.645um -0.085um 5.815um 0.085um
paint locali
label B c locali
save pfet_01v8_W8_L1_m1__nf8_gtop_sdfull_outS
gds write pfet_01v8_W8_L1_m1__nf8_gtop_sdfull_outS
quit -noprompt
