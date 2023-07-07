#!/bin/sh

su bird -s /usr/bin/python3 fullbogons.py

cleanup() {
    echo "Shutting down BIRD..."
    birdc down
}

trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

bird -u bird -c bird.conf -d & wait $!
