drc off
snap internal
cellname delete XM3
load XM3 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8 XM3_pc w 8.0 l 1.0 nf 1 m 1
select top cell
expand
save XM3
gds write XM3
cellname delete XM4
load XM4 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8 XM4_pc w 8.0 l 1.0 nf 1 m 1
select top cell
expand
save XM4
gds write XM4
cellname delete XM1
load XM1 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8 XM1_pc w 24.0 l 0.5 nf 1 m 1
select top cell
expand
save XM1
gds write XM1
cellname delete XM2
load XM2 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8 XM2_pc w 24.0 l 0.5 nf 1 m 1
select top cell
expand
save XM2
gds write XM2
cellname delete XM5
load XM5 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8 XM5_pc w 24.0 l 1.0 nf 1 m 1
select top cell
expand
save XM5
gds write XM5
quit -noprompt
