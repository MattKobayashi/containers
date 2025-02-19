FROM python:3.13.2-alpine3.20@sha256:e885b40c1ed9f3134030e99a27bd61e98e376bf6d6709cccfb3c0aa6e856f56a

WORKDIR /opt/vyos-blog-alert

RUN apk --no-cache add supercronic \
	&& python3 -m pip install --break-system-packages feedparser

COPY main.py main.py
COPY crontab crontab

ENTRYPOINT ["/usr/bin/supercronic", "/opt/vyos-blog-alert/crontab"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
