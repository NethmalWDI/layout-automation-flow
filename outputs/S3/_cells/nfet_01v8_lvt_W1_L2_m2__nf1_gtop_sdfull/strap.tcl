drc off
gds read nfet_01v8_lvt_W1_L2_m2__nf1_gtop_sdfull.gds
load nfet_01v8_lvt_W1_L2_m2__nf1_gtop_sdfull
select top cell
box 0.455um 0.975um 0.685um 1.175um
paint metal1
label D c metal1
box 2.745um 0.975um 2.975um 1.175um
paint metal1
label S c metal1
box 0.735um 1.635um 2.695um 1.865um
paint metal1
label G c metal1
box 1.630um -0.085um 1.800um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W1_L2_m2__nf1_gtop_sdfull
gds write nfet_01v8_lvt_W1_L2_m2__nf1_gtop_sdfull
quit -noprompt
