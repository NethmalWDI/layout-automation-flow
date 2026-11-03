drc off
gds read nfet_01v8_W24_L0p5_m1__nf2_gtop_sdhalf_outD_ng.gds
load nfet_01v8_W24_L0p5_m1__nf2_gtop_sdhalf_outD_ng
select top cell
box 0.805um 8.790um 1.065um 9.110um
paint m2c
box 0.010um 8.790um 1.860um 9.110um
paint metal2
label S c metal2
box 0.015um 3.150um 0.275um 3.470um
paint m2c
box 1.595um 3.150um 1.855um 3.470um
paint m2c
box 0.010um 3.150um 1.860um 3.470um
paint metal2
label D c metal2
box 0.145um 12.290um 1.725um 12.520um
paint metal1
label G c metal1
box 0.050um 6.080um 0.150um 6.180um
paint pwell
label B c pwell
save nfet_01v8_W24_L0p5_m1__nf2_gtop_sdhalf_outD_ng
gds write nfet_01v8_W24_L0p5_m1__nf2_gtop_sdhalf_outD_ng
quit -noprompt
