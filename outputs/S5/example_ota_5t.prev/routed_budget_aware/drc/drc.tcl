gds read /foss/designs/outputs/S5/example_ota_5t/routed_budget_aware/example_ota_5t_routed.gds
load example_ota_5t_routed
select top cell
puts "CELL_BBOX_LAMBDA [box values]"
puts "SUBCELLS [llength [cellname list children example_ota_5t_routed]]"
flatten example_ota_5t_routed_flat
load example_ota_5t_routed_flat
select top cell
puts "FLAT_BBOX_LAMBDA [box values]"
drc style drc(full)
drc euclidean on
drc check
drc catchup
set n [drc list count total]
puts "DRC_TOTAL $n"
set f [open /foss/designs/outputs/S5/example_ota_5t/routed_budget_aware/drc/drc_report.txt w]
puts $f "top example_ota_5t_routed (flattened) gds /foss/designs/outputs/S5/example_ota_5t/routed_budget_aware/example_ota_5t_routed.gds"
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
