drc off
gds read nfet_01v8_W1p4_L0p6_m36__nf1_gboth_sdfull_ng.gds
load nfet_01v8_W1p4_L0p6_m36__nf1_gboth_sdfull_ng
select top cell
box 0.030um 1.140um 0.260um 1.340um
paint metal1
label D c metal1
box 0.920um 1.140um 1.150um 1.340um
paint metal1
label S c metal1
box 0.310um 2.000um 0.870um 2.230um
paint metal1
label G c metal1
box 0.050um 1.090um 0.150um 1.190um
paint pwell
label B c pwell
save nfet_01v8_W1p4_L0p6_m36__nf1_gboth_sdfull_ng
gds write nfet_01v8_W1p4_L0p6_m36__nf1_gboth_sdfull_ng
quit -noprompt
