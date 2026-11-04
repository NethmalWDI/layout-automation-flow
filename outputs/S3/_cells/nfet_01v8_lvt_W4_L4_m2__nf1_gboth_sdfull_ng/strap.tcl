drc off
gds read nfet_01v8_lvt_W4_L4_m2__nf1_gboth_sdfull_ng.gds
load nfet_01v8_lvt_W4_L4_m2__nf1_gboth_sdfull_ng
select top cell
box 0.030um 2.440um 0.260um 2.640um
paint metal1
label D c metal1
box 4.320um 2.440um 4.550um 2.640um
paint metal1
label S c metal1
box 0.310um 4.600um 4.270um 4.830um
paint metal1
label G c metal1
box 0.050um 2.390um 0.150um 2.490um
paint pwell
label B c pwell
save nfet_01v8_lvt_W4_L4_m2__nf1_gboth_sdfull_ng
gds write nfet_01v8_lvt_W4_L4_m2__nf1_gboth_sdfull_ng
quit -noprompt
