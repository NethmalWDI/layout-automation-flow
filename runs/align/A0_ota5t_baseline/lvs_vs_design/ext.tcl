gds read /foss/designs/runs/align/A0_ota5t_baseline/OTA5T_0.gds
load OTA5T_0
select top cell
port makeall
extract path /foss/designs/runs/align/A0_ota5t_baseline/lvs_vs_design
extract all
ext2spice lvs
ext2spice -p /foss/designs/runs/align/A0_ota5t_baseline/lvs_vs_design -o /foss/designs/runs/align/A0_ota5t_baseline/lvs_vs_design/OTA5T_0_extracted.spice
quit -noprompt
