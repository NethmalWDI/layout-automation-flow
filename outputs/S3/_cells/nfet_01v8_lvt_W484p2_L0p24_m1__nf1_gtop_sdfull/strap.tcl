drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf1_gtop_sdfull.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf1_gtop_sdfull
select top cell
box 0.455um 242.575um 0.685um 242.775um
paint metal1
label D c metal1
box 0.985um 242.575um 1.215um 242.775um
paint metal1
label S c metal1
box 0.690um 484.835um 0.980um 485.065um
paint metal1
label G c metal1
box 0.750um -0.085um 0.920um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W484p2_L0p24_m1__nf1_gtop_sdfull
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf1_gtop_sdfull
quit -noprompt
