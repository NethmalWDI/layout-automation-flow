#!/usr/bin/env bash
# Plan v2: finish the queue unattended, then the post-hoc test of a 'least-bad' fallback for relaxed S3 device
# types (Imasha's decision, 2026-10-27; written by Claude Code; see docs/STATUS.md and the progress log).
#
# 1. Waits until the side lane (scripts/plan_v2_laneA_now.sh writes runs/logs/plan_v2_laneA_now.log.exit) and
#    the resume script's lane B (its last step, ref_ttsky_rc, in runs/logs/plan_v2_lane_B.log) have both ended.
# 2. Stops the paused first pass of scripts/plan_v2_resume.sh (kill -STOP since 06:26; found by its state and
#    command line), keeps that pass's logs as runs/logs/plan_v2_*_pass1.log and runs the resume script again.
#    It skips every .done step and runs the no-PVT ablation, eta 0.9, the golden snapshots and the report.
# 3. Post-hoc test, labelled as such and not pre-registered: for every design whose 'after' S3 relaxed a device
#    type, S3 again on the same 'after' budgets with --relax-fallback least-bad (a relaxed type keeps the
#    option whose worst check, access R included, is broken least, instead of the default PCell), written to
#    outputs/posthoc/least_bad/<design>/; snapshot tag after_posthoc_leastbad; the report is written again.
#    The 'after' outputs are not touched. LOADBench first: its 'after' PM fell to 48 deg this way.
#
# Run inside the container, from the repo root, detached:
#   docker exec -d layout-s0s3 bash -lc "cd /foss/designs && bash scripts/plan_v2_after_queue.sh > runs/logs/plan_v2_after_queue.log 2>&1; echo \$? > runs/logs/plan_v2_after_queue.log.exit"
# Stop it: kill its bash (pgrep -af plan_v2_after_queue), then any python3 it started.
set -u
cd /foss/designs && source scripts/env.sh
ST=runs/state/plan_v2
L=runs/logs
P=outputs/posthoc/least_bad

lanes_done() {
  [ -f $L/plan_v2_laneA_now.log.exit ] && grep -Eq '^(    ref_ttsky_rc rc=|--- skip ref_ttsky_rc)' $L/plan_v2_lane_B.log
}
live_resume() {   # copies of the resume script that are neither stopped nor zombies
  ps -eo stat=,args= | awk '$1 !~ /^[TZ]/ && $0 ~ /bash scripts\/plan_v2_resume[.]sh/' | wc -l
}

echo "##### plan v2 after-queue $(date '+%F %T'): waiting for the side lane and lane B"
until lanes_done; do sleep 60; done
echo "both lanes ended $(date '+%F %T'): side lane exit $(cat $L/plan_v2_laneA_now.log.exit);" \
     "lane B: $(grep -E 'ref_ttsky_rc' $L/plan_v2_lane_B.log | tail -1)"

# 2. the second pass of the resume script
for p in $(ps -eo pid=,stat=,args= | awk '$2 ~ /^T/ && $0 ~ /bash scripts\/plan_v2_resume[.]sh/ {print $1}'); do
  pp=$(ps -o ppid= -p $p | tr -d ' ')
  kill -KILL $p && echo "stopped the paused resume script, PID $p"
  sleep 2
  if [ -n "$pp" ] && [ "$(ps -o stat= -p $pp | cut -c1)" != Z ] && tr '\0' ' ' < /proc/$pp/cmdline 2>/dev/null | grep -q 'plan_v2_resume[.]sh'; then
    kill -KILL $pp && echo "and its wrapper, PID $pp"
  fi
done
sleep 2
if [ "$(live_resume)" != 0 ]; then
  echo "the resume script was already started again by someone else: waiting for it $(date '+%F %T')"
  while [ "$(live_resume)" != 0 ]; do sleep 60; done
else
  for f in plan_v2_resume plan_v2_lane_A plan_v2_lane_B; do
    [ -f $L/$f.log ] && [ ! -f $L/${f}_pass1.log ] && cp -p $L/$f.log $L/${f}_pass1.log
  done
  echo "=== resume script, pass 2 $(date '+%F %T') (log $L/plan_v2_resume.log)"
  bash scripts/plan_v2_resume.sh > $L/plan_v2_resume.log 2>&1
  echo "    resume script rc=$? $(date '+%F %T')"
fi
grep -q '^##### plan v2 resume ended' $L/plan_v2_resume.log || { echo "the resume script did not finish: no post-hoc test"; exit 1; }
tail -3 $L/plan_v2_resume.log

# 3. the post-hoc test
for d in loadbench_miller ota5t_stress iadc_ota ttsky25a_fd example_ota_5t; do
  n=posthoc_leastbad_$d
  if [ -f "$ST/$n.done" ]; then echo "--- skip $n (done $(cat "$ST/$n.done"))"; continue; fi
  if [ ! -f "$ST/snap_${d}_after.done" ] || [ -d runs/tmp/aside/$d ]; then
    echo "--- $d: no finished 'after' run, or its outputs are still set aside: not tested"; continue
  fi
  nrel=$(python3 -c "import json,sys; r=json.load(open(sys.argv[1])); print(len((r.get('S3') or {}).get('relaxed') or []))" \
         outputs/compare/$d/after.json 2>/dev/null)
  if [ "${nrel:-0}" = 0 ]; then echo "--- $d: no relaxed type in its 'after' S3: nothing to test"; continue; fi
  echo "=== $n: $nrel relaxed types in 'after' $(date '+%F %T')"
  rm -f $P/$d/s3_report.json
  python3 -m src.s3.run inputs/$d/package.yaml --workers 4 --relax-fallback least-bad --out $P/$d > $L/$n.log 2>&1
  rc=$?
  echo "    $n rc=$rc $(date '+%T')  log: $L/$n.log"
  if [ $rc -le 1 ] && [ -f $P/$d/s3_report.json ]; then
    python3 - outputs/S3/$d/s3_report.json $P/$d/s3_report.json <<'EOF'
import json, sys
a, b = (json.load(open(f))["provenance"]["inputs"] for f in sys.argv[1:3])
same = {x["path"]: x["sha256"] for x in a} == {x["path"]: x["sha256"] for x in b}
print("    same inputs as the 'after' S3 (S0 circuit, S2 budgets, PDK rules, package):", "yes" if same else "NO")
EOF
    python3 scripts/compare_before_after.py snap $d after_posthoc_leastbad $P/$d && date '+%F %T' > "$ST/$n.done"
  fi
done
python3 scripts/compare_before_after.py report
echo "##### plan v2 after-queue ended $(date '+%F %T')"
