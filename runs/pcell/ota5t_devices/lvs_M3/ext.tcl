gds read /foss/designs/runs/pcell/ota5t_devices/M3.gds
load M3
flatten M3_flat
load M3_flat
select top cell
port makeall
extract path /foss/designs/runs/pcell/ota5t_devices/lvs_M3
extract all
ext2spice lvs
ext2spice -p /foss/designs/runs/pcell/ota5t_devices/lvs_M3 -o /foss/designs/runs/pcell/ota5t_devices/lvs_M3/M3_extracted.spice
quit -noprompt
