FROM python:3.13.2-alpine3.20

WORKDIR /opt/growatt-ev/

RUN adduser --system growatt-ev \
	&& python3 -m pip install --break-system-packages paho-mqtt tuya-connector-python

COPY --chown=growatt-ev main.py main.py

USER growatt-ev

ENTRYPOINT ["python3", "-u", "main.py"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
