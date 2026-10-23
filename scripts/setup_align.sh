#!/usr/bin/env bash
# Installs ALIGN into its own venv inside the layout-s0s3 container (not the image).
# Run as root: docker exec -u 0 layout-s0s3 bash /foss/designs/scripts/setup_align.sh
set -euxo pipefail
ALIGN_VERSION=0.9.8
PDK_REPO=https://github.com/ALIGN-analoglayout/ALIGN-pdk-sky130.git
PDK_COMMIT=${PDK_COMMIT:-main}
VENV=/opt/venv-align
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq coinor-libcgl1 coinor-libcbc3.1 coinor-libosi1v5 python3-dev  # python3-dev: gdspy (ALIGN dep) has no cp312 wheel and needs Python.h
[ -x $VENV/bin/python ] || python3 -m venv $VENV
$VENV/bin/pip install -q --upgrade pip
$VENV/bin/pip install -q "align-analoglayout==${ALIGN_VERSION}"
chown -R 1000:1000 $VENV
mkdir -p /foss/designs/external
if [ ! -d /foss/designs/external/ALIGN-pdk-sky130 ]; then
  git clone -q $PDK_REPO /foss/designs/external/ALIGN-pdk-sky130
fi
git config --global --add safe.directory /foss/designs/external/ALIGN-pdk-sky130
cd /foss/designs/external/ALIGN-pdk-sky130 && git checkout -q $PDK_COMMIT && git rev-parse HEAD > /foss/designs/runs/env/align_pdk_commit.txt
chown -R 1000:1000 /foss/designs/external/ALIGN-pdk-sky130 || true
$VENV/bin/pip freeze > /foss/designs/runs/env/requirements-align.lock.txt
$VENV/bin/schematic2layout.py -h | head -5
echo SETUP_ALIGN_DONE
