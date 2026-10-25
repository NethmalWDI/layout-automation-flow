#!/usr/bin/env bash
# gLayout in its own venv inside layout-s0s3 (container layer only). Run as root.
set -euxo pipefail
VENV=/opt/venv-glayout
[ -x $VENV/bin/python ] || python3 -m venv $VENV
$VENV/bin/pip install -q --upgrade pip setuptools wheel  # some glayout deps build from sdist
$VENV/bin/pip install -q "glayout==0.2.0"
chown -R 1000:1000 $VENV
$VENV/bin/pip freeze > /foss/designs/runs/env/requirements-glayout.lock.txt
$VENV/bin/python -c "import glayout, sys; print('glayout at', glayout.__file__)"
echo SETUP_GLAYOUT_DONE
