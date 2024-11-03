#!/bin/bash
pip-compile --upgrade --strip-extras
pip-compile --upgrade --strip-extras requirements-dev.in
./sync_dependencies.sh
