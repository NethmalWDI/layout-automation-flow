gds read /foss/designs/runs/pcell/ota5t_devices/M2.gds
load M2
flatten M2_flat
load M2_flat
select top cell
port makeall
extract path /foss/designs/runs/pcell/ota5t_devices/lvs_M2
extract all
ext2spice lvs
ext2spice -p /foss/designs/runs/pcell/ota5t_devices/lvs_M2 -o /foss/designs/runs/pcell/ota5t_devices/lvs_M2/M2_extracted.spice
quit -noprompt
