drc off
gds read nfet_01v8_lvt_W10_L1_m2__nf2_gboth_sdhalf_outS.gds
load nfet_01v8_lvt_W10_L1_m2__nf2_gboth_sdhalf_outS
select top cell
box 0.440um 4.195um 0.700um 4.515um
paint m2c
box 3.020um 4.195um 3.280um 4.515um
paint m2c
box 0.435um 4.195um 3.285um 4.515um
paint metal2
label S c metal2
box 1.730um 2.055um 1.990um 2.375um
paint m2c
box 0.435um 2.055um 3.285um 2.375um
paint metal2
label D c metal2
box 0.570um 5.945um 3.150um 6.175um
paint metal1
label G c metal1
box 1.775um -0.085um 1.945um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W10_L1_m2__nf2_gboth_sdhalf_outS
gds write nfet_01v8_lvt_W10_L1_m2__nf2_gboth_sdhalf_outS
quit -noprompt
