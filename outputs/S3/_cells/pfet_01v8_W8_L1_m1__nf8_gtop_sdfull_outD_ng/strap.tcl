drc off
gds read pfet_01v8_W8_L1_m1__nf8_gtop_sdfull_outD_ng.gds
load pfet_01v8_W8_L1_m1__nf8_gtop_sdfull_outD_ng
select top cell
box 1.485um 0.940um 1.745um 1.260um
paint m2c
box 4.065um 0.940um 4.325um 1.260um
paint m2c
box 6.645um 0.940um 6.905um 1.260um
paint m2c
box 9.225um 0.940um 9.485um 1.260um
paint m2c
box 0.190um 0.940um 10.780um 1.260um
paint metal2
label S c metal2
box 0.195um 0.360um 0.455um 0.680um
paint m2c
box 2.775um 0.360um 3.035um 0.680um
paint m2c
box 5.355um 0.360um 5.615um 0.680um
paint m2c
box 7.935um 0.360um 8.195um 0.680um
paint m2c
box 10.515um 0.360um 10.775um 0.680um
paint m2c
box 0.190um 0.360um 10.780um 0.680um
paint metal2
label D c metal2
box 0.325um 1.515um 10.645um 1.745um
paint metal1
label G c metal1
box 0.050um 0.855um 0.150um 0.955um
paint nwell
label B c nwell
save pfet_01v8_W8_L1_m1__nf8_gtop_sdfull_outD_ng
gds write pfet_01v8_W8_L1_m1__nf8_gtop_sdfull_outD_ng
quit -noprompt
