drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdfull_outD_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdfull_outD_ng
select top cell
box 0.545um 30.330um 0.805um 30.650um
paint m2c
box 1.605um 30.330um 1.865um 30.650um
paint m2c
box 2.665um 30.330um 2.925um 30.650um
paint m2c
box 3.725um 30.330um 3.985um 30.650um
paint m2c
box 4.785um 30.330um 5.045um 30.650um
paint m2c
box 5.845um 30.330um 6.105um 30.650um
paint m2c
box 6.905um 30.330um 7.165um 30.650um
paint m2c
box 7.965um 30.330um 8.225um 30.650um
paint m2c
box 0.010um 30.330um 8.760um 30.650um
paint metal2
label S c metal2
box 0.015um 0.490um 0.275um 0.810um
paint m2c
box 1.075um 0.490um 1.335um 0.810um
paint m2c
box 2.135um 0.490um 2.395um 0.810um
paint m2c
box 3.195um 0.490um 3.455um 0.810um
paint m2c
box 4.255um 0.490um 4.515um 0.810um
paint m2c
box 5.315um 0.490um 5.575um 0.810um
paint m2c
box 6.375um 0.490um 6.635um 0.810um
paint m2c
box 7.435um 0.490um 7.695um 0.810um
paint m2c
box 8.495um 0.490um 8.755um 0.810um
paint m2c
box 0.010um 0.490um 8.760um 0.810um
paint metal2
label D c metal2
box 0.145um 30.860um 8.625um 31.090um
paint metal1
label G c metal1
box 0.050um 15.520um 0.150um 15.620um
paint pwell
label B c pwell
save nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdfull_outD_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf16_gboth_sdfull_outD_ng
quit -noprompt
