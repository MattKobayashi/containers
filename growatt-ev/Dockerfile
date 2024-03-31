FROM python:3-alpine

WORKDIR /opt/growatt-ev/

RUN apk --no-cache upgrade \
	# && apk --no-cache add supercronic \
	&& adduser --system growatt-ev \
	# && python3 -m pip install --break-system-packages growattServer tuya-connector-python
	&& python3 -m pip install --break-system-packages paho-mqtt tuya-connector-python

COPY --chown=growatt-ev main2.py main.py

USER growatt-ev

ENTRYPOINT ["python3", "main.py"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
