drc off
gds read nfet_01v8_W24_L1_m1__nf4_gtop_sdhalf_outS.gds
load nfet_01v8_W24_L1_m1__nf4_gtop_sdhalf_outS
select top cell
box 0.440um 4.635um 0.700um 4.955um
paint m2c
box 3.020um 4.635um 3.280um 4.955um
paint m2c
box 5.600um 4.635um 5.860um 4.955um
paint m2c
box 0.435um 4.635um 5.865um 4.955um
paint metal2
label S c metal2
box 1.730um 1.995um 1.990um 2.315um
paint m2c
box 4.310um 1.995um 4.570um 2.315um
paint m2c
box 0.435um 1.995um 5.865um 2.315um
paint metal2
label D c metal2
box 0.570um 6.635um 5.730um 6.865um
paint metal1
label G c metal1
box 3.065um -0.085um 3.235um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L1_m1__nf4_gtop_sdhalf_outS
gds write nfet_01v8_W24_L1_m1__nf4_gtop_sdhalf_outS
quit -noprompt
