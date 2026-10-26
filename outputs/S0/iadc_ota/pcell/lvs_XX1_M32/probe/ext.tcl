gds read /foss/designs/outputs/S0/iadc_ota/pcell/XX1_M32.gds
load XX1_M32
set kids [cellname list children XX1_M32]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX1_M32/probe/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX1_M32/probe
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX1_M32/probe -o /foss/designs/outputs/S0/iadc_ota/pcell/lvs_XX1_M32/probe/extracted.spice
quit -noprompt
