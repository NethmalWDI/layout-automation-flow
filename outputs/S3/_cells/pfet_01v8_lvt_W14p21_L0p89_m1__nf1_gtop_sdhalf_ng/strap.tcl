drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gtop_sdhalf_ng.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gtop_sdhalf_ng
select top cell
box 0.210um 7.415um 0.440um 7.615um
paint metal1
label D c metal1
box 1.390um 7.415um 1.620um 7.615um
paint metal1
label S c metal1
box 0.490um 14.725um 1.340um 14.955um
paint metal1
label G c metal1
box 0.050um 7.460um 0.150um 7.560um
paint nwell
label B c nwell
save pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gtop_sdhalf_ng
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gtop_sdhalf_ng
quit -noprompt
