drc off
snap internal
gds read /foss/designs/outputs/S4/example_ota_5t/blocks/pmos_current_mirror_load__AB/pmos_current_mirror_load__AB.gds
gds read /foss/designs/outputs/S4/example_ota_5t/blocks/nmos_differential_pair__AB/nmos_differential_pair__AB.gds
gds read /foss/designs/outputs/S4/example_ota_5t/blocks/nmos_current_mirror_bias__A/nmos_current_mirror_bias__A.gds
load example_ota_5t_routed -silent
box -4.0400um -15.2150um -4.0400um -15.2150um
getcell pmos_current_mirror_load__AB
box -4.2200um -37.5250um -4.2200um -37.5250um
getcell nmos_differential_pair__AB v
box -3.3600um -58.0350um -3.3600um -58.0350um
getcell nmos_current_mirror_bias__A v
tech unlock *
box -1.0000um -20.3250um -0.6000um -11.9150um
paint metal4
box -1.0000um -12.3150um -0.6000um -11.9150um
paint via3
box -1.0000um -20.3250um -0.6000um -19.9250um
paint via3
box -1.8000um -19.4250um -1.4000um -13.7150um
paint metal4
box -1.8000um -14.1150um -1.4000um -13.7150um
paint via3
box -1.8000um -19.4250um -1.4000um -19.0250um
paint via3
box -1.6500um -19.2750um -1.5500um -19.1750um
label OUTP c metal4
box -1.0000um -41.7350um -0.6000um -34.5150um
paint metal4
box -1.0000um -34.9150um -0.6000um -34.5150um
paint via3
box -1.0000um -41.7350um -0.6000um -41.3350um
paint via3
box -1.8000um -36.8650um -1.4000um -36.1650um
paint metal4
box -1.8000um -36.7150um -1.4000um -36.3150um
paint via3
box -1.6500um -36.5650um -1.5500um -36.4650um
label INN c metal4
box 1.4000um -35.9650um 1.8000um -35.2650um
paint metal4
box 1.4000um -35.8150um 1.8000um -35.4150um
paint via3
box 1.5500um -35.6650um 1.6500um -35.5650um
label INP c metal4
box -0.2000um -57.3750um 0.2000um -56.6750um
paint metal4
box -0.2000um -57.2250um 0.2000um -56.8250um
paint via3
box -0.0500um -57.0750um 0.0500um -56.9750um
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
box 0.6000um -56.3250um 1.0000um -18.2250um
paint metal4
box 0.6000um -18.6250um 1.0000um -18.2250um
paint via3
box 0.6000um -56.3250um 1.0000um -55.9250um
paint via3
box 0.6000um -40.9350um 1.0000um -40.5350um
paint via3
box -0.2000um -18.6250um 1.0000um -18.2250um
paint metal3
box -0.2000um -40.9350um 1.0000um -40.5350um
paint metal3
box -0.2500um -18.6750um 0.2500um -18.1750um
paint locali
box -0.1700um -18.5950um 0.1700um -18.2550um
paint mcon
box -0.1700um -18.5950um 0.1700um -18.2550um
paint m2c
box -0.2000um -18.6250um 0.2000um -18.2250um
paint m3c
box -0.2500um -18.6750um 0.2500um -18.1750um
paint metal3
box -0.2500um -40.9850um 0.2500um -40.4850um
paint locali
box -0.1700um -40.9050um 0.1700um -40.5650um
paint mcon
box -0.1700um -40.9050um 0.1700um -40.5650um
paint m2c
box -0.2000um -40.9350um 0.2000um -40.5350um
paint m3c
box -0.2500um -40.9850um 0.2500um -40.4850um
paint metal3
box 0.7500um -56.1750um 0.8500um -56.0750um
label VSS c metal4
tech revert
save example_ota_5t_routed
gds write example_ota_5t_routed
quit -noprompt
