drc off
gds read nfet_01v8_lvt_W5_L20_m2__nf1_gboth_sdhalf_ng.gds
load nfet_01v8_lvt_W5_L20_m2__nf1_gboth_sdhalf_ng
select top cell
box 0.030um 2.940um 0.260um 3.140um
paint metal1
label D c metal1
box 20.320um 2.940um 20.550um 3.140um
paint metal1
label S c metal1
box 0.310um 5.600um 20.270um 5.830um
paint metal1
label G c metal1
box 0.050um 2.890um 0.150um 2.990um
paint pwell
label B c pwell
save nfet_01v8_lvt_W5_L20_m2__nf1_gboth_sdhalf_ng
gds write nfet_01v8_lvt_W5_L20_m2__nf1_gboth_sdhalf_ng
quit -noprompt
