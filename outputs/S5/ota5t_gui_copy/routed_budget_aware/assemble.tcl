drc off
snap internal
gds read /foss/designs/outputs/S4/ota5t_gui_copy/blocks/pmos_current_mirror_load__AB/pmos_current_mirror_load__AB.gds
gds read /foss/designs/outputs/S4/ota5t_gui_copy/blocks/nmos_differential_pair__ABBA/nmos_differential_pair__ABBA.gds
gds read /foss/designs/outputs/S4/ota5t_gui_copy/blocks/nmos_current_mirror_bias__A/nmos_current_mirror_bias__A.gds
load ota5t_gui_copy_routed -silent
box -6.5800um -16.1150um -6.5800um -16.1150um
getcell pmos_current_mirror_load__AB
box -7.2900um -40.2250um -7.2900um -40.2250um
getcell nmos_differential_pair__ABBA v
box 11.0900um -40.2250um 11.0900um -40.2250um
getcell nmos_current_mirror_bias__A v
tech unlock *
box -1.0000um -22.1250um -0.6000um -13.7150um
paint metal4
box -1.0000um -14.1150um -0.6000um -13.7150um
paint via3
box -1.0000um -22.1250um -0.6000um -21.7250um
paint via3
box -1.8000um -20.3250um -1.4000um -14.6150um
paint metal4
box -1.8000um -15.0150um -1.4000um -14.6150um
paint via3
box -1.8000um -20.3250um -1.4000um -19.9250um
paint via3
box -1.6500um -20.1750um -1.5500um -20.0750um
label OUTP c metal4
box 8.6000um -23.9250um 9.0000um -20.8250um
paint metal4
box 8.6000um -21.2250um 9.0000um -20.8250um
paint via3
box 8.6000um -23.9250um 9.0000um -23.5250um
paint via3
box 7.4900um -21.2250um 9.0000um -20.8250um
paint metal3
box 8.6000um -23.9250um 11.6900um -23.5250um
paint metal3
box -1.0000um -39.5650um -0.6000um -38.8650um
paint metal4
box -1.0000um -39.4150um -0.6000um -39.0150um
paint via3
box -0.8500um -39.2650um -0.7500um -39.1650um
label INN c metal4
box 0.6000um -38.6650um 1.0000um -37.9650um
paint metal4
box 0.6000um -38.5150um 1.0000um -38.1150um
paint via3
box 0.7500um -38.3650um 0.8500um -38.2650um
label INP c metal4
box 11.8000um -39.5650um 12.2000um -38.8650um
paint metal4
box 11.8000um -39.4150um 12.2000um -39.0150um
paint via3
box 11.9500um -39.2650um 12.0500um -39.1650um
label VBIAS c metal4
box 0.6000um -15.8150um 1.0000um -2.0000um
paint metal4
box 0.6000um -2.4000um 1.0000um -2.0000um
paint via3
box 0.6000um -15.8150um 1.0000um -15.4150um
paint via3
box 0.5500um -15.8650um 1.0500um -15.3650um
paint locali
box 0.6300um -15.7850um 0.9700um -15.4450um
paint mcon
box 0.6300um -15.7850um 0.9700um -15.4450um
paint m2c
box 0.6000um -15.8150um 1.0000um -15.4150um
paint m3c
box 0.5500um -15.8650um 1.0500um -15.3650um
paint metal3
box 0.7500um -15.6650um 0.8500um -15.5650um
label VDD c metal4
box 9.4000um -38.5150um 9.8000um -19.1250um
paint metal4
box 9.4000um -23.0250um 9.8000um -22.6250um
paint via3
box 9.4000um -19.5250um 9.8000um -19.1250um
paint via3
box 9.4000um -38.5150um 9.8000um -38.1150um
paint via3
box 9.4000um -23.1250um 9.8000um -22.7250um
paint via3
box 7.4900um -23.0250um 9.8000um -22.6250um
paint metal3
box 0.2000um -19.5250um 9.8000um -19.1250um
paint metal3
box 9.4000um -38.5150um 11.6900um -38.1150um
paint metal3
box 9.4000um -23.1250um 14.6500um -22.7250um
paint metal3
box 9.4000um -23.1250um 9.8000um -22.6250um
paint metal3
box 0.1500um -19.5750um 0.6500um -19.0750um
paint locali
box 0.2300um -19.4950um 0.5700um -19.1550um
paint mcon
box 0.2300um -19.4950um 0.5700um -19.1550um
paint m2c
box 0.2000um -19.5250um 0.6000um -19.1250um
paint m3c
box 0.1500um -19.5750um 0.6500um -19.0750um
paint metal3
box 14.2000um -23.1750um 14.7000um -22.6750um
paint locali
box 14.2800um -23.0950um 14.6200um -22.7550um
paint mcon
box 14.2800um -23.0950um 14.6200um -22.7550um
paint m2c
box 14.2500um -23.1250um 14.6500um -22.7250um
paint m3c
box 14.2000um -23.1750um 14.7000um -22.6750um
paint metal3
box 9.5500um -38.3650um 9.6500um -38.2650um
label VSS c metal4
tech revert
save ota5t_gui_copy_routed
gds write ota5t_gui_copy_routed
quit -noprompt
