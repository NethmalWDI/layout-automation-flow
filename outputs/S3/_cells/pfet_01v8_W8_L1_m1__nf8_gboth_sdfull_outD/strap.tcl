drc off
gds read pfet_01v8_W8_L1_m1__nf8_gboth_sdfull_outD.gds
load pfet_01v8_W8_L1_m1__nf8_gboth_sdfull_outD
select top cell
box 1.730um 1.460um 1.990um 1.780um
paint m2c
box 4.310um 1.460um 4.570um 1.780um
paint m2c
box 6.890um 1.460um 7.150um 1.780um
paint m2c
box 9.470um 1.460um 9.730um 1.780um
paint m2c
box 0.435um 1.460um 11.025um 1.780um
paint metal2
label S c metal2
box 0.440um 0.880um 0.700um 1.200um
paint m2c
box 3.020um 0.880um 3.280um 1.200um
paint m2c
box 5.600um 0.880um 5.860um 1.200um
paint m2c
box 8.180um 0.880um 8.440um 1.200um
paint m2c
box 10.760um 0.880um 11.020um 1.200um
paint m2c
box 0.435um 0.880um 11.025um 1.200um
paint metal2
label D c metal2
box 0.570um 2.035um 10.890um 2.265um
paint metal1
label G c metal1
box 5.645um -0.085um 5.815um 0.085um
paint locali
label B c locali
save pfet_01v8_W8_L1_m1__nf8_gboth_sdfull_outD
gds write pfet_01v8_W8_L1_m1__nf8_gboth_sdfull_outD
quit -noprompt
