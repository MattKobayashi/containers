#!/bin/sh

su bird -s /usr/bin/python3 fullbogons.py
exec bird -u bird -c bird.conf
