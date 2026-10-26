#!/usr/bin/env bash
# The hand-drawn iadc OTA layout (upstream layout/ota/ota.gds, cell 'ota') measured the flow's way, as
# scripts/reference_ttsky25a.sh does for the TTSKY25a tile. The layout contains the switched-capacitor CMFB;
# for the AC benches its clocks are held static in phase 1 (p1 = VDD, p2 = 0), the CMFB output node cmc is
# driven by the same ideal CMFB law as the flow's AC model (ASSUMPTION, circuits/iadc_ota/SOURCE.md), and
# the 30 uA bias current is the upstream testbench's. In phase 1 the CMFB's sampling capacitors sit between
# cm and bias_a, so the outputs see C3/C4 (to cmc) as in the flow's model.
cd /foss/designs && source scripts/env.sh
G=circuits/iadc_ota/upstream_src/layout/ota/ota.gds
P="ip=INP,in=INN,op=OUTP,on=OUTN,VDD=VDD,VSS=VSS,cm=cm_w,cmc=cmc_w,bias_a=bias_a_w,i_bias=ib_w,p1=p1_w,p1_b=p1b_w,p2=p2_w,p2_b=p2b_w"
B="Bcmfb cmc_w VSS V = v(bias_a_w) + (v(OUTP) + v(OUTN))/2 - v(cm_w);Ibias_ext VDD ib_w 30u;Vp1 p1_w VSS 1.8;Vp1b p1b_w VSS 0;Vp2 p2_w VSS 0;Vp2b p2b_w VSS 1.8"
SKIP=""; [ -f outputs/reference_layout/iadc_ota/ota_pex.spice ] && SKIP="--skip-extract"
python3 scripts/reference_layout.py iadc_ota $G ota $SKIP --ports "$P" --bias "$B"
# R+C extraction (Magic extresist, 324 k resistors, about 1.3 GB and 30 min): run it when nothing else is running.
# --map-shorted is needed: the R+C netlist exposes the CMFB sub-cell's clock ports separately (Magic reports them
# as shorted to p1, p1_b, ...); left unconnected, its switch gates float and the operating point is wrong.
#   python3 scripts/reference_layout.py iadc_ota $G ota --skip-extract --ports "$P" --bias "$B" --rc --rc-tol 100 \
#       --map-shorted --tag rc100s
