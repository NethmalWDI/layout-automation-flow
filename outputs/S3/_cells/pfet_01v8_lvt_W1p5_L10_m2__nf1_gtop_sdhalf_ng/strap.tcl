drc off
gds read pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf_ng.gds
load pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf_ng
select top cell
box 0.210um 1.060um 0.440um 1.260um
paint metal1
label D c metal1
box 10.500um 1.060um 10.730um 1.260um
paint metal1
label S c metal1
box 0.490um 2.015um 10.450um 2.245um
paint metal1
label G c metal1
box 0.050um 1.105um 0.150um 1.205um
paint nwell
label B c nwell
save pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf_ng
gds write pfet_01v8_lvt_W1p5_L10_m2__nf1_gtop_sdhalf_ng
quit -noprompt
