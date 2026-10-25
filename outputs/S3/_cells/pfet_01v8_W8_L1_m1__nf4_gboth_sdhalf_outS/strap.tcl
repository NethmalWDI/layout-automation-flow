drc off
gds read pfet_01v8_W8_L1_m1__nf4_gboth_sdhalf_outS.gds
load pfet_01v8_W8_L1_m1__nf4_gboth_sdhalf_outS
select top cell
box 0.440um 1.990um 0.700um 2.310um
paint m2c
box 3.020um 1.990um 3.280um 2.310um
paint m2c
box 5.600um 1.990um 5.860um 2.310um
paint m2c
box 0.435um 1.990um 5.865um 2.310um
paint metal2
label S c metal2
box 1.730um 1.350um 1.990um 1.670um
paint m2c
box 4.310um 1.350um 4.570um 1.670um
paint m2c
box 0.435um 1.350um 5.865um 1.670um
paint metal2
label D c metal2
box 0.570um 3.035um 5.730um 3.265um
paint metal1
label G c metal1
box 3.065um -0.085um 3.235um 0.085um
paint locali
label B c locali
save pfet_01v8_W8_L1_m1__nf4_gboth_sdhalf_outS
gds write pfet_01v8_W8_L1_m1__nf4_gboth_sdhalf_outS
quit -noprompt
