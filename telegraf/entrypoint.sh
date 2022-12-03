#!/bin/sh -e

if [ $# == 0 ] || [ "${1:0:1}" == "-" ]; then
  exec telegraf "$@"
else
  exec "$@"
fi
