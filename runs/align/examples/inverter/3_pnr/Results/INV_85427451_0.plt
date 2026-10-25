#Use this file as a script for gnuplot
#(See http://www.gnuplot.info/ for details)

set title" #Blocks= 2, #Terminals= 4, #Nets= 4,Area=1.57194e+09, HPWL= 119040 "

set nokey
#   Uncomment these two lines starting with "set"
#   to save an EPS file for inclusion into a latex document
# set terminal postscript eps color solid 20
# set output "result.eps"

#   Uncomment these two lines starting with "set"
#   to save a PS file for printing
# set terminal postscript portrait color solid 20
# set output "result.ps"


set xrange [-50:29290]

set yrange [-50:53810]

set label "X_M0" at 14620 , 13440 center 

set label "D" at 13760 , 20160


set label "G" at 14620 , 11760


set label "S" at 15480 , 13440


set label "X_M1" at 14620 , 40320 center 

set label "D" at 13760 , 33600


set label "G" at 14620 , 42000


set label "S" at 15480 , 40320


set label "ZN" at 0 , 20160 center                

set label "I" at 14620 , 0 center                

set label "SN" at 15480 , 0 center                

set label "SP" at 15480 , 53760 center                

plot[:][:] '-' with lines linestyle 3, '-' with lines linestyle 7, '-' with lines linestyle 1, '-' with lines linestyle 0

# block X_M0 select 3 bsize 4
	0	0
	0	26880
	29240	26880
	29240	0
	0	0

# block X_M1 select 3 bsize 4
	0	26880
	0	53760
	29240	53760
	29240	26880
	0	26880


EOF
	13480	26360
	13480	13960
	14040	13960
	14040	26360
	13480	26360

	14340	17960
	14340	5560
	14900	5560
	14900	17960
	14340	17960

	15200	25520
	15200	1360
	15760	1360
	15760	25520
	15200	25520

	13480	27400
	13480	39800
	14040	39800
	14040	27400
	13480	27400

	14340	35800
	14340	48200
	14900	48200
	14900	35800
	14340	35800

	15200	28240
	15200	52400
	15760	52400
	15760	28240
	15200	28240


EOF

	0	20160
	0	20160
	0	20160
	0	20160
	0	20160

	14620	0
	14620	0
	14620	0
	14620	0
	14620	0

	15480	0
	15480	0
	15480	0
	15480	0
	15480	0

	15480	53760
	15480	53760
	15480	53760
	15480	53760
	15480	53760

EOF

#Net: ZN
	13760	20160
	13760	33600
	13760	20160

	13760	20160
	0	20160
	13760	20160


#Net: I
	14620	11760
	14620	42000
	14620	11760

	14620	11760
	14620	0
	14620	11760


#Net: SN
	15480	13440
	15480	0
	15480	13440


#Net: SP
	15480	40320
	15480	53760
	15480	40320


EOF

pause -1 'Press any key'