gds read /foss/designs/outputs/S4/ota5t_gui_copy/blocks/nmos_differential_pair__ABBA/nmos_differential_pair__ABBA.gds
load nmos_differential_pair__ABBA
select top cell
port makeall
set f [open /foss/designs/outputs/S4/ota5t_gui_copy/blocks/nmos_differential_pair__ABBA/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/ota5t_gui_copy/blocks/nmos_differential_pair__ABBA/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/ota5t_gui_copy/blocks/nmos_differential_pair__ABBA/lvs/lvs -o /foss/designs/outputs/S4/ota5t_gui_copy/blocks/nmos_differential_pair__ABBA/lvs/lvs/extracted.spice
quit -noprompt
