drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gtop_sdhalf_outS_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gtop_sdhalf_outS_ng
select top cell
box 0.015um 90.580um 0.275um 90.900um
paint m2c
box 1.075um 90.580um 1.335um 90.900um
paint m2c
box 2.135um 90.580um 2.395um 90.900um
paint m2c
box 0.010um 90.580um 2.400um 90.900um
paint metal2
label S c metal2
box 0.545um 30.410um 0.805um 30.730um
paint m2c
box 1.605um 30.410um 1.865um 30.730um
paint m2c
box 0.010um 30.410um 2.400um 30.730um
paint metal2
label D c metal2
box 0.145um 121.340um 2.265um 121.570um
paint metal1
label G c metal1
box 0.050um 60.605um 0.150um 60.705um
paint pwell
label B c pwell
save nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gtop_sdhalf_outS_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf4_gtop_sdhalf_outS_ng
quit -noprompt
