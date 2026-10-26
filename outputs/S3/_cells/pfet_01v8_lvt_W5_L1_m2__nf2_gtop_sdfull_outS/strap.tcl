drc off
gds read pfet_01v8_lvt_W5_L1_m2__nf2_gtop_sdfull_outS.gds
load pfet_01v8_lvt_W5_L1_m2__nf2_gtop_sdfull_outS
select top cell
box 0.440um 2.605um 0.700um 2.925um
paint m2c
box 3.020um 2.605um 3.280um 2.925um
paint m2c
box 0.435um 2.605um 3.285um 2.925um
paint metal2
label S c metal2
box 1.730um 0.525um 1.990um 0.845um
paint m2c
box 0.435um 0.525um 3.285um 0.845um
paint metal2
label D c metal2
box 0.570um 3.180um 3.150um 3.410um
paint metal1
label G c metal1
box 1.775um -0.085um 1.945um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W5_L1_m2__nf2_gtop_sdfull_outS
gds write pfet_01v8_lvt_W5_L1_m2__nf2_gtop_sdfull_outS
quit -noprompt
