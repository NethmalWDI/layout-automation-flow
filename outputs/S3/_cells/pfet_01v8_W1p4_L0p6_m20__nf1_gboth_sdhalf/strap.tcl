drc off
gds read pfet_01v8_W1p4_L0p6_m20__nf1_gboth_sdhalf.gds
load pfet_01v8_W1p4_L0p6_m20__nf1_gboth_sdhalf
select top cell
box 0.455um 1.530um 0.685um 1.730um
paint metal1
label D c metal1
box 1.345um 1.530um 1.575um 1.730um
paint metal1
label S c metal1
box 0.735um 2.435um 1.295um 2.665um
paint metal1
label G c metal1
box 0.930um -0.085um 1.100um 0.085um
paint locali
label B c locali
save pfet_01v8_W1p4_L0p6_m20__nf1_gboth_sdhalf
gds write pfet_01v8_W1p4_L0p6_m20__nf1_gboth_sdhalf
quit -noprompt
