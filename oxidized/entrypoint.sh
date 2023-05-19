#!/bin/sh -e

if [ ! "${OX_DEVICE_USER+set}" = set ]; then
	echo "Please set the OX_DEVICE_USER environment variable. Exiting..."
	exit 1
else
	yq -i '.username = strenv(OX_DEVICE_USER)' /home/oxidized/.config/oxidized/config
fi

if [ ! "${OX_DEVICE_PASS+set}" = set ]; then
	echo "Please set the OX_DEVICE_PASS environment variable. Exiting..."
	exit 1
else
	yq -i '.password = strenv(OX_DEVICE_PASS)' /home/oxidized/.config/oxidized/config
fi

if [ ! "${OX_ROUTER_DB+set}" = set ]; then
	yq -i '.source.csv.file = "/home/oxidized/.config/oxidized/router.db"' /home/oxidized/.config/oxidized/config
else
	yq -i '.source.csv.file = strenv(OX_ROUTER_DB)' /home/oxidized/.config/oxidized/config
fi

if [ ! "${OX_GIT_REPO_DIR+set}" = set ]; then
	yq -i '.output.git.repo = "/home/oxidized/backups"' /home/oxidized/.config/oxidized/config
else
	yq -i '.output.git.repo = strenv(OX_GIT_REPO_DIR)' /home/oxidized/.config/oxidized/config
fi

if [ ! "${OX_GIT_USER+set}" = set ]; then
	echo "Please set the OX_GIT_USER environment variable. Exiting..."
	exit 1
else
	yq -i '.output.git.user = strenv(OX_GIT_USER)' /home/oxidized/.config/oxidized/config
fi

if [ ! "${OX_GIT_EMAIL+set}" = set ]; then
	echo "Please set the OX_GIT_EMAIL environment variable. Exiting..."
	exit 1
else
	yq -i '.output.git.email = strenv(OX_GIT_EMAIL)' /home/oxidized/.config/oxidized/config
fi

if [ ! "${OX_GITHUB_USER+set}" = set ]; then
	echo "Please set the OX_GITHUB_USER environment variable. Exiting..."
	exit 1
else
	yq -i '.hooks.push_to_remote.username = strenv(OX_GITHUB_USER)' /home/oxidized/.config/oxidized/config
fi

if [ ! "${OX_GITHUB_TOKEN+set}" = set ]; then
	echo "Please set the OX_GITHUB_TOKEN environment variable. Exiting..."
	exit 1
else
	yq -i '.hooks.push_to_remote.password = strenv(OX_GITHUB_TOKEN)' /home/oxidized/.config/oxidized/config
fi

if [ ! "${OX_GITHUB_ORG+set}" = set ]; then
	echo "Please set the OX_GITHUB_ORG environment variable. Exiting..."
	exit 1
fi

if [ ! "${OX_GITHUB_REPO+set}" = set ]; then
	echo "Please set the OX_GITHUB_REPO environment variable. Exiting..."
	exit 1
else
	export OX_GITHUB_URL="https://github.com/${OX_GITHUB_ORG}/${OX_GITHUB_REPO}.git"
	export OX_GITHUB_AUTH_URL="https://${OX_GITHUB_TOKEN}@github.com/${OX_GITHUB_ORG}/${OX_GITHUB_REPO}.git"
	yq -i '.hooks.push_to_remote.remote_repo = strenv(OX_GITHUB_URL)' /home/oxidized/.config/oxidized/config
fi

if [ "${OX_CONFIG_RELOAD_INTERVAL+set}" = set ]; then
	yq -i '.interval = env(OX_CONFIG_RELOAD_INTERVAL)' /home/oxidized/.config/oxidized/config
fi

[ -f /home/oxidized/.config/oxidized/pid ] && rm /home/oxidized/.config/oxidized/pid

git clone ${OX_GITHUB_AUTH_URL} ${OX_GIT_REPO_DIR} && exec oxidized
