drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdfull_outS_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdfull_outS_ng
select top cell
box 0.015um 60.600um 0.275um 60.920um
paint m2c
box 1.075um 60.600um 1.335um 60.920um
paint m2c
box 2.135um 60.600um 2.395um 60.920um
paint m2c
box 3.195um 60.600um 3.455um 60.920um
paint m2c
box 4.255um 60.600um 4.515um 60.920um
paint m2c
box 0.010um 60.600um 4.520um 60.920um
paint metal2
label S c metal2
box 0.545um 0.490um 0.805um 0.810um
paint m2c
box 1.605um 0.490um 1.865um 0.810um
paint m2c
box 2.665um 0.490um 2.925um 0.810um
paint m2c
box 3.725um 0.490um 3.985um 0.810um
paint m2c
box 0.010um 0.490um 4.520um 0.810um
paint metal2
label D c metal2
box 0.145um 61.130um 4.385um 61.360um
paint metal1
label G c metal1
box 0.050um 30.655um 0.150um 30.755um
paint pwell
label B c pwell
save nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdfull_outS_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdfull_outS_ng
quit -noprompt
