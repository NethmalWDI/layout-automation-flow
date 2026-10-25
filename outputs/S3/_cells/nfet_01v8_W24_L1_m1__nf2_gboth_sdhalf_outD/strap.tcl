drc off
gds read nfet_01v8_W24_L1_m1__nf2_gboth_sdhalf_outD.gds
load nfet_01v8_W24_L1_m1__nf2_gboth_sdhalf_outD
select top cell
box 1.730um 9.445um 1.990um 9.765um
paint m2c
box 0.435um 9.445um 3.285um 9.765um
paint metal2
label S c metal2
box 0.440um 3.805um 0.700um 4.125um
paint m2c
box 3.020um 3.805um 3.280um 4.125um
paint m2c
box 0.435um 3.805um 3.285um 4.125um
paint metal2
label D c metal2
box 0.570um 12.945um 3.150um 13.175um
paint metal1
label G c metal1
box 1.775um -0.085um 1.945um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L1_m1__nf2_gboth_sdhalf_outD
gds write nfet_01v8_W24_L1_m1__nf2_gboth_sdhalf_outD
quit -noprompt
