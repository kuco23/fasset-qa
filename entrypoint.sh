#!/bin/sh
set -e

chown -R 0:0 /app/fasset-bots-config/users/**/*secrets.json
python -u -m cli "$@"