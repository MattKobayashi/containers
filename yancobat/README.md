# YANCoBaT

YANCoBaT stands for 'Yet Another Network Configuration Backup Tool'. Because we don't have enough of 'em!

## Configuration

Create a GitHub repository for your network device backups. Add a `hosts.yaml` file with details of the devices to be backed up (use the example `hosts.yaml` in this repository to get started). The Docker image relies upon the presence of this file (with this exact name) in the repository to run the playbook successfully.

Set the following environment variables when creating your Docker container:

- `TZ=` Your preferred timezone, e.g. `Australia/Brisbane`
- `GIT_USER=` Your preferred user name for Git commits (optional, default: `YANCoBaT`).
- `GIT_EMAIL=` Your preferred user email for Git commits.
- `DEVICE_USER=` Your devices' SSH username for backups (recommended to be a locally-configured read-only user).
- `DEVICE_PASS=` Your devices' SSH password for backups (recommended to be a locally-configured read-only user). This value can also be passed as a Docker secret (highly recommended).
- `GITHUB_REPO=` The short-form name of your GitHub backups repository, e.g. `MattKobayashi/containers`.
- `GITHUB_TOKEN=` A GitHub personal access token with read-write permissions for your GitHub backups repository. This value can also be passed as a Docker secret (highly recommended).
- `NOTIFY_TELEGRAM=` Boolean flag for Telegram notifications (optional, default: `false`).
- `NOTIFY_TELEGRAM_TOKEN=` Your Telegram bot token (required if `NOTIFY_TELEGRAM=true`). This value can also be passed as a Docker secret (highly recommended).
- `NOTIFY_TELEGRAM_CHAT_ID=` Your Telegram chat ID (required if `NOTIFY_TELEGRAM=true`).
- `NOTIFY_SLACK=` Boolean flag for Slack notifications (optional, default: `false`).
- `NOTIFY_SLACK_TOKEN=` Your Slack bot token (required if `NOTIFY_SLACK=true`). This value can also be passed as a Docker secret (highly recommended).
- `NOTIFY_SLACK_CHANNEL=` Your Slack channel ID (required if `NOTIFY_SLACK=true`).

## Running

Simply start the container as a daemon:

`docker run -d --name yancobat -e 'ENV_VARS=whatever' ghcr.io/mattkobayashi/yancobat`

Or use the example `docker-compose.yml` from this repository to run as a Docker Compose project (recommended).
