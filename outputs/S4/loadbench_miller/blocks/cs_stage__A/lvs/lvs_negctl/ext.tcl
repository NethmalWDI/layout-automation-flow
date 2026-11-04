gds read /foss/designs/outputs/S4/loadbench_miller/blocks/cs_stage__A/cs_stage__A.gds
load cs_stage__A
select top cell
port makeall
set f [open /foss/designs/outputs/S4/loadbench_miller/blocks/cs_stage__A/lvs/lvs_negctl/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/loadbench_miller/blocks/cs_stage__A/lvs/lvs_negctl
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/loadbench_miller/blocks/cs_stage__A/lvs/lvs_negctl -o /foss/designs/outputs/S4/loadbench_miller/blocks/cs_stage__A/lvs/lvs_negctl/extracted.spice
quit -noprompt
