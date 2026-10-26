drc off
gds read pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gboth_sdfull.gds
load pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gboth_sdfull
select top cell
box 0.455um 7.935um 0.685um 8.135um
paint metal1
label D c metal1
box 1.635um 7.935um 1.865um 8.135um
paint metal1
label S c metal1
box 0.735um 15.245um 1.585um 15.475um
paint metal1
label G c metal1
box 1.075um -0.085um 1.245um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gboth_sdfull
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf1_gboth_sdfull
quit -noprompt
