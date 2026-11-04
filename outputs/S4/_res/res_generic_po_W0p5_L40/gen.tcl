drc off
snap internal
cellname delete res_generic_po_W0p5_L40
load res_generic_po_W0p5_L40 -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__res_generic_po res_generic_po_W0p5_L40_pc w 0.5 l 40.0 guard 0
select top cell
expand
save res_generic_po_W0p5_L40
gds write res_generic_po_W0p5_L40
quit -noprompt
