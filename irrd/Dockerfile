FROM pypy:3-slim

ENV SOURCE_FILE=irrexplorer.tar.gz \
    SOURCE_URL=https://github.com/NLNOG/irrexplorer/archive/c4eb6599c1bd359f1464834bf5e07828aec1769a.tar.gz \
    SOURCE_SHA1SUM=cd031821503510b35346be06f9f38dc736c9ff2a

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y build-essential sudo postgresql redis \
    && adduser --gecos '' --disabled-password irrd \
    && adduser --gecos '' --disabled-password irrexplorer \
    && pip install --upgrade pip \
    && su -c 'pip install irrd' irrd

WORKDIR /opt/irrexplorer

RUN wget -O "$SOURCE_FILE" "$SOURCE_URL" \
    && echo "${SOURCE_SHA1SUM}  ${SOURCE_FILE}" | sha1sum -c - \
    && tar -xz --strip-components=1 --file="$SOURCE_FILE" \
    && poetry install \
    && poetry run frontend-install \
    && poetry run frontend-build

# Set expose ports and entrypoint
EXPOSE 43/tcp
EXPOSE 8000/tcp
ENTRYPOINT /usr/local/bin/irrd --foreground

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
