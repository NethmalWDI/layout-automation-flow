drc off
gds read nfet_01v8_W24_L1_m1__nf1_gboth_sdhalf_ng.gds
load nfet_01v8_W24_L1_m1__nf1_gboth_sdhalf_ng
select top cell
box 0.030um 12.440um 0.260um 12.640um
paint metal1
label D c metal1
box 1.320um 12.440um 1.550um 12.640um
paint metal1
label S c metal1
box 0.310um 24.600um 1.270um 24.830um
paint metal1
label G c metal1
box 0.050um 12.390um 0.150um 12.490um
paint pwell
label B c pwell
save nfet_01v8_W24_L1_m1__nf1_gboth_sdhalf_ng
gds write nfet_01v8_W24_L1_m1__nf1_gboth_sdhalf_ng
quit -noprompt
