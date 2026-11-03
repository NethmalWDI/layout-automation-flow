drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdhalf_outD_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdhalf_outD_ng
select top cell
box 1.225um 166.480um 1.485um 166.800um
paint m2c
box 3.285um 166.480um 3.545um 166.800um
paint m2c
box 0.190um 166.480um 4.580um 166.800um
paint metal2
label S c metal2
box 0.195um 55.960um 0.455um 56.280um
paint m2c
box 2.255um 55.960um 2.515um 56.280um
paint m2c
box 4.315um 55.960um 4.575um 56.280um
paint m2c
box 0.190um 55.960um 4.580um 56.280um
paint metal2
label D c metal2
box 0.325um 222.465um 4.445um 222.695um
paint metal1
label G c metal1
box 0.050um 111.330um 0.150um 111.430um
paint nwell
label B c nwell
save pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdhalf_outD_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdhalf_outD_ng
quit -noprompt
