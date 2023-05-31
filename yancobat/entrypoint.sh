#!/bin/sh

if [ -f /run/secrets/DEVICE_PASS ]; then
	export DEVICE_PASS=$(</run/secrets/DEVICE_PASS)
fi

if [ -f /run/secrets/GITHUB_TOKEN ]; then
	export GITHUB_TOKEN=$(</run/secrets/GITHUB_TOKEN)
fi

if [ -f /run/secrets/NOTIFY_TELEGRAM_TOKEN ]; then
	export NOTIFY_TELEGRAM_TOKEN=$(</run/secrets/NOTIFY_TELEGRAM_TOKEN)
fi

if [ -f /run/secrets/NOTIFY_SLACK_TOKEN ]; then
	export NOTIFY_SLACK_TOKEN=$(</run/secrets/NOTIFY_SLACK_TOKEN)
fi

ansible-playbook /ansible/clone-repo.yaml
exec supercronic /ansible/crontab/ansible-cron
