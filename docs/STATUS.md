# STATUS: live handoff between Claude Code, Cowork and Imasha

Read this file first and update it when you start or stop work (see `CLAUDE.md`, "Working together"). Times are given in container time (CET).

**Last updated:** 2026-10-27 01:10 Sri Lanka time (2026-10-26 20:36 CET in the container), by Cowork.

## Running (container `layout-s0s3`)

**Nothing is running.** All plan-v2 runs were stopped cleanly at 20:35 CET for the night (`scripts/plan_v2_stop.sh`).
The PC goes off; from 2026-10-27 the work continues with Claude Code (`docs/HANDOFF.md`).

- **Next:** start `scripts/plan_v2_resume.sh` (see its header). It skips the finished steps marked in
  `runs/state/plan_v2/`.
- **Stopped mid-way, redone by the resume script:**
  - iadc_ota 'before' S3 (v1);
  - ttsky25a_fd 'before' S2 (v1; its S1 finished at 19:50 with all gates passing, G1.4 included);
  - loadbench_miller 'after' S2 (its PVT points finished at 20:35 and are kept);
  - queue_v2h and queue_v2i (replaced by the resume script).
- **Finished:**
  - 5T and ota5t_stress before and after;
  - loadbench before;
  - iadc hand layout C-only and R+C;
  - TTSKY tile C-only.

## Claims (who is editing what)

| Who | Files / designs | Since |
|---|---|---|
| Cowork | slides and the claude.ai project doc 13 only (the record and the scripts are released to Claude Code) | 2026-10-27 |
| Claude Code | from 2026-10-27: the runs (`scripts/plan_v2_resume.sh`) and the write-up, per `docs/HANDOFF.md` | 2026-10-27 |

## Pending tasks (plan v2)

1. Finish the runs: `scripts/plan_v2_resume.sh` (before/after for all designs, no-PVT ablation, eta 0.9, TTSKY R+C, golden snapshots, report).
2. Fill flow record 7.5 (before/after table) and 7.6 (baseline table) with the final numbers.
3. Compare G2.0's prediction with the hand layouts' drawn → PEX loss, for TTSKY and iadc, using the after runs (iadc 'before' done, flow record 7.8).
4. R+C extraction of the TTSKY25a tile (in the resume script; iadc's is done and clean: `reference_layout_rc100s.json`).
5. Golden snapshots for v2 (in the resume script).
6. Slides: v2-beforeafter, v2-baselines, v2-next and the groups slide.
7. Claude.ai project doc 13.
8. Independent review at the milestone (queue done and write-up done).
9. Imasha commits after each step (GitHub Desktop).

## Open questions for Imasha

- **iadc G1.1** (not blocking): 21 functional devices sit below vdsat at the operating point: 15 MOS-resistor stacks with the gate at cm, plus some current sources. Is that the design intent? Until answered, it is reported as a FAIL, with that explanation.
- **TTSKY paper numbers** (information only): the paper's post-layout 2.3 MHz / 52° is not reproduced by the tile's PEX, even at the bench conditions (ff, 20 °C, MIM MF=100). How was that run set up?

## Recent results

- iadc hand layout R+C (`rc100s`, `--map-shorted`): clean. Gain 57.24 dB, GBW 153.7 MHz, PM 78.7 deg; wire R costs GBW 2.5 MHz and PM 2.5 deg beyond C, and moves the output CM by -68 mV.
- 5T after and ota5t_stress after: see `docs/before_after.md` (after the report step) and flow record 7.5 and 7.6.

## Recent changes

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
