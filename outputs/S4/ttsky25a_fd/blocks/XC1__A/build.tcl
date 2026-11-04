drc off
snap internal
gds read /foss/designs/outputs/S4/ttsky25a_fd/blocks/XC1__A/XC1_mim.gds
load XC1__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell XC1_mim
box 5.000um 9.805um 5.400um 12.050um
paint metal4
box 11.700um -1.650um 12.100um 0.260um
paint metal4
box 20.490um 9.805um 20.890um 12.050um
paint metal4
box 27.190um -1.650um 27.590um 0.260um
paint metal4
box 35.980um 9.805um 36.380um 12.050um
paint metal4
box 42.680um -1.650um 43.080um 0.260um
paint metal4
box 51.470um 9.805um 51.870um 12.050um
paint metal4
box 58.170um -1.650um 58.570um 0.260um
paint metal4
box 66.960um 9.805um 67.360um 12.050um
paint metal4
box 73.660um -1.650um 74.060um 0.260um
paint metal4
box 5.000um 11.650um 5.400um 12.050um
paint via3
box 11.700um -1.650um 12.100um -1.250um
paint via3
box 20.490um 11.650um 20.890um 12.050um
paint via3
box 27.190um -1.650um 27.590um -1.250um
paint via3
box 35.980um 11.650um 36.380um 12.050um
paint via3
box 42.680um -1.650um 43.080um -1.250um
paint via3
box 51.470um 11.650um 51.870um 12.050um
paint via3
box 58.170um -1.650um 58.570um -1.250um
paint via3
box 66.960um 11.650um 67.360um 12.050um
paint via3
box 73.660um -1.650um 74.060um -1.250um
paint via3
box -1.800um 11.650um 75.920um 12.050um
paint metal3
box -1.700um 11.800um -1.600um 11.900um
label Vop1 c metal3
box -1.800um -1.650um 75.920um -1.250um
paint metal3
box -1.700um -1.500um -1.600um -1.400um
label Vom c metal3
tech revert
save XC1__A
gds write XC1__A
quit -noprompt
