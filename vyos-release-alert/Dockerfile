FROM python:3.12.7-alpine3.20

WORKDIR /opt/vyos-blog-alert

RUN apk --no-cache add supercronic \
	&& python3 -m pip install --break-system-packages feedparser

COPY main.py main.py
COPY crontab crontab

ENTRYPOINT ["/usr/bin/supercronic", "/opt/vyos-blog-alert/crontab"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
