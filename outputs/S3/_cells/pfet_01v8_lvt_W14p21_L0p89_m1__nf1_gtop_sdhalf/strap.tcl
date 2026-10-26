drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gtop_sdhalf.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gtop_sdhalf
select top cell
box 0.455um 7.580um 0.685um 7.780um
paint metal1
label D c metal1
box 1.635um 7.580um 1.865um 7.780um
paint metal1
label S c metal1
box 0.735um 14.890um 1.585um 15.120um
paint metal1
label G c metal1
box 1.075um -0.085um 1.245um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gtop_sdhalf
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gtop_sdhalf
quit -noprompt
