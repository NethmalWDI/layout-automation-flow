gds read /foss/designs/runs/align/examples/five_transistor_ota/FIVE_TRANSISTOR_OTA_0.gds
load FIVE_TRANSISTOR_OTA_0
select top cell
puts "CELL_BBOX_LAMBDA [box values]"
puts "SUBCELLS [llength [cellname list children FIVE_TRANSISTOR_OTA_0]]"
flatten FIVE_TRANSISTOR_OTA_0_flat
load FIVE_TRANSISTOR_OTA_0_flat
select top cell
puts "FLAT_BBOX_LAMBDA [box values]"
drc style drc(full)
drc euclidean on
drc check
drc catchup
set n [drc list count total]
puts "DRC_TOTAL $n"
set f [open /foss/designs/runs/align/examples/five_transistor_ota/drc/drc_report.txt w]
puts $f "top FIVE_TRANSISTOR_OTA_0 (flattened) gds /foss/designs/runs/align/examples/five_transistor_ota/FIVE_TRANSISTOR_OTA_0.gds"
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
