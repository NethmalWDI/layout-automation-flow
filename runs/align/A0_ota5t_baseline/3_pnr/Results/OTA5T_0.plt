#Use this file as a script for gnuplot
#(See http://www.gnuplot.info/ for details)

set title" #Blocks= 3, #Terminals= 4, #Nets= 6,Area=2.28856e+09, HPWL= 374300 "

set nokey
#   Uncomment these two lines starting with "set"
#   to save an EPS file for inclusion into a latex document
# set terminal postscript eps color solid 20
# set output "result.eps"

#   Uncomment these two lines starting with "set"
#   to save a PS file for printing
# set terminal postscript portrait color solid 20
# set output "result.ps"


set xrange [-50:75730]

set yrange [-50:30290]

set label "X_M3_M4" at 41280 , 22680 center 

set label "DA" at 40420 , 20160


set label "DB" at 41280 , 16800


set label "S" at 42140 , 23100


set label "X_M1_M2" at 41280 , 7560 center 

set label "B" at 41280 , 1680


set label "DA" at 42140 , 14280


set label "DB" at 40420 , 13440


set label "GA" at 42140 , 5880


set label "GB" at 40420 , 5040


set label "S" at 41280 , 12600


set label "X_M5" at 18060 , 22680 center 

set label "D" at 18060 , 15960


set label "G" at 18060 , 24360


set label "S" at 18920 , 22680


set label "OUTP" at 41280 , 30240 center                

set label "INP" at 42140 , 0 center                

set label "INN" at 40420 , 0 center                

set label "VBIAS" at 18060 , 30240 center                

plot[:][:] '-' with lines linestyle 3, '-' with lines linestyle 7, '-' with lines linestyle 1, '-' with lines linestyle 0

# block X_M3_M4 select 0 bsize 4
	36120	15120
	36120	30240
	46440	30240
	46440	15120
	36120	15120

# block X_M1_M2 select 0 bsize 4
	6880	0
	6880	15120
	75680	15120
	75680	0
	6880	0

# block X_M5 select 0 bsize 4
	0	15120
	0	30240
	36120	30240
	36120	15120
	0	15120


EOF
	40140	15640
	40140	24680
	40700	24680
	40700	15640
	40140	15640

	40080	16520
	40080	17080
	42480	17080
	42480	16520
	40080	16520

	41860	17320
	41860	28880
	42420	28880
	42420	17320
	41860	17320

	73440	1960
	73440	1400
	9120	1400
	9120	1960
	73440	1960

	73440	14560
	73440	14000
	10840	14000
	10840	14560
	73440	14560

	71720	13720
	71720	13160
	9120	13160
	9120	13720
	71720	13720

	73440	6160
	73440	5600
	10840	5600
	10840	6160
	73440	6160

	71720	5320
	71720	4760
	9120	4760
	9120	5320
	71720	5320

	74300	12880
	74300	12320
	8260	12320
	8260	12880
	74300	12880

	2240	15680
	2240	16240
	33880	16240
	33880	15680
	2240	15680

	2240	24080
	2240	24640
	33880	24640
	33880	24080
	2240	24080

	18640	16480
	18640	28880
	19200	28880
	19200	16480
	18640	16480


EOF

	41280	30240
	41280	30240
	41280	30240
	41280	30240
	41280	30240

	42140	0
	42140	0
	42140	0
	42140	0
	42140	0

	40420	0
	40420	0
	40420	0
	40420	0
	40420	0

	18060	30240
	18060	30240
	18060	30240
	18060	30240
	18060	30240

EOF

#Net: NET3
	40420	20160
	42140	14280
	40420	20160


#Net: OUTP
	41280	16800
	40420	13440
	41280	16800

	41280	16800
	41280	30240
	41280	16800


#Net: INP
	42140	5880
	42140	0
	42140	5880


#Net: INN
	40420	5040
	40420	0
	40420	5040


#Net: NET1
	41280	12600
	18060	15960
	41280	12600


#Net: VBIAS
	18060	24360
	18060	30240
	18060	24360


EOF

pause -1 'Press any key'