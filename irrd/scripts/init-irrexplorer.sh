#!/usr/bin/env sh
cd /opt/irrexplorer/
/opt/irrexplorer/bin/poetry lock
/opt/irrexplorer/bin/poetry install
/opt/irrexplorer/bin/poetry add psycopg2@^2.9.9
/opt/irrexplorer/bin/poetry run python3 init-irrexplorer.py
/opt/irrexplorer/bin/poetry run frontend-install
/opt/irrexplorer/bin/poetry run frontend-build
/opt/irrexplorer/bin/poetry run alembic upgrade head
