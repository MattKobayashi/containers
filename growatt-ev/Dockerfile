FROM python:3.13.3-alpine3.21@sha256:18159b2be11db91f84b8f8f655cd860f805dbd9e49a583ddaac8ab39bf4fe1a7

WORKDIR /opt/growatt-ev/

RUN adduser --system growatt-ev \
	&& apk --no-cache add py3-uv

COPY --chown=growatt-ev main.py main.py

USER growatt-ev

ENTRYPOINT ["/usr/bin/uv", "run", "main.py"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
