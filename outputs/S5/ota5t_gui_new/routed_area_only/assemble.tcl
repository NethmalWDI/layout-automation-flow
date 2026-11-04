drc off
snap internal
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM3__A/XM3__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM4__A/XM4__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM1__A/XM1__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM2__A/XM2__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM5__A/XM5__A.gds
load ota5t_gui_new_routed -silent
box -3.1700um -14.5100um -3.1700um -14.5100um
getcell XM3__A
box -2.7700um -32.0200um -2.7700um -32.0200um
getcell XM4__A
box -2.8600um -52.8600um -2.8600um -52.8600um
getcell XM1__A
box -2.8600um -73.7000um -2.8600um -73.7000um
getcell XM2__A
box -2.7150um -106.5400um -2.7150um -106.5400um
getcell XM5__A
tech unlock *
box -1.0000um -72.8900um -0.6000um -29.6200um
paint metal4
box -1.0000um -30.0200um -0.6000um -29.6200um
paint via3
box -1.0000um -72.8900um -0.6000um -72.4900um
paint via3
box -0.8500um -72.7400um -0.7500um -72.6400um
label OUTP c metal4
box 1.4000um -52.0500um 1.8000um -12.1100um
paint metal4
box 1.4000um -12.5100um 1.8000um -12.1100um
paint via3
box 1.4000um -19.0100um 1.8000um -18.6100um
paint via3
box 1.4000um -52.0500um 1.8000um -51.6500um
paint via3
box -3.4000um -104.8300um -3.0000um -36.7300um
paint metal4
box -3.4000um -37.1300um -3.0000um -36.7300um
paint via3
box -3.4000um -57.9700um -3.0000um -57.5700um
paint via3
box -3.4000um -104.8300um -3.0000um -104.4300um
paint via3
box -3.4000um -37.1300um -2.2600um -36.7300um
paint metal3
box -3.4000um -57.9700um -2.2600um -57.5700um
paint metal3
box -3.4000um -104.8300um -2.1150um -104.4300um
paint metal3
box -0.2000um -57.2200um 0.2000um -56.5200um
paint metal4
box -0.2000um -57.0700um 0.2000um -56.6700um
paint via3
box -0.0500um -56.9200um 0.0500um -56.8200um
label INN c metal4
box -0.2000um -36.3800um 0.2000um -35.6800um
paint metal4
box -0.2000um -36.2300um 0.2000um -35.8300um
paint via3
box -0.0500um -36.0800um 0.0500um -35.9800um
label INP c metal4
box -0.2000um -78.0600um 0.2000um -77.3600um
paint metal4
box -0.2000um -77.9100um 0.2000um -77.5100um
paint via3
box -0.0500um -77.7600um 0.0500um -77.6600um
label VBIAS c metal4
box -0.2000um -31.7200um 0.2000um -13.0100um
paint metal4
box -0.2000um -13.4100um 0.2000um -13.0100um
paint via3
box -0.2000um -14.2100um 0.2000um -13.8100um
paint via3
box -0.2000um -30.9200um 0.2000um -30.5200um
paint via3
box -0.2000um -31.7200um 0.2000um -31.3200um
paint via3
box -0.2500um -14.2600um 0.2500um -13.7600um
paint locali
box -0.1700um -14.1800um 0.1700um -13.8400um
paint mcon
box -0.1700um -14.1800um 0.1700um -13.8400um
paint m2c
box -0.2000um -14.2100um 0.2000um -13.8100um
paint m3c
box -0.2500um -14.2600um 0.2500um -13.7600um
paint metal3
box -0.2500um -31.7700um 0.2500um -31.2700um
paint locali
box -0.1700um -31.6900um 0.1700um -31.3500um
paint mcon
box -0.1700um -31.6900um 0.1700um -31.3500um
paint m2c
box -0.2000um -31.7200um 0.2000um -31.3200um
paint m3c
box -0.2500um -31.7700um 0.2500um -31.2700um
paint metal3
box -0.0500um -31.5700um 0.0500um -31.4700um
label VDD c metal4
box 0.6000um -106.5300um 1.0000um -52.4500um
paint metal4
box 0.6000um -52.8500um 1.0000um -52.4500um
paint via3
box 0.6000um -73.6900um 1.0000um -73.2900um
paint via3
box 0.6000um -105.7300um 1.0000um -105.3300um
paint via3
box 0.6000um -106.5300um 1.0000um -106.1300um
paint via3
box -0.2000um -52.8500um 1.0000um -52.4500um
paint metal3
box -0.2000um -73.6900um 1.0000um -73.2900um
paint metal3
box -0.2000um -106.5300um 1.0000um -106.1300um
paint metal3
box -0.2500um -52.9000um 0.2500um -52.4000um
paint locali
box -0.1700um -52.8200um 0.1700um -52.4800um
paint mcon
box -0.1700um -52.8200um 0.1700um -52.4800um
paint m2c
box -0.2000um -52.8500um 0.2000um -52.4500um
paint m3c
box -0.2500um -52.9000um 0.2500um -52.4000um
paint metal3
box -0.2500um -73.7400um 0.2500um -73.2400um
paint locali
box -0.1700um -73.6600um 0.1700um -73.3200um
paint mcon
box -0.1700um -73.6600um 0.1700um -73.3200um
paint m2c
box -0.2000um -73.6900um 0.2000um -73.2900um
paint m3c
box -0.2500um -73.7400um 0.2500um -73.2400um
paint metal3
box -0.2500um -106.5800um 0.2500um -106.0800um
paint locali
box -0.1700um -106.5000um 0.1700um -106.1600um
paint mcon
box -0.1700um -106.5000um 0.1700um -106.1600um
paint m2c
box -0.2000um -106.5300um 0.2000um -106.1300um
paint m3c
box -0.2500um -106.5800um 0.2500um -106.0800um
paint metal3
box 0.7500um -106.3800um 0.8500um -106.2800um
label VSS c metal4
tech revert
save ota5t_gui_new_routed
gds write ota5t_gui_new_routed
quit -noprompt
