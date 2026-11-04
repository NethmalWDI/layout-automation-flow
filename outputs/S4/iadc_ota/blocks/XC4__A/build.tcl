drc off
snap internal
gds read /foss/designs/outputs/S4/iadc_ota/blocks/XC4__A/XC4_mim.gds
load XC4__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell XC4_mim
box 2.400um 4.605um 2.800um 6.850um
paint metal4
box 6.500um -1.650um 6.900um 0.260um
paint metal4
box 12.690um 4.605um 13.090um 6.850um
paint metal4
box 16.790um -1.650um 17.190um 0.260um
paint metal4
box 22.980um 4.605um 23.380um 6.850um
paint metal4
box 27.080um -1.650um 27.480um 0.260um
paint metal4
box 33.270um 4.605um 33.670um 6.850um
paint metal4
box 37.370um -1.650um 37.770um 0.260um
paint metal4
box 2.400um 6.450um 2.800um 6.850um
paint via3
box 6.500um -1.650um 6.900um -1.250um
paint via3
box 12.690um 6.450um 13.090um 6.850um
paint via3
box 16.790um -1.650um 17.190um -1.250um
paint via3
box 22.980um 6.450um 23.380um 6.850um
paint via3
box 27.080um -1.650um 27.480um -1.250um
paint via3
box 33.270um 6.450um 33.670um 6.850um
paint via3
box 37.370um -1.650um 37.770um -1.250um
paint via3
box -1.800um 6.450um 39.630um 6.850um
paint metal3
box -1.700um 6.600um -1.600um 6.700um
label on c metal3
box -1.800um -1.650um 39.630um -1.250um
paint metal3
box -1.700um -1.500um -1.600um -1.400um
label cmc c metal3
tech revert
save XC4__A
gds write XC4__A
quit -noprompt
