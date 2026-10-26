drc off
gds read nfet_01v8_lvt_W10_L1_m2__nf2_gtop_sdhalf_outD.gds
load nfet_01v8_lvt_W10_L1_m2__nf2_gtop_sdhalf_outD
select top cell
box 1.730um 3.885um 1.990um 4.205um
paint m2c
box 0.435um 3.885um 3.285um 4.205um
paint metal2
label S c metal2
box 0.440um 1.745um 0.700um 2.065um
paint m2c
box 3.020um 1.745um 3.280um 2.065um
paint m2c
box 0.435um 1.745um 3.285um 2.065um
paint metal2
label D c metal2
box 0.570um 5.635um 3.150um 5.865um
paint metal1
label G c metal1
box 1.775um -0.085um 1.945um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W10_L1_m2__nf2_gtop_sdhalf_outD
gds write nfet_01v8_lvt_W10_L1_m2__nf2_gtop_sdhalf_outD
quit -noprompt
