drc off
snap internal
gds read /foss/designs/outputs/S4/ota5t_gui_copy/blocks/pmos_current_mirror_load__AB/pmos_current_mirror_load__AB.gds
gds read /foss/designs/outputs/S4/ota5t_gui_copy/blocks/nmos_differential_pair__ABBA/nmos_differential_pair__ABBA.gds
gds read /foss/designs/outputs/S4/ota5t_gui_copy/blocks/nmos_current_mirror_bias__A/nmos_current_mirror_bias__A.gds
load ota5t_gui_copy_routed -silent
box -6.5800um -16.1150um -6.5800um -16.1150um
getcell pmos_current_mirror_load__AB
box -7.2900um -40.2250um -7.2900um -40.2250um
getcell nmos_differential_pair__ABBA
box -3.3600um -60.7350um -3.3600um -60.7350um
getcell nmos_current_mirror_bias__A
tech unlock *
box -0.2000um -37.6150um 0.2000um -13.7150um
paint metal4
box -0.2000um -14.1150um 0.2000um -13.7150um
paint via3
box -0.2000um -37.6150um 0.2000um -37.2150um
paint via3
box -1.0000um -39.4150um -0.6000um -14.6150um
paint metal4
box -1.0000um -15.0150um -0.6000um -14.6150um
paint via3
box -1.0000um -39.4150um -0.6000um -39.0150um
paint via3
box -0.8500um -39.2650um -0.7500um -39.1650um
label OUTP c metal4
box -1.8000um -59.9250um -1.4000um -38.1150um
paint metal4
box -1.8000um -38.5150um -1.4000um -38.1150um
paint via3
box -1.8000um -59.9250um -1.4000um -59.5250um
paint via3
box -1.8000um -20.4750um -1.4000um -19.7750um
paint metal4
box -1.8000um -20.3250um -1.4000um -19.9250um
paint via3
box -1.6500um -20.1750um -1.5500um -20.0750um
label INN c metal4
box 1.4000um -21.3750um 1.8000um -20.6750um
paint metal4
box 1.4000um -21.2250um 1.8000um -20.8250um
paint via3
box 1.5500um -21.0750um 1.6500um -20.9750um
label INP c metal4
box -0.2000um -44.5850um 0.2000um -43.8850um
paint metal4
box -0.2000um -44.4350um 0.2000um -44.0350um
paint via3
box -0.0500um -44.2850um 0.0500um -44.1850um
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
box 0.6000um -60.7250um 1.0000um -36.3150um
paint metal4
box 0.6000um -36.7150um 1.0000um -36.3150um
paint via3
box 0.6000um -40.2150um 1.0000um -39.8150um
paint via3
box 0.6000um -45.3350um 1.0000um -44.9350um
paint via3
box 0.6000um -60.7250um 1.0000um -60.3250um
paint via3
box 0.2000um -40.2150um 1.0000um -39.8150um
paint metal3
box -0.2000um -60.7250um 1.0000um -60.3250um
paint metal3
box 0.1500um -40.2650um 0.6500um -39.7650um
paint locali
box 0.2300um -40.1850um 0.5700um -39.8450um
paint mcon
box 0.2300um -40.1850um 0.5700um -39.8450um
paint m2c
box 0.2000um -40.2150um 0.6000um -39.8150um
paint m3c
box 0.1500um -40.2650um 0.6500um -39.7650um
paint metal3
box -0.2500um -60.7750um 0.2500um -60.2750um
paint locali
box -0.1700um -60.6950um 0.1700um -60.3550um
paint mcon
box -0.1700um -60.6950um 0.1700um -60.3550um
paint m2c
box -0.2000um -60.7250um 0.2000um -60.3250um
paint m3c
box -0.2500um -60.7750um 0.2500um -60.2750um
paint metal3
box 0.7500um -60.5750um 0.8500um -60.4750um
label VSS c metal4
tech revert
save ota5t_gui_copy_routed
gds write ota5t_gui_copy_routed
quit -noprompt
