drc off
gds read nfet_01v8_lvt_W4_L4_m2__nf1_gboth_sdhalf.gds
load nfet_01v8_lvt_W4_L4_m2__nf1_gboth_sdhalf
select top cell
box 0.455um 2.785um 0.685um 2.985um
paint metal1
label D c metal1
box 4.745um 2.785um 4.975um 2.985um
paint metal1
label S c metal1
box 0.735um 4.945um 4.695um 5.175um
paint metal1
label G c metal1
box 2.630um -0.085um 2.800um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W4_L4_m2__nf1_gboth_sdhalf
gds write nfet_01v8_lvt_W4_L4_m2__nf1_gboth_sdhalf
quit -noprompt
