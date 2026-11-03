drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf4_gtop_sdhalf_outS_ng.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf4_gtop_sdhalf_outS_ng
select top cell
box 0.195um 16.965um 0.455um 17.285um
paint m2c
box 2.255um 16.965um 2.515um 17.285um
paint m2c
box 4.315um 16.965um 4.575um 17.285um
paint m2c
box 0.190um 16.965um 4.580um 17.285um
paint metal2
label S c metal2
box 1.225um 5.995um 1.485um 6.315um
paint m2c
box 3.285um 5.995um 3.545um 6.315um
paint m2c
box 0.190um 5.995um 4.580um 6.315um
paint metal2
label D c metal2
box 0.325um 23.175um 4.445um 23.405um
paint metal1
label G c metal1
box 0.050um 11.685um 0.150um 11.785um
paint nwell
label B c nwell
save pfet_01v8_lvt_W90p63_L0p74_m1__nf4_gtop_sdhalf_outS_ng
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf4_gtop_sdhalf_outS_ng
quit -noprompt
