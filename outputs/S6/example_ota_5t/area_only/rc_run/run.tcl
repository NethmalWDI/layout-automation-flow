gds read /foss/designs/outputs/S5/example_ota_5t/routed_area_only/example_ota_5t_routed.gds
load example_ota_5t_routed
select top cell
flatten example_ota_5t_routed_flat
load example_ota_5t_routed_flat
select top cell
port makeall
extract do local
extract all
ext2sim labels on
ext2sim
extresist tolerance 100
extresist all
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist on
ext2spice -o /foss/designs/outputs/S6/example_ota_5t/area_only/example_ota_5t_routed_pexrc.spice

quit -noprompt
