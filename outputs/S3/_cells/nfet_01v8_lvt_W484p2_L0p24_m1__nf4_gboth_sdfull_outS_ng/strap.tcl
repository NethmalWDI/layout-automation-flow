drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gboth_sdfull_outS_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gboth_sdfull_outS_ng
select top cell
box 0.015um 121.120um 0.275um 121.440um
paint m2c
box 1.075um 121.120um 1.335um 121.440um
paint m2c
box 2.135um 121.120um 2.395um 121.440um
paint m2c
box 0.010um 121.120um 2.400um 121.440um
paint metal2
label S c metal2
box 0.545um 0.490um 0.805um 0.810um
paint m2c
box 1.605um 0.490um 1.865um 0.810um
paint m2c
box 0.010um 0.490um 2.400um 0.810um
paint metal2
label D c metal2
box 0.145um 121.650um 2.265um 121.880um
paint metal1
label G c metal1
box 0.050um 60.915um 0.150um 61.015um
paint pwell
label B c pwell
save nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gboth_sdfull_outS_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gboth_sdfull_outS_ng
quit -noprompt
