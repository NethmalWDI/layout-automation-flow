drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gboth_sdhalf_outD_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gboth_sdhalf_outD_ng
select top cell
box 0.545um 11.450um 0.805um 11.770um
paint m2c
box 1.605um 11.450um 1.865um 11.770um
paint m2c
box 2.665um 11.450um 2.925um 11.770um
paint m2c
box 3.725um 11.450um 3.985um 11.770um
paint m2c
box 4.785um 11.450um 5.045um 11.770um
paint m2c
box 5.845um 11.450um 6.105um 11.770um
paint m2c
box 6.905um 11.450um 7.165um 11.770um
paint m2c
box 7.965um 11.450um 8.225um 11.770um
paint m2c
box 9.025um 11.450um 9.285um 11.770um
paint m2c
box 10.085um 11.450um 10.345um 11.770um
paint m2c
box 11.145um 11.450um 11.405um 11.770um
paint m2c
box 12.205um 11.450um 12.465um 11.770um
paint m2c
box 13.265um 11.450um 13.525um 11.770um
paint m2c
box 14.325um 11.450um 14.585um 11.770um
paint m2c
box 15.385um 11.450um 15.645um 11.770um
paint m2c
box 16.445um 11.450um 16.705um 11.770um
paint m2c
box 0.010um 11.450um 17.240um 11.770um
paint metal2
label S c metal2
box 0.015um 4.240um 0.275um 4.560um
paint m2c
box 1.075um 4.240um 1.335um 4.560um
paint m2c
box 2.135um 4.240um 2.395um 4.560um
paint m2c
box 3.195um 4.240um 3.455um 4.560um
paint m2c
box 4.255um 4.240um 4.515um 4.560um
paint m2c
box 5.315um 4.240um 5.575um 4.560um
paint m2c
box 6.375um 4.240um 6.635um 4.560um
paint m2c
box 7.435um 4.240um 7.695um 4.560um
paint m2c
box 8.495um 4.240um 8.755um 4.560um
paint m2c
box 9.555um 4.240um 9.815um 4.560um
paint m2c
box 10.615um 4.240um 10.875um 4.560um
paint m2c
box 11.675um 4.240um 11.935um 4.560um
paint m2c
box 12.735um 4.240um 12.995um 4.560um
paint m2c
box 13.795um 4.240um 14.055um 4.560um
paint m2c
box 14.855um 4.240um 15.115um 4.560um
paint m2c
box 15.915um 4.240um 16.175um 4.560um
paint m2c
box 16.975um 4.240um 17.235um 4.560um
paint m2c
box 0.010um 4.240um 17.240um 4.560um
paint metal2
label D c metal2
box 0.145um 15.730um 17.105um 15.960um
paint metal1
label G c metal1
box 0.050um 7.955um 0.150um 8.055um
paint pwell
label B c pwell
save nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gboth_sdhalf_outD_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gboth_sdhalf_outD_ng
quit -noprompt
