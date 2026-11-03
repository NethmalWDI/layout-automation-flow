drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gtop_sdhalf_outS_ng.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gtop_sdhalf_outS_ng
select top cell
box 0.195um 3.465um 0.455um 3.785um
paint m2c
box 2.255um 3.465um 2.515um 3.785um
paint m2c
box 4.315um 3.465um 4.575um 3.785um
paint m2c
box 6.375um 3.465um 6.635um 3.785um
paint m2c
box 8.435um 3.465um 8.695um 3.785um
paint m2c
box 0.190um 3.465um 8.700um 3.785um
paint metal2
label S c metal2
box 1.225um 1.495um 1.485um 1.815um
paint m2c
box 3.285um 1.495um 3.545um 1.815um
paint m2c
box 5.345um 1.495um 5.605um 1.815um
paint m2c
box 7.405um 1.495um 7.665um 1.815um
paint m2c
box 0.190um 1.495um 8.700um 1.815um
paint metal2
label D c metal2
box 0.325um 5.175um 8.565um 5.405um
paint metal1
label G c metal1
box 0.050um 2.685um 0.150um 2.785um
paint nwell
label B c nwell
save pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gtop_sdhalf_outS_ng
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf8_gtop_sdhalf_outS_ng
quit -noprompt
