#Use this file as a script for gnuplot
#(See http://www.gnuplot.info/ for details)

set title" #Blocks= 1, #Terminals= 4, #Nets= 4,Area=7.28179e+08, HPWL= 82960 "

set nokey
#   Uncomment these two lines starting with "set"
#   to save an EPS file for inclusion into a latex document
# set terminal postscript eps color solid 20
# set output "result.eps"

#   Uncomment these two lines starting with "set"
#   to save a PS file for printing
# set terminal postscript portrait color solid 20
# set output "result.ps"


set xrange [-50:24130]

set yrange [-50:30290]

set label "X_MN0_MN1_MP0_MP1" at 12040 , 15120 center 

set label "SN" at 17200 , 7560


set label "SN" at 6880 , 7560


set label "SP" at 17200 , 22680


set label "SP" at 6880 , 22680


set label "VI" at 18060 , 5880


set label "VI" at 18060 , 24360


set label "VO" at 6020 , 14280


set label "VO" at 6020 , 15960


set label "VSS" at 24080 , 7560 center                

set label "VDD" at 24080 , 22680 center                

set label "IN" at 18060 , 0 center                

set label "OUT" at 0 , 14280 center                

plot[:][:] '-' with lines linestyle 3, '-' with lines linestyle 7, '-' with lines linestyle 1, '-' with lines linestyle 0

# block X_MN0_MN1_MP0_MP1 select 0 bsize 4
	0	0
	0	30240
	24080	30240
	24080	0
	0	0


EOF
	16920	1360
	16920	13760
	17480	13760
	17480	1360
	16920	1360

	6600	1360
	6600	13760
	7160	13760
	7160	1360
	6600	1360

	16920	16480
	16920	28880
	17480	28880
	17480	16480
	16920	16480

	6600	16480
	6600	28880
	7160	28880
	7160	16480
	6600	16480

	14280	5600
	14280	6160
	21840	6160
	21840	5600
	14280	5600

	14280	24080
	14280	24640
	21840	24640
	21840	24080
	14280	24080

	2240	14000
	2240	14560
	9800	14560
	9800	14000
	2240	14000

	2240	15680
	2240	16240
	9800	16240
	9800	15680
	2240	15680


EOF

	24080	7560
	24080	7560
	24080	7560
	24080	7560
	24080	7560

	24080	22680
	24080	22680
	24080	22680
	24080	22680
	24080	22680

	18060	0
	18060	0
	18060	0
	18060	0
	18060	0

	0	14280
	0	14280
	0	14280
	0	14280
	0	14280

EOF

#Net: VSS
	17200	7560
	24080	7560
	17200	7560


#Net: VDD
	17200	22680
	24080	22680
	17200	22680


#Net: IN
	18060	5880
	18060	0
	18060	5880


#Net: OUT
	6020	14280
	0	14280
	6020	14280


EOF

pause -1 'Press any key'