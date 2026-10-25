#Use this file as a script for gnuplot
#(See http://www.gnuplot.info/ for details)

set title" #Blocks= 3, #Terminals= 4, #Nets= 6,Area=3.79116e+09, HPWL= 168720 "

set nokey
#   Uncomment these two lines starting with "set"
#   to save an EPS file for inclusion into a latex document
# set terminal postscript eps color solid 20
# set output "result.eps"

#   Uncomment these two lines starting with "set"
#   to save a PS file for printing
# set terminal postscript portrait color solid 20
# set output "result.ps"


set xrange [-50:55090]

set yrange [-50:68930]

set label "X_M4_M5" at 27520 , 7560 center 

set label "DA" at 28380 , 10080


set label "DB" at 24940 , 13440


set label "S" at 26660 , 7140


set label "X_M1_M2" at 27520 , 55440 center 

set label "DA" at 26660 , 52920


set label "DB" at 27520 , 49560


set label "S" at 28380 , 55860


set label "X_M0_M3" at 27520 , 28560 center 

set label "B" at 27520 , 16800


set label "DA" at 25800 , 35280


set label "DB" at 26660 , 34440


set label "GA" at 27520 , 26880


set label "GB" at 28380 , 26040


set label "S" at 29240 , 33600


set label "ID" at 28380 , 0 center                

set label "VOUT" at 27520 , 68880 center                

set label "VINP" at 27520 , 0 center                

set label "VINN" at 28380 , 0 center                

plot[:][:] '-' with lines linestyle 3, '-' with lines linestyle 7, '-' with lines linestyle 1, '-' with lines linestyle 0

# block X_M4_M5 select 0 bsize 4
	0	0
	0	15120
	55040	15120
	55040	0
	0	0

# block X_M1_M2 select 0 bsize 4
	0	42000
	0	68880
	55040	68880
	55040	42000
	0	42000

# block X_M0_M3 select 0 bsize 4
	0	15120
	0	42000
	55040	42000
	55040	15120
	0	15120


EOF
	28660	14600
	28660	5560
	28100	5560
	28100	14600
	28660	14600

	45920	13720
	45920	13160
	3960	13160
	3960	13720
	45920	13720

	26940	12920
	26940	1360
	26380	1360
	26380	12920
	26940	12920

	26380	42520
	26380	63320
	26940	63320
	26940	42520
	26380	42520

	27240	43360
	27240	55760
	27800	55760
	27800	43360
	27240	43360

	28100	44200
	28100	67520
	28660	67520
	28660	44200
	28100	44200

	3960	17080
	3960	16520
	51080	16520
	51080	17080
	3960	17080

	25520	41480
	25520	29080
	26080	29080
	26080	41480
	25520	41480

	26380	40640
	26380	28240
	26940	28240
	26940	40640
	26380	40640

	27240	33080
	27240	20680
	27800	20680
	27800	33080
	27240	33080

	28100	32240
	28100	19840
	28660	19840
	28660	32240
	28100	32240

	28960	39800
	28960	27400
	29520	27400
	29520	39800
	28960	39800


EOF

	28380	0
	28380	0
	28380	0
	28380	0
	28380	0

	27520	68880
	27520	68880
	27520	68880
	27520	68880
	27520	68880

	27520	0
	27520	0
	27520	0
	27520	0
	27520	0

	28380	0
	28380	0
	28380	0
	28380	0
	28380	0

EOF

#Net: ID
	28380	10080
	28380	0
	28380	10080


#Net: SOURCE
	24940	13440
	29240	33600
	24940	13440


#Net: NET8
	26660	52920
	25800	35280
	26660	52920


#Net: VOUT
	27520	49560
	26660	34440
	27520	49560

	27520	49560
	27520	68880
	27520	49560


#Net: VINP
	27520	26880
	27520	0
	27520	26880


#Net: VINN
	28380	26040
	28380	0
	28380	26040


EOF

pause -1 'Press any key'