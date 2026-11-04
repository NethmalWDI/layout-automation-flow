gds read /foss/designs/outputs/S4/iadc_ota/blocks/nmos_matched_cascode_pair_10__AB/nmos_matched_cascode_pair_10__AB.gds
load nmos_matched_cascode_pair_10__AB
select top cell
port makeall
set f [open /foss/designs/outputs/S4/iadc_ota/blocks/nmos_matched_cascode_pair_10__AB/lvs/lvs/cellname.txt w]; puts $f [cellname list self]; close $f
extract path /foss/designs/outputs/S4/iadc_ota/blocks/nmos_matched_cascode_pair_10__AB/lvs/lvs
extract all
ext2spice lvs
ext2spice -p /foss/designs/outputs/S4/iadc_ota/blocks/nmos_matched_cascode_pair_10__AB/lvs/lvs -o /foss/designs/outputs/S4/iadc_ota/blocks/nmos_matched_cascode_pair_10__AB/lvs/lvs/extracted.spice
quit -noprompt
