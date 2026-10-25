drc off
snap internal
cellname delete M3
load M3 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8 M3_pc w 8 l 1 nf 1 m 1 guard 1
select top cell
expand
save M3
gds write M3
cellname delete M4
load M4 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8 M4_pc w 8 l 1 nf 1 m 1 guard 1
select top cell
expand
save M4
gds write M4
cellname delete M1
load M1 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8 M1_pc w 24 l 0.5 nf 1 m 1 guard 1
select top cell
expand
save M1
gds write M1
cellname delete M2
load M2 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8 M2_pc w 24 l 0.5 nf 1 m 1 guard 1
select top cell
expand
save M2
gds write M2
cellname delete M5
load M5 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__nfet_01v8 M5_pc w 24 l 1 nf 1 m 1 guard 1
select top cell
expand
save M5
gds write M5
quit -noprompt
