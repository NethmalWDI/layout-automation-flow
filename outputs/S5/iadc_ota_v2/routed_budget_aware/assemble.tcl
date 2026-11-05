drc off
snap internal
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_bias_c__cc1/x1_cm_bias_c__cc1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_bias_b__cc3/x1_cm_bias_b__cc3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/pmos_dummy_2__f3/pmos_dummy_2__f3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/pmos_dummy__f1/pmos_dummy__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cl_src__id4/x2_cl_src__id4.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cl_casc__cc1/x2_cl_casc__cc1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cc_cm__strings1/x1_cc_cm__strings1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_diff__cc1/x2_diff__cc1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_bias_b__f2/x1_diode_bias_b__f2.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_cm_iref__cc1/x1_cm_iref__cc1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC4__A/XC4__A.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/nmos_dummy__f1/nmos_dummy__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/XC3__A/XC3__A.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_diode_m2d__f5/x1_diode_m2d__f5.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_casc__cc6/x2_cm_casc__cc6.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x2_cm_tail__cc6/x2_cm_tail__cc6.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m3__f1/x1_single_m3__f1.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m5__f3/x1_single_m5__f3.gds
gds read /foss/designs/outputs/S4/iadc_ota_v2/blocks/x1_single_m4__f1/x1_single_m4__f1.gds
load iadc_ota_v2_routed -silent
box -43.9975um -23.5800um -43.9975um -23.5800um
getcell x1_cm_bias_c__cc1
box -2.8375um -23.5800um -2.8375um -23.5800um
getcell x1_cm_bias_b__cc3
box -80.2375um -53.0700um -80.2375um -53.0700um
getcell pmos_dummy_2__f3 v
box -69.8775um -53.0700um -69.8775um -53.0700um
getcell pmos_dummy__f1 v
box -50.2775um -53.0700um -50.2775um -53.0700um
getcell x2_cl_src__id4
box -22.7175um -53.0700um -22.7175um -53.0700um
getcell x2_cl_casc__cc1 v
box -68.2525um -66.3300um -68.2525um -66.3300um
getcell x1_cc_cm__strings1
box -22.8425um -66.3300um -22.8425um -66.3300um
getcell x2_diff__cc1
box -0.9925um -66.3300um -0.9925um -66.3300um
getcell x1_diode_bias_b__f2
box -49.7225um -76.0200um -49.7225um -76.0200um
getcell x1_cm_iref__cc1
box -75.4325um -88.5200um -75.4325um -88.5200um
getcell XC4__A v
box -32.9025um -88.5200um -32.9025um -88.5200um
getcell nmos_dummy__f1 v
box 9.5675um -88.5200um 9.5675um -88.5200um
getcell XC3__A v
box -47.4925um -143.0600um -47.4925um -143.0600um
getcell x1_diode_m2d__f5
box -24.5625um -143.0600um -24.5625um -143.0600um
getcell x2_cm_casc__cc6 v
box 3.1275um -143.0600um 3.1275um -143.0600um
getcell x2_cm_tail__cc6 v
box -21.8025um -152.0000um -21.8025um -152.0000um
getcell x1_single_m3__f1
box -22.4025um -174.5300um -22.4025um -174.5300um
getcell x1_single_m5__f3
box -30.6825um -183.4700um -30.6825um -183.4700um
getcell x1_single_m4__f1
tech unlock *
box -6.6000um -25.0000um -1.4000um -24.6000um
paint metal3
box -6.6000um -25.0000um -6.2000um -22.2000um
paint metal4
box -1.8000um -25.0000um -1.4000um -22.2000um
paint metal4
box -6.6000um -25.0000um -6.2000um -24.6000um
paint via3
box -1.8000um -25.0000um -1.4000um -24.6000um
paint via3
box -6.6000um -22.7900um -6.2000um -22.0900um
paint metal4
box -6.6000um -22.6800um -6.2000um -22.2800um
paint via3
box -1.8000um -22.7900um -1.4000um -22.0900um
paint metal4
box -1.8000um -22.6800um -1.4000um -22.2800um
paint via3
box -7.4000um -25.8000um -0.6000um -25.4000um
paint metal3
box -7.4000um -25.8000um -7.0000um -20.6000um
paint metal4
box -1.0000um -25.8000um -0.6000um -19.8000um
paint metal4
box -1.0000um -25.8000um -0.6000um -25.4000um
paint via3
box -7.4000um -25.8000um -7.0000um -25.4000um
paint via3
box -7.4000um -21.2900um -7.0000um -20.4900um
paint metal4
box -7.4000um -21.1800um -7.0000um -20.7800um
paint via3
box -1.0000um -20.5400um -0.6000um -19.6900um
paint metal4
box -1.0000um -20.4300um -0.6000um -20.0300um
paint via3
box -8.2000um -26.6000um 0.2000um -26.2000um
paint metal3
box -8.2000um -26.6000um -7.8000um -21.4000um
paint metal4
box -0.2000um -26.6000um 0.2000um -21.4000um
paint metal4
box -0.2000um -26.6000um 0.2000um -26.2000um
paint via3
box -8.2000um -26.6000um -7.8000um -26.2000um
paint via3
box -8.2000um -22.0400um -7.8000um -21.2900um
paint metal4
box -8.2000um -21.9300um -7.8000um -21.5300um
paint via3
box -0.2000um -22.0400um 0.2000um -21.2900um
paint metal4
box -0.2000um -21.9300um 0.2000um -21.5300um
paint via3
box -26.6000um -53.8000um -21.4000um -53.4000um
paint metal3
box -26.6000um -43.4000um -21.4000um -43.0000um
paint metal3
box -26.6000um -53.8000um -26.2000um -43.0000um
paint metal4
box -21.8000um -60.2000um -21.4000um -53.4000um
paint metal4
box -21.8000um -45.0000um -21.4000um -43.0000um
paint metal4
box -26.6000um -43.4000um -26.2000um -43.0000um
paint via3
box -26.6000um -53.8000um -26.2000um -53.4000um
paint via3
box -21.8000um -43.4000um -21.4000um -43.0000um
paint via3
box -21.8000um -53.8000um -21.4000um -53.4000um
paint via3
box -21.8000um -60.3100um -21.4000um -59.5400um
paint metal4
box -21.8000um -60.0500um -21.4000um -59.6500um
paint via3
box -26.6000um -50.7800um -26.2000um -50.0900um
paint metal4
box -26.6000um -50.6700um -26.2000um -50.2700um
paint via3
box -21.8000um -45.4200um -21.4000um -44.4900um
paint metal4
box -21.8000um -45.3100um -21.4000um -44.9100um
paint via3
box -27.4000um -54.6000um -20.6000um -54.2000um
paint metal3
box -22.6000um -42.6000um -20.6000um -42.2000um
paint metal3
box -27.4000um -54.6000um -27.0000um -51.8000um
paint metal4
box -22.6000um -54.6000um -22.2000um -42.2000um
paint metal4
box -21.0000um -61.0000um -20.6000um -54.2000um
paint metal4
box -21.0000um -45.8000um -20.6000um -42.2000um
paint metal4
box -27.4000um -54.6000um -27.0000um -54.2000um
paint via3
box -21.0000um -54.6000um -20.6000um -54.2000um
paint via3
box -22.6000um -54.6000um -22.2000um -54.2000um
paint via3
box -22.6000um -42.6000um -22.2000um -42.2000um
paint via3
box -21.0000um -42.6000um -20.6000um -42.2000um
paint via3
box -21.0000um -61.1100um -20.6000um -60.2900um
paint metal4
box -21.0000um -60.8000um -20.6000um -60.4000um
paint via3
box -27.4000um -52.3100um -27.0000um -51.6600um
paint metal4
box -27.4000um -52.1700um -27.0000um -51.7700um
paint via3
box -21.0000um -46.1700um -20.6000um -45.2900um
paint metal4
box -21.0000um -46.0600um -20.6000um -45.6600um
paint via3
box -37.8000um -89.8000um -23.0000um -89.4000um
paint metal3
box -55.4000um -67.4000um -23.0000um -67.0000um
paint metal3
box -23.4000um -41.8000um -19.8000um -41.4000um
paint metal3
box -55.4000um -88.2000um -55.0000um -67.0000um
paint metal4
box -37.8000um -89.8000um -37.4000um -88.6000um
paint metal4
box -23.4000um -98.6000um -23.0000um -89.4000um
paint metal4
box -23.4000um -67.4000um -23.0000um -41.4000um
paint metal4
box -20.2000um -46.6000um -19.8000um -41.4000um
paint metal4
box -55.4000um -67.4000um -55.0000um -67.0000um
paint via3
box -37.8000um -89.8000um -37.4000um -89.4000um
paint via3
box -23.4000um -67.4000um -23.0000um -67.0000um
paint via3
box -23.4000um -41.8000um -23.0000um -41.4000um
paint via3
box -20.2000um -41.8000um -19.8000um -41.4000um
paint via3
box -23.4000um -89.8000um -23.0000um -89.4000um
paint via3
box -23.4000um -98.9900um -23.0000um -98.0900um
paint metal4
box -23.4000um -98.8800um -23.0000um -98.4800um
paint via3
box -37.8000um -89.1100um -37.4000um -88.0100um
paint metal4
box -37.8000um -88.5200um -37.4000um -88.1200um
paint via3
box -55.4000um -88.6300um -55.0000um -87.6900um
paint metal4
box -55.4000um -88.5200um -55.0000um -88.1200um
paint via3
box -20.2000um -46.9200um -19.8000um -46.0900um
paint metal4
box -20.2000um -46.8100um -19.8000um -46.4100um
paint via3
box -23.2500um -98.4500um -23.1500um -98.3500um
label on c metal4
box -0.2000um -89.8000um 10.6000um -89.4000um
paint metal3
box 47.0000um -89.8000um 53.0000um -89.4000um
paint metal3
box 51.8000um -43.4000um 53.0000um -43.0000um
paint metal3
box -0.2000um -99.4000um 0.2000um -89.4000um
paint metal4
box 10.2000um -89.8000um 10.6000um -88.6000um
paint metal4
box 47.0000um -89.8000um 47.4000um -88.6000um
paint metal4
box 51.8000um -48.2000um 52.2000um -43.0000um
paint metal4
box 52.6000um -89.8000um 53.0000um -43.0000um
paint metal4
box 47.0000um -89.8000um 47.4000um -89.4000um
paint via3
box -0.2000um -89.8000um 0.2000um -89.4000um
paint via3
box 52.6000um -89.8000um 53.0000um -89.4000um
paint via3
box 10.2000um -89.8000um 10.6000um -89.4000um
paint via3
box 51.8000um -43.4000um 52.2000um -43.0000um
paint via3
box 52.6000um -43.4000um 53.0000um -43.0000um
paint via3
box -0.2000um -99.7400um 0.2000um -98.8900um
paint metal4
box -0.2000um -99.6300um 0.2000um -99.2300um
paint via3
box 10.2000um -89.1100um 10.6000um -88.0100um
paint metal4
box 10.2000um -88.5200um 10.6000um -88.1200um
paint via3
box 47.0000um -89.1100um 47.4000um -88.0100um
paint metal4
box 47.0000um -88.5200um 47.4000um -88.1200um
paint via3
box 51.8000um -48.4200um 52.2000um -47.6900um
paint metal4
box 51.8000um -48.3100um 52.2000um -47.9100um
paint via3
box -0.0500um -99.2500um 0.0500um -99.1500um
label op c metal4
box -1.0000um -91.4000um 4.2000um -91.0000um
paint metal3
box -1.0000um -97.0000um -0.6000um -91.0000um
paint metal4
box 3.8000um -95.4000um 4.2000um -91.0000um
paint metal4
box 3.8000um -91.4000um 4.2000um -91.0000um
paint via3
box -1.0000um -91.4000um -0.6000um -91.0000um
paint via3
box -1.0000um -97.4900um -0.6000um -96.4900um
paint metal4
box -1.0000um -97.3800um -0.6000um -96.9800um
paint via3
box 3.8000um -95.5100um 4.2000um -94.6200um
paint metal4
box 3.8000um -95.1300um 4.2000um -94.7300um
paint via3
box -1.8000um -90.6000um 5.0000um -90.2000um
paint metal3
box -1.8000um -97.8000um -1.4000um -90.2000um
paint metal4
box 4.6000um -93.8000um 5.0000um -90.2000um
paint metal4
box -1.8000um -90.6000um -1.4000um -90.2000um
paint via3
box 4.6000um -90.6000um 5.0000um -90.2000um
paint via3
box -1.8000um -98.2400um -1.4000um -97.2900um
paint metal4
box -1.8000um -98.1300um -1.4000um -97.7300um
paint via3
box 4.6000um -93.9100um 5.0000um -93.1200um
paint metal4
box 4.6000um -93.6300um 5.0000um -93.2300um
paint via3
box -24.2000um -55.4000um -19.8000um -55.0000um
paint metal3
box -24.2000um -27.4000um -5.4000um -27.0000um
paint metal3
box -6.6000um -13.0000um -5.4000um -12.6000um
paint metal3
box -24.2000um -55.4000um -23.8000um -27.0000um
paint metal4
box -20.2000um -55.4000um -19.8000um -51.8000um
paint metal4
box -6.6000um -13.8000um -6.2000um -12.6000um
paint metal4
box -5.8000um -27.4000um -5.4000um -12.6000um
paint metal4
box -0.2000um -70.6000um 0.2000um -65.4000um
paint metal4
box 47.0000um -65.8000um 47.4000um -51.8000um
paint metal4
box -20.2000um -55.4000um -19.8000um -55.0000um
paint via3
box -5.8000um -27.4000um -5.4000um -27.0000um
paint via3
box -24.2000um -27.4000um -23.8000um -27.0000um
paint via3
box -5.8000um -13.0000um -5.4000um -12.6000um
paint via3
box -24.2000um -55.4000um -23.8000um -55.0000um
paint via3
box -6.6000um -13.0000um -6.2000um -12.6000um
paint via3
box -0.2000um -70.7100um 0.2000um -69.7800um
paint metal4
box -0.2000um -70.2900um 0.2000um -69.8900um
paint via3
box -0.2000um -65.9100um 0.2000um -65.0100um
paint metal4
box -0.2000um -65.5200um 0.2000um -65.1200um
paint via3
box 47.0000um -65.9100um 47.4000um -65.0100um
paint metal4
box 47.0000um -65.5200um 47.4000um -65.1200um
paint via3
box 47.0000um -52.6800um 47.4000um -51.6900um
paint metal4
box 47.0000um -52.5700um 47.4000um -52.1700um
paint via3
box -20.2000um -52.6800um -19.8000um -51.6900um
paint metal4
box -20.2000um -52.5700um -19.8000um -52.1700um
paint via3
box -6.6000um -14.0300um -6.2000um -13.2900um
paint metal4
box -6.6000um -13.9200um -6.2000um -13.5200um
paint via3
box -28.2000um -144.2000um -20.6000um -143.8000um
paint metal3
box -49.8000um -77.0000um -46.2000um -76.6000um
paint metal3
box -49.8000um -68.2000um -25.4000um -67.8000um
paint metal3
box -49.8000um -77.0000um -49.4000um -67.8000um
paint metal4
box -46.6000um -112.2000um -46.2000um -76.6000um
paint metal4
box -28.2000um -144.2000um -27.8000um -111.8000um
paint metal4
box -25.8000um -68.2000um -25.4000um -19.0000um
paint metal4
box -21.0000um -146.6000um -20.6000um -143.8000um
paint metal4
box -21.0000um -144.2000um -20.6000um -143.8000um
paint via3
box -46.6000um -77.0000um -46.2000um -76.6000um
paint via3
box -49.8000um -77.0000um -49.4000um -76.6000um
paint via3
box -49.8000um -68.2000um -49.4000um -67.8000um
paint via3
box -28.2000um -144.2000um -27.8000um -143.8000um
paint via3
box -25.8000um -68.2000um -25.4000um -67.8000um
paint via3
box -21.0000um -146.7100um -20.6000um -145.7600um
paint metal4
box -21.0000um -146.2700um -20.6000um -145.8700um
paint via3
box -28.2000um -112.5100um -27.8000um -111.6900um
paint metal4
box -28.2000um -112.4000um -27.8000um -112.0000um
paint via3
box -46.6000um -112.5100um -46.2000um -111.6900um
paint metal4
box -46.6000um -112.4000um -46.2000um -112.0000um
paint via3
box -25.8000um -19.7900um -25.4000um -18.8900um
paint metal4
box -25.8000um -19.6800um -25.4000um -19.2800um
paint via3
box -29.8000um -145.0000um -23.0000um -144.6000um
paint metal3
box -29.8000um -177.8000um -29.4000um -142.2000um
paint metal4
box -23.4000um -145.0000um -23.0000um -142.2000um
paint metal4
box -20.2000um -146.6000um -19.8000um -142.2000um
paint metal4
box -29.8000um -145.0000um -29.4000um -144.6000um
paint via3
box -23.4000um -145.0000um -23.0000um -144.6000um
paint via3
box -29.8000um -177.9100um -29.4000um -177.2300um
paint metal4
box -29.8000um -177.7400um -29.4000um -177.3400um
paint via3
box -29.8000um -142.7100um -29.4000um -141.7400um
paint metal4
box -29.8000um -142.2500um -29.4000um -141.8500um
paint via3
box -23.4000um -142.7600um -23.0000um -142.0900um
paint metal4
box -23.4000um -142.6500um -23.0000um -142.2500um
paint via3
box -20.2000um -142.7600um -19.8000um -142.0900um
paint metal4
box -20.2000um -142.6500um -19.8000um -142.2500um
paint via3
box -20.2000um -147.1300um -19.8000um -146.0900um
paint metal4
box -20.2000um -147.0200um -19.8000um -146.6200um
paint via3
box -5.8000um -143.4000um 4.2000um -143.0000um
paint metal3
box -21.0000um -155.4000um -20.6000um -151.0000um
paint metal4
box -6.6000um -178.6000um -6.2000um -155.0000um
paint metal4
box -5.8000um -155.4000um -5.4000um -143.0000um
paint metal4
box 3.8000um -143.4000um 4.2000um -142.2000um
paint metal4
box -5.8000um -143.4000um -5.4000um -143.0000um
paint via3
box 3.8000um -143.4000um 4.2000um -143.0000um
paint via3
box -6.6000um -178.7100um -6.2000um -177.9800um
paint metal4
box -6.6000um -178.4900um -6.2000um -178.0900um
paint via3
box -6.6000um -155.5100um -6.2000um -154.7000um
paint metal4
box -6.6000um -155.2100um -6.2000um -154.8100um
paint via3
box -21.0000um -155.5100um -20.6000um -154.7000um
paint metal4
box -21.0000um -155.2100um -20.6000um -154.8100um
paint via3
box -21.0000um -151.5100um -20.6000um -150.6800um
paint metal4
box -21.0000um -151.1900um -20.6000um -150.7900um
paint via3
box -5.8000um -155.5100um -5.4000um -154.7000um
paint metal4
box -5.8000um -155.2100um -5.4000um -154.8100um
paint via3
box 3.8000um -142.7600um 4.2000um -142.0900um
paint metal4
box 3.8000um -142.6500um 4.2000um -142.2500um
paint via3
box -6.4500um -178.4500um -6.3500um -178.3500um
label bias_a c metal4
box -25.0000um -56.2000um -19.0000um -55.8000um
paint metal3
box -19.4000um -55.4000um 0.2000um -55.0000um
paint metal3
box -26.6000um -29.0000um -24.6000um -28.6000um
paint metal3
box -9.0000um -28.2000um -2.2000um -27.8000um
paint metal3
box -2.6000um 0.6000um -1.4000um 1.0000um
paint metal3
box -43.4000um -26.6000um -43.0000um -18.2000um
paint metal4
box -26.6000um -29.0000um -26.2000um -26.2000um
paint metal4
box -25.0000um -56.2000um -24.6000um -28.6000um
paint metal4
box -19.4000um -56.2000um -19.0000um -55.0000um
paint metal4
box -9.0000um -28.2000um -8.6000um -18.2000um
paint metal4
box -2.6000um -28.2000um -2.2000um 1.0000um
paint metal4
box -1.8000um -1.0000um -1.4000um 1.0000um
paint metal4
box -0.2000um -56.2000um 0.2000um -55.0000um
paint metal4
box -1.8000um 0.6000um -1.4000um 1.0000um
paint via3
box -25.0000um -56.2000um -24.6000um -55.8000um
paint via3
box -19.4000um -55.4000um -19.0000um -55.0000um
paint via3
box -25.0000um -29.0000um -24.6000um -28.6000um
paint via3
box -2.6000um -28.2000um -2.2000um -27.8000um
paint via3
box -2.6000um 0.6000um -2.2000um 1.0000um
paint via3
box -0.2000um -55.4000um 0.2000um -55.0000um
paint via3
box -26.6000um -29.0000um -26.2000um -28.6000um
paint via3
box -19.4000um -56.2000um -19.0000um -55.8000um
paint via3
box -9.0000um -28.2000um -8.6000um -27.8000um
paint via3
box -0.2000um -56.5400um 0.2000um -55.6900um
paint metal4
box -0.2000um -56.4300um 0.2000um -56.0300um
paint via3
box -26.6000um -26.9900um -26.2000um -26.0900um
paint metal4
box -26.6000um -26.8800um -26.2000um -26.4800um
paint via3
box -43.4000um -26.9900um -43.0000um -26.0900um
paint metal4
box -43.4000um -26.8800um -43.0000um -26.4800um
paint via3
box -43.4000um -18.7100um -43.0000um -17.6700um
paint metal4
box -43.4000um -18.1800um -43.0000um -17.7800um
paint via3
box -9.0000um -18.7100um -8.6000um -17.6700um
paint metal4
box -9.0000um -18.1800um -8.6000um -17.7800um
paint via3
box -1.8000um -1.1100um -1.4000um -0.3900um
paint metal4
box -1.8000um -0.9000um -1.4000um -0.5000um
paint via3
box -50.6000um -25.0000um -42.2000um -24.6000um
paint metal3
box -50.6000um -59.4000um -50.2000um -24.6000um
paint metal4
box -42.6000um -25.0000um -42.2000um -19.8000um
paint metal4
box -50.6000um -25.0000um -50.2000um -24.6000um
paint via3
box -42.6000um -25.0000um -42.2000um -24.6000um
paint via3
box -50.6000um -59.5100um -50.2000um -58.5900um
paint metal4
box -50.6000um -59.1000um -50.2000um -58.7000um
paint via3
box -42.6000um -20.5400um -42.2000um -19.6900um
paint metal4
box -42.6000um -20.4300um -42.2000um -20.0300um
paint via3
box -50.4500um -59.2500um -50.3500um -59.1500um
label cm c metal4
box -30.6000um -185.0000um -29.4000um -184.6000um
paint metal3
box -30.6000um -175.4000um -21.4000um -175.0000um
paint metal3
box -30.6000um -185.0000um -30.2000um -175.0000um
paint metal4
box -29.8000um -185.0000um -29.4000um -182.2000um
paint metal4
box -21.8000um -175.4000um -21.4000um -172.6000um
paint metal4
box -30.6000um -185.0000um -30.2000um -184.6000um
paint via3
box -30.6000um -175.4000um -30.2000um -175.0000um
paint via3
box -21.8000um -175.4000um -21.4000um -175.0000um
paint via3
box -29.8000um -185.0000um -29.4000um -184.6000um
paint via3
box -29.8000um -182.7700um -29.4000um -182.0900um
paint metal4
box -29.8000um -182.6600um -29.4000um -182.2600um
paint via3
box -21.8000um -173.1100um -21.4000um -172.4600um
paint metal4
box -21.8000um -172.9700um -21.4000um -172.5700um
paint via3
box -49.0500um -69.8500um -48.5500um -69.3500um
paint metal4
box -49.0000um -69.9100um -48.6000um -69.0300um
paint metal4
box -49.0000um -69.5400um -48.6000um -69.1400um
paint via3
box -48.8500um -69.6500um -48.7500um -69.5500um
label IBIAS c metal4
box -5.0000um -67.4000um 28.2000um -67.0000um
paint metal3
box -5.0000um -67.4000um -4.6000um -65.4000um
paint metal4
box 27.8000um -96.2000um 28.2000um -67.0000um
paint metal4
box -5.0000um -67.4000um -4.6000um -67.0000um
paint via3
box 27.8000um -67.4000um 28.2000um -67.0000um
paint via3
box 27.8000um -96.3100um 28.2000um -95.3700um
paint metal4
box 27.8000um -95.8800um 28.2000um -95.4800um
paint via3
box -5.0000um -65.9100um -4.6000um -65.0100um
paint metal4
box -5.0000um -65.5200um -4.6000um -65.1200um
paint via3
box -53.0000um -53.8000um -48.6000um -53.4000um
paint metal3
box -53.8000um -47.4000um -52.6000um -47.0000um
paint metal3
box -73.8000um -38.6000um -68.6000um -38.2000um
paint metal3
box -53.0000um -25.8000um -41.4000um -25.4000um
paint metal3
box -79.4000um -40.2000um -79.0000um -39.0000um
paint metal4
box -73.8000um -39.4000um -73.4000um -38.2000um
paint metal4
box -69.0000um -49.0000um -68.6000um -38.2000um
paint metal4
box -53.8000um -48.2000um -53.4000um -47.0000um
paint metal4
box -53.0000um -53.8000um -52.6000um -25.4000um
paint metal4
box -49.0000um -53.8000um -48.6000um -51.0000um
paint metal4
box -41.8000um -25.8000um -41.4000um -18.2000um
paint metal4
box -19.4000um -47.4000um -19.0000um -23.0000um
paint metal4
box 0.6000um -44.2000um 1.0000um -20.6000um
paint metal4
box -69.0000um -38.6000um -68.6000um -38.2000um
paint via3
box -73.8000um -38.6000um -73.4000um -38.2000um
paint via3
box -49.0000um -53.8000um -48.6000um -53.4000um
paint via3
box -41.8000um -25.8000um -41.4000um -25.4000um
paint via3
box -53.0000um -47.4000um -52.6000um -47.0000um
paint via3
box -53.0000um -25.8000um -52.6000um -25.4000um
paint via3
box -53.8000um -47.4000um -53.4000um -47.0000um
paint via3
box -53.0000um -53.8000um -52.6000um -53.4000um
paint via3
box -49.0000um -53.1100um -48.6000um -52.4600um
paint metal4
box -49.0000um -52.9700um -48.6000um -52.5700um
paint via3
box -49.0000um -51.5300um -48.6000um -50.8900um
paint metal4
box -49.0000um -51.4200um -48.6000um -51.0200um
paint via3
box -53.8000um -48.5650um -53.4000um -47.6900um
paint metal4
box -53.8000um -48.4550um -53.4000um -48.0550um
paint via3
box -69.0000um -48.5650um -68.6000um -47.6900um
paint metal4
box -69.0000um -48.4550um -68.6000um -48.0550um
paint via3
box -69.0000um -49.3650um -68.6000um -48.4900um
paint metal4
box -69.0000um -49.2550um -68.6000um -48.8550um
paint via3
box -73.8000um -39.8500um -73.4000um -38.8900um
paint metal4
box -73.8000um -39.7400um -73.4000um -39.3400um
paint via3
box -79.4000um -39.8500um -79.0000um -38.8900um
paint metal4
box -79.4000um -39.7400um -79.0000um -39.3400um
paint via3
box -79.4000um -40.6500um -79.0000um -39.6900um
paint metal4
box -79.4000um -40.5400um -79.0000um -40.1400um
paint via3
box -41.8000um -23.5900um -41.4000um -22.8900um
paint metal4
box -41.8000um -23.4800um -41.4000um -23.0800um
paint via3
box -41.8000um -19.0400um -41.4000um -18.0900um
paint metal4
box -41.8000um -18.9300um -41.4000um -18.5300um
paint via3
box -19.4000um -23.5900um -19.0000um -22.8900um
paint metal4
box -19.4000um -23.4800um -19.0000um -23.0800um
paint via3
box -19.4000um -44.6200um -19.0000um -43.6900um
paint metal4
box -19.4000um -44.5100um -19.0000um -44.1100um
paint via3
box -19.4000um -47.6700um -19.0000um -46.8900um
paint metal4
box -19.4000um -47.5600um -19.0000um -47.1600um
paint via3
box 0.6000um -44.6200um 1.0000um -43.6900um
paint metal4
box 0.6000um -44.5100um 1.0000um -44.1100um
paint via3
box 0.6000um -23.5900um 1.0000um -22.8900um
paint metal4
box 0.6000um -23.4800um 1.0000um -23.0800um
paint via3
box 0.6000um -21.2900um 1.0000um -20.4900um
paint metal4
box 0.6000um -21.1800um 1.0000um -20.7800um
paint via3
box -49.0500um -53.0200um -48.5500um -52.5200um
paint locali
box -48.9700um -52.9400um -48.6300um -52.6000um
paint mcon
box -48.9700um -52.9400um -48.6300um -52.6000um
paint m2c
box -49.0000um -52.9700um -48.6000um -52.5700um
paint m3c
box -49.0500um -53.0200um -48.5500um -52.5200um
paint metal3
box -53.8500um -48.5050um -53.3500um -48.0050um
paint locali
box -53.7700um -48.4250um -53.4300um -48.0850um
paint mcon
box -53.7700um -48.4250um -53.4300um -48.0850um
paint m2c
box -53.8000um -48.4550um -53.4000um -48.0550um
paint m3c
box -53.8500um -48.5050um -53.3500um -48.0050um
paint metal3
box -69.0500um -48.5050um -68.5500um -48.0050um
paint locali
box -68.9700um -48.4250um -68.6300um -48.0850um
paint mcon
box -68.9700um -48.4250um -68.6300um -48.0850um
paint m2c
box -69.0000um -48.4550um -68.6000um -48.0550um
paint m3c
box -69.0500um -48.5050um -68.5500um -48.0050um
paint metal3
box -73.8500um -39.7900um -73.3500um -39.2900um
paint locali
box -73.7700um -39.7100um -73.4300um -39.3700um
paint mcon
box -73.7700um -39.7100um -73.4300um -39.3700um
paint m2c
box -73.8000um -39.7400um -73.4000um -39.3400um
paint m3c
box -73.8500um -39.7900um -73.3500um -39.2900um
paint metal3
box -79.4500um -39.7900um -78.9500um -39.2900um
paint locali
box -79.3700um -39.7100um -79.0300um -39.3700um
paint mcon
box -79.3700um -39.7100um -79.0300um -39.3700um
paint m2c
box -79.4000um -39.7400um -79.0000um -39.3400um
paint m3c
box -79.4500um -39.7900um -78.9500um -39.2900um
paint metal3
box -41.8500um -23.5300um -41.3500um -23.0300um
paint locali
box -41.7700um -23.4500um -41.4300um -23.1100um
paint mcon
box -41.7700um -23.4500um -41.4300um -23.1100um
paint m2c
box -41.8000um -23.4800um -41.4000um -23.0800um
paint m3c
box -41.8500um -23.5300um -41.3500um -23.0300um
paint metal3
box -19.4500um -23.5300um -18.9500um -23.0300um
paint locali
box -19.3700um -23.4500um -19.0300um -23.1100um
paint mcon
box -19.3700um -23.4500um -19.0300um -23.1100um
paint m2c
box -19.4000um -23.4800um -19.0000um -23.0800um
paint m3c
box -19.4500um -23.5300um -18.9500um -23.0300um
paint metal3
box -19.4500um -44.5600um -18.9500um -44.0600um
paint locali
box -19.3700um -44.4800um -19.0300um -44.1400um
paint mcon
box -19.3700um -44.4800um -19.0300um -44.1400um
paint m2c
box -19.4000um -44.5100um -19.0000um -44.1100um
paint m3c
box -19.4500um -44.5600um -18.9500um -44.0600um
paint metal3
box 0.5500um -44.5600um 1.0500um -44.0600um
paint locali
box 0.6300um -44.4800um 0.9700um -44.1400um
paint mcon
box 0.6300um -44.4800um 0.9700um -44.1400um
paint m2c
box 0.6000um -44.5100um 1.0000um -44.1100um
paint m3c
box 0.5500um -44.5600um 1.0500um -44.0600um
paint metal3
box 0.5500um -23.5300um 1.0500um -23.0300um
paint locali
box 0.6300um -23.4500um 0.9700um -23.1100um
paint mcon
box 0.6300um -23.4500um 0.9700um -23.1100um
paint m2c
box 0.6000um -23.4800um 1.0000um -23.0800um
paint m3c
box 0.5500um -23.5300um 1.0500um -23.0300um
paint metal3
box -48.8500um -52.8500um -48.7500um -52.7500um
label VDD c metal4
box 2.2000um -185.0000um 3.4000um -184.6000um
paint metal3
box -7.4000um -175.4000um 3.4000um -175.0000um
paint metal3
box -6.6000um -153.0000um -4.6000um -152.6000um
paint metal3
box -29.0000um -145.8000um -22.2000um -145.4000um
paint metal3
box 4.6000um -89.0000um 5.8000um -88.6000um
paint metal3
box 4.6000um -83.4000um 5.8000um -83.0000um
paint metal3
box -50.6000um -77.8000um -48.6000um -77.4000um
paint metal3
box -5.8000um -68.2000um 1.0000um -67.8000um
paint metal3
box -55.4500um -65.8500um -54.9500um -65.3500um
paint metal4
box -50.6000um -77.8000um -50.2000um -66.2000um
paint metal4
box -49.0000um -77.8000um -48.6000um -75.8000um
paint metal4
box -46.6500um -75.4500um -46.1500um -74.9500um
paint metal4
box -32.2000um -113.0000um -31.8000um -87.8000um
paint metal4
box -29.0000um -145.8000um -28.6000um -112.6000um
paint metal4
box -22.6000um -145.8000um -22.2000um -141.4000um
paint metal4
box -22.6000um -96.2000um -22.2000um -87.8000um
paint metal4
box -20.2000um -156.2000um -19.8000um -151.8000um
paint metal4
box -7.4000um -175.4000um -7.0000um -174.2000um
paint metal4
box -6.6000um -153.0000um -6.2000um -151.8000um
paint metal4
box -5.8000um -68.2000um -5.4000um -66.2000um
paint metal4
box -5.0000um -175.4000um -4.6000um -141.4000um
paint metal4
box 0.6000um -68.2000um 1.0000um -66.2000um
paint metal4
box 2.2000um -185.0000um 2.6000um -183.0000um
paint metal4
box 3.0000um -185.0000um 3.4000um -175.0000um
paint metal4
box 4.6000um -89.0000um 5.0000um -87.8000um
paint metal4
box 4.6000um -84.2000um 5.0000um -75.8000um
paint metal4
box 5.4000um -94.6000um 5.8000um -83.0000um
paint metal4
box 22.2000um -75.4000um 22.6000um -66.2000um
paint metal4
box -7.4000um -175.4000um -7.0000um -175.0000um
paint via3
box 3.0000um -175.4000um 3.4000um -175.0000um
paint via3
box 5.4000um -89.0000um 5.8000um -88.6000um
paint via3
box -6.6000um -153.0000um -6.2000um -152.6000um
paint via3
box 4.6000um -83.4000um 5.0000um -83.0000um
paint via3
box -22.6000um -145.8000um -22.2000um -145.4000um
paint via3
box 4.6000um -89.0000um 5.0000um -88.6000um
paint via3
box 5.4000um -83.4000um 5.8000um -83.0000um
paint via3
box 3.0000um -185.0000um 3.4000um -184.6000um
paint via3
box -29.0000um -145.8000um -28.6000um -145.4000um
paint via3
box -5.0000um -153.0000um -4.6000um -152.6000um
paint via3
box -50.6000um -77.8000um -50.2000um -77.4000um
paint via3
box 0.6000um -68.2000um 1.0000um -67.8000um
paint via3
box -49.0000um -77.8000um -48.6000um -77.4000um
paint via3
box -5.8000um -68.2000um -5.4000um -67.8000um
paint via3
box -5.0000um -175.4000um -4.6000um -175.0000um
paint via3
box 2.2000um -185.0000um 2.6000um -184.6000um
paint via3
box 2.2000um -183.5700um 2.6000um -182.8900um
paint metal4
box 2.2000um -183.4600um 2.6000um -183.0600um
paint via3
box -7.4000um -174.7100um -7.0000um -174.0100um
paint metal4
box -7.4000um -174.5200um -7.0000um -174.1200um
paint via3
box -6.6000um -152.3100um -6.2000um -151.4800um
paint metal4
box -6.6000um -151.9900um -6.2000um -151.5900um
paint via3
box -20.2000um -152.3100um -19.8000um -151.4800um
paint metal4
box -20.2000um -151.9900um -19.8000um -151.5900um
paint via3
box -20.2000um -156.3100um -19.8000um -155.4500um
paint metal4
box -20.2000um -155.9600um -19.8000um -155.5600um
paint via3
box -5.0000um -142.0100um -4.6000um -141.2900um
paint metal4
box -5.0000um -141.9000um -4.6000um -141.5000um
paint via3
box -22.6000um -142.0100um -22.2000um -141.2900um
paint metal4
box -22.6000um -141.9000um -22.2000um -141.5000um
paint via3
box -29.0000um -143.5100um -28.6000um -142.5400um
paint metal4
box -29.0000um -143.0500um -28.6000um -142.6500um
paint via3
box -29.0000um -113.2600um -28.6000um -112.4900um
paint metal4
box -29.0000um -113.1500um -28.6000um -112.7500um
paint via3
box -32.2000um -113.2600um -31.8000um -112.4900um
paint metal4
box -32.2000um -113.1500um -31.8000um -112.7500um
paint via3
box -32.2000um -88.3100um -31.8000um -87.6000um
paint metal4
box -32.2000um -88.1100um -31.8000um -87.7100um
paint via3
box -22.6000um -88.3100um -22.2000um -87.6000um
paint metal4
box -22.6000um -88.1100um -22.2000um -87.7100um
paint via3
box -22.6000um -96.6900um -22.2000um -95.6900um
paint metal4
box -22.6000um -96.5800um -22.2000um -96.1800um
paint via3
box 4.6000um -88.3100um 5.0000um -87.6000um
paint metal4
box 4.6000um -88.1100um 5.0000um -87.7100um
paint via3
box 5.4000um -93.1100um 5.8000um -92.3200um
paint metal4
box 5.4000um -92.8300um 5.8000um -92.4300um
paint via3
box 5.4000um -94.7100um 5.8000um -93.8700um
paint metal4
box 5.4000um -94.3800um 5.8000um -93.9800um
paint via3
box 4.6000um -84.3300um 5.0000um -83.6900um
paint metal4
box 4.6000um -84.2200um 5.0000um -83.8200um
paint via3
box 4.6000um -76.3100um 5.0000um -75.5000um
paint metal4
box 4.6000um -76.0100um 5.0000um -75.6100um
paint via3
box -46.6000um -76.1200um -46.2000um -74.8900um
paint metal4
box -46.6000um -76.0100um -46.2000um -75.6100um
paint via3
box -46.6000um -75.5100um -46.2000um -74.7000um
paint metal4
box -46.6000um -75.2100um -46.2000um -74.8100um
paint via3
box 22.2000um -75.5100um 22.6000um -74.7000um
paint metal4
box 22.2000um -75.2100um 22.6000um -74.8100um
paint via3
box 22.2000um -66.7100um 22.6000um -65.8100um
paint metal4
box 22.2000um -66.3200um 22.6000um -65.9200um
paint via3
box 0.6000um -66.7100um 1.0000um -65.8100um
paint metal4
box 0.6000um -66.3200um 1.0000um -65.9200um
paint via3
box -5.8000um -66.7100um -5.4000um -65.8100um
paint metal4
box -5.8000um -66.3200um -5.4000um -65.9200um
paint via3
box -49.0000um -76.3100um -48.6000um -75.5000um
paint metal4
box -49.0000um -76.0100um -48.6000um -75.6100um
paint via3
box -50.6000um -66.7100um -50.2000um -65.8100um
paint metal4
box -50.6000um -66.3200um -50.2000um -65.9200um
paint via3
box -55.4000um -66.4300um -55.0000um -65.2900um
paint metal4
box -55.4000um -66.3200um -55.0000um -65.9200um
paint via3
box -55.4000um -65.9100um -55.0000um -65.0100um
paint metal4
box -55.4000um -65.5200um -55.0000um -65.1200um
paint via3
box 2.1500um -183.5100um 2.6500um -183.0100um
paint locali
box 2.2300um -183.4300um 2.5700um -183.0900um
paint mcon
box 2.2300um -183.4300um 2.5700um -183.0900um
paint m2c
box 2.2000um -183.4600um 2.6000um -183.0600um
paint m3c
box 2.1500um -183.5100um 2.6500um -183.0100um
paint metal3
box -7.4500um -174.5700um -6.9500um -174.0700um
paint locali
box -7.3700um -174.4900um -7.0300um -174.1500um
paint mcon
box -7.3700um -174.4900um -7.0300um -174.1500um
paint m2c
box -7.4000um -174.5200um -7.0000um -174.1200um
paint m3c
box -7.4500um -174.5700um -6.9500um -174.0700um
paint metal3
box -6.6500um -152.0400um -6.1500um -151.5400um
paint locali
box -6.5700um -151.9600um -6.2300um -151.6200um
paint mcon
box -6.5700um -151.9600um -6.2300um -151.6200um
paint m2c
box -6.6000um -151.9900um -6.2000um -151.5900um
paint m3c
box -6.6500um -152.0400um -6.1500um -151.5400um
paint metal3
box -20.2500um -152.0400um -19.7500um -151.5400um
paint locali
box -20.1700um -151.9600um -19.8300um -151.6200um
paint mcon
box -20.1700um -151.9600um -19.8300um -151.6200um
paint m2c
box -20.2000um -151.9900um -19.8000um -151.5900um
paint m3c
box -20.2500um -152.0400um -19.7500um -151.5400um
paint metal3
box -29.0500um -143.1000um -28.5500um -142.6000um
paint locali
box -28.9700um -143.0200um -28.6300um -142.6800um
paint mcon
box -28.9700um -143.0200um -28.6300um -142.6800um
paint m2c
box -29.0000um -143.0500um -28.6000um -142.6500um
paint m3c
box -29.0500um -143.1000um -28.5500um -142.6000um
paint metal3
box -22.6500um -96.6300um -22.1500um -96.1300um
paint locali
box -22.5700um -96.5500um -22.2300um -96.2100um
paint mcon
box -22.5700um -96.5500um -22.2300um -96.2100um
paint m2c
box -22.6000um -96.5800um -22.2000um -96.1800um
paint m3c
box -22.6500um -96.6300um -22.1500um -96.1300um
paint metal3
box 5.3500um -92.8800um 5.8500um -92.3800um
paint locali
box 5.4300um -92.8000um 5.7700um -92.4600um
paint mcon
box 5.4300um -92.8000um 5.7700um -92.4600um
paint m2c
box 5.4000um -92.8300um 5.8000um -92.4300um
paint m3c
box 5.3500um -92.8800um 5.8500um -92.3800um
paint metal3
box 4.5500um -84.2700um 5.0500um -83.7700um
paint locali
box 4.6300um -84.1900um 4.9700um -83.8500um
paint mcon
box 4.6300um -84.1900um 4.9700um -83.8500um
paint m2c
box 4.6000um -84.2200um 5.0000um -83.8200um
paint m3c
box 4.5500um -84.2700um 5.0500um -83.7700um
paint metal3
box 4.5500um -76.0600um 5.0500um -75.5600um
paint locali
box 4.6300um -75.9800um 4.9700um -75.6400um
paint mcon
box 4.6300um -75.9800um 4.9700um -75.6400um
paint m2c
box 4.6000um -76.0100um 5.0000um -75.6100um
paint m3c
box 4.5500um -76.0600um 5.0500um -75.5600um
paint metal3
box -46.6500um -76.0600um -46.1500um -75.5600um
paint locali
box -46.5700um -75.9800um -46.2300um -75.6400um
paint mcon
box -46.5700um -75.9800um -46.2300um -75.6400um
paint m2c
box -46.6000um -76.0100um -46.2000um -75.6100um
paint m3c
box -46.6500um -76.0600um -46.1500um -75.5600um
paint metal3
box 22.1500um -66.3700um 22.6500um -65.8700um
paint locali
box 22.2300um -66.2900um 22.5700um -65.9500um
paint mcon
box 22.2300um -66.2900um 22.5700um -65.9500um
paint m2c
box 22.2000um -66.3200um 22.6000um -65.9200um
paint m3c
box 22.1500um -66.3700um 22.6500um -65.8700um
paint metal3
box 0.5500um -66.3700um 1.0500um -65.8700um
paint locali
box 0.6300um -66.2900um 0.9700um -65.9500um
paint mcon
box 0.6300um -66.2900um 0.9700um -65.9500um
paint m2c
box 0.6000um -66.3200um 1.0000um -65.9200um
paint m3c
box 0.5500um -66.3700um 1.0500um -65.8700um
paint metal3
box -5.8500um -66.3700um -5.3500um -65.8700um
paint locali
box -5.7700um -66.2900um -5.4300um -65.9500um
paint mcon
box -5.7700um -66.2900um -5.4300um -65.9500um
paint m2c
box -5.8000um -66.3200um -5.4000um -65.9200um
paint m3c
box -5.8500um -66.3700um -5.3500um -65.8700um
paint metal3
box -49.0500um -76.0600um -48.5500um -75.5600um
paint locali
box -48.9700um -75.9800um -48.6300um -75.6400um
paint mcon
box -48.9700um -75.9800um -48.6300um -75.6400um
paint m2c
box -49.0000um -76.0100um -48.6000um -75.6100um
paint m3c
box -49.0500um -76.0600um -48.5500um -75.5600um
paint metal3
box -50.6500um -66.3700um -50.1500um -65.8700um
paint locali
box -50.5700um -66.2900um -50.2300um -65.9500um
paint mcon
box -50.5700um -66.2900um -50.2300um -65.9500um
paint m2c
box -50.6000um -66.3200um -50.2000um -65.9200um
paint m3c
box -50.6500um -66.3700um -50.1500um -65.8700um
paint metal3
box -55.4500um -66.3700um -54.9500um -65.8700um
paint locali
box -55.3700um -66.2900um -55.0300um -65.9500um
paint mcon
box -55.3700um -66.2900um -55.0300um -65.9500um
paint m2c
box -55.4000um -66.3200um -55.0000um -65.9200um
paint m3c
box -55.4500um -66.3700um -54.9500um -65.8700um
paint metal3
box 2.3500um -183.2500um 2.4500um -183.1500um
label VSS c metal4
box -38.6000um -79.4000um 10.6000um -79.0000um
paint metal3
box 46.2000um -79.4000um 77.0000um -79.0000um
paint metal3
box -38.6000um -80.2000um -38.2000um -79.0000um
paint metal4
box 10.2000um -80.2000um 10.6000um -79.0000um
paint metal4
box 46.2000um -80.2000um 46.6000um -79.0000um
paint metal4
box 76.6000um -141.8000um 77.0000um -79.0000um
paint metal4
box 76.6000um -79.4000um 77.0000um -79.0000um
paint via3
box 46.2000um -79.4000um 46.6000um -79.0000um
paint via3
box -38.6000um -79.4000um -38.2000um -79.0000um
paint via3
box 10.2000um -79.4000um 10.6000um -79.0000um
paint via3
box 76.6000um -142.0100um 77.0000um -141.2900um
paint metal4
box 76.6000um -141.9000um 77.0000um -141.5000um
paint via3
box 46.2000um -80.4300um 46.6000um -79.6900um
paint metal4
box 46.2000um -80.3200um 46.6000um -79.9200um
paint via3
box 10.2000um -80.4300um 10.6000um -79.6900um
paint metal4
box 10.2000um -80.3200um 10.6000um -79.9200um
paint via3
box -38.6000um -80.4300um -38.2000um -79.6900um
paint metal4
box -38.6000um -80.3200um -38.2000um -79.9200um
paint via3
box 76.7500um -141.6500um 76.8500um -141.5500um
label cmc c metal4
box -20.2500um -58.6500um -19.7500um -58.1500um
paint metal4
box -20.2000um -58.7100um -19.8000um -58.0400um
paint metal4
box -20.2000um -58.5500um -19.8000um -58.1500um
paint via3
box -20.0500um -58.4500um -19.9500um -58.3500um
label in c metal4
box -19.4500um -59.4500um -18.9500um -58.9500um
paint metal4
box -19.4000um -59.5100um -19.0000um -58.7900um
paint metal4
box -19.4000um -59.3000um -19.0000um -58.9000um
paint via3
box -19.2500um -59.2500um -19.1500um -59.1500um
label ip c metal4
tech revert
save iadc_ota_v2_routed
gds write iadc_ota_v2_routed
quit -noprompt
