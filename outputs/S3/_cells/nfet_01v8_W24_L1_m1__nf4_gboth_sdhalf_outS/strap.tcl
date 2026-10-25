drc off
gds read nfet_01v8_W24_L1_m1__nf4_gboth_sdhalf_outS.gds
load nfet_01v8_W24_L1_m1__nf4_gboth_sdhalf_outS
select top cell
box 0.440um 4.945um 0.700um 5.265um
paint m2c
box 3.020um 4.945um 3.280um 5.265um
paint m2c
box 5.600um 4.945um 5.860um 5.265um
paint m2c
box 0.435um 4.945um 5.865um 5.265um
paint metal2
label S c metal2
box 1.730um 2.305um 1.990um 2.625um
paint m2c
box 4.310um 2.305um 4.570um 2.625um
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
save nfet_01v8_W24_L1_m1__nf4_gboth_sdhalf_outS
gds write nfet_01v8_W24_L1_m1__nf4_gboth_sdhalf_outS
quit -noprompt
