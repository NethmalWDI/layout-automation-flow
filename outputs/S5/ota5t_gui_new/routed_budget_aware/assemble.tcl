drc off
snap internal
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM3__A/XM3__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM4__A/XM4__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM1__A/XM1__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM2__A/XM2__A.gds
gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM5__A/XM5__A.gds
load ota5t_gui_new_routed -silent
box -7.4400um -14.5100um -7.4400um -14.5100um
getcell XM3__A
box 1.9000um -14.5100um 1.9000um -14.5100um
getcell XM4__A
box -7.2200um -35.3500um -7.2200um -35.3500um
getcell XM1__A v
box 1.5000um -35.3500um 1.5000um -35.3500um
getcell XM2__A v
box -2.7150um -68.1900um -2.7150um -68.1900um
getcell XM5__A v
tech unlock *
box 2.2000um -18.7200um 2.6000um -12.1100um
paint metal4
box 2.2000um -12.5100um 2.6000um -12.1100um
paint via3
box 2.2000um -18.7200um 2.6000um -18.3200um
paint via3
box 2.3500um -18.5700um 2.4500um -18.4700um
label OUTP c metal4
box -1.8000um -18.7200um -1.4000um -1.1000um
paint metal4
box -1.8000um -1.5000um -1.4000um -1.1000um
paint via3
box -1.8000um -1.5000um -1.4000um -1.1000um
paint via3
box -1.8000um -18.7200um -1.4000um -18.3200um
paint via3
box -1.8000um -1.5000um 2.5000um -1.1000um
paint metal3
box -7.0200um -18.7200um -1.4000um -18.3200um
paint metal3
box -1.0000um -40.4600um -0.6000um -33.2400um
paint metal4
box -1.0000um -33.6400um -0.6000um -33.2400um
paint via3
box -1.0000um -33.6400um -0.6000um -33.2400um
paint via3
box -1.0000um -40.4600um -0.6000um -40.0600um
paint via3
box -2.1000um -33.6400um -0.6000um -33.2400um
paint metal3
box -1.0000um -33.6400um 2.1000um -33.2400um
paint metal3
box 2.2000um -34.6900um 2.6000um -33.9900um
paint metal4
box 2.2000um -34.5400um 2.6000um -34.1400um
paint via3
box 2.3500um -34.3900um 2.4500um -34.2900um
label INN c metal4
box -2.6000um -34.6900um -2.2000um -33.9900um
paint metal4
box -2.6000um -34.5400um -2.2000um -34.1400um
paint via3
box -2.4500um -34.3900um -2.3500um -34.2900um
label INP c metal4
box -0.2000um -67.5300um 0.2000um -66.8300um
paint metal4
box -0.2000um -67.3800um 0.2000um -66.9800um
paint via3
box -0.0500um -67.2300um 0.0500um -67.1300um
label VBIAS c metal4
box -0.2000um -14.2100um 0.2000um -13.0100um
paint metal4
box -0.2000um -13.4100um 0.2000um -13.0100um
paint via3
box -0.2000um -14.2100um 0.2000um -13.8100um
paint via3
box -0.2000um -13.4100um 0.2000um -13.0100um
paint via3
box -0.2000um -14.2100um 0.2000um -13.8100um
paint via3
box -1.7000um -13.4100um 0.2000um -13.0100um
paint metal3
box -4.4700um -14.2100um 0.2000um -13.8100um
paint metal3
box -0.2000um -13.4100um 2.5000um -13.0100um
paint metal3
box -0.2000um -14.2100um 4.8700um -13.8100um
paint metal3
box -4.5200um -14.2600um -4.0200um -13.7600um
paint locali
box -4.4400um -14.1800um -4.1000um -13.8400um
paint mcon
box -4.4400um -14.1800um -4.1000um -13.8400um
paint m2c
box -4.4700um -14.2100um -4.0700um -13.8100um
paint m3c
box -4.5200um -14.2600um -4.0200um -13.7600um
paint metal3
box 4.4200um -14.2600um 4.9200um -13.7600um
paint locali
box 4.5000um -14.1800um 4.8400um -13.8400um
paint mcon
box 4.5000um -14.1800um 4.8400um -13.8400um
paint m2c
box 4.4700um -14.2100um 4.8700um -13.8100um
paint m3c
box 4.4200um -14.2600um 4.9200um -13.7600um
paint metal3
box -0.0500um -14.0600um 0.0500um -13.9600um
label VDD c metal4
box -0.2000um -39.5600um 0.2000um -17.5200um
paint metal4
box -0.2000um -17.9200um 0.2000um -17.5200um
paint via3
box -0.2000um -17.9200um 0.2000um -17.5200um
paint via3
box -0.2000um -39.5600um 0.2000um -39.1600um
paint via3
box -0.2000um -38.7600um 0.2000um -38.3600um
paint via3
box -4.5600um -17.9200um 0.2000um -17.5200um
paint metal3
box -0.2000um -17.9200um 4.5600um -17.5200um
paint metal3
box -4.6100um -17.9700um -4.1100um -17.4700um
paint locali
box -4.5300um -17.8900um -4.1900um -17.5500um
paint mcon
box -4.5300um -17.8900um -4.1900um -17.5500um
paint m2c
box -4.5600um -17.9200um -4.1600um -17.5200um
paint m3c
box -4.6100um -17.9700um -4.1100um -17.4700um
paint metal3
box 4.1100um -17.9700um 4.6100um -17.4700um
paint locali
box 4.1900um -17.8900um 4.5300um -17.5500um
paint mcon
box 4.1900um -17.8900um 4.5300um -17.5500um
paint m2c
box 4.1600um -17.9200um 4.5600um -17.5200um
paint m3c
box 4.1100um -17.9700um 4.6100um -17.4700um
paint metal3
box -0.2500um -38.8100um 0.2500um -38.3100um
paint locali
box -0.1700um -38.7300um 0.1700um -38.3900um
paint mcon
box -0.1700um -38.7300um 0.1700um -38.3900um
paint m2c
box -0.2000um -38.7600um 0.2000um -38.3600um
paint m3c
box -0.2500um -38.8100um 0.2500um -38.3100um
paint metal3
box -0.0500um -39.4100um 0.0500um -39.3100um
label VSS c metal4
tech revert
save ota5t_gui_new_routed
gds write ota5t_gui_new_routed
quit -noprompt
