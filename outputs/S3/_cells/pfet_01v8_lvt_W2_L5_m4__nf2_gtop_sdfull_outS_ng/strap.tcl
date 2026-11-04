drc off
gds read pfet_01v8_lvt_W2_L5_m4__nf2_gtop_sdfull_outS_ng.gds
load pfet_01v8_lvt_W2_L5_m4__nf2_gtop_sdfull_outS_ng
select top cell
box 0.195um 0.940um 0.455um 1.260um
paint m2c
box 10.775um 0.940um 11.035um 1.260um
paint m2c
box 0.190um 0.940um 11.040um 1.260um
paint metal2
label S c metal2
box 5.485um 0.360um 5.745um 0.680um
paint m2c
box 0.190um 0.360um 11.040um 0.680um
paint metal2
label D c metal2
box 0.325um 1.515um 10.905um 1.745um
paint metal1
label G c metal1
box 0.050um 0.855um 0.150um 0.955um
paint nwell
label B c nwell
save pfet_01v8_lvt_W2_L5_m4__nf2_gtop_sdfull_outS_ng
gds write pfet_01v8_lvt_W2_L5_m4__nf2_gtop_sdfull_outS_ng
quit -noprompt
