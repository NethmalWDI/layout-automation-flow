gds read /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM5__A/XM5__A.gds
load XM5__A
select top cell
port makeall
set f [open /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM5__A/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM5__A/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM5__A/lvs/lvs -o /foss/designs/outputs/S4/ota5t_gui_new/blocks/XM5__A/lvs/lvs/extracted.spice
quit -noprompt
