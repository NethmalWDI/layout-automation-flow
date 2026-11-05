gds read /foss/designs/outputs/S0/ttsky25a_fd_v2/pcell/XX2_X1_R4.gds
load XX2_X1_R4
select top cell
puts "CELL_BBOX_LAMBDA [box values]"
puts "SUBCELLS [llength [cellname list children XX2_X1_R4]]"
flatten XX2_X1_R4_flat
load XX2_X1_R4_flat
select top cell
puts "FLAT_BBOX_LAMBDA [box values]"
drc style drc(full)
drc euclidean on
drc check
drc catchup
set n [drc list count total]
puts "DRC_TOTAL $n"
set f [open /foss/designs/outputs/S0/ttsky25a_fd_v2/pcell/drc_XX2_X1_R4/drc_report.txt w]
puts $f "top XX2_X1_R4 (flattened) gds /foss/designs/outputs/S0/ttsky25a_fd_v2/pcell/XX2_X1_R4.gds"
puts $f "DRC_TOTAL $n"
foreach {why boxes} [drc listall why] { puts $f "[llength $boxes]\t$why" }
close $f
# negative control: a 0.05 um wide met1 sliver must be flagged. It sits away from the layout: at the origin it fell
# inside the area of an existing error (a ringless cell's n-well tap rule), and Magic's total did not grow (plan v4)
box -20um -20um -19.95um -19um
paint metal1
drc check
drc catchup
puts "NEG_CONTROL_TOTAL [drc list count total]"
quit -noprompt
