# verlihub

The `verlihub` DC++ hub server in a Debian-based Docker image.

## Prerequisites

- A MySQL/MariaDB server (this can also run in a Docker container)

## Configuration

This image is configured using environment variables and Docker secrets.

### Environment variables

|Variable name|Required?|Description|
|---|---|---|
|`MYSQL_DB_HOST`|✅|The hostname or IP address of the MySQL/MariaDB server|
|`MYSQL_DB_NAME`|❌|The name of the MySQL/MariaDB database to be created (defaults to `verlihub`)|
|`MYSQL_USER`|❌|The username of the database user with full permissions over the `MYSQL_DB_NAME` database (defaults to `verlihub`)|
|`VH_CONFIG_DIR`|❌|The directory where Verlihub stores configuration data (defaults to `/opt/verlihub/.config/verlihub`)|
|`VH_HUB_HOST`|✅|The hostname of the Verlihub server|
|`VH_HUB_PORT`|❌|The port that the Verlihub server runs on (defaults to `411` when `NET_BIND_SERVICE` capability is added, otherwise `4111`)|
|`VH_HUB_NAME`|❌|The name of the Verlihub server (defaults to `Verlihub`)|
|`VH_MASTER_NAME`|✅|The username of the master user on the Verlihub server|

### Secrets

|Secret name|Required?|Description|
|---|---|---|
|`MYSQL_PASSWORD`|✅|The password of the database user with full permissions over the `MYSQL_DB_NAME` database|
|`VH_MASTER_PASSWORD`|✅|The password of the master user on the Verlihub server|

## Running the container

Due to the use of Docker secrets, this container requires the use of Docker Compose. An example Compose file can be found in this repository, please use and modify it to suit your needs.
