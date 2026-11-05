#!/bin/bash
# Finishes the ttsky25a_fd_v2 run (rule set v2 on ttsky25a_fd; started 2026-11-05) unattended and refreshes the
# documents that show its results. Resumable: it starts at the first stage without a report, so a PC turned off
# mid-run loses only the stage that was running. Run inside the container, detached:
#   docker exec -d layout-s0s3 bash -lc "bash /foss/designs/scripts/finish_ttsky_v2.sh"
# Steps: S<first unfinished> .. S7 (runs/logs/gui_ttsky25a_fd_v2_finish.log), then
# docs/reports/ttsky25a_fd_v2_report.html, the README pictures (outputs/report/readme/) and docs/progress_report.*
# (runs/logs/finish_ttsky_v2_reports.log); runs/logs/finish_ttsky_v2.done marks the end. About 3.5 h from S1.
set -u
cd /foss/designs
D=ttsky25a_fd_v2
# a run started earlier in this container session (the S0-S3 chain of 2026-11-05) is waited for, not doubled
while pgrep -f "src.flow run $D" > /dev/null; do sleep 60; done
source scripts/env.sh
FROM=""
for s in S0 S1 S2 S3 S4 S5 S6 S7; do
  l=$(echo "$s" | tr 'S' 's')
  if [ ! -f "outputs/$s/$D/${l}_report.json" ]; then FROM=$s; break; fi
done
if [ -n "$FROM" ]; then
  python3 -u -m src.flow run $D --from $FROM > runs/logs/gui_${D}_finish.log 2>&1
  echo $? > runs/logs/gui_${D}_finish.log.exit
fi
{
  python3 scripts/make_design_report.py $D
  python3 scripts/make_readme_figures.py
  python3 scripts/make_progress_report.py
} > runs/logs/finish_ttsky_v2_reports.log 2>&1
date > runs/logs/finish_ttsky_v2.done
