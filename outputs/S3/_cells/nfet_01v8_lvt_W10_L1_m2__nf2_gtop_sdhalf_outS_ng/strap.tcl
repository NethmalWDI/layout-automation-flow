drc off
gds read nfet_01v8_lvt_W10_L1_m2__nf2_gtop_sdhalf_outS_ng.gds
load nfet_01v8_lvt_W10_L1_m2__nf2_gtop_sdhalf_outS_ng
select top cell
box 0.015um 3.540um 0.275um 3.860um
paint m2c
box 2.595um 3.540um 2.855um 3.860um
paint m2c
box 0.010um 3.540um 2.860um 3.860um
paint metal2
label S c metal2
box 1.305um 1.400um 1.565um 1.720um
paint m2c
box 0.010um 1.400um 2.860um 1.720um
paint metal2
label D c metal2
box 0.145um 5.290um 2.725um 5.520um
paint metal1
label G c metal1
box 0.050um 2.580um 0.150um 2.680um
paint pwell
label B c pwell
save nfet_01v8_lvt_W10_L1_m2__nf2_gtop_sdhalf_outS_ng
gds write nfet_01v8_lvt_W10_L1_m2__nf2_gtop_sdhalf_outS_ng
quit -noprompt
