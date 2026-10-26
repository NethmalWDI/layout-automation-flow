gds read /foss/designs/outputs/S0/ttsky25a_fd/pcell/XM33.gds
load XM33
select top cell
puts "CELL_BBOX_LAMBDA [box values]"
puts "SUBCELLS [llength [cellname list children XM33]]"
flatten XM33_flat
load XM33_flat
select top cell
puts "FLAT_BBOX_LAMBDA [box values]"
drc style drc(full)
drc euclidean on
drc check
drc catchup
set n [drc list count total]
puts "DRC_TOTAL $n"
set f [open /foss/designs/outputs/S0/ttsky25a_fd/pcell/drc_XM33/drc_report.txt w]
puts $f "top XM33 (flattened) gds /foss/designs/outputs/S0/ttsky25a_fd/pcell/XM33.gds"
puts $f "DRC_TOTAL $n"
foreach {why boxes} [drc listall why] { puts $f "[llength $boxes]\t$why" }
close $f
# negative control: a 0.05 um wide met1 sliver must be flagged
box 0um 0um 0.05um 1um
paint metal1
drc check
drc catchup
puts "NEG_CONTROL_TOTAL [drc list count total]"
quit -noprompt
