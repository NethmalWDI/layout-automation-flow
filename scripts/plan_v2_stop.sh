#!/usr/bin/env bash
# Stop every plan-v2 run in the container cleanly (before switching the PC off). Run inside the container:
#   docker exec layout-s0s3 bash /foss/designs/scripts/plan_v2_stop.sh
# Order: the queue / lane shells first (so they cannot start a next step or write a .done marker), then the
# flow and stage processes, then the simulators. Finished steps keep their runs/state/plan_v2/*.done markers;
# the interrupted step runs again from its start next time (scripts/plan_v2_resume.sh).
# The container's PID 1 does not reap, so killed processes stay as <defunct> zombies: harmless, gone after a
# container restart.
me=$$
pids() { pgrep -f "$1" | grep -vx "$me" | grep -vx "$PPID"; }
list() { for p in "$@"; do ps -o pid=,args= -p "$p" 2>/dev/null | cut -c1-110; done; }
shells=$(pids 'plan_v2_resume|queue_v2|ttsky_before_s1|iadc_before_s3|lane_[AB]')
echo "shells:"; list $shells
[ -n "$shells" ] && kill -9 $shells 2>/dev/null
sleep 1
work=$(pids 'python3 -m src\.|scripts/reference_layout|scripts/compare_before_after|scripts/reference_(iadc|ttsky25a)')
echo "flow / stage processes:"; list $work
[ -n "$work" ] && kill -9 $work 2>/dev/null
sleep 1
sims=$(pgrep -x ngspice; pgrep -x magic; pgrep -x netgen; pgrep -f 'netgen|magic -dnull')
sims=$(echo "$sims" | sort -u | grep -v '^$')
echo "simulators: $(echo $sims | wc -w)"
[ -n "$sims" ] && kill -9 $sims 2>/dev/null
sleep 1
left=$(ps -eo stat=,args= | grep -v '^Z' | grep -E 'python3 -m src|ngspice|reference_layout|queue_v2|plan_v2_resume' | grep -v grep | grep -v plan_v2_stop)
echo "still running: ${left:-none}"
ls runs/state/plan_v2 2>/dev/null | sed 's/^/done: /'
