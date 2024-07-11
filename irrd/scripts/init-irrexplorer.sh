#!/usr/bin/env sh
cd /opt/irrexplorer/
/usr/bin/poetry install
/usr/bin/poetry add psycopg2@^2.9.9
/usr/bin/poetry run python3 init-irrexplorer.py
/usr/bin/poetry run frontend-install
/usr/bin/poetry run frontend-build
/usr/bin/poetry run alembic upgrade head
