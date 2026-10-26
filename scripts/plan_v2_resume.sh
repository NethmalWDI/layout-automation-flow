#!/usr/bin/env bash
# Plan v2: every run still to do, resumable (written 2026-10-27 01:05 for the overnight stop and the move to
# Claude Code; see docs/HANDOFF.md).
#
# Each step writes runs/state/plan_v2/<step>.done when it finishes. A step with a .done marker is skipped,
# so the script can be stopped at any time (PC off, container stopped) and started again: an interrupted
# step simply runs again from its start. A `flow run` step counts as done when it finished (PASS or FAIL,
# rc 0 or 1); a crash (ERROR, rc 2) is not marked and stops that lane.
#
# Run inside the container, from the repo root, detached (it takes about 5-6 hours):
#   docker exec -d layout-s0s3 bash -lc "cd /foss/designs && bash scripts/plan_v2_resume.sh > runs/logs/plan_v2_resume.log 2>&1"
# Progress: tail runs/logs/plan_v2_resume.log runs/logs/plan_v2_lane_A.log runs/logs/plan_v2_lane_B.log ;
#           ls runs/state/plan_v2/
# Stop cleanly: see docs/HANDOFF.md ("Before switching the PC off").
#
# Lanes A and B run side by side with 2 ngspice workers each (the container has 4 cores); the final part
# (eta 0.9, golden snapshots, report) waits for both.
set -u
cd /foss/designs && source scripts/env.sh
ST=runs/state/plan_v2
mkdir -p "$ST" runs/tmp/aside
W=${W:-2}

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
  step "$1_after_pvt" python3 -m src.s0.pvt "inputs/$1/package.yaml" --workers $W || return 1
  fstep "$1_after_S2S3" "$1" --from S2 --workers $W || return 1
  snap "$1" after
}
restore_aside() {   # put back outputs set aside by an interrupted ablation / eta step
  local d=$1
  if [ -d runs/tmp/aside/$d/S2 ]; then
    echo "    restoring the after outputs of $d set aside by an interrupted step"
    rm -rf outputs/S2/$d outputs/S3/$d
    mv runs/tmp/aside/$d/S2 outputs/S2/$d && mv runs/tmp/aside/$d/S3 outputs/S3/$d
    rm -rf runs/tmp/aside/$d
  fi
}
aside() {     # aside <design>: keep the after outputs safe while a variant overwrites them
  local d=$1
  rm -rf runs/tmp/aside/$d && mkdir -p runs/tmp/aside/$d
  cp -a outputs/S2/$d runs/tmp/aside/$d/S2 && cp -a outputs/S3/$d runs/tmp/aside/$d/S3
}

lane_A() {
  # iadc_ota: 'before' S3 (v1) and its snapshot, then 'after'; loadbench 'after'; the hand-drawn iadc layout
  # (C only) against the after-run G2.0; the no-PVT ablation of the two 5T designs.
  fstep iadc_before_S3 iadc_ota --stage S3 --variant v1 --workers $W && snap iadc_ota before || return 1
  after loadbench_miller
  after iadc_ota
  step ref_iadc_final bash scripts/reference_iadc.sh
  for d in example_ota_5t ota5t_stress; do
    restore_aside $d
    if [ ! -f "$ST/snap_${d}_after_nopvt.done" ]; then
      aside $d
      step abl_nopvt_${d}_S2 python3 -m src.s2.run inputs/$d/package.yaml --workers $W --no-pvt --no-baselines
      step abl_nopvt_${d}_S3 python3 -m src.s3.run inputs/$d/package.yaml --workers $W
      snap $d after_nopvt
      rm -f "$ST/abl_nopvt_${d}_S2.done" "$ST/abl_nopvt_${d}_S3.done"
      restore_aside $d
    fi
  done
}

lane_B() {
  # ttsky25a_fd: 'before' from S2 (v1; S1 with the L-ratioed mirror fix finished on 2026-10-26), its
  # snapshot, 'after', the hand-drawn tile (C only, three condition sets), then the tile's R+C extraction.
  fstep ttsky_before_S2S3 ttsky25a_fd --from S2 --variant v1 --workers $W && snap ttsky25a_fd before || return 1
  after ttsky25a_fd
  step ref_ttsky_final bash scripts/reference_ttsky25a.sh
  G=circuits/ttsky25a_fd/upstream_src/gds/tt_um_diff.gds
  P="ena=VSS,ua[1]=INP,ua[2]=INN,ua[4]=OUTP,ua[5]=OUTN,ua[0]=VREF,ua[3]=RGM,VDPWR=VDD,VGND=VSS,ui_in[0]=EN1,ui_in[1]=EN2"
  B="Rgm_ext RGM VSS 12k;Vref_ext VREF VSS 0.9;Ven1 EN1 VSS 1.8;Ven2 EN2 VSS 0"
  step ref_ttsky_rc bash -c "ulimit -v 3000000; python3 scripts/reference_layout.py ttsky25a_fd $G tt_um_diff --skip-extract \
      --ports '$P' --bias '$B' --rc --rc-tol 100 --map-shorted --tag rc100s"
}

echo "##### plan v2 resume $(date '+%F %T'); done so far: $(ls $ST 2>/dev/null | tr '\n' ' ')"
lane_A > runs/logs/plan_v2_lane_A.log 2>&1 &
PA=$!
lane_B > runs/logs/plan_v2_lane_B.log 2>&1 &
PB=$!
wait $PA; echo "lane A ended rc=$? $(date '+%T')"
wait $PB; echo "lane B ended rc=$? $(date '+%T')"

# PREREG headline: S2 (SPICE-scored baselines) at eta = 0.9 for every design, snapped as 'after_eta0.9'.
# S3 is not re-run (the snapshot shows it as not run); the after outputs are set aside and restored.
for d in example_ota_5t ota5t_stress loadbench_miller iadc_ota ttsky25a_fd; do
  restore_aside $d
  [ -f "$ST/snap_${d}_after_eta0.9.done" ] && { echo "--- skip eta 0.9 $d"; continue; }
  [ -f "$ST/snap_${d}_after.done" ] || { echo "--- eta 0.9 $d: no after run yet"; continue; }
  aside $d
  rm -rf outputs/S3/$d
  step eta9_${d}_S2 python3 -m src.s2.run inputs/$d/package.yaml --workers 4 --eta 0.9
  snap $d after_eta0.9
  rm -f "$ST/eta9_${d}_S2.done"
  restore_aside $d
done

# golden snapshots of the v2 'after' outputs (tests/golden/), only when every after run is in
if ls "$ST"/snap_{example_ota_5t,ota5t_stress,loadbench_miller,iadc_ota,ttsky25a_fd}_after.done >/dev/null 2>&1; then
  for d in example_ota_5t ota5t_stress loadbench_miller iadc_ota ttsky25a_fd; do
    step golden_$d python3 -m src.flow snapshot $d
  done
fi
python3 scripts/compare_before_after.py report
echo "##### plan v2 resume ended $(date '+%F %T'); done: $(ls $ST | wc -l) steps"
