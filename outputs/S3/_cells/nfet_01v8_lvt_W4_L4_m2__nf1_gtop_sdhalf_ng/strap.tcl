drc off
gds read nfet_01v8_lvt_W4_L4_m2__nf1_gtop_sdhalf_ng.gds
load nfet_01v8_lvt_W4_L4_m2__nf1_gtop_sdhalf_ng
select top cell
box 0.030um 2.130um 0.260um 2.330um
paint metal1
label D c metal1
box 4.320um 2.130um 4.550um 2.330um
paint metal1
label S c metal1
box 0.310um 4.290um 4.270um 4.520um
paint metal1
label G c metal1
box 0.050um 2.080um 0.150um 2.180um
paint pwell
label B c pwell
save nfet_01v8_lvt_W4_L4_m2__nf1_gtop_sdhalf_ng
gds write nfet_01v8_lvt_W4_L4_m2__nf1_gtop_sdhalf_ng
quit -noprompt
