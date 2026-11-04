gds read /foss/designs/outputs/S5/ttsky25a_fd/routed_budget_aware/ttsky25a_fd_routed.gds
load ttsky25a_fd_routed
select top cell
flatten ttsky25a_fd_routed_flat
load ttsky25a_fd_routed_flat
select top cell
port makeall
extract path /foss/designs/outputs/S6/ttsky25a_fd/budget_aware
extract do local
extract all
ext2spice lvs
ext2spice -o /foss/designs/outputs/S6/ttsky25a_fd/budget_aware/ttsky25a_fd_routed_lvs.spice
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist off
ext2spice -o /foss/designs/outputs/S6/ttsky25a_fd/budget_aware/ttsky25a_fd_routed_pex.spice

quit -noprompt
