drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gtop_sdhalf_outS_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gtop_sdhalf_outS_ng
select top cell
box 0.195um 332.610um 0.455um 332.930um
paint m2c
box 2.255um 332.610um 2.515um 332.930um
paint m2c
box 0.190um 332.610um 2.520um 332.930um
paint metal2
label S c metal2
box 1.225um 111.210um 1.485um 111.530um
paint m2c
box 0.190um 111.210um 2.520um 111.530um
paint metal2
label D c metal2
box 0.325um 444.035um 2.385um 444.265um
paint metal1
label G c metal1
box 0.050um 222.115um 0.150um 222.215um
paint nwell
label B c nwell
save pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gtop_sdhalf_outS_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf2_gtop_sdhalf_outS_ng
quit -noprompt
