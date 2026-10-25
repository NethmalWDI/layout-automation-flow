drc off
gds read nfet_01v8_W24_L1_m1__nf2_gtop_sdhalf_outD.gds
load nfet_01v8_W24_L1_m1__nf2_gtop_sdhalf_outD
select top cell
box 1.730um 9.135um 1.990um 9.455um
paint m2c
box 0.435um 9.135um 3.285um 9.455um
paint metal2
label S c metal2
box 0.440um 3.495um 0.700um 3.815um
paint m2c
box 3.020um 3.495um 3.280um 3.815um
paint m2c
box 0.435um 3.495um 3.285um 3.815um
paint metal2
label D c metal2
box 0.570um 12.635um 3.150um 12.865um
paint metal1
label G c metal1
box 1.775um -0.085um 1.945um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L1_m1__nf2_gtop_sdhalf_outD
gds write nfet_01v8_W24_L1_m1__nf2_gtop_sdhalf_outD
quit -noprompt
