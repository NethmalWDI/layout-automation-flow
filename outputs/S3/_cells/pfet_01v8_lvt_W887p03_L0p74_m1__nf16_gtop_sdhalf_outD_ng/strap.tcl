drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outD_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outD_ng
select top cell
box 1.225um 41.550um 1.485um 41.870um
paint m2c
box 3.285um 41.550um 3.545um 41.870um
paint m2c
box 5.345um 41.550um 5.605um 41.870um
paint m2c
box 7.405um 41.550um 7.665um 41.870um
paint m2c
box 9.465um 41.550um 9.725um 41.870um
paint m2c
box 11.525um 41.550um 11.785um 41.870um
paint m2c
box 13.585um 41.550um 13.845um 41.870um
paint m2c
box 15.645um 41.550um 15.905um 41.870um
paint m2c
box 0.190um 41.550um 16.940um 41.870um
paint metal2
label S c metal2
box 0.195um 14.190um 0.455um 14.510um
paint m2c
box 2.255um 14.190um 2.515um 14.510um
paint m2c
box 4.315um 14.190um 4.575um 14.510um
paint m2c
box 6.375um 14.190um 6.635um 14.510um
paint m2c
box 8.435um 14.190um 8.695um 14.510um
paint m2c
box 10.495um 14.190um 10.755um 14.510um
paint m2c
box 12.555um 14.190um 12.815um 14.510um
paint m2c
box 14.615um 14.190um 14.875um 14.510um
paint m2c
box 16.675um 14.190um 16.935um 14.510um
paint m2c
box 0.190um 14.190um 16.940um 14.510um
paint metal2
label D c metal2
box 0.325um 55.955um 16.805um 56.185um
paint metal1
label G c metal1
box 0.050um 28.075um 0.150um 28.175um
paint nwell
label B c nwell
save pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outD_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outD_ng
quit -noprompt
