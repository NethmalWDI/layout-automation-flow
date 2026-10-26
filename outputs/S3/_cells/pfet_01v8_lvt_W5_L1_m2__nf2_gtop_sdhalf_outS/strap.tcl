drc off
gds read pfet_01v8_lvt_W5_L1_m2__nf2_gtop_sdhalf_outS.gds
load pfet_01v8_lvt_W5_L1_m2__nf2_gtop_sdhalf_outS
select top cell
box 0.440um 2.010um 0.700um 2.330um
paint m2c
box 3.020um 2.010um 3.280um 2.330um
paint m2c
box 0.435um 2.010um 3.285um 2.330um
paint metal2
label S c metal2
box 1.730um 1.120um 1.990um 1.440um
paint m2c
box 0.435um 1.120um 3.285um 1.440um
paint metal2
label D c metal2
box 0.570um 3.180um 3.150um 3.410um
paint metal1
label G c metal1
box 1.775um -0.085um 1.945um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W5_L1_m2__nf2_gtop_sdhalf_outS
gds write pfet_01v8_lvt_W5_L1_m2__nf2_gtop_sdhalf_outS
quit -noprompt
