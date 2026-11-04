# STATUS: live handoff between Claude Code, Cowork and Imasha

Read this file first and update it when you start or stop work (see `CLAUDE.md`, "Working together"). Times are given in container time (CET).

**Last updated:** 2026-11-04 10:09 CET, by Claude Code. **Now: plan v4, S4–S7 (block generation, placement,
routing, verification) on branch `s4-s5`**, from `main` at tag `s0s3-reviewed` (`ec359567`). The plan is
`docs/plan_v4_S4_S7.md`; the phases are under *Plan v4 (s4-s5)* below.
- Phases 0–4 are committed: `e6306879`, `a3e9277e`, `1e4d166f`, `f26c136a` and `3089366a`. Phase 2's commit carries an unrelated message
  ("dementia_care_guide_sinhala (2)", a GitHub Desktop slip); its content is Phase 2's, and history is not rewritten.
- Phases 5, 6 and 7 are committed (`27a075a6`, `6d0c6bb7`, `a5b250de`). The merge of `s4-s5` into `main` is Imasha's.
- **Phase 8 (`ttsky25a_fd`), branch `s5-ttsky`:** plan and PREREG agreed; 8.1 (S0–S3) done; 8.2 S4 PASS; 8.3 S5's
  placement fits the 250 × 200 µm outline for both costs (legal, unrouted DRC 0). Part 1 committed (`76a92ba9`).
  Part 2 done: grid-routed (DRC 0, LVS match), S6 G6.1 PASS (C-only), S7: every spec met, G7.2 FAIL on GBW (within
  η with the MIM double count cancelled); flow record 7.23, rows 87–91. Part 2 committed (`7839123d`).
  8.7 done: independent review (row 92, fixes), all three designs re-run from S4 (5T and LOADBench goldens unchanged),
  walkthrough covers ttsky (flow record 7.24). 8.7 committed (`f99774b4`). The full report for any reader:
  `docs/ttsky25a_fd_report.html` (`scripts/make_ttsky_report.py`). **Waiting for Imasha's review and commit.**
  The independent-LLM comparison waits (Imasha, 14:25).
- Phase 6 (LOADBench through S4–S7), 02:36–04:10 CET 2026-11-04: LOADBench runs S0–S7: S4 and S5's sign-off pass; G5.4, G6.2 and G7.2 (GBW) fail;
  every spec is met post-layout. The 5T, re-run with the new code, still passes S0–S7.
  ASSUMPTIONS until Imasha answers plan questions 3–5: the PMOS bank drawn side by side as S3 sized it; no dummies.
  The Miller capacitor is drawn as S0's PREDICTED binding (`sky130_fd_pr__cap_mim_m3_1`, 15.66 × 15.66 µm).

`main` holds the reviewed S0–S3 state (the supervisor review, merged; `1626d11b` and Imasha's STATUS commit
`ec359567`) and is not touched until a review merges `s4-s5`.

**Plan v3 Phase A is complete and committed** (`docs/plan_v3_phaseA.md`, tag `phaseA-v3a`).
- Steps 0–13 and the sky130A environment change are committed. The environment change is commit `70279125`, named
  "step_9"; step 9 is `fb1b9adf`; step 12 is `14e97f7e`.
- Step 13 (documentation, independent review D) and the G2.8 follow-up are `67b3b83d`. In the follow-up, G2.8
  SPICE-checks PVT points again (Imasha's answer (a) to review D 1).
- Claude Code has released its Phase A claim. Nothing is running.
- **Where to read the results:** flow record 7.13 (and 7.9, review D), `docs/before_after.md`, and the step
  records below.
- **Next is Imasha's call:** the optional follow-ups under *Open questions* (none blocking), and Plan v3's phases
  B–E.

**Resumed 2026-11-02 12:12 CET** after the overnight stop (2026-11-01 22:05):
- the container was running with no job, and there was no `.git/index.lock`;
- step 9 was committed, and the working tree was clean.

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

- Nothing running (19:29 CET 2026-11-04).

Runs of 2026-11-04 evening (branch `gui-tools`), ended:
- iadc_ota S0–S3 re-run with today's code (branch `gui-tools`), 15:34–18:15 CET (`runs/logs/p9_iadc_S0S3.log`): every stage finished; FAIL G0.7, G1.1, G2.7, G3.3/G3.5, as in October.
- iadc_ota S4–S7 in the Tiny Tapeout 1x2 analog tile (`inputs/iadc_ota/layout.yaml`, outline 161 x 225.77 um): first try 18:17–18:18 ERROR in S4 (two stubs 0.49 um apart in the W 1.2 / L 0.2 unit cell; fixed, flow record row 94); again from 18:20 CET (`runs/logs/p9_iadc_S4S7b.log`, `.log.exit`).
- GUI end-to-end test (branch `gui-tools`), from 15:37 CET, started through the GUI's own API: `ota5t_gui_copy` (a copy of the 5T with `matching: centroid`, `dummies: true`) and `ota5t_gui_new` (the 5T entered as a new design, benches generated), each S0–S7 then its simple report (`runs/logs/gui_<design>.log`, `.log.exit`, `_report.log`). First pass ended 17:13: the copy stopped in S5 (S4 gave the 5T PMOS mirror no variant under matching: centroid; fixed, flow record row 93), the new design failed G0.6 and S1 (uploaded measurements from other benches; no ac_drive; fixed in the GUI). Second pass from 17:15: the copy from S4, the new design (recreated: specs from its own results) from S0.

- iadc_ota S4–S7, third try 18:32: S4 FAIL G4.2 (the same 32/8 DRC errors: the stubs were not the cause); fourth try 18:52 with `pin_origin: bbox` (row 95): S4 PASS, S5 ERROR (no placement of x1, x2 fits the tile; row 96 fixed x1; x2 needs folding, FEEDBACK).

Plan v4 Phase 8's runs have ended (2026-11-04, CET):
- Plan v4 Phase 8.1 ended (`runs/logs/v4_p8_tt_S0S3.log`): S0 PASS (06:21–06:43), S1 FAIL G1.2, S2 PASS (77 min),
  S3 FAIL G3.3/G3.5 (53 min). Goldens S1–S3 of `ttsky25a_fd` refreshed on purpose (S0 unchanged).
- Plan v4 Phase 8.2: `ttsky25a_fd --stage S4`: first run 09:33, ERROR (stubs too close: a gate pad at the bottom next to
  a strip); second run: the same ERROR (its cause: unit_pins read the .mag at 0.005 um/unit; these cells have no magscale line, 0.01 um). Third run: ERROR (S0 gives four blocks one name; parallel builds overwrote each other). Fourth: every variant DRC/LVS clean, G4.4 FAIL on a pair of two sizes (gate fixed: matched pairs only). Fifth: S4 PASS (53 variants DRC/LVS clean).
- Plan v4 Phase 8.3: `ttsky25a_fd --stage S5` (macros, three shapes), 10:03–10:08 CET (`runs/logs/v4_p8_tt_S5.log`):
  placement legal and inside the outline; routing failed (the spine router; the grid router is next).
- Plan v4 Phase 8.5: `ttsky25a_fd --stage S5` with the grid router: first run DRC 12/14 (stacks near rings and wires), LVS budget-aware match, area-only short. Second: budget-aware DRC 0 and LVS match; area-only unroutable (Vss: a narrow ring had no stack column). Third: both layouts routed, top-level DRC 0 and LVS match (controls caught); G5.4 FAIL (budgets).
- Plan v4 Phase 8.6: `ttsky25a_fd --from S6`, first run 11:12–11:38: stopped by Claude Code (the R+C extraction's .res.ext passed
  2.37 GB on the supplies). Second run 11:45–11:50 (supplies left out of R+C): the R+C netlist's ports came out unconnected
  and the flat LVS did not merge the resistor strings. R+C switched off for this design; internal tracks unlabelled.
- Plan v4 Phase 8.6: `ttsky25a_fd --from S4` (S4–S7), 11:54–12:09: S6 flat LVS failed (resistor strings not merged across
  labelled nodes; with the labels removed, 199 capacitances lost their nets). Labels back, series merging off in S6's LVS.
- Plan v4 Phase 8.6: `ttsky25a_fd --from S5` (S5–S7), 12:18–12:33 CET (`runs/logs/v4_p8_tt_S5S7.log`): S5 FAIL G5.4 only; S6 FAIL G6.1 (`flat_lvs` misread cut names and a crossed symmetric pair, row 90) and G6.2; S7 FAIL G7.2, G7.5 empty (row 91). The run from 12:12 passed S4, then the `flow_summary.json` write hit Errno 22: `src/flow.py` wrote it without the retrying `write_text` (now it uses it, ten tries).
- Plan v4 Phase 8.6: `ttsky25a_fd --from S6`, 12:34–12:40 CET (`runs/logs/v4_p8_tt_S6S7c.log`): S6 FAIL G6.2 only (G6.1 PASS); S7 FAIL G7.2 on GBW (1.26 of the allowance), G7.1 PASS, G7.5 within η. Goldens S5–S7 taken.
- Plan v4 Phase 8.7: after the review fixes, one chain, 13:16–14:13 CET: `ttsky25a_fd`, then `example_ota_5t`, then `loadbench_miller`, each `--from S4` (`runs/logs/v4_p87_<design>.log`, `.exit` per design). The 5T and LOADBench runs check that Phase 8 left them unchanged (goldens). ttsky S4 PASS (unchanged), S5–S7 FAIL on G5.4, G6.2, G7.2 as before (placements changed a little: row 92); the 5T S4–S7 PASS; LOADBench S4 PASS, S5–S7 FAIL as before. Every 5T and LOADBench golden matches; ttsky's S5–S7 retaken.

Plan v4 Phase 7's runs have ended (2026-11-04, CET):
- Plan v4 Phase 7: `example_ota_5t --from S5`, ended 05:09 CET after about 3.5 min (`runs/logs/v4_p7_5t_S5S7.log`): PASS (before the review fixes).
- Plan v4 Phase 7, final runs with the review fixes, from 05:15 CET 2026-11-04: one chain: `example_ota_5t --from S4`
  then `loadbench_miller --from S4` (`runs/logs/v4_p7_final_5t.log`, `runs/logs/v4_p7_final_lb.log`): ended 05:55;
  the 5T S4–S7 PASS; LOADBench S4 PASS, S5–S7 FAIL on G5.4, G6.2, G7.2 as expected; no failed simulation.

Plan v4 Phase 6's runs have ended (2026-11-04, CET; results under *Plan v4*, Phase 6 record):
- Plan v4 Phase 6: `loadbench_miller --stage S4` (second run: tap strips, MIM block), from 02:45 CET 2026-11-04
  (`runs/logs/v4_p6_lb_S4b.log`). The first run, 02:36–02:38, FAILED G4.2/G4.5 on the PMOS bank (LU.3).
  Second run 02:45–02:51: the bank passes; the MIM block FAILED capm.11 (2). Third run 02:48–02:50 PASS (`runs/logs/v4_p6_lb_S4c.log`).
- Plan v4 Phase 6: `loadbench_miller --stage S5`, 02:49–02:52 (`runs/logs/v4_p6_lb_S5.log`): FAIL G5.2 (met3 notch) and G5.4.
  Second S5 run (router fixes): FAIL, no spine for outFirstStage (same-net notch rule too strict). Third: LVS ok, DRC 2 (a met3 run lengthened past a fill). Fourth: DRC 0, LVS match; G5.4 FAIL as expected (outFirstStage length, S3's access R).
- Plan v4 Phase 6: `loadbench_miller --from S6` (S6, S7), 03:00–03:24 CET (`runs/logs/v4_p6_lb_S6S7.log`): S6 FAIL G6.2;
  S7's two R+C AC runs killed (rc −9, out of memory with four decks at once). A test of one AC deck alone runs in
  `runs/tmp/acalone/` 03:24–03:40: exit 0, 15 min, peak 5.3 GB (so one large deck at a time).
- Plan v4 Phase 6: `example_ota_5t --from S4` (S4–S7 with the Phase 6 code), 03:26–03:31 CET (`runs/logs/v4_p6_5t_S4S7.log`): all PASS.
- Plan v4 Phase 6: `loadbench_miller --from S6` (final, one large deck at a time), 03:40–04:05 CET (`runs/logs/v4_p6_lb_S6S7b.log`):
  S6 FAIL G6.2 (2 min), S7 FAIL G7.2 on GBW (22 min), no failed run.


Earlier:
- Plan v4 Phase 1's S3 runs, with ringless unit cells, have ended (results under *Plan v4*, Phase 1 record):
  - `example_ota_5t --stage S3`: 19:25–19:46 CET 2026-11-03, PASS (`runs/logs/v4_p1_5t_S3.log`).
  - `loadbench_miller --stage S3`: 19:48–20:45 CET 2026-11-03, FAIL G3.5 only, as before
    (`runs/logs/v4_p1_lb_S3.log`).

**Earlier:**
- Review phase 3's full runs from S0 have ended, with no ERROR.
  - `example_ota_5t`: 19:15–19:45, S0–S3 all PASS (`runs/logs/review_p3_5t.log`).
  - `loadbench_miller`: 19:45–20:04, S2 PASS; S0, S1 and S3 FAIL only on their known findings
    (`runs/logs/review_p3_lb.log`).
- Review phase 1: `loadbench_miller --stage S0` ran 18:13–18:24 (`runs/logs/review_p1_lb_S0.log`). G0.7 fails on
  N3 only again, the known PDK finding.
- After review D 1 (Imasha: re-add PVT checks to G2.8): `example_ota_5t --from S2` 15:01–15:19 (S2 PASS, S3 PASS) and
  `loadbench_miller --from S2` 15:19–15:35 (S2 PASS, S3 FAIL G3.5 as before); logs `runs/logs/phaseA_reviewD_*_S2S3.log`.
- Phase A step 12, after Imasha's answer (a): `loadbench_miller --from S2` ran 13:48–13:55, S2 PASS and S3 FAIL G3.5
  as before (`runs/logs/phaseA_step12_lb_S2S3_fix.log`).
- Phase A step 12's re-run has ended, with no ERROR.
  - `example_ota_5t --from S1`: 13:17–13:24, S1, S2 and S3 PASS (`runs/logs/phaseA_step12_5t.log`).
  - `loadbench_miller --from S0`: 13:24–13:41 (`runs/logs/phaseA_step12_lb.log`). S0 FAIL G0.7 and S1 FAIL G1.6,
    both known. **S2 PASS.** S3 FAIL G3.5: 3 types relaxed.
- Phase A step 11's `ota5t_stress` S1 re-run check has ended, 13:09–13:10
  (`runs/logs/phaseA_step11_stress_S1_rerun.log`): S1 rc 0, golden S1 OK.
  - Its committed S1 outputs, flow summary and S1 logs were set aside in `runs/tmp/aside/step11/` before the run
    and copied back after it. `git status` shows no change for this frozen design.
  - The re-run's own outputs are kept for reference in `runs/tmp/step11_rerun_outputs/` (git-ignored).
- Phase A step 10's LOADBench S1 run has ended, 12:19, in 23 s (`runs/logs/phaseA_step10_lb_S1.log`): S1/run rc 3
  (G1.6 FAIL, as in plan v2), `symbolic_patch_miller` rc 0. The S1 numbers are identical to step 7's.
- Phase A step 9's 5T S2 run has ended, 21:53–21:58, PASS with rc 0 (`runs/logs/phaseA_step9_5t_S2.log`). It was
  started from a login shell + `env.sh`; all 123 ngspice logs show sky130's init ("hs a").
- Phase A step 8's 5T S2 run has ended, 20:40–20:46, PASS with rc 0 (`runs/logs/phaseA_step8_5t_S2.log`).
- Phase A step 7's S1 re-run has ended, 20:07–20:08 (`runs/logs/phaseA_step7_S1.log`): `example_ota_5t` PASS;
  `loadbench_miller` FAIL on G1.6 only, as in plan v2.
- Phase A step 6's two 5T S2 runs have ended, both PASS with rc 0: the tolerance run, 18:54–18:59
  (`runs/logs/phaseA_step6_5t_S2.log`), and the final run with `lp_floor_k`, 19:33–19:38
  (`runs/logs/phaseA_step6_5t_S2_final.log`).
- Phase A step 5's LOADBench S0 + S1 re-run ended at 17:54 (`runs/logs/phaseA_step5_loadbench_S0S1.log`), with
  the expected statuses: S0 FAIL on G0.7 (the known PDK finding) and S1 FAIL on G1.6, as in plan v2.
- Phase A step 3's two 5T S2 runs have ended, both PASS with rc 0: 17:16–17:21 (`runs/logs/phaseA_step3_5t_S2.log`),
  and the re-run after the G2.9 label fix, 17:22–17:28 (`runs/logs/phaseA_step3_5t_S2_rerun.log`).
- Phase A step 2's two 5T S2 runs have ended, both PASS with rc 0. The baseline with the unchanged code ran
  16:28–16:32 (`runs/logs/phaseA_step2_baseline_5t_S2.log`); the step 2 code ran 16:35–16:46
  (`runs/logs/phaseA_step2_new_5t_S2.log`).

**Plan v2 (finished):** every plan-v2 run had ended by 13:04:39 CET on 2026-10-27. `runs/tmp/aside/` is empty, so no design's outputs are
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
| Claude Code | The local GUI: new `gui/`, `scripts/gui_backend.py`, `scripts/make_design_report.py`; design copies it creates (`circuits/<copy>/`, `inputs/<copy>/`, lines added to `circuits/SOURCE_SHA256.txt`) | 2026-11-04 15:15 CET |
| Claude Code | Plan v4 Phase 8 on branch `s5-ttsky` (8.7 from 13:16: also re-runs `outputs/S4`–`S7` of `example_ota_5t` and `loadbench_miller`, and `scripts/make_s4s7_walkthrough.py`): `src/s4/`–`src/s7/`, `inputs/ttsky25a_fd/layout.yaml`, `tests/`, `outputs/S4`–`S7` (and S0–S3 re-runs) for `ttsky25a_fd`, `PREREG.md`, docs (plan v5, README, STATUS, progress log, flow record) | 2026-11-04 06:10 CET |
| Claude Code | Plan v4 on branch `s4-s5`: `src/s3/`, new `src/s4/`–`src/s7/`, `src/flow.py`, `scripts/`, `tests/`, `outputs/S3`–`S7` for `example_ota_5t` and `loadbench_miller`, `PREREG.md`, docs (plan v4, README, STATUS, progress log, flow record). S0–S2 outputs are frozen (`tests/frozen/`), not claimed | 2026-11-03 19:10 CET |
| Claude Code | **released 2026-11-02 23:20 CET**: supervisor review on branch `s0-s3-review`, phases 1–6 done (the rehearsal included). Held since 2026-11-02 18:15 CET, narrowed after phase 5 | 2026-11-02 18:15 CET |
| Claude Code | Plan v3 Phase A: `src/`, `scripts/benchlib.py`, `scripts/compare_before_after.py`, `inputs/example_ota_5t/`, `inputs/loadbench_miller/`, `outputs/*/example_ota_5t/`, `outputs/*/loadbench_miller/`, `PREREG.md`, `tests/`; plus the doc updates the plan's steps ask for (README, progress log, flow record section 7 draft) | **released 2026-11-02 14:50 CET**: Phase A done (steps 0–13). Held since 2026-11-01 16:10, paused overnight 22:05, resumed 2026-11-02 12:12 |
| Cowork | **released 2026-11-01**: Phase A plan written (`docs/plan_v3_phaseA.md`; `docs/HANDOFF.md` rewritten; this file; progress log). No code or outputs changed. **Next: Claude Code claims Phase A at its step 0** | 2026-11-01 |
| Cowork (earlier) | **released 2026-10-27 17:15 CET**: Plan v3 review pack done (`docs/plan_v3_review_pack.md`, `docs/plan_v3/`, flow record 7.12 and rows 46–50, project doc 14). Earlier: the documentation pass (released 14:20). No runs, no flow code changed | 2026-10-27 |
| Claude Code | **released 2026-10-27 13:35 CET**: the runs are finished; the write-up goes to Cowork (Imasha's decision) | 2026-10-27 |

## Plan v4 (s4-s5), from 2026-11-03

**Goal** (Imasha): S4 and S5 (block placement, overall placement and routing) on the 5T and LOADBench, with the final
layouts checked by extraction and SPICE (S6, S7); stabilise; then a more complex design. Our own engine (decision
D8), keeping the flow's novelty: S2's joint budgets drive placement and routing, and every extracted parasitic is
checked against its budget. S3's unit cells lose their guard rings; S4's blocks get one each. Plan:
`docs/plan_v4_S4_S7.md`; PREREG amendment of 2026-11-03.

| Phase | Work | State |
|---|---|---|
| 0 | Freeze test for S0–S2; plan; PREREG amendment; STATUS | **done**, committed `e6306879` |
| 1 | S3 without guard rings; re-run the 5T and LOADBench; compare with the reviewed S3 | **done**, committed `a3e9277e` |
| 2 | S4 on the 5T: pair, mirror, single device; rings; variants | **done**, committed `1e4d166f` (mis-titled) |
| 3 | S5 placement on the 5T; area-only baseline | **done**, committed `f26c136a` |
| 4 | S5 router on the 5T | **done**, committed `3089366a` |
| 5 | S6/S7 on the 5T | **done**, committed `27a075a6` |
| 6 | LOADBench through S4–S7 | **done**, committed `6d0c6bb7` |
| 7 | Stabilise: goldens, walkthrough to S7, review, merge | **done**, committed `a5b250de` (merge: Imasha) |
| 8 | Harder design: `ttsky25a_fd` (Imasha), its given hierarchy | **in progress**: S0–S4 done, S5 placement done; routing next |

Phase 7 record (2026-11-04, 05:01–05:57 CET; flow record 7.21, rows 77–80):
- **The MIM capacitor:** Magic's sky130 rules charge metal4 over metal3 across the top plate too, so the 22.5 fF
  between the capacitor's plates is very likely counted twice (row 77). G6.5 and G7.5 (info) report it; the gates
  keep Magic's numbers. **With it cancelled, LOADBench is within eta on every spec** (GBW 22.71 MHz, 0.58; PM
  64.77°, 0.21); with it, G7.2 fails on GBW (22.13 MHz, 1.08).
- **Review** (independent agent): G6.2 now reads a gate net's ground C from the .ext when the netlist has none
  (LOADBench: 21 violations, FirstStageYout1 3.0 ×, outFirstStage 2.7 ×); `flat_lvs` handles cut names; G7.5's
  runs fixed before use; a missing measurement fails G7.1; m > 1 fails S4 loudly; block names, half-unit width,
  routing order (rows 78–80).
- **Goldens** for S4–S7 on both designs (28 comparisons); S5's candidates in `candidates.json.gz`;
  `docs/s4_s7_walkthrough.html` (`scripts/make_s4s7_walkthrough.py`); the S0–S3 walkthrough unchanged.
- 176 tests pass.

Phase 6 record (2026-11-04, 02:36–04:10 CET; flow record 7.20, rows 71–76):
- **S4 PASS** (9 variants): the PMOS bank gets a tap strip between P8 and P5 (LU.3: 16.0 → 10.1 µm; row 71); the
  MIM capacitor is a block of its own, tracks 1.45 µm from its top plate (capm.11; row 72).
- **S5:** 20 736 candidates; both costs chose the same placement (bank / pair / mirror / cs_stage + capacitor,
  5680 µm²): no candidate keeps outFirstStage within its 16.3 µm budget (best 1.65 ×). Top-level DRC 0 and LVS match.
  G5.4 FAIL: outFirstStage's length (1.70 ×) and series R that S3's access R had already used (G3.5's relaxation).
  Router fixes: joined tracks connected once, parallel-run limits, layout-view names in G5.4, same-net bridges
  (rows 73, 74).
- **S6:** G6.1 PASS; G6.2 FAIL on 19 of 38 elements, the largest at the Miller capacitor (out~outFirstStage 29.3 fF
  against 4.7; out 67 fF against 40). G6.4 (new, info): the C-only netlist lacks the gate nets' ground capacitance
  (8.9 %; 5T 3.6 %; row 75). kpex counts the MIM capacitor itself (758 against 230 fF).
- **S7:** every spec met (G7.1 PASS). G7.2 FAIL on GBW: 23.39 → 22.12 MHz, 54 % of the margin against 50 % allowed;
  gain −0.017 dB, PM −0.06°. PREREG predicted the failure on gain. 22.5 of the 29.3 fF coupling is between the
  capacitor's own plates as Magic extracts it (open: real, or counted twice with the device model).
- H4 not refuted (G6.2 and G7.2 both fail); H5 not testable (one placement).
- S7 runs a deck over 20 MB on its own (one R+C AC run peaks at 5.3 GB of the container's 5.9; row 76); identical
  decks run once, and S6 extracts once when both costs chose one placement.
- **5T re-run** with this code: all PASS, same placements, net3's wire use 0.42 → 0.18; PM 79.42°, GBW 101.32 MHz.
- Tests: 8 new or changed in `tests/test_s4s5.py`; 165 tests and 20 goldens pass from PowerShell.
- `.gitignore`: LOADBench's 75 MB R+C netlist (S6 regenerates it in 2 min). LOADBench's `placement.json` is 17 MB
  (20 736 scored candidates); compressing the candidate list is a Phase 7 item.

Phase 5 record (2026-11-03, 22:21–22:38 CET; flow record 7.19, row 70):
- **S6** (`src/s6/run.py`): Magic C-only and R+C extraction of both routed layouts, flat LVS, and every capacitance
  assigned to a net or a coupling.
  - G6.2: every budgeted parasitic within its S2 budget. Budget-aware worst use 0.29 (OUTP~net3); area-only 0.46.
  - G6.3 (info, kpex 2.5D): total capacitance within 5 % of Magic's, couplings within about 20 %, ground
    capacitance split differently.
- **S7** (`src/s7/run.py`): the schematic, drawn devices, C-only and R+C views in S0's AC/OP/NOISE benches.
  - Budget-aware R+C: gain 31.693 dB, GBW 101.25 MHz, PM 79.36°, power 150.5 µW, noise 339.5 nV/√Hz. All specs
    met; the worst loss is 0.15 of eta × margin (PM).
- **H4 holds on the 5T. H5 mostly:** less loss on gain, GBW and PM; noise a tie.
- **G2.0's prediction** is within 25 % for PM only (GBW −29 %, noise −41 %, gain −97 %).
- **Not evaluated:** device saturation and PVT points.
- **Bug fixed** (row 70): the R+C wrapper joined same-named ports and shorted every unit's pins (1.6 A).
- S6 and S7 are flow stages (`./flow run <d> --from S6`). 4 tests.
- `.gitignore` now ignores the `.prev` folders of S4–S7 and S7's R+C bench netlists (3 MB copies of S6's netlist):
  the Phase 5 commit is 6.5 MB, not 49 MB. The 190 `.prev` files of S4 and S5 that Phases 2–4 committed stay in
  history; to stop tracking them (files kept on disk), Imasha can run
  `git rm -r --cached outputs/S4/example_ota_5t.prev outputs/S5/example_ota_5t.prev`.

Phase 4 record (2026-11-03, 21:44–21:58 CET; flow record 7.18, rows 68–69):
- **Router** (`src/s5/route.py`): a spine router for row placements.
  - One metal4 spine per net (0.4 µm, 0.8 µm grid), via3 onto the block tracks, contact stacks from the ring body
    pins.
  - Nets in least-slack order; INP/INN mirrored jointly at ±x; port labels with the layout view's names.
  - Not the plan's general maze router; it fails loudly otherwise.
- **Both placements routed, and signed off:**
  - top-level DRC 0 and LVS a unique match against S0's layout view (with the drawn finger counts), controls
    caught;
  - every evaluated `route.*` rule passes. EM, bias-net coupling and digital crossings are not evaluated, as S2
    marked them.
- **Budget use of the wire lengths:** budget-aware 0.42 / 0.08 / 0.07 (net3 / OUTP / net1); area-only 0.77 / 0.36 /
  0.37. Same area.
- **S5 is a flow stage:** `flow status` shows S0–S5 PASS for the 5T.
- **Bugs found and fixed:**
  - row 68: instance names, so VBIAS was unlabelled and nf was not set;
  - row 69: the router's minimum-area and spacing DRC errors, and the hard pair placed one net at a time.
- **Tests:** 3 new.

Phase 3 record (2026-11-03, 21:31–21:40 CET; flow record 7.17):
- **PREREG amendment first.** S5's constants were fixed before any code: rows, gaps, enumeration, the budget-aware
  cost (λ = 10, μ = 1), the area-only baseline, and the routing layers for Phase 4.
- **S5 placement** (`src/s5/place.py`, `src/s5/run.py`; not a flow stage until routing joins).
  - 96 candidates on the 5T.
  - Both winners: mirror / pair / tail, 525.8 µm², unrouted DRC 0 (control caught).
  - Budget-aware flips the pair and the tail, so shared tracks face each other. Wire-budget use falls from 0.77 →
    0.42 (net3), 0.36 → 0.08 (OUTP) and 0.37 → 0.07 (net1) against area-only. G5.1 passes.
- **Times corrected** from the commit timestamps: Phase 1 ran 19:20–20:55 CET and Phase 2 20:57–21:28. I had
  written estimated end times before they happened.
- **Tests:** 4 new (partitions, the wire estimate, the symmetric-axis rule, the 5T placement).

Phase 2 record (2026-11-03, 20:57–21:28 CET; flow record 7.16):
- **S4** (`src/s4/run.py`, `src/s4/block.py`), now a flow stage (`./flow run <d> --stage S4`).
  - Blocks: matching groups first, then S0's blocks; one type and one body net per block.
  - Variants: AB (mirror image), ABBA and ABAB (from half units built as S3 cells), A, row.
  - Template: a row of units; met2 stubs to one met3 track per net; a met2 column for a net on both sides; one tap
    ring from the PDK's `guard_ring_draw`, labelled `<body>_body`.
  - Sign-off: DRC with nothing deferred, LVS against the IR, both with negative controls.
- **5T:** 5 variants in 33 s, all gates pass.
  - Areas: mirror AB 135 µm²; pair AB 163, ABBA 207 (common centroid), ABAB 207; tail 118.
  - The blocks are generous (track bands and ring). S5 weighs it; a denser template can follow.
- **Fixed on the way** (flow record 7.16):
  - A single-finger cell's strips go down: the template's own spacing check stopped the first run.
  - A met2 column joins a net's two tracks.
  - G4.4 now requires a geometric mirror image, because the first centroid-only measure passed ABAB.
- **Times corrected.** Phase 1's LOADBench run had been recorded in the host's clock (Sri Lanka, CET + 4:30) as
  "00:18–01:15 on the 4th". It ran 19:48–20:45 CET on 2026-11-03, as its report's own timestamp shows. Fixed here,
  in the progress log and in the flow record.
- **Tests:** 4 new (the block plan for both designs, the symmetry measures, the stub sides, the 5T blocks' sign-off).

Phase 1 record (2026-11-03, 19:20–20:55 CET; flow record 7.15 and row 67; times corrected in Phases 2 and 3):
- **Ringless cells, tried by hand first** (two 5T cells, `runs/tmp/s3ng/`):
  - DRC flags only the tap rules (LU.2, LU.3, nwell.4). S3 now defers them to S4 (`options.TAP_RULES`; counted
    from Magic's per-rule list).
  - The body pin B is a label on a small patch of the well: the n-well for PMOS, pwell (the substrate in Magic's
    sky130 extraction) for NMOS. LVS and the extraction keep B as a port.
  - The DRC negative control moved off the layout (row 67).
- **Code:**
  - `src/s3/options.py`: `GUARD = 0`, `TAP_RULES`, `cell_name()` with `_ng`.
  - `src/s3/strap.py`: the well label.
  - `src/common/pcell.py`: `drc(defer=…)`, and `lvs_device(body_port=…)`, which is not used now.
  - `src/s3/run.py`: `--guard`.
  - `src/flow.py`: S2's cells step and `--variant v1` keep ringed cells.
  - `scripts/magic_drc.sh`: the negative control's position.
- **Results:**
  - 5T: PASS, the same choices, area 200.8 → 126.9 µm², specs unchanged.
  - LOADBench: FAIL G3.5 with the same 3 relaxed types, all 216 options signed off, area 2079 → 1817 µm². P5 moves
    from `nf16_gtop` to `nf16_gboth`. Specs unchanged (PM 65.15°).
  - The PREREG prediction held: every chosen cell is smaller, and G3.3 still meets every spec.
- **Checks:**
  - S0–S2 byte-identical (freeze).
  - The two S3 goldens refreshed, the rest unchanged.
  - The S0–S3 walkthrough regenerated.
  - 3 new tests.

Phase 0 record (2026-11-03, 19:10–19:17 CET; no run):
- **Freeze.** `scripts/freeze_outputs.py` wrote `tests/frozen/s0_s2_outputs.json`: the SHA-256 of the 75 S0–S2 files
  later stages read, for both designs (top-level JSON, S0's `ref/` and `tb/`, S2's `pdk/*.json`), at `ec359567`.
  `tests/test_s4s5.py` fails if any changes; a test with one wrong and one missing entry confirmed it catches both.
- **Plan** `docs/plan_v4_S4_S7.md`: the stages, how decisions are taken (type and well rules, symmetry, designer
  rows, a budget-aware cost), the inputs, each design's blocks, the gates, the phases, and the open questions.
- **PREREG amendment of 2026-11-03**, before any S3 change or S4–S7 code: the S3 change, the gates, H4 (a layout
  within its budgets meets the specs within eta), H5 (budget-aware against area-only placement), and per-design
  predictions (the 5T passes; LOADBench fails G7.2 on gain).
- **FEEDBACK NEEDED** (plan section 8; not blocking Phase 1): LOADBench's PMOS bank ratio; drawing the ideal Miller
  capacitor as a MIM capacitor; dummies; RALF (needs a download); the harder design.

## Supervisor review (s0-s3-review), from 2026-11-02 evening

**Goal** (Imasha, for the supervisor inspection on 2026-11-03): S0–S3 run on `example_ota_5t` and `loadbench_miller`
with no ERROR, and the output of every step is shown. Work happens on branch `s0-s3-review` (from `fd8d7118`;
Phase A is tagged `phaseA-v3a`), and Imasha commits after each phase. Before the meeting she merges the branch into
`main`. `main` is at `a8c6f7d3` ("status_update", 2026-11-01), an ancestor of the branch, so the merge is a
fast-forward. It brings Phase A into `main` as well: Phase A lived on `plan-v3-phaseA` and was never merged.
(Corrected in phase 6: this line used to say `main` had not moved since the branch point.)

**Decisions** (Imasha, 2026-11-02, the recommended answers):
- the branch is `s0-s3-review`;
- LOADBench's FAIL gates are presented as explained findings, with no rule change;
- the walkthrough is Markdown plus HTML in the repo;
- the only optional follow-ups are the `USER` quirk and an Errno 22 retry.

| Phase | Work | State |
|---|---|---|
| 0 | Branch `s0-s3-review`, tag `phaseA-v3a` (Imasha) | **done** |
| 1 | Fix the `env.sh` regression (DRC/LVS scripts stopped under `set -u`); re-run LOADBench S0; refresh its golden | **done**, committed `33e6277f` |
| 2 | Robustness: the login-shell `USER` quirk; a retry on Errno 22 writes | **done**, committed `bf67fd09` |
| 3 | Clean full runs from S0 of both designs; snapshot `review`; goldens; tests | **done**, committed `214eb337` |
| 4 | `docs/s0_s3_walkthrough.md` + HTML, generated from the outputs | **done**, committed `58c4f207` |
| 5 | README "For reviewers", flow record 7.14, STATUS, log, `CLAUDE.md` test line | **done**, committed `b2448dd3` |
| 6 | Rehearsal from PowerShell; commit, merge into `main`, push (Imasha) | **done**: committed `973661c5`, merged into `main` and pushed |

*After the merge* (2026-11-03 morning; Claude Code; no S0–S3 run; committed by Imasha as `1626d11b`):
- **S3 option plot (row 65).** Explaining the walkthrough, I saw that the plot mixed the options S3 may choose
  (main mode A-bin) with the other modes' options, all drawn alike. Smaller green points next to the chosen cell
  seemed to contradict "smallest that fits".
  - Fix: the main mode's options are filled, the others hollow, with a title saying so. The plotting is now
    `plot_option_space()` in `src/s3/run.py`.
  - `scripts/replot_s3_options.py` redrew both designs' plots from the saved tables, so only the two PNGs
    changed. The walkthrough was regenerated, with a caption explaining the marking.
- **Line endings (row 66).** GitHub Desktop's checkout of `main` (Git for Windows, `core.autocrlf=true`, no
  `.gitattributes`) wrote CRLF into the 855 files Phase A and the review had changed.
  - bash could not parse `scripts/env.sh` (syntax error, line 7), so every flow command failed. It was found when
    the plot redraw stopped.
  - Fix: the 855 files were converted back to LF. Each one's bytes were then checked against its committed blob:
    854 identical, plus `src/s3/run.py` with the plot change.
  - `.gitattributes` (`* text=auto eol=lf`) makes every future checkout write LF.
    `docs/context/project_context_S0-S9.md`, committed with CRLF, is left as it is.
  - **GitHub Desktop will list the 855 files as changed with empty diffs.** Git's index still records their old
    sizes. Committing them changes nothing in their content; it only refreshes the index.
- **`flow status` time (row 66).** It showed the checkout's time (08:13) for every stage, because it read the
  report file's time. It now reads the report's provenance time: 5T 19:15–19:44, LOADBench 19:45–20:04 on
  2026-11-02.
- **Tests:** 4 new (the chosen cell is a main-mode option, for both designs; shell files are LF; the status time).
  `.\flow.ps1 test` from PowerShell: 138 passed, golden 20 of 20 OK (`runs/logs/review_fix_test.log`).
- **Docs:** README (the line-endings note, S3's plot row, 138 tests), `CLAUDE.md` (138 tests), flow record rows
  65–66 and 7.14, the progress log.
- **The walkthrough explains its results** (Imasha's request, 2026-11-03), as in my explanation to her that
  morning.
  - It opens with "How to read this page" (margin, eta and the allowance, expected need, first order vs SPICE,
    PASS/FAIL/ERROR, negative controls).
  - Each table and plot has a typed *How to read it* note (46 in all), including the layout pictures' colours,
    which were checked in the PDK's KLayout layer file.
  - 23 *What it shows here* lines are built from the numbers, e.g. which specs miss at which PVT supplies, the
    hand model's PM gap, and how many budgets fall below need. Each design also has an *In short* summary.
  - I checked every generated line against the data. The walkthrough test now requires the notes and the
    summary.

Phase 6 record (2026-11-02, to 23:20 CET; the README's commands from PowerShell, as a reviewer would type them;
nothing that rewrites the committed outputs):

| Command | Result |
|---|---|
| `.\flow.ps1 list` | the 5 designs, exit 0 |
| `.\flow.ps1 status example_ota_5t` / `loadbench_miller` | S0–S3 PASS / FAIL G0.7, FAIL G1.6, PASS, FAIL G3.5, as the README says; exit 0; no `[INFO]` lines |
| the same without `FLOW_CONTAINER` (throwaway container from the local image) | same output, 2 s |
| `.\flow.ps1 test` | 134 passed, golden 20 of 20 OK, 13 s (`runs/logs/review_p6_test.log`) |
| `make_s0s3_walkthrough.py --out runs/tmp/rehearsal/…` (the README's container form) | identical to the committed walkthrough except the commit hash in its header |

- **Found and fixed (flow record row 64):** Python held the flow's own lines until a command ended. The output had
  no terminal (`docker exec -i`), so "== unit tests" came after pytest's results, and a `run` would have shown
  nothing for 30 minutes. Both launchers now pass `PYTHONUNBUFFERED=1` on both paths; the README's direct command
  uses `python3 -u` and the quiet variable. Re-run: "== unit tests" comes first, 134 passed, golden 20 of 20 OK
  (`runs/logs/review_p6_test_unbuf.log`); the `docker run` path's golden check passes too.
- **Not rehearsed:** a live `run`. It rewrites the committed outputs (ids and timestamps), which would then have to
  be discarded in GitHub Desktop. Phase 3's full runs used the same command inside the container.
- **Records:** flow record row 64, 7.14's phase table and findings, the header and the changelog (rows 62–64);
  this file; the progress log. The statement about `main` above is corrected.

Phase 5 record (2026-11-02 evening; documentation and the launchers, no run):
- **README "For reviewers"**, right after the design table: what to read first (the walkthrough), the expected
  statuses with the reason for each LOADBench FAIL, the PowerShell commands and their run times, where the outputs
  go, and that a run rewrites the committed outputs (the results reproduce; ids and timestamps change).
  - It points at `status example_ota_5t` and `status loadbench_miller`. `status all` also lists the three plan-v2
    designs, whose October FAILs are not part of this review; the README says so.
- **Launchers:** `flow.ps1` and `flow` pass `IIC_OSIC_TOOLS_QUIET=1` to `docker exec` too, as their `docker run`
  path already did. Without it, every command started with the image's two long `[INFO] Final PATH…` lines.
- **Flow record:**
  - section 7.14, the review (phases, runs, what it found);
  - row 63, the walkthrough generator's bugs (phase 4);
  - 7.13's open list notes that the `USER` and Errno 22 items are now fixed;
  - the header's *Last updated* line, which still said 2026-10-27.
  - Merged with `scripts/merge_section7.py`.
- **`CLAUDE.md`:** the test line said `tests/test_v2.py` (24 tests). It now gives `./flow test`: 134 tests in
  `tests/`, then 20 golden comparisons.
- **`.\flow.ps1 test`** from PowerShell: 134 passed, golden 20 of 20 OK, 13 s, with no `[INFO]` lines
  (`runs/logs/review_p5_test.log`).

Phase 4 record (2026-11-02 evening, first draft generated 20:22 CET, finished after a usage-limit break; no run,
outputs read only):
- **`docs/s0_s3_walkthrough.md`** and a self-contained **`docs/s0_s3_walkthrough.html`** (pandoc, 31 images
  embedded, 3.3 MB), written by `scripts/make_s0s3_walkthrough.py` from `outputs/` only.
  - Per design: the status and run time of each stage, and an explanation of each failed gate, with its numbers
    read from the files.
  - Per stage: what it does, every gate with its result and meaning, the main numbers, the plots.
- **Checked against the reports before committing.** Three generator bugs, fixed:
  - the 5T's G0.6 table and the G3.3 "Schematic" column were empty: G0.6 keeps the values under `compare`
    (upstream vs rerun) when there is an upstream run, under `measured` otherwise (LOADBench);
  - the total device area counted one cell per type (5T 128.7 µm²), not every device as S3 does (200.8 µm²);
  - LOADBench's margins had no units (its IR has none; now taken from the spec name).
- **Notes where a table could be misread:**
  - G2.5's "within" allows 1.02 × (`TOL_USE`), which is why LOADBench's pm_deg passes at 1.007;
  - G2.8 scores every rule before the closure step, so "ours" reads unsafe on the 5T while G2.5 passes (flow
    record 7.13);
  - a G3.7 table gives the four option modes' areas.
- **The same cross-check corrected my phase 3 run times** (above).
- **Tests:** 2 new.
  - G0.6's two shapes.
  - The walkthrough covers both designs, explains every failed gate, has no empty G3.3 cell, and its area matches
    S3's own total. With the first G0.6 reading put back, the test fails, as it should.
- **README:** the walkthrough is listed under *Documents*, with its command.
- **`.\flow.ps1 test`** from PowerShell: 134 passed, golden 20 of 20 OK (`runs/logs/review_p4_test.log`).

Phase 3 record (2026-11-02 evening, final code `bf67fd09`, started from a login shell + `env.sh`, PC kept awake):

| Design | S0 | S1 | S2 | S3 | Run time |
|---|---|---|---|---|---|
| example_ota_5t | PASS | PASS | PASS | PASS | 29 min (S0 20.3, of which PVT + Monte Carlo 19.5; S2 8.2) |
| loadbench_miller | FAIL (G0.7) | FAIL (G1.6) | PASS | FAIL (G3.5) | 20 min (S0 10.8, S2 7.9) |

(Run times corrected in phase 4 from the flow summaries: I had written S1's 19.9 *seconds* as the 5T's S0 time.)

- **No ERROR anywhere.** LOADBench's FAILs are its three known findings:
  - G0.7: N3 only, 6 DRC errors (the PDK cell at its netlist size); 8 of 9 devices pass;
  - G1.6: 1 of 54 resistance checks (P5's source, a bias shift);
  - G3.5: 3 relaxed device types.
- The 5T's G0.7 passes on all 5 devices with both negative controls: DRC and LVS really run under the fixed
  `env.sh` (it was the 5T's first S0 since October).
- **Snapshots `review`** for both designs; the identity check passed. Against `after_v3a`
  (`outputs/review/<design>_after_v3a_vs_review.json`) both runs are identical:
  - the budgets (SPICE verification change 0);
  - the six budget rules' verdicts, SPICE uses and violated specs;
  - S3's cells, area and final specs (5T 200.8 µm², PM 79.95°; LOADBench 2079 µm², PM 65.17°).

  So a run from scratch with the final code reproduces Phase A's results.
- **Tests:** `.\flow.ps1 test` from PowerShell: 132 passed, golden 20 of 20 OK. The goldens still match, so no
  refresh is needed.
- **Prepared for phase 4:** the walkthrough generator, drafted and tried in `runs/tmp/` (git-ignored); it moved to
  `scripts/` in phase 4.

Phase 2 record (flow record rows 55 and 61; no run):
- **`USER` quirk.** `scripts/env.sh` keeps the part of `USER` after a newline: the image's login profile sets it
  to "1000\ndesigner". pytest's temp folder then has a normal name, and Netgen's round-trip test passes from a
  login shell. It is safe under `set -u` with `USER` unset.
- **Errno 22.** `src/common/tools.py` has `write_text()`, which retries `OSError` EINVAL up to 5 times, backing
  off 0.5 s more each try; any other error is raised at once. `write_json` uses it, and so do the ngspice log, rc
  and deck writes and the Netgen log write. The ~30 one-off `write_text` calls elsewhere in `src/` are unchanged.
- **Tests:**
  - 2 new: the retry, and the `USER` clean-up.
  - `.\flow.ps1 test` from PowerShell, as a reviewer would run it: 132 passed, golden 20 of 20 OK. The Netgen
    round-trip test now passes on that path.
- **Docs:** README ("Running the tests") and flow record rows 55 and 61, merged.

Phase 1 record (flow record row 62):
- **The regression.** My sky130A change (`70279125`, row 57) made `scripts/env.sh` source the image's
  `sak-pdk-script.sh`. That script reads unset variables (line 100: `KLAYOUT_PYTHONPATH`). `magic_drc.sh` and
  `magic_lvs.sh` run with `set -uo pipefail` and source `env.sh`, so they exited (rc 127) before Magic ran.
  - Effect: LOADBench's S0 re-run in step 12 recorded G0.7 with no DRC/LVS result for all 9 devices (`errors:
    None`). Before, N3 alone failed, with 6 real DRC errors.
  - I reported that G0.7 failure in step 12 as "the known one" without opening the per-device detail.
  - S3 built no new cell after `70279125`, so its results were not affected; the 5T's S0 dated from before.
- **The fix.** `env.sh` switches nounset off around the image's script and restores it. Two tests in
  `tests/test_phaseA.py`: `env.sh` under `set -u` (nounset kept), and a real Magic DRC through `pcell.drc` on a
  committed 5T PCell (0 errors, negative control caught).
- **Re-run of LOADBench S0**, 18:13–18:24:
  - G0.7: N3 fails (6 DRC errors, met1.6 at the PDK cell's gate pad, the known PDK finding); the other 8 devices
    pass DRC and LVS with both negative controls, identical to step 5's run.
  - The circuit IR and `pvt.json` are unchanged apart from provenance, so S1–S3 need no re-run.
  - The LOADBench S0 golden came out identical to the committed one (it records G0.7 as a gate verdict only).
- **Tests:** 130 passed; golden 20 of 20 OK.
- **Records:** flow record row 62, merged.

## Plan v3 Phase A (decided 2026-11-01): next work, for Claude Code

The plan is in **`docs/plan_v3_phaseA.md`**: steps 0–13, each with its files, change, test and "done when", plus the
predictions to write into PREREG before the runs.

**Progress (Claude Code):**

| Step | State | Result |
|---|---|---|
| 0 setup and claim | **done** 2026-11-01 16:10 CET, committed `03390202` | see below |
| 1 PREREG amendment | **done**, committed `02279b98` | `PREREG.md`, *Amendments*: "2026-11-01, Plan v3 Phase A (5T and LOADBench)". It has the plan's items 1–8 with Q3's tolerance and the do-no-harm ASSUMPTION, plus the section 4 predictions table, checked identical to the plan by diff. Text only: no code changed |
| 2 run hygiene | **done**, committed `1e53a965` | exit code 3 for a gate FAIL; S2/S3 clean output folders with `run_id`; the snapshot identity check. Tests: 99 passed, golden 20/20 OK. 5T S2 budgets identical. Details below |
| 3 nominal-only budgets | **done**, committed `47ee9df4` | `budget_corners: nominal` for the 5T and LOADBench; PVT use reported in G2.9. The 5T regression check against `after_nopvt` is exact. Details below |
| 4 S3 saturation do-no-harm | **done**, committed `81b1bdb1` | `use_check()` in S3; `TOL_USE` = 0.02 in `src/common/tolerance.py`. No change on the 5T or LOADBench: every device is saturated. Details below |
| 5 tagging and grouping | **done**, committed `651bf5d5` | dummy-aware tagger; mirror-bank rule; LOADBench designer groups. LOADBench's IR has one bank {P2, P8, P5}, consistent in G1.4; the designer file agrees fully. Details below |
| 6 one tolerance, lp_floor_k | **done**, committed `8e716213` | `TOL_USE` for every use check; `lp_floor_k` in G2.8 (Imasha's answer (a)). 5T S2 PASS; G2.8 outcome words unchanged; new reference budgets. Details below |
| 7 PM reference phase | **done**, committed `f79e53f8` | PM's reference is the 1 Hz phase rounded to the nearest multiple of 180°, in the linear model and the bench template. Both designs' G1.2 PM differences move by under 0.002°. Details below |
| 8 G2.0 route lengths | **done**, committed `8cc70503` | route stubs from the representative cells, in G2.0 and in the need the allocation uses (Imasha's answer (b), PREREG note). 5T S2 PASS: only XM5's route moves; 11 of 21 budgets move; G2.8 outcome words unchanged. Details below |
| – sky130A environment (Imasha's request, before step 9) | **done**, committed `70279125` | `scripts/env.sh` selects sky130A with the image's `sak-pdk` command; `TOOL_ENV` pins the same. Not a plan step; no rule or number changes. Details below |
| 9 SPICE vs first order | **done**, committed `fb1b9adf` | agreement fields on every SPICE-verified check (G2.5, G2.8) and the `G2.10_model_agreement (info)` summary. 5T: 72 checks, none flagged; the row-42 corner is in G2.9 at 6.34 × allowed, not binding. Budgets identical to step 8. Details below |
| 10 LOADBench hand model | **done**, committed `9370baa7` | patched copy P1 with the NMOS-mirror doublet, PREDICTED (patched, post hoc). Hand PM gap 17.0° → 1.7° (exact rational 3.0°); GBW gap 6.7 → 2.2 MHz. G1.5 unchanged and report-only. Details below |
| 11 tests and goldens | **done**, committed `2a9897c0` | pytest 124 passed + the expected 5T S2 golden failure; `./flow test` golden 19 of 20 OK; `ota5t_stress` S1 re-run: golden OK, its committed outputs put back. Details below |
| 12 re-run, snapshot, compare | **done**, committed `14e97f7e` | 5T: every prediction holds. LOADBench: S2 now PASS; S3 PM 65.17°, 3 types relaxed (6 in plan v2); ours "ok" after the tolerance fix (Imasha's answer (a)). Goldens refreshed, 20 of 20 OK. Details below (verdicts as corrected in step 13) |
| 13 documentation and review | **done**, committed `67b3b83d` | flow record rows 40–49 linked to their fixes, rows 51–61 and section 7.13; review D (9 findings, all checked; 7.9); post-hoc PREREG amendment for the at-bound tolerance; README. Details below |
| after review D 1 | **done**, committed `67b3b83d` (with step 13) | G2.8 SPICE-checks each rule's most-used PVT points again (Imasha's answer (a)). Budgets and S3 unchanged. With the PVT points: LOADBench every rule "unsafe"; 5T only `lp_floor` "ok"; row 42's sign disagreement reproduced. Details below |

After review D 1 (2026-11-02, Imasha's answer (a), about 15:00):
- **Code** (`src/s2/run.py`):
  - `top_corner_checks()` moved to module level, with an explicit pool.
  - G2.5 keeps the budgeted corners only: none in nominal mode, because its closure step would change the budgets.
  - G2.8's pool is the budgeted corners or, with `budget_corners: nominal`, G2.9's PVT constraints. Each rule's 5
    most-used points form one common set.
  - Each rule has `outcome` (every simulated check, as in plan v2) and `outcome_nominal` (nominal checks only).
  - G2.8 records `pvt_checks_simulated` and `pvt_pool`.
  - Tests: 2 new (selection, and that G2.5 and G2.8 use their own pools); 128 passed.
- **PREREG:** a dated note, post hoc, after review D.
- **Runs** (from a login shell + `env.sh`):
  - the 5T `--from S2`, 15:01–15:19: S2 took 17 min instead of 6, for the PVT checks;
  - LOADBench `--from S2`, 15:19–15:35.
  - For both, budgets are identical to the committed `after_v3a`, S3 is unchanged (5T PASS; LOADBench G3.5 as
    before), and every gate is as before.
  - `after_v3a` was re-taken for both. Goldens: 20 of 20 still OK (they do not track G2.8's words), so no refresh.
    `before_after.md` is unchanged.
- **5T** (9 PVT points simulated):

  | Rule | Outcome (nominal only) | Worst SPICE use of allowed |
  |---|---|---|
  | per_net | unsafe (unsafe) | 1.84 |
  | equal | **unsafe** (ok) | 2.76 at GBW tt, 0.9 V, 27 C, where the spec is missed |
  | lp_sum | unsafe (unsafe) | |
  | lp_floor | ok (ok) | 0.25 |
  | lp_floor_k | unsafe (unsafe) | |
  | ours | unsafe (unsafe) | 1.086, at the nominal point |

  - Ours' PVT points all sit lower in SPICE than first order says, e.g. GBW ss, 0.9 V, 85 C: 1.69 first order,
    0.07 SPICE.
  - **Row 42 reproduced:** at GBW tt, 0.9 V, 27 C, first order gives 6.42 × and SPICE −2.27 × (the GBW rises).
    The same sign disagreement shows for `lp_sum` and `lp_floor_k`. G2.10 flags 18 of 126.
- **LOADBench** (7 PVT points simulated):

  | Rule | Outcome (nominal only) | Worst SPICE use of allowed |
  |---|---|---|
  | per_net | unsafe (unsafe) | 123.6 |
  | equal | unsafe + infeasible (infeasible) | 6.3 |
  | lp_sum | unsafe + infeasible, unverified (infeasible, unverified) | 1021 |
  | lp_floor | unsafe (unsafe) | 75.6 |
  | lp_floor_k | **unsafe** (ok) | 8.4 |
  | ours | **unsafe** (ok) | 75.8, gain at sf, 0.9 V, −40 C, where the spec is missed |

  - First order is accurate there: 78.7 against 75.8.
  - H1 judged with the PVT points fails for every rule. G2.10 flags 25 of 118.
- **Flow record:** 7.13 (tables, reading, predictions for steps 6 and 9, open items), row 60, and review D's row 1
  in 7.9, merged. README: the G2.8 note.

Step 13 record:
- **Flow record** (`docs/flow_record_section7_draft.md`, merged with `scripts/merge_section7.py`):
  - rows 40–49 now point to their Phase A fix;
  - rows 51–61 are what Phase A itself found;
  - new section 7.13 covers what changed by step, the two results tables, the predictions with their outcomes,
    and what is still open;
  - a changelog line.
- **A correction of my own** before the review. I had written that step 6's prediction "ours' outcome word
  unchanged" fails for LOADBench. But step 6 kept `outcome()`'s 2 % threshold, so it changes no word. Ours'
  "infeasible" → "ok" comes from step 3 and the at-bound fix. STATUS, the log and 7.13 say so.
- **Review D** (a fresh agent, without STATUS or the progress log) returned 9 findings. Every one checked out
  against the files (table in 7.9). What was done:
  - G2.8's `after_v3a` words are labelled nominal-only, since no PVT point is simulated: FEEDBACK NEEDED.
  - The at-bound tolerance got a dated post-hoc PREREG amendment (2026-11-02), and the 1e-9 word is reported too.
  - Close calls are called ties: LOADBench's 1.007 / 1.015 / 1.032; the 5T's 1.086 vs 1.085.
  - **S3's cache** kept 208 LOADBench decks simulated under the IHP init in October. All 208 were re-simulated
    under sky130's (`runs/tmp/step13_s3_init_check.py`, log `runs/tmp/s3_init_check.log`): every measurement is
    identical, the chosen cells included. LOADBench's S3 results stand; row 57 is corrected.
  - G3.3's saturation test is unchanged for below-vdsat devices (iadc only): row 41.
  - The tables give both G2.9 counts (16/15 and 57/50, on 39 of 45 points) and the tolerance of each G2.5 "pass".
  - Step 6 is now "partly" on both designs; step 3's attribution and row 42's wording are corrected.
  - A "route part of the need" row is in both tables.
  - The `v1` variant no longer reproducing plan v2 exactly is listed as open.
- **README:** the `after_v3a` tag and how to compare tags. Always give `--json`.
- **Tests:** 126 passed (docs-only step).

Step 12 record (2026-11-02):
- **Runs**, started from a login shell + `env.sh` (sky130A pinned); no ERROR.
  - The 5T `--from S1`: 13:17–13:24, all PASS. Its S2 is identical to step 9's: 21 budgets equal.
  - LOADBench `--from S0`: 13:24–13:41. S0 FAIL G0.7, S1 FAIL G1.6 (both as in plan v2), **S2 PASS**, S3 FAIL G3.5.
- **Snapshots** `after_v3a` for both designs; the identity check passed.
- **Comparisons:** `scripts/compare_eta09_rerun.py` was called with `--json outputs/phaseA/<d>/compare_<first>_vs_after_v3a.json`.
  - The plan's command had no `--json`, so it would have overwritten the committed
    `outputs/posthoc/eta09_rerun/compare.json`.
  - The script also read that re-run's kept S2 folder and clock by design name. It now does so only for the
    `after_eta0.9_rerun` tag; the default pair's output is unchanged (checked).
- **LOADBench, plan v2 → `after_v3a`:**

  | | before (v1) | after (v2) | post hoc least-bad | **after_v3a** |
  |---|---|---|---|---|
  | S2 | PASS | FAIL G2.3, G2.7 | (same S2) | **PASS** |
  | Round-1 t | 0.076 | 0.00094 | | **0.497** |
  | Starved | 21/40 | 39/42 | | 29/40 |
  | S3 relaxed types | 3 | 6 | 6 | **3** |
  | S3 PM | 64.91° | 48.06° | 64.73° | **65.17°** |
  | S3 GBW (MHz) | 22.96 | 22.55 | 22.74 | 23.02 |
  | S3 area (µm²) | 2342 | 4396 | 2142 | **2079** |
  | Power (µW) | 551 | 361 | 555 | 554 |

- **Predictions (section 4):**

  | Step | 5T | LOADBench |
  |---|---|---|
  | 3 | Held at step 3; step 8's choice (b) later moved the need, so t is now 3.93 | **Mostly.** 37 of 40 budgets larger (geomean ×97). Smaller: P2.d (10× cap, need cut by step 8's route), P5.s (need ÷7 from step 8, budget 0.18 → 0.63 × need), tail~ibias (at the cap in v2, now binds on GBW). 29 of 40 are still starved: no longer from the PVT points, but at nominal, since G2.0 gain is 1.00 of margin and eta is 0.5. PVT points over 1.0: yes, 57 (worst gain at `sf_v0.9_t-40`, 78.7 ×) |
  | 4 | holds (G1.1 pass) | holds (G1.1 pass) |
  | 5 | holds | holds (G1.4 pass) |
  | 6 | holds | G2.5 passes (PM at 1.007). `lp_floor_k` has more room in total (Σ budget/need 276 vs 39), with 12 of 40 elements below `lp_floor`. **"Ours' outcome word unchanged" holds** for step 6 itself: `outcome()` already had the 2 % threshold before Phase A, so step 6 changes no outcome word. (Corrected in step 13: this cell first said "fails".) Between plan v2 and `after_v3a`, ours goes "infeasible" → "ok". That comes from step 3, since the floors fit at the nominal corner (G2.7 FAIL → PASS), and from the at-bound fix below; before that fix, the word stayed "infeasible" only through a rounding edge |
  | 7 | holds (2.0e-5°) | holds (1.6e-3°) |
  | 8 | holds (small change) | holds: G2.0 gain 6.64 → 1.00, PM 3.74 → 0.79, GBW 0.91 → 0.34 |
  | 9 | holds | listed: 4 checks, all baselines (per_net GBW and PM; lp_sum gain with a sign disagreement, first order 0.31 vs SPICE −8.69; lp_sum GBW). None for ours |
  | 10 | — | holds (17.0° → 1.7°) |
  | 12 | holds exactly: area 200.8 µm², the same cells, none relaxed, the same final specs as `after_nopvt` | holds: 3 relaxed < 6; PM 65.17° ≥ 64.7° |

- **Tolerance fix** (Imasha's answer (a), about 13:47):
  - **The bug.** Phase 2 (`budgets.refine`) leaves a pinned budget xm × (1 − 10⁻⁹) of room. G2.8's score
    counted "below floor" and "starved" below floor or need × (1 − 10⁻⁹), so a budget at its floor fell either
    side by rounding.
  - **On LOADBench,** 7 budgets sat at floor × (1 − 10⁻⁹). One, `ibias~out` (20.38719997961 against 20.3872),
    landed 10⁻¹³ on the wrong side, and ours was scored "infeasible".
  - **The change.** `src/s2/baselines.py` has `AT_BOUND_TOL` = 10⁻⁶ for both tests, and the snapshot's "starved"
    count in `scripts/compare_before_after.py` uses the same. Reporting only: no budget changes.
  - **Re-run.** LOADBench's S2 and S3 ran again, 13:48–13:55, and `after_v3a` was re-taken. Ours is now "ok",
    with nothing below a floor. Every other number and word is identical to the first run, including S3's cells,
    PM and area.
  - On the 5T no budget sits within 10⁻⁶ of its floor or need: no effect.
  - Test: `test_budget_at_its_floor_or_need_is_not_below_it`, with LOADBench's numbers.
  - **For step 13:** a journey row in flow record 7.1 (from row 51). PREREG is unchanged: the definition, "budget
    below the library floor", stays; only its numerical tolerance moved.
- **G2.8 on LOADBench, plan v2 'after' → `after_v3a`:**
  - per_net: unsafe + infeasible → unsafe (6.77);
  - equal: infeasible → infeasible;
  - lp_sum: unsafe + infeasible (unverified) → infeasible (unverified, 1 failed run);
  - lp_floor: unsafe + infeasible → unsafe (1.03);
  - lp_floor_k: new, ok (1.015);
  - **ours: infeasible → ok (1.007).**
- **Goldens (Q4).** `python3 -m src.flow snapshot <d> --stage all` for both designs. The 5T's S0 snapshot came out
  identical, since S0 was not re-run. Then `pytest tests/`: 126 passed. `./flow test`: golden 20 of 20 OK.
- **`docs/before_after.md`** was regenerated (`compare_before_after.py report`).
  - Only the 5T and LOADBench tables changed, each gaining an `after_v3a` column. The other designs' sections and
    every earlier column are unchanged (checked in the diff).
  - The introduction has a line for the new tag.
  - The first write hit Errno 22 (the known transient file lock on the Windows mount); the retry worked.
- **Comparison files:** `outputs/phaseA/example_ota_5t/compare_after_nopvt_vs_after_v3a.json` and
  `outputs/phaseA/loadbench_miller/compare_after_posthoc_leastbad_vs_after_v3a.json`.

Step 11 record (no code changed):
- **`python3 -m pytest -q tests/`** (`bash -c` + `env.sh`): 124 passed, 1 failed.
  - The failure is the 5T S2 golden, as since step 3. It still holds plan v2's PVT budgets; the plan refreshes
    it in step 12 (Q4).
  - So the suite cannot pass "in full" before step 12. Every other test passes.
- **`./flow test`** (unit tests + golden comparison of the committed outputs, no re-run): golden 19 of 20 OK.
  - The other four designs (`iadc_ota`, `loadbench_miller`, `ota5t_stress`, `ttsky25a_fd`) match on S0–S3, and so
    do the 5T's S0, S1 and S3. LOADBench's S0 and S1 were re-run in steps 5, 7 and 10 and still match.
  - The 5T S2 has 29 differences: budgets from steps 3, 6 and 8. One is
    `verify.gbw_mhz@tt_v0.9_t27: missing now (was -0.1635)`, row 42's SPICE result, which nominal budgets no
    longer simulate.
- **`./flow test --design ota5t_stress --stage S1 --rerun`** (13:09–13:10; started as `CLAUDE.md` says, from a
  login shell): the shared code still runs on a frozen design.
  - S1 rc 0, golden S1 OK.
  - **Differences against the committed S1** (`runs/tmp/step7_diff.py`): only PM values, from step 7's reference
    (the 1 Hz phase is −4.5 × 10⁻⁶°). G1.2's PM difference went from 0.019684° to 0.019680°. Every other number is
    identical. The rest are keys added by code since that S1 was made (2026-10-25: G1.1 `not_saturated` and
    `dummies_excluded`; G1.4 `consistent`, `ratio_Wm`, `not_matching_blocks`) and provenance (time, commit,
    package hash).
  - **Not regenerated:** `pkg_yaml()` in `src/flow.py` reads a package without its `inherit`, so `ota5t_stress`
    gets no `s1_extras` and its `symbolic_patch_check.json` was not rewritten. This is existing behaviour.
  - **`--rerun` writes in place.** It overwrites `outputs/S1/<design>/`, so this frozen design's committed S1
    files, flow summary and S1 logs were set aside first and copied back after. Its golden was not refreshed. The
    re-run's outputs are kept in `runs/tmp/step11_rerun_outputs/`. README now says that `--rerun` overwrites.
  - The unit tests inside that run also failed `test_round_trip_matches`. That is the login-shell `USER` quirk
    (step 7 notes), not a code change; with `bash -c` it passes.
- **Suggestion (not done):** the quirk bites `./flow test` whenever it runs from a login shell, as `./flow` and
  `flow.ps1` do. Two one-line fixes are possible, and each needs your OK:
  - give pytest `--basetemp=runs/tmp/pytest` in `src/flow.py`'s `cmd_test`;
  - or clean `USER` in `scripts/env.sh`.

Step 10 record (A5, row 49; pending task 1m, LOADBench only):
- **What changed.**
  - New `src/s1/symbolic_patch_miller.py`. The 5T's `symbolic_patch.py` is unchanged.
  - It writes `inputs/loadbench_miller/upstream_patched/equations.predicted.P1.json`, a copy of the hash-frozen
    `circuits/loadbench_miller/upstream/equations.predicted.json`, labelled **PREDICTED (patched, post hoc)**.
    Nothing is written into `circuits/`.
  - **The copy's first-stage transconductance:** Gm(s) = gm1/2·(1 + 1/(1 + s·τm)) = gm1·(1 + s·τm/2)/(1 + s·τm).
    - τm = C_m / g_m, where g_m = gm + gds of N1 (diode) + gds of P7 (mirror-side input).
    - C_m is the S1 linear model's capacitance at `FirstStageYout1`, as the plan says. It is written as
      C4_N1 + the rest: C4 of the diode device sits on no other node, so the patched model also gives a symbolic
      sensitivity to that node, as the 5T's patch does.
    - The doublet's pole is at 1/τm and its zero at 2/τm. Gm(0) = gm1, so the DC gain is the original's.
  - **wu** solves the magnitude condition with the doublet exactly (the 5T P1 form). PM adds
    atan(wu·τm) − atan(wu·τz) to the original lags.
  - **Symbols:** the mirrored half uses the file's gm1 (G1 of P6), a matched-pair assumption; P6 and P7's gm
    differ by 0.9 %. A 1:1 mirror (N1 = N4) is assumed.
  - **Package and flow:** `s1_extras: [symbolic_patch_miller]` in LOADBench's package, and the step in
    `src/flow.py`'s S1 branch, next to `symbolic_patch`. Documented in `docs/INPUTS.md`, the template and README.
- **The mirror node** (S1 OP and linear model):

  | Quantity | Value |
  |---|---|
  | C, linear model | 1142 fF |
  | C, sum of the file's level-0 symbols on the node (comparison only) | 1340 fF, +17 % |
  | g_m (equals the linear model's) | 238.46 µS |
  | τm | 4.79 ns |
  | Pole / zero | 33.2 / 66.4 MHz (the plan's "about 33 MHz") |

- **Results** (`outputs/S1/loadbench_miller/symbolic_patch_check.json`, `plots/symbolic_patch.png`):

  | Model | PM | Gap to SPICE (65.32°) | GBW | Gap to SPICE (23.39 MHz) | Gain |
  |---|---|---|---|---|---|
  | Original (G1.5) | 82.35° | +17.02° | 30.08 MHz | +6.69 | 58.05 dB |
  | P1 | 66.99° | **+1.67°** | 25.54 MHz | +2.16 | 58.05 dB |
  | P1, exact rational H(s) | 68.28° | +2.95° | 24.03 MHz | +0.64 | |
  | Original, exact rational H(s) | 83.34° | +18.0° | 27.85 MHz | +4.46 | |

  - **Mirror-node sensitivity.** The original gives 0 by construction. P1 gives PM −0.00485 °/fF and GBW
    −0.00437 MHz/fF, against SPICE's −0.00376 and −0.00364: the right sign, 29 % and 20 % high.
  - At the output, P1 gives PM −0.0030 °/fF, against SPICE's −0.0025; the original gives −0.0035.
- **Prediction (section 4), step 10:** holds. The hand PM gap falls from about 17° to a few degrees (1.7°; 3.0°
  with the exact H(s)). It was fitted after seeing this circuit, so it still has to be judged on other designs.
- **Checked:**
  - **G1.5:** stays as it was, report-only (pass `None`), computed from the unpatched file.
  - **S2:** reads no hand model (a test checks that no S2 source mentions `symbolic`, `upstream_patched` or
    `equations`), so its budgets cannot change.
  - **LOADBench S1 through the flow** (12:19, 23 s): S1/run rc 3, G1.6 FAIL as in plan v2; the new step rc 0.
    Every S1 number is identical to step 7's. Only provenance changed: time, commit, and the package hash, from
    the new `s1_extras`. It is LOADBench's first S1 run with sky130A pinned.
- **Tests.** 4 new:
  - the patched copy's structure: label, hash of the original, term order, unchanged gain;
  - the exact H(s) with and without the doublet;
  - LOADBench's results: the gap closes, the original matches G1.5, the 33 MHz pole, nothing in `circuits/`;
  - S2 reads no hand model.

  `tests/test_phaseA.py` has 38 tests, all passing. The full suite is 124 passed plus the expected 5T S2 golden
  failure.
- **Note.** The new module takes the PM reference rounded to 180° (step 7) in its exact check. The 5T module
  (`symbolic_patch.py`) still uses the phase at 1 rad/s unrounded. Its effect there is negligible, with the
  dominant pole near 2 MHz, so it is left as it is.

Step 9 record (row 42; pending task 1e):
- **What changed** (`src/s2/run.py`):
  - `agreement()` adds four fields to every check S2 simulates (G2.5 rows, every iteration; each G2.8 method's
    SPICE rows):
    - `first_order_use_frac_of_allowed` and `spice_use_frac_of_allowed`, both as a fraction of eta × margin;
    - `diff_frac_of_margin` = |SPICE − first order| / margin;
    - `sign_disagrees`.
  - **Naming, not in the plan:** the plan calls the first two `first_order_use` and `spice_use`. But `spice_use`
    already holds G2.5's raw use in the check's units, read by the closure step, the plots and the snapshots. The
    new names follow G2.8's existing `spice_use_frac_of_allowed`.
  - `model_agreement()` builds `G2.10_model_agreement (info)` (pass `None`):
    - every check with a sign disagreement or a difference above `MODEL_AGREEMENT_FLAG` = 0.25 of the margin,
      with its source ("G2.5 iteration k", "G2.8 <method>");
    - the 0.25 is an ASSUMPTION for flagging only, and the report says so;
    - failed runs (no SPICE value) are not compared.
  - **PVT points.** With `budget_corners: nominal` they are not SPICE-verified. G2.10 lists each spec's worst G2.9
    point (first order) beside the nominal check's first-order and SPICE use. When the point is over 1 while the
    nominal check is within its allowance in SPICE, it adds a note saying so.
  - With `--no-spice`, G2.10 says nothing was simulated.
- **5T S2 run** (21:53–21:58, PASS; the first run with sky130A pinned, launched from a login shell):
  - **Budgets:** identical to `budgets_step8.json` (largest relative difference 0.0). That confirms step 9 only
    reports and the environment change moves no number. All 123 ngspice logs show "hs a".
  - **G2.10:** 72 checks compared, none flagged, no sign disagreement. The largest differences:
    - ours / G2.5: PM, first order 1.000 vs SPICE 0.825 of allowed, a gap of 0.088 of the margin;
    - lp_sum and lp_floor_k: GBW 0.999 vs 0.748 (0.126);
    - per_net: PM 1.493 vs 1.158 (0.168).
  - **PVT worst points** (first order; all three noted as differing from the nominal SPICE result):

    | Spec | Worst G2.9 point | Use of allowed | Nominal SPICE use |
    |---|---|---|---|
    | GBW | `tt_v0.9_t27`, row 42's corner | 6.34 | 0.587 |
    | PM | `sf_v1.1_t-40` | 1.23 | 0.825 |
    | gain | `fs_v0.9_t-40` | 1.07 | 0.972 |

    G2.9 has 16 point × spec checks over 1 (19 in step 3, before steps 6 and 8 changed the budgets).
  - Row 42 in plan v2: at that corner first order said full use, but SPICE measured −0.16 of the margin, i.e. the
    GBW rose. With nominal budgets the corner is not simulated, so that sign disagreement is reported from plan v2
    only. G2.10 says the corner's figure is first order.
- **Predictions (section 4), step 9:** the 5T's holds: the row-42 corner appears in the PVT report and no longer
  binds. LOADBench's ("listed checks, if any") is read in step 12.
- **Tests.** 2 new, on fake numbers: the agreement fields, including a failed run, and the G2.10 summary (flagging,
  failed runs not counted, the PVT note). `tests/test_phaseA.py` has 34 tests, all passing; the full suite is 120
  passed plus the expected 5T S2 golden failure.

sky130A environment record (Imasha's request, 2026-11-01 evening, while step 9 was being read):
- **Why.** iic-osic-tools starts on its default PDK, IHP-SG13G2: the login profile sets `PDK`,
  `SPICE_USERINIT_DIR`, `KLAYOUT_PATH` and so on for IHP. ngspice then reads IHP's init and not sky130's (step 8
  record).
- **What changed.**
  - `scripts/env.sh` now calls the image's own switch, `source /foss/tools/sak/sak-pdk-script.sh sky130A`, which is
    what the `sak-pdk` alias runs. It then checks that `PDK` and `SPICE_USERINIT_DIR` are sky130A's.
    - The script returns status 1 for every PDK except GF180, because its last line is `[ -n "$GF_PDK_OPTION" ] &&
      …`. So `env.sh` judges by the variables, and `source scripts/env.sh && …` (as in `./flow`) keeps working.
  - `src/common/tools.py`: `TOOL_ENV` pins the same variables `sak-pdk sky130A` sets: `PDKPATH`,
    `SPICE_USERINIT_DIR`, `KLAYOUT_PATH` and `STD_CELL_LIBRARY` (`PDK` and `PDK_ROOT` were already pinned). That
    covers ngspice, Magic, Netgen and KLayout started from a shell that did not source `env.sh`.
  - `CLAUDE.md` (environment) and README say so.
- **How the sky130 init is reached.** `sky130A/libs.tech/ngspice` holds a file named `spinit`, not `.spiceinit`.
  ngspice therefore falls back to `$HOME/.spiceinit` (`/headless/.spiceinit`: `ngbehavior=hsa`, `ng_nomodcheck`,
  `enable_noisy_r`). Checked: with `HOME` pointed at an empty folder the same run has "No compatibility mode".
  - So the PDK's own `spinit` (KLU solver, 8 threads) is not used; the solver stays SPARSE 1.3, as in every run so
    far.
- **Checked.**
  - A login shell + `env.sh`: `PDK`, `PDKPATH`, `SPICE_USERINIT_DIR`, `KLAYOUT_PATH` and `STD_CELL_LIBRARY` are
    sky130A's, and `./flow status` runs.
  - A login shell left on IHP, without `env.sh`: `run_ngspice` on TTSKY's noise bench reads the sky130 init ("hs
    a", no OSDI errors) and gives 139.742 nV/√Hz, the sky130-init value.
  - Tests: from `bash -c` + `env.sh`, 118 passed plus the expected 5T S2 golden failure. From a login shell, the
    `USER` newline quirk (step 7 notes) still fails the netgen round trip; `sak-pdk` does not touch `USER`.
- **Effect on results.** None expected: the S0 benches agree to 7 × 10⁻⁶ between the two inits (step 8 record).
  From now on every run uses the sky130 init. Step 12's re-run then has one init for all of Phase A's outputs;
  until then the committed outputs mix both.

Step 8 record (row 44; pending task 1g; Imasha's answer (b)):
- **What changed** (`src/s2/run.py`):
  - `route_sizes()` gives each device the bounding box of its type's representative S3 cell. That is the cell
    G2.7 already picks, and whose capacitance plan v2 already put in the need. Devices of a type with no
    representative cell, and passives, keep S0's as-sized PCell, marked `route_from: as-sized PCell`.
    - m > 1 is scaled as √m × the unit cell's sides, marked ASSUMPTION in the code. Neither design has m > 1.
  - S2 builds the problem once with the as-sized PCells to find the representative cells, then again with their
    route lengths. The element set is the same; the floors are recomputed if it ever differs.
  - The need's wiring part is now the representative route. Each element keeps the as-sized wiring as
    `w_parts.wiring_as_sized_pcell`.
  - G2.0 records `route_lengths` (per device: source, half-perimeter, as-sized half-perimeter) and a second column,
    `fraction_of_margin_route_as_sized_pcell`. Its note no longer says "default device cells".
  - The `v1` variant keeps the as-sized route.
- **PREREG:** a dated amendment at the end, "Plan v3 Phase A step 8: G2.0's route part is part of the expected
  need". Item 6's "no budget changes" was written assuming G2.0 is information only.
- **5T S2 run** (20:40–20:46, PASS; reference budgets `outputs/phaseA/example_ota_5t/budgets_step8.json`, run_id
  `2026-11-01T20:40:25-6fd258ff`). The results match the probe exactly.
  - **Route:** only XM5 moves, from 14.42 to 9.06 µm; its representative cell is the nf = 2 one. The other four
    devices move by ≤ 0.01 µm.
  - **G2.0:** small change, as predicted. GBW 0.058 → 0.054 of margin, noise 0.015 → 0.013, sat_XM5 0.147 → 0.127;
    gain and PM unchanged. The as-sized column reproduces step 6's G2.0 exactly.
  - **'Ours':**
    - round-1 t goes from 3.401 to 3.925;
    - 11 of 21 final budgets change: XM5.s −25.3 %, XM5.g −8.4 %, XM5.d −6.8 %, net1 −5.5 %,
      XM1+XM2.s +14.4 %, and 6 more by +0.3 % to +1.8 %;
    - min budget / need goes from 3.23 to 3.73.
  - **G2.5:** passes after 2 iterations, with the same closure (the 3 gain-harmful budgets) and gain at 0.972 of
    its allowed use. sat_XM5 is at 0.983.
  - **G2.8 outcome words are unchanged** (per_net unsafe, equal ok, lp_sum unsafe, lp_floor ok, lp_floor_k unsafe,
    ours unsafe 1.086). Two details changed:
    - lp_floor's SPICE use went from 0.293 to 0.254;
    - lp_sum and lp_floor_k now starve one element, XM5.d at 0.75 × its need. `lp_floor_k` is now below `lp_floor`
      on the 5T too (1 of 21), the starving that answer (a) expected.
- **LOADBench** (probe on its current S0/S1 and the nominal problem; its S2 runs in step 12):
  - the N3 route goes from 244 to 34 µm, P5 from 446 to 61, and the rest 2–3× shorter;
  - G2.0 gain goes from 6.64 to 1.00 of margin, PM from 3.74 to 0.79, GBW from 0.91 to 0.34;
  - round-1 t goes from 0.074 to 0.50.
- **Predictions (section 4), step 8:** both hold. On the 5T, G2.0 changes little. On LOADBench, G2.0's route part
  drops a lot (probe; confirmed in step 12).
- **Tests.** 4 new:
  - LOADBench's N3 and P5 routes equal their representative cells, and the need's wiring moved with them;
  - on the 5T only XM5 moves;
  - m > 1 scaling and the fallback;
  - G2.0 = rate × the need the allocation uses (replaces "budgets identical").

  `tests/test_phaseA.py` has 32 tests, all passing. The full suite is 118 passed plus the expected 5T S2 golden
  failure.
- **Found on the way: ngspice's init depends on the launching shell** (not caused by step 8; question under *Open
  questions*).
  - This run was started with `bash -c`. Step 6's 5T S2 was started with `bash -lc`, as in `CLAUDE.md`, `./flow`
    and `flow.ps1`. The image's login profile sets `SPICE_USERINIT_DIR` to the IHP PDK's folder, so ngspice skips
    `/headless/.spiceinit` and its sky130 settings: `ngbehavior=hsa` (the nf vs W compatibility) and
    `enable_noisy_r`.
  - That is why many S2 `work/` logs changed: the header says "hs a" instead of "No compatibility mode", the IHP
    init's OSDI load errors are gone, and so are 9 `bsim4v5.out` files.
  - **Numbers:** `runs/tmp/envcheck.py` ran every design's S0 benches under both inits.
    - All 15 decks give identical measurements except TTSKY's: noise 139.742 vs 139.741 nV/√Hz (7 × 10⁻⁶), and
      a DC differential output of 10⁻¹⁴ vs 10⁻¹³ V, zero either way.
    - The OP values in the 5T's S2 logs are identical, and so are G2.8's SPICE uses for unchanged budget sets.
    - Not checked: S3's extracted-cell decks and the hand-layout PEX runs.
  - The committed outputs already mix both inits. S0 of the 5T, iadc and TTSKY used the sky130 one; LOADBench's
    S0 (step 5), both S1 runs (step 7) and the step 6 S2 used the IHP one.

Step 7 record (A6, row 46; pending task 1j):
- **What changed.**
  - `src/s1/linear.py`: `pm_reference()` rounds the 1 Hz phase to the nearest multiple of 180°, as
    `floor(x / 180 + 0.5)`, like the bench. `metrics()` subtracts that reference instead of the 1 Hz phase.
  - `FastModel.delta()` uses the same reference for the base and the changed model. The PM change is now the
    change of the phase at the UGB; plan v2 also subtracted the change of the 1 Hz phase. The reference moves only
    if a change carries the 1 Hz phase across a rounding boundary, and then exactly as in `metrics()`.
  - `src/s1/run.py`: G1.2 and `linear_model.json` gain a `pm_reference` record:
    - the linear model's 1 Hz phase, its reference, and its PM by plan v2's rule;
    - the frozen AC bench's 1 Hz phase, read from that bench's own `ph_dc` measurement in S0's log, with its
      distance from the reference and its PM by both rules.
  - `scripts/benchlib.py`, AC template: `let ph_ref = 180 * floor(ph_dc / 180 + 0.5)`, and PM uses `ph_ref`.
    ngspice-47 has no `round()` ("no function as round with that arity"), so it uses the plan's fallback.
- **Checked in ngspice-47** (one pole at 25 Hz, DC gain ±10⁴): PM 90.006° for both signs (reference 0° and 180°).
  The old formula gives 92.296°, 2.29° high.
- **Frozen benches** (not edited): the 1 Hz phase is −0.0000205° for the 5T and −0.00160° for LOADBench (S0's AC
  logs). Both are below the plan's 0.01°, far from its 0.05° stop.
- **S1 re-run, done-when check** (G1.2 PM difference, linear − SPICE, against plan v2's 'after' snapshot):

  | Design | Plan v2 | Now | Change |
  |---|---|---|---|
  | example_ota_5t | +0.010946° | +0.010926° | −0.00002° |
  | loadbench_miller | −0.026880° | −0.028522° | −0.00164° |

  - Both are within 0.01°. Gain and GBW differences are identical, and G1.2 passes for both.
  - The PM recomputed by plan v2's rule from the record equals the committed linear PM exactly (80.945746°,
    65.296420°).
- **What else moved in S1:** only PM values. The PM rates per fF and per Ω moved by 10⁻⁷ to 3 × 10⁻⁴ (relative),
  and so did the quantities built from them (`fF_to_consume_margin`, G1.3/G1.6 PM checks). Every non-PM number is
  identical (checked file by file against `HEAD`, `runs/tmp/step7_diff.py`).
- **The 5T's S1 had not been re-run since 2026-10-26.** Its new files also carry fields added by later commits:
  - `not_saturated` and `dummies_excluded` in G1.1;
  - `consistent`, `ratio_Wm` and `not_matching_blocks` in G1.4 and `intent.json`;
  - `dummies_excluded_from_tags`;
  - a new package hash, from step 3's `budget_corners`.

  No value changed with them.
- **S2 and S3 still use the S1 numbers from before step 7.** The differences are at most 3 × 10⁻⁴ relative on PM
  rates. Step 12's re-run uses the new S1.
- **Tests.**
  - 4 new: the 25 Hz one-pole case through `metrics()`, `FastModel.delta()` against `metrics()` at a 25 Hz pole,
    the bench template run in ngspice, and the frozen benches' 1 Hz phase for the two designs.
  - `tests/test_phaseA.py` has 28, all passing.
  - Full suite (tools on `PATH`): 114 passed, plus the expected 5T S2 golden failure. The S1 goldens of both
    designs still match after the re-run.
- **Notes.**
  1. **Package scripts left unchanged.** `scripts/make_loadbench_package.py` and `scripts/make_ttsky25a_package.py`
     carry their own AC control blocks with the old formula. They wrote the hash-frozen benches, so changing them
     would make their output differ from the frozen files.
  2. **Hand models unchanged.** `src/s1/symbolic_patch.py` (the hand models) measures PM from the phase at
     1 rad/s, unrounded. It is not in step 7's list. On these designs the effect is negligible (dominant poles near
     2 MHz and 28 kHz). Step 10 edits that file and can use the same reference.
  3. **A test-environment quirk, not caused by step 7.** In a login shell (`bash -lc`), the image sets `USER` to
     "1000\ndesigner". pytest puts that into its temp folder name, and netgen then fails
     `test_s0_integration.py::test_round_trip_matches`. It passes with `bash -c` + `source scripts/env.sh`, or with
     `--basetemp`. README says so.

Step 6 record (A4; review C items 3, 5 and 11; pending tasks 1e and 1i):
- **One tolerance.** `TOL_USE` = 0.02 of the allowed use (eta × margin) is now used by:
  - G2.5's gate and its closure step, which shrinks budgets when SPICE use exceeds allowed × (1 + tol);
  - `outcome()`'s "unsafe" line;
  - S3, as `TOL_USE` × eta of the margin, which equals the old 1 % at eta 0.5.

  `TOL_VERIFY` and S3's `TOL` are gone. The 10 % is kept only as a reported column,
  `within_first_order_error_10pct`.
- **Effect on the 5T** (both runs give the same budgets and G2.5):
  - G2.5's first round found gain at 1.086 × its allowed use: first order says 1.000, SPICE says 8.6 % more.
    With the old 10 % this would have passed without a closure.
  - The closure shrank the 3 gain-harmful budgets (`XM1+XM2.d`, `XM3+XM4.d`, `XM3+XM4.s`) by 9.76 %. The
    second round has gain at 0.972 (SPICE 0.8245 against 0.8485 allowed), and G2.5 passes. The other 18 budgets
    are unchanged.
  - New reference budgets for steps 7–10: `outputs/phaseA/example_ota_5t/budgets_step6.json` (run_id
    `2026-11-01T19:33:06-7dfda46c`). It differs from `budgets_step3.json` only in those 3 elements.
- **`lp_floor_k`** (Imasha's answer (a), 2026-11-01 19:18 CET). `lp_floor()` takes an `upper` cap in units of
  need. `lp_floor_k` is the same LP with ours' bounds, [floor, 10 × need]. G2.8 now scores six rules; the plots,
  the snapshots and `docs/before_after.md` list whatever G2.8 lists, so they need no change.
- **G2.8 on the 5T** (final run; first order and SPICE at eta 0.5; every rule scored before the closure):

  | Rule | Outcome | Worst use / allowed, first order | SPICE | Starved | Budget / need, min / geomean |
  |---|---|---|---|---|---|
  | per_net | unsafe | 1.894 | 1.836 | 0 of 21 | 4.896 / 9.612 |
  | equal | ok | 0.677 | 0.714 | 1 of 21 | 0.942 / 5.632 |
  | lp_sum | unsafe | 1.000 | 1.085 | 0 of 21 | 1.453 / 8.225 |
  | lp_floor | ok | 0.294 | 0.293 | 0 of 21 | 1.0 / 1.0 |
  | **lp_floor_k** | **unsafe** | 1.000 | 1.085 | 0 of 21 | 1.453 / 8.225 |
  | ours | unsafe | 1.000 | 1.086 | 0 of 21 | 3.231 / 8.005 |

  - On the 5T, `lp_floor_k` equals `lp_sum`: the plain LP's optimum already meets every floor. It is below
    `lp_floor` for 0 of 21 elements.
  - Like ours and `lp_sum`, it fills the gain check to first order 1.000, and SPICE finds 8.5 % more, so it is
    "unsafe".
  - No SPICE run failed, and no budget is below its floor.
- **Tests.** The plan's test "`lp_floor_k` ≥ `lp_floor` element by element" was replaced, as answer (a) says, by:
  - same bounds as ours;
  - objective ≥ `lp_floor`'s, which holds whenever every floor is at most its need;
  - an example where `lp_floor_k` starves an element.

  `tests/test_phaseA.py` has 24 tests, all passing; the full suite is 110 passed plus the expected 5T S2 golden
  failure (step 3).
- **Optional phase-2 iteration cap: not done.** It matters only above 200 elements (the 5T has 21, LOADBench about
  40), so it has no effect on Phase A's designs. It would only change the frozen iadc (750) and TTSKY (2678) runs.
- **Predictions (section 4), step 6, on the 5T:** all hold.
  - G2.5 had one more check over 1.02 (gain), which the closure fixed.
  - Ours' outcome word is unchanged ("unsafe").
  - `lp_floor_k` gets more room than `lp_floor` (budget / need geomean 8.225 against 1.0).
  - LOADBench is checked in step 12. The probe on its plan-v2 numbers already shows 13 of 40 elements below
    `lp_floor`, so "more room" there has to be read as the total, not element by element.
- **Not in the plan's list:** `scripts/make_v2_figures.py` names the plan-v2 rules only. It draws plan v2's
  snapshots, which have no `lp_floor_k`, so it is unchanged. Step 13 can extend it if v3 figures need the new rule.

Step 5 record (A3, rows 47–48; D-e):
- **(a) Dummy-aware tagger** (`src/s1/run.py`).
  - `dummy_devices()`: devices in a hierarchy block of category or primitive "dummy", or with d = g = s.
  - `classify_nodes` skips them when tagging diode-connected and tail nodes. Their capacitance stays in the linear
    model.
  - `node_classes.json` lists them. Neither design has dummies, so there is no change on them; a synthetic test
    covers the rule.
- **(b) Mirror-bank rule** (`src/s0/ingest.py`, `merge_mirror_banks()`).
  - Mirror blocks of one polarity whose devices share the gate net and the source net, with a diode-connected
    device, become one block `<p|n>mos-current-mirror-bank`. The bank lists the diode device first, the blocks it
    was merged from, and the W × m ratios.
  - LOADBench: X4 {P2, P8} and X5 {P2, P5} become `pmos_current_mirror_bank_ibias` {P2, P8, P5}, ratio
    1 : 2.4298 : 23.781. Its name is unique; the two blocks it replaces were both `p_current_mirror`.
  - The 5T's blocks are unchanged (test on its committed IR).
- **(c) Designer groups.** `inputs/loadbench_miller/designer_groups.yaml` (2026-11-01, "designer review
  (Imasha)", the plan's groups and floorplan rows), pointed to by the package key `designer_groups`
  (documented in `docs/INPUTS.md`). S0's `apply_designer_groups()`:
  - compares each group with the automatic blocks; the result is G0.11 (info);
  - puts the designer's group in place of an automatic block it agrees with (`source: designer`, `agrees_with`),
    and replaces an automatic block of the same matching class that it disagrees with. Blocks of another class
    stay, so P5 can be in the bank and in the CS stage;
  - copies the floorplan rows into the IR, under `hierarchy.floorplan_rows`, for S4 only;
  - adds the file to S0's provenance.
- **LOADBench S0 + S1 re-run, 17:42–17:54:**
  - IR blocks: `cs_stage`, `input_pair`, `nmos_mirror_load`, `pmos_bias_bank`, all from the designer, all agreeing
    with the automatic blocks.
  - G0.11: full agreement.
  - S1 G1.4 PASS: the bank is one mirror group, consistent (same L 0.74 µm and model, ratio 1 : 2.43 : 23.78);
    `cs_stage` is in `not_matching_blocks`.
  - Gate results are as in plan v2: S0 fails only G0.7, S1 only G1.6.
  - The exit codes now separate them: `pcell_binding` returned 3, so S0 carried on to PVT.
- **Predictions (section 4), step 5:** all hold.
  - 5T: blocks unchanged.
  - LOADBench: one bank, consistent in G1.4; the CS stage not matched; the designer file and the automatic rule
    agree.
- **Tests.** 5 new; `tests/test_phaseA.py` has 22, all passing, and the S0 and S1 test files pass. The full suite
  is 108 passed plus the expected 5T S2 golden failure. LOADBench's S0 and S1 goldens are still OK after the
  re-run.
- **Note.** LOADBench's S2 and S3 outputs still come from plan v2. They read the new S0 IR at their next run, in
  step 12.

Step 4 record (A1, row 41):
- **What was wrong.** For a device already below vdsat in the schematic, S3 measured its check against the negative
  vds − vdsat. The limit `allowed + TOL × margin` was then negative, so every option failed, even one that did no
  harm. The slack flipped sign, so more harm looked better to the least-bad pick.
- **What changed.**
  - `src/s3/run.py`: `use_check()` is the one allowance check, used both per option and in G3.3's `within`.
    - For such a device the check is "do no harm": `u ≤ TOL_USE × |schematic vds − vdsat|`, with the slack
      against that, marked `rule: do-no-harm (below vdsat in the schematic)`. G3.3 lists the checks that used it.
    - Specs and saturated devices keep the plan-v2 formula exactly.
  - `src/common/tolerance.py`: `TOL_USE` = 0.02, the one tolerance of Q3. Step 6 wires it into G2.5, `outcome()`
    and S3's `TOL`.
- **Effect on the two designs: none** (plan prediction: "no change if every functional device is saturated").
  - S1 G1.1 passes for both.
  - S3's baseline vds − vdsat is positive for every device: the 5T's 5 devices are at least 0.0196 V above, and
    LOADBench's 8 at least 0.2045 V.
  - So every check takes the unchanged formula, and their S3 results cannot move. No re-run was needed.
  - For reference, iadc (frozen) has 45 such devices.
- **Tests.** Two new ones in `tests/test_phaseA.py`, which now has 17 passing tests. The full suite is 103 passed
  plus the expected 5T S2 golden failure from step 3; the other 19 golden comparisons are OK.
- **For Imasha:**
  1. The plan's test example ("+1 mV of harm fails" at −0.05 V) sits exactly on the limit of the committed
     PREREG rule, `TOL_USE` × 0.05 V = 1 mV, so it passes. The test checks both sides of the limit instead:
     0.5 mV passes, 2 mV fails.
     - The example would hold only with `TOL_USE` × eta × |vds − vdsat| (0.5 mV). Say if that was meant; it would
       need a PREREG amendment.
  2. G3.3 also requires every device to end saturated (vds − vdsat > 0 after layout). The plan did not change
     that, so a device below vdsat by design still fails G3.3. That is iadc's case, and the open G1.1 question. It
     does not affect the 5T or LOADBench.

Step 3 record:
- **Packages.** `budget_corners: nominal` in `inputs/example_ota_5t/package.yaml` and
  `inputs/loadbench_miller/package.yaml`.
  - **Not in the plan:** `inputs/ota5t_stress/package.yaml` inherits the 5T package, so it would have switched to
    nominal too. It now says `budget_corners: all` explicitly and keeps plan v2's behaviour.
  - A test checks the key for all five designs. The key is in `docs/INPUTS.md`.
- **S2 (`src/s2/run.py`).**
  - `allocation_constraints()`: with `nominal`, the PVT points' constraints are computed but kept out of the
    allocation. Verification and the baselines then see nominal checks only, as `--no-pvt` does.
  - `pvt_use_table()`: the final budgets' first-order use at each of the 45 points, as a fraction of eta × that
    point's margin, goes into G2.9 (info), with the worst point and the checks over 1. Where a spec has no
    constraint, the row says why.
  - `budgets.json` and `s2_report.json` record `budget_corners` and `pvt_points`. `--no-pvt` is unchanged.
- **Regression check** (5T, `budget_corners: nominal`, against the `after_nopvt` snapshot): **exact**.
  - `t_round1` 3.401087, `n_budgeted` 21, `starved` 0, `min_ratio_to_need` 3.231033: relative difference 0.
  - `expected_use_fraction` identical; `verify`, 9 SPICE checks, identical.
  - Reference budgets for steps 4–10: `outputs/phaseA/example_ota_5t/budgets_step3.json` (run_id
    `2026-11-01T17:22:43-e3ca9f36`).
- **G2.9 for the 5T:**
  - All 45 points are listed: 135 point × spec cells, 103 with a number.
  - 22 cells say "spec not met before layout". 10 say "not defined: gain below 0 dB", which covers GBW and PM at
    five 0.9 V points where the gain is −3 to −16 dB.
  - Worst: GBW at `tt_v0.9_t27`, at 7.80 × its allowed share. That is row 42's corner, now reported rather than
    binding.
  - 19 checks are over 1: reported, not gated.
- **Tests.** `tests/test_phaseA.py` has 15 tests, all passing; the full suite has 102 tests, of which 101 pass.
  - **Expected failure:** the 5T's S2 golden snapshot still holds plan v2's budgets, which were set at every PVT
    point (`budget.OUTP` 3.76 → 37.6 fF; the PVT verify checks are gone). The plan replaces these two designs'
    goldens after step 12 (Q4). Until then `./flow test` and CI report this one difference. The other 19 golden
    comparisons are OK.
- **LOADBench.** Its step 3 prediction (budgets larger than plan v2's 'after'; PVT points above 1.0 in G2.9) is
  checked when LOADBench is re-run in step 12; step 3 asks only for the 5T run.

Step 2 record:
- **Exit codes.** `src/common/hygiene.py` holds `EXIT_PASS` = 0, `EXIT_GATE_FAIL` = 3, `gate_exit()`,
  `new_run_id()` and `fresh_output_dir()`.
  - The S0 ingest and binding stages, S1, S2 and S3 return 3 on a gate FAIL; `pvt` has information-only gates.
  - `flow.run_stage` maps 0 → PASS, 3 → FAIL, anything else → ERROR, even when a fresh report exists, and stops a
    stage at its first erring command.
- **Clean folders.**
  - S2 moves the run before to `outputs/S2/<d>.prev/` and writes `run_id` and `eta` into all 7 of its JSON files.
  - S3 moves its report files the same way and keeps `sim/` (a cache, used only for identical decks) and `_cells/`.
    Its files carry `run_id`, `s2_run_id` and `eta`.
  - `.prev` folders are git-ignored.
- **Snapshot check.** `compare_before_after.py snap` refuses (exit 2) when the S2 files' `run_id`s or etas
  disagree, when `budgets.json` has no `s2_report.json`, or when a file is older than the S2 start in
  `flow_summary.json`.
- **New tests** (`tests/test_phaseA.py`, 12):
  - exit code to status, including a crash after writing a fresh report (row 40);
  - a stage stops at a crashed command;
  - no file from an earlier run, and caches are kept;
  - `snap` refuses mixed `run_id`s and unfinished or stale S2 files, and accepts one run.
- **Done-when check on the 5T:**
  - A baseline run with the unchanged code reproduced the committed plan-v2 budgets exactly (63 values; G2.5
    SPICE uses within 0.0021 of the margin).
  - The step 2 run then gave the same budgets again: 63 values identical, `t_round1` 1.0491, gates equal, SPICE
    uses within 0.0018.
  - One `run_id` is in all 7 files. A planted stale file went to `.prev`. All 673 files in the folder are from
    this run, and the snapshot check passes.
- **Notes:**
  - S2 now runs without its SPICE cache (the old `work/` goes to `.prev`): 5T S2 took 10.7 min instead of 3.8.
    Plan step 12's times should allow for this.
  - `pdk_parasitics` still exits 1 when its table is incomplete. That is now an ERROR that stops S2; it runs only
    when `outputs/S2/pdk/parasitics.json` is missing.
  - The flow's own exit code (`./flow run`: 0, 1 for FAIL, 2 for ERROR) is unchanged; the plan did not ask for it.

Step 0 record:
- **Container:** `layout-s0s3` is up (image `hpretl/iic-osic-tools:2026.10`), with no python3 running and nothing in
  `runs/tmp/aside/`.
- **Git (read-only):** branch `plan-v3-phaseA`; HEAD `a8c6f7d3` ("status_update"), which comes after `6c0d387a`.
  Tag `prereg-v1` points at `a8c6f7d3`. No `.git/index.lock`, and the working tree was clean.
- **Q1–Q4:** answered with the recommended answers (plan section 2). Imasha's part, the tag and the branch, is done.
- **Baseline tests, with nothing changed:**
  - `python3 -m pytest -q tests/`: 87 passed (6 s).
  - `./flow test` (`python3 -m src.flow test`): rc 0. The same 87 unit tests passed, and the golden comparison is OK
    for all 5 designs × S0–S3 (20 of 20).
  - No failure existed before Phase A.

- **Scope:** Phase A fixes on `example_ota_5t` and `loadbench_miller` only. `ota5t_stress`, `iadc_ota` and
  `ttsky25a_fd` are frozen, but they must keep passing their tests.
- **Imasha's decisions (2026-11-01):**
  - budgets at the nominal corner only, with the 45 PVT points reported, not gated;
  - allowance = eta × nominal margin, eta = 0.5;
  - LOADBench's PMOS bank keeps its sizes (P2 : P8 : P5 = 1 : 2.43 : 23.8);
  - no LLM at run time.
- **Designer grouping (Imasha's comments on the review pack, 2026-11-01):**
  - LOADBench: P2, P8 and P5 are one PMOS mirror bank. The CS stage (N3 with P5 as its load) is a functional
    group with no N3–P5 matching.
  - Floorplan rows run VDD → VSS: PMOS sources, then the diff pair, then the NMOS mirror and N3. They are recorded
    for S4.
  - iadc and TTSKY25a groupings are recorded in the Claude Doc and not used in Phase A.
- **How the pending tasks below map to plan steps:**

  | Pending task | Plan step |
  |---|---|
  | 1d | step 4 |
  | 1e | steps 6 and 9 |
  | 1f | step 2 (the TTSKY eta 0.9 re-run is out of scope) |
  | 1g | step 8 |
  | 1h | replaced by nominal-only budgets (step 3) |
  | 1i | step 6 |
  | 1j | step 7 |
  | 1k | step 5a |
  | 1l | out of scope, except the generic mirror-bank rule (step 5b) |
  | 1m | step 10, LOADBench only |
  | 1n | out of scope |

- **Questions Q1–Q4 (plan section 2): answered 2026-11-01, all with the recommended answers.**
  - Q1: tag `prereg-v1` on Imasha's commit before the amendment.
  - Q2: work on the branch `plan-v3-phaseA`.
  - Q3: one tolerance, `TOL_USE` = 0.02 of the allowed use.
  - Q4: refresh these two designs' golden snapshots after the re-run.
  - **Imasha's part:** create the tag and the branch in GitHub Desktop. At step 0, Claude Code checks that both exist.

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

**FEEDBACK NEEDED (Claude Code, 2026-11-04 10:09, Phase 8):**
1. S1's G1.2 fails on `ttsky25a_fd` because it compares two PM conventions (flow record row 81); the model agrees with
   SPICE within 0.06° under either. Fix S1 (a reviewed stage; the 5T's and LOADBench's S1 would move by < 0.05°), or keep
   it as a reported finding?
2. To fit 250 × 200 µm, matched pairs inside a macro may share a row and lose the single shared axis (plan section 10).
   Keep the outline first, or is the shared axis worth a bigger outline?

**FEEDBACK NEEDED (Claude Code, 2026-11-04 19:29, GUI and iadc):**
1. iadc_ota's x2 cannot fit the 161 µm tile: two single devices of m = 96 (XX2_M5, XX2_M6, 1.4/0.6 µm units) are
   drawn as one row of 96 copies, 198 µm. How should S4 fold such a device? (a) several single-row blocks of the
   same device, each with its own tap ring (simplest; more area); (b) a multi-row array inside one ring (more work);
   (c) fewer copies with more fingers each (changes the designer's unit-transistor style).
2. Two latent flow issues are fixed only for iadc (opt-in, so the finished designs keep their results): every
   block's stubs sit up to 0.125 µm off their strips' centres (row 95, `pin_origin: bbox`), and S5's annealing
   dropped macro shapes whose start was outside the outline (row 96, `search_from_outside`). Make them the default
   and re-run the 5T, LOADBench and ttsky S4–S7?
3. iadc_ota's layout instructions repeat the ttsky decisions (centroid/interdigitated, dummies at the row ends,
   although the netlist has the designer's own dummies) and take the whole tile as the outline (power straps and
   pins not routed): ASSUMPTIONs; confirm?

**Answered 2026-11-04 15:10 (Imasha), next work:** (1) a simple local web GUI to edit a design's schematic netlist,
hierarchy, specs and (optional) layout instructions, run the whole flow and get a simple report, with no LLM
tokens: a PowerShell server on localhost that runs the flow through docker exec (no install, the container
unchanged); an edit is saved as a new design copy (the original's frozen sources and results untouched). (2) Then
iadc_ota laid out to fit a Tiny Tapeout analog tile. (3) Then the LLM approach with the Claude CLI, after (1) and
(2) (supervisor's permission to be confirmed then).

**FEEDBACK NEEDED (Claude Code, 2026-11-04 15:00, the ttsky report):** the tile's regions are matched to the
schematic's sub-circuits by their cell names only (Diff_opamp_ly = x1, cs_p_5 = x2's PMOS, bias_dummy = bias);
is that right, and what are block_01–04, res, res_5 and the capacitor cells? (Report section 8, question 5.)

**Answered 2026-11-04 14:25 (Imasha), Phase 8.7:** (1) matching stays "common centroid or interdigitated as needed": the variant follows the spec- and area-driven cost, no extra rule without a reason (no change; G5.7 reports the result). (2) Not the independent-LLM comparison yet: first a full ttsky report for any reader, with the layouts, post-layout results and the hand-layout comparison (done: `docs/ttsky25a_fd_report.html`).

~~**FEEDBACK NEEDED (Claude Code, 2026-11-04 14:20, Phase 8.7):**~~ (answered above)
1. S5 may choose an interdigitated (ABAB) variant for a matched block when it costs less; on `ttsky25a_fd` 7 of 20
   matched blocks (budget-aware) are not common-centroid, among them the signal-path `pmos_matched_cascode_pair`
   (G5.7; flow record 7.24). Keep it (your "common centroid or interdigitated as needed"), or keep only the
   common-centroid variant where a block has one (a PREREG amendment, and S5–S7 re-run)?
2. The independent-LLM comparison (after Phase 8) needs an API connection: may Claude Code set one up, and which?

**FEEDBACK NEEDED (Claude Code, 2026-11-04 12:42, Phase 8 part 2):**
1. R+C extraction is off for `ttsky25a_fd` (Magic's extresist ran past 2 GB on the supply rings; flow record row 87).
   S7 evaluates the C-only netlist, as the hand layout was measured. Accept C-only for this design, or should R+C be
   tried another way (e.g. per sub-circuit, or with a coarser tolerance)?
2. G7.2 fails on GBW with Magic's netlist (1.26 of the allowance) and passes with the Miller capacitors' own plate
   coupling cancelled (0.45). The same question as LOADBench's (Phase 6, question 2): which number should G7.2 use?
3. About 100 direct file writes in `src/` and `scripts/` still have no Errno 22 retry (row 89). Convert them all
   (a mechanical change across reviewed stages), or leave them until one fails?

**Answered 2026-11-04 (Imasha), Phase 8 plan:** the code arranges the floorplan; specs as recommended (kept); res_packs
interleaved, matched transistors common-centroid or interdigitated; dummies; a hard outline of 250 × 200 µm; books may
follow; a branch for Phase 8; an independent LLM after Phase 8. **Still open:** the outline's orientation (ASSUMPTION:
250 µm wide, 200 µm tall).

**FEEDBACK NEEDED (Claude Code, 2026-11-04 04:10, plan v4 Phase 6; not blocking):**
1. Plan questions 3 and 5 still stand: the PMOS bank side by side (used), or units rounded to an integer ratio;
   dummies now or later (none used).
2. The Miller capacitor's 22.5 fF plate coupling is very likely counted twice by Magic (Phase 7, row 77). Should
   G7.2 gate on Magic's number (now: LOADBench FAIL on GBW, 1.08) or on G7.5's, with it cancelled (PASS, 0.58)?
3. outFirstStage's 16.3 µm budget cannot be met by any row placement of these blocks (best 1.65 ×). Options:
   accept and report it (current), let S5 place the capacitor and N3 beside the pair, or ask S2 for budgets that
   know the block sizes.
4. RALF (needs a GitHub download) and the harder design for Phase 8 (`ttsky25a_fd` or `iadc_ota`), as before.

**Resolved 2026-11-02 ~15:00 CET (Imasha): (a), G2.8 SPICE-checks PVT points again.** Done; the record is under
*Plan v3 Phase A*, "After review D 1", and in flow record 7.13. The question as it was asked:

**Was FEEDBACK NEEDED (Claude Code, 2026-11-02 14:50, after Phase A; review D 1): should G2.8 and H1 cover the PVT
points again?**
- **What happens now.** With `budget_corners: nominal` (step 3), S2's constraints are nominal only, so G2.5 and
  G2.8 SPICE-check no PVT point. Every `after_v3a` outcome word is for the nominal corner. Plan v2's words also
  covered each rule's most-used PVT points.
- **Why it matters.** H1 is defined "at every PVT corner where the schematic meets the spec", so H1 is not tested in
  Phase A. PREREG's Phase A item 1 moved budgets to the nominal corner, but did not say that G2.8 stops simulating
  PVT points.
- **(a) SPICE-check PVT points again in G2.8 (recommended).** Each rule's most-used G2.9 points, reported and not
  gated, as plan v2 did. Then re-run S2 for both designs (about 15 min) and re-take `after_v3a`. Budgets do not
  change; only the G2.8 words may.
- **(b) Declare it.** A dated PREREG amendment: in Phase A, G2.8 and H1 are judged at the nominal corner only, and
  the PVT points are reported first order in G2.9. Documentation only.

**Optional follow-ups from Phase A and review D** (none blocks anything; each is small, and needs your OK):
1. **S3's simulation cache key:** include the ngspice init (review D 4). Today's results are unaffected
   (re-simulated, identical).
2. **G2.9:** count "over" at 1 + `TOL_USE` rather than at 1 (review D 6).
3. **`budgets.refine`:** never leave a budget below its floor (review D 2), making `AT_BOUND_TOL` unnecessary.
4. **G3.3's saturation test** for devices below vdsat in the schematic (review D 5; needed before any iadc re-run).
5. **The login-shell `USER` quirk:** `--basetemp` in `./flow test`, or clean `USER` in `env.sh` (row 55).
6. **`pkg_yaml()`** should follow `inherit` (row 58).
7. **A retry on Errno 22** in the write helpers (row 61).
8. **Later phases.** Plan v3's phases B–E (`docs/plan_v3_phaseA.md`, section 1) and decisions D4–D8 wait for you.

**Resolved 2026-11-02 ~13:47 CET (Imasha): (a), fix the tolerance edge**, done in step 12; ours on LOADBench is now
"ok". The question as it was asked:

**Was FEEDBACK NEEDED (Claude Code, 2026-11-02 13:45, Phase A step 12): fix a tolerance edge that marks ours
"infeasible" on LOADBench?**
- **What happens.**
  - Ours' max-min budget for `ibias~out` equals its library floor exactly: 20.3872.
  - Phase 2 (`budgets.refine`) relaxes each max-min budget's lower bound to xm × (1 − 10⁻⁹) (`src/s2/budgets.py`,
    line 206), and the solver returns that bound: 20.38719997961.
  - G2.8's score flags "below floor" when x < floor × (1 − 10⁻⁹) (`src/s2/baselines.py`, `score`). The refined
    value is 10⁻¹³ below that threshold, so ours is scored "infeasible".
  - The budget is at its floor; the two 10⁻⁹ tolerances just don't nest.
- **Effect.** On LOADBench, ours is "infeasible" only because of this. Its SPICE worst use is 1.007 of allowed,
  within 1.02, so the outcome would be **"ok"**. On the 5T no ours budget sits at a floor: no effect.
- **(a) Fix (recommended).**
  - Make the two tests nest: `score`'s below-floor test gets a tolerance wider than `refine`'s 10⁻⁹ relaxation,
    e.g. x < floor × (1 − 10⁻⁶). It changes reporting only; no budget changes.
  - Then re-run LOADBench's S2 and S3 (about 8 min; S3 so that its `s2_run_id` matches), re-take its `after_v3a`
    snapshot, and add a journey row (flow record 7.1, from row 51) in step 13.
  - Ours' word on LOADBench then becomes "ok", so step 6's prediction "outcome words for ours unchanged" fails
    for LOADBench. The explanation line: plan v2's "infeasible" came from infeasible floors; now the floors are
    feasible and ours meets its allowance.
- **(b) Keep as is.** Report "infeasible", with a note that it is a tolerance artefact (budget at its floor to
  10⁻⁹). The prediction then "holds" only through the artefact.

**Resolved 2026-11-01 (Imasha, during step 9): select sky130A with the image's `sak-pdk` command**, done; see
"sky130A environment" under *Plan v3 Phase A*. The question as it was asked:

**Was FEEDBACK NEEDED (Claude Code, 2026-11-01 20:54; not blocking): pin ngspice's init so it does not depend on the
launching shell?**
- A login shell (`bash -lc`, used by `./flow`, `flow.ps1`, `CLAUDE.md` and the plan-v2 scripts) sets
  `SPICE_USERINIT_DIR` to the IHP PDK. Then ngspice runs without sky130's `ngbehavior=hsa` and `enable_noisy_r`.
  A plain shell reads `/headless/.spiceinit`, which has them. Details are in the step 8 record.
- On every design's S0 benches the two inits agree to 7 × 10⁻⁶. So far it is log noise, not a numerical change,
  but S3's extracted-cell and PEX decks were not checked.
- **Suggestion:** in `src/common/tools.py`'s `TOOL_ENV`, set `SPICE_USERINIT_DIR` to a repo folder holding the three
  sky130 lines, so every run uses them whatever shell started it. That changes no rule, but it touches every
  SPICE run, so it needs your OK. It could go before step 12's re-run.

**Resolved 2026-11-01 20:36 CET (Imasha): (b), the route lengths set the need everywhere**, done in step 8,
with a dated PREREG amendment. The question as it was asked:

**Was FEEDBACK NEEDED (Claude Code, 2026-11-01 20:30, Phase A step 8): should the new route lengths also set the
allocation's expected need?**
- **The conflict.** The plan changes G2.0's route lengths to the representative cells, and its test says "G2.0
  is info only, so no budget changes; 'ours' budgets identical". In the code, though, those lengths are the wiring
  part of every element's expected need (`build_problem()`: `unit` → `L_est` → `w`). G2.0 is rate × that need, and
  the allocation shares the budgets in units of the same need (`budgets.allocate`, max-min of x / w). Moving the
  lengths therefore moves 'ours' budgets.
- **Probe** (`runs/tmp/step8_probe.py`, read-only). It rebuilds the nominal problem at eta 0.5 and runs S2's own
  allocate + refine; it reproduces the committed 5T max-min budgets to 3 × 10⁻⁸.

  | | 5T: as-sized → representative | LOADBench: as-sized → representative |
  |---|---|---|
  | Route half-perimeters that change | XM5 14.4 → 9.1 µm | N3 244 → 34 µm, P5 446 → 61 µm, P8 48 → 15, N1/N4 36 → 15, P2 21 → 8.7, P6/P7 9.6 → 6.7 |
  | G2.0, fraction of margin at expected need | gain 0.086 → 0.086, GBW 0.058 → 0.054, PM 0.075 → 0.075, sat_XM5 0.147 → 0.127 | gain 6.64 → 1.00, GBW 0.91 → 0.34, PM 3.74 → 0.79 |
  | 'ours' if the need changes too | 11 of 21 budgets change (XM5.s −25 %, XM5.g −8 %, XM1+XM2.s +14 %); round-1 t 3.40 → 3.93 | 33 of 40 change, mostly up (N3.g +285 %, N1+N4.d +247 %); round-1 t 0.074 → 0.50 |

  The section 4 predictions for step 8 (5T "small change", LOADBench "route part of G2.0 drops a lot") hold
  either way. Capacitor2 has no library cell, so it keeps its as-sized length and is listed as such.
- **(b) The route lengths set the need everywhere (recommended).** G2.0 and the allocation use the same need, as
  plan v2 already did for the cell part. The artefact (single 244 and 446 µm stubs) leaves the budgets too, which
  is what row 44 asks. 'Ours' budgets change as in the table, the step 6 reference budgets are superseded, and the
  plan's "budgets identical" test is replaced by "the need's wiring part uses the representative cells; G2.0 =
  rate × the need the allocation uses". It needs a dated note under PREREG item 6.
- **(a) G2.0 only.** G2.0 reports the representative-cell route, with the as-sized one as a second column. The
  allocation keeps the as-sized need, so budgets are identical and the plan's test holds. But the budgets keep the
  artefact, and G2.0 is no longer rate × the need the allocation uses.
- Either way: m > 1 (not in these two designs) is scaled as √m × the unit cell's sides, marked ASSUMPTION.

**Resolved 2026-11-01 19:18 CET (Imasha): `lp_floor_k` is (a), the literal definition**, done in step 6. There
was no separate answer on the closure, so it uses the 2 %, as the plan says. If it should stay at 10 %, say so: the
5T's G2.5 would then fail on gain (1.086 > 1.02). The question as it was asked:

**Was FEEDBACK NEEDED (Claude Code, 2026-11-01 19:05, Phase A step 6): how to define `lp_floor_k`.**
- PREREG item 5 says: "the `lp_floor` baseline also scored with the upper bound ours uses, KAPPA × need". Taken
  literally, that is the same LP (maximise the sum of budget/need, each budget at least its floor), capped at
  10 × need instead of at need.
- The plan's test expects `lp_floor_k` ≥ `lp_floor` element by element. An LP does not guarantee that: with more
  room it can move to a vertex that starves some elements to give others up to 10 × need.
  - 5T: it holds (21 of 21 elements; budget/need goes from 1.0 to 1.45–10).
  - **LOADBench: it fails.** 13 of 40 elements get less than under `lp_floor`, some down to 0 × need (e.g.
    `FirstStageYout1~out` 1.0 → 0.0). Measured on LOADBench's nominal problem rebuilt from its plan-v2 budgets
    file (`runs/tmp/lp_floor_k_probe.py`).
- **(a) Literal (recommended).** The same LP with ours' bounds, as PREREG item 5 is written. It is the clean
  max-sum counterpart to ours' max-min with identical bounds. The element-by-element test is replaced by "same
  bounds as ours; objective ≥ `lp_floor`'s". Its starving is then a result to report.
- **(b) Two phases.** `lp_floor` first, capped at need; then extra room up to 10 × need without lowering any
  element. It is never below `lp_floor` by construction, but it is a different method from the one PREREG item 5
  names, and would need a note there.
- Also, to confirm: the closure now uses the 2 % too (literal plan; effect on the 5T in *Step 6 so far*). The
  alternative keeps the closure at 10 %: budgets unchanged, but G2.5 then fails on the 5T's gain (1.086 > 1.02).

**Answered 2026-11-01 (Imasha, in Cowork):**

- D1: nominal only for now, not the middle 9.
- D2/D3: share of nominal margin, eta = 0.5, the same share for every spec.
- D9: Phase A only, on the 5T and LOADBench.
- D10: no LLM at run time.
- LOADBench: keep the PMOS bank sizes.

Still open, and deferred with the out-of-scope designs and phases:

- D4: LOADBench's specs stay ASSUMPTION.
- D5–D8.

**Was FEEDBACK NEEDED (Cowork, 2026-10-27 evening): Plan v3 decisions D1–D10.** Full reasoning and the per-circuit
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

- 2026-11-04 evening (Claude Code, branch `gui-tools`): **the local GUI** (edit a design as a copy, or make a new
  one from files; run the flow; simple report; no LLM), tested end to end on two 5T demos (`ota5t_gui_copy`
  S0–S7 PASS; `ota5t_gui_new` all stages ran). **iadc_ota** in the Tiny Tapeout tile: S0–S3 re-run, S4 PASS, S5
  waits for a decision on folding (FEEDBACK). Flow record rows 93–96, section 7.25. 192 tests; 32 goldens.
- 2026-11-04 afternoon (Claude Code): **the ttsky report, expanded** at Imasha's request: the schematics with the
  sub-circuits and every block marked in colour (xschem, from a scratch copy), every block numbered (B1–B33) and
  pictured, the layouts annotated, the tile's regions by its cell names, S1/S2's main nodes with their budgets
  and results, the exact S4/S5 algorithms and cost, who decides what (code / Imasha / LLM), the novelty status,
  the planned LLM integration, and every variant in an appendix. `scripts/report_figures.py`.
- 2026-11-04 afternoon (Claude Code): **the ttsky report** (`docs/ttsky25a_fd_report.md` and `.html`,
  `scripts/make_ttsky_report.py`, `scripts/report_layout_png.py`): the layouts, matching, post-layout results and
  the comparison with the hand-drawn tile, for any reader, every number read from `outputs/`. The tile's op-amp
  measured in its GDS: 156.8 × 218.0 µm. Imasha's matching answer recorded (no change).
- 2026-11-04 afternoon (Claude Code): **Phase 8.7**: independent review of Phase 8 (flow record row 92): S7's
  C-only fallback limited to `rc_extraction: false`, S5's symmetric flag only for mirror-image blocks, three latent
  fixes, G5.7 (info) for matched blocks' centring. All three designs re-run from S4: the 5T and LOADBench goldens
  match; ttsky's placements changed a little, conclusions hold (7.24). Walkthrough covers ttsky. 189 tests; 32
  goldens. Waiting for Imasha's commit.
- 2026-11-04 midday (Claude Code): **Phase 8, part 2**: `ttsky25a_fd` grid-routed, extracted (C only) and simulated
  (flow record 7.23, rows 85–91). S5: DRC 0, LVS match, inside the outline; S6 G6.1 PASS; S7 G7.1 PASS, G7.2 FAIL on
  GBW; the drawn → C-only GBW loss (−5.9 %) is below the hand layout's (−6.8 %). `flat_lvs` and G7.5 fixed;
  `flow.py` retries its summary write. 188 tests pass; 32 golden comparisons match. Waiting for Imasha's commit.
- 2026-11-04 morning (Claude Code): **Phase 8, part 1**: `ttsky25a_fd` S0–S3 re-run, S4 PASS, S5 placement inside the
  outline (flow record 7.22, rows 81–84); routing next. Waiting for Imasha's commit on `s5-ttsky`.
- 2026-11-04 morning (Claude Code): **Phase 8 plan** for `ttsky25a_fd` (`docs/plan_v5_ttsky25a.md`): the design's own
  hierarchy as macros, annealing inside a macro, a grid router, m-arrays, resistor blocks; who decides what. No code.
- 2026-11-04 morning (Claude Code): **plan v4 Phase 7 on `s4-s5`**: the MIM double count (without it LOADBench is
  within eta), an independent review's fixes, S4–S7 goldens, the S4–S7 walkthrough. Committed `a5b250de`.
- 2026-11-04 early morning (Claude Code): **plan v4 Phase 6 on `s4-s5`**: LOADBench through S4–S7. S4 and the
  top-level layout signed off; G5.4, G6.2 and G7.2 (GBW) fail; every spec met post-layout. Router, S6 and S7 fixes
  (rows 71–76); the 5T re-run keeps every verdict. Committed `6d0c6bb7`.
- 2026-11-03 late evening (Claude Code): **plan v4 Phase 5 on `s4-s5`**: S6 extraction against S2's budgets and S7
  post-layout SPICE on the 5T. The 5T runs S0–S7, all PASS; H4 holds, H5 mostly. Committed `27a075a6`.
- 2026-11-03 late evening (Claude Code): **plan v4 Phase 4 on `s4-s5`**: S5 routing on the 5T. Both placements are
  routed, with top-level DRC and LVS clean and S2's route rules met; S5 is a flow stage. Committed `3089366a`.
- 2026-11-03 late evening (Claude Code): **plan v4 Phase 3 on `s4-s5`**: S5 placement on the 5T (budget-aware against area-only; textbook stack found, half the wire-budget use); PREREG constants first. Committed `f26c136a`.
- 2026-11-03 late evening (Claude Code): **plan v4 Phase 2 on `s4-s5`**: S4 (blocks from S3's ringless cells, one
  guard ring each) built and signed off on the 5T; S4 is a flow stage. Committed `1e4d166f`.
- 2026-11-03 evening (Claude Code): **plan v4 Phase 1 on `s4-s5`**: S3's unit cells without guard rings (body labelled on the
  well, tap rules deferred to S4), re-run on both designs. Same verdicts, 37 % and 13 % less device area, specs
  unchanged; S3 goldens refreshed. Flow record 7.15, row 67. Committed `a3e9277e`.
- 2026-11-03 evening (Claude Code): **plan v4 Phase 0 on branch `s4-s5`**: freeze test for the S0–S2 outputs later
  stages read, `docs/plan_v4_S4_S7.md`, and PREREG's amendment of 2026-11-03 (gates, H4, H5, predictions), written
  before any S3 change or S4–S7 code. Waiting for Imasha's commit.
- 2026-11-03 morning (Claude Code): **after the merge into `main`**: the S3 option plot marks the options S3 may
  choose (row 65); the CRLF line endings written by the checkout are restored to LF and `.gitattributes` keeps LF
  (row 66); `flow status` shows the reports' own times; the walkthrough explains how to read each table and plot,
  and what it shows for each design. Committed and pushed as `1626d11b` on `main`. Details under *Supervisor
  review*, *After the merge*.
- 2026-11-02 evening (Claude Code): **Supervisor review, branch `s0-s3-review`**: phases 1–3 committed
  (`33e6277f` the `env.sh` fix, `bf67fd09` robustness, `214eb337` the clean runs), phase 4 the S0–S3 walkthrough
  (`58c4f207`: `docs/s0_s3_walkthrough.md` + HTML, `scripts/make_s0s3_walkthrough.py`), phase 5 (`b2448dd3`:
  README "For reviewers", flow record 7.14 and row 63, quiet launchers, the `CLAUDE.md` test line). Phase 6, the
  rehearsal from PowerShell (row 64: the launchers' output is unbuffered), is done and waiting for Imasha's commit
  and the merge into `main`. Details under *Supervisor review (s0-s3-review)*.
- 2026-11-02 (Claude Code): **Plan v3 Phase A, step 13**: flow record rows 40–61 and section 7.13, review D (9
  findings, all checked, 7.9), the post-hoc PREREG amendment for the at-bound tolerance, README. Phase A is
  complete; the claim is released. Committed `67b3b83d`, with the G2.8 follow-up (PVT checks back after review D 1).
- 2026-11-02 (Claude Code): **Plan v3 Phase A, step 12**: the 5T and LOADBench re-run (`after_v3a`), the G2.8
  tolerance fix (Imasha's answer (a)), goldens refreshed, `before_after.md` regenerated. Committed `14e97f7e`.
- 2026-11-02 (Claude Code): **Plan v3 Phase A, step 11**: the test pass before step 12, documentation only.
  Committed `2a9897c0`.
- 2026-11-02 (Claude Code): **Plan v3 Phase A, step 10**: LOADBench's hand model with the NMOS-mirror doublet,
  PREDICTED (patched, post hoc). Committed `9370baa7`.
- 2026-11-01 (Claude Code): **Plan v3 Phase A, steps 0–9, and the sky130A environment** (branch
  `plan-v3-phaseA`). Each change and its result is in the progress table under *Plan v3 Phase A*. All are
  committed.
- 2026-11-01 (Cowork): **Plan v3 Phase A planned** (no code, runs or outputs changed).
  - `docs/plan_v3_phaseA.md`: the decisions, Q1–Q4, steps 0–13, the predictions, the open issues per stage (for
    this version and for a new SPICE file), and how LLMs are used in each stage.
  - `docs/HANDOFF.md` rewritten for Phase A, with a new first message for Claude Code.
  - This file: the Phase A section, the decisions, and claims.
  - Progress-log entry.
  - The designer-review sections (LOADBench, iadc, TTSKY25a groupings) were added to the Claude Doc "Plan v3:
    circuit review pack and implementation plan". The `docs/plan_v3_review_pack.md` mirror predates them; the
    LOADBench part that Phase A needs is in the plan.
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
