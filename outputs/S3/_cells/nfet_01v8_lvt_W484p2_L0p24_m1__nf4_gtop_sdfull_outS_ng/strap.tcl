drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gtop_sdfull_outS_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gtop_sdfull_outS_ng
select top cell
box 0.015um 120.810um 0.275um 121.130um
paint m2c
box 1.075um 120.810um 1.335um 121.130um
paint m2c
box 2.135um 120.810um 2.395um 121.130um
paint m2c
box 0.010um 120.810um 2.400um 121.130um
paint metal2
label S c metal2
box 0.545um 0.180um 0.805um 0.500um
paint m2c
box 1.605um 0.180um 1.865um 0.500um
paint m2c
box 0.010um 0.180um 2.400um 0.500um
paint metal2
label D c metal2
box 0.145um 121.340um 2.265um 121.570um
paint metal1
label G c metal1
box 0.050um 60.605um 0.150um 60.705um
paint pwell
label B c pwell
save nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gtop_sdfull_outS_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gtop_sdfull_outS_ng
quit -noprompt
