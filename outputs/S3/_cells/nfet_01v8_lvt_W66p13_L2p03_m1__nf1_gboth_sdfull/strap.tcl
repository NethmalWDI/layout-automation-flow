drc off
gds read nfet_01v8_lvt_W66p13_L2p03_m1__nf1_gboth_sdfull.gds
load nfet_01v8_lvt_W66p13_L2p03_m1__nf1_gboth_sdfull
select top cell
box 0.455um 33.850um 0.685um 34.050um
paint metal1
label D c metal1
box 2.775um 33.850um 3.005um 34.050um
paint metal1
label S c metal1
box 0.735um 67.075um 2.725um 67.305um
paint metal1
label G c metal1
box 1.645um -0.085um 1.815um 0.085um
paint locali
label B c locali
save nfet_01v8_lvt_W66p13_L2p03_m1__nf1_gboth_sdfull
gds write nfet_01v8_lvt_W66p13_L2p03_m1__nf1_gboth_sdfull
quit -noprompt
