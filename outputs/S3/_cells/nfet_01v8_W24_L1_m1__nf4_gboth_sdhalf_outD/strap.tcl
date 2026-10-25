drc off
gds read nfet_01v8_W24_L1_m1__nf4_gboth_sdhalf_outD.gds
load nfet_01v8_W24_L1_m1__nf4_gboth_sdhalf_outD
select top cell
box 1.730um 4.945um 1.990um 5.265um
paint m2c
box 4.310um 4.945um 4.570um 5.265um
paint m2c
box 0.435um 4.945um 5.865um 5.265um
paint metal2
label S c metal2
box 0.440um 2.305um 0.700um 2.625um
paint m2c
box 3.020um 2.305um 3.280um 2.625um
paint m2c
box 5.600um 2.305um 5.860um 2.625um
paint m2c
box 0.435um 2.305um 5.865um 2.625um
paint metal2
label D c metal2
box 0.570um 6.945um 5.730um 7.175um
paint metal1
label G c metal1
box 3.065um -0.085um 3.235um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L1_m1__nf4_gboth_sdhalf_outD
gds write nfet_01v8_W24_L1_m1__nf4_gboth_sdhalf_outD
quit -noprompt
