gds read /foss/designs/circuits/iadc_ota/upstream_src/layout/ota/ota.gds
load ota
select top cell
flatten ota_flat
load ota_flat
select top cell
port makeall
extract path /foss/designs/outputs/reference_layout/iadc_ota
extract do local
extract all
ext2spice lvs
ext2spice -o /foss/designs/outputs/reference_layout/iadc_ota/ota_lvs.spice
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist off
ext2spice -o /foss/designs/outputs/reference_layout/iadc_ota/ota_pex.spice

quit -noprompt
