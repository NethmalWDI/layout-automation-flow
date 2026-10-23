gds read /foss/designs/runs/align/smoke_five_transistor_ota/FIVE_TRANSISTOR_OTA_0.gds
load FIVE_TRANSISTOR_OTA_0
select top cell
extract path /foss/designs/runs/align/smoke_five_transistor_ota/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/runs/align/smoke_five_transistor_ota/lvs -o /foss/designs/runs/align/smoke_five_transistor_ota/lvs/FIVE_TRANSISTOR_OTA_0_extracted.spice
quit -noprompt
