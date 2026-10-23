gds read /foss/designs/runs/align/smoke_five_transistor_ota/FIVE_TRANSISTOR_OTA_0.gds
load FIVE_TRANSISTOR_OTA_0
select top cell
port makeall
extract path /foss/designs/runs/align/smoke_five_transistor_ota/lvs_expanded
extract all
ext2spice lvs
ext2spice -p /foss/designs/runs/align/smoke_five_transistor_ota/lvs_expanded -o /foss/designs/runs/align/smoke_five_transistor_ota/lvs_expanded/FIVE_TRANSISTOR_OTA_0_extracted.spice
quit -noprompt
