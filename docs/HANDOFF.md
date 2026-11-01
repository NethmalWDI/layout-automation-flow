# Handoff: Plan v3 Phase A with Claude Code (from 2026-11-01)

Written by Cowork on 2026-11-01. Read it together with:

- `CLAUDE.md`: the rules, the environment and how the agents work together;
- `docs/STATUS.md`: what is running and what is open;
- **`docs/plan_v3_phaseA.md`**: the step-by-step plan Claude Code carries out.

The previous handoff (plan-v2 runs, 2026-10-27) is in git history.

## 1. Where things stand

- **Nothing is running.**
  - Plan v2 is finished, written up (flow record section 7) and reviewed (review C).
  - The Plan v3 review pack is done (`docs/plan_v3_review_pack.md`, Claude Doc "Plan v3: circuit review pack and
    implementation plan").
  - The designers' grouping comments are recorded in that doc (2026-11-01).
- **Imasha's decisions (2026-11-01):**
  - Phase A fixes only, on `example_ota_5t` and `loadbench_miller`.
  - Budgets at the nominal corner only; the PVT points are reported, not gated.
  - Allowance = eta × nominal margin, with eta = 0.5.
  - LOADBench's PMOS bank keeps its sizes.
  - Section 1 of the plan has the full list.
- **The other three designs are frozen for now:** `ota5t_stress`, `iadc_ota` and `ttsky25a_fd`.

## 2. One-time setup (about 5 min)

Claude Code is the **Code** tab of the Claude desktop app, next to Home. Nothing has to be installed
(https://code.claude.com/docs/en/desktop-quickstart).

1. **Before you start:**
   - Commit the current state in GitHub Desktop.
   - If you agree with question Q1 of the plan, tag that commit `prereg-v1` (History → right-click the commit →
     Create Tag).
   - Create the branch `plan-v3-phaseA` (Q2).
2. **Start Docker.** Start Docker Desktop, then run `docker start layout-s0s3`.
3. **Open the repo in the Code tab.** Under the prompt box:
   - environment: **Local**;
   - folder: **Open folder…** → `C:\Users\suind\Documents\GitHub\layout-automation-s0-s3`.
4. **Permission mode.** Use **Manual** or **Accept edits**, and approve `docker exec` commands as they come.
5. **Power.** Long runs (plan step 12) need the PC awake. Set Windows to never sleep while plugged in (row 39).
6. **Paste this as your first message:**

   > Read CLAUDE.md, docs/STATUS.md, docs/HANDOFF.md and docs/plan_v3_phaseA.md. Do step 0 of the plan: check
   > the container and git (read-only), then ask me questions Q1–Q4 in one message and wait for my answers. After
   > that, work through the plan one step at a time. At the end of each step, run its tests, update
   > docs/STATUS.md, tell me "ready to commit" with the suggested message, and wait for me. Do not run git
   > commands that change anything; I commit with GitHub Desktop. Do not install anything. If a value is
   > missing or a prediction in section 4 fails, stop and ask me.

## 3. Daily routine

**Start of day**

1. Start Docker Desktop, then run `docker start layout-s0s3`.
2. Open Claude Code in the repo and ask: "Read docs/STATUS.md and docs/plan_v3_phaseA.md, and continue from the
   next step."

**While working**

- Runs (plan step 12) are detached inside the container, so closing Claude Code does not stop them. Switching
  the PC off or stopping Docker does.
- Commit after each step, when Claude Code says "ready to commit".

**Before switching the PC off**

1. Ask Claude Code: "stop any running job cleanly and update STATUS.md".
2. Commit in GitHub Desktop.
3. Switch off.

## 4. What Claude Code has and does not have

| | Claude Code (Code tab, Local, on your PC) | Cowork (Home tab, runs in the cloud) |
|---|---|---|
| Repo files and container | direct: file edits, `docker exec` | through the desktop app |
| Works while you are away | only while the PC and the app are on | yes, but it can't reach the container when the PC is off |
| claude.ai project docs, Claude Docs, slides | no (copies in `docs/context/project_docs/`, and the review pack in `docs/plan_v3_review_pack.md`) | yes |
| Git | only if you allow it (rule: you commit) | no |

Both read `CLAUDE.md` and `docs/STATUS.md`. If you use both on the same day:

- claim files in STATUS.md before editing them;
- don't let both agents start runs in the container.

## 5. After Phase A

Bring the results back to Cowork when you want:

- the write-up in the Claude Doc;
- project doc 15;
- the slides.

Phases B–E, the other three designs and S4 come after that, and you decide the order.
