drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_W24_L1_m1__nf2_gtop_sdfull_outD_ng/nfet_01v8_W24_L1_m1__nf2_gtop_sdfull_outD_ng.gds
load nmos_current_mirror_bias__A -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_W24_L1_m1__nf2_gtop_sdfull_outD_ng
box 1.255um 12.320um 1.615um 12.680um
paint metal1
box 1.305um 12.340um 1.565um 12.660um
paint m2c
box 1.335um 12.500um 1.535um 14.490um
paint metal2
box 1.235um 14.290um 1.635um 14.690um
paint m3c
box 1.335um -1.000um 1.535um 0.280um
paint metal2
box 1.235um -1.200um 1.635um -0.800um
paint m3c
box 0.170um 11.980um 0.370um 13.590um
paint metal2
box 0.070um 13.390um 0.470um 13.790um
paint m3c
box -1.800um 13.390um 4.920um 13.790um
paint metal3
box -1.700um 13.540um -1.600um 13.640um
label VSS c metal3
box -1.800um 14.290um 4.920um 14.690um
paint metal3
box -1.700um 14.440um -1.600um 14.540um
label net2 c metal3
box -1.800um -1.200um 4.920um -0.800um
paint metal3
box -1.700um -1.050um -1.600um -0.950um
label net1 c metal3
box -0.800um -1.800um 3.920um 15.290um
sky130::guard_ring_draw psc psd
box 1.510um -1.850um 1.610um -1.750um
label VSS_body c locali
tech revert
save nmos_current_mirror_bias__A
gds write nmos_current_mirror_bias__A
quit -noprompt
