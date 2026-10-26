drc off
gds read nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdhalf_outS.gds
load nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdhalf_outS
select top cell
box 0.440um 2.010um 0.700um 2.330um
paint m2c
box 5.020um 2.010um 5.280um 2.330um
paint m2c
box 0.435um 2.010um 5.285um 2.330um
paint metal2
label S c metal2
box 2.730um 1.120um 2.990um 1.440um
paint m2c
box 0.435um 1.120um 5.285um 1.440um
paint metal2
label D c metal2
box 0.570um 3.135um 5.150um 3.365um
paint metal1
label G c metal1
box 2.775um -0.085um 2.945um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdhalf_outS
gds write nfet_01v8_lvt_W5_L2_m2__nf2_gtop_sdhalf_outS
quit -noprompt
