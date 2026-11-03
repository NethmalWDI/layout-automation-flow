drc off
gds read nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gboth_sdhalf_outS_ng.gds
load nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gboth_sdhalf_outS_ng
select top cell
box 0.015um 11.450um 0.275um 11.770um
paint m2c
box 1.075um 11.450um 1.335um 11.770um
paint m2c
box 2.135um 11.450um 2.395um 11.770um
paint m2c
box 3.195um 11.450um 3.455um 11.770um
paint m2c
box 4.255um 11.450um 4.515um 11.770um
paint m2c
box 5.315um 11.450um 5.575um 11.770um
paint m2c
box 6.375um 11.450um 6.635um 11.770um
paint m2c
box 7.435um 11.450um 7.695um 11.770um
paint m2c
box 8.495um 11.450um 8.755um 11.770um
paint m2c
box 9.555um 11.450um 9.815um 11.770um
paint m2c
box 10.615um 11.450um 10.875um 11.770um
paint m2c
box 11.675um 11.450um 11.935um 11.770um
paint m2c
box 12.735um 11.450um 12.995um 11.770um
paint m2c
box 13.795um 11.450um 14.055um 11.770um
paint m2c
box 14.855um 11.450um 15.115um 11.770um
paint m2c
box 15.915um 11.450um 16.175um 11.770um
paint m2c
box 16.975um 11.450um 17.235um 11.770um
paint m2c
box 0.010um 11.450um 17.240um 11.770um
paint metal2
label S c metal2
box 0.545um 4.240um 0.805um 4.560um
paint m2c
box 1.605um 4.240um 1.865um 4.560um
paint m2c
box 2.665um 4.240um 2.925um 4.560um
paint m2c
box 3.725um 4.240um 3.985um 4.560um
paint m2c
box 4.785um 4.240um 5.045um 4.560um
paint m2c
box 5.845um 4.240um 6.105um 4.560um
paint m2c
box 6.905um 4.240um 7.165um 4.560um
paint m2c
box 7.965um 4.240um 8.225um 4.560um
paint m2c
box 9.025um 4.240um 9.285um 4.560um
paint m2c
box 10.085um 4.240um 10.345um 4.560um
paint m2c
box 11.145um 4.240um 11.405um 4.560um
paint m2c
box 12.205um 4.240um 12.465um 4.560um
paint m2c
box 13.265um 4.240um 13.525um 4.560um
paint m2c
box 14.325um 4.240um 14.585um 4.560um
paint m2c
box 15.385um 4.240um 15.645um 4.560um
paint m2c
box 16.445um 4.240um 16.705um 4.560um
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
save nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gboth_sdhalf_outS_ng
gds write nfet_01v8_lvt_W484p2_L0p24_m1__nf32_gboth_sdhalf_outS_ng
quit -noprompt
