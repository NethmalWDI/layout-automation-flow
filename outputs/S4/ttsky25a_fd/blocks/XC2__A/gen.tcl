drc off
snap internal
cellname delete XC2_mim
load XC2_mim -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__cap_mim_m3_1 XC2_mim_pc w 10 l 10 nx 5 ny 1
select top cell
expand
save XC2_mim
gds write XC2_mim
quit -noprompt
