# STATUS: live handoff between Claude Code, Cowork and Imasha

Read this file first and update it when you start or stop work (see `CLAUDE.md`, "Working together"). Times are given in container time (CET).

**Last updated:** 2026-10-27 17:15 CET (21:45 Sri Lanka time), by Cowork (Plan v3 review pack finished; nothing running; decisions D1–D10 wait for Imasha).

## Handoff to Cowork (2026-10-27 13:35 CET)

Claude Code stopped here at Imasha's request. She will run Cowork on this folder for the documentation.

- **State:** all plan-v2 runs are finished, and nothing is running or set aside. (Cowork, later: Imasha committed
  today's runs as `1aa7f791 "v1_v2_handoff"`, 17:54 Sri Lanka time; the documentation pass after it is uncommitted.)
- **Where the results are:**
  - `docs/before_after.md`: every design, every snapshot tag (before, after, after_nopvt, after_eta0.9,
    after_eta0.9_rerun, after_posthoc_leastbad), the budget-rule tables at eta 0.9 (PREREG headline) and the
    hand-layout vs G2.0 table.
  - Below in this file: *Recent results* (with the reading of each result), *Open questions* and *Pending tasks*.
  - The day's story is in `docs/progress_log.md` (the 2026-10-27 entry) and flow record 7.1, rows 37–39.
- **Documentation still to write** (Pending tasks 2, 3, 6–8):
  - flow record 7.5 (before/after for loadbench, iadc, TTSKY, with the post-hoc test as its own labelled
    column);
  - 7.6 (budget rules at eta 0.9);
  - 7.8 (hand layouts against the 'after' G2.0);
  - the slides, project doc 13 and the independent review.
- **Rule change to carry into the write-up:** from 2026-10-27, S3's rule for relaxed types is 'least-bad'
  (PREREG amendment). Plan v2's results used the old rule and stay as recorded.
- **Open technical items, not documentation** (Pending tasks 1, 1a–1c): `./flow test` on the new golden
  snapshots; TTSKY tile R+C not trusted (gmin stepping); the ota5t_stress drift between 2026-10-26 and today;
  the resume script's latent eta 0.9 bug.

## Running (container `layout-s0s3`)

**Nothing.** Every plan-v2 run had ended by 13:04:39 CET. `runs/tmp/aside/` is empty, so no design's outputs are
left set aside. The results are under *Recent results*.

| Script | Ended (CET) | What it did |
|---|---|---|
| `scripts/plan_v2_laneA_now.sh` (side lane) | 09:25, exit 0 | lane A: iadc 'before' S3, LOADBench 'after', iadc 'after', iadc hand layout |
| `scripts/plan_v2_resume.sh`, first pass, lane B | 10:08 | TTSKY 'before' and 'after', hand tile, tile R+C |
| `scripts/plan_v2_after_queue.sh` | 12:40, exit 0 | stopped the paused first pass at 10:08:47 and ran the resume script's second pass (no-PVT ablation, eta 0.9 for all 5 designs, golden snapshots, report; 10:08–12:36, 33 steps done in all), then the post-hoc 'least-bad' S3 on 4 designs (12:36–12:40) |
| `scripts/plan_v2_eta09_rerun.sh` | 13:04, exit 0 | S2 at eta 0.9 again for example_ota_5t and loadbench_miller, with the PC awake, and the comparison |

- **New outputs:**
  - `outputs/posthoc/least_bad/<design>/` (snapshot tag `after_posthoc_leastbad`);
  - `outputs/posthoc/eta09_rerun/`, with `compare.json` and per design `S2/` and `clock.json` (snapshot tag
    `after_eta0.9_rerun`);
  - `docs/before_after.md`, regenerated at 13:04 with every column.
- For GitHub Desktop: the post-hoc folders add 41 files, about 20 MB. Their `sim/` and `S2/work/` folders are
  git-ignored.
- The post-hoc folders were seeded with the 'after' runs' `sim/` folders: TTSKY, LOADBench and ota5t_stress at
  11:41–11:48, iadc at 12:11 (file counts checked). S3 reuses a simulation only when the deck text is identical and the run's exit code
  was 0, so the results equal a fresh run's. Each post-hoc S3 took 0.5–1.5 min.
- **Standby, for future runs.** Windows put the PC into Modern Standby on idle timeout five times this morning,
  between 06:59 and 11:16 CET, which slowed the runs. There was no standby after 11:16; the app has held the PC
  awake since 12:00.
  - For long runs, set Windows Settings → System → Power → "Make my device sleep after" to Never when plugged in,
    or keep a Claude session working.
  - The re-run's `clock.json` shows wall clock 5 % ahead of container uptime even with the PC awake (25–32 s per
    run). That is the Docker VM's normal clock drift, so only a much larger jump means a standby.

Earlier history of this run:

- 05:30: `scripts/plan_v2_resume.sh` started, with two lanes.
- 05:55: lane A stopped. iadc 'before' S3 had no DRC-clean cell for its 1.2/0.2 µm LVT devices. Fixed at 06:18
  by the gate-pad met1.6 patch.
- 06:26–06:27: the main script was paused (`kill -STOP 49`) and lane A's steps were restarted as
  `scripts/plan_v2_laneA_now.sh` (Imasha's decision), next to lane B.
- 08:40: `scripts/plan_v2_after_queue.sh` started; it took over at 10:08 and ended at 12:40.
- 11:59: `scripts/plan_v2_eta09_rerun.sh` started (Imasha's decision); it ran 12:40–13:04.
- **Logs:**
  - first pass: `runs/logs/plan_v2_resume_pass1.log`, `plan_v2_lane_A_pass1.log` (the 05:30 attempt) and
    `plan_v2_lane_B_pass1.log`;
  - side lane: `runs/logs/plan_v2_laneA_now.log`;
  - second pass: `runs/logs/plan_v2_resume.log`, `plan_v2_lane_A.log` and `plan_v2_lane_B.log`;
  - after-queue: `runs/logs/plan_v2_after_queue.log`.
- **Progress:** `ls runs/state/plan_v2/` (a `.done` marker per finished step).
- **Before this run:** all plan-v2 runs were stopped cleanly at 20:35 CET on 2026-10-26 for the night.

## Claims (who is editing what)

| Who | Files / designs | Since |
|---|---|---|
| Cowork | **released 2026-10-27 17:15 CET**: Plan v3 review pack done (`docs/plan_v3_review_pack.md`, `docs/plan_v3/`, flow record 7.12 and rows 46–50, project doc 14). Earlier: the documentation pass (released 14:20). No runs, no flow code changed | 2026-10-27 |
| Claude Code | **released 2026-10-27 13:35 CET**: the runs are finished; the write-up goes to Cowork (Imasha's decision) | 2026-10-27 |

## Pending tasks (plan v2)

1. ~~Finish the runs~~: **done 13:04.** That covers before/after for all designs, the no-PVT ablation, eta 0.9,
   the golden snapshots, the report, the post-hoc test and the eta 0.9 re-run. Next: `./flow test` (unit tests and
   golden comparison) on the new golden snapshots.
1a. TTSKY tile R+C (`rc100s`): both R+C runs warn "Dynamic gmin stepping failed", so the numbers are not trusted.
   Find the cause and run it again. iadc's first R+C run had the same symptom, from floating sub-cell ports.
1b. Before the write-up, check why ota5t_stress 'after' and 'after_eta0.9' differ slightly. Both ran at eta 0.9,
   so they should be identical. `scripts/compare_eta09_rerun.py ota5t_stress --first after --rerun after_eta0.9`
   (12:00): same gates and failed-run counts, but SPICE worst use moves, e.g. 'ours' 0.984 → 1.11, which turns
   "infeasible" into "unsafe + infeasible". The 5T and LOADBench eta 0.9 re-runs reproduced their first runs
   exactly, so the drift is not run-to-run noise. Something changed between 2026-10-26 20:13 and today: code, the
   cell library or S1/S0 inputs.
1c. `scripts/plan_v2_resume.sh`, a latent problem: the eta 0.9 step marks S2 done on rc 0. If the script is
   interrupted between that S2 run and its snapshot, the next start puts the 'after' outputs back, skips S2, and
   snaps the 'after' S2 under `after_eta0.9`. This only bites for a design whose eta 0.9 S2 passes, and it has
   not happened. Fix it when the script is not running (script B avoids it: its S2 run has no marker).
1d. **(review C, row 41)** S3 saturation check: a device below vdsat before layout gets a negative margin, so every
   option fails; iadc's S3 results are artefacts. Fix (`src/s3/run.py`: `mg_of`, the `ok` test, G3.3 `within`, the
   least-bad slack), then re-run iadc S3.
1e. **(row 42)** 5T binding corner GBW@tt_v0.9_t27: first order 0.5 of margin, SPICE −0.16 (GBW rises). Check the
   corner's rates and baseline; add a gate on |SPICE − first order| / margin; use one tolerance (G2.5 has 10 %,
   `outcome()` 2 %).
1f. **(row 43)** Variant S2 runs leave stale files: clear `outputs/S2/<d>` before a variant run; make `snap` check
   that `budgets.json`, `s2_report.json`, `baselines.json` share eta and run; the resume script must tell a crash
   from a FAIL (both rc 1). Then re-run TTSKY25a S2 at eta 0.9 (row 40).
1g. **(row 44)** G2.0 route lengths still come from S0's as-sized PCells; take them from the representative cells.
1h. Near-zero-margin PVT points bind every design (7.6 table): decide how they count, amend PREREG, re-run.
1i. Fair re-scoring: LP with floors with ours' upper bound (10 x need); phase 2 above 200 elements on an iteration
   cap instead of 300 s wall clock (budgets.py).
1j. **(Plan v3 A6, row 46)** PM is measured as 180 + phase at the UGB − phase at 1 Hz (`scripts/benchlib.py` AC
   template, `src/s1/linear.py`). TTSKY25a's dominant pole is at about 25 Hz, so its PM reads 2.3° high. Fix: round
   the 1 Hz phase to the nearest 180°. Changing the bench template changes testbench files and golden snapshots:
   a logged decision.
1k. **(A3, row 47)** S1 node tagger: skip devices of category dummy (`primitives.json`) when tagging diode-connected
   nodes; keep their capacitance.
1l. **(A3, row 48)** Structure recognition (`scripts/recognize_structures.py`, `scripts/schematic_groups.py`):
   TTSKY25a cascode pairs (x1_M4, x1_M8) and (x1_M19, x1_M3); add the second-stage pair (x2_M9, x2_M4); iadc's `cm`
   devices as one composite of 5 parallel stacks × 4 series units. Regenerating `upstream/primitives.json` touches
   hash-frozen files: update `SOURCE.md` and `circuits/SOURCE_SHA256.txt`.
1m. **(A5, row 49)** Correct the PREDICTED hand models (LOADBench mirror doublet; iadc fold-node current split,
   with gmb; TTSKY25a fold-node pole and CMFB-sense load). Post hoc on these circuits: also judge on held-out designs.
1n. **(row 50)** iadc provenance: `circuits/iadc_ota/SOURCE.md` and `config.yaml` say upstream gives no figures;
   `folded_cascode_3_core.sch` has a Performance Summary (53.7 dB, 70°, 344 MHz, CL 0.3 pF). Correct the note
   (logged decision); see D6.
2. ~~Fill flow record 7.5 and 7.6~~: **done 2026-10-27 (Cowork)**, with the post-hoc column labelled, the eta 0.9
   table and the hypothesis reading; corrected after review C.
3. ~~G2.0 vs the hand layouts~~: **done** (7.7, 7.8; like-for-like after review C).
4. R+C extraction of the TTSKY25a tile: run at 10:08, but not trusted yet (item 1a). iadc's is done and clean:
   `reference_layout_rc100s.json`.
5. ~~Golden snapshots for v2~~: taken at 12:36 by the resume script (`tests/golden/`); `./flow test` is still to
   run (item 1).
6. ~~Slides~~: **done**, deck version 7 (section "Plan v2", 15 slides); titles in `docs/slides_v2.md`.
7. ~~Claude.ai project doc 13~~: **done** (`claude/13_plan_v2_results_and_review.md`; copy in `docs/context/project_docs/`).
8. ~~Independent review~~: **done**, review C (flow record 7.9): 14 findings, all checked; write-up corrected,
   technical items 1d–1i open.
9. Imasha commits after each step (GitHub Desktop).

## Open questions for Imasha

**FEEDBACK NEEDED (Cowork, 2026-10-27 evening): Plan v3 decisions D1–D10.** Full reasoning and the per-circuit
questions are in the Claude Doc "Plan v3: circuit review pack and implementation plan" (copy:
`docs/plan_v3_review_pack.md`, section "Decisions needed from you").

| # | Decision | Cowork's recommendation |
|---|---|---|
| D1 | Corner set for budgets | middle 9 (nominal; ss, ff, sf, fs at nominal V and T; tt at 0.9 and 1.1 VDD; tt at −40 and 85 °C); the other 36 reported with a do-no-harm check |
| D2 | Allowance rule | Option B: eta × nominal margin per corner, applied with that corner's own sensitivities |
| D3 | Allowance values (ΔPM, ΔGBW %, Δgain dB, Δpower) and eta | Imasha's numbers; one table for every design, in PREREG before any re-run |
| D4 | Specs for designs without upstream specs | judge layout on degradation; report the derived absolute specs, do not gate on them |
| D5 | Suspect selection rule | topology tags plus the top S1 nets and pairs covering a fixed share of predicted loss per spec, capped at k; Imasha's share and k |
| D6 | iadc reference | include C3/C4 (our bench) or not (the upstream Performance Summary, which our operating point reproduces without them) |
| D7 | TTSKY25a calibration | attribute the tile's extracted 3° PM loss to S1's suspects now (C3), labelled post hoc |
| D8 | CMFB loop stability | add as a reported check for fully differential designs |
| D9 | Phase A fixes A1–A6 (pending tasks 1d, 1f, 1i–1m) | approve as the first technical work, before any re-run |
| D10 | LLM | defer until a deterministic S4 works |

Per-circuit questions (in the doc): LOADBench (keep PM ≥ 60° with 65.3° in the schematic? N1/N4 layout?); iadc
(C3/C4 in the reference? allowance for a 0.3 pF load? keep the 38 upstream dummies?); TTSKY25a (how the paper's 52°
run was set up; 4.9× supply-power change between 0.9 and 1.1 VDD; CMFB loop check; the corrected pairings).

**FEEDBACK NEEDED (Cowork, 2026-10-27): which technical items to do, and in what order.** None was done in the
documentation pass. Suggested order (each is a run or a code change):

1. Fix the S3 saturation check (1d) and re-run iadc S3 (about 10 min with the cache).
2. Fix the snapshot / resume-script problems (1f), then re-run TTSKY25a S2 at eta 0.9 (about 25 min, PC awake), so
   the PREREG headline has all five designs.
3. Explain the 5T binding corner (1e) and the ota5t_stress drift (1b); both are diffs of existing outputs first.
4. Decide how near-zero-margin PVT points should count (1h). This is a methodology decision for you (and your
   supervisor), to be written into PREREG before any re-run.
5. Fair re-scoring of the baselines (1i), G2.0 route lengths (1g), `./flow test` on the golden snapshots (1),
   TTSKY25a tile R+C (1a: its unmapped ports include sub-cell copies of bias nets, as iadc's first run did).


- **Resolved 2026-10-27:** how to restart lane A. Imasha chose to run its iadc and loadbench steps now
  (`scripts/plan_v2_laneA_now.sh`) and to keep the no-PVT ablation for the restart of the resume script after lane B.
- **Resolved 2026-10-27:** iadc S3 had no layout for its 1.2/0.2 µm LVT devices. Fixed as Imasha suggested, with a
  met1 patch on the gate pad (see *Recent changes*).

- **Resolved and done 2026-10-27 13:30 (Imasha): 'least-bad' is the S3 default for future runs.** There is a
  dated amendment in PREREG.md. Plan v2's 'after' results and the post-hoc label stay as they are.
- **Resolved and done 2026-10-27:** the eta 0.9 re-run with the PC awake (Imasha: yes). It ran 12:41–13:04, and
  both designs reproduced their first runs exactly. The question as it was asked:
- **Re-run S2 at eta 0.9 for example_ota_5t and loadbench_miller with the PC awake?**
  - Both ran almost entirely during a standby: 10:15–10:27 (standby 10:07–10:26) and 10:46–11:20 (standby
    10:46–11:16).
  - A SPICE check that the standby slows past its 180 s limit counts as a failed run. That marks a rule's outcome
    "unverified" and can hide a violation, and these eta 0.9 baselines are PREREG's headline.
  - Their logs were removed when the 'after' outputs were put back, so this can't be checked now. The 5T
    eta 0.9 run has 8 failed lp_sum runs and LOADBench 4.
  - Where logs remain, standby made at most one run time out: an iadc 'after' lp_floor check, at 08:54, which
    changes no outcome. No timeout in today's PVT sweeps or S3 simulations.
  - A re-run would take about 30 minutes, after the post-hoc test.
- **Resolved and done 2026-10-27 (Imasha): LOADBench 'after' PM.** The 'after' result is kept as it is, and the
  least-bad fallback was tested as a separately labelled post-hoc S3 run (12:36–12:40). It gave PM 64.7°. The
  question as it was asked:
- **LOADBench 'after' misses the PM spec** (48.1° against ≥ 60°; 'before' 64.9°; details under *Recent
  results*).
  - What happened: S2 leaves almost no budget, so S3 relaxes all 6 device types. A relaxed type keeps the
    default PCell: nf = 1, the device as sized. For the two widest devices that is a single finger with a gate
    resistance of 8.2 kΩ (484 µm) and 4.9 kΩ (887 µm). 'Before' used nf = 8 cells for both.
  - The 484/0.24 µm nf = 1 cell only became DRC-clean with this morning's gate-pad patch. Before the patch, the
    fallback took that type's option with the most slack.
  - The question: keep the rule the runs were set up with and report this in 7.5? Or also test, as a separately
    labelled post-hoc run after the queue, a fallback that keeps the option that breaks its allowances least,
    gate resistance included? That would be an S3-only run, about 30 min for LOADBench. It may also change the
    relaxed types of the other designs.
- **iadc G1.1** (not blocking): 21 functional devices sit below vdsat at the operating point: 15 MOS-resistor stacks with the gate at cm, plus some current sources. Is that the design intent? Until answered, it is reported as a FAIL, with that explanation. (Cowork, Plan v3 review: the upstream schematic's Performance Summary is reproduced by our operating point without C3/C4, which suggests the fold sources M11/M12 in triode are intended; flow record row 50, D6.)
- **TTSKY paper numbers** (information only): the paper's post-layout 2.3 MHz / 52° is not reproduced by the tile's PEX, even at the bench conditions (ff, 20 °C, MIM MF=100). How was that run set up?

## Recent results

**Post-hoc 'least-bad' fallback test** (12:36–12:40; not pre-registered). It re-runs S3 on the same 'after' inputs
(checked by hash for all four designs); a relaxed type keeps the option that breaks its allowances least, access
R included.

| Design | 'after' (default fallback) | post-hoc (least-bad) |
|---|---|---|
| loadbench_miller | PM **48.1°** (fails ≥ 60°), G3.3 FAIL; area 4396 µm²; power 361 µW | PM **64.7°** (meets), G3.3 PASS; area 2142 µm²; power 555 µW |
| ota5t_stress | GBW 356.3 MHz, PM 62.4°; area 257 µm² | GBW 370.2 MHz, PM 63.8°; area 206 µm² |
| iadc_ota | 22 of 22 types relaxed | the same cells: no change |
| ttsky25a_fd | 10 of 22 types relaxed | the same cells: no change |

- LOADBench: 5 of 6 types change. The 484/0.24 nfet goes nf1 → nf64 (gate R 8184 → 3 Ω) and the 887/0.74 pfet
  goes nf1 → nf64 (4855 → 2 Ω). Gain 57.99 dB and GBW 22.74 MHz. 'Before' (v1) had PM 64.9°, area 2342 µm²
  and power 551 µW.
- LOADBench power: the nf1 fallback also cut power from 551 to 361 µW. Its long S/D strips put 88–161 Ω in the
  sources of large, weakly inverted devices, which lowers their current. So the 'after' run moved the bias point
  as well as the phase margin. This is an inference from the access R values; no separate run tested it.
- Why iadc and TTSKY don't change (checked on the option tables): in iadc the A-bin mode leaves every relaxed type
  only nf = 1 options. In TTSKY some relaxed types also have nf = 2, but for all 10 the least-bad option is the
  default cell itself.
- All four post-hoc S3 runs still FAIL G3.5: relaxed types stay flagged, as designed.

**S2 at eta 0.9 re-run with the PC awake** (12:41–13:04; `outputs/posthoc/eta09_rerun/compare.json`):
example_ota_5t and loadbench_miller match their first runs exactly. Gates, every rule's outcome, failed-run counts,
SPICE worst use and verification are all identical, so the standby did not change the first runs.
- The 5T re-run's lp_sum rule again has 8 failed runs, 4 of them ngspice timeouts. They happened with the PC
  awake, so those budget scenarios really do not converge.
- No standby occurred during the re-run (Windows event log).

**TTSKY S2 at eta 0.9** (12:36): **not a valid result (Cowork, 2026-10-27; flow record row 40).** The run crashed
(`OSError: [Errno 22] Invalid argument` writing an ngspice log; traceback in `runs/logs/plan_v2_resume.log`), and the
snapshot mixed that run's `budgets.json` with the eta 0.5 report, which is why every rule looked unchanged. Also,
`docs/before_after.md` shows the budget-rule tables of the 'after' runs only; the eta 0.9 table is in flow record 7.6.

Today's plan-v2 runs (CET). In S3 'before' runs, FAILs in G3.3 and G3.5 are part of the before picture: v1 rules, mode A-free.

- **iadc 'before' S3** (v1, 06:27–06:32): FAIL G3.3, G3.5.
  - Every spec is met: gain 53.47 dB, GBW 203.8 MHz, PM 76.5°.
  - G3.3 fails on saturation only. All 45 devices below vdsat are already flagged by S1 G1.1 before any layout
    (the open G1.1 question).
  - G3.5: all 22 device types are relaxed, and each one fails a saturation check.
- **TTSKY 'before'** (v1): S2 PASS (05:39). S3 (73 min) FAIL G3.3, G3.5.
  - Every spec is met: gain 98.42 dB, GBW 2.046 MHz, PM 77.9°, power 452.6 µW.
  - G3.3 fails only because power uses more than its allowance.
  - 4 of 22 types are relaxed.
- **LOADBench 'after'** (v2, 06:32–07:27): S2 FAIL G2.7, G2.3. S3 FAIL G3.3, G3.5.
  - S2, G2.7: the library's cheapest cells alone use 1.16–2.80 × eta × margin at 4 PVT points. The worst are
    GBW at sf, 1 V, 85 °C (2.80) and gain at sf, 0.9 V, −40 °C (2.43). So, as with ota5t_stress, S2 says
    before S3 that the design does not fit.
  - S2, G2.3: round-1 t = 0.00094, and 39 of 42 elements are starved. Phase 2 (SLSQP) did not converge
    ("Positive directional derivative for linesearch"), so the max-min budgets are kept, which is the code's
    safe fallback.
  - S3: all 6 types relaxed. Gain 57.74 dB, GBW 22.55 MHz, power 361 µW, **PM 48.1° (spec ≥ 60°; 'before'
    64.9°)**. Total device area 4396 µm² ('before' 2342 µm²).
  - Cause, read from the S3 outputs (no extra simulation): every relaxed type keeps its nf = 1 default. Their
    gate resistances are nfet 484.2/0.24: 8184 Ω; pfet 887.03/0.74: 4855 Ω; pfet 90.63/0.74: 532 Ω.
    - Each cell simulated alone, without its access resistance, costs at most 1.0° of PM (1.1° summed over
      the types).
    - All cells together, with their access resistances, cost 17.3°.
    - So the loss points to the access (gate) resistance. See *Open questions*.
- **PVT points:** TTSKY 5 of 45 meet every spec (07:22); iadc 27 of 45 (08:06).
- **iadc 'after'** (v2, 08:06–09:22): S2 FAIL G2.7 (t = 0.0166, 574 of 750 elements starved, 105 PVT
  constraints). S3 FAIL G3.3, G3.5.
  - All 22 types are relaxed, every one on a saturation check (the devices S1 G1.1 flags), and each keeps its
    default nf = 1 cell. 'Before' did the same, so the final specs are identical to 'before': 53.47 dB,
    203.8 MHz, 76.5°.
- **TTSKY 'after'** (v2, 07:22–09:26): S2 FAIL G2.7 (t = 0.227, 2035 of 2678 elements starved, 104 PVT
  constraints). Every baseline rule has failed SPICE runs, so they are marked "unverified".
  - S3 FAIL G3.3, G3.5. 10 of 22 types are relaxed, mostly on S/D access R.
  - Final: 98.42 dB, 2.046 MHz, 77.86°, 452.6 µW: the same as 'before' (to within 0.002°). Area 4092 µm²
    ('before' 4025).
- **iadc hand layout, final** (09:25): the same layout numbers as last night (PEX 53.60 dB, 156.2 MHz, 81.2°), now
  set against the 'after' G2.0. LVS against the layout view fails, as known: the layout includes the CMFB's
  switches and capacitors.
- **TTSKY tile, final** (09:30): PEX 108.1 dB, 1.426 MHz, 77.6°. Wiring costs 0.104 MHz of GBW and 3.0° of PM.
  It fails the derived GBW spec before wiring, as known.
- **TTSKY tile R+C** (`rc100s`, 10:08): finished, but both R+C runs warn "Dynamic gmin stepping failed". By the
  project's rule (review B), its numbers are **not trusted** yet: 108.10 dB, 1.459 MHz, 77.25°, 474.6 µW (C only:
  481.2 µW). See *Open questions*.
- **No-PVT ablation** (10:09–10:15):
  - example_ota_5t: S2 and S3 PASS, area 200.8 µm² ('after' 237.0).
  - ota5t_stress: S2 PASS (G2.7 passes without the PVT constraints), and S3 PASS with no relaxed type ('after'
    relaxed 3 of 3), area 200.8 µm² ('after' 256.6).
  - So in ota5t_stress the PVT constraints are what forces the relaxations.
- **S2 at eta 0.9** (snapshots `after_eta0.9`):
  - example_ota_5t: PASS, t = 1.89, none starved.
  - ota5t_stress: FAIL G2.7, t = 0.2575, 20 of 21 starved.
  - loadbench_miller: FAIL G2.3, G2.7, t = 0.0017, 39 of 42 starved.
  - iadc_ota (12:08): FAIL G2.7, t = 0.0299, 572 of 750 starved. Every budget rule's outcome is the same as in
    its eta 0.5 'after' run; 'ours' is "infeasible", with SPICE worst use 0.97 of allowed.
  - To check before the write-up: ota5t_stress 'after' already ran at eta 0.9, so these two runs should be
    identical, but they differ slightly (t 0.2567 vs 0.2575; 'ours' scored "infeasible" vs "unsafe +
    infeasible"). Code changed in between (the baseline re-scoring after review B), which may explain it.
- iadc hand layout R+C (`rc100s`, `--map-shorted`): clean. Gain 57.24 dB, GBW 153.7 MHz, PM 78.7 deg; wire R costs GBW 2.5 MHz and PM 2.5 deg beyond C, and moves the output CM by -68 mV.
- 5T after and ota5t_stress after: see `docs/before_after.md` (after the report step) and flow record 7.5 and 7.6.

## Recent changes

- 2026-10-27 17:15 CET (Cowork): **Plan v3 review pack** (no runs, no flow code changed).
  - Claude Doc "Plan v3: circuit review pack and implementation plan" (https://claude.ai/artifact/R15Aj6FzDVKxcYwLT1WAr5),
    mirrored as `docs/plan_v3_review_pack.md`; figures in `docs/plan_v3/img/` (drawn by `docs/plan_v3/src/*.py` or
    rendered from the upstream xschem sources).
  - Flow record 7.12 and journey rows 46–50; changelog line. Progress-log entry.
  - Independent review of the pack (12 findings, checked and applied), plus one correction found afterwards (the
    TTSKY25a tile loses about 3° of PM in our extraction, so the paper's 52° stays unexplained).
  - New pending tasks 1j–1n; FEEDBACK NEEDED D1–D10 under *Open questions*.
  - claude.ai project doc 14 and its copy in `docs/context/project_docs/`.
- 2026-10-27 14:20 CET (Cowork): **documentation pass** (no runs, no flow code changed).
  - Flow record section 7 completed: 7.5 for LOADBench, iadc and TTSKY25a (post-hoc column labelled), 7.6 (held-out
    designs at eta 0.5, eta 0.9 headline, binding-margin table, H1/H1b/H1c), 7.7 and 7.8 against the 'after' G2.0,
    7.9 review C, 7.10 limitations, new 7.11 assessment, journey rows 40–44. Header, status at a glance, problems
    log and changelog of `docs/flow_record.md` updated.
  - Figures `docs/flow_record/img/v2_*.png`, drawn from the snapshots by the new `scripts/make_v2_figures.py`
    (documentation only).
  - Review C (independent agent, 14 findings): every finding checked against the files; the write-up corrected;
    the code-level findings are pending tasks 1d–1i.
  - Slide deck version 7 (section "Plan v2"); `docs/slides_v2.md`; claude.ai project doc 13 and its copy in
    `docs/context/project_docs/`.
  - Deploy incident, fixed: a stale archive with a reused name overwrote `PREREG.md` and the section 7 draft for
    about 5 minutes; both restored (md5 checked). `.incoming/apply.sh` now checks the archive md5 (row 45).
- 2026-10-27 13:30 (Claude Code): **S3 default for relaxed types is now 'least-bad'** (Imasha's decision; PREREG
  amendment).
  - `src/s3/options.py`, `src/s3/run.py`, `src/flow.py`: the v1 variant pins the old rule, and `./flow run` and
    `./flow test` take `--relax-fallback`.
  - `src/golden.py` records the rule in snapshots, and S3 golden re-runs use the recorded rule (plan v2's: the
    old one).
  - `scripts/plan_v2_resume.sh` and `scripts/plan_v2_laneA_now.sh` pin the old rule.
  - Also: `tests/test_s3.py`, README, the report intro and flow record row 38. Tests: 51 passed.
- 2026-10-27 13:10 (Claude Code): all runs finished. Results are under *Recent results*: the post-hoc test, the
  eta 0.9 re-run and TTSKY's eta 0.9. A new FEEDBACK NEEDED question asks whether to adopt 'least-bad'. No code
  changed; the read-only checks are in `runs/tmp/*.py`.
- 2026-10-27 12:00 (Claude Code): **eta 0.9 re-run prepared and queued** (Imasha's decision).
  - `scripts/plan_v2_eta09_rerun.sh` is script B under *Running*. `scripts/compare_eta09_rerun.py` compares a
    design's first run with its re-run, or any two snapshot tags (`--first`, `--rerun`).
  - `.gitignore` ignores `outputs/posthoc/*/*/S2/work/`; the report's intro explains the new tag; README updated.
  - Checked: syntax, the clock record, the waiting and set-aside checks, and the comparison script on existing
    snapshots.
- 2026-10-27 11:50 (Claude Code): run check.
  - The after-queue script took over at 10:08 as planned.
  - The standby periods were found in the Windows event log, and the timeouts were checked against them.
  - The post-hoc folders were seeded with the 'after' `sim/` folders, so the post-hoc test takes minutes,
    not an hour.
  - No code changed. The read-only checks are in `runs/tmp/*.py`.
- 2026-10-27 08:40 (Claude Code): **post-hoc 'least-bad' fallback test prepared and queued** (Imasha's decision).
  - `src/s3/options.py`: `relaxed_pick` holds the relaxed-type rule. 'default' is unchanged and is what every
    run uses. 'least-bad' always keeps the option with the largest min_slack, so the access R of d, g and s
    counts.
  - `src/s3/run.py`: `--relax-fallback default|least-bad` and `--out <folder>`. The fallback is recorded in G3.5
    and in `device_decisions.json`. Without the new options, S3 behaves as before.
  - `scripts/compare_before_after.py`: `snap <design> <tag> [<S3 folder>]`. Checked: without the folder, its
    record of LOADBench 'after' is identical to the 07:27 snapshot.
  - `scripts/plan_v2_after_queue.sh` (job 3 under *Running*); `.gitignore` ignores
    `outputs/posthoc/*/*/sim/` (about 120 MB per design); README, S3 section; `tests/test_s3.py`: 5 passed.
  - Dry check of the existing LOADBench option table: least-bad would keep nf = 64 cells for the 484 and 887 µm
    devices (gate R 3 and 2 Ω instead of 8184 and 4855 Ω). SPICE has not checked this yet; the post-hoc run will.
- 2026-10-27 08:20 (Claude Code): run check, with no change to code or runs. Results are under *Recent results*,
  and there is one FEEDBACK NEEDED question (LOADBench PM). The read-only probes are in `runs/tmp/status_probe*.py`.
- 2026-10-27 06:27 (Claude Code): added `scripts/plan_v2_laneA_now.sh`, lane A of the resume script without the
  no-PVT ablation, with the same `.done` markers, so it can run next to the resume script's lane B. The main
  resume script is paused (`kill -STOP 49`), so its final part can't overwrite iadc's S2 outputs while the side lane uses them.
- 2026-10-27 06:18 (Claude Code): **S3 gate-pad met1.6 patch for short-L devices.** At L = 0.2–0.24 µm the
  PDK PCell's gate contact pad is 0.290 × 0.230 µm = 0.067 µm², below met1.6 (0.083 µm²). This is why every iadc
  1.2/0.2 LVT cell and LOADBench's 484/0.24 nf = 1 cells failed DRC.
  - `src/s3/strap.py` (`pad_patch`) widens such a pad along the gate to the minimum area (0.370 × 0.230 =
    0.085 µm²). The PCell is unchanged, and so are the cell size and the gap to the S/D strips.
  - `src/s3/run.py` rebuilds cached cells that failed DRC before the patch; signed-off cells are never rebuilt.
  - iadc: 88/88 options signed off (was 80). `tests/test_v2.py` 24 passed. Logged in the progress log and
    flow record 7.1, rows 7 and 37.
  - Not covered: TTSKY `W0p5_L20` sdhalf cells, whose S/D strip is 0.0817 µm² (narrow W, a different cause;
    the sdfull options pass).
- 2026-10-27 01:10: overnight stop. Added:
  - `scripts/plan_v2_resume.sh` (resumable remaining runs, two lanes) and `scripts/plan_v2_stop.sh`;
  - `docs/HANDOFF.md` (the move to Claude Code);
  - `docs/context/project_docs/` (copies of the claude.ai project docs 08–12; 05–07 were already in `docs/`).
- 2026-10-26 20:20: `scripts/compare_before_after.py` snapshots keep G2.0's split (route C, cell C, R) and each budget rule's budget / need; the report adds a hand-layout vs G2.0 table.
- 2026-10-26: added `CLAUDE.md` and `docs/STATUS.md` so that Claude Code and Cowork can share the project state.
  - Cowork deploys now go through `.incoming/apply.sh`, which refuses to overwrite files changed since Cowork's last sync.
- 2026-10-26: the TTSKY structure groups were accepted by Imasha.
  - L-ratioed mirrors are now split into equal-L subsets for G1.4.
  - Schematic group figures are in `docs/flow_record/img/ttsky25a_fd_groups_*.svg`.
- 2026-10-26: fixed a series of bugs; details are in flow record section 7.1, rows 1–32:
  - MIM ×M counted twice;
  - S3 m>1 unit cells;
  - triode saturation constraints;
  - the LVS negative control on long channels;
  - the S2 solver NaN;
  - baseline scoring.
