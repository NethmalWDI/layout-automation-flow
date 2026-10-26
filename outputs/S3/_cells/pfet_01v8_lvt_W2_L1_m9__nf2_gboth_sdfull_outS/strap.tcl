drc off
gds read pfet_01v8_lvt_W2_L1_m9__nf2_gboth_sdfull_outS.gds
load pfet_01v8_lvt_W2_L1_m9__nf2_gboth_sdfull_outS
select top cell
box 0.440um 1.460um 0.700um 1.780um
paint m2c
box 3.020um 1.460um 3.280um 1.780um
paint m2c
box 0.435um 1.460um 3.285um 1.780um
paint metal2
label S c metal2
box 1.730um 0.880um 1.990um 1.200um
paint m2c
box 0.435um 0.880um 3.285um 1.200um
paint metal2
label D c metal2
box 0.570um 2.035um 3.150um 2.265um
paint metal1
label G c metal1
box 1.775um -0.085um 1.945um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W2_L1_m9__nf2_gboth_sdfull_outS
gds write pfet_01v8_lvt_W2_L1_m9__nf2_gboth_sdfull_outS
quit -noprompt
