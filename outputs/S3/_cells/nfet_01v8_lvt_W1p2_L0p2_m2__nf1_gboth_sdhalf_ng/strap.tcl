drc off
gds read nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gboth_sdhalf_ng.gds
load nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gboth_sdhalf_ng
select top cell
box 0.030um 1.040um 0.260um 1.240um
paint metal1
label D c metal1
box 0.520um 1.040um 0.750um 1.240um
paint metal1
label S c metal1
box 0.205um 1.800um 0.575um 2.030um
paint metal1
box 0.205um 0.050um 0.575um 0.280um
paint metal1
box 0.205um 1.800um 0.575um 2.030um
paint metal1
label G c metal1
box 0.050um 0.990um 0.150um 1.090um
paint pwell
label B c pwell
save nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gboth_sdhalf_ng
gds write nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gboth_sdhalf_ng
quit -noprompt
