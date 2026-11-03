drc off
gds read nfet_01v8_W24_L0p5_m1__nf2_gboth_sdhalf_outS_ng.gds
load nfet_01v8_W24_L0p5_m1__nf2_gboth_sdhalf_outS_ng
select top cell
box 0.015um 9.100um 0.275um 9.420um
paint m2c
box 1.595um 9.100um 1.855um 9.420um
paint m2c
box 0.010um 9.100um 1.860um 9.420um
paint metal2
label S c metal2
box 0.805um 3.460um 1.065um 3.780um
paint m2c
box 0.010um 3.460um 1.860um 3.780um
paint metal2
label D c metal2
box 0.145um 12.600um 1.725um 12.830um
paint metal1
label G c metal1
box 0.050um 6.390um 0.150um 6.490um
paint pwell
label B c pwell
save nfet_01v8_W24_L0p5_m1__nf2_gboth_sdhalf_outS_ng
gds write nfet_01v8_W24_L0p5_m1__nf2_gboth_sdhalf_outS_ng
quit -noprompt
