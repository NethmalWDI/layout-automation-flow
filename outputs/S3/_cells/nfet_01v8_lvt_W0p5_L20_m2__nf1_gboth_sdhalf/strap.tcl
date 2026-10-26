drc off
gds read nfet_01v8_lvt_W0p5_L20_m2__nf1_gboth_sdhalf.gds
load nfet_01v8_lvt_W0p5_L20_m2__nf1_gboth_sdhalf
select top cell
box 0.455um 1.035um 0.685um 1.235um
paint metal1
label D c metal1
box 20.745um 1.035um 20.975um 1.235um
paint metal1
label S c metal1
box 0.735um 1.445um 20.695um 1.675um
paint metal1
label G c metal1
box 10.630um -0.085um 10.800um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W0p5_L20_m2__nf1_gboth_sdhalf
gds write nfet_01v8_lvt_W0p5_L20_m2__nf1_gboth_sdhalf
quit -noprompt
