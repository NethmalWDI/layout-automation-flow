drc off
snap internal
cellname delete pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdhalf_outS
load pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdhalf_outS -silent
box 0 0 0 0
magic::gencell sky130::sky130_fd_pr__pfet_01v8_lvt pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdhalf_outS_pc w 1.7763 l 0.89 nf 8 m 1 topc 1 botc 1 diffcov 50 viasrc 50 viadrn 50 guard 1 conn_gates 1
select top cell
expand
save pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdhalf_outS
gds write pfet_01v8_lvt_W14p21_L0p89_m1__nf8_gboth_sdhalf_outS
quit -noprompt
