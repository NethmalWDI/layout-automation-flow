drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf1_gboth_sdhalf_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf1_gboth_sdhalf_ng
select top cell
box 0.030um 242.540um 0.260um 242.740um
paint metal1
label D c metal1
box 0.560um 242.540um 0.790um 242.740um
paint metal1
label S c metal1
box 0.225um 484.800um 0.595um 485.030um
paint metal1
box 0.225um 0.050um 0.595um 0.280um
paint metal1
box 0.225um 484.800um 0.595um 485.030um
paint metal1
label G c metal1
box 0.050um 242.490um 0.150um 242.590um
paint pwell
label B c pwell
save nfet_01v8_lvt_W484p2_L0p24_m1__nf1_gboth_sdhalf_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf1_gboth_sdhalf_ng
quit -noprompt
