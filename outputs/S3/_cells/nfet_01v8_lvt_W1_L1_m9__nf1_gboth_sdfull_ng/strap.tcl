drc off
gds read nfet_01v8_lvt_W1_L1_m9__nf1_gboth_sdfull_ng.gds
load nfet_01v8_lvt_W1_L1_m9__nf1_gboth_sdfull_ng
select top cell
box 0.030um 0.940um 0.260um 1.140um
paint metal1
label D c metal1
box 1.320um 0.940um 1.550um 1.140um
paint metal1
label S c metal1
box 0.310um 1.600um 1.270um 1.830um
paint metal1
label G c metal1
box 0.050um 0.890um 0.150um 0.990um
paint pwell
label B c pwell
save nfet_01v8_lvt_W1_L1_m9__nf1_gboth_sdfull_ng
gds write nfet_01v8_lvt_W1_L1_m9__nf1_gboth_sdfull_ng
quit -noprompt
