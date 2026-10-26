drc off
gds read pfet_01v8_lvt_W6_L1_m2__nf4_gboth_sdfull_outS.gds
load pfet_01v8_lvt_W6_L1_m2__nf4_gboth_sdfull_outS
select top cell
box 0.440um 1.960um 0.700um 2.280um
paint m2c
box 3.020um 1.960um 3.280um 2.280um
paint m2c
box 5.600um 1.960um 5.860um 2.280um
paint m2c
box 0.435um 1.960um 5.865um 2.280um
paint metal2
label S c metal2
box 1.730um 0.880um 1.990um 1.200um
paint m2c
box 4.310um 0.880um 4.570um 1.200um
paint m2c
box 0.435um 0.880um 5.865um 1.200um
paint metal2
label D c metal2
box 0.570um 2.535um 5.730um 2.765um
paint metal1
label G c metal1
box 3.065um -0.085um 3.235um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W6_L1_m2__nf4_gboth_sdfull_outS
gds write pfet_01v8_lvt_W6_L1_m2__nf4_gboth_sdfull_outS
quit -noprompt
