#Use this file as a script for gnuplot
#(See http://www.gnuplot.info/ for details)

set title" #Blocks= 4, #Terminals= 4, #Nets= 5,Area=7.28179e+08, HPWL= 121600 "

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

set label "X_M0" at 18060 , 7560 center 

set label "D" at 18060 , 14280


set label "G" at 18060 , 5880


set label "S" at 17200 , 7560


set label "X_M2" at 6020 , 7560 center 

set label "D" at 6020 , 14280


set label "G" at 6020 , 5880


set label "S" at 6880 , 7560


set label "X_M1" at 18060 , 22680 center 

set label "D" at 18060 , 15960


set label "G" at 18060 , 24360


set label "S" at 17200 , 22680


set label "X_M3" at 6020 , 22680 center 

set label "D" at 6020 , 15960


set label "G" at 6020 , 24360


set label "S" at 6880 , 22680


set label "VI" at 18060 , 0 center                

set label "SN" at 24080 , 7560 center                

set label "VO" at 0 , 14280 center                

set label "SP" at 24080 , 22680 center                

plot[:][:] '-' with lines linestyle 3, '-' with lines linestyle 7, '-' with lines linestyle 1, '-' with lines linestyle 0

# block X_M0 select 0 bsize 4
	12040	0
	12040	15120
	24080	15120
	24080	0
	12040	0

# block X_M2 select 0 bsize 4
	0	0
	0	15120
	12040	15120
	12040	0
	0	0

# block X_M1 select 0 bsize 4
	12040	15120
	12040	30240
	24080	30240
	24080	15120
	12040	15120

# block X_M3 select 0 bsize 4
	0	15120
	0	30240
	12040	30240
	12040	15120
	0	15120


EOF
	21840	14560
	21840	14000
	14280	14000
	14280	14560
	21840	14560

	21840	6160
	21840	5600
	14280	5600
	14280	6160
	21840	6160

	17480	13760
	17480	1360
	16920	1360
	16920	13760
	17480	13760

	2240	14560
	2240	14000
	9800	14000
	9800	14560
	2240	14560

	2240	6160
	2240	5600
	9800	5600
	9800	6160
	2240	6160

	6600	13760
	6600	1360
	7160	1360
	7160	13760
	6600	13760

	21840	15680
	21840	16240
	14280	16240
	14280	15680
	21840	15680

	21840	24080
	21840	24640
	14280	24640
	14280	24080
	21840	24080

	17480	16480
	17480	28880
	16920	28880
	16920	16480
	17480	16480

	2240	15680
	2240	16240
	9800	16240
	9800	15680
	2240	15680

	2240	24080
	2240	24640
	9800	24640
	9800	24080
	2240	24080

	6600	16480
	6600	28880
	7160	28880
	7160	16480
	6600	16480


EOF

	18060	0
	18060	0
	18060	0
	18060	0
	18060	0

	24080	7560
	24080	7560
	24080	7560
	24080	7560
	24080	7560

	0	14280
	0	14280
	0	14280
	0	14280
	0	14280

	24080	22680
	24080	22680
	24080	22680
	24080	22680
	24080	22680

EOF

#Net: VM
	18060	14280
	6020	5880
	18060	14280

	18060	14280
	18060	15960
	18060	14280

	18060	14280
	6020	24360
	18060	14280


#Net: VI
	18060	5880
	18060	24360
	18060	5880

	18060	5880
	18060	0
	18060	5880


#Net: SN
	17200	7560
	6880	7560
	17200	7560

	17200	7560
	24080	7560
	17200	7560


#Net: VO
	6020	14280
	6020	15960
	6020	14280

	6020	14280
	0	14280
	6020	14280


#Net: SP
	17200	22680
	6880	22680
	17200	22680

	17200	22680
	24080	22680
	17200	22680


EOF

pause -1 'Press any key'