#!/bin/sh

su bird -s /usr/bin/uv run fullbogons.py

cleanup() {
    echo "Shutting down BIRD..."
    birdc down & wait
}

trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

/usr/bin/supercronic /bird/crontab/fullbogons-cron &
bird -u bird -c bird.conf -d & wait $!
