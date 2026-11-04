drc off
snap internal
cellname delete XC3_mim
load XC3_mim -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__cap_mim_m3_1 XC3_mim_pc w 4.8 l 4.8 nx 4 ny 1
select top cell
expand
save XC3_mim
gds write XC3_mim
quit -noprompt
