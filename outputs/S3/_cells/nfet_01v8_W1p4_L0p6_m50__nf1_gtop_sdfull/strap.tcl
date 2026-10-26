drc off
gds read nfet_01v8_W1p4_L0p6_m50__nf1_gtop_sdfull.gds
load nfet_01v8_W1p4_L0p6_m50__nf1_gtop_sdfull
select top cell
box 0.455um 1.175um 0.685um 1.375um
paint metal1
label D c metal1
box 1.345um 1.175um 1.575um 1.375um
paint metal1
label S c metal1
box 0.735um 2.035um 1.295um 2.265um
paint metal1
label G c metal1
box 0.930um -0.085um 1.100um 0.085um
paint locali
label B c locali
save nfet_01v8_W1p4_L0p6_m50__nf1_gtop_sdfull
gds write nfet_01v8_W1p4_L0p6_m50__nf1_gtop_sdfull
quit -noprompt
