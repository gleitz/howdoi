#!/bin/bash
# Setup a virtual environment for manual testing.
virtualenv --no-site-packages .env
. ./.env/bin/activate
pip install -U pip
pip install -r requirements.txt
