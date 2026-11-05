drc off
snap internal
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng/nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng.gds
gds read /foss/designs/outputs/S3/_cells/nfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdfull_ng/nfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdfull_ng.gds
load x1_single_m4__f3 -silent
tech unlock *
box 0.000um 0.000um 0.000um 0.000um
getcell nfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdfull_ng
box 1.480um 0.000um 1.480um 0.000um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng
box 2.960um 0.000um 2.960um 0.000um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng
box 4.440um 0.000um 4.440um 0.000um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng
box 5.920um 0.000um 5.920um 0.000um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng h
box 7.400um 0.000um 7.400um 0.000um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng h
box 8.880um 0.000um 8.880um 0.000um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng h
box 10.360um 0.000um 10.360um 0.000um
getcell nfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdfull_ng
box 0.000um 5.670um 0.000um 5.670um
getcell nfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdfull_ng
box 1.480um 5.670um 1.480um 5.670um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng
box 2.960um 5.670um 2.960um 5.670um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng
box 4.440um 5.670um 4.440um 5.670um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng
box 5.920um 5.670um 5.920um 5.670um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng h
box 7.400um 5.670um 7.400um 5.670um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng h
box 8.880um 5.670um 8.880um 5.670um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng h
box 10.360um 5.670um 10.360um 5.670um
getcell nfet_01v8_W1p4_L0p6_m4__nf1_gtop_sdfull_ng
box 0.000um 12.090um 0.000um 12.090um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng
box 1.480um 12.090um 1.480um 12.090um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng
box 2.960um 12.090um 2.960um 12.090um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng
box 4.440um 12.090um 4.440um 12.090um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng
box 5.920um 12.090um 5.920um 12.090um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng h
box 7.400um 12.090um 7.400um 12.090um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng h
box 8.880um 12.090um 8.880um 12.090um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng h
box 10.360um 12.090um 10.360um 12.090um
getcell nfet_01v8_W1p4_L0p6_m18__nf1_gboth_sdfull_ng h
box 0.535um 1.720um 0.895um 2.080um
paint metal1
box 0.585um 1.740um 0.845um 2.060um
paint m2c
box 0.615um 1.900um 0.815um 2.870um
paint metal2
box 0.515um 2.670um 0.915um 3.070um
paint m3c
box 0.090um 0.130um 0.450um 0.490um
paint metal1
box 0.140um 0.150um 0.400um 0.470um
paint m2c
box 0.170um -0.550um 0.370um 0.310um
paint metal2
box 0.070um -0.750um 0.470um -0.350um
paint m3c
box 0.980um 0.130um 1.340um 0.490um
paint metal1
box 1.030um 0.150um 1.290um 0.470um
paint m2c
box 1.060um -0.550um 1.260um 0.310um
paint metal2
box 0.960um -0.750um 1.360um -0.350um
paint m3c
box 2.015um 2.050um 2.375um 2.410um
paint metal1
box 2.065um 2.070um 2.325um 2.390um
paint m2c
box 2.095um 2.230um 2.295um 3.620um
paint metal2
box 1.995um 3.420um 2.395um 3.820um
paint m3c
box 1.570um 0.460um 1.930um 0.820um
paint metal1
box 1.620um 0.480um 1.880um 0.800um
paint m2c
box 1.650um -0.550um 1.850um 0.640um
paint metal2
box 1.550um -0.750um 1.950um -0.350um
paint m3c
box 2.460um 0.460um 2.820um 0.820um
paint metal1
box 2.510um 0.480um 2.770um 0.800um
paint m2c
box 2.540um -1.300um 2.740um 0.640um
paint metal2
box 2.440um -1.500um 2.840um -1.100um
paint m3c
box 3.495um 2.050um 3.855um 2.410um
paint metal1
box 3.545um 2.070um 3.805um 2.390um
paint m2c
box 3.575um 2.230um 3.775um 3.620um
paint metal2
box 3.475um 3.420um 3.875um 3.820um
paint m3c
box 3.050um 0.460um 3.410um 0.820um
paint metal1
box 3.100um 0.480um 3.360um 0.800um
paint m2c
box 3.130um -0.550um 3.330um 0.640um
paint metal2
box 3.030um -0.750um 3.430um -0.350um
paint m3c
box 3.940um 0.460um 4.300um 0.820um
paint metal1
box 3.990um 0.480um 4.250um 0.800um
paint m2c
box 4.020um -1.300um 4.220um 0.640um
paint metal2
box 3.920um -1.500um 4.320um -1.100um
paint m3c
box 4.975um 2.050um 5.335um 2.410um
paint metal1
box 5.025um 2.070um 5.285um 2.390um
paint m2c
box 5.055um 2.230um 5.255um 3.620um
paint metal2
box 4.955um 3.420um 5.355um 3.820um
paint m3c
box 4.530um 0.460um 4.890um 0.820um
paint metal1
box 4.580um 0.480um 4.840um 0.800um
paint m2c
box 4.610um -0.550um 4.810um 0.640um
paint metal2
box 4.510um -0.750um 4.910um -0.350um
paint m3c
box 5.420um 0.460um 5.780um 0.820um
paint metal1
box 5.470um 0.480um 5.730um 0.800um
paint m2c
box 5.500um -1.300um 5.700um 0.640um
paint metal2
box 5.400um -1.500um 5.800um -1.100um
paint m3c
box 6.455um 2.050um 6.815um 2.410um
paint metal1
box 6.505um 2.070um 6.765um 2.390um
paint m2c
box 6.535um 2.230um 6.735um 3.620um
paint metal2
box 6.435um 3.420um 6.835um 3.820um
paint m3c
box 6.900um 0.460um 7.260um 0.820um
paint metal1
box 6.950um 0.480um 7.210um 0.800um
paint m2c
box 6.980um -0.550um 7.180um 0.640um
paint metal2
box 6.880um -0.750um 7.280um -0.350um
paint m3c
box 6.010um 0.460um 6.370um 0.820um
paint metal1
box 6.060um 0.480um 6.320um 0.800um
paint m2c
box 6.090um -1.300um 6.290um 0.640um
paint metal2
box 5.990um -1.500um 6.390um -1.100um
paint m3c
box 7.935um 2.050um 8.295um 2.410um
paint metal1
box 7.985um 2.070um 8.245um 2.390um
paint m2c
box 8.015um 2.230um 8.215um 3.620um
paint metal2
box 7.915um 3.420um 8.315um 3.820um
paint m3c
box 8.380um 0.460um 8.740um 0.820um
paint metal1
box 8.430um 0.480um 8.690um 0.800um
paint m2c
box 8.460um -0.550um 8.660um 0.640um
paint metal2
box 8.360um -0.750um 8.760um -0.350um
paint m3c
box 7.490um 0.460um 7.850um 0.820um
paint metal1
box 7.540um 0.480um 7.800um 0.800um
paint m2c
box 7.570um -1.300um 7.770um 0.640um
paint metal2
box 7.470um -1.500um 7.870um -1.100um
paint m3c
box 9.415um 2.050um 9.775um 2.410um
paint metal1
box 9.465um 2.070um 9.725um 2.390um
paint m2c
box 9.495um 2.230um 9.695um 3.620um
paint metal2
box 9.395um 3.420um 9.795um 3.820um
paint m3c
box 9.860um 0.460um 10.220um 0.820um
paint metal1
box 9.910um 0.480um 10.170um 0.800um
paint m2c
box 9.940um -0.550um 10.140um 0.640um
paint metal2
box 9.840um -0.750um 10.240um -0.350um
paint m3c
box 8.970um 0.460um 9.330um 0.820um
paint metal1
box 9.020um 0.480um 9.280um 0.800um
paint m2c
box 9.050um -1.300um 9.250um 0.640um
paint metal2
box 8.950um -1.500um 9.350um -1.100um
paint m3c
box 10.895um 1.720um 11.255um 2.080um
paint metal1
box 10.945um 1.740um 11.205um 2.060um
paint m2c
box 10.975um 1.900um 11.175um 2.870um
paint metal2
box 10.875um 2.670um 11.275um 3.070um
paint m3c
box 10.450um 0.130um 10.810um 0.490um
paint metal1
box 10.500um 0.150um 10.760um 0.470um
paint m2c
box 10.530um -0.550um 10.730um 0.310um
paint metal2
box 10.430um -0.750um 10.830um -0.350um
paint m3c
box 11.340um 0.130um 11.700um 0.490um
paint metal1
box 11.390um 0.150um 11.650um 0.470um
paint m2c
box 11.420um -0.550um 11.620um 0.310um
paint metal2
box 11.320um -0.750um 11.720um -0.350um
paint m3c
box 0.535um 7.390um 0.895um 7.750um
paint metal1
box 0.585um 7.410um 0.845um 7.730um
paint m2c
box 0.615um 7.570um 0.815um 8.540um
paint metal2
box 0.515um 8.340um 0.915um 8.740um
paint m3c
box 0.090um 5.800um 0.450um 6.160um
paint metal1
box 0.140um 5.820um 0.400um 6.140um
paint m2c
box 0.170um 5.120um 0.370um 5.980um
paint metal2
box 0.070um 4.920um 0.470um 5.320um
paint m3c
box 0.980um 5.800um 1.340um 6.160um
paint metal1
box 1.030um 5.820um 1.290um 6.140um
paint m2c
box 1.060um 5.120um 1.260um 5.980um
paint metal2
box 0.960um 4.920um 1.360um 5.320um
paint m3c
box 2.015um 7.720um 2.375um 8.080um
paint metal1
box 2.065um 7.740um 2.325um 8.060um
paint m2c
box 2.095um 7.900um 2.295um 9.290um
paint metal2
box 1.995um 9.090um 2.395um 9.490um
paint m3c
box 1.570um 6.130um 1.930um 6.490um
paint metal1
box 1.620um 6.150um 1.880um 6.470um
paint m2c
box 1.650um 5.120um 1.850um 6.310um
paint metal2
box 1.550um 4.920um 1.950um 5.320um
paint m3c
box 2.460um 6.130um 2.820um 6.490um
paint metal1
box 2.510um 6.150um 2.770um 6.470um
paint m2c
box 2.540um 4.370um 2.740um 6.310um
paint metal2
box 2.440um 4.170um 2.840um 4.570um
paint m3c
box 3.495um 7.720um 3.855um 8.080um
paint metal1
box 3.545um 7.740um 3.805um 8.060um
paint m2c
box 3.575um 7.900um 3.775um 9.290um
paint metal2
box 3.475um 9.090um 3.875um 9.490um
paint m3c
box 3.050um 6.130um 3.410um 6.490um
paint metal1
box 3.100um 6.150um 3.360um 6.470um
paint m2c
box 3.130um 5.120um 3.330um 6.310um
paint metal2
box 3.030um 4.920um 3.430um 5.320um
paint m3c
box 3.940um 6.130um 4.300um 6.490um
paint metal1
box 3.990um 6.150um 4.250um 6.470um
paint m2c
box 4.020um 4.370um 4.220um 6.310um
paint metal2
box 3.920um 4.170um 4.320um 4.570um
paint m3c
box 4.975um 7.720um 5.335um 8.080um
paint metal1
box 5.025um 7.740um 5.285um 8.060um
paint m2c
box 5.055um 7.900um 5.255um 9.290um
paint metal2
box 4.955um 9.090um 5.355um 9.490um
paint m3c
box 4.530um 6.130um 4.890um 6.490um
paint metal1
box 4.580um 6.150um 4.840um 6.470um
paint m2c
box 4.610um 5.120um 4.810um 6.310um
paint metal2
box 4.510um 4.920um 4.910um 5.320um
paint m3c
box 5.420um 6.130um 5.780um 6.490um
paint metal1
box 5.470um 6.150um 5.730um 6.470um
paint m2c
box 5.500um 4.370um 5.700um 6.310um
paint metal2
box 5.400um 4.170um 5.800um 4.570um
paint m3c
box 6.455um 7.720um 6.815um 8.080um
paint metal1
box 6.505um 7.740um 6.765um 8.060um
paint m2c
box 6.535um 7.900um 6.735um 9.290um
paint metal2
box 6.435um 9.090um 6.835um 9.490um
paint m3c
box 6.900um 6.130um 7.260um 6.490um
paint metal1
box 6.950um 6.150um 7.210um 6.470um
paint m2c
box 6.980um 5.120um 7.180um 6.310um
paint metal2
box 6.880um 4.920um 7.280um 5.320um
paint m3c
box 6.010um 6.130um 6.370um 6.490um
paint metal1
box 6.060um 6.150um 6.320um 6.470um
paint m2c
box 6.090um 4.370um 6.290um 6.310um
paint metal2
box 5.990um 4.170um 6.390um 4.570um
paint m3c
box 7.935um 7.720um 8.295um 8.080um
paint metal1
box 7.985um 7.740um 8.245um 8.060um
paint m2c
box 8.015um 7.900um 8.215um 9.290um
paint metal2
box 7.915um 9.090um 8.315um 9.490um
paint m3c
box 8.380um 6.130um 8.740um 6.490um
paint metal1
box 8.430um 6.150um 8.690um 6.470um
paint m2c
box 8.460um 5.120um 8.660um 6.310um
paint metal2
box 8.360um 4.920um 8.760um 5.320um
paint m3c
box 7.490um 6.130um 7.850um 6.490um
paint metal1
box 7.540um 6.150um 7.800um 6.470um
paint m2c
box 7.570um 4.370um 7.770um 6.310um
paint metal2
box 7.470um 4.170um 7.870um 4.570um
paint m3c
box 9.415um 7.720um 9.775um 8.080um
paint metal1
box 9.465um 7.740um 9.725um 8.060um
paint m2c
box 9.495um 7.900um 9.695um 9.290um
paint metal2
box 9.395um 9.090um 9.795um 9.490um
paint m3c
box 9.860um 6.130um 10.220um 6.490um
paint metal1
box 9.910um 6.150um 10.170um 6.470um
paint m2c
box 9.940um 5.120um 10.140um 6.310um
paint metal2
box 9.840um 4.920um 10.240um 5.320um
paint m3c
box 8.970um 6.130um 9.330um 6.490um
paint metal1
box 9.020um 6.150um 9.280um 6.470um
paint m2c
box 9.050um 4.370um 9.250um 6.310um
paint metal2
box 8.950um 4.170um 9.350um 4.570um
paint m3c
box 10.895um 7.390um 11.255um 7.750um
paint metal1
box 10.945um 7.410um 11.205um 7.730um
paint m2c
box 10.975um 7.570um 11.175um 8.540um
paint metal2
box 10.875um 8.340um 11.275um 8.740um
paint m3c
box 10.450um 5.800um 10.810um 6.160um
paint metal1
box 10.500um 5.820um 10.760um 6.140um
paint m2c
box 10.530um 5.120um 10.730um 5.980um
paint metal2
box 10.430um 4.920um 10.830um 5.320um
paint m3c
box 11.340um 5.800um 11.700um 6.160um
paint metal1
box 11.390um 5.820um 11.650um 6.140um
paint m2c
box 11.420um 5.120um 11.620um 5.980um
paint metal2
box 11.320um 4.920um 11.720um 5.320um
paint m3c
box 0.535um 14.140um 0.895um 14.500um
paint metal1
box 0.585um 14.160um 0.845um 14.480um
paint m2c
box 0.615um 14.320um 0.815um 14.960um
paint metal2
box 0.515um 14.760um 0.915um 15.160um
paint m3c
box 0.090um 12.550um 0.450um 12.910um
paint metal1
box 0.140um 12.570um 0.400um 12.890um
paint m2c
box 0.170um 11.540um 0.370um 12.730um
paint metal2
box 0.070um 11.340um 0.470um 11.740um
paint m3c
box 0.980um 12.550um 1.340um 12.910um
paint metal1
box 1.030um 12.570um 1.290um 12.890um
paint m2c
box 1.060um 11.540um 1.260um 12.730um
paint metal2
box 0.960um 11.340um 1.360um 11.740um
paint m3c
box 2.015um 14.140um 2.375um 14.500um
paint metal1
box 2.065um 14.160um 2.325um 14.480um
paint m2c
box 2.095um 14.320um 2.295um 15.710um
paint metal2
box 1.995um 15.510um 2.395um 15.910um
paint m3c
box 1.570um 12.550um 1.930um 12.910um
paint metal1
box 1.620um 12.570um 1.880um 12.890um
paint m2c
box 1.650um 10.790um 1.850um 12.730um
paint metal2
box 1.550um 10.590um 1.950um 10.990um
paint m3c
box 2.460um 12.550um 2.820um 12.910um
paint metal1
box 2.510um 12.570um 2.770um 12.890um
paint m2c
box 2.540um 10.040um 2.740um 12.730um
paint metal2
box 2.440um 9.840um 2.840um 10.240um
paint m3c
box 3.495um 14.140um 3.855um 14.500um
paint metal1
box 3.545um 14.160um 3.805um 14.480um
paint m2c
box 3.575um 14.320um 3.775um 15.710um
paint metal2
box 3.475um 15.510um 3.875um 15.910um
paint m3c
box 3.050um 12.550um 3.410um 12.910um
paint metal1
box 3.100um 12.570um 3.360um 12.890um
paint m2c
box 3.130um 10.790um 3.330um 12.730um
paint metal2
box 3.030um 10.590um 3.430um 10.990um
paint m3c
box 3.940um 12.550um 4.300um 12.910um
paint metal1
box 3.990um 12.570um 4.250um 12.890um
paint m2c
box 4.020um 10.040um 4.220um 12.730um
paint metal2
box 3.920um 9.840um 4.320um 10.240um
paint m3c
box 4.975um 14.140um 5.335um 14.500um
paint metal1
box 5.025um 14.160um 5.285um 14.480um
paint m2c
box 5.055um 14.320um 5.255um 15.710um
paint metal2
box 4.955um 15.510um 5.355um 15.910um
paint m3c
box 4.530um 12.550um 4.890um 12.910um
paint metal1
box 4.580um 12.570um 4.840um 12.890um
paint m2c
box 4.610um 10.790um 4.810um 12.730um
paint metal2
box 4.510um 10.590um 4.910um 10.990um
paint m3c
box 5.420um 12.550um 5.780um 12.910um
paint metal1
box 5.470um 12.570um 5.730um 12.890um
paint m2c
box 5.500um 10.040um 5.700um 12.730um
paint metal2
box 5.400um 9.840um 5.800um 10.240um
paint m3c
box 6.455um 14.140um 6.815um 14.500um
paint metal1
box 6.505um 14.160um 6.765um 14.480um
paint m2c
box 6.535um 14.320um 6.735um 15.710um
paint metal2
box 6.435um 15.510um 6.835um 15.910um
paint m3c
box 6.900um 12.550um 7.260um 12.910um
paint metal1
box 6.950um 12.570um 7.210um 12.890um
paint m2c
box 6.980um 10.790um 7.180um 12.730um
paint metal2
box 6.880um 10.590um 7.280um 10.990um
paint m3c
box 6.010um 12.550um 6.370um 12.910um
paint metal1
box 6.060um 12.570um 6.320um 12.890um
paint m2c
box 6.090um 10.040um 6.290um 12.730um
paint metal2
box 5.990um 9.840um 6.390um 10.240um
paint m3c
box 7.935um 14.140um 8.295um 14.500um
paint metal1
box 7.985um 14.160um 8.245um 14.480um
paint m2c
box 8.015um 14.320um 8.215um 15.710um
paint metal2
box 7.915um 15.510um 8.315um 15.910um
paint m3c
box 8.380um 12.550um 8.740um 12.910um
paint metal1
box 8.430um 12.570um 8.690um 12.890um
paint m2c
box 8.460um 10.790um 8.660um 12.730um
paint metal2
box 8.360um 10.590um 8.760um 10.990um
paint m3c
box 7.490um 12.550um 7.850um 12.910um
paint metal1
box 7.540um 12.570um 7.800um 12.890um
paint m2c
box 7.570um 10.040um 7.770um 12.730um
paint metal2
box 7.470um 9.840um 7.870um 10.240um
paint m3c
box 9.415um 14.140um 9.775um 14.500um
paint metal1
box 9.465um 14.160um 9.725um 14.480um
paint m2c
box 9.495um 14.320um 9.695um 15.710um
paint metal2
box 9.395um 15.510um 9.795um 15.910um
paint m3c
box 9.860um 12.550um 10.220um 12.910um
paint metal1
box 9.910um 12.570um 10.170um 12.890um
paint m2c
box 9.940um 10.790um 10.140um 12.730um
paint metal2
box 9.840um 10.590um 10.240um 10.990um
paint m3c
box 8.970um 12.550um 9.330um 12.910um
paint metal1
box 9.020um 12.570um 9.280um 12.890um
paint m2c
box 9.050um 10.040um 9.250um 12.730um
paint metal2
box 8.950um 9.840um 9.350um 10.240um
paint m3c
box 10.895um 14.140um 11.255um 14.500um
paint metal1
box 10.945um 14.160um 11.205um 14.480um
paint m2c
box 10.975um 14.320um 11.175um 14.960um
paint metal2
box 10.875um 14.760um 11.275um 15.160um
paint m3c
box 11.340um 12.550um 11.700um 12.910um
paint metal1
box 11.390um 12.570um 11.650um 12.890um
paint m2c
box 11.420um 11.540um 11.620um 12.730um
paint metal2
box 11.320um 11.340um 11.720um 11.740um
paint m3c
box 10.450um 12.550um 10.810um 12.910um
paint metal1
box 10.500um 12.570um 10.760um 12.890um
paint m2c
box 10.530um 11.540um 10.730um 12.730um
paint metal2
box 10.430um 11.340um 10.830um 11.740um
paint m3c
box 12.090um -1.300um 12.290um 10.040um
paint metal2
box 11.990um -1.500um 12.390um -1.100um
paint m3c
box 11.990um 4.170um 12.390um 4.570um
paint m3c
box 11.990um 9.840um 12.390um 10.240um
paint m3c
box 12.690um -0.550um 12.890um 10.790um
paint metal2
box 12.590um -0.750um 12.990um -0.350um
paint m3c
box 12.590um 2.670um 12.990um 3.070um
paint m3c
box 12.590um 4.920um 12.990um 5.320um
paint m3c
box 12.590um 8.340um 12.990um 8.740um
paint m3c
box 12.590um 10.590um 12.990um 10.990um
paint m3c
box 13.290um 3.620um 13.490um 15.710um
paint metal2
box 13.190um 3.420um 13.590um 3.820um
paint m3c
box 13.190um 9.090um 13.590um 9.490um
paint m3c
box 13.190um 15.510um 13.590um 15.910um
paint m3c
box 13.890um 11.540um 14.090um 14.960um
paint metal2
box 13.790um 11.340um 14.190um 11.740um
paint m3c
box 13.790um 14.760um 14.190um 15.160um
paint m3c
box -0.400um 14.760um 14.390um 15.160um
paint metal3
box -0.300um 14.910um -0.200um 15.010um
label VSS c metal3
box -0.400um 15.510um 14.390um 15.910um
paint metal3
box -0.300um 15.660um -0.200um 15.760um
label bias_d c metal3
box -0.400um -0.750um 14.390um -0.350um
paint metal3
box -0.300um -0.600um -0.200um -0.500um
label bias_a c metal3
box -0.400um -1.500um 14.390um -1.100um
paint metal3
box -0.300um -1.350um -0.200um -1.250um
label x1_m5d c metal3
box -0.100um 2.670um 13.090um 3.070um
paint metal3
box -0.100um 3.420um 13.690um 3.820um
paint metal3
box -0.100um 4.920um 13.090um 5.320um
paint metal3
box -0.100um 4.170um 12.490um 4.570um
paint metal3
box -0.100um 8.340um 13.090um 8.740um
paint metal3
box -0.100um 9.090um 13.690um 9.490um
paint metal3
box -0.100um 11.340um 14.290um 11.740um
paint metal3
box -0.100um 10.590um 13.090um 10.990um
paint metal3
box -0.100um 9.840um 12.490um 10.240um
paint metal3
box -0.400um -2.100um 14.390um 16.110um
sky130::guard_ring_draw psc psd
box 6.945um -2.150um 7.045um -2.050um
label VSS_body c locali
tech revert
save x1_single_m4__f3
gds write x1_single_m4__f3
quit -noprompt
