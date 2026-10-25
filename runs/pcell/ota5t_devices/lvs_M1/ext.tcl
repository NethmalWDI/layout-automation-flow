gds read /foss/designs/runs/pcell/ota5t_devices/M1.gds
load M1
flatten M1_flat
load M1_flat
select top cell
port makeall
extract path /foss/designs/runs/pcell/ota5t_devices/lvs_M1
extract all
ext2spice lvs
ext2spice -p /foss/designs/runs/pcell/ota5t_devices/lvs_M1 -o /foss/designs/runs/pcell/ota5t_devices/lvs_M1/M1_extracted.spice
quit -noprompt
