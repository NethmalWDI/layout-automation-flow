drc off
snap internal
gds read /foss/designs/outputs/S4/loadbench_miller/blocks/Capacitor2__A/Capacitor2_mim.gds
load Capacitor2__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell Capacitor2_mim
box 7.830um 15.465um 8.230um 17.710um
paint metal4
box 17.360um -1.650um 17.760um 0.260um
paint metal4
box 7.830um 17.310um 8.230um 17.710um
paint via3
box 17.360um -1.650um 17.760um -1.250um
paint via3
box -1.800um 17.310um 19.620um 17.710um
paint metal3
box -1.700um 17.460um -1.600um 17.560um
label outFirstStage c metal3
box -1.800um -1.650um 19.620um -1.250um
paint metal3
box -1.700um -1.500um -1.600um -1.400um
label out c metal3
tech revert
save Capacitor2__A
gds write Capacitor2__A
quit -noprompt
