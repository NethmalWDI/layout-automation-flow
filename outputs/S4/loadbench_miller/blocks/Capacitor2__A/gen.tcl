drc off
snap internal
cellname delete Capacitor2_mim
load Capacitor2_mim -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__cap_mim_m3_1 Capacitor2_mim_pc w 15.66 l 15.66
select top cell
expand
save Capacitor2_mim
gds write Capacitor2_mim
quit -noprompt
