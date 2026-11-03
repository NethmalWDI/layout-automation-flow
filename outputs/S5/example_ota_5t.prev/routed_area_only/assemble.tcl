drc off
snap internal
gds read /foss/designs/outputs/S4/example_ota_5t/blocks/pmos_current_mirror_load__AB/pmos_current_mirror_load__AB.gds
gds read /foss/designs/outputs/S4/example_ota_5t/blocks/nmos_differential_pair__AB/nmos_differential_pair__AB.gds
gds read /foss/designs/outputs/S4/example_ota_5t/blocks/nmos_current_mirror_bias__A/nmos_current_mirror_bias__A.gds
load example_ota_5t_routed -silent
box -4.0400um -15.2150um -4.0400um -15.2150um
getcell pmos_current_mirror_load__AB
box -4.2200um -37.5250um -4.2200um -37.5250um
getcell nmos_differential_pair__AB
box -3.3600um -58.0350um -3.3600um -58.0350um
getcell nmos_current_mirror_bias__A
tech unlock *
box -1.0000um -35.8150um -0.6000um -1.1000um
paint metal4
box -1.0000um -1.5000um -0.6000um -1.1000um
paint via3
box -1.0000um -12.3150um -0.6000um -11.9150um
paint via3
box -1.0000um -35.8150um -0.6000um -35.4150um
paint via3
box -1.8000um -36.7150um -1.4000um -13.7150um
paint metal4
box -1.8000um -14.1150um -1.4000um -13.7150um
paint via3
box -1.8000um -36.7150um -1.4000um -36.3150um
paint via3
box -1.6500um -36.5650um -1.5500um -36.4650um
label OUTP c metal4
box 0.6000um -57.2250um 1.0000um -20.8250um
paint metal4
box 0.6000um -21.2250um 1.0000um -20.8250um
paint via3
box 0.6000um -57.2250um 1.0000um -56.8250um
paint via3
box -2.6000um -19.5750um -2.2000um -18.8750um
paint metal4
box -2.6000um -19.4250um -2.2000um -19.0250um
paint via3
box -2.4500um -19.2750um -2.3500um -19.1750um
label INN c metal4
box 2.2000um -20.4750um 2.6000um -19.7750um
paint metal4
box 2.2000um -20.3250um 2.6000um -19.9250um
paint via3
box 2.3500um -20.1750um 2.4500um -20.0750um
label INP c metal4
box -0.2000um -41.8850um 0.2000um -41.1850um
paint metal4
box -0.2000um -41.7350um 0.2000um -41.3350um
paint via3
box -0.0500um -41.5850um 0.0500um -41.4850um
label VBIAS c metal4
box -0.2000um -14.9150um 0.2000um -12.8150um
paint metal4
box -0.2000um -13.2150um 0.2000um -12.8150um
paint via3
box -0.2000um -14.9150um 0.2000um -14.5150um
paint via3
box -0.2000um -14.9150um 0.6000um -14.5150um
paint metal3
box 0.1500um -14.9650um 0.6500um -14.4650um
paint locali
box 0.2300um -14.8850um 0.5700um -14.5450um
paint mcon
box 0.2300um -14.8850um 0.5700um -14.5450um
paint m2c
box 0.2000um -14.9150um 0.6000um -14.5150um
paint m3c
box 0.1500um -14.9650um 0.6500um -14.4650um
paint metal3
box -0.0500um -14.7650um 0.0500um -14.6650um
label VDD c metal4
box -1.0000um -58.0250um -0.6000um -37.1150um
paint metal4
box -1.0000um -37.5150um -0.6000um -37.1150um
paint via3
box -1.0000um -42.6350um -0.6000um -42.2350um
paint via3
box -1.0000um -58.0250um -0.6000um -57.6250um
paint via3
box -1.0000um -37.5150um 0.2000um -37.1150um
paint metal3
box -1.0000um -58.0250um 0.2000um -57.6250um
paint metal3
box -0.2500um -37.5650um 0.2500um -37.0650um
paint locali
box -0.1700um -37.4850um 0.1700um -37.1450um
paint mcon
box -0.1700um -37.4850um 0.1700um -37.1450um
paint m2c
box -0.2000um -37.5150um 0.2000um -37.1150um
paint m3c
box -0.2500um -37.5650um 0.2500um -37.0650um
paint metal3
box -0.2500um -58.0750um 0.2500um -57.5750um
paint locali
box -0.1700um -57.9950um 0.1700um -57.6550um
paint mcon
box -0.1700um -57.9950um 0.1700um -57.6550um
paint m2c
box -0.2000um -58.0250um 0.2000um -57.6250um
paint m3c
box -0.2500um -58.0750um 0.2500um -57.5750um
paint metal3
box -0.8500um -57.8750um -0.7500um -57.7750um
label VSS c metal4
tech revert
save example_ota_5t_routed
gds write example_ota_5t_routed
quit -noprompt
