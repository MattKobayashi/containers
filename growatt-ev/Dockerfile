FROM python:3-alpine

WORKDIR /opt/growatt-ev/

RUN apk --no-cache upgrade \
	&& apk --no-cache add supercronic \
	&& adduser --system growatt-ev \
	&& python3 -m pip install --break-system-packages growattServer tuya-connector-python

COPY --chown=growatt-ev main.py main.py
COPY --chown=growatt-ev crontab crontab

USER growatt-ev

ENTRYPOINT ["supercronic", "/opt/growatt-ev/crontab"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
