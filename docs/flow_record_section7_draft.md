## 7. Plan v2 (2026-10-26): new circuits, generality fixes, corners, baselines and hand layouts

This section is the whole story of 2026-10-26: what we set out to do, what we ran, what went wrong, how
each problem was found, what was changed, and what the numbers became. "Before" is the flow as it was on
the morning of 2026-10-26 (variant v1, still runnable as `--variant v1`); "after" is v2. Every number comes
from `outputs/compare/<design>/{before,after}.json`, `docs/before_after.md` or the file named next to it.

### 7.0 What plan v2 set out to do

The external review (project doc 11) and the decisions taken on it (project doc 12) asked for: real
circuits beyond the 5T OTA (two fully differential designs with hand-drawn layouts, and a LOADBench op-amp),
run first with the flow as it was ("before") and then with the updates ("after"); PVT corners and mismatch;
the R19 fix and library floors in S2; baselines (per-net budgets, equal split, an LP, the hand-drawn layouts);
an S3 that keeps fingers in the sized device's model bin; a pre-registration; and an independent review.

Decisions of the day, from you:

- TTSKY25a: the flow's DUT stays `Opamp_with_bias.sch` (the tile's bias switch block hardly changes the
  area), and its specs are the schematic's own performance (gain -1 dB, GBW x 0.9, power x 1.1, PM >= 60 deg,
  as for LOADBench). The ICM 2026 paper's post-layout figures are a reported reference only.
- Git: you commit and push with GitHub Desktop; the flow's sessions do not run git while `.git/index.lock`
  exists.
- Work continues while your laptop is on, with hourly updates; decisions are asked as FEEDBACK NEEDED.

### 7.1 The journey: what went wrong, how it was found, what changed

In order of discovery. "Found by" says which mechanism caught it: a gate (the flow checking itself), a crash,
a run that took too long, reading the code, a comparison with SPICE or with a hand layout, or one of the two
independent reviews (7.9). Effects are on the numbers reported later in this section.

| # | Stage | What went wrong | Found by | What we changed | Effect |
|---|---|---|---|---|---|
| 1 | S0 | The old flow refused LOADBench (`unsupported element 'Ibias'`) | a clean refusal (correct behaviour) | current sources and passives in the parser and the IR | LOADBench ingests |
| 2 | S0/S1 | The Miller capacitor would have vanished: the IR recorded no passives, so the model's guard never fired | reading the code behind 1 | passives in the IR, the linear model, the layout view and the binding | Miller model vs SPICE 0.017 dB, 0.36 %, 0.03 deg |
| 3 | S1 | A current source's node was treated as AC ground | reading the code behind 1 | only voltage-source nodes are AC ground | correct AC model with ideal bias currents |
| 4 | S0 | m > 1 PCells are drawn as unconnected copies; 95 of 96 TTSKY25a bindings failed LVS | G0.7 | LVS of the copies as drawn (extracted connectivity, W/L/nf, count, negative control) | bindings pass |
| 5 | S0 | The designers' TTSKY25a bench saved only `i(vmeas)` | G0.8 reproduction failed | `save all` in the re-run | 98.401 / 2.0515 / 78.236 reproduced |
| 6 | S0 | iadc bias current on the wrong node; an off-chip element's exposed node was VDD | G0.8 / reading the IR | the exposed node is the non-port terminal | correct bias |
| 7 | S0 | The PDK PCell at the netlist size fails met1.6 (minimum area): LOADBench's 484 um finger, iadc's 1.2/0.2 um LVT devices | G0.7 | kept as a FAIL (a real PDK finding); S3 patches the gate pad (row 37) | S3 cells sign off (row 37); G0.7 still reports the bare PCell |
| 8 | S0 | 45 PVT points took too long one process at a time | run time | one ngspice process per corner looping over VDD and T, checked equal to separate runs | minutes, not hours |
| 9 | S2 | The dual method for phase 2 on large problems was wrong | a check against SLSQP | interior-point (trust-constr) above 200 elements, checked against SLSQP | same optimum |
| 10 | all | Review A, 17 findings on the v2 code before any run | review A (7.9) | 10 applied, 2 not (see 7.9) | |
| 11 | S2/S3 | First 5T after-run relaxed the input pair and tail: the expected need took each element's minimum over different cells, which no single cell achieves | S3 G3.5 FAIL, traced | the need comes from ONE representative cell per device type | 5T after: S3 PASS |
| 12 | S2 | S2 crashed: a baseline's huge resistance left no DC solution and ngspice hung for 600 s | S2 ERROR (TimeoutExpired) | a timed-out run is a failed run; scenarios time out at 180 s | S2 completes |
| 13 | hand layout | The extracted tile would not simulate: header continuation lines, ground on the `ena` pin, floating PEX metal | failed simulations | continuation lines joined, ports mapped, 1 Tohm shunts on every node (all netlists) | 18 runs, no warnings |
| 14 | git | GitHub Desktop could not join the repository's two-commit history (README created on GitHub) and stashed all uncommitted work, reverting fixes and deleting run logs mid-run | reverted code found in the container, then `git reflog` / `git stash list` | `git merge --allow-unrelated-histories origin/main` (no file changed, no force-push), stash restored into the working tree, runs restarted | your push went through |
| 15 | S1 | iadc S1 crashed in G1.4 (division by zero): the recogniser had put 24 of 38 dummies into 6 false mirrors | S1 ERROR, traced | dummies assigned first; iadc package regenerated (TTSKY25a output unchanged, checked) | G1.4 PASS |
| 16 | S0 | Your spec decision changed `config.yaml`; G0.3 refused the changed file | G0.3 (hash freeze) | the frozen hash updated on purpose, with the reason | G0.3 PASS |
| 17 | hand layout | Our "designers' conditions" run of the tile passed `MF=100` only, which in this PDK scales mismatch, not capacitance: 1 load unit instead of 100 | reading the PDK model while chasing 20, checked with ngspice | `MF=100 M=100`, re-run | tile PEX at ff/20 C: 1.43 MHz, 78.0 deg |
| 18 | all | Review B, 11 findings on the code and on this section's first draft | review B (7.9) | all 11 addressed | 7.5-7.8 rewritten |
| 19 | S2 | The baseline comparison was tilted: a failed SPICE run counted as a violation, the LP had no floors, only ours' worst corners were simulated | review B items 1-3 | failed runs apart; `lp_floor` baseline; each method's own worst corners; outcome words defined (PREREG amendment) | 7.6 re-run |
| 20 | S3 | Our explanation of the 5T area increase was wrong (we blamed gate resistance) | review B item 7, then the option table | the binding terminals are drain and source (8.0 ohm allowed; folded cells 8.5-17 ohm on one side) | 7.5 corrected |
| 21 | S2 | iadc phase 2 ran 2.5 hours: elements with zero need made the objective NaN | run time, NaN warnings in the log | objective without the need, strictly positive x, 300 s cap | minutes |
| 22 | S1 | A PDK capacitor's multiplier counted twice (ngspice reports C already x M); iadc model GBW = half of SPICE | G1.1 passive cross-check and G1.2 | value read as reported for C (R / M stays), checked with an ngspice test | iadc model vs SPICE 0.09 dB, 2.8 %, 0.18 deg; TTSKY25a 0.07 dB, 0.09 %, 0.06 deg |
| 23 | S1 | G1.1 counted dummies as unsaturated devices | iadc G1.1, reading the list | dummies excluded | 21 functional devices remain (triode by design, open question) |
| 24 | S2 | Saturation constraints for devices not saturated before layout: negative margins forced budgets to zero | inspecting iadc's constraints (83 sat constraints, many with b < 0) | only saturated devices get one; the others are listed in G2.0 | iadc budgets |
| 25 | S2 | G2.1 failed: placement rules may name a capacitor | iadc G2.1 | passives are valid names | G2.1 PASS |
| 26 | S3 | S3 stopped on iadc: cells of m > 1 devices were drawn with unconnected copies, none signed off | S3 ERROR | one unit cell per option, scaled to the device (area x m, R / m, C x m, `m=` in the circuit) | S3 runs on iadc and TTSKY25a |
| 27 | S0 | 18 TTSKY25a bindings failed their own negative control: L + 0.1 um is within Netgen's tolerance on 10-20 um channels | G0.7 | L + 10 % (at least 0.1 um) | G0.7 PASS |
| 28 | hand layout | iadc layout: separately drawn pieces of a labelled net come out as `VDD_uq3`, `p1_uq0` | unmapped ports in the run record | tied to their net | 6 runs, no warnings |
| 29 | hand layout | The R+C extraction read the C-only `.ext` and ignored the resistances | 0 resistors in the netlist, nonsense results | the R+C extraction runs in its own folder | 324 k resistors |
| 30 | hand layout | The R+C AC run of the iadc layout (324 k resistors) took over 4 GB next to the main queue and nearly pushed the container out of memory | memory check (260 MB left) | run stopped; KLU sparse solver, only the output vectors saved, a 2.6 GB cap per run, extresist tolerance as a parameter | runs at about 1.3 GB |
| 31 | S1 | TTSKY25a G1.4 failed: its bias mirrors are ratioed by channel length (L = 2, 10, 20 um on one gate), which the rule "a mirror shares L" calls inconsistent; S2 would then have asked for identical cells across different L | G1.4 | an L-ratioed mirror is recorded as such and its equal-L subsets are checked as mirrors | TTSKY25a re-run from S1 |
| 32 | infra | A queue waited forever on a stopped run whose process had become a zombie (`kill -0` succeeds on zombies) | the queue log did not move | queues wait on a log line, not a pid | |
| 33 | infra | A second agent (Claude Code on the laptop) and Cowork's deploys could silently overwrite each other's edits: Cowork unpacks its copy over the repo | your question about working with both, then reading the deploy step | `CLAUDE.md` (shared rules and protocol), `docs/STATUS.md` (live handoff), and a deploy step that refuses to overwrite a file changed since Cowork last saw it | no silent overwrite |
| 34 | S2 | After review B's fixes, the LP with floors came out "ok" on the 5T like ours, and the table could not tell them apart | reading the re-run table | budget / need (min and geometric mean) added: the LP with floors gives every element exactly its need, ours 3.2 x on the geometric mean | 7.6 |
| 35 | hand layout | The iadc R+C run gave 19.4 dB with gmin-stepping failures: the R+C netlist exposes the CMFB sub-cell's clock ports separately, and the bench left them floating | the run's own warnings (recorded per run since review B) and an implausible gain; Magic's "electrically shorted" warnings | `--map-shorted`: a port Magic reports as shorted to a mapped port is tied to that port's node | clean R+C run (7.8) |
| 36 | infra | The PC had to go off at 01:30 with about 6 h of runs left; the queues could not resume, and two of them set outputs aside in the container's /tmp | planning the overnight stop | `scripts/plan_v2_resume.sh`: every step writes a `.done` marker and is skipped next time, outputs set aside go to `runs/tmp/aside/` and are restored after an interruption, two lanes side by side; `scripts/plan_v2_stop.sh` stops everything in a safe order | runs continue with Claude Code (docs/HANDOFF.md) |
| 37 | S3 | iadc 'before' S3 stopped: its two 1.2/0.2 um LVT types had no signed-off cell. Every option iadc builds for them (nf = 1, in the sized W bin) failed met1.6, because the PCell's gate contact pad stays 0.290 x 0.230 um = 0.067 um2 at short L (also LOADBench's 484/0.24 nf = 1 cells) | S3 ERROR (`no built option`), then every met1 island of the failing cells measured: only the gate pads are below 0.083 um2 | the strap step widens a gate pad below the minimum area along the gate, away from the S/D strips, to 0.370 x 0.230 = 0.085 um2 (Imasha's suggestion); cells that failed DRC before the patch are rebuilt, signed-off cells are not | iadc 88 of 88 options signed off (was 80): DRC 0, LVS match, negative control still caught, cell size unchanged |
| 38 | S3 | LOADBench 'after' missed PM: 48.1° against ≥ 60° ('before' 64.9°). S2's budgets were starved at the PVT points, so all 6 types were relaxed, and a relaxed type keeps its default PCell. The 484/0.24 and 887/0.74 um devices became single fingers with 8.2 and 4.9 kohm of gate R. The 484 um cell only passed DRC after row 37's patch; before that, the fallback took nf = 8 | G3.3 FAIL, then the chosen cells' access R in `device_decisions.json`: the cells alone cost about 1° of PM, all cells with their access R 17.3° | none in the flow: the 'after' result stands. A 'least-bad' fallback (`--relax-fallback least-bad`: largest min_slack, access R included) is tested post hoc after the queue, in its own folder and snapshot column (Imasha's decision) | post hoc, not pre-registered, same inputs: LOADBench PM 64.7° (spec met), G3.3 passes, area 4396 → 2142 um2, the wide devices at nf = 64 (gate R 2–3 ohm); ota5t_stress area 257 → 206 um2 with GBW and PM slightly up; iadc and TTSKY unchanged (the least-bad option is the default cell). Adopted as the S3 default for later runs (PREREG amendment 2026-10-27; Imasha's decision); plan v2's results keep the old rule |
| 39 | infra | Windows put the PC into Modern Standby on idle timeout five times during the runs (06:59–11:16). The container slowed or paused, and a SPICE check slowed past its 180 s limit would count as a failed run ("unverified", a violation possibly hidden). The eta 0.9 runs of the 5T and LOADBench ran almost entirely in standby, and their logs were gone | the processes' run times were 28–32 min shorter than the wall clock; the Windows event log (Kernel-Power 506/507) | timeouts checked against the standby windows: one possible case (an iadc lp_floor check, no outcome change). The two eta 0.9 runs were re-run with the PC awake (app keep-awake), keeping their logs and a wall-clock vs uptime record | identical results: gates, outcomes, failed-run counts and worst use. For long runs, keep the PC awake |

### 7.2 New designs and what had to be predicted

| Design | Upstream gave | We predicted (labelled PREDICTED / ASSUMPTION) | Reproduction check |
|---|---|---|---|
| `loadbench_miller` (LOADBench, row 546 of 1024, chosen by a fixed rule) | sized netlist, ~1000 Pareto points with metrics, structure recognition, OP/AC/DC/tran benches | specs (gain −1 dB, GBW ×0.9 of our own simulation, PM ≥ 60°, power ≤ 1.1× LOADBench), noise bench, textbook two-stage Miller equations, MIM binding of the ideal Miller capacitor | G0.8: gain 58.00 vs 58.0 dB, GBW 23.39 vs 23.41 MHz, PM 65.32 vs 65.33°, power 558.4 vs 558.4 µW |
| `ttsky25a_fd` (your TTSKY25a op-amp) | xschem schematics, the designers' testbench, the taped-out GDS, README post-layout figures | flat netlist (xschem + `scripts/flatten_spice.py`), dido benches, specs from the schematic's own performance (gain -1 dB, GBW x 0.9, power x 1.1, PM >= 60 deg, as for LOADBench; the README/paper figures are post-layout results, and the designer chose the schematic as the reference), rule-based primitives, textbook two-stage FD equations | G0.8 against your own bench `Opamp_with_Bias_tb.sch` re-run (tt, 27 C default, open loop, 200 x 1x1 um MIM units per output; ours: chokes, 529 fF ideal): gain 98.401 vs 98.401 dB, GBW 2.0517 vs 2.0515 MHz, PM 78.234 vs 78.236°, power 451.98 vs 451.98 µW |
| `iadc_ota` (r09g/iadc) | netlist, hand-drawn layout with LVS/PEX netlists, transient benches only | AC model of the switched-capacitor CMFB (ideal CMFB with its steady-state law, C3/C4 kept), specs, primitives, textbook folded-cascode equations | no upstream AC figures exist (G0.8 not applicable) |

The rule-based structure recogniser (`scripts/recognize_structures.py`) was checked on the Miller against
LOADBench's own recognition: same differential pair and NMOS mirror; the two PMOS mirrors that share their
diode are one 3-device mirror in ours; the CS driver is a single device in ours and part of an "inverter"
in theirs.

**Which devices the flow treats as matched (TTSKY25a).** The upstream stage that would say which devices form
a differential pair, a mirror or a matched pair did not exist for this design, so the flow predicted it from
the netlist (`scripts/recognize_structures.py`, PREDICTED). The pictures are your own xschem schematics with
each group boxed and tagged (G1, G2, ...) under its SPICE name; the table maps each flat SPICE name to its
schematic instance (`XX1_M5` = M5 of Diff_opamp, `XX2_M7` = M7 of Common_source_stage, `XM33` = M33 of
Opamp_with_bias). You accepted these groups on 2026-10-26. G6-G8 and G14-G15 are the two mirrors whose
devices differ in channel length (journey #31): the flow matches only devices of equal length within them.
Regenerate with `python3 scripts/schematic_groups.py ttsky25a_fd`.

![Diff_opamp with the flow's groups](flow_record/img/ttsky25a_fd_groups_Diff_opamp.svg)

![Common_source_stage with the flow's groups](flow_record/img/ttsky25a_fd_groups_Common_source_stage.svg)

![Opamp_with_bias (top level, bias) with the flow's groups](flow_record/img/ttsky25a_fd_groups_Opamp_with_bias.svg)

| G | kind | devices (SPICE name -> schematic instance) | sheet |
|---|---|---|---|
| G1 | nmos-differential-pair | XX1_M5 -> M5, XX1_M6 -> M6 | Diff_opamp |
| G2 | nmos-differential-pair | XX1_M18 -> M18, XX1_M16 -> M16 | Diff_opamp |
| G3 | nmos-differential-pair | XX1_M10 -> M10, XX1_M17 -> M17 | Diff_opamp |
| G4 | pmos-differential-pair | XX2_M7 -> M7, XX2_M8 -> M8 | Common_source_stage |
| G5 | nmos-current-mirror | XM33 -> M33, XM37 -> M37, XM41 -> M41 | Opamp_with_bias |
| G6 | nmos-current-mirror ratioed by L, subset 1 (single device: nothing to match) | XX1_M46 -> M46 (L = 2 um, the reference diode) | Diff_opamp |
| G7 | nmos-current-mirror ratioed by L, subset 2 | XX1_M1 -> M1, XX1_M2 -> M2, XX1_M7 -> M7, XX1_M9 -> M9 (L = 10 um) | Diff_opamp |
| G8 | nmos-current-mirror ratioed by L, subset 3 | XX1_M22 -> M22, XX1_M15 -> M15 (L = 20 um) | Diff_opamp |
| G9 | nmos-current-mirror | XX1_M23 -> M23, XX1_M24 -> M24 | Diff_opamp |
| G10 | nmos-current-mirror | XX2_M10 -> M10, XX2_M11 -> M11 | Common_source_stage |
| G11 | nmos-current-mirror-load | XX2_M5 -> M5, XX2_M6 -> M6 | Common_source_stage |
| G12 | pmos-current-mirror | XM39 -> M39, XM38 -> M38 | Opamp_with_bias |
| G13 | pmos-current-mirror-load | XX1_M20 -> M20, XX1_M21 -> M21 | Diff_opamp |
| G14 | pmos-current-mirror ratioed by L, subset 1 (single device) | XX2_M12 -> M12 (6/1 um, diode) | Common_source_stage |
| G15 | pmos-current-mirror ratioed by L, subset 2 (single device) | XX2_M3 -> M3 (1/5 um) | Common_source_stage |
| G16 | nmos-matched-cascode-pair | XX1_M19 -> M19, XX1_M4 -> M4 | Diff_opamp |
| G17 | nmos-matched-cascode-pair | XX1_M3 -> M3, XX1_M8 -> M8 | Diff_opamp |
| G18 | nmos-matched-current-source-pair | XX2_M2 -> M2, XX2_M1 -> M1 | Common_source_stage |
| G19 | pmos-matched-current-source-pair | XM32 -> M32, XM34 -> M34 | Opamp_with_bias |
| G20 | pmos-matched-current-source-pair | XM43 -> M43, XM44 -> M44 | Opamp_with_bias |
| G21 | pmos-matched-current-source-pair | XM45 -> M45, XM54 -> M54 | Opamp_with_bias |
| G22 | pmos-matched-cascode-pair | XX1_M11 -> M11, XX1_M12 -> M12 | Diff_opamp |
| G23 | pmos-matched-current-source-pair | XX1_M13 -> M13, XX1_M14 -> M14 | Diff_opamp |

### 7.3 What the old flow did on the new circuits, and the generality fixes

The v1 code stopped in S0 on LOADBench (`unsupported element 'Ibias'`): correct behaviour, because the
parser refuses what it does not model. Reading the code behind that refusal found two silent bugs that would
have followed:

1. **The Miller capacitor would have vanished.** S0's IR did not record passives at all, so the linear
   model's guard (`if ir.get("passives")`) could never fire, and the layout view dropped every passive.
2. **An ideal current source's node was AC ground.** The linear model grounded the nodes of every internal
   source; that is right for a voltage source and wrong for a current source (open circuit).

Fixed without changing any algorithm: current sources; ideal and PDK passives (MIM, poly resistors) in the
IR, the linear model, the layout view and the PCell binding; off-chip test elements; port roles; external
reference gate G0.8; differential outputs and dido benches; benches found by name; PDK passive values read
from the simulator; dummies skipped in the resistance sensitivities. After these, the Miller's linear model
matches SPICE to 0.017 dB, 0.36 % GBW and 0.03° PM (G1.2), with the Miller capacitor stamped.

Further findings while ingesting:

- **The PDK PCell at the netlist's own size is not always DRC-clean.** LOADBench's single-finger NMOS
  (W = 484 µm, L = 0.24 µm) gives 6 × met1.6 (minimum area) violations with default options (G0.7 FAIL).
  S3 must finger it.
- **m > 1 PCells are drawn as unconnected copies.** All TTSKY25a devices are m = 2; S0's device LVS assumed
  one connected device and failed 95 of 96 bindings. Fixed by checking the copies as drawn (extracted
  connectivity, netlist W/L/nf, device count, negative control with L changed). S3 had the same problem one
  stage later: its option cells were drawn with the m copies unconnected, so none signed off and S3 stopped
  on iadc_ota. S3 now builds one unit cell (m = 1) per option and scales it to the device: area x m (an upper
  bound until S4 places the copies), access resistance / m, the cell's capacitance x m in S2's floors and
  needs, and an `m=` instance multiplier when the cell replaces the device in the circuit simulations.
- **The textbook models (our predictions of the upstream symbolic stage) are optimistic** in the same way
  as the 5T "pole drop-out": Miller PM 82.3° predicted vs 65.3° SPICE, GBW +29 %.
- **A negative control that cannot fail.** The device LVS negative control changed L by a fixed 0.1 um; on
  TTSKY25a's long-channel devices (L = 10 and 20 um) that is within Netgen's relative tolerance, so the wrong
  reference matched and 18 bindings failed their own control. The change is now 10 % of L (at least 0.1 um).
- **The rule-based recogniser had put dummies into mirrors.** A dummy with drain, gate and source on one net
  looks diode-connected, so on iadc_ota 24 of the 38 dummies formed 6 false blocks (one a 10-device "PMOS
  mirror load"), and S1's matching check divided by their zero gm. Dummies (gate tied to source, or all
  terminals on the rails) are now assigned first; the iadc package was regenerated (48 -> 67 blocks). The
  TTSKY25a output is unchanged (checked), LOADBench uses its own recognition, and S1's matching check now
  reports a device that is off instead of crashing.
- **A PDK capacitor's multiplier was counted twice.** ngspice reports a MIM capacitor's value already
  multiplied by the instance multiplier M (four 4.8 x 4.8 um units read 196 fF), and S1 multiplied by M
  again. On iadc_ota the CMFB capacitors C3/C4 became 784 fF and the linear model's GBW was half of SPICE's
  (105 vs 210 MHz). G1.1's cross-check of every PDK passive against the simulator flagged it (rel. diff
  -0.75). Fixed in `op.passive_value` (resistors are reported per copy, so R / M stays); after the fix the
  model matches SPICE to 0.09 dB, 2.8 % GBW and 0.18 deg. TTSKY25a's Miller capacitors (M = 5) would have
  been hit the same way; its runs are after the fix.
- **Saturation constraints for devices that are not saturated.** S2 made one per device, so a dummy or a
  MOS resistor (iadc_ota: 21 functional devices below BSIM's vdsat, 15 of them in five series stacks with the
  gate at cm, i.e. triode by design) gave a negative "margin" that forces every budget touching it to zero.
  Now only devices saturated before layout get one; the others are listed in G2.0. G1.1 still fails on
  iadc_ota for those 21 devices (dummies are no longer counted): it is the BSIM vds > vdsat test, and the
  design intent of each device is the designer's to state, not ours to assume.
- **The large phase-2 solver could run for hours.** With more than 200 elements (iadc_ota: 756) phase 2 uses
  an interior-point solver; elements with zero expected need made its objective NaN. The objective no longer
  depends on the need, and the solve is capped at 300 s (the phase-1 budgets are kept past it).
- **The repository's schematic is not the taped-out circuit.** The TTSKY25a tile layout extracts to 86
  merged devices vs 58 in `Opamp_with_bias.sch` (a bias switch block, bias dummies, more MIM units and
  resistors). See 7.6.

### 7.4 What v2 changes (code)

| Stage | Change | Gate |
|---|---|---|
| S0 | 45 PVT points (5 corners × VDD ±10 % × −40/27/85 °C), run as one ngspice process per corner (checked equal to separate runs); 200-run mismatch Monte Carlo (tt_mm, one seed per run) | G0.9, G0.10 (info) |
| S2 | Library floors: no element below what the cheapest cell of the S3 library (main mode A-bin) puts on it; expected need from ONE representative cell per type (not per-element minima, which no single cell achieves) | G2.7 |
| S2 | R19 fix: phase 2 never trims an element below min(phase-1 budget, need) nor below its floor | G2.3 |
| S2 | One constraint per spec and PVT point where the sized circuit meets the spec (exact linear model at that point's operating point; resistance rates: nominal + change); SPICE checks of the binding corners | G2.9, G2.5 |
| S2 | Three other budget rules on the same sensitivities and the same eta, scored first order and in SPICE: per-net (SpiceXplorer's rule), equal split, a plain LP (maximise the sum of budget/need) and the same LP with the library floors and budgets capped at need; eta sweep 0.3–1.0 | G2.8 |
| S3 | Option modes B / A-bin / A-free + rule-of-thumb folding (finger 4 µm); wide-device nf 16–64; v2 R allowance (a cell may use the library's lowest access R of its terminal) | G3.7 |

An independent review agent read the v2 code before the runs; its 17 findings and what was done with each
are in 7.9.

### 7.5 Results before and after

**example_ota_5t** (before = v1, after = v2; both S2 and S3 PASS):

| | before (v1) | after (v2) |
|---|---|---|
| S3 cells (PMOS load / input pair / tail) | nf2 / nf2 / nf4 | nf1 / nf1 / nf2 |
| total device area | 187.2 um2 | 237.0 um2 (+27 %) |
| final gain / GBW / PM (cells in the circuit) | 32.88 dB / 101.9 MHz / 79.84 deg | 31.80 dB / 102.4 MHz / 79.63 deg |
| fingers outside the sized device's W bin | (not checked in v1) | none (A-bin) |

Why v2 costs area here: S2's round 1 is now bound by a PVT point, GBW at tt, VDD −10 %, 27 C (point tt_v0.9_t27, G2.9), not by
the nominal margins, so every budget sits at its need (t = 1.05). The input pair's gate then gets only the
library's lowest gate resistance (273 ohm), which one of its 12 cells has: the unfolded default. In v2's other
modes: B (nf as in the netlist) 254.5 um2 with the tail relaxed; A-free 232.0 um2 but the tail's 6 um fingers
leave the sized W bin; rule-of-thumb folding 190.5 um2 with all three types over their allowances. So the area
v1 saved came from nominal-only budgets and, for the tail (nf4, 6 um fingers), from a finger in another model bin.

**ota5t_stress** (eta 0.9; the 5T with a 200 fF load and tight specs):

| | before (v1) | after (v2) |
|---|---|---|
| S2 gates | PASS | G2.7 FAIL: the library's cheapest cells do not fit |
| S2 round-1 t (budget / need) / elements starved | 1.00 / 11 of 21 | 0.26 / 20 of 21 |
| PVT constraints | none | 83 |
| budgets in SPICE, worst use / allowed | 0.84 (GBW, nominal) | 0.89 (GBW at ss, 1.1 V, 85 C) |
| S3 | G3.5 FAIL: 2 device types relaxed | G3.5 FAIL: 3 device types relaxed |
| total device area | 206.9 um2 | 256.6 um2 |
| final gain / GBW / PM | 32.22 dB / 369.2 MHz / 63.65 deg | 31.75 dB / 356.3 MHz / 62.41 deg |

Both versions end with S3 relaxing cells: at eta 0.9 this design does not fit. The difference is where the
flow says so. v1's S2 passed with 11 of 21 budgets below their expected need, and S3 found out by relaxing two device types.
v2's S2 fails G2.7 before any cell is chosen, names the binding point (GBW at ss, 1.1 V, 85 C, where the
margin is 7.8 MHz against 37.4 MHz nominal), and gives the number: the cheapest library cells alone use
1.26 x eta x that margin.

(loadbench_miller, ttsky25a_fd, iadc_ota: filled when their after-runs end)

### 7.6 Joint vs per-net budgets: the three-outcome result

Five budget rules on the same sensitivities, the same eta and the same constraints (nominal + PVT points),
scored two ways: first order (the sum the rule assumed) and in SPICE (every budget that hurts a spec inserted
into the transistor netlist at once, at each rule's own most-used PVT points; one common set of checks per
design). The words follow PREREG's amendment (review B, item 3):

- **unsafe**: use / allowed > 1 in SPICE or first order (the layout would eat more than eta x margin);
- **infeasible**: an element budgeted below its library floor, i.e. below what the cheapest S3 cell already
  adds there, so no layout can meet it ("starved" = below the expected need, a softer signal);
- **ok**: neither. A SPICE run that fails (no DC solution, timeout) is listed apart and marks the outcome
  "unverified", never a violation (review B, item 1).

The last numeric column says how much room a rule leaves the layout: budget / expected need, minimum and
geometric mean over the budgeted elements. The tables below are the re-runs after review B
(`docs/before_after.md`); the first version of the 5T table counted per-net's one failed run as a GBW violation.

**example_ota_5t** (eta 0.5, 21 elements, 103 PVT constraints, 19 SPICE checks):

| Rule | Use / allowed, 1st order | Use / allowed, SPICE | Failed runs | Starved | Below floor | Budget / need, min / geomean | Outcome |
|---|---|---|---|---|---|---|---|
| per-net (SpiceXplorer's rule) | 4.21 | 1.71 | 1 | 0 | 0 | 1.77 / 8.68 | **unsafe** |
| equal split | 0.62 | 1.21 | 0 | 4 | 2 | 0.11 / 3.53 | **unsafe + infeasible** |
| plain LP (max sum of budget / need) | 1.00 | 1.77 | 1 | 4 | 4 | 0 / 0.03 | **unsafe + infeasible** |
| LP with floors, capped at need | 0.95 | 0.29 | 0 | 0 | 0 | 1.00 / 1.00 | **ok** |
| ours (joint max-min, floors, PVT) | 1.00 | 0.65 | 0 | 0 | 0 | 1.00 / 3.19 | **ok** |

Two rules are safe and feasible on the 5T. The LP with floors reaches that by giving every element exactly its
expected need (it is capped there, as review B asked, so that it does not sit on vertices at 0 or 10 x need):
any net that comes out above its estimate breaks it. Ours is as safe in SPICE (0.65 of the allowance) and leaves
the layout 3.2 x the expected need on the geometric mean; the elements at 1.0 are the ones the GBW point at tt,
0.9 V, 27 C binds. Per-net budgets each net as if it were alone and overshoots the allowance 1.7 x in SPICE;
equal split and the plain LP put elements below the cheapest library cell.

**ota5t_stress** (eta 0.9, 21 elements, 83 PVT constraints, 22 SPICE checks): no rule works, and S2 says so
before any layout (G2.7 FAIL). At ss, VDD +10 %, 85 C the GBW margin is 7.8 MHz (37.4 MHz nominal), and the
cheapest library cells alone use 1.26 x eta x that margin, so the LP with floors falls back to no floors.

| Rule | Use / allowed, 1st order | Use / allowed, SPICE | Specs violated in SPICE | Failed runs | Starved | Below floor | Budget / need, min / geomean | Outcome |
|---|---|---|---|---|---|---|---|---|
| per-net | 10.5 | 8.96 | GBW nominal and at 6 PVT points, PM at 5, gain at 1 | 0 | 1 | 0 | 0.90 / 5.16 | **unsafe** |
| equal split | 0.76 | 0.74 | none | 0 | 13 | 11 | 0.06 / 0.73 | **infeasible** |
| plain LP | 1.00 | 11.2 | GBW at sf, 1.0 V, 27 C | 8 | 11 | 11 | 0 / 0.00 | **unsafe + infeasible** (unverified) |
| LP with floors (floors dropped) | 1.00 | 9.02 | GBW at 2 points | 9 | 6 | 4 | 0 / 0.005 | **unsafe + infeasible** (unverified) |
| ours | 1.00 | 0.98 | none | 0 | 20 | 15 | 0.26 / 0.31 | **infeasible** |

Ours is the only rule that stays inside the allowance in SPICE here, and it reports the design as infeasible
instead of handing out budgets that a layout cannot meet. Equal split also stays inside, but by starving 13 of
21 elements; the two LPs put many elements at zero, and those circuits often have no DC solution in SPICE.

(other designs: to be filled)

### 7.7 The hand-drawn TTSKY25a layout measured the flow's way

`scripts/reference_ttsky25a.sh` extracts the taped-out tile `tt_um_diff` with Magic (an LVS netlist, and a PEX
netlist with every capacitance, cthresh 0, no wire resistance) and simulates three netlists in the flow's own
dido benches (DC feedback through chokes, differential output, 1 Tohm shunts on every node in all three runs):
the flow's DUT (`Opamp_with_bias.sch`), the tile's drawn devices without parasitics, and the tile's PEX. Tile
pins: en_1 = 1.8 V, en_2 = 0. All 18 simulations ended with rc 0 and no numerical warnings
(`outputs/reference_layout/ttsky25a_fd/reference_layout*.json`, key `runs`).

| Conditions | Netlist | Gain (dB) | GBW (MHz) | PM (deg) | Power (uW) |
|---|---|---|---|---|---|
| flow bench: tt, 27 C, ideal 529 fF loads | schematic (flow DUT) | 98.39 | 2.052 | 78.23 | 452.0 |
| | tile, drawn devices only | 108.12 | 1.530 | 80.56 | 481.2 |
| | tile, PEX | 108.11 | 1.426 | 77.60 | 481.2 |
| designers' `gain_and_phase.sch`: ff, 20 C, 100 x (1x1 um) MIM units per output | schematic | 97.53 | 2.073 | 78.66 | 588.3 |
| | tile, drawn devices only | 108.49 | 1.537 | 80.87 | 618.8 |
| | tile, PEX | 108.47 | 1.430 | 77.98 | 618.8 |
| tt, 27 C, the same 100 MIM units | schematic | 98.39 | 2.052 | 78.84 | 452.0 |
| | tile, drawn devices only | 108.12 | 1.529 | 81.16 | 481.2 |
| | tile, PEX | 108.11 | 1.424 | 78.18 | 481.2 |

ICM 2026 paper / README (post-layout simulation, reported): gain ~100 dB, GBW 2.3 MHz, PM 52 deg, CMRR ~91 dB at
1 kHz, power ~500 uW.

What this says, and what it does not:

1. **Drawn -> PEX (capacitance only) costs** GBW -6.8 to -6.9 %, PM -2.9 to -3.0 deg, gain -0.01 dB, power 0,
   at all three condition sets. This is the hand layout's wiring capacitance, the quantity S2 budgets. Wire
   resistance is not extracted, so it is a lower bound of the layout's cost.
2. **The tile is not the repository's schematic.** LVS of the tile against the flow's layout view fails (86
   merged devices against 58: a bias switch block, bias dummies, and a MIM network of four groups of 8 x
   10x10 um units plus 3 units per output, against 5 units per Miller capacitor). Without any parasitic, the
   tile's devices give +9.7 dB gain, -25 % GBW and +29 uW against the schematic at the same conditions.
   The designer kept the schematic as the flow's DUT (2026-10-26).
3. **Under the flow's specs the tile fails GBW before any wiring.** The specs are the schematic's own
   performance (GBW >= 0.9 x 2.052 = 1.85 MHz), and the tile's drawn devices give 1.53 MHz. Its wiring loss,
   0.104 MHz, is 51 % of the schematic's 0.205 MHz GBW margin, above eta = 0.5: a layout of the tile's wiring
   quality would not fit the budget of this spec rule. This depends on the x 0.9 rule, so the comparison with
   S2's G2.0 prediction is read as a ratio of losses, not as pass or fail.
4. **The paper's 2.3 MHz / 52 deg is not reproduced** by either netlist, even at the designers' own bench
   conditions (1.43 MHz / 78.0 deg for the tile's PEX, 2.07 MHz / 78.7 deg for the schematic). How that run
   was set up (extraction tool, wire resistance, which netlist) is not in the repository: open question.
5. With en_2 = 1.8 V the drawn devices still give 108.4 dB but the PEX gives 3.8 dB: a different DC solution
   (start-up / bias bistability or a numerical artefact), not a capacitance effect. Not investigated; with
   both enables at 0 neither netlist converged.

Correction recorded here: the first runs of the MIM-load condition sets (14:14) passed only `MF=100`, which in
this PDK scales the mismatch term, not the capacitance, so they had one 1x1 um unit (2.6 fF) per output. The
table above is from the corrected runs (`MF=100 M=100`); the PEX loss changed by less than 0.003 MHz.

### 7.8 The hand-drawn iadc_ota layout, and a first test of G2.0

`scripts/reference_iadc.sh` measures the upstream layout (`layout/ota/ota.gds`, cell `ota`) the same way. The
layout contains the switched-capacitor CMFB; in the AC benches its clocks are held in phase 1 (p1 = VDD,
p2 = 0) and its output node cmc is driven by the same ideal CMFB law as the flow's AC model (ASSUMPTION), so
the outputs see C3/C4 to cmc as in the model. Magic names separately drawn pieces of a labelled net
`<name>_uqN` (VDD_uq3, p1_uq0); they are tied to their net. 6 runs, rc 0, no warnings. LVS against the flow's
layout view fails as expected (the layout has the CMFB's switches and capacitors).

| tt, 27 C, 0.3 pF loads | Gain (dB) | GBW (MHz) | PM (deg) | Power (uW) |
|---|---|---|---|---|
| schematic AC model (flow DUT) | 53.47 | 209.9 | 77.2 | 757.9 |
| layout, drawn devices only | 53.60 | 171.9 | 82.1 | 757.2 |
| layout, PEX (all capacitance) | 53.60 | 156.2 | 81.2 | 757.2 |

- **Wiring capacitance (drawn -> PEX): GBW -15.6 MHz (-9.1 %), PM -0.9 deg, gain 0.**
- **Drawn devices vs the schematic model: GBW -18 %.** This is not only layout: the drawn circuit also has the
  CMFB's switches and sampling capacitors on its nodes and the as-drawn diffusion areas. Not separated yet.
- **G2.0, wiring part (the 'before' S2 run, v1):** S2 predicts, before any layout, that the estimated wiring
  capacitance of a compact layout costs GBW 15.5 MHz (0.74 of the 21 MHz margin), PM 2.4 deg and gain 0. The
  hand layout's wiring costs 15.6 MHz, 0.9 deg and 0. GBW agrees to 1 %, PM is over-predicted 2.7 x. One
  circuit and one number each: a first data point for the G2.0 validity hypothesis (PREREG: within 25 %), not
  a confirmation. G2.0's total (3.7 margins of GBW) is dominated by the expected terminal resistances (3.0
  margins), which this capacitance-only PEX cannot test.

**R+C extraction of the same layout** (Magic extresist, tolerance 100; 324 k resistors; KLU;
`outputs/reference_layout/iadc_ota/reference_layout_rc100s.json`). The first run was not usable: gmin stepping
failed and it gave 19.4 dB of gain. The cause was in the netlist, not in the solver. The R+C netlist exposes
the CMFB sub-cell's ports (`sc_cmfb_0.p1`, the transmission gates' enables, ...) as separate ports. Magic
reports them as electrically shorted to the top-level clocks, but the bench left them unconnected, so switch
gates floated. With `--map-shorted` each such port is tied to the node of the port it is shorted to; the
re-run has rc 0 and no warnings.

| tt, 27 C, 0.3 pF loads | Gain (dB) | GBW (MHz) | PM (deg) | Power (uW) | Output CM (V) |
|---|---|---|---|---|---|
| layout, drawn devices only | 53.60 | 171.9 | 82.1 | 757.2 | 0.924 |
| layout, capacitance only | 53.60 | 156.2 | 81.2 | 757.2 | 0.924 |
| layout, R + C | 57.24 | 153.7 | 78.7 | 773.4 | 0.856 |

| Loss from the drawn devices | G2.0 'before' predicts: C / R | layout: C only | layout: R + C | layout's R part (R+C − C) |
|---|---|---|---|---|
| GBW (MHz) | 15.5 / 62.1 | 15.6 | 18.2 | 2.5 |
| PM (deg) | 2.38 / 2.53 | 0.88 | 3.34 | 2.46 |
| gain (dB) | 0 / 2.88 | 0 | −3.64 (a gain increase) | −3.64 |

- **The resistance moves the operating point.** Output common mode drops by 68 mV and supply current rises
  2 %: IR drop on the hand layout's bias and supply wiring. The 3.6 dB gain *increase* comes with that DC
  shift, so the gain row is not a parasitic loss in G2.0's sense. G2.0's linear rates cannot predict a DC
  shift of this size. S2's DC saturation constraints cover part of it, but only per device.
- **PM: the R part agrees** (2.53 predicted, 2.46 measured).
- **GBW: the R part is over-predicted 25 x** (62.1 MHz predicted, 2.5 MHz measured). 52 of the 62 MHz come
  from the access resistance of v1's expected cells: the as-sized single-finger default PCell, whose gate
  and straps run the full width of one long finger. The hand layout draws its wide devices with many fingers. That is what v2 changes:
  the expected need comes from the S3 library's representative cell (7.4). Whether v2's G2.0 is closer is
  read from the 'after' run (below).
- One circuit, one layout. The C part of GBW agreeing to 1 % is encouraging; the R part shows that G2.0 is
  only as good as its assumed cells.

### 7.9 Independent reviews of v2

Two independent review agents read the code, with no access to our conclusions beyond what the files say.
Code comments cite their items as "review item N" (review A, before the runs) and "review B, item N" (after the
first runs, on the code and on this section's first draft).

**Review A (before the runs, 17 findings).** Applied: phase 2 keeps a hair of room above pinned elements (1);
the constraint check's tolerance is the solver's (2); S3's per-device share comes from the same cell (3); an
option that adds nothing to an element counts as 0 there (4); S3's cache is written back so S2's floors read the
same values (5); nets that touch only passives get a wiring estimate (7); a PVT point without a linear-model
rate gives no constraint instead of a vacuous one (8); corner resistance rates are the nominal rate plus the
linear-model change (9); corner checks break ties by the smaller margin (10); only options of S3's main mode
set the floors (15). Not applied: S3 still checks at the nominal point only (a limitation, 7.10), and the
concern about MF and m on PDK passives, where we kept the rule "value x M" and relied on G1.1's cross-check of
every PDK passive against the simulator. That cross-check then failed on iadc_ota (C3/C4 read as 784 fF
against 196 fF): ngspice already reports a capacitor's value multiplied by M, so S1 counted M twice (fixed,
`op.passive_value`; resistors are reported per copy, so R / M stays).

**Review B (after the first runs, 11 findings).**

| # | Finding | Done |
|---|---|---|
| 1 | A failed SPICE run (timeout, no DC solution) was counted as a spec violation, and plotted as 0 | failed runs are listed apart and never counted as violations; missing values are not drawn; 7.5 re-run |
| 2 | Baselines did not get the library floors, and the plain LP sits on vertices (budgets at 0 or 10 x need) | new baseline `lp_floor`: same LP with floors and budgets capped at need; the plain LP kept and renamed (no "Choudhury-style") |
| 3 | SPICE checks were picked from ours' binding corners; outcome words did not follow the stated rule | each method's own most-used corners are checked (one common set); outcome = unsafe / infeasible / ok from use / allowed, floors and SPICE |
| 4 | `reference_layout` compared off-nominal runs with nominal margins; MIM-load regex could silently do nothing | no comparison off nominal; drawn - PEX loss reported per run; rc and warnings recorded; the load replacement must match; MF=100 alone gave 1 unit (re-run) |
| 5 | The hand-layout section (now 7.7) overstated (PEX trust, LVS not reported, tile vs schematic, spec rule) | rewritten: LVS result, 18 runs without warnings, the tile fails the derived GBW spec before wiring |
| 6 | Recogniser: rail-gated off devices missed, native / MOS-cap devices mis-labelled, case-sensitive rails | polarity-aware off test, native excluded, MOS capacitors, no rail-gated device in a pair; TTSKY25a and iadc outputs unchanged (checked) |
| 7 | The results section (now 7.5) attributed the 5T area to PVT budgets without the ablation, and the gate-R story contradicted 1/nf^2 | ablation without PVT constraints run; rewritten from the option table (the binding terminals are drain and source, not gate) |
| 8 | `specs_from_achieved` silently skipped missing values and replaced config specs | a missing value or two rules for one spec stop S0; each spec's source is recorded in G0.6 |
| 9 | G1.4 passed matched groups with a nearly-off member | a member below 1e-3 of the group's largest gm makes the group inconsistent |
| 10 | Before/after snapshots could pick up a stale report after a crash | a report older than the start of an ERROR stage is marked stale |
| 11 | Minor: timeout decoding, silent `with_conditions`, G0.8 bench, block count | decode with replacement, stderr kept, `timed_out` flag; `with_conditions` raises when a line is missing; 48 - 6 + 24 + 1 = 67 blocks (XX1_M3 left its false cascode pair as a single) |

### 7.10 Limitations and open questions

- **S3 checks at the nominal point only.** S2's budgets cover the PVT points; S3's in-circuit check of the
  chosen cells does not yet (review A).
- **The hand-layout comparisons rest on two layouts, and on one R+C extraction.** iadc has a clean R+C run (7.8,
  rows 29, 30, 35); the TTSKY25a tile's is next. G2.0's resistance part has one data point.
- **The TTSKY25a tile is a later circuit than the schematic** (7.7); only its drawn -> PEX loss is comparable.
- **The ICM 2026 paper's 2.3 MHz / 52 deg** is not reproduced: how was that post-layout run set up? (to you)
- **iadc G1.1:** 21 functional devices are below BSIM's vdsat (15 in MOS-resistor stacks, 6 current sources
  at vds 0.10-0.21 V). Is each intended? The flow does not assume design intent (to the iadc authors' docs).
- **PREREG headline eta:** the SPICE-scored baseline comparison runs at each design's eta, not at 0.9 for all
  (amendment); a run at 0.9 is still to do.
- **Area of m > 1 devices** is m x the unit cell, an upper bound until S4 places the copies.

