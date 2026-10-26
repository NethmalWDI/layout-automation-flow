drc off
gds read pfet_01v8_lvt_W2_L5_m4__nf2_gboth_sdfull_outD.gds
load pfet_01v8_lvt_W2_L5_m4__nf2_gboth_sdfull_outD
select top cell
box 5.730um 1.460um 5.990um 1.780um
paint m2c
box 0.435um 1.460um 11.285um 1.780um
paint metal2
label S c metal2
box 0.440um 0.880um 0.700um 1.200um
paint m2c
box 11.020um 0.880um 11.280um 1.200um
paint m2c
box 0.435um 0.880um 11.285um 1.200um
paint metal2
label D c metal2
box 0.570um 2.035um 11.150um 2.265um
paint metal1
label G c metal1
box 5.775um -0.085um 5.945um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W2_L5_m4__nf2_gboth_sdfull_outD
gds write pfet_01v8_lvt_W2_L5_m4__nf2_gboth_sdfull_outD
quit -noprompt
