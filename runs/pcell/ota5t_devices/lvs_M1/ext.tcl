gds read /foss/designs/runs/pcell/ota5t_devices/M1.gds
load M1
set kids [cellname list children M1]
load [lindex $kids 0]
select top cell
port makeall
set f [open /foss/designs/runs/pcell/ota5t_devices/lvs_M1/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/runs/pcell/ota5t_devices/lvs_M1
extract all
ext2spice lvs
ext2spice -p /foss/designs/runs/pcell/ota5t_devices/lvs_M1 -o /foss/designs/runs/pcell/ota5t_devices/lvs_M1/extracted.spice
quit -noprompt
