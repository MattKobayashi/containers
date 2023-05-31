#!/bin/sh

if [ -f /run/secrets/GITHUB_TOKEN ]; then
	GITHUB_TOKEN=$(</run/secrets/GITHUB_TOKEN)
fi

if [ -f /run/secrets/NOTIFY_TELEGRAM_TOKEN ]; then
	NOTIFY_TELEGRAM_TOKEN=$(</run/secrets/NOTIFY_TELEGRAM_TOKEN)
fi

if [ -f /run/secrets/NOTIFY_SLACK_TOKEN ]; then
	NOTIFY_SLACK_TOKEN=$(</run/secrets/NOTIFY_SLACK_TOKEN)
fi

ansible-playbook /ansible/clone-repo.yaml
exec supercronic /ansible/crontab/ansible-cron
