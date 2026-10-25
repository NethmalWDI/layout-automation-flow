"""
Standalone TB.extract producer for the MLCAD26 opamp benchmark.

Drop this file into an opamp results folder (or run it from one with
`python /path/to/standalone_tb_extract.py`) after ngspice has produced the
result_*.raw files. Writes TB.extract in cwd in the same shape
SimulationInterface.calculateSimulationResults would write.

Input files expected in cwd:
    CombinedTestBench.cir         (device -> model lookup)
    params.cir                    (W/L/multiplier values for area + RG*/FEC*)
    result_op.raw                 (operating point + mosfet vth/vgs/vds/...)
    result_dc.raw                 (icmr_min, icmr_max meas results)
    result_dc_vout.raw            (vout_min, vout_max meas results)
    result_ac_vdc.raw             (gain_commonmode -> CMRR)
    result_ac_vdd.raw             (gain_vdd -> PSRR)
    result_ac_vtran.raw           (frequency sweep -> dc_gain, ft, PM)
    result_tran.raw               (slew_pos, slew_neg)

Dependencies: numpy + stdlib.

Pure-Python reimplementation of the relevant slices of
simulators/opamp_perf_calc.py + simulators/constraints_calc.py +
simulators/results_config.py + utils/pyspice_module/.../RawFile.py, with no
imports from the project. Hardcoded for the 'combined-reduced' testbench layout
produced by this project's OpAmpTestbenchGeneration (subckt instance named
XOpAmp, sublevel model names msky130_fd_pr__{n,p}fet_01v8_lvt). Adjust the
constants below for other technologies.

The per-opamp CONSTRAINTS list below is auto-generated from the opamp's
constraint_settings.xml by tests/gen_standalone_extracts.py; it exactly mirrors
the ordered, named constraints ResultsConfig.get_constraints_results_string
writes. Each entry is (constraint_name, safety_margin); the device(s) and rule
are recovered from the name by splitting on '_' -- precisely how the framework
recovers them.
"""

import os
import re
import sys
from decimal import Decimal

import numpy as np


# ---------- tech / testbench constants ----------------------------------------

# Sentinel written for missing/failed analyses, matching the project's config
# 'infinity'. The framework substitutes these when a result_*.raw file is
# absent (an infeasible design whose sub-simulation didn't run/converge).
INFINITY = 9999999999999
MINUS_INFINITY = -INFINITY

# How the testbench wraps the opamp subcircuit (matches the config
# 'testcircuit_name' = XOpAmp + the xtb_tran wrapper around it). The
# result_op.raw variable for a mosfet param looks like:
#   @m.<TESTBENCH_PREFIX>.x<device_lower>.<MSUBLEVEL[model]>[vth]
TESTBENCH_PREFIX = 'xtb_tran.xopamp'

# Subcircuit-level model instance name inside the mosfet macro. Matches the
# config 'device_sublevel_extraction_mapping'.
MSUBLEVEL = {
    'sky130_fd_pr__nfet_01v8_lvt': 'msky130_fd_pr__nfet_01v8_lvt',
    'sky130_fd_pr__pfet_01v8_lvt': 'msky130_fd_pr__pfet_01v8_lvt',
}

# Rules that operate on a device PAIR (name is <struct>_<rule>_<dev1>_<dev2>);
# every other rule operates on a single device (name is <struct>_<rule>_<dev>).
# Matches the split ResultsConfig.get_constraints_results_string performs.
PAIR_RULES = {'FEVa', 'FEVb', 'FECa', 'FECb', 'FEVGSa', 'FEVGSb'}


# === BEGIN CONSTRAINTS (auto-generated per opamp) ===========================
# Ordered list of (constraint_name, safety_margin), matching the framework's
# constraints_dict ordering exactly. Replace this block for a different opamp.
OPAMP_NAME = 'SimpleTwoStageOpAmp_SimpleOpAmp1_1'
CONSTRAINTS = [
    ('PDifferentialPair_pInv_NormalTransistorPmos7', 0.0),
    ('PDifferentialPair_pInv_NormalTransistorPmos6', 0.0),
    ('PDifferentialPair_pSat_NormalTransistorPmos7', 0.0),
    ('PDifferentialPair_pSat_NormalTransistorPmos6', 0.0),
    ('PDifferentialPair_pREO_NormalTransistorPmos7', 1.0),
    ('PDifferentialPair_pREO_NormalTransistorPmos6', 1.0),
    ('PDifferentialPair_FEVa_NormalTransistorPmos7_NormalTransistorPmos6', 0.2),
    ('PDifferentialPair_FEVb_NormalTransistorPmos7_NormalTransistorPmos6', 0.2),
    ('NSimpleCurrentMirror_nInv_DiodeTransistorNmos1', 0.0),
    ('NSimpleCurrentMirror_nInv_NormalTransistorNmos4', 0.0),
    ('NSimpleCurrentMirror_nSat_DiodeTransistorNmos1', 0.0),
    ('NSimpleCurrentMirror_nSat_NormalTransistorNmos4', 0.0),
    ('PSimpleCurrentMirror_pInv_DiodeTransistorPmos2', 0.0),
    ('PSimpleCurrentMirror_pInv_NormalTransistorPmos8', 0.0),
    ('PSimpleCurrentMirror_pInv_NormalTransistorPmos5', 0.0),
    ('PSimpleCurrentMirror_pSat_DiodeTransistorPmos2', 0.0),
    ('PSimpleCurrentMirror_pSat_NormalTransistorPmos8', 0.0),
    ('PSimpleCurrentMirror_pSat_NormalTransistorPmos5', 0.0),
]
# === END CONSTRAINTS =======================================================


# ---------- minimal ngspice .raw binary parser --------------------------------

def parse_raw(path):
    """Return dict var_name -> 1-D numpy array (complex if Flags: complex)."""
    with open(path, 'rb') as f:
        content = f.read()
    for marker in (b'Binary:\n', b'Binary:\r\n'):
        idx = content.find(marker)
        if idx >= 0:
            data_start = idx + len(marker)
            header = content[:idx].decode('ascii', errors='replace')
            break
    else:
        raise ValueError(f"{path}: no 'Binary:' marker")

    n_vars = int(re.search(r'No\. Variables:\s*(\d+)', header).group(1))
    n_pts = int(re.search(r'No\. Points:\s*(\d+)', header).group(1))
    flags = re.search(r'Flags:\s*(\S+)', header).group(1).strip().lower()

    vars_section = header.split('Variables:', 1)[1]
    names = []
    for line in vars_section.splitlines():
        items = [x.strip() for x in line.split('\t') if x.strip()]
        if len(items) >= 2 and items[0].isdigit():
            names.append(items[1])
        if len(names) >= n_vars:
            break

    cols = n_vars * (2 if flags == 'complex' else 1)
    arr = np.frombuffer(
        content[data_start:], dtype='f8', count=cols * n_pts,
    ).reshape(n_pts, cols).T
    if flags == 'complex':
        out = arr[0::2].astype('complex128')
        out.imag = arr[1::2]
    else:
        out = arr
    return {names[i]: out[i] for i in range(n_vars)}


# ---------- testbench / params helpers ----------------------------------------

def parse_device_models(tb_path):
    """Return dict device_name -> model_name by scanning CombinedTestBench.cir."""
    with open(tb_path, 'r') as f:
        text = f.read()
    out = {}
    # `XDeviceName <nodes...> <model_name> <params...>`
    for line in text.splitlines():
        m = re.match(r'\s*[Xx](\S+).*?\s(sky130_fd_pr__\S+)', line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def read_param(params_text, name):
    """Return the float value of parameter `name` from params.cir, following
    `a = param_b` -> `param_b = 0.5` indirection.

    Matches `<name>=<value>` anywhere (the `=` anchor makes it robust), so it
    works for both the ngspice per-line form `.param name=value` and the HSPICE
    block form (`.PARAM` then `+ name=value` continuation lines) -- mirrors the
    framework's get_width/get_length regex."""
    m = re.search(r'\b' + re.escape(name) + r'\s*=\s*(\S+)', params_text)
    if m is None:
        return None
    val = m.group(1).rstrip(',;')
    try:
        return float(val)
    except ValueError:
        if val.startswith('param_'):
            return read_param(params_text, val)
        return None


def op_value(raw_op, device, model, param):
    """Absolute value of an operating-point mosfet parameter."""
    sublevel = MSUBLEVEL[model]
    key = f'@m.{TESTBENCH_PREFIX}.x{device.lower()}.{sublevel}[{param}]'
    var = raw_op.get(key)
    if var is None:
        raise KeyError(f"missing operating-point variable in result_op.raw: {key}")
    return abs(float(var[0]))


# ---------- performances ------------------------------------------------------

def correct_phase_series(phase):
    """Same single-jump de-wrap the project's calc_ac_perfs uses."""
    phase = phase - phase[0]
    for i in range(len(phase) - 1):
        d = phase[i + 1] - phase[i]
        if 2 * np.pi * 0.9 < abs(d) < 2 * np.pi * 1.1:
            phase[i + 1:] = phase[i + 1:] - 2 * np.pi
    return phase


def calc_dc(raw_op, raw_dc, raw_dc_vout):
    if raw_op is not None:
        v_inn = float(raw_op['v(xtb_tran.inn)'][0])
        v_vdd = float(raw_op['v(xtb_tran.vdd!)'][0])
        i_vdd = float(raw_op['i(v.xtb_tran.vdd)'][0])
        power = Decimal(v_vdd) * Decimal(-1) * Decimal(i_vdd)
        offset = abs(Decimal(v_inn) - Decimal(v_vdd) / 2)
    else:
        power = INFINITY
        offset = INFINITY
    if raw_dc is not None:
        icmr_min = float(raw_dc['icmr_min'][0])
        icmr_max = float(raw_dc['icmr_max'][0])
    else:
        icmr_min = INFINITY
        icmr_max = MINUS_INFINITY
    if raw_dc_vout is not None:
        vout_min = float(raw_dc_vout['vout_min'][0])
        vout_max = float(raw_dc_vout['vout_max'][0])
    else:
        vout_min = INFINITY
        vout_max = MINUS_INFINITY
    return power, offset, icmr_min, icmr_max, vout_min, vout_max


def calc_ac(raw_ac_vdc, raw_ac_vdd, raw_ac_vtran):
    A_cm = None if raw_ac_vdc is None else float(raw_ac_vdc['gain_commonmode'][0].real)
    A_ps = None if raw_ac_vdd is None else float(raw_ac_vdd['gain_vdd'][0].real)

    A_0 = 0.0
    if raw_ac_vtran is None:
        gain = transit_freq = phase_margin = MINUS_INFINITY
    else:
        freq = raw_ac_vtran['frequency'].real
        vdb = raw_ac_vtran['vdb(xtb_ac_vtran.out)'].real
        ph = correct_phase_series(raw_ac_vtran['ph(xtb_ac_vtran.out)'].real)

        gain = 0.0
        vdb_min_geq_0 = float('inf')
        vdb_max_leq_0 = float('-inf')
        fq_max_leq_0 = fq_min_geq_0 = 0.0
        ph_max_leq_0 = ph_min_geq_0 = 0.0
        vdb_sec_geq_0 = fq_sec_geq_0 = ph_sec_geq_0 = 0.0
        vdb_sec_leq_0 = fq_sec_leq_0 = ph_sec_leq_0 = 0.0

        for i, fv in enumerate(freq):
            vdb_sec_geq_0 = vdb[i]; fq_sec_geq_0 = freq[i]; ph_sec_geq_0 = ph[i]
            if np.round(fv, 1) == 1.0:
                gain = vdb[i]
            if np.round(fv, 1) == 10.0:
                A_0 = vdb[i]
            if 0 <= vdb[i] <= vdb_min_geq_0:
                vdb_min_geq_0 = vdb[i]; fq_min_geq_0 = freq[i]; ph_min_geq_0 = ph[i]
            if vdb_max_leq_0 < vdb[i] <= 0:
                vdb_max_leq_0 = vdb[i]; fq_max_leq_0 = freq[i]; ph_max_leq_0 = ph[i]
            if vdb[i] < 0 and vdb_sec_leq_0 >= vdb_max_leq_0:
                vdb_sec_leq_0 = vdb[i]; fq_sec_leq_0 = freq[i]; ph_sec_leq_0 = ph[i]

        if fq_max_leq_0 == 0 and ph_max_leq_0 == 0:
            # all positive; extrapolate to vdb=0
            slope = (fq_min_geq_0 - fq_sec_geq_0) / (vdb_min_geq_0 - vdb_sec_geq_0)
            transit_freq = fq_sec_geq_0 + slope * (0 - vdb_sec_geq_0)
            slope_ph = (ph_min_geq_0 - ph_sec_geq_0) / (fq_min_geq_0 - fq_sec_geq_0)
            ph_ft = ph_sec_geq_0 + slope_ph * (transit_freq - fq_sec_geq_0)
        elif fq_min_geq_0 == 0 and ph_min_geq_0 == 0:
            slope = (fq_max_leq_0 - fq_sec_leq_0) / (vdb_max_leq_0 - vdb_sec_leq_0)
            transit_freq = fq_sec_leq_0 + slope * (0 - vdb_sec_leq_0)
            slope_ph = (ph_max_leq_0 - ph_sec_leq_0) / (fq_max_leq_0 - fq_sec_leq_0)
            ph_ft = ph_sec_leq_0 + slope_ph * (transit_freq - fq_sec_leq_0)
        elif fq_min_geq_0 == fq_max_leq_0:
            transit_freq = fq_min_geq_0
            ph_ft = ph_min_geq_0
        else:
            slope1 = (vdb_max_leq_0 - vdb_min_geq_0) / (fq_max_leq_0 - fq_min_geq_0)
            transit_freq = fq_min_geq_0 - vdb_min_geq_0 / slope1
            slope2 = (ph_max_leq_0 - ph_min_geq_0) / (fq_max_leq_0 - fq_min_geq_0)
            ph_ft = ph_min_geq_0 + slope2 * (transit_freq - fq_min_geq_0)

        phase_margin = 180 + np.degrees(ph_ft)

    cmrr = (A_0 - A_cm) if A_cm is not None else MINUS_INFINITY
    psrr = (A_0 - A_ps) if A_ps is not None else MINUS_INFINITY
    return gain, transit_freq, phase_margin, cmrr, psrr


def calc_tran(raw_tran):
    if raw_tran is None:
        return MINUS_INFINITY, INFINITY
    return (float(raw_tran['slew_pos'][0]),
            float(raw_tran['slew_neg'][0]))


def calc_area(devices_dict, params_text):
    total = 0.0
    for dev in devices_dict:
        w = read_param(params_text, f'param_w{dev}')
        l = read_param(params_text, f'param_l{dev}')
        m = read_param(params_text, f'param_m{dev}')
        if w is None or l is None:
            continue
        total += w * l * (m if m is not None else 1.0)
    return total


# ---------- constraints -------------------------------------------------------

def apply_rule(rule, devices, margin, raw_op, devices_dict, params_text):
    def v(dev, p):
        return op_value(raw_op, dev, devices_dict[dev], p)

    if rule in ('nInv', 'pInv'):
        d, = devices; return (v(d, 'vgs') - v(d, 'vth')) - margin
    if rule in ('nSat', 'pSat'):
        d, = devices; return v(d, 'vds') - v(d, 'vdsat') - margin
    if rule in ('nLin', 'pLin'):
        d, = devices; return v(d, 'vdsat') - v(d, 'vds') - margin
    if rule in ('nREO', 'pREO'):
        d, = devices; return -(v(d, 'vgs') - v(d, 'vth')) + margin
    if rule in ('nFEVDS', 'pFEVDS'):
        d, = devices; return v(d, 'vds') - margin
    if rule == 'RGA':
        d, = devices
        return read_param(params_text, f'param_l{d}') \
               * read_param(params_text, f'param_w{d}') - margin
    if rule == 'RGL':
        d, = devices; return read_param(params_text, f'param_l{d}') - margin
    if rule == 'RGW':
        d, = devices; return read_param(params_text, f'param_w{d}') - margin
    if rule == 'FEVa':
        d1, d2 = devices; return -(v(d1, 'vds') - v(d2, 'vds')) + margin
    if rule == 'FEVb':
        d1, d2 = devices; return (v(d1, 'vds') - v(d2, 'vds')) + margin
    if rule == 'FECa':
        d1, d2 = devices
        return (v(d2, 'id') / v(d1, 'id')
                - read_param(params_text, f'param_w{d2}')
                / read_param(params_text, f'param_w{d1}') + margin)
    if rule == 'FECb':
        d1, d2 = devices
        return (-v(d2, 'id') / v(d1, 'id')
                + read_param(params_text, f'param_w{d2}')
                / read_param(params_text, f'param_w{d1}') + margin)
    if rule == 'FEVGSa':
        d1, d2 = devices; return (v(d1, 'vgs') - v(d2, 'vgs')) + margin
    if rule == 'FEVGSb':
        d1, d2 = devices; return -(v(d1, 'vgs') - v(d2, 'vgs')) + margin
    raise ValueError(f"unknown constraint rule: {rule}")


def compute_constraints(raw_op, devices_dict, params_text):
    """Emit (name, value) for each (name, margin) in CONSTRAINTS.

    Device(s) and rule are recovered from the name exactly as
    ResultsConfig.get_constraints_results_string does: split on '_', where
    parts[0] = struct_type, parts[1] = rule, parts[2] (and parts[3] for pair
    rules) = device name(s). Device names carry no underscores, so the split is
    unambiguous."""
    if raw_op is None:
        # No operating point (result_op.raw absent) -> the framework writes
        # minus-infinity for every constraint (handle_missing_results_file).
        return [(name, MINUS_INFINITY) for name, _margin in CONSTRAINTS]
    out = []
    for name, margin in CONSTRAINTS:
        parts = name.split('_')
        rule = parts[1]
        if rule in PAIR_RULES:
            devices = (parts[2], parts[3])
        else:
            devices = (parts[2],)
        out.append((name, apply_rule(rule, devices, margin,
                                     raw_op, devices_dict, params_text)))
    return out


# ---------- driver ------------------------------------------------------------

PERF_ORDER = ['P', 'Voffset', 'icmr_min', 'icmr_max', 'vout_min', 'vout_max',
              'dc_gain', 'ft', 'phaseMargin', 'CMRR', 'PSRR',
              'SR_pos', 'SR_neg', 'area', 'icmr_diff', 'vout_diff']


def load_raw(path):
    """parse_raw, but return None if the file is absent or unreadable, so a
    missing/failed analysis becomes an infinity performance rather than a crash
    (matching the framework's handling of infeasible designs)."""
    if not os.path.exists(path):
        return None
    try:
        return parse_raw(path)
    except Exception:
        return None


def main(cwd='.'):
    os.chdir(cwd)
    raw_op       = load_raw('result_op.raw')
    raw_dc       = load_raw('result_dc.raw')
    raw_dc_vout  = load_raw('result_dc_vout.raw')
    raw_ac_vdc   = load_raw('result_ac_vdc.raw')
    raw_ac_vdd   = load_raw('result_ac_vdd.raw')
    raw_ac_vtran = load_raw('result_ac_vtran.raw')
    raw_tran     = load_raw('result_tran.raw')

    devices_dict = parse_device_models('CombinedTestBench.cir')
    with open('params.cir') as f:
        params_text = f.read()

    power, offset, icmr_min, icmr_max, vout_min, vout_max = \
        calc_dc(raw_op, raw_dc, raw_dc_vout)
    gain, ft, pm, cmrr, psrr = calc_ac(raw_ac_vdc, raw_ac_vdd, raw_ac_vtran)
    sr_pos, sr_neg = calc_tran(raw_tran)
    area = calc_area(devices_dict, params_text)

    perfs = {
        'P': str(power),
        'Voffset': str(offset),
        'icmr_min': str(icmr_min),
        'icmr_max': str(icmr_max),
        'vout_min': str(vout_min),
        'vout_max': str(vout_max),
        'dc_gain': str(gain),
        'ft': str(ft),
        'phaseMargin': str(pm),
        'CMRR': str(cmrr),
        'PSRR': str(psrr),
        'SR_pos': str(sr_pos),
        'SR_neg': str(sr_neg),
        'area': str(area),
        'icmr_diff': str(float(icmr_max) - float(icmr_min)),
        'vout_diff': str(float(vout_max) - float(vout_min)),
    }

    constraints = compute_constraints(raw_op, devices_dict, params_text)

    with open('TB.extract', 'w') as f:
        f.write('Begin Performances\n')
        for k in PERF_ORDER:
            f.write(f'{k} = {perfs[k]}\n')
        f.write('End Performances\n\n')
        f.write('Begin Constraints\n')
        for name, val in constraints:
            f.write(f'{name} = {val}\n')
        f.write('End Constraints\n')

    print(f"wrote TB.extract in {os.path.abspath('.')} ({OPAMP_NAME}, "
          f"{len(constraints)} constraints)")


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
