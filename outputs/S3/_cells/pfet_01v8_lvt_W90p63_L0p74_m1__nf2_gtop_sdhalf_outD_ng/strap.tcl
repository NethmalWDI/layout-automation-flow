drc off
gds read pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gtop_sdhalf_outD_ng.gds
load pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gtop_sdhalf_outD_ng
select top cell
box 1.225um 33.960um 1.485um 34.280um
paint m2c
box 0.190um 33.960um 2.520um 34.280um
paint metal2
label S c metal2
box 0.195um 11.660um 0.455um 11.980um
paint m2c
box 2.255um 11.660um 2.515um 11.980um
paint m2c
box 0.190um 11.660um 2.520um 11.980um
paint metal2
label D c metal2
box 0.325um 45.835um 2.385um 46.065um
paint metal1
label G c metal1
box 0.050um 23.015um 0.150um 23.115um
paint nwell
label B c nwell
save pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gtop_sdhalf_outD_ng
gds write pfet_01v8_lvt_W90p63_L0p74_m1__nf2_gtop_sdhalf_outD_ng
quit -noprompt
