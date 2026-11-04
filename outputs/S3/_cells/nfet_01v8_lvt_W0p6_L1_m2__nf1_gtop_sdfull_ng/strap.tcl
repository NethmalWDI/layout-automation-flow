drc off
gds read nfet_01v8_lvt_W0p6_L1_m2__nf1_gtop_sdfull_ng.gds
load nfet_01v8_lvt_W0p6_L1_m2__nf1_gtop_sdfull_ng
select top cell
box 0.030um 0.430um 0.260um 0.630um
paint metal1
label D c metal1
box 1.320um 0.430um 1.550um 0.630um
paint metal1
label S c metal1
box 0.310um 0.890um 1.270um 1.120um
paint metal1
label G c metal1
box 0.050um 0.380um 0.150um 0.480um
paint pwell
label B c pwell
save nfet_01v8_lvt_W0p6_L1_m2__nf1_gtop_sdfull_ng
gds write nfet_01v8_lvt_W0p6_L1_m2__nf1_gtop_sdfull_ng
quit -noprompt
