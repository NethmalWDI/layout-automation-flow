drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gboth_sdfull_outS_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gboth_sdfull_outS_ng
select top cell
box 0.015um 242.170um 0.275um 242.490um
paint m2c
box 1.075um 242.170um 1.335um 242.490um
paint m2c
box 0.010um 242.170um 1.340um 242.490um
paint metal2
label S c metal2
box 0.545um 0.490um 0.805um 0.810um
paint m2c
box 0.010um 0.490um 1.340um 0.810um
paint metal2
label D c metal2
box 0.145um 242.700um 1.205um 242.930um
paint metal1
label G c metal1
box 0.050um 121.440um 0.150um 121.540um
paint pwell
label B c pwell
save nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gboth_sdfull_outS_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf2_gboth_sdfull_outS_ng
quit -noprompt
