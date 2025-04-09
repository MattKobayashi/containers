FROM python:3.13.3-alpine3.20@sha256:cd01a123d91e75ac4fcfef154e746939687823112a055d9a3492c65d6768125c

WORKDIR /opt/vyos-blog-alert

RUN apk --no-cache add supercronic \
	&& python3 -m pip install --break-system-packages feedparser

COPY main.py main.py
COPY crontab crontab

ENTRYPOINT ["/usr/bin/supercronic", "/opt/vyos-blog-alert/crontab"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
