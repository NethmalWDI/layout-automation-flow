drc off
gds read nfet_01v8_lvt_W5_L2_m2__nf2_gboth_sdhalf_outD_ng.gds
load nfet_01v8_lvt_W5_L2_m2__nf2_gboth_sdhalf_outD_ng
select top cell
box 2.305um 1.975um 2.565um 2.295um
paint m2c
box 0.010um 1.975um 4.860um 2.295um
paint metal2
label S c metal2
box 0.015um 1.085um 0.275um 1.405um
paint m2c
box 4.595um 1.085um 4.855um 1.405um
paint m2c
box 0.010um 1.085um 4.860um 1.405um
paint metal2
label D c metal2
box 0.145um 3.100um 4.725um 3.330um
paint metal1
label G c metal1
box 0.050um 1.640um 0.150um 1.740um
paint pwell
label B c pwell
save nfet_01v8_lvt_W5_L2_m2__nf2_gboth_sdhalf_outD_ng
gds write nfet_01v8_lvt_W5_L2_m2__nf2_gboth_sdhalf_outD_ng
quit -noprompt
