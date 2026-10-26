drc off
gds read nfet_01v8_lvt_W4_L4_m2__nf2_gtop_sdhalf_outD.gds
load nfet_01v8_lvt_W4_L4_m2__nf2_gtop_sdhalf_outD
select top cell
box 4.730um 1.635um 4.990um 1.955um
paint m2c
box 0.435um 1.635um 9.285um 1.955um
paint metal2
label S c metal2
box 0.440um 0.995um 0.700um 1.315um
paint m2c
box 9.020um 0.995um 9.280um 1.315um
paint m2c
box 0.435um 0.995um 9.285um 1.315um
paint metal2
label D c metal2
box 0.570um 2.635um 9.150um 2.865um
paint metal1
label G c metal1
box 4.775um -0.085um 4.945um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W4_L4_m2__nf2_gtop_sdhalf_outD
gds write nfet_01v8_lvt_W4_L4_m2__nf2_gtop_sdhalf_outD
quit -noprompt
