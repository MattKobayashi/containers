FROM python:3-alpine

RUN apk --no-cache upgrade \
	&& apk --no-cache add poetry git docker-cli-compose bash

WORKDIR /opt/peeringdb-mirror/

COPY pyproject.toml /opt/peeringdb-mirror/pyproject.toml
COPY --chmod=0755 entrypoint.sh /opt/peeringdb-mirror/entrypoint.sh
COPY config.yaml /opt/peeringdb-mirror/.peeringdb/config.yaml

ENTRYPOINT ["/opt/peeringdb-mirror/entrypoint.sh"]

EXPOSE 8000/tcp

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
