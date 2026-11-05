# Handoff: continuing the layout flow on another PC or with another Claude account (2026-11-05)

Written by Claude Code on 2026-11-05, when Imasha put active work on hold. The previous handoffs (Cowork,
2026-10-27 and 2026-11-01) are in git history. Read this file with:
- `CLAUDE.md`: the rules (Imasha's, verbatim), the environment and how agents work here;
- `docs/STATUS.md`: what is running, recent changes, open questions;
- `README.md`: what the flow is, its results and how to run it.

## 1. Where things stand

**The flow.** Stages S0–S7 are built and run end to end on four designs:
- `example_ota_5t`;
- `loadbench_miller`;
- `ttsky25a_fd` (Imasha's taped-out op-amp);
- `iadc_ota` (the OTA of an incremental ADC, in a Tiny Tapeout tile).

Every layout is DRC-clean and LVS-matched. After layout, all specs are met except iadc's GBW, whose spec is an
ASSUMPTION. S8 (diagnosis and repair) and S9 (selection) are planned, not built. A local GUI (`gui/gui.ps1`) and
per-design reports exist. No LLM is used by the flow.

**Branches** (Imasha commits and pushes with GitHub Desktop):
- `main`: S0–S3 as reviewed;
- `s4-s5`, `s5-ttsky`, `gui-tools`: plan v4 and its phases. `gui-tools` was committed with the reviewer pack
  (`d6958ca61`);
- **`rules-v2` (current):** layout rule set v2, phases 1–2.
  - Committed by Imasha after this handoff was written, except the `ttsky25a_fd_v2` outputs, which were still being
    written.
  - Check `git log -3`.

**Layout rule set v2** (`docs/rules_v2/ruleset_v2.md`, PREREG amendment 2026-11-05, flow record 7.26, rows 101–106):
- opt-in per design with `ruleset: v2` in `inputs/<d>/layout.yaml`;
- phases 1 and 2 built:
  - DRC × 1.1 spacing;
  - no wire over devices;
  - channels widened until routing succeeds;
  - Imasha's drawn blocks with the designer's dummies;
  - 2-D common centroid and cross-quad;
  - paper screening;
- result on `iadc_ota_v2`: 35–45 % less area than v1, not yet the 1.3 × hand-layout target;
- **phase 3 is on hold: `docs/rules_v2/phase3_plan.md`**;
- phase 3 step 1 (flat packing) was run on 2026-11-06:
  - area-only: 13,983 µm² (1.05 × the hand layout), but with 8 nwell.2a DRC errors, now fixed in the code (row 107). **Re-run S5–S7 first.**
  - budget-aware: 29,442 µm², DRC-clean but worse than with macros.
- The outputs under `outputs/S5`–`S7/iadc_ota_v2` are this flat run. The phase-2 result is in commit `6c92fdee1`.

**Tests:** 211 unit tests plus 36 golden comparisons (`.\flow.ps1 test`); all pass. The goldens prove the finished
designs (v1) unchanged.

## 2. What may still be running

When this was written (18:50 CET 2026-11-05), the container `layout-s0s3` was running three things:
1. **`ttsky25a_fd_v2` S0–S3** (`runs/logs/gui_ttsky25a_fd_v2_S0S3.log`). S0 passed.
2. **`scripts/finish_ttsky_v2.sh`.** It runs the stages still missing up to S7, then regenerates three things:
   `docs/reports/ttsky25a_fd_v2_report.html`, the README pictures, and `docs/progress_report.*`. It writes
   `runs/logs/finish_ttsky_v2.done` at the end.
3. **The phase 3 packing dry run** (`runs/logs/p3_dry.log`; it changes no file the flow reads).

**Imasha stopped the ttsky run on 2026-11-06 (S0 passed, S1 interrupted) and put the work on hold for the week.** It needed
about 4 hours more. The finish script is resumable: it starts at the first stage of `ttsky25a_fd_v2` without a
report. So, on the next start:

```powershell
docker start layout-s0s3
docker exec -d layout-s0s3 bash -lc "bash /foss/designs/scripts/finish_ttsky_v2.sh"
```

That is about 3.5 hours from S1, less if S1–S2 had finished. Wait for `runs/logs/finish_ttsky_v2.done`.

**Then:**
- run `.\flow.ps1 status ttsky25a_fd_v2`;
- if S5 failed, read `runs/logs/flow/ttsky25a_fd_v2/S5_run.log`. Flow record rows 103–106 show the kinds of failure
  v2 met on iadc and how each was found.
- The README's ttsky text still describes v1 only. Add a sentence and a row for v2 from
  `docs/progress_report.md` section 5, which fills itself in.
- Commit the `ttsky25a_fd_v2` outputs.

## 3. Setting up on another PC

1. **Docker Desktop**, about 20 GB free. Then `git clone` the repository and check out `rules-v2`.
2. **The image:** `docker pull hpretl/iic-osic-tools:2026.10`. It holds Magic, Netgen, ngspice, xschem, KLayout,
   kpex, SKY130 and every Python package of `requirements.txt`, so nothing else is installed.
3. **Run without a named container** (tested): `.\flow.ps1 <command>` starts a throwaway container from the image
   with the repository mounted at `/foss/designs`.
   - `.\flow.ps1 test` should give 211 passed and the 36 goldens OK.
4. **A named container** for long or detached runs, as used on Imasha's PC. **ASSUMPTION:** this exact command was
   not run on another PC:

   ```powershell
   docker run -d --name layout-s0s3 -v "${PWD}:/foss/designs" -w /foss/designs hpretl/iic-osic-tools:2026.10 --skip sleep infinity
   $env:FLOW_CONTAINER="layout-s0s3"; .\flow.ps1 status all
   ```

5. **Always `source scripts/env.sh`** inside the container before running Python. It switches the image from IHP to
   sky130A. `flow.ps1`, `flow` and the GUI do it for you.

## 4. Conventions that save time

- **Python runs in the container only**, never on the host. On Windows, `python3` on the host is a Store stub that
  can hang a shell.
- **From Git Bash:** `MSYS_NO_PATHCONV=1 docker exec -e IIC_OSIC_TOOLS_QUIET=1 layout-s0s3 bash -lc "cd /foss/designs && source scripts/env.sh && ..."`.
- **Write retries.** The Windows-mounted repository sometimes refuses a write (Errno 22). Write with a retry, as
  `src/common/tools.write_text` does.
- **Escapes.** When writing Markdown from Python, beware `"\f"` (a form feed) in strings such as `.\flow.ps1`. It
  broke the README once (2026-11-05).
- **Long runs:** detach them (`docker exec -d ... ; echo $? > <log>.exit`) and wait on the `.exit` file, never on a
  PID; the container does not reap processes.
  - Don't edit `src/` while a flow run is going: each stage loads the code when it starts.
- **Every meaningful step:**
  - an entry in `docs/progress_log.md`;
  - a row in the flow record's journey table for any bug: edit `docs/flow_record_section7_draft.md`, then
    `python3 scripts/merge_section7.py`;
  - STATUS kept current;
  - README updated when running something changes.
- **PREREG.md:** change hypotheses, thresholds or search settings only with a dated amendment written before the
  run.
- **Never** invent a value (mark ASSUMPTION or ask Imasha), never touch `circuits/*/source|upstream` (hash-frozen),
  never commit (Imasha does), never connect to an outside service without the supervisor's permission.

## 5. What to do next (in order)

1. Re-run `iadc_ota_v2` from S5 with the n-well fix, then regenerate its report and the README pictures
   (`make_design_report.py iadc_ota_v2`, `make_readme_figures.py`) and update the README's phase 3
   paragraph. The command is in `docs/rules_v2/phase3_plan.md`, step 1.
2. Resume ttsky (section 2), then add its result to the README.
3. Phase 3 of rule set v2 (`docs/rules_v2/phase3_plan.md`):
   - macro packing;
   - channels only where needed;
   - shared ring edges and the outer ring;
   - the per-net look at wiring loss.
4. The LLM step (planned, measured against the rule-only flow): the Claude CLI, once the supervisor agrees.
   `docs/progress_report.md` section 8 has the plan, pros and cons.
5. S8 and S9.

## 6. Open questions for Imasha (also in `docs/STATUS.md`)

- iadc's GBW spec (188.9 MHz, an ASSUMPTION) and its other ASSUMPTIONs.
- R+C extraction for ttsky.
- Whether to make the opt-in fixes the default for the finished designs: `pin_origin: bbox`, the shelf start, and
  v2's latent-v1 fixes (rows 101, 106).
- A drawn hierarchy for ttsky under v2.
