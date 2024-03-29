#!/bin/bash

if [ -f /run/secrets/TOKEN ]; then
	TOKEN=$(</run/secrets/TOKEN)
fi

REPOSITORY=$REPO
ACCESS_TOKEN=$TOKEN

echo "REPO ${REPOSITORY}"
echo "ACCESS_TOKEN ${ACCESS_TOKEN}"

REG_TOKEN=$(curl -X POST -H "Authorization: token ${ACCESS_TOKEN}" -H "Accept: application/vnd.github+json" https://api.github.com/repos/${REPOSITORY}/actions/runners/registration-token | jq .token --raw-output)

/actions-runner/config.sh --url https://github.com/${REPOSITORY} --token ${REG_TOKEN} --disableupdate

cleanup() {
    echo "Removing runner..."
    /actions-runner/config.sh remove --token ${REG_TOKEN}
}

trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

/actions-runner/run.sh & wait $!
