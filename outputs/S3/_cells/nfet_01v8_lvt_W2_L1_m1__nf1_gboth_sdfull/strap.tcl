drc off
gds read nfet_01v8_lvt_W2_L1_m1__nf1_gboth_sdfull.gds
load nfet_01v8_lvt_W2_L1_m1__nf1_gboth_sdfull
select top cell
box 0.455um 1.785um 0.685um 1.985um
paint metal1
label D c metal1
box 1.745um 1.785um 1.975um 1.985um
paint metal1
label S c metal1
box 0.735um 2.945um 1.695um 3.175um
paint metal1
label G c metal1
box 1.130um -0.085um 1.300um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W2_L1_m1__nf1_gboth_sdfull
gds write nfet_01v8_lvt_W2_L1_m1__nf1_gboth_sdfull
quit -noprompt
