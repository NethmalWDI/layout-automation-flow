"""Testbench templates of the flow (single source of truth for new design packages).

diso_amp_<AC|OP|NOISE>: differential input, single-ended output OUT (as the 5T example).
dido_amp_<AC|OP|NOISE>: differential input, differential output OUTP/OUTN, CL on each output.

Both close the loop at DC through 1 GH chokes from the output(s) to the inverting input(s) and leave
it open from 1 Hz up (loop corner ~5 uHz): the DC operating point is the unity-gain follower's, as in
an offset-corrected open-loop bench, and a one-sided parasitic cannot rail the output. The AC stimulus
enters through 1 F couplers, so the inputs see exactly the stated AC drive.
Measurements (echo MEAS name value): gain_db (at 1 Hz), gbw_mhz (|H| = 1), pm_deg (180 + phase at UGB
- phase at 1 Hz, unwrapped), isup_ua, power_uw, vout_v (signal output DC: v(OUT) or v(OUTP)-v(OUTN)),
voutcm_v (dido), vnoise_nv_rthz (input-referred at 1 kHz), vnoise_rms_uv_rms.
"""
from __future__ import annotations

HEAD = """* {design} on {tb}
.lib $PDK_ROOT/sky130A/libs.tech/combined/sky130.lib.spice tt
.param VDD_V=1.8 VCM_V=0.9 CL_F=1p
.temp 27

**.subckt {tb}
"""

DISO_NET = """x1 INP INN net1 VDD 0 OUT dut_amp
Vsup VDD 0 'VDD_V'
Vinp INP 0 dc 'VCM_V' ac {acp}
* DC unity feedback through a 1 GH choke, INN held at AC ground by 1 F (loop open from 1 Hz up)
Lfb OUT INN 1G
Cfb INN 0 1
Cload OUT 0 'CL_F'
"""

DIDO_NET = """x1 INP INN OUTN VDD 0 OUTP dut_amp
Vsup VDD 0 'VDD_V'
* AC drive through 1 F couplers; DC set by unity feedback through 1 GH chokes (OUTP->INN, OUTN->INP)
Vacp ACP 0 dc 0 ac {acp}
Vacn ACN 0 dc 0 ac {acn}
Cinp ACP INP 1
Cinn ACN INN 1
Lfbp OUTP INN 1G
Lfbn OUTN INP 1G
Cloadp OUTP 0 'CL_F'
Cloadn OUTN 0 'CL_F'
"""

AC = """.control
  save all
  ac dec 40 1 1G
  let hsig = {sig}
  let hdb = db(hsig)
  let gph_deg = 180/pi * cph(hsig)
  meas ac gain_db find hdb at=1
  meas ac gbw_hz  when hdb=0
  meas ac ph_dc   find gph_deg at=1
  meas ac ph_ugb  find gph_deg when hdb=0
  let gbw_mhz = gbw_hz / 1e6
  let pm_deg  = 180 + (ph_ugb - ph_dc)
  echo MEAS gain_db $&gain_db
  echo MEAS gbw_mhz $&gbw_mhz
  echo MEAS pm_deg $&pm_deg
  write
  quit 0
.endc
"""

OP = """.control
  save all
  op
  let isup    = abs(i(vsup))
  let isup_ua = isup * 1e6
  let power_uw = isup * v(VDD) * 1e6
  let vout_v  = {sig}
  echo MEAS isup_ua $&isup_ua
  echo MEAS power_uw $&power_uw
  echo MEAS vout_v $&vout_v
{extra}  write
  quit 0
.endc
"""

NOISE = """.control
  save all
  let npd    = 20
  let fstart = 1
  let fspot  = 1e3
  noise {onode} {src} dec 20 1 1e9
  setplot noise1
  let idx = npd * log10(fspot/fstart)
  let vnoise_nv_rthz = inoise_spectrum[$&idx] * 1e9
  echo MEAS vnoise_nv_rthz $&vnoise_nv_rthz
  write
  set appendwrite
  setplot noise2
  let vnoise_rms_uv_rms = inoise_total * 1e6
  echo MEAS vnoise_rms_uv_rms $&vnoise_rms_uv_rms
  write
  quit 0
.endc
"""


def bench(design: str, kind: str, dut_text: str, xdut_line: str, differential_output: bool,
          wrapper_extra: str = "") -> str:
    """kind: AC | OP | NOISE. xdut_line: 'XDUT <nodes in the DUT's port order> <design>' using the
    wrapper ports INP INN OUTN VDD VSS OUTP. wrapper_extra: lines placed inside dut_amp (ideal CMFB,
    bias sources that are not part of the DUT)."""
    pre = "dido" if differential_output else "diso"
    tb = f"{pre}_amp_{kind}"
    if differential_output:
        acp, acn = {"AC": ("0.5", "-0.5"), "OP": ("0", "0"), "NOISE": ("1", "0")}[kind]
        net = DIDO_NET.format(acp=acp, acn=acn)
        sig = "v(OUTP) - v(OUTN)"
        onode, src = "v(OUTP,OUTN)", "Vacp"
        extra = "  let voutcm_v = (v(OUTP) + v(OUTN)) / 2\n  echo MEAS voutcm_v $&voutcm_v\n"
    else:
        net = DISO_NET.format(acp={"AC": "1", "OP": "0", "NOISE": "1"}[kind])
        sig, onode, src, extra = "v(OUT)", "v(OUT)", "Vinp", ""
    body = {"AC": AC.format(sig=sig), "OP": OP.format(sig=sig, extra=extra),
            "NOISE": NOISE.format(onode=onode, src=src)}[kind]
    return (HEAD.format(design=design, tb=tb) + net + body + "**.ends\n\n" +
            ".subckt dut_amp INP INN OUTN VDD VSS OUTP\n" + xdut_line + "\n" + wrapper_extra +
            ".ends\n\n" + dut_text + ".end\n")
