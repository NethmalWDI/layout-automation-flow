drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gtop_sdhalf_outS_ng.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gtop_sdhalf_outS_ng
select top cell
box 0.195um 6.965um 0.455um 7.285um
paint m2c
box 2.255um 6.965um 2.515um 7.285um
paint m2c
box 4.315um 6.965um 4.575um 7.285um
paint m2c
box 0.190um 6.965um 4.580um 7.285um
paint metal2
label S c metal2
box 1.225um 2.665um 1.485um 2.985um
paint m2c
box 3.285um 2.665um 3.545um 2.985um
paint m2c
box 0.190um 2.665um 4.580um 2.985um
paint metal2
label D c metal2
box 0.325um 9.845um 4.445um 10.075um
paint metal1
label G c metal1
box 0.050um 5.020um 0.150um 5.120um
paint nwell
label B c nwell
save pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gtop_sdhalf_outS_ng
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf4_gtop_sdhalf_outS_ng
quit -noprompt
