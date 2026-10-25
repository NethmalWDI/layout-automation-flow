gds read /foss/designs/runs/pcell/ota5t_devices/M1.gds
load M1
select top cell
port makeall
extract path /foss/designs/runs/pcell/ota5t_devices/lvs_probe_M1
extract all
ext2spice lvs
ext2spice -p /foss/designs/runs/pcell/ota5t_devices/lvs_probe_M1 -o /foss/designs/runs/pcell/ota5t_devices/lvs_probe_M1/M1_extracted.spice
quit -noprompt
