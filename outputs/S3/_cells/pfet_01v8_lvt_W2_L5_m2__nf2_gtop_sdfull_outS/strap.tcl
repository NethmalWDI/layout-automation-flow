drc off
gds read pfet_01v8_lvt_W2_L5_m2__nf2_gtop_sdfull_outS.gds
load pfet_01v8_lvt_W2_L5_m2__nf2_gtop_sdfull_outS
select top cell
box 0.440um 1.105um 0.700um 1.425um
paint m2c
box 11.020um 1.105um 11.280um 1.425um
paint m2c
box 0.435um 1.105um 11.285um 1.425um
paint metal2
label S c metal2
box 5.730um 0.525um 5.990um 0.845um
paint m2c
box 0.435um 0.525um 11.285um 0.845um
paint metal2
label D c metal2
box 0.570um 1.680um 11.150um 1.910um
paint metal1
label G c metal1
box 5.775um -0.085um 5.945um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W2_L5_m2__nf2_gtop_sdfull_outS
gds write pfet_01v8_lvt_W2_L5_m2__nf2_gtop_sdfull_outS
quit -noprompt
