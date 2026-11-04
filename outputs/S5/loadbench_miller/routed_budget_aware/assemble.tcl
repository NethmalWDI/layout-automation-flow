drc off
snap internal
gds read /foss/designs/outputs/S4/loadbench_miller/blocks/pmos_bias_bank__row/pmos_bias_bank__row.gds
gds read /foss/designs/outputs/S4/loadbench_miller/blocks/input_pair__AB/input_pair__AB.gds
gds read /foss/designs/outputs/S4/loadbench_miller/blocks/nmos_mirror_load__AB/nmos_mirror_load__AB.gds
gds read /foss/designs/outputs/S4/loadbench_miller/blocks/cs_stage__A/cs_stage__A.gds
gds read /foss/designs/outputs/S4/loadbench_miller/blocks/Capacitor2__A/Capacitor2__A.gds
load loadbench_miller_routed -silent
box -17.5500um -64.6500um -17.5500um -64.6500um
getcell pmos_bias_bank__row
box -5.1100um -83.0700um -5.1100um -83.0700um
getcell input_pair__AB
box -21.2000um -101.0800um -21.2000um -101.0800um
getcell nmos_mirror_load__AB
box -22.7600um -124.7700um -22.7600um -124.7700um
getcell cs_stage__A
box 1.3400um -124.7700um 1.3400um -124.7700um
getcell Capacitor2__A
tech unlock *
box -1.0000um -87.2800um -0.6000um -80.6700um
paint metal4
box -1.0000um -81.0700um -0.6000um -80.6700um
paint via3
box -1.0000um -87.2800um -0.6000um -86.8800um
paint via3
box 1.4000um -105.8100um 1.8000um -81.5700um
paint metal4
box 1.4000um -81.9700um 1.8000um -81.5700um
paint via3
box 1.4000um -100.2700um 1.8000um -99.8700um
paint via3
box 1.4000um -105.2900um 1.8000um -104.8900um
paint via3
box 1.4000um -105.8100um 1.8000um -105.4100um
paint via3
box -2.2600um -105.2900um 1.8000um -104.8900um
paint metal3
box 1.3200um -105.8100um 2.0200um -105.4100um
paint metal3
box 1.3400um -105.8100um 1.8000um -104.8900um
paint metal3
box 1.3200um -105.8100um 1.8000um -104.8900um
paint metal3
box 0.6000um -82.7700um 1.0000um -62.2500um
paint metal4
box 0.6000um -62.6500um 1.0000um -62.2500um
paint via3
box 0.6000um -70.9500um 1.0000um -70.5500um
paint via3
box 0.6000um -82.7700um 1.0000um -82.3700um
paint via3
box -0.2000um -82.7700um 1.0000um -82.3700um
paint metal3
box -0.2500um -82.8200um 0.2500um -82.3200um
paint locali
box -0.1700um -82.7400um 0.1700um -82.4000um
paint mcon
box -0.1700um -82.7400um 0.1700um -82.4000um
paint m2c
box -0.2000um -82.7700um 0.2000um -82.3700um
paint m3c
box -0.2500um -82.8200um 0.2500um -82.3200um
paint metal3
box -1.8000um -124.7700um -1.4000um -63.1500um
paint metal4
box -1.8000um -63.5500um -1.4000um -63.1500um
paint via3
box -1.8000um -123.9600um -1.4000um -123.5600um
paint via3
box -1.8000um -124.7700um -1.4000um -124.3700um
paint via3
box -2.2600um -123.9600um -1.4000um -123.5600um
paint metal3
box -1.8000um -124.7700um 1.9400um -124.3700um
paint metal3
box -1.6500um -124.6200um -1.5500um -124.5200um
label out c metal4
box -0.2000um -2.5500um 0.2000um -1.8500um
paint metal4
box -0.2000um -2.4000um 0.2000um -2.0000um
paint via3
box -0.0500um -2.2500um 0.0500um -2.1500um
label IBIAS c metal4
box -2.6000um -70.2000um -2.2000um -69.5000um
paint metal4
box -2.6000um -70.0500um -2.2000um -69.6500um
paint via3
box -2.4500um -69.9000um -2.3500um -69.8000um
label in1 c metal4
box 2.2000um -69.3000um 2.6000um -68.6000um
paint metal4
box 2.2000um -69.1500um 2.6000um -68.7500um
paint via3
box 2.3500um -69.0000um 2.4500um -68.9000um
label in2 c metal4
box -2.6000um -124.7600um -2.2000um -87.7800um
paint metal4
box -2.6000um -88.1800um -2.2000um -87.7800um
paint via3
box -2.6000um -101.0700um -2.2000um -100.6700um
paint via3
box -2.6000um -106.1900um -2.2000um -105.7900um
paint via3
box -2.6000um -124.7600um -2.2000um -124.3600um
paint via3
box -2.6000um -101.0700um 0.6000um -100.6700um
paint metal3
box -12.4100um -124.7600um -2.2000um -124.3600um
paint metal3
box 0.1500um -101.1200um 0.6500um -100.6200um
paint locali
box 0.2300um -101.0400um 0.5700um -100.7000um
paint mcon
box 0.2300um -101.0400um 0.5700um -100.7000um
paint m2c
box 0.2000um -101.0700um 0.6000um -100.6700um
paint m3c
box 0.1500um -101.1200um 0.6500um -100.6200um
paint metal3
box -12.4600um -124.8100um -11.9600um -124.3100um
paint locali
box -12.3800um -124.7300um -12.0400um -124.3900um
paint mcon
box -12.3800um -124.7300um -12.0400um -124.3900um
paint m2c
box -12.4100um -124.7600um -12.0100um -124.3600um
paint m3c
box -12.4600um -124.8100um -11.9600um -124.3100um
paint metal3
box -2.4500um -124.6100um -2.3500um -124.5100um
label sourceNmos c metal4
box -1.0000um -64.3500um -0.6000um -1.1000um
paint metal4
box -1.0000um -1.5000um -0.6000um -1.1000um
paint via3
box -1.0000um -64.3500um -0.6000um -63.9500um
paint via3
box -1.0000um -64.3500um 0.2000um -63.9500um
paint metal3
box -0.2500um -64.4000um 0.2500um -63.9000um
paint locali
box -0.1700um -64.3200um 0.1700um -63.9800um
paint mcon
box -0.1700um -64.3200um 0.1700um -63.9800um
paint m2c
box -0.2000um -64.3500um 0.2000um -63.9500um
paint m3c
box -0.2500um -64.4000um 0.2500um -63.9000um
paint metal3
box -0.8500um -64.2000um -0.7500um -64.1000um
label sourcePmos c metal4
tech revert
save loadbench_miller_routed
gds write loadbench_miller_routed
quit -noprompt
