gds read /foss/designs/circuits/ttsky25a_fd/upstream_src/gds/tt_um_diff.gds
load tt_um_diff
select top cell
flatten tt_um_diff_flat
load tt_um_diff_flat
select top cell
port makeall
extract path /foss/designs/outputs/reference_layout/ttsky25a_fd
extract do local
extract all
ext2spice lvs
ext2spice -o /foss/designs/outputs/reference_layout/ttsky25a_fd/tt_um_diff_lvs.spice
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist off
ext2spice -o /foss/designs/outputs/reference_layout/ttsky25a_fd/tt_um_diff_pex.spice

quit -noprompt
