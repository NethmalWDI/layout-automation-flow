drc off
gds read nfet_01v8_lvt_W0p6_L5_m2__nf1_gboth_sdfull_ng.gds
load nfet_01v8_lvt_W0p6_L5_m2__nf1_gboth_sdfull_ng
select top cell
box 0.030um 0.740um 0.260um 0.940um
paint metal1
label D c metal1
box 5.320um 0.740um 5.550um 0.940um
paint metal1
label S c metal1
box 0.310um 1.200um 5.270um 1.430um
paint metal1
label G c metal1
box 0.050um 0.690um 0.150um 0.790um
paint pwell
label B c pwell
save nfet_01v8_lvt_W0p6_L5_m2__nf1_gboth_sdfull_ng
gds write nfet_01v8_lvt_W0p6_L5_m2__nf1_gboth_sdfull_ng
quit -noprompt
