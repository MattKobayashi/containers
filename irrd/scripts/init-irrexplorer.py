#!/usr/bin/env python3
import psycopg2
import time
import os
import yaml
from dotenv import set_key
from pathlib import Path

def execute_sql_command(host, admin_database, admin_user, admin_password, sql_command, max_retries=10, retry_interval=5):
    """Executes an SQL command (like CREATE DATABASE) on a PostgreSQL server,
       waiting for the database to be ready.

    Args:
        host: Hostname or IP of the PostgreSQL server.
        admin_database: Name of an existing database for the initial connection
                        (typically 'postgres' or a similar administrative database).
        admin_user: Username with sufficient privileges to create databases.
        admin_password: Password for the admin_user.
        sql_command: The SQL command to execute.
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
                host=host,
                database=admin_database,
                user=admin_user,
                password=admin_password
            )
            conn.set_session(autocommit=True)
            cur = conn.cursor()

            # Execute the SQL command
            cur.execute(sql_command)
            print("SQL command executed successfully.")
            return True

        except psycopg2.OperationalError as e:
            print(f"Database not ready yet. Retrying in {retry_interval} seconds... (Attempt {retries + 1}/{max_retries})")
            time.sleep(retry_interval)  # Wait before retrying
            retries += 1

        except psycopg2.errors.DuplicateDatabase as e:
            print("Database already exists, skipping...")
            return True

        except psycopg2.errors.DuplicateObject as e:
            print("Object already exists, skipping...")
            return True

    # Max retries reached
    print("Error: Database connection could not be established after multiple retries.")
    return False

# Example Usage (replace with your actual credentials and command)
with open("/etc/irrexplorer.yaml", "r") as yaml_conf:
    irrexplorer_conf = yaml.safe_load(yaml_conf)

host = irrexplorer_conf["irrexplorer"]["database_url"].split("/")[2].split("@")[1]
admin_database = irrexplorer_conf["irrexplorer"]["admin_database"]
admin_user = irrexplorer_conf["irrexplorer"]["admin_user"]
admin_password = irrexplorer_conf["irrexplorer"]["admin_password"]
database = irrexplorer_conf["irrexplorer"]["database_url"].split("/")[3]
user = irrexplorer_conf["irrexplorer"]["database_url"].split("/")[2].split("@")[0].split(":")[0]
password = irrexplorer_conf["irrexplorer"]["database_url"].split("/")[2].split("@")[0].split(":")[1]

# Create the database first
sql_command = f"""
CREATE DATABASE {database};
"""
execute_sql_command(host, admin_database, admin_user, admin_password, sql_command)

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
