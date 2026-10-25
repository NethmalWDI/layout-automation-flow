drc off
gds read pfet_01v8_W8_L1_m1__nf2_gboth_sdhalf_outD.gds
load pfet_01v8_W8_L1_m1__nf2_gboth_sdhalf_outD
select top cell
box 1.730um 3.490um 1.990um 3.810um
paint m2c
box 0.435um 3.490um 3.285um 3.810um
paint metal2
label S c metal2
box 0.440um 1.850um 0.700um 2.170um
paint m2c
box 3.020um 1.850um 3.280um 2.170um
paint m2c
box 0.435um 1.850um 3.285um 2.170um
paint metal2
label D c metal2
box 0.570um 5.035um 3.150um 5.265um
paint metal1
label G c metal1
box 1.775um -0.085um 1.945um 0.085um
paint locali
label B c locali
save pfet_01v8_W8_L1_m1__nf2_gboth_sdhalf_outD
gds write pfet_01v8_W8_L1_m1__nf2_gboth_sdhalf_outD
quit -noprompt
