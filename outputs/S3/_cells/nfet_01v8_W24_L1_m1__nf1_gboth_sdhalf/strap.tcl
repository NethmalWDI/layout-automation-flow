drc off
gds read nfet_01v8_W24_L1_m1__nf1_gboth_sdhalf.gds
load nfet_01v8_W24_L1_m1__nf1_gboth_sdhalf
select top cell
box 0.455um 12.785um 0.685um 12.985um
paint metal1
label D c metal1
box 1.745um 12.785um 1.975um 12.985um
paint metal1
label S c metal1
box 0.735um 24.945um 1.695um 25.175um
paint metal1
label G c metal1
box 1.130um -0.085um 1.300um 0.085um
paint locali
label B c locali
save nfet_01v8_W24_L1_m1__nf1_gboth_sdhalf
gds write nfet_01v8_W24_L1_m1__nf1_gboth_sdhalf
quit -noprompt
