drc off
gds read nfet_01v8_lvt_W4_L4_m2__nf2_gtop_sdhalf_outS_ng.gds
load nfet_01v8_lvt_W4_L4_m2__nf2_gtop_sdhalf_outS_ng
select top cell
box 0.015um 1.290um 0.275um 1.610um
paint m2c
box 8.595um 1.290um 8.855um 1.610um
paint m2c
box 0.010um 1.290um 8.860um 1.610um
paint metal2
label S c metal2
box 4.305um 0.650um 4.565um 0.970um
paint m2c
box 0.010um 0.650um 8.860um 0.970um
paint metal2
label D c metal2
box 0.145um 2.290um 8.725um 2.520um
paint metal1
label G c metal1
box 0.050um 1.080um 0.150um 1.180um
paint pwell
label B c pwell
save nfet_01v8_lvt_W4_L4_m2__nf2_gtop_sdhalf_outS_ng
gds write nfet_01v8_lvt_W4_L4_m2__nf2_gtop_sdhalf_outS_ng
quit -noprompt
