#!/bin/bash
# Initialize a Python 3.12 virtual environment
# Usage: ./init_virtualenv.sh [venv_path]
# Default venv_path is .venv

VENV_PATH="${1:-.venv}"

[ -d "$VENV_PATH" ] && rm -Rf "$VENV_PATH"
python3.12 -m venv "$VENV_PATH"
. "$VENV_PATH/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-test.txt
