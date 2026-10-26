drc off
gds read nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdhalf_outS.gds
load nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdhalf_outS
select top cell
box 0.440um 2.010um 0.700um 2.330um
paint m2c
box 3.020um 2.010um 3.280um 2.330um
paint m2c
box 5.600um 2.010um 5.860um 2.330um
paint m2c
box 0.435um 2.010um 5.865um 2.330um
paint metal2
label S c metal2
box 1.730um 1.120um 1.990um 1.440um
paint m2c
box 4.310um 1.120um 4.570um 1.440um
paint m2c
box 0.435um 1.120um 5.865um 1.440um
paint metal2
label D c metal2
box 0.570um 3.135um 5.730um 3.365um
paint metal1
label G c metal1
box 3.065um -0.085um 3.235um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdhalf_outS
gds write nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdhalf_outS
quit -noprompt
