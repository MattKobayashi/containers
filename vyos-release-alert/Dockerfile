FROM python:3.13.3-alpine3.20@sha256:8ef4cefd6d7cc74633d7f30de2ef342e32ec8bfd74bcb29bc0e8cd56ac2593c9

WORKDIR /opt/vyos-blog-alert

RUN apk --no-cache add supercronic \
	&& python3 -m pip install --break-system-packages feedparser

COPY main.py main.py
COPY crontab crontab

ENTRYPOINT ["/usr/bin/supercronic", "/opt/vyos-blog-alert/crontab"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
