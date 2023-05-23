# ansible-network-backup

A customised Ansible network backup playbook in an Alpine-based Docker image. Small, lightweight and (most importantly) up-to-date with source.

## Configuration

Create a GitHub repository for your network device backups. Add a `hosts.yaml` file with details of the devices to be backed up (use the example `hosts.yaml` in this repository to get started). The Docker image relies upon the presence of this file (with this exact name) in the repository to run the playbook successfully.

Set the following environment variables when creating your Docker container:

- `TZ=` Your preferred timezone, e.g. `Australia/Brisbane`
- `GIT_USER=` Your preferred user name for Git commits (optional, default: `Ansible`)
- `GIT_EMAIL=` Your preferred user email for Git commits
- `DEVICE_USER=` Your devices' SSH username for backups (recommended to be a read-only user)
- `DEVICE_PASS=` Your devices' SSH password for backups (recommended to be a read-only user)
- `GITHUB_REPO=` The short-form name of your GitHub backups repository, e.g. `MattKobayashi/containers`
- `GITHUB_TOKEN=` A GitHub personal access token with read-write permissions for your GitHub backups repository

## Running

Simply start the container as a daemon:

`docker run -d --name ansible-network-backup -e 'ENV_VARS=whatever' ghcr.io/mattkobayashi/ansible-network-backup`

Or use the example `docker-compose.yml` from this repository to run as a Docker Compose project (recommended).