drc off
gds read nfet_01v8_lvt_W10_L1_m2__nf1_gtop_sdhalf_ng.gds
load nfet_01v8_lvt_W10_L1_m2__nf1_gtop_sdhalf_ng
select top cell
box 0.030um 5.130um 0.260um 5.330um
paint metal1
label D c metal1
box 1.320um 5.130um 1.550um 5.330um
paint metal1
label S c metal1
box 0.310um 10.290um 1.270um 10.520um
paint metal1
label G c metal1
box 0.050um 5.080um 0.150um 5.180um
paint pwell
label B c pwell
save nfet_01v8_lvt_W10_L1_m2__nf1_gtop_sdhalf_ng
gds write nfet_01v8_lvt_W10_L1_m2__nf1_gtop_sdhalf_ng
quit -noprompt
