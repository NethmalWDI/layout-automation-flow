drc off
gds read pfet_01v8_lvt_W6_L1_m2__nf2_gboth_sdhalf_outD.gds
load pfet_01v8_lvt_W6_L1_m2__nf2_gboth_sdhalf_outD
select top cell
box 1.730um 2.740um 1.990um 3.060um
paint m2c
box 0.435um 2.740um 3.285um 3.060um
paint metal2
label S c metal2
box 0.440um 1.600um 0.700um 1.920um
paint m2c
box 3.020um 1.600um 3.280um 1.920um
paint m2c
box 0.435um 1.600um 3.285um 1.920um
paint metal2
label D c metal2
box 0.570um 4.035um 3.150um 4.265um
paint metal1
label G c metal1
box 1.775um -0.085um 1.945um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W6_L1_m2__nf2_gboth_sdhalf_outD
gds write pfet_01v8_lvt_W6_L1_m2__nf2_gboth_sdhalf_outD
quit -noprompt
