gds read /foss/designs/runs/pcell/ota5t_devices/M5.gds
load M5
flatten M5_flat
load M5_flat
select top cell
port makeall
extract path /foss/designs/runs/pcell/ota5t_devices/lvs_M5
extract all
ext2spice lvs
ext2spice -p /foss/designs/runs/pcell/ota5t_devices/lvs_M5 -o /foss/designs/runs/pcell/ota5t_devices/lvs_M5/M5_extracted.spice
quit -noprompt
