gds read /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_matched_current_source_pair_4__ABAB/pmos_matched_current_source_pair_4__ABAB.gds
load pmos_matched_current_source_pair_4__ABAB
select top cell
port makeall
set f [open /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_matched_current_source_pair_4__ABAB/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_matched_current_source_pair_4__ABAB/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_matched_current_source_pair_4__ABAB/lvs/lvs_negctl -o /foss/designs/outputs/S4/ttsky25a_fd/blocks/pmos_matched_current_source_pair_4__ABAB/lvs/lvs_negctl/extracted.spice
quit -noprompt
