drc off
gds read pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gtop_sdhalf_ng.gds
load pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gtop_sdhalf_ng
select top cell
box 0.210um 1.010um 0.440um 1.210um
paint metal1
label D c metal1
box 1.100um 1.010um 1.330um 1.210um
paint metal1
label S c metal1
box 0.490um 1.915um 1.050um 2.145um
paint metal1
label G c metal1
box 0.050um 1.055um 0.150um 1.155um
paint nwell
label B c nwell
save pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gtop_sdhalf_ng
gds write pfet_01v8_lvt_W1p4_L0p6_m6__nf1_gtop_sdhalf_ng
quit -noprompt
