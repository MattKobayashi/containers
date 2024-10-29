#!/usr/bin/env python3
"""Script to initialize the IRR Explorer database."""

import time
import sys
from pathlib import Path
import psycopg2
import yaml
from dotenv import set_key


def execute_sql_command(
    db_host, db_admin_database, db_admin_user, db_admin_password, sql_cmd, max_retries=10, retry_interval=5
):
    """Executes an SQL command (like CREATE DATABASE) on a PostgreSQL server,
       waiting for the database to be ready.

    Args:
        host: Hostname or IP of the PostgreSQL server.
        admin_db: Name of an existing database for the initial connection
            (typically 'postgres' or a similar administrative database).
        db_admin_user: Username with sufficient privileges to create databases.
        db_admin_password: Password for the admin_user.
        sql_cmd: The SQL command to execute.
        max_retries: Maximum number of connection attempts (default 10).
        retry_interval: Time in seconds between retries (default 5).

    Returns:
        True if successful, False otherwise. Prints informative messages.
    """

    retries = 0
    while retries < max_retries:
        try:
            # Attempt connection to the admin database
            conn = psycopg2.connect(
                host=db_host, database=db_admin_database, user=db_admin_user, password=db_admin_password
            )
            conn.set_session(autocommit=True)
            cur = conn.cursor()

            # Execute the SQL command
            cur.execute(sql_cmd)
            print("SQL command executed successfully.")
            return True

        except psycopg2.OperationalError:
            print(
                f"Database not ready yet. Retrying in {retry_interval} "
                f"seconds...\n(Attempt {retries + 1}/{max_retries})"
            )
            time.sleep(retry_interval)  # Wait before retrying
            retries += 1

        except psycopg2.errors.DuplicateDatabase:
            print("Database already exists, skipping...")
            return True

        except psycopg2.errors.DuplicateObject:
            print("Object already exists, skipping...")
            return True

    # Max retries reached
    print("Error: Database connection could not be established after multiple " "retries.")
    return False


try:
    with open("/etc/irrexplorer.yaml", "r", encoding="utf-8") as yaml_conf:
        irrexplorer_conf = yaml.safe_load(yaml_conf)
except FileNotFoundError:
    print("Error: Configuration file /etc/irrexplorer.yaml not found.")
    sys.exit(1)

db_url = irrexplorer_conf["irrexplorer"]["database_url"]
host = db_url.split("/")[2].split("@")[1]
admin_database = irrexplorer_conf["irrexplorer"]["admin_database"]
admin_user = irrexplorer_conf["irrexplorer"]["admin_user"]
admin_password = irrexplorer_conf["irrexplorer"]["admin_password"]
database = irrexplorer_conf["irrexplorer"]["database_url"].split("/")[3]
db_url_parts = irrexplorer_conf["irrexplorer"]["database_url"].split("/")
db_user_info = db_url_parts[2].split("@")[0].split(":")
user = db_user_info[0]
password = db_user_info[1]

# Create the database first
sql_command = f"""
CREATE DATABASE {database};
"""
execute_sql_command(
    db_host=host,
    db_admin_database=admin_database,
    db_admin_user=admin_user,
    db_admin_password=admin_password,
    sql_cmd=sql_command,
)

# Do the rest
sql_command = f"""
CREATE ROLE {user} WITH LOGIN ENCRYPTED PASSWORD '{password}';
GRANT ALL PRIVILEGES ON DATABASE {database} TO {user};
GRANT ALL ON SCHEMA public TO {user};
"""
execute_sql_command(host, database, admin_user, admin_password, sql_command)

# Export environment variables
env_file = Path("/opt/irrexplorer/.env")
env_file.touch(mode=0o600, exist_ok=True)
set_key(dotenv_path=env_file, key_to_set="DATABASE_URL", value_to_set=irrexplorer_conf["irrexplorer"]["database_url"])
set_key(dotenv_path=env_file, key_to_set="IRRD_ENDPOINT", value_to_set=irrexplorer_conf["irrexplorer"]["irrd_endpoint"])

# Create supercronic file
cron_file = Path("/opt/irrexplorer/cron/import-data")
cron_file.touch(mode=0o600, exist_ok=True)
cron_file.write_text(
    f"{irrexplorer_conf['irrexplorer']['import_data_cron']} /opt/irrexplorer/bin/poetry run import-data\n",
    encoding="utf-8",
)
