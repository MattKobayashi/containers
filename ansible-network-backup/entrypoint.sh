#!/bin/sh

ansible-playbook /ansible/clone-repo.yaml
exec supercronic /ansible/crontab/ansible-cron
