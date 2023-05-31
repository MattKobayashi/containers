#!/bin/sh

if [ -f /run/secrets/GITHUB_TOKEN ]; then
	GITHUB_TOKEN=$(</run/secrets/GITHUB_TOKEN)
fi

ansible-playbook /ansible/clone-repo.yaml
exec supercronic /ansible/crontab/ansible-cron
