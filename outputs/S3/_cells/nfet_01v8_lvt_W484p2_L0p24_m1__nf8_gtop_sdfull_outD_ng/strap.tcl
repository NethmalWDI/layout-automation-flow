drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdfull_outD_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdfull_outD_ng
select top cell
box 0.545um 60.290um 0.805um 60.610um
paint m2c
box 1.605um 60.290um 1.865um 60.610um
paint m2c
box 2.665um 60.290um 2.925um 60.610um
paint m2c
box 3.725um 60.290um 3.985um 60.610um
paint m2c
box 0.010um 60.290um 4.520um 60.610um
paint metal2
label S c metal2
box 0.015um 0.180um 0.275um 0.500um
paint m2c
box 1.075um 0.180um 1.335um 0.500um
paint m2c
box 2.135um 0.180um 2.395um 0.500um
paint m2c
box 3.195um 0.180um 3.455um 0.500um
paint m2c
box 4.255um 0.180um 4.515um 0.500um
paint m2c
box 0.010um 0.180um 4.520um 0.500um
paint metal2
label D c metal2
box 0.145um 60.820um 4.385um 61.050um
paint metal1
label G c metal1
box 0.050um 30.345um 0.150um 30.445um
paint pwell
label B c pwell
save nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdfull_outD_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gtop_sdfull_outD_ng
quit -noprompt
