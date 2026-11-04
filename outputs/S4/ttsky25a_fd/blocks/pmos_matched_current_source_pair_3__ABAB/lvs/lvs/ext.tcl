gds read /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_matched_current_source_pair_3__ABAB/pmos_matched_current_source_pair_3__ABAB.gds
load pmos_matched_current_source_pair_3__ABAB
select top cell
port makeall
set f [open /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_matched_current_source_pair_3__ABAB/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_matched_current_source_pair_3__ABAB/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_matched_current_source_pair_3__ABAB/lvs/lvs -o /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_matched_current_source_pair_3__ABAB/lvs/lvs/extracted.spice
quit -noprompt
