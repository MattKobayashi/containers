FROM python:3.12.6-alpine3.20

WORKDIR /opt/growatt-ev/

RUN apk --no-cache upgrade \
	&& adduser --system growatt-ev \
	&& python3 -m pip install --break-system-packages paho-mqtt tuya-connector-python

COPY --chown=growatt-ev main.py main.py

USER growatt-ev

ENTRYPOINT ["python3", "-u", "main.py"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
