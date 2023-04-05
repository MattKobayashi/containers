#! /bin/sh -e

if [ -n ${DATABASE_URL} ]; then
	echo "Please set the DATABASE_URL environment variable. Exiting..."
	exit 1
else
	exec poetry run alembic
fi

if [ -n ${IRRD_ENDPOINT} ]; then
	echo "Please set the IRRD_ENDPOINT environment variable. Exiting..."
	exit 1
else
	exec poetry run http
fi
