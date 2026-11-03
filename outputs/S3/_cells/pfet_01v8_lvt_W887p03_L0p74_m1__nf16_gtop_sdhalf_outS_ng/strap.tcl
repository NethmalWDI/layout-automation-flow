drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outS_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outS_ng
select top cell
box 0.195um 41.550um 0.455um 41.870um
paint m2c
box 2.255um 41.550um 2.515um 41.870um
paint m2c
box 4.315um 41.550um 4.575um 41.870um
paint m2c
box 6.375um 41.550um 6.635um 41.870um
paint m2c
box 8.435um 41.550um 8.695um 41.870um
paint m2c
box 10.495um 41.550um 10.755um 41.870um
paint m2c
box 12.555um 41.550um 12.815um 41.870um
paint m2c
box 14.615um 41.550um 14.875um 41.870um
paint m2c
box 16.675um 41.550um 16.935um 41.870um
paint m2c
box 0.190um 41.550um 16.940um 41.870um
paint metal2
label S c metal2
box 1.225um 14.190um 1.485um 14.510um
paint m2c
box 3.285um 14.190um 3.545um 14.510um
paint m2c
box 5.345um 14.190um 5.605um 14.510um
paint m2c
box 7.405um 14.190um 7.665um 14.510um
paint m2c
box 9.465um 14.190um 9.725um 14.510um
paint m2c
box 11.525um 14.190um 11.785um 14.510um
paint m2c
box 13.585um 14.190um 13.845um 14.510um
paint m2c
box 15.645um 14.190um 15.905um 14.510um
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
save pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outS_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf16_gtop_sdhalf_outS_ng
quit -noprompt
