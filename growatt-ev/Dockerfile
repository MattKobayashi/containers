FROM python:3.13.2-alpine3.21@sha256:323a717dc4a010fee21e3f1aac738ee10bb485de4e7593ce242b36ee48d6b352

WORKDIR /opt/growatt-ev/

RUN adduser --system growatt-ev \
	&& apk --no-cache add py3-uv

COPY --chown=growatt-ev main.py main.py

USER growatt-ev

ENTRYPOINT ["/usr/bin/uv", "run", "main.py"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
