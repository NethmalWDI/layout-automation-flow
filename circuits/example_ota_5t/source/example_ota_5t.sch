v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -150 -30 -150 0 {lab=#net1}
N -150 0 0 0 {lab=#net1}
N 0 0 150 0 {lab=#net1}
N 150 -30 150 0 {lab=#net1}
N -150 -240 -150 -210 {lab=VDD}
N 150 -240 150 -210 {lab=VDD}
N -150 -60 -90 -60 {lab=VSS}
N -0 0 -0 30 {lab=#net1}
N 0 60 50 60 {lab=VSS}
N 50 60 80 60 {lab=VSS}
N 0 120 80 120 {lab=VSS}
N 80 60 80 120 {lab=VSS}
N 0 90 0 120 {lab=VSS}
N 0 120 0 150 {lab=VSS}
N -90 60 -40 60 {lab=#net2}
N -240 -60 -190 -60 {lab=INP}
N 190 -60 240 -60 {lab=INN}
N -90 60 -90 70 {lab=#net2}
N -90 140 -90 150 {lab=VSS}
N -90 70 -90 80 {lab=#net2}
N -90 -60 -70 -60 {lab=VSS}
N 90 -60 150 -60 {lab=VSS}
N 70 -60 90 -60 {lab=VSS}
N 150 -120 150 -90 {lab=OUTP}
N -150 -120 -150 -90 {lab=#net3}
N 150 -120 200 -120 {lab=OUTP}
N 150 -150 150 -120 {lab=OUTP}
N -150 -150 -150 -120 {lab=#net3}
N -110 -180 110 -180 {lab=#net3}
N -150 -120 -70 -120 {lab=#net3}
N -70 -180 -70 -120 {lab=#net3}
N -200 -180 -150 -180 {lab=VDD}
N -230 -180 -200 -180 {lab=VDD}
N -230 -240 -150 -240 {lab=VDD}
N -230 -240 -230 -180 {lab=VDD}
N 150 -240 200 -240 {lab=VDD}
N 200 -240 230 -240 {lab=VDD}
N 150 -180 230 -180 {lab=VDD}
N 230 -240 230 -180 {lab=VDD}
N 150 -270 150 -240 {lab=VDD}
N -150 -270 -150 -240 {lab=VDD}
N -90 160 0 160 {lab=VSS}
N -90 150 -90 160 {lab=VSS}
N -0 150 -0 160 {lab=VSS}
C {sky130_fd_pr/pfet_01v8.sym} -130 -180 0 1 {name=M3
L=1
W=4
nf=1
mult=1
model=pfet_01v8
spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} 130 -180 0 0 {name=M4
L=1
W=4
nf=1
mult=1
model=pfet_01v8
spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} -170 -60 0 0 {name=M1
L=0.5
W=4
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} 170 -60 0 1 {name=M2
L=0.5
W=4
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} -20 60 0 0 {name=M5
L=1
W=4
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} 150 -270 0 0 {name=p11 sig_type=std_logic lab=VDD}
C {vsource.sym} -90 110 0 1 {name=V1 value=0.75 savecurrent=false}
C {devices/ipin.sym} -240 -60 0 0 {name=P4 lab=INP}
C {devices/ipin.sym} 240 -60 0 1 {name=P3 lab=INN}
C {devices/opin.sym} 200 -120 0 0 {name=P9 lab=OUTP}
C {iopin.sym} -150 -270 0 0 {name=p1 lab=VDD}
C {devices/lab_pin.sym} 70 -60 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -70 -60 0 1 {name=p6 sig_type=std_logic lab=VSS}
C {iopin.sym} 0 160 0 0 {name=p7 lab=VSS}
