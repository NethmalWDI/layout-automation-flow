gds read /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_differential_pair__ABBA/pmos_differential_pair__ABBA.gds
load pmos_differential_pair__ABBA
select top cell
port makeall
set f [open /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_differential_pair__ABBA/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_differential_pair__ABBA/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_differential_pair__ABBA/lvs/lvs_negctl -o /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_differential_pair__ABBA/lvs/lvs_negctl/extracted.spice
quit -noprompt
