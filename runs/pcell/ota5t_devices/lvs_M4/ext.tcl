gds read /foss/designs/runs/pcell/ota5t_devices/M4.gds
load M4
flatten M4_flat
load M4_flat
select top cell
port makeall
extract path /foss/designs/runs/pcell/ota5t_devices/lvs_M4
extract all
ext2spice lvs
ext2spice -p /foss/designs/runs/pcell/ota5t_devices/lvs_M4 -o /foss/designs/runs/pcell/ota5t_devices/lvs_M4/M4_extracted.spice
quit -noprompt
