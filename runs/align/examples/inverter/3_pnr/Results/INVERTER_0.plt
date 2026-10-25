#Use this file as a script for gnuplot
#(See http://www.gnuplot.info/ for details)

set title" #Blocks= 1, #Terminals= 4, #Nets= 4,Area=1.57194e+09, HPWL= 119040 "

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

set label "X_MN0_MP0" at 14620 , 26880 center 

set label "I" at 14620 , 11760


set label "I" at 14620 , 42000


set label "SN" at 15480 , 13440


set label "SP" at 15480 , 40320


set label "ZN" at 13760 , 20160


set label "ZN" at 13760 , 33600


set label "IN" at 14620 , 0 center                

set label "VSS" at 15480 , 0 center                

set label "VDD" at 15480 , 53760 center                

set label "OUT" at 0 , 20160 center                

plot[:][:] '-' with lines linestyle 3, '-' with lines linestyle 7, '-' with lines linestyle 1, '-' with lines linestyle 0

# block X_MN0_MP0 select 0 bsize 4
	0	0
	0	53760
	29240	53760
	29240	0
	0	0


EOF
	14340	5560
	14340	17960
	14900	17960
	14900	5560
	14340	5560

	14340	35800
	14340	48200
	14900	48200
	14900	35800
	14340	35800

	15200	1360
	15200	25520
	15760	25520
	15760	1360
	15200	1360

	15200	28240
	15200	52400
	15760	52400
	15760	28240
	15200	28240

	13480	13960
	13480	26360
	14040	26360
	14040	13960
	13480	13960

	13480	27400
	13480	39800
	14040	39800
	14040	27400
	13480	27400


EOF

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

	0	20160
	0	20160
	0	20160
	0	20160
	0	20160

EOF

#Net: IN
	14620	11760
	14620	0
	14620	11760


#Net: VSS
	15480	13440
	15480	0
	15480	13440


#Net: VDD
	15480	40320
	15480	53760
	15480	40320


#Net: OUT
	13760	20160
	0	20160
	13760	20160


EOF

pause -1 'Press any key'