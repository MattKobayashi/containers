#!/bin/sh

/actions-runner/config.sh --url ${GITHUB_REPO_URL} --token ${GITHUB_TOKEN}
exec /actions-runner/run.sh
