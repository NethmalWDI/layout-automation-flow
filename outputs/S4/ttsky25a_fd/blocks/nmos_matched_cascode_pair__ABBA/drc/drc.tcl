gds read /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_matched_cascode_pair__ABBA/nmos_matched_cascode_pair__ABBA.gds
load nmos_matched_cascode_pair__ABBA
select top cell
puts "CELL_BBOX_LAMBDA [box values]"
puts "SUBCELLS [llength [cellname list children nmos_matched_cascode_pair__ABBA]]"
flatten nmos_matched_cascode_pair__ABBA_flat
load nmos_matched_cascode_pair__ABBA_flat
select top cell
puts "FLAT_BBOX_LAMBDA [box values]"
drc style drc(full)
drc euclidean on
drc check
drc catchup
set n [drc list count total]
puts "DRC_TOTAL $n"
set f [open /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_matched_cascode_pair__ABBA/drc/drc_report.txt w]
puts $f "top nmos_matched_cascode_pair__ABBA (flattened) gds /foss/designs/outputs/S4/ttsky25a_fd/blocks/nmos_matched_cascode_pair__ABBA/nmos_matched_cascode_pair__ABBA.gds"
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
