#!/usr/bin/env sh
cd /opt/irrd/
python3 init-irrd.py \
&& irrd_database_upgrade
