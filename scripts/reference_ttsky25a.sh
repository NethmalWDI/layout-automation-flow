#!/usr/bin/env bash
# The taped-out TTSKY25a tile (tt_um_diff) measured the flow's way: Magic extraction (LVS netlist and a
# C-only PEX), LVS against the flow's layout view, and the schematic, the drawn devices and the PEX in the
# flow's own dido benches, at three condition sets:
#   (default)            the flow's bench: tt, 27 C, ideal 529 fF loads      -> reference_layout.json
#   paper_ff_20C_mim100  the designers' gain_and_phase.sch: ff, 20 C, 100 x 1x1 um MIM loads
#   tt_27C_mim100        the same loads at tt, 27 C (separates the corner from the load)
# Tile pins: ui_in[0] = en_1 = 1.8 V, ui_in[1] = en_2 = 0 (the bias setting that matches the schematic).
# Run inside the image from the repository root; the first call extracts (about 5 min), the others reuse it.
cd /foss/designs && source scripts/env.sh
G=circuits/ttsky25a_fd/upstream_src/gds/tt_um_diff.gds
P="ena=VSS,ua[1]=INP,ua[2]=INN,ua[4]=OUTP,ua[5]=OUTN,ua[0]=VREF,ua[3]=RGM,VDPWR=VDD,VGND=VSS,ui_in[0]=EN1,ui_in[1]=EN2"
B="Rgm_ext RGM VSS 12k;Vref_ext VREF VSS 0.9;Ven1 EN1 VSS 1.8;Ven2 EN2 VSS 0"
SKIP=""; [ -f outputs/reference_layout/ttsky25a_fd/tt_um_diff_pex.spice ] && SKIP="--skip-extract"
python3 scripts/reference_layout.py ttsky25a_fd $G tt_um_diff $SKIP --ports "$P" --bias "$B"
python3 scripts/reference_layout.py ttsky25a_fd $G tt_um_diff --skip-extract --ports "$P" --bias "$B" \
  --corner ff --temp 20 --mim-load 1,1,100 --tag paper_ff_20C_mim100
python3 scripts/reference_layout.py ttsky25a_fd $G tt_um_diff --skip-extract --ports "$P" --bias "$B" \
  --corner tt --temp 27 --mim-load 1,1,100 --tag tt_27C_mim100
