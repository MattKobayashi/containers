FROM python:3.12-slim-bookworm

# Install xz
RUN apt-get update \
    && apt-get --yes upgrade \
    && apt-get --yes install xz-utils

# Add s6-overlay
WORKDIR /tmp
ENV S6_OVERLAY_VERSION=3.1.6.2
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz.sha256 /tmp
RUN echo "$(cat s6-overlay-noarch.tar.xz.sha256)" | sha256sum -c - \
    && tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz.sha256 /tmp
RUN echo "$(cat s6-overlay-x86_64.tar.xz.sha256)" | sha256sum -c - \
    && tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz
COPY s6-rc.d/ /etc/s6-overlay/s6-rc.d/

# IRRd
USER root
RUN adduser --gecos '' --disabled-password irrd \
    && mkdir -p /opt/irrd \
    && chown -R irrd:irrd /opt/irrd \
    && apt-get --yes install build-essential rustc python3-psycopg2 libpq-dev postgresql-client
USER irrd
WORKDIR /opt/irrd
RUN pip install --upgrade pip \
    && pip install irrd
COPY --chown=irrd:irrd init-irrd.py /opt/irrd/init-irrd.py

# IRR Explorer
USER root
RUN adduser --gecos '' --disabled-password irrexplorer \
    && mkdir -p /opt/irrexplorer \
    && chown -R irrexplorer:irrexplorer /opt/irrexplorer \
    && apt-get --yes install nodejs npm python3-poetry \
    && npm install --global yarn \
    && pip install poetry-dotenv-plugin
USER irrexplorer
WORKDIR /opt/irrexplorer
COPY --chown=irrexplorer:irrexplorer .env /opt/irrexplorer/.env
ENV IRRE_SOURCE_SHA1SUM=29eae66e26021342fcc67e7f71883beafe90c0c7
ADD --chown=irrexplorer:irrexplorer https://github.com/NLNOG/irrexplorer/archive/ab995b3dd2b6f868153e5b612ee08e8458dd7ada.tar.gz /tmp/irrexplorer.tar.gz
RUN echo "${IRRE_SOURCE_SHA1SUM}  /tmp/irrexplorer.tar.gz" | sha1sum -c - \
    && tar -xz --strip-components=1 --file="/tmp/irrexplorer.tar.gz" \
    && poetry self add poetry-dotenv-plugin \
    && poetry install \
    && poetry run frontend-install \
    && poetry run frontend-build

# Set expose ports and entrypoint
EXPOSE 43/tcp
EXPOSE 8000/tcp
ENTRYPOINT ["/init"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
