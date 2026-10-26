drc off
gds read nfet_01v8_lvt_W1_L10_m2__nf1_gboth_sdfull.gds
load nfet_01v8_lvt_W1_L10_m2__nf1_gboth_sdfull
select top cell
box 0.455um 1.285um 0.685um 1.485um
paint metal1
label D c metal1
box 10.745um 1.285um 10.975um 1.485um
paint metal1
label S c metal1
box 0.735um 1.945um 10.695um 2.175um
paint metal1
label G c metal1
box 5.630um -0.085um 5.800um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W1_L10_m2__nf1_gboth_sdfull
gds write nfet_01v8_lvt_W1_L10_m2__nf1_gboth_sdfull
quit -noprompt
