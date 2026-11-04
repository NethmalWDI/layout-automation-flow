drc off
gds read nfet_01v8_lvt_W4_L4_m2__nf2_gboth_sdhalf_outD_ng.gds
load nfet_01v8_lvt_W4_L4_m2__nf2_gboth_sdhalf_outD_ng
select top cell
box 4.305um 1.600um 4.565um 1.920um
paint m2c
box 0.010um 1.600um 8.860um 1.920um
paint metal2
label S c metal2
box 0.015um 0.960um 0.275um 1.280um
paint m2c
box 8.595um 0.960um 8.855um 1.280um
paint m2c
box 0.010um 0.960um 8.860um 1.280um
paint metal2
label D c metal2
box 0.145um 2.600um 8.725um 2.830um
paint metal1
label G c metal1
box 0.050um 1.390um 0.150um 1.490um
paint pwell
label B c pwell
save nfet_01v8_lvt_W4_L4_m2__nf2_gboth_sdhalf_outD_ng
gds write nfet_01v8_lvt_W4_L4_m2__nf2_gboth_sdhalf_outD_ng
quit -noprompt
