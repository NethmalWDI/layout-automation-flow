drc off
gds read pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gtop_sdhalf_outD_ng.gds
load pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gtop_sdhalf_outD_ng
select top cell
box 1.225um 13.960um 1.485um 14.280um
paint m2c
box 0.190um 13.960um 2.520um 14.280um
paint metal2
label S c metal2
box 0.195um 4.990um 0.455um 5.310um
paint m2c
box 2.255um 4.990um 2.515um 5.310um
paint m2c
box 0.190um 4.990um 2.520um 5.310um
paint metal2
label D c metal2
box 0.325um 19.165um 2.385um 19.395um
paint metal1
label G c metal1
box 0.050um 9.680um 0.150um 9.780um
paint nwell
label B c nwell
save pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gtop_sdhalf_outD_ng
gds write pfet_01v8_lvt_W37p3_L0p74_m1__nf2_gtop_sdhalf_outD_ng
quit -noprompt
