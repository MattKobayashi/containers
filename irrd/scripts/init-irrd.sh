#!/usr/bin/env sh
cd /opt/irrd/
/opt/irrd/irrd-venv/bin/python3 init-irrd.py
/opt/irrd/irrd-venv/bin/irrd_database_upgrade
