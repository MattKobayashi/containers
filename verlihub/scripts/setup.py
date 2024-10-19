#!/usr/bin/env python3
"""Script for initialising the Verlihub server."""
import mysql.connector
from mysql.connector import Error
import os
import sys
import time


def create_connection(host_name, user_name, user_password, db_name):
    """Creates a connection to the MySQL database."""
    new_connection = None
    try:
        new_connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return new_connection


def execute_query(query_connection, query):
    """Executes a query on the database."""
    cursor = query_connection.cursor()
    try:
        cursor.execute(query)
        query_connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def generate_config_file(file_path):
    """Generates a configuration file with predefined contents."""
    config_content = f"""
db_host = {VH_MYSQL_DB_HOST}
db_data = {VH_MYSQL_DB_NAME}
db_user = {VH_MYSQL_USER}
db_pass = {VH_MYSQL_PASSWORD}
db_charset = utf8mb4
        """
    try:
        with open(file_path, 'w', encoding='utf-8') as config_file:
            config_file.write(config_content)
        print(f"Configuration file created at {file_path}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")


# Get the configuration from environment variables and secrets
try:
    VH_MYSQL_DB_HOST = os.environ['MYSQL_DB_HOST']
    VH_MYSQL_DB_NAME = os.environ.get('MYSQL_DB_NAME', 'verlihub')
    VH_MYSQL_USER = os.environ.get('MYSQL_USER', 'verlihub')
    try:
        with open(
            '/run/secrets/VH_MYSQL_PASSWORD', 'r', encoding='utf-8'
        ) as file:
            VH_MYSQL_PASSWORD = file.read().strip()
    except FileNotFoundError:
        print("VH_MYSQL_PASSWORD secret not found.")
        sys.exit(1)
    VH_HUB_CONFIG_DIR = os.environ.get(
        'VH_HUB_CONFIG_DIR', '/opt/verlihub/.config/verlihub'
    ).rstrip('/')
    VH_HUB_HOST = os.environ['VH_HUB_HOST']
    VH_HUB_PORT = os.environ.get('VH_HUB_PORT', '411')
    VH_HUB_NAME = os.environ.get('VH_HUB_NAME', 'Verlihub')
    VH_HUB_MASTER_NAME = os.environ['VH_HUB_MASTER_NAME']
    try:
        with open(
            '/run/secrets/VH_HUB_MASTER_PASSWORD', 'r', encoding='utf-8'
        ) as file:
            VH_HUB_MASTER_PASSWORD = file.read().strip()
    except FileNotFoundError:
        print("VH_HUB_MASTER_PASSWORD secret not found.")
        sys.exit(1)
except KeyError:
    print("One or more environment variables not set.")
    sys.exit(1)

# Connect to the MySQL database
connection = create_connection(
    VH_MYSQL_DB_HOST, VH_MYSQL_USER, VH_MYSQL_PASSWORD, VH_MYSQL_DB_NAME
)

# Generate the configuration file
generate_config_file(VH_CONFIG_DIR + "/dbconfig")

# Define the configuration queries
config_queries = [
    f"CREATE TABLE IF NOT EXISTS {VH_MYSQL_DB_NAME}.SetupList (file varchar(30), var varchar(50), val text, primary key(file, var));",
    f"UPDATE SetupList SET val='{VH_HUB_HOST}:{VH_HUB_PORT}' WHERE var='hub_host';",
    f"UPDATE SetupList SET val='{VH_HUB_PORT}' WHERE var='listen_port';"
]

# Execute the configuration queries
for query in config_queries:
    execute_query(connection, query)

# Create the master user
master_query = f"""
INSERT INTO reglist (nick, class, login_pwd, pwd_change, pwd_crypt) VALUES ('{VH_HUB_MASTER_NAME}', 10, '{VH_HUB_MASTER_PASSWORD}', 0, 0);
"""
execute_query(connection, master_query)

# Import the contents of default_reglist.sql
try:
    with open(
        '/opt/verlihub/sql/default_reglist.sql',
        'r',
        encoding='utf-8'
    ) as sql_file:
        sql_script = sql_file.read()
        cursor = connection.cursor()
        cursor.execute(sql_script)
        connection.commit()
except IOError as e:
    print(f"An error occurred while reading the file: {e}")
except Error as e:
    print(f"The error '{e}' occurred")

# Export the configuration directory as an environment variable
try:
    with open('/opt/verlihub/verlihub.env', 'w', encoding='utf-8') as file:
        file.write(f"VERLIHUB_CFG={VH_HUB_CONFIG_DIR}")
except IOError as e:
    print(f"An error occurred while writing to the file: {e}")
