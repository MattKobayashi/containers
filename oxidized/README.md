# Oxidized

Oxidized in an Alpine-based Docker image. Small, lightweight and (most importantly) up-to-date with source.

## Configuration

Set the following environment variables when creating your Docker container:

- OX_DEVICE_USER: The username used to SSH into a device being backed up.
- OX_DEVICE_PASS: The password used to SSH into a device being backed up.
- OX_ROUTER_DB: The path to the router.db file (optional, default: `/home/oxidized/.config/oxidized/router.db`).
- OX_GIT_REPO_DIR: The path to the local Git repository (optional, default: `/home/oxidized/backups`).
- OX_GIT_USER: The name used for the local Git repository user.
- OX_GIT_EMAIL: The email address used for the local Git repository user.
- OX_GITHUB_USER: Your GitHub username.
- OX_GITHUB_TOKEN: Your GitHub Personal Access Token.
- OX_GITHUB_ORG: Your GitHub organisation.
- OX_GITHUB_REPO: The name of the remote repository on GitHub (not including the organisation name).
- OX_CONFIG_RELOAD_INTERVAL: The interval, in seconds, between reloads of device configurations (optional, default: 3600),

## Running

Simply start the daemon:

`docker run -d --name oxidized --volume /path/to/oxidized/data:/home/oxidized/.config/oxidized --port 8888:8888/tcp ghcr.io/mattkobayashi/oxidized`

## Explanatory notes

- None!