.subckt ota5t vdd outp inp inn vss vbias
M3 net3 net3 vdd vdd sky130_fd_pr__pfet_01v8 L=1e-6 w=2.1e-6 nf=4
M4 outp net3 vdd vdd sky130_fd_pr__pfet_01v8 L=1e-6 w=2.1e-6 nf=4
M1 net3 inp net1 vss sky130_fd_pr__nfet_01v8 L=0.5e-6 w=0.63e-6 nf=38
M2 outp inn net1 vss sky130_fd_pr__nfet_01v8 L=0.5e-6 w=0.63e-6 nf=38
M5 net1 vbias vss vss sky130_fd_pr__nfet_01v8 L=1e-6 w=0.63e-6 nf=38
.ends ota5t
