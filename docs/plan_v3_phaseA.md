# Plan v3, Phase A: implementation plan for Claude Code (5T OTA and LOADBench only)

Written by Cowork on 2026-11-01 for Claude Code, which will carry it out on Imasha's laptop. Read it after
`CLAUDE.md`, `docs/STATUS.md` and `docs/HANDOFF.md`. The background is in `docs/plan_v3_review_pack.md` (the
review pack, Phase A table) and in the flow record, section 7.1 (journey rows 40–50).

Contents:

1. Scope and the decisions in force
2. Questions to ask Imasha before the first edit
3. Order of work (steps 0–13), each with files, change, test and "done when"
4. Expected effect on the two designs (written before the runs)
5. Open issues per stage: in this version, and for a new SPICE file
6. How LLMs are used in each stage
7. Out of scope

---

## 1. Scope and the decisions in force

**Designs:** `example_ota_5t` and `loadbench_miller` only. `ota5t_stress`, `iadc_ota` and `ttsky25a_fd` are
frozen for now. Their outputs, snapshots and golden files stay as they are, and they must keep running: no change
may break them (the unit tests and `./flow test` check this).

**Work:** Phase A of Plan v3 only, which means cleaning the evidence. Phases B–E, S4 and every LLM role are out of
scope.

Imasha's decisions (2026-11-01, answered in Cowork):

| # | Decision | What it means in the code |
|---|---|---|
| D-a | Scope: Phase A fixes only, on the 5T and LOADBench | review-pack items A1–A6, plus rows 42–44 and the nominal-only budgets |
| D-b | Corners: **nominal only for now** (replaces D1's "middle 9" recommendation) | S2 budgets use the nominal constraints only. S0 still simulates the 45 PVT points, and S2 reports what the final budgets use at each of them (first order, **reported, not gated**) |
| D-c | Allowance: **share of margin, eta = 0.5** | allowance = 0.5 × (achieved − spec) for each spec at nominal. This is the current S2 rule and default (`ETA_DEFAULT`), so the package needs no `eta` key. The eta sweep (0.3–1.0) stays as a report |
| D-d | LOADBench PMOS bank: **keep the sizes** | P2, P8 and P5 stay at W = 37.3, 90.63 and 887.03 µm (L = 0.74 µm), ratio 1 : 2.43 : 23.8. No netlist change |
| D-e | Designer grouping (Imasha's review comments, 2026-11-01) | LOADBench: P2, P8 and P5 form one PMOS mirror bank (gate `ibias`, source `sourcePmos`). The common-source stage is a functional group: N3 with P5 as its load, and no N3–P5 matching. Floorplan rows run from VDD to VSS: PMOS sources, then the diff pair, then the NMOS mirror and the CS stage. The rows are recorded for S4 and not used in S0–S3 |
| D-f | LLM | none at run time (D10, "defer until a deterministic S4 works"). See section 6 |

**Unchanged rules:**

- S3's relaxed-type fallback stays `least-bad`, the default since the 2026-10-27 PREREG amendment.
- The nf grid, the representative-cell floors and the frozen constants stay as they are. Phase A changes only the
  constants named in step 1.

**No new software.** Every step uses the pinned container image and `requirements.txt`. If a step seems to need a
package, stop and ask Imasha.

---

## 2. Questions for Imasha before the first edit (answered 2026-11-01)

**Answered.** Imasha accepted every recommended answer below (2026-11-01, in Cowork). Do not ask these again.
Before step 1, check that she has done her part, with read-only git commands:

- the tag `prereg-v1` exists (`git tag`);
- the current branch is `plan-v3-phaseA` (`git branch --show-current`).

If either is missing, stop and remind her.

| # | Question | Recommended |
|---|---|---|
| Q1 | `PREREG.md` is still headed "DRAFT, not yet frozen", and no `prereg-v1` git tag exists (checked 2026-11-01). Should she tag the current commit as `prereg-v1` in GitHub Desktop before Phase A, so that step 1's amendment is a dated change on top of it? | Yes: tag first (History → right-click the commit → Create Tag), then step 1 |
| Q2 | Work on a branch? | Yes: she creates `plan-v3-phaseA` in GitHub Desktop and commits there after each step |
| Q3 | One tolerance everywhere (step 6). 0.02 of the allowed use (eta × margin) is the PREREG "unsafe" threshold. G2.5 goes from 10 % to 2 %, and S3's 1 % of margin becomes 0.02 × eta × margin, which is the same 1 % at eta 0.5. More G2.5 checks may then fail | 0.02. Keep the 10 % figure only as a reported column ("within first-order model error"), not as a gate |
| Q4 | After step 12, replace the golden snapshots of these two designs with the Phase A outputs? The old snapshots stay in git history | Yes |

These are defaults; change them only if Imasha says so:

- **Designer groups.** They go in a new file, `inputs/loadbench_miller/designer_groups.yaml`, outside the
  hash-frozen folders. S0 reads it after the upstream blocks (step 5).
- **Testbenches.** The frozen testbenches of the two designs are not changed. Their 1 Hz phase error is
  negligible: with the dominant pole at GBW / A0, about 2.7 MHz for the 5T and 29 kHz for LOADBench, it is
  about 2e-5° and 2e-3°. Step 7 measures it and records it. The PM fix goes into `src/s1/linear.py` and into the template
  in `scripts/benchlib.py`, which only new designs use.
- **Saturation tolerance.** For a device already below vdsat in the schematic, S3 allows a further drop of the
  shared tolerance × |its schematic value of vds − vdsat|. This is an ASSUMPTION, stated in the step 1 amendment.

---

## 3. Order of work

Each step ends with these four actions:

- run the step's tests;
- update `docs/STATUS.md`;
- tell Imasha "ready to commit", with the suggested message;
- wait for her, because she commits.

Times are estimates.

Run every command inside the container:

```powershell
docker exec layout-s0s3 bash -lc "cd /foss/designs && source scripts/env.sh && <command>"
```

### Step 0: setup and claim (15 min)

1. Read `CLAUDE.md`, `docs/STATUS.md`, `docs/HANDOFF.md` and this file.
2. Check the container. Run `docker ps`, then `docker exec layout-s0s3 pgrep -af '^python3'`, which should show
   nothing running.
3. Check git, read-only:
   - `git log --oneline -5` should start at Imasha's latest commit, which is at or after `6c0d387a`;
   - make sure there is no `.git/index.lock`.
4. Q1–Q4 are answered (section 2). Check the tag `prereg-v1` and the branch `plan-v3-phaseA`; if either is missing, stop and tell Imasha.
5. Claim the work in STATUS.md, under *Claims*: "Claude Code: Plan v3 Phase A, `src/`, `scripts/benchlib.py`,
   `scripts/compare_before_after.py`, `inputs/example_ota_5t/`, `inputs/loadbench_miller/`,
   `outputs/*/example_ota_5t/`, `outputs/*/loadbench_miller/`, `PREREG.md`, `tests/`, since <date>".
6. Baseline test run, with nothing changed yet: `python3 -m pytest -q tests/` and `./flow test`. Record the
   result. Any failure that existed before Phase A must be known before the work starts.

### Step 1: PREREG amendment, before any code change (30 min)

- **Why.** Phase A changes rules and constants. The pre-registration says these changes are dated amendments,
  written before the runs they affect.
- **File.** `PREREG.md`, *Amendments*: one entry, "2026-11-0x, Plan v3 Phase A (5T and LOADBench)". It lists:
  1. Budgets use nominal constraints only. The 45 PVT points are reported at the final budgets, not gated (D-b).
  2. eta = 0.5, share of nominal margin (D-c). The eta sweep is reported.
  3. One tolerance, `TOL_USE` (Q3), used by G2.5, `outcome()` and S3.
  4. S3 saturation do-no-harm for devices below vdsat in the schematic (step 4; the ASSUMPTION above).
  5. The `lp_floor` baseline is also scored with the upper bound ours uses (KAPPA × need) as `lp_floor_k`. The
     plan-v2 `lp_floor` (capped at need) is kept.
  6. G2.0's route part uses the representative cells (step 8).
  7. The PM reference phase is rounded to the nearest 180° (step 7).
  8. Designer groups (D-e) and the mirror-bank rule (step 5).
  9. The predictions of section 4 of this plan, copied in as written, before the runs.
- **Done when.** The amendment is in, and Imasha has read it. Suggested commit message: `PREREG: Plan v3 Phase A
  amendment (nominal budgets, eta 0.5, one tolerance)`.

### Step 2: run hygiene, crash vs FAIL and stale files (A2; rows 40 and 43; 1 h)

**Why.** In plan v2 a crashed S2 run was snapped as if it had finished, because a crash and a gate FAIL both exit
with code 1. Variant runs also reused the S2 folder, so old files stayed behind.

**Files and changes:**

| File | Change |
|---|---|
| `src/s0/ingest.py`, `src/s0/pcell_binding.py`, `src/s0/pvt.py`, `src/s1/run.py`, `src/s2/run.py`, `src/s3/run.py` | A gate FAIL returns a new constant `EXIT_GATE_FAIL = 3` (one shared definition, e.g. `src/common.py` or `src/flow_codes.py`). PASS stays 0. A crash stays 1 (Python's own exit code for an uncaught exception) |
| `src/flow.py` (`run_stage`, lines ~104–135) | Status from the exit codes: 0 → PASS, 3 → FAIL, anything else → ERROR, together with the existing fresh-report check |
| `src/s2/run.py` (start of `main`) | Before writing anything, move the old `outputs/S2/<d>/` to `outputs/S2/<d>.prev/`, replacing any earlier `.prev`, then start from an empty folder. Every S2 output carries the same `run_id` (ISO time + 8 hex characters) and `eta` |
| `src/s3/run.py` | The same for S3's report files. Keep the cell cache, which S3 reuses on purpose: find where it lives and leave it alone |
| `scripts/compare_before_after.py` (`snap`, line 72) | Refuse to snap when `budgets.json`, `s2_report.json` and `baselines.json` disagree on `run_id` or `eta`, or when any of them is older than the stage's start time in `flow_summary.json`. Print what disagrees |

Leave the `scripts/plan_v2_*.sh` scripts as they are. They are plan-v2 records, and Phase A does not use them.

**Tests** (new, in `tests/test_v2.py` or a new `tests/test_phaseA.py`):

- a stage that raises returns 1 and `flow` reports ERROR;
- a gate FAIL returns 3 and `flow` reports FAIL;
- `snap` refuses a folder with mixed `run_id`s;
- S2 leaves no file from an earlier run.

**Done when:**

- the tests pass;
- `./flow run example_ota_5t --stage S2` gives the same budgets as before, with `run_id` in every file.

Suggested commit message: `Phase A step 2: exit code 3 for gate FAIL, S2/S3 clean output folders, snapshot
identity check`.

### Step 3: nominal-only budgets, PVT reported (D-b; row 42 in part; 1.5 h)

**Why.** This is Imasha's decision D-b. It also removes the plan-v2 artefact where tiny PVT margins bound every
design (STATUS 1h).

**Files and changes:**

- `inputs/example_ota_5t/package.yaml` and `inputs/loadbench_miller/package.yaml`: add
  `budget_corners: nominal`. The other designs have no key and keep the plan-v2 behaviour (`all`).
- `src/s2/run.py`, around line 466, where the PVT constraints are built:
  - With `budget_corners: nominal`, still call `S2PVT.constraints(...)`, but keep its constraints out of
    `constraints`, the list that allocation uses.
  - After allocation, score the final budgets on them: use `B.check(x, pvt_constraints)` or `baselines.score`.
  - Report the result in `G2.9_pvt_constraints (info)`. For each PVT point and spec, give the use as a fraction of
    eta × that point's margin, the worst point, and the points where the spec was not met before layout. The
    pass value stays `None` (info).
- `--no-pvt` keeps its present meaning: no PVT at all. The v1 variant and the plan-v2 ablation use it.
- Write the budget corner set into `budgets.json` and `s2_report.json` (`"budget_corners": "nominal"`).

**Tests:**

- With `budget_corners: nominal`, the allocation's constraint list holds nominal checks only.
- G2.9 lists all 45 points.
- **Regression check:**
  1. Run 5T S2 with `budget_corners: nominal`.
  2. Compare it with the `after_nopvt` snapshot (`outputs/compare/example_ota_5t/after_nopvt.json`, S2 part).
     That run used the same nominal constraints, through `--no-pvt`. These must match:
     - `t_round1` = 3.4011, `n_budgeted` = 21, `starved` = 0, `min_ratio_to_need` = 3.2310, all within 1e-6
       relative;
     - `expected_use_fraction` must match too;
     - `verify` (the SPICE uses per check) within 1e-3.
  3. The snapshot has no per-element budgets, so also save this run's `budgets.json` as the reference for
     steps 4–10.
  4. If anything differs, stop and find out why before going on.

**Done when:** the tests pass; G2.9 shows the PVT use table for the 5T.

Suggested commit message: `Phase A step 3: nominal-only budgets with PVT use reported (budget_corners)`.

### Step 4: S3 saturation do-no-harm (A1; row 41; 45 min)

**Why.** For a device already below vdsat in the schematic, `mg_of(k)` returns a negative margin. The test
`u <= allowance + TOL × margin` then fails for every option, and the least-bad slack changes sign.

**Files and changes:** `src/s3/run.py`:

- `mg_of` (~line 194);
- the `ok` and `slack_frac_of_margin` lines (~217–218);
- G3.3's `within` (search `within`);
- the least-bad slack (~256).

For a `sat_` key whose schematic value is ≤ 0:

- the check becomes "do no harm": `ok = u <= TOL_USE × |base|`;
- the slack is computed against |base|;
- the check is marked `"rule": "do-no-harm (below vdsat in the schematic)"`.

Saturated devices keep today's rule.

**Tests:**

- A unit test with a fake base `sat_V` of −0.05 V. An option that changes it by +1 mV of harm fails. An option
  with no harm passes. The slack keeps its sign.
- **Check:**
  - In the 5T and LOADBench S1 outputs, are any functional devices below vdsat? Look at G1.1.
  - If none are, the step changes nothing on these designs. Record that.

**Done when:** the tests pass, and the effect on the two designs is recorded.

Suggested commit message: `Phase A step 4: S3 saturation check is do-no-harm for devices below vdsat in the
schematic`.

### Step 5: tagging and grouping, with the designer's groups (A3; rows 47–48; D-e; 1.5 h)

**Three changes:**

**(a) Dummy-aware tagger** (row 47). In `src/s1/run.py`, `classify_nodes` (~line 76; `diode = {...}`):

- skip devices whose category is `dummy` when it tags diode-connected and tail nodes;
- read the category from the S0 IR or the primitives. Find where S0 stores it (`primitives.json` category
  `dummy`, or the recogniser's dummy list);
- keep the dummies' capacitance in the linear model.

Neither design has dummies, so this protects new SPICE files. Add a unit test with a synthetic IR: a device whose
d, g and s all sit on `VSS`.

**(b) Mirror-bank rule.** In S0, after `map_hierarchy` builds the blocks (`src/s0/ingest.py`, ~line 61):

- **Rule.** Mirror blocks of the same polarity whose devices share the gate net and the source net, at least one
  of them diode-connected, are merged into one block, `primitive: <p|n>mos-current-mirror-bank`. The block records
  its `merged_from` blocks and gives each member's W × m ratio to the diode device.
- **Other groups.** A device can stay in one functional, non-matching block as well, as P5 does in the CS stage.
- **LOADBench.** X4 {P2, P8} and X5 {P2, P5} become one bank {P2, P8, P5}, ratio 1 : 2.43 : 23.8. Today two blocks
  share the name `p_current_mirror`, so name the merged block uniquely.
- **5T.** Unchanged. XM5's gate is driven by the ideal source V1, and there is no diode device, so there is
  nothing to merge.
- **S1 G1.4.** Check that a bank is handled as a mirror ratioed by W × m with the same L and model, which is
  consistent (`_matching_entry`, ~line 122).

**(c) Designer groups file.**

- **The file.** Create `inputs/loadbench_miller/designer_groups.yaml` with Imasha's grouping, dated 2026-11-01,
  with `source: designer review (Imasha)`:

  ```yaml
  groups:
    - {name: pmos_bias_bank, kind: mirror_bank, devices: [XDiodeTransistorPmos2, XNormalTransistorPmos8, XNormalTransistorPmos5]}
    - {name: input_pair, kind: diff_pair, devices: [XNormalTransistorPmos7, XNormalTransistorPmos6]}
    - {name: nmos_mirror_load, kind: mirror, devices: [XDiodeTransistorNmos1, XNormalTransistorNmos4]}
    - {name: cs_stage, kind: functional, devices: [XNormalTransistorNmos3, XNormalTransistorPmos5], matching: none}
  floorplan_rows:          # for S4 only; top (VDD side) to bottom (VSS side)
    - [XDiodeTransistorPmos2, XNormalTransistorPmos8, XNormalTransistorPmos5]
    - [XNormalTransistorPmos7, XNormalTransistorPmos6]      # own n-well: body tied to the common source
    - [XDiodeTransistorNmos1, XNormalTransistorNmos4, XNormalTransistorNmos3]   # N3 here or below, "as space allows"
  ```

- **How S0 uses it.** Point to the file from the package with `designer_groups:`. S0 reads it after the upstream
  blocks and after (b), and then:
  - compares each designer group with the automatic blocks and reports agreement as info, under a new info item in
    the S0 report;
  - lets the designer's groups win where they disagree, and records them in `circuit_ir.json` →
    `hierarchy.blocks` with `source: designer`;
  - copies `floorplan_rows` into the IR untouched for S4. Nothing in S0–S3 uses them.
- **Frozen files.** Do not edit `circuits/loadbench_miller/upstream/*`, which is hash-frozen.

**Tests:**

- The LOADBench IR has one bank {P2, P8, P5}.
- The CS stage is listed in `not_matching_blocks`.
- The designer file agrees with the automatic result (expected: full agreement).
- The 5T blocks are unchanged.
- `tests/test_s0*.py` still pass.

**Done when:** the tests pass, and LOADBench S0 and S1 are re-run and show the bank in G1.4.

Suggested commit message: `Phase A step 5: dummy-aware tagger, mirror-bank rule, designer groups for LOADBench`.

### Step 6: fair scoring and one tolerance (A4; review C items 3, 5 and 11; 1 h)

**Files and changes:**

- **One tolerance.** Add `TOL_USE = 0.02` (Q3) in one place and import it in three places:
  - `src/s2/run.py`: `TOL_VERIFY` (line 36) and G2.5 (~line 652);
  - `src/s2/baselines.py`: `outcome(tol=...)`;
  - `src/s3/run.py`: `TOL` (line 31), now used as `TOL_USE × eta` of the margin.

  Keep G2.5's 10 % as a reported column only (`within_first_order_error_10pct`).
- **lp_floor_k.** In `src/s2/baselines.py`, `lp_floor` (~line 73), add an `upper` argument. `run_all` scores
  both:
  - `lp_floor`, capped at need, as in plan v2;
  - `lp_floor_k`, capped at KAPPA × need (`budgets.py` line 36), the same as ours.

  Add `lp_floor_k` to the tables and figures that list the methods (`run.py` G2.8, `compare_before_after.py`).
- **Optional.** The phase-2 iteration cap instead of 300 s of wall-clock time (`budgets.py`, line ~142). It
  matters only above 200 elements, so not for these two designs. Do it only if it is quick, and write down that it
  has no effect here.

**Tests:**

- `grep` finds no other tolerance constants for use checks.
- `lp_floor_k` ≥ `lp_floor` element by element.
- `outcome()` uses `TOL_USE`.

**Done when:** the tests pass.

Suggested commit message: `Phase A step 6: one tolerance (TOL_USE), lp_floor_k with ours' upper bound`.

### Step 7: PM reference phase (A6; row 46; 30 min)

**Why.** PM is measured as 180 + (phase at the unity-gain frequency − phase at 1 Hz). When the dominant pole is
near 1 Hz, the 1 Hz phase is already part of the roll-off.

**Files and changes:**

- `src/s1/linear.py`:
  - line ~169: replace `ph[0]` by `180 × round(ph[0] / 180)`;
  - line ~252, in `delta`: use the same reference for both models;
  - write the reference used, and the raw 1 Hz phase, into the S1 report.
- `scripts/benchlib.py`, the AC template (lines ~53–57): make the same change in ngspice syntax for generated
  benches. Check that it parses in ngspice-47; if there is no easy `round`, use `floor(x/180 + 0.5)`.
- **Frozen benches.** Do not edit `circuits/*/testbenches/` (hash-frozen). For the 5T and LOADBench, measure the
  1 Hz phase's distance from the nearest multiple of 180° (S0 AC raw data, or a one-off ngspice run) and record
  it in the S1 report. Expected: below 0.01°. If it is above 0.05°, stop and ask Imasha.

**Tests:** a unit test where `linear` gets a one-pole H(s) with the pole at 25 Hz. PM must come out against the
rounded reference, and the old formula must read about 2.3° high.

**Done when:** the tests pass, and both designs' S1 G1.2 PM differences are within 0.01° of plan v2.

Suggested commit message: `Phase A step 7: PM reference phase rounded to the nearest 180 deg (model and bench
template)`.

### Step 8: G2.0 route lengths from the representative cells (row 44; 1 h)

**Why.** In plan v2, G2.0's route part still took lengths from S0's as-sized PCells. LOADBench's are single
fingers of 484 and 887 µm, so the route R comes out mostly as an artefact.

**File and change:** `src/s2/run.py`, line ~237, where `unit = {d: (w + h) / 2 ...}` uses `device_sizes(s0)`:

- Take the half-perimeter from the `bbox_um` of the representative option of the device's type. That option is in
  the S3 library S2 already loads (`library_floors` → `representative`; S3 rows carry `geometry.bbox_um`).
- If a type has no representative cell, fall back to `device_sizes(s0)` and list the device in G2.0 as
  `route_from: as-sized PCell`.
- Both designs have m = 1 everywhere. For m > 1, scale as S3 does and mark the rule ASSUMPTION in the code.
- Keep the as-sized value in G2.0 as a second column for comparison.

**Tests:**

- On LOADBench, the route length of N3 and P5 drops to the representative cell's size.
- The 5T changes little.
- G2.0 is info only, so no budget changes. Check that 'ours' budgets are identical before and after this step.

**Done when:** the tests pass.

Suggested commit message: `Phase A step 8: G2.0 route lengths from the representative cells`.

### Step 9: SPICE vs first order, per verified check (row 42; 1 h)

**Why.** For the 5T's binding PVT check, first order said ours used all of its allowance, while SPICE measured
−0.16 of the margin: the GBW rose. G2.5 never compares the two.

**File and change:** `src/s2/run.py`, G2.5 and G2.8 (~lines 590–670). For every check simulated in SPICE, add:

- `first_order_use` and `spice_use`, both as a fraction of eta × margin;
- `diff_frac_of_margin = |spice − first order| / margin`;
- `sign_disagrees`.

**Reported, not gated.** Add a summary `G2.10_model_agreement (info)` listing the checks with a sign disagreement
or with `diff_frac_of_margin` above 0.25. The 0.25 is an ASSUMPTION for flagging only; say so in the report.

With nominal-only budgets, the 5T check of row 42 (GBW at tt, 0.9 V, 27 °C) no longer binds. Report it from the
G2.9 PVT table instead, and write a note in G2.10 when the nominal results differ from it.

**Tests:** a unit test of the summary on fake numbers.

**Done when:** the tests pass.

Suggested commit message: `Phase A step 9: SPICE vs first-order agreement reported per verified check`.

### Step 10: LOADBench hand model with the mirror doublet (A5; row 49; 1.5 h)

**Why.** LOADBench's PREDICTED textbook equations have no NMOS-mirror pole-zero doublet (pole at about 33 MHz).
That doublet accounts for the whole 17° gap between the hand PM and SPICE.

**Context.** The 5T already has this fix: `src/s1/symbolic_patch.py` writes patched copies P1 and P2 of the
upstream equations.

**Files and changes:**

- Extend `symbolic_patch.py`, or add `src/s1/symbolic_patch_miller.py` (simpler, and keeps the 5T module as it
  is), to write a patched copy of `circuits/loadbench_miller/upstream/equations.predicted.json`. Its first-stage
  transconductance gets the mirror doublet:

  `Gm(s) = gm_P7/2 · (1 + 1/(1 + s·τm))`, with `τm = C(FirstStageYout1) / (gm_N1 + gds_N1 + gds_P7)`,

  using the S1 OP values. This is the textbook form: check its signs and symbols against the file's conventions,
  as `symbolic_patch.py` does for the 5T. The node capacitance comes from the S1 linear model. The zero sits at about 2/τm.
- **Write location.** `inputs/loadbench_miller/upstream_patched/equations.predicted.P1.json`. That folder is not
  frozen, and nothing is written into `circuits/`.
- Label the copy **PREDICTED (patched, post hoc)**. It was fitted after seeing this circuit, so judge it on new
  designs too.
- Add `s1_extras: [symbolic_patch_miller]` to LOADBench's package. Add the step in `src/flow.py`, `steps()`, S1
  branch, next to `symbolic_patch`.

**Tests:**

- The patched hand PM is within a few degrees of SPICE (record the number).
- The unpatched copy still gives the old value.
- G1.5 stays report-only.
- S2 budgets do not change, because S2 uses the SPICE-linearised model.

**Done when:** the tests pass, and `outputs/S1/loadbench_miller/` holds a `symbolic_patch_check.json` like the
5T's.

Suggested commit message: `Phase A step 10: LOADBench hand model with the NMOS mirror doublet (PREDICTED, post
hoc)`.

### Step 11: tests and goldens (1 h)

1. Run `python3 -m pytest -q tests/`, which must pass in full.
2. Run `./flow test`. The other three designs compare their committed outputs with their goldens, so they should
   still pass unchanged.
3. Also run `./flow test --design ota5t_stress --stage S1 --rerun`. It is quick, and it shows that the shared code
   still runs on a frozen design. Differences from steps 6–7 are expected there: record them, but don't refresh
   its golden.

Golden refresh for the two designs (Q4) is part of step 12, after the re-runs.

### Step 12: re-run, snapshot and compare (runs 1–3 h; check the plan-v2 run times in `runs/logs/flow/`)

Run the jobs detached, as `CLAUDE.md` describes, one design at a time. Record each job under *Running* in
STATUS.md.

```bash
python3 -m src.flow run example_ota_5t --from S1     # S0 unchanged for the 5T (check: step 5 left its blocks as they were)
python3 -m src.flow run loadbench_miller --from S0   # S0 changes (bank, designer groups)
python3 scripts/compare_before_after.py snap example_ota_5t after_v3a
python3 scripts/compare_before_after.py snap loadbench_miller after_v3a
python3 scripts/compare_eta09_rerun.py example_ota_5t --first after_nopvt --rerun after_v3a
python3 scripts/compare_eta09_rerun.py loadbench_miller --first after_posthoc_leastbad --rerun after_v3a
python3 -m src.flow snapshot example_ota_5t --stage all      # golden refresh, only with Q4 = yes
python3 -m src.flow snapshot loadbench_miller --stage all
```

**Checks:**

- If a run ends with ERROR, stop. Find the cause and add a journey row (flow record 7.1, from row 51).
- Compare with the predictions of section 4. Every prediction that fails gets one line of explanation. Do not
  change a rule to make a prediction come true.
- Run `python3 scripts/compare_before_after.py report` to regenerate `docs/before_after.md`. If it would rewrite
  the other designs' sections, check that their content is unchanged.

Suggested commit message: `Phase A step 12: 5T and LOADBench re-run (after_v3a), golden snapshots refreshed`.

### Step 13: documentation and an independent review (1–1.5 h)

1. **Flow record.**
   - Add rows 51 onward to the 7.1 journey table, one per bug found during Phase A.
   - Add a new section 7.13, "Plan v3 Phase A (5T and LOADBench)". It covers what changed, the before/after
     table (after or after_nopvt → after_v3a), the predictions and their outcomes, and what is still open.
   - Edit `docs/flow_record_section7_draft.md`, then run `python3 scripts/merge_section7.py`.
2. **Other files.**
   - `docs/progress_log.md`: a dated entry.
   - `README.md`: `budget_corners`, `designer_groups`, exit code 3, `lp_floor_k`, the new S1 extra, tag
     `after_v3a`.
   - `docs/STATUS.md`: results, then release the claim.
3. **Independent review.** Start a sub-agent that has not seen our conclusions. Give it:
   - the Phase A diff (`git diff <tag>..HEAD -- src scripts`);
   - this plan;
   - section 7.13.

   Ask it to find bugs, unfair comparisons, and claims the data does not support. Record each finding and what was
   done about it, as review D in 7.9.
4. Tell Imasha it is ready for the final commit, and list any **FEEDBACK NEEDED** question.

---

## 4. Expected effect on the two designs (PREDICTED, written before the runs)

Copy this table into the step 1 amendment unchanged. The word "expected" means a prediction, not a result.

| Step | example_ota_5t | loadbench_miller |
|---|---|---|
| 2 hygiene | no number changes | no number changes |
| 3 nominal budgets | allocation identical to the `after_nopvt` snapshot (t_round1 3.401, 21 elements, min ratio to need 3.23; regression check) | budgets larger than plan-v2 'after' (no longer starved at the PVT points). The PVT use table shows points above 1.0 (reported, not gated) |
| 4 S3 do-no-harm | no change if every functional device is saturated (check G1.1) | same |
| 5 grouping | blocks unchanged | one bank {P2, P8, P5}, consistent in G1.4; the CS stage is not matched; designer file and automatic rule agree |
| 6 tolerance, lp_floor_k | G2.5 may report more checks over 1.02. Outcome words for ours unchanged at eta 0.5; lp_floor_k gets more room than lp_floor | same |
| 7 PM reference | about 2e-5° (pole at about 2.7 MHz) | about 2e-3° (pole at about 29 kHz) |
| 8 G2.0 route | small change | route part of G2.0 drops a lot (no 484 and 887 µm single fingers) |
| 9 model agreement | the row-42 corner appears in the PVT report, no longer binding | listed checks, if any |
| 10 hand model | — | hand PM gap falls from about 17° to a few degrees (G1.5, report only) |
| 12 S3 and SPICE | area and relaxed types close to `after_nopvt` | fewer relaxed types than plan-v2 'after' (all 6 were relaxed). PM after S3 at or above plan-v2 post hoc 64.7° |

---

## 5. Open issues per stage: in this version, and for a new SPICE file

Every row comes from the journey table (rows 1–50), the review pack or the code. The **Phase A** column says
whether this plan touches it.

### S0: ingest, binding, PVT

| Issue | 5T / LOADBench now | With a new SPICE file | Phase A |
|---|---|---|---|
| Element support: SKY130 MOSFETs (incl. LVT), R, C, ideal V and I sources (rows 1–3) | fine | other devices (BJT, diode, MIM cap, poly resistor, HV devices) stop S0 with "unsupported element". Each needs parser, IR, linear-model and binding support, plus a test | no |
| Hierarchy and naming: flattening (`scripts/flatten_spice.py`), instance prefixes (`x1_M3`), name map to the upstream primitives | 5T through `inputs/example_ota_5t/name_map.yaml`; LOADBench through LOADBench's own recognition | without `primitives.json` and a name map there are no blocks, so G1.4 has no groups. You need `scripts/recognize_structures.py` (rule-based; row 48 shows its errors) or a `designer_groups.yaml` | step 5 adds the designer file |
| m, mult, nf, MF semantics (rows 4, 17, 26) | all m = 1 | m > 1 is drawn as copies, LVS-checked; MF alone scales mismatch, not capacitance | no |
| PDK: SKY130A only; the metal model is metal1 only | fine | another PDK needs new PCells, rules and a parasitic table | no |
| Interface by hand: port roles, `bias_sources`, `ac_drive`, testbench port map (`inputs/_template`) | written | must be written for each design; a wrong role gives a wrong AC ground (rows 3, 6) | no |
| Bench types: only `diso` (single-ended output) and `dido` (fully differential) amplifier benches | fine | comparators, LDOs, bandgaps, filters and anything switched have no bench, so no margins and no budgets | no |
| Specs: 5T has the upstream's real specs; LOADBench's are an ASSUMPTION (gain −1 dB, GBW × 0.9, PM ≥ 60°) | the size of LOADBench's margin is set by that rule (PM 65.3° → 5.3° of margin) | with no specs you need a rule or the designer's numbers (D4); `specs_from_achieved` stops on a missing value (review B item 8) | no (D4 still open) |
| Reproduction G0.8: the designer's conditions (load, bias, VDD) | reproduced | needs the designer's bench; TTSKY needed `save all` (row 5) | no |
| Hash freezing (rows 16, 45) | in `circuits/SOURCE_SHA256.txt` | every new design's source, upstream and testbench files must be added; a change is a logged decision | no |
| Ideal elements without a layout device: LOADBench's Cc 0.5 pF and Ibias 10 µA | Ibias removed from the layout view; Cc is ideal | S4 must decide: MIM capacitor or external? Is the bias pin off-chip? | no (S4 question) |
| G0.7 met1.6 at netlist size: single-finger cells at short L (rows 7, 37) | LOADBench's N3 (484/0.24) fails as drawn, a real PDK finding; S3 patches the gate pad | expect it for any wide, short-L single finger | no |
| PVT: 45 points + 200 Monte Carlo runs (row 8) | minutes | scales with circuit size; still needed for the step 3 report | step 3 (report) |

### S1: intent, linear model, sensitivities

| Issue | 5T / LOADBench now | With a new SPICE file | Phase A |
|---|---|---|---|
| PREDICTED hand equations per topology | 5T: upstream + patch; LOADBench: textbook, missing the mirror doublet (row 49) | a new topology has none, so G1.5 is skipped (report only). Someone has to write them; LLM drafting is a planned role (section 6) | step 10 (LOADBench) |
| Metrics: gain, GBW, PM and noise only | fine | no slew, settling, CMRR, PSRR, offset or power budgets (power is unbudgeted, review C 14) | no |
| Linear model from the SPICE OP (G1.2: 0.2 dB, 3 %, 2°) | within tolerance | needs a DC operating point; clocked or large-signal circuits are not covered | no |
| Node-time-constant pole estimates use DC resistance (row 49, iadc triode fold node) | fine | misleading where devices sit in triode | no |
| Tagger heuristics (diode, tail); dummies (row 47) | no dummies | dummies with g = d = s are tagged as mirrors | step 5a |
| L-ratioed mirrors (row 31) | none | handled: equal-L subsets checked | no |
| PM measurement (row 46) | negligible (about 2e-5° and 2e-3°) | wrong when the dominant pole is near 1 Hz | step 7 |
| CMFB loop not analysed (D8) | single-ended | fully differential designs need it | no |
| Sensitivity cost: central differences ±1 fF on every net and pair | seconds | the pair count grows with nets²; a large netlist needs pruning (the planned suspect list, D5) | no |
| Matching groups from blocks (G1.4) | 5T fine; LOADBench gets the bank | only as good as recognition or the designer file | step 5 |

### S2: budgets

| Issue | 5T / LOADBench now | With a new SPICE file | Phase A |
|---|---|---|---|
| Corner set | plan v2 used all 45 PVT points; tiny margins bound every design (1h) | same risk | step 3: nominal only, PVT reported |
| First order vs SPICE (row 42) | 5T's binding corner contradicted | unknown until checked | step 9 (report) |
| Tolerances: 1 %, 2 % and 10 % in different places (review C 3) | inconsistent | same | step 6 |
| Baseline fairness: `lp_floor` capped at need, ours at 10 × (review C 5) | favours ours | same | step 6 (`lp_floor_k`) |
| Phase 2 capped by wall-clock time above 200 elements (row 21, review C 11) | below 200 elements | results can depend on machine load | optional in step 6 |
| Floors come from the S3 A-bin library; a type with no signed-off cell has none (row 37) | LOADBench N3 needs the gate-pad patch | new device types, new floors | no |
| G2.0 uncalibrated: metal1 route model, one stub per pin, harmful rates only; PREREG's 25 % claim untested until S5–S7 | LOADBench route part is an artefact (row 44) | same | step 8 (route), calibration later |
| Specs not met before layout (negative margin) | none | constraints skipped and listed (row 24); nothing to budget | no |
| Stale files and crashes (rows 40, 43) | risk in variant runs | same | step 2 |

### S3: device options

| Issue | 5T / LOADBench now | With a new SPICE file | Phase A |
|---|---|---|---|
| Saturation check for devices below vdsat (row 41) | probably not hit (check) | every option fails | step 4 |
| Relaxed fallback: least-bad, decided post hoc (2026-10-27 amendment) | LOADBench needed it | same rule | no |
| Option grid: nf 1–8 (16–64 for wide fingers), gate contacts, S/D coverage; giant single fingers; short-L gate-pad patch | fine with the patch | other device types need their own options and a signed-off cell | no |
| Run time: one Magic cell + extraction + SPICE per option | minutes | TTSKY took 73 min; grows with types × options | no |
| G3.3 checks nominal only | consistent with D-b now | same | step 3 makes it consistent |
| Decides per device type, not per placement; matching groups are not used | fine for S3 | matching and common-centroid belong to S4 | no |

### S4 (not built): questions from the designer review, for later

1. **Floorplan rows by current path.** For LOADBench these are recorded in `designer_groups.yaml` (step 5). How
   does S4 turn rows into placement?
2. **The PMOS bank's ratio.** It is 1 : 2.43 : 23.8, not an integer ratio. Should a common unit cell with a small
   ratio error be used, or no common-centroid at all? Imasha decided to keep the sizes (D-d), so S4 must say how it
   draws non-integer ratios.
3. **Dummies.** The designer rule is dummies at row ends, switched off, with the extra drain capacitance charged to
   that net's budget. Neither netlist has dummies, so S4 adds them and S2 must know their cost.
4. **The diff pair P6/P7.** Its bulk is tied to the common source, so it needs its own n-well.
5. **Ideal Cc and Ibias.** These need layout decisions: a MIM capacitor, and the bias pin.

### Infrastructure

| Issue | Status | What to do |
|---|---|---|
| Windows Modern Standby slowed or paused runs (row 39) | open | before long runs, set the power plan to "never sleep" while plugged in, or keep the PC awake |
| Writes into the mounted folder failed with `Errno 22` (row 40) | open | rare; step 2's exit codes and identity checks catch it |
| Zombies: `kill -0` succeeds on them (row 32) | rule in `CLAUDE.md` | wait on log lines and `.exit` files, never on a PID |
| Deploy conflicts between Claude Code and Cowork (rows 33, 45) | `apply.sh` guards | don't let both agents edit the same files; claim in STATUS.md |
| Memory for R+C runs (row 30) | capped | not needed in Phase A |
| Docker must be running | — | step 0 checks it |

### Checklist for a new SPICE file (questions to answer before S0)

1. Is it SKY130A, and are all its devices supported (S0 table above)?
2. Is it flat, or hierarchical with known subcircuits? Who provides the structure: `primitives.json`, the
   recogniser, or a designer file?
3. What are the port roles, the bias sources and the AC drive? Is there a single-ended (diso) or fully
   differential (dido) amplifier bench?
4. Where do the specs come from: the upstream, the designer, or an ASSUMPTION rule?
5. Does the designer's bench reproduce in G0.8, with the same load, bias, VDD and temperature?
6. Are there dummies, ideal elements, L-ratioed mirrors, or devices in triode by design?
7. Is a hand model available, or will G1.5 be skipped?
8. How many nets and pairs (S1 cost), device types (S3 cost) and elements (above 200, phase 2 is time-capped)?

---

## 6. How LLMs are used in each stage

**In the implemented flow (S0–S3), no LLM runs.** There is no LLM call anywhere in `src/` (checked with grep on
2026-11-01). Every number comes from:

- ngspice simulations;
- the SPICE-linearised model;
- Magic and KLayout geometry;
- the LP and max-min solvers (HiGHS through SciPy `linprog`, SLSQP or trust-constr).

The same inputs give the same outputs. S2 allocates twice to check this, and the golden tests compare whole
outputs.

LLMs were used around the flow, not inside it:

- **Developer.** Claude Code and Cowork wrote the code, the package generators and the scripts.
- **Reviewer.** Independent agents ran reviews A, B and C (flow record 7.9), plus the Plan v3 and study-guide
  reviews. They found real bugs, for example rows 41–44 and 46.
- **Analyst.** Hand equations, labelled PREDICTED. Phase A keeps all three roles.

| Stage | What runs (deterministic) | LLM at run time | How an LLM was used to build it | Planned LLM role (not built) | Guardrail that keeps the result honest |
|---|---|---|---|---|---|
| S0 ingest | parser, IR, PCell binding with LVS, 45 PVT points | none | wrote the parser and package generators (`make_loadbench_package.py`); read the upstream sources to write `SOURCE.md`; Cowork found the iadc provenance error (row 50) | draft `package.yaml` (port roles, bias sources) and a `primitives.json` for a new netlist | G0 gates: hash freeze, LVS of every binding, G0.8 reproduction; a person approves; anything not from upstream is labelled ASSUMPTION |
| S1 intent | SPICE OP, linear model, central-difference sensitivities, tags, G1.x | none | wrote the PREDICTED equations for LOADBench and the 5T patch; reviewers found the PM bug (row 46) and the missing hand-model elements (row 49) | explain and audit: read the sensitivity table, propose missing elements, write the "why" for each suspect net | the SPICE-linearised model is the reference (G1.2); hand models are report-only (G1.5) |
| S2 budgets | max-min allocation with floors, LP baselines, SPICE checks | none | implemented the allocator and baselines; reviews B and C found unfair scoring and stale files | propose rules (which nets to budget together, the suspect list D5). The numbers still come from the solver | PREREG rules frozen before runs; four baselines; SPICE verification G2.5 and G2.8 |
| S3 devices | PCell option grid, extraction, SPICE per option | none | wrote the option grid and evaluation; a review found the saturation bug (row 41) | prune the option grid to save run time, with reasons | every chosen option is still simulated (G3.3); the fallback rule is fixed in PREREG |
| S4/S5 (not built) | — | — | — | planner and tuner: propose floorplans from the designer's rules; tools place and route; PEX checks | D10: no LLM until a deterministic S4 works, so there is a baseline to beat |

**What this means for the paper.** The contribution of S0–S3 is the deterministic budgeting and checking. LLM
roles would be added later as separate, ablatable components, measured against this deterministic flow.

---

## 7. Out of scope (do not start)

- **Other designs.** `ota5t_stress`, `iadc_ota`, `ttsky25a_fd` and any re-run of them. That includes the TTSKY
  S2 eta 0.9 re-run (row 40), the TTSKY and iadc recognition fixes (row 48), iadc's provenance note (row 50) and
  its hand model.
- **Other phases.** Phase B (sizing–layout contract), C (suspect list, D5), D (S3 candidates, S4 blocks) and
  E (PEX).
- **Other corner sets.** D1's middle 9 corners, near-zero-margin PVT rules (1h) and the CMFB check (D8).
- **New software or connections.** Any new package, and any GitHub or other connection.
