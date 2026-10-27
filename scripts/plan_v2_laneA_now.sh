#!/usr/bin/env bash
# Plan v2: lane A of scripts/plan_v2_resume.sh, without its no-PVT ablation, run on its own while that script's
# lane B (TTSKY) is still running (written 2026-10-27 by Claude Code; see docs/STATUS.md).
#
# Lane A had stopped at 05:55 on iadc 'before' S3 (no signed-off cell for the 1.2/0.2 um LVT devices; fixed by
# the gate-pad met1.6 patch in src/s3/strap.py, flow record 7.1 row 37). A second copy of plan_v2_resume.sh
# would start a duplicate TTSKY job, so this script runs only lane A's steps, with the same step names and
# .done markers in runs/state/plan_v2/: the resume script skips them when it is started again after lane B.
# The no-PVT ablation is left to that restart (it sets 5T outputs aside, as the resume script's eta 0.9 part does).
#
# Run inside the container, from the repo root, detached:
#   docker exec -d layout-s0s3 bash -lc "cd /foss/designs && bash scripts/plan_v2_laneA_now.sh > runs/logs/plan_v2_laneA_now.log 2>&1; echo \$? > runs/logs/plan_v2_laneA_now.log.exit"
set -u
cd /foss/designs && source scripts/env.sh
ST=runs/state/plan_v2
mkdir -p "$ST"
W=${W:-2}

# step, fstep, snap and after: copied from scripts/plan_v2_resume.sh
step() {      # step <name> <command...>   done when rc = 0
  local n=$1; shift
  if [ -f "$ST/$n.done" ]; then echo "--- skip $n (done $(cat "$ST/$n.done"))"; return 0; fi
  echo "=== $n $(date '+%F %T')"
  "$@"; local rc=$?
  echo "    $n rc=$rc $(date '+%T')"
  [ $rc -eq 0 ] && date '+%F %T' > "$ST/$n.done"
  return $rc
}
fstep() {     # fstep <name> <flow args...>   done when the flow finished (PASS rc 0 or FAIL rc 1)
  local n=$1; shift
  if [ -f "$ST/$n.done" ]; then echo "--- skip $n (done $(cat "$ST/$n.done"))"; return 0; fi
  echo "=== $n $(date '+%F %T')"
  python3 -m src.flow run "$@"; local rc=$?
  echo "    $n rc=$rc $(date '+%T')"
  [ $rc -le 1 ] && { date '+%F %T' > "$ST/$n.done"; return 0; }
  return $rc
}
snap() { step "snap_$1_$2" python3 scripts/compare_before_after.py snap "$1" "$2"; }
after() {     # the v2 'after' run of a design: PVT points, then S2 and S3
  # plan v2 ran S3 with the old relaxed-type rule; the S3 default changed on 2026-10-27 (PREREG amendment)
  step "$1_after_pvt" python3 -m src.s0.pvt "inputs/$1/package.yaml" --workers $W || return 1
  fstep "$1_after_S2S3" "$1" --from S2 --workers $W --relax-fallback default || return 1
  snap "$1" after
}

echo "##### plan v2 lane A (side run) $(date '+%F %T'); done so far: $(ls $ST 2>/dev/null | tr '\n' ' ')"
fstep iadc_before_S3 iadc_ota --stage S3 --variant v1 --workers $W && snap iadc_ota before || exit 1
after loadbench_miller
after iadc_ota
step ref_iadc_final bash scripts/reference_iadc.sh
echo "##### plan v2 lane A (side run) ended $(date '+%F %T')"
