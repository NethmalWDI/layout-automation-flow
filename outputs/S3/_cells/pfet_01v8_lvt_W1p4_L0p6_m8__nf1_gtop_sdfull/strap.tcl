drc off
gds read pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull.gds
load pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull
select top cell
box 0.455um 1.175um 0.685um 1.375um
paint metal1
label D c metal1
box 1.345um 1.175um 1.575um 1.375um
paint metal1
label S c metal1
box 0.735um 2.080um 1.295um 2.310um
paint metal1
label G c metal1
box 0.930um -0.085um 1.100um 0.085um
paint locali
label B c locali
save pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull
gds write pfet_01v8_lvt_W1p4_L0p6_m8__nf1_gtop_sdfull
quit -noprompt
