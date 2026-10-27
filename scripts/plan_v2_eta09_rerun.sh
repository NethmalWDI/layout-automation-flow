#!/usr/bin/env bash
# Plan v2: S2 at eta 0.9 again for example_ota_5t and loadbench_miller, with the PC awake (Imasha's decision,
# 2026-10-27; written by Claude Code; see docs/STATUS.md). Their first eta 0.9 runs (10:15-10:27 and 10:46-11:20 CET)
# ran almost entirely while Windows had the PC in Modern Standby, and their logs are gone, so a SPICE check pushed
# past its 180 s limit by the standby (a failed run: outcome "unverified", a violation possibly hidden) cannot be
# ruled out.
#
# 1. Waits until scripts/plan_v2_after_queue.sh has ended (the queue and the post-hoc test); stops if it did not
#    finish, or if other designs' outputs are still set aside.
# 2. For each design, the resume script's eta 0.9 step: 'after' outputs set aside, S2 --eta 0.9 --workers 4,
#    snapshot, 'after' outputs put back. Three differences: the snapshot tag is after_eta0.9_rerun (the first run's
#    after_eta0.9 stays); the re-run's S2 folder is kept in outputs/posthoc/eta09_rerun/<design>/S2; and
#    outputs/posthoc/eta09_rerun/<design>/clock.json records wall-clock time against container uptime over the
#    run (a standby or a paused VM shows as a jump).
# 3. scripts/compare_eta09_rerun.py (first run against re-run), then the before/after report.
#
# Run inside the container, from the repo root, detached:
#   docker exec -d layout-s0s3 bash -lc "cd /foss/designs && bash scripts/plan_v2_eta09_rerun.sh > runs/logs/plan_v2_eta09_rerun.log 2>&1; echo \$? > runs/logs/plan_v2_eta09_rerun.log.exit"
# Stop it: kill its bash (pgrep -af plan_v2_eta09_rerun), then its python3; an interrupted design is put back and
# re-run when the script is started again.
set -u
cd /foss/designs && source scripts/env.sh
ST=runs/state/plan_v2
L=runs/logs
R=outputs/posthoc/eta09_rerun
DESIGNS="example_ota_5t loadbench_miller"

step() {      # step <name> <command...>   done when rc = 0 (as in scripts/plan_v2_resume.sh)
  local n=$1; shift
  if [ -f "$ST/$n.done" ]; then echo "--- skip $n (done $(cat "$ST/$n.done"))"; return 0; fi
  echo "=== $n $(date '+%F %T')"
  "$@"; local rc=$?
  echo "    $n rc=$rc $(date '+%T')"
  [ $rc -eq 0 ] && date '+%F %T' > "$ST/$n.done"
  return $rc
}
restore_aside() {   # as in scripts/plan_v2_resume.sh
  local d=$1
  if [ -d runs/tmp/aside/$d/S2 ]; then
    echo "    restoring the after outputs of $d set aside by an interrupted step"
    rm -rf outputs/S2/$d outputs/S3/$d
    mv runs/tmp/aside/$d/S2 outputs/S2/$d && mv runs/tmp/aside/$d/S3 outputs/S3/$d
    rm -rf runs/tmp/aside/$d
  fi
}
aside() {     # as in scripts/plan_v2_resume.sh
  local d=$1
  rm -rf runs/tmp/aside/$d && mkdir -p runs/tmp/aside/$d
  cp -a outputs/S2/$d runs/tmp/aside/$d/S2 && cp -a outputs/S3/$d runs/tmp/aside/$d/S3
}
clock() { echo "$(date +%s.%N) $(cut -d' ' -f1 /proc/uptime)"; }

echo "##### plan v2 eta 0.9 re-run $(date '+%F %T'): waiting for scripts/plan_v2_after_queue.sh"
until [ -f $L/plan_v2_after_queue.log.exit ]; do sleep 60; done
if ! grep -q '^##### plan v2 after-queue ended' $L/plan_v2_after_queue.log; then
  echo "the after-queue script did not finish (exit $(cat $L/plan_v2_after_queue.log.exit)): nothing re-run"; exit 1
fi
other=$(ls runs/tmp/aside 2>/dev/null | grep -v -x -e example_ota_5t -e loadbench_miller)
if [ -n "$other" ]; then echo "outputs of other designs are still set aside ($other): nothing re-run"; exit 1; fi
echo "the after-queue script has ended; starting $(date '+%F %T')"

for d in $DESIGNS; do
  restore_aside $d
  [ -f "$ST/snap_${d}_after_eta0.9_rerun.done" ] && { echo "--- skip eta 0.9 re-run $d"; continue; }
  aside $d || { echo "could not set $d aside: stopped"; exit 1; }
  rm -rf outputs/S3/$d
  mkdir -p $R/$d && touch $R/$d/.started
  c0=$(clock)
  echo "=== eta 0.9 re-run of $d $(date '+%F %T')"   # no .done marker: after an interruption S2 must run again
  python3 -m src.s2.run inputs/$d/package.yaml --workers 4 --eta 0.9
  echo "    S2 rc=$? $(date '+%T')"
  c1=$(clock)
  python3 - "$c0" "$c1" > $R/$d/clock.json <<'EOF'
import json, sys
w0, u0 = map(float, sys.argv[1].split())
w1, u1 = map(float, sys.argv[2].split())
print(json.dumps({"wall_s": round(w1 - w0, 1), "uptime_s": round(u1 - u0, 1), "jump_s": round((w1 - w0) - (u1 - u0), 1),
                  "note": "wall-clock time minus container uptime over the S2 run; a standby or a paused VM shows as a jump"},
                 indent=1))
EOF
  echo "    clock: $(tr -d '\n ' < $R/$d/clock.json | cut -c1-90)"
  if [ outputs/S2/$d/s2_report.json -nt $R/$d/.started ]; then
    step snap_${d}_after_eta0.9_rerun python3 scripts/compare_before_after.py snap $d after_eta0.9_rerun
    rm -rf $R/$d/S2 && cp -a outputs/S2/$d $R/$d/S2
  else
    echo "    no new S2 report for $d: not snapped"
  fi
  restore_aside $d
done
python3 scripts/compare_eta09_rerun.py $DESIGNS
python3 scripts/compare_before_after.py report
echo "##### plan v2 eta 0.9 re-run ended $(date '+%F %T')"
