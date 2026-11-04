drc off
gds read nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdhalf_outS_ng.gds
load nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdhalf_outS_ng
select top cell
box 0.015um 1.665um 0.275um 1.985um
paint m2c
box 2.595um 1.665um 2.855um 1.985um
paint m2c
box 5.175um 1.665um 5.435um 1.985um
paint m2c
box 0.010um 1.665um 5.440um 1.985um
paint metal2
label S c metal2
box 1.305um 0.775um 1.565um 1.095um
paint m2c
box 3.885um 0.775um 4.145um 1.095um
paint m2c
box 0.010um 0.775um 5.440um 1.095um
paint metal2
label D c metal2
box 0.145um 2.790um 5.305um 3.020um
paint metal1
label G c metal1
box 0.050um 1.330um 0.150um 1.430um
paint pwell
label B c pwell
save nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdhalf_outS_ng
gds write nfet_01v8_lvt_W10_L1_m2__nf4_gtop_sdhalf_outS_ng
quit -noprompt
