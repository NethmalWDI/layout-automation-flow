drc off
snap internal
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC3__A/XC3_mim.gds
load XC3__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell XC3_mim
box 2.400um 4.605um 2.800um 6.900um
paint metal4
box 6.500um -1.700um 6.900um 0.260um
paint metal4
box 12.690um 4.605um 13.090um 6.900um
paint metal4
box 16.790um -1.700um 17.190um 0.260um
paint metal4
box 22.980um 4.605um 23.380um 6.900um
paint metal4
box 27.080um -1.700um 27.480um 0.260um
paint metal4
box 33.270um 4.605um 33.670um 6.900um
paint metal4
box 37.370um -1.700um 37.770um 0.260um
paint metal4
box 2.400um 6.500um 2.800um 6.900um
paint via3
box 6.500um -1.700um 6.900um -1.300um
paint via3
box 12.690um 6.500um 13.090um 6.900um
paint via3
box 16.790um -1.700um 17.190um -1.300um
paint via3
box 22.980um 6.500um 23.380um 6.900um
paint via3
box 27.080um -1.700um 27.480um -1.300um
paint via3
box 33.270um 6.500um 33.670um 6.900um
paint via3
box 37.370um -1.700um 37.770um -1.300um
paint via3
box -0.400um 6.500um 38.230um 6.900um
paint metal3
box -0.300um 6.650um -0.200um 6.750um
label op c metal3
box -0.400um -1.700um 38.230um -1.300um
paint metal3
box -0.300um -1.550um -0.200um -1.450um
label cmc c metal3
tech revert
save XC3__A
gds write XC3__A
quit -noprompt
