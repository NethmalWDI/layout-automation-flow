drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gboth_sdfull_outD_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gboth_sdfull_outD_ng
select top cell
box 0.545um 15.200um 0.805um 15.520um
paint m2c
box 1.605um 15.200um 1.865um 15.520um
paint m2c
box 2.665um 15.200um 2.925um 15.520um
paint m2c
box 3.725um 15.200um 3.985um 15.520um
paint m2c
box 4.785um 15.200um 5.045um 15.520um
paint m2c
box 5.845um 15.200um 6.105um 15.520um
paint m2c
box 6.905um 15.200um 7.165um 15.520um
paint m2c
box 7.965um 15.200um 8.225um 15.520um
paint m2c
box 9.025um 15.200um 9.285um 15.520um
paint m2c
box 10.085um 15.200um 10.345um 15.520um
paint m2c
box 11.145um 15.200um 11.405um 15.520um
paint m2c
box 12.205um 15.200um 12.465um 15.520um
paint m2c
box 13.265um 15.200um 13.525um 15.520um
paint m2c
box 14.325um 15.200um 14.585um 15.520um
paint m2c
box 15.385um 15.200um 15.645um 15.520um
paint m2c
box 16.445um 15.200um 16.705um 15.520um
paint m2c
box 0.010um 15.200um 17.240um 15.520um
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
box 9.555um 0.490um 9.815um 0.810um
paint m2c
box 10.615um 0.490um 10.875um 0.810um
paint m2c
box 11.675um 0.490um 11.935um 0.810um
paint m2c
box 12.735um 0.490um 12.995um 0.810um
paint m2c
box 13.795um 0.490um 14.055um 0.810um
paint m2c
box 14.855um 0.490um 15.115um 0.810um
paint m2c
box 15.915um 0.490um 16.175um 0.810um
paint m2c
box 16.975um 0.490um 17.235um 0.810um
paint m2c
box 0.010um 0.490um 17.240um 0.810um
paint metal2
label D c metal2
box 0.145um 15.730um 17.105um 15.960um
paint metal1
label G c metal1
box 0.050um 7.955um 0.150um 8.055um
paint pwell
label B c pwell
save nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gboth_sdfull_outD_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gboth_sdfull_outD_ng
quit -noprompt
