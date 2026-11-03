drc off
gds read pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdfull_outS_ng.gds
load pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdfull_outS_ng
select top cell
box 0.195um 221.890um 0.455um 222.210um
paint m2c
box 2.255um 221.890um 2.515um 222.210um
paint m2c
box 4.315um 221.890um 4.575um 222.210um
paint m2c
box 0.190um 221.890um 4.580um 222.210um
paint metal2
label S c metal2
box 1.225um 0.550um 1.485um 0.870um
paint m2c
box 3.285um 0.550um 3.545um 0.870um
paint m2c
box 0.190um 0.550um 4.580um 0.870um
paint metal2
label D c metal2
box 0.325um 222.465um 4.445um 222.695um
paint metal1
label G c metal1
box 0.050um 111.330um 0.150um 111.430um
paint nwell
label B c nwell
save pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdfull_outS_ng
gds write pfet_01v8_lvt_W887p03_L0p74_m1__nf4_gboth_sdfull_outS_ng
quit -noprompt
