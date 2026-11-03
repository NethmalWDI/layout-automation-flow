drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdhalf_outD_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdhalf_outD_ng
select top cell
box 0.545um 45.495um 0.805um 45.815um
paint m2c
box 1.605um 45.495um 1.865um 45.815um
paint m2c
box 2.665um 45.495um 2.925um 45.815um
paint m2c
box 3.725um 45.495um 3.985um 45.815um
paint m2c
box 0.010um 45.495um 4.520um 45.815um
paint metal2
label S c metal2
box 0.015um 15.595um 0.275um 15.915um
paint m2c
box 1.075um 15.595um 1.335um 15.915um
paint m2c
box 2.135um 15.595um 2.395um 15.915um
paint m2c
box 3.195um 15.595um 3.455um 15.915um
paint m2c
box 4.255um 15.595um 4.515um 15.915um
paint m2c
box 0.010um 15.595um 4.520um 15.915um
paint metal2
label D c metal2
box 0.145um 61.130um 4.385um 61.360um
paint metal1
label G c metal1
box 0.050um 30.655um 0.150um 30.755um
paint pwell
label B c pwell
save nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdhalf_outD_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf8_gboth_sdhalf_outD_ng
quit -noprompt
