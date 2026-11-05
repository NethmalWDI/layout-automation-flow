drc off
snap internal
cellname delete XC4_mim
load XC4_mim -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__cap_mim_m3_1 XC4_mim_pc w 4.8 l 4.8 nx 4 ny 1
select top cell
expand
save XC4_mim
gds write XC4_mim
quit -noprompt
