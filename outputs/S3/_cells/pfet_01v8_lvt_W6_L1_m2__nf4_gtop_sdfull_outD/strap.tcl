drc off
gds read pfet_01v8_lvt_W6_L1_m2__nf4_gtop_sdfull_outD.gds
load pfet_01v8_lvt_W6_L1_m2__nf4_gtop_sdfull_outD
select top cell
box 1.730um 1.605um 1.990um 1.925um
paint m2c
box 4.310um 1.605um 4.570um 1.925um
paint m2c
box 0.435um 1.605um 5.865um 1.925um
paint metal2
label S c metal2
box 0.440um 0.525um 0.700um 0.845um
paint m2c
box 3.020um 0.525um 3.280um 0.845um
paint m2c
box 5.600um 0.525um 5.860um 0.845um
paint m2c
box 0.435um 0.525um 5.865um 0.845um
paint metal2
label D c metal2
box 0.570um 2.180um 5.730um 2.410um
paint metal1
label G c metal1
box 3.065um -0.085um 3.235um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W6_L1_m2__nf4_gtop_sdfull_outD
gds write pfet_01v8_lvt_W6_L1_m2__nf4_gtop_sdfull_outD
quit -noprompt
