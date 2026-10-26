# Handoff: plan v2 continues with Claude Code (from 2026-10-27)

Written by Cowork on 2026-10-27 at 01:10 (Sri Lanka time), just before the PC was switched off for the night.
Read it together with `CLAUDE.md` (the rules, the environment and how the agents work together) and
`docs/STATUS.md` (what is running and what is open).

## 1. Where things stand tonight

All runs were stopped cleanly at about 01:15. Nothing is lost: whatever was half-done is re-run by
`scripts/plan_v2_resume.sh`. That script skips every step that already finished; the list of finished steps is
in `runs/state/plan_v2/`.

| Design | before (v1) | after (v2) | Notes |
|---|---|---|---|
| example_ota_5t | done | done | baselines re-scored after review B |
| ota5t_stress | done | done | G2.7 FAIL in S2 (expected: does not fit at eta 0.9) |
| loadbench_miller | done | to do | |
| iadc_ota | S0–S2 done, S3 to redo | to do | hand layout: C-only and R+C runs done (flow record 7.8) |
| ttsky25a_fd | S1 done, S2–S3 to redo | to do | hand tile: C-only runs done; R+C to do |

Also still to do:

- the no-PVT ablation of the two 5T designs;
- S2 at eta = 0.9 for every design (PREREG's headline eta);
- the golden snapshots of the v2 outputs;
- the before/after report.

`plan_v2_resume.sh` runs all of these, in about 5–6 hours.

## 2. One-time setup (about 5 min)

Claude Code is already inside the Claude desktop app: it is the **Code** tab at the top of the sidebar, next to
Home. Nothing has to be installed (https://code.claude.com/docs/en/desktop-quickstart).

1. **Start Docker.** Start Docker Desktop, then run `docker start layout-s0s3` in a terminal (Docker Desktop's
   container list works too).
2. **Open the repo in the Code tab.** In the Claude desktop app, click **Code**. Under the prompt box:
   - environment selector: **Local** (top entry);
   - folder: **Open folder…** → `C:\Users\suind\Documents\GitHub\layout-automation-s0-s3`.

   Claude Code reads `CLAUDE.md` from that folder.
3. **Permission mode:** **Manual** (it asks before every edit and command) or **Accept edits** (edits go
   through, commands still ask). Approve `docker exec` commands as they come.
4. **Paste this as your first message:**

   > Read CLAUDE.md, docs/STATUS.md and docs/HANDOFF.md. Check the container (`docker exec layout-s0s3 pgrep
   > -af '^python3'`) and `runs/state/plan_v2/`. Then start the remaining plan-v2 runs with
   > scripts/plan_v2_resume.sh exactly as its header says, record the job in docs/STATUS.md, and tell me
   > what will run and how long it takes. Do not run git; I commit with GitHub Desktop.

The command-line version (`claude` in a terminal, https://code.claude.com/docs/en/setup) does the same; you
only need it if you prefer a terminal.

## 3. Daily routine

**Start of day**

1. Start Docker Desktop, then run `docker start layout-s0s3`.
2. Open Claude Code in the repo. Ask: "Read docs/STATUS.md and continue."
3. If runs are pending, Claude Code restarts `scripts/plan_v2_resume.sh`. It only does what is left.

**While working**

- The runs are detached inside the container, so closing Claude Code does not stop them. Only switching the
  PC off, or stopping Docker, stops them.
- Claude Code only looks at them while the app is open and you ask. The desktop app can also run scheduled
  tasks (for example "every hour: check the runs, update STATUS.md") while the PC and the app are on.
- Ask it now and then: "check the runs and update STATUS.md".

**Before switching the PC off**

1. Tell Claude Code (Code tab): "stop the plan-v2 runs cleanly and update STATUS.md". What it does:
   - finds the job PIDs with `pgrep -af 'plan_v2|src\.|reference_layout'`;
   - kills the lanes' bash processes first, then their python and ngspice children;
   - leaves the `.done` markers as they are; the step that was interrupted runs again next time.
2. Commit in GitHub Desktop.
3. Switch off.

**After each milestone** (all runs done; then after the write-up)

- Ask Claude Code for an independent review with a sub-agent:

  > Start an independent review agent that has not seen our conclusions. Give it the code (src/,
  > scripts/), docs/before_after.md and flow record section 7, and ask it to find wrong claims, unfair
  > baseline scoring and bugs. Record its findings and what we did with each in flow record 7.9.

## 4. Remaining work, in order

1. **Finish the runs:** `scripts/plan_v2_resume.sh`, about 5–6 h. Fix a crash if one happens. Every fix gets a
   row in the journey table (flow record 7.1) with these columns:
   - what went wrong;
   - how it was found;
   - what changed;
   - the effect.
2. **Write up the results** in `docs/flow_record_section7_draft.md`, then run `python3 scripts/merge_section7.py`.
   - 7.5 before/after: loadbench, iadc, ttsky. 5T and stress are already written.
   - 7.6 baselines: the five rules on every design, at the design's own eta and at eta 0.9 (H1, H1b, H1c of
     `PREREG.md`).
   - 7.7 and 7.8 hand layouts: G2.0 from the *after* runs against drawn → PEX. Use the table at the end of each
     design in `docs/before_after.md`. The TTSKY tile also gets its R+C result.
   - 7.10 limitations: update.
3. **Independent review** (milestone): see "After each milestone" in section 3.
4. **Golden tests:** `./flow test` must pass on the new snapshots; CI runs it on every push.
5. **Slides and the claude.ai project doc 13.** Claude Code cannot publish to claude.ai. Either open Cowork
   (the Claude desktop app) for these two items, or have Claude Code write the slide text into
   `docs/slides_v2.md` and publish it from Cowork later.
6. **Next research step (plan v2, item 6):** restructure S3 into a unit library and S4a block planning
   (`docs/context/project_docs/12_flow_v2_decisions.md`, "S3/S4: restructure").

## 5. What Claude Code has and does not have

| | Claude Code (Code tab, Local, on your PC) | Cowork (Home tab, runs in the cloud) |
|---|---|---|
| Repo files and container | direct: file edits, `docker exec` | through the desktop app |
| Works while you are away | only while the PC and the app are on | yes, with scheduled check-ins, but it can't reach the container when the PC is off |
| Updates to your phone | no | yes |
| claude.ai project docs, slides | no (copies of the docs are in `docs/context/project_docs/`) | yes |
| Git | only if you allow it (rule: you commit) | no |

Both read `CLAUDE.md` and `docs/STATUS.md`. If you use both on the same day:

- claim files in STATUS.md before editing them;
- don't let both agents start runs in the container.

## 6. Open questions for you (not blocking)

- **iadc G1.1:** 21 functional devices are below vdsat. 15 of them are MOS-resistor stacks with the gate at cm;
  the rest are current sources. Is that intended by the iadc designers?
- **TTSKY25a paper:** how was the post-layout run (2.3 MHz / 52 deg) set up? Which netlist, which extraction,
  and was wire resistance included?
