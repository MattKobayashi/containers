FROM python:3.13.3-alpine3.21@sha256:7ce9864f2f4181df6ad32ea6625fb80bee3031d679faec6015623525ba753706

WORKDIR /opt/growatt-ev/

RUN adduser --system growatt-ev \
	&& apk --no-cache add py3-uv

COPY --chown=growatt-ev main.py main.py

USER growatt-ev

ENTRYPOINT ["/usr/bin/uv", "run", "main.py"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
