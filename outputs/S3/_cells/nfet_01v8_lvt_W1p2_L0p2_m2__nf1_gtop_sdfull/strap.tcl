drc off
gds read nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull.gds
load nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull
select top cell
box 0.455um 1.075um 0.685um 1.275um
paint metal1
label D c metal1
box 0.945um 1.075um 1.175um 1.275um
paint metal1
label S c metal1
box 0.630um 1.835um 1.000um 2.065um
paint metal1
box 0.630um 1.835um 1.000um 2.065um
paint metal1
label G c metal1
box 0.730um -0.085um 0.900um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull
gds write nfet_01v8_lvt_W1p2_L0p2_m2__nf1_gtop_sdfull
quit -noprompt
