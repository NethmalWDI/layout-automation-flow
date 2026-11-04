drc off
gds read nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf_ng.gds
load nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf_ng
select top cell
box 0.030um 0.380um 0.260um 0.580um
paint metal1
label D c metal1
box 20.320um 0.380um 20.550um 0.580um
paint metal1
label S c metal1
box 0.310um 0.790um 20.270um 1.020um
paint metal1
label G c metal1
box 0.050um 0.330um 0.150um 0.430um
paint pwell
label B c pwell
save nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf_ng
gds write nfet_01v8_lvt_W0p5_L20_m2__nf1_gtop_sdhalf_ng
quit -noprompt
