#!/usr/bin/env python3
"""Script for initialising the Verlihub server."""
import os
import sys
import mysql.connector
from mysql.connector import Error


def execute_query(query_connection, query):
    """Executes a query on the database."""
    cursor = query_connection.cursor()
    try:
        cursor.execute(query)
        query_connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# Get the configuration from environment variables and secrets
try:
    VH_MYSQL_DB_HOST = os.environ['VH_MYSQL_DB_HOST']
    VH_MYSQL_DB_NAME = os.environ.get('VH_MYSQL_DB_NAME', 'verlihub')
    VH_MYSQL_USER = os.environ.get('VH_MYSQL_USER', 'verlihub')
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
    VH_HUB_PORT = os.environ.get('VH_HUB_PORT', '4111')
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
try:
    connection = mysql.connector.connect(
        host=VH_MYSQL_DB_HOST,
        user=VH_MYSQL_USER,
        passwd=VH_MYSQL_PASSWORD,
        database=VH_MYSQL_DB_NAME,
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
    print("Connection to MySQL DB successful")
except mysql.connector.Error as e:
    print(f"The error '{e}' occurred")
    sys.exit(1)

# Define the configuration queries
config_queries = [
    f"""CREATE TABLE IF NOT EXISTS {VH_MYSQL_DB_NAME}.SetupList (
        file varchar(30),
        var varchar(50),
        val text,
        PRIMARY KEY(file, var)
    );""",
    f"UPDATE SetupList SET val='{VH_HUB_HOST}:{VH_HUB_PORT}' WHERE var='hub_host';",
    f"UPDATE SetupList SET val='{VH_HUB_PORT}' WHERE var='listen_port';",
    f"""CREATE TABLE IF NOT EXISTS {VH_MYSQL_DB_NAME}.reglist (
        nick varchar(64) NOT NULL,
        class int(2) DEFAULT 1,
        class_protect int(2) DEFAULT 0,
        class_hidekick int(2) DEFAULT 0,
        hide_kick tinyint(1) DEFAULT 0,
        hide_keys tinyint(1) DEFAULT 0,
        show_keys tinyint(1) DEFAULT 0,
        hide_share tinyint(1) DEFAULT 0,
        hide_chat tinyint(1) DEFAULT 0,
        hide_ctmmsg tinyint(1) DEFAULT 0,
        reg_date int(11),
        reg_op varchar(64),
        pwd_change tinyint(1) DEFAULT 1,
        pwd_crypt tinyint(1) DEFAULT 1,
        login_pwd varchar(60),
        login_last int(11) DEFAULT 0,
        logout_last int(11) DEFAULT 0,
        login_cnt int(11) DEFAULT 0,
        login_ip varchar(15),
        error_last int(11),
        error_cnt int(11) DEFAULT 0,
        error_ip varchar(15),
        enabled tinyint(1) DEFAULT 1,
        note_op varchar(255),
        note_usr varchar(255),
        auth_ip varchar(15),
        alternate_ip varchar(15),
        fake_ip varchar(15),
        PRIMARY KEY(nick),
        INDEX login_index (login_last),
        INDEX logout_index (logout_last)
    );"""
]

# Execute the configuration queries
for config_query in config_queries:
    execute_query(connection, config_query)

# Create the master user
master_query = f"""
INSERT INTO reglist (nick, class, login_pwd, pwd_change, pwd_crypt) VALUES ('{VH_HUB_MASTER_NAME}', 10, '{VH_HUB_MASTER_PASSWORD}', 0, 0);
"""
execute_query(connection, master_query)

# Import the contents of default_reglist.sql
try:
    with open(
        '/usr/local/share/verlihub/sql/default_reglist.sql',
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

# Close the MySQL database connection
connection.close()

# Generate the configuration file
try:
    with open(
        VH_HUB_CONFIG_DIR + "/dbconfig",
        'w',
        encoding='utf-8'
    ) as config_file:
        config_content = f"""
db_host = {VH_MYSQL_DB_HOST}
db_data = {VH_MYSQL_DB_NAME}
db_user = {VH_MYSQL_USER}
db_pass = {VH_MYSQL_PASSWORD}
db_charset = utf8mb4
        """
        config_file.write(config_content)
    print(f"Configuration file created at {VH_HUB_CONFIG_DIR}/dbconfig")
except IOError as e:
    print(
        "An error occurred while writing to the file",
        f"{VH_HUB_CONFIG_DIR}/dbconfig: {e}"
    )

# Export the configuration directory as an environment variable
try:
    with open('/opt/verlihub/verlihub.env', 'w', encoding='utf-8') as env_file:
        env_file.write(f"VERLIHUB_CFG={VH_HUB_CONFIG_DIR}")
    print("Environment file created at /opt/verlihub/verlihub.env")
except IOError as e:
    print(
        "An error occurred while writing to the file",
        f"/opt/verlihub/verlihub.env: {e}"
    )
