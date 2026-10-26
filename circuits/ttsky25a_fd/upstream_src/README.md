![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg)

# Fully Differential Op-Amp for Electrode–Skin Impedance Extraction (Tiny Tapeout TTSKY25a)

A two-stage, fully differential CMOS operational amplifier designed in the open-source **SkyWater SKY130** process and **fabricated on the Tiny Tapeout TTSKY25a shuttle**. It is the core building block of a custom ASIC that extracts electrode–skin impedance (ESI) mismatch in wearable EEG, so that motion artifacts can be cancelled with an adaptive filter.

- **Paper:** I. Nethmal\*, L. Atapattu\*, E. Jayathilaka\*, S. Madugalle\*, *et al.*, "An Open-Source CMOS ASIC for I/Q Based Electrode-Skin Impedance Mismatch Extraction," accepted at **IEEE ICM 2026** (\*equal contribution).
- **System-level work:** "A Dry-Contact Ear-EEG System With Continuous Electrode-Skin Impedance Mismatch Monitoring for Motion Artifact Cancellation Using DRL Stimulus," **IEEE BioCAS 2026** — [arXiv:2609.02777](https://arxiv.org/abs/2609.02777)
- **Status:** fabricated chips received; post-silicon functional testing is in progress. All performance figures below are **post-layout simulation**, not measurements.
- Tiny Tapeout datasheet: [EpitaXC](https://tinytapeout.com/chips/ttsky25a/tt_um_diff)

## Results (post-layout simulation)

| Parameter | Value |
|---|---|
| Process / supply | SKY130 130 nm CMOS / 1.8 V |
| DC open-loop gain | ≈ 100 dB |
| Unity-gain bandwidth | 2.3 MHz |
| Phase margin | ≥ 52° |
| CMRR | ≈ 91 dB at 1 kHz |
| Power | ≈ 500 µW |
| Layout area | ≈ 0.04 mm² |

<p align="center">
  <img src="figures/opamp_postlayout_gain_cmrr_phase.png" width="48%" alt="Post-layout gain, CMRR and phase"/>
  <img src="figures/bpf_postlayout_response.png" width="48%" alt="Post-layout band-pass filter response"/>
</p>
<p align="center"><em>Left: post-layout open-loop gain, CMRR and phase. Right: 4th-order MFB band-pass filter built from two of these op-amps, centred at 1.05 kHz (213 Hz bandwidth). Figures from the ICM 2026 paper.</em></p>

<!-- <p align="center"><img src="figures/opamp_postlayout_gain_cmrr_phase.png" width="75%" alt="Post-layout gain, CMRR and phase"/></p>
<p align="center"><em><strong>Figure 1.</strong> Post-layout open-loop gain, CMRR and phase response of the op-amp (from the ICM 2026 paper).</em></p>

<p align="center"><img src="figures/bpf_postlayout_response.png" width="75%" alt="Post-layout band-pass filter response"/></p>
<p align="center"><em><strong>Figure 2.</strong> Post-layout response of the 4th-order MFB band-pass filter built from two of these op-amps, centred at 1.05 kHz with 213 Hz bandwidth (from the ICM 2026 paper).</em></p> -->

## Layout

<p align="center"><img src="figures/opamp_layout.jpg" width="70%" alt="Tiny Tapeout die and op-amp layout"/></p>
<p align="center"><em>Tiny Tapeout TTSKY25a die (left) and the op-amp layout (right), drawn in Magic. Common-centroid placement, dummy devices and symmetric routing reduce mismatch in the differential paths.</em></p>

## Architecture

- **First stage:** folded-cascode OTA, chosen for high gain with a wider input common-mode range than a telescopic stage at 1.8 V.
- **Second stage:** common-source gain stage for output swing and drive.
- **Common-mode feedback:** a separate CMFB loop for each stage (differential-amplifier CMFB on stage 1, resistor-sensing CMFB on stage 2).
- **Compensation:** Miller capacitors between the two stages.
- **Bias:** on-chip beta-multiplier current reference with start-up. Two digital pins select self-bias or an external bias current for characterisation.

### 1. Operational Amplifier
![Op-amp](docs/Operational_amplifier.png)

### 2. Biasing Circuit
![Bias](docs/Biasing_circuit.png)

### 3. Folded Cascode Op-Amp
![Folded cascode](docs/folded_cascode_opamp.png)

### 4. Common Source Stage
![CS stage](docs/Common_source_stage.png)


## Where it fits: the ESI-extraction ASIC

A low-amplitude 1 kHz stimulus is injected through the driven-right-leg (DRL) electrode. Two of these op-amps form a 4th-order active-RC band-pass filter that isolates the carrier, and two fully differential multipliers demodulate it into I/Q components. The filter's R and C are off-chip, so the centre frequency can be tuned without a re-spin. The multiplier was laid out separately in IHP SG13G2 for UNIC-CASS 2026: [NethmalWDI/unic_cass_ihp](https://github.com/NethmalWDI/unic_cass_ihp).

<p align="center"><img src="figures/system_architecture.png" width="70%" alt="ESI extraction system architecture"/></p>

## Repository structure

| Path | Contents |
|---|---|
| `src/Opamp_Design/src` | Xschem schematics: OTA, CS stage, bias, top level |
| `src/Opamp_Design/testbenches`, `src/Opamp_Design/Simulations` | Testbenches: gain/phase, CMRR, PSRR, linearity, transient |
| `src/Bandpass_filter`, `src/Multiplier` | Filter and multiplier schematics and testbenches |
| `mag/`, `gds/`, `lef/` | Magic layout and Tiny Tapeout submission views |
| `docs/` | Tiny Tapeout datasheet and earlier simulation figures |

**Tools:** Xschem, ngspice, Magic, KLayout, Netgen — all open source.

## Test plan (in progress)

Using the AD03 board (see the datasheet): functional check in a band-pass configuration, then offset, linearity, CMRR and PSRR measurements, compared against the post-layout values above.

## Contributors and roles

| Contributor | Role |
|---|---|
| Sajitha Madugalle | Behavioural modelling |
| Lohan Atapattu | Schematic design and simulation |
| Erandee Jayathilaka | Layout |
| **Imasha Nethmal** | **Layout, simulation, and Tiny Tapeout submission** |

Department of Electronic and Telecommunication Engineering, University of Moratuwa, Sri Lanka. Original repository: [LohanAtapattu/ttsky25_EpitaXC](https://github.com/LohanAtapattu/ttsky25_EpitaXC).
