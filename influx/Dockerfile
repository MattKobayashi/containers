FROM lscr.io/linuxserver/baseimage-alpine:3.20
ARG TARGETPLATFORM
ARG TARGETOS
ARG TARGETARCH
ARG INFLUX_DB_VERSION=2.7.1
ARG INFLUX_CLI_VERSION=2.7.1

# Get binaries
ADD https://dl.influxdata.com/influxdb/releases/influxdb2-${INFLUX_DB_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz /tmp/
ADD https://dl.influxdata.com/influxdb/releases/influxdb2-${INFLUX_DB_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz.asc /tmp/
ADD https://dl.influxdata.com/influxdb/releases/influxdb2-client-${INFLUX_CLI_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz /tmp/
ADD https://dl.influxdata.com/influxdb/releases/influxdb2-client-${INFLUX_CLI_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz.asc /tmp/

# Verify downloaded binaries
RUN apk --no-cache add gpg gpg-agent \
    && curl -s https://repos.influxdata.com/influxdata-archive_compat.key | gpg --import - \
    && gpg --verify /tmp/influxdb2-${INFLUX_DB_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz.asc /tmp/influxdb2-${INFLUX_DB_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz \
    && gpg --verify /tmp/influxdb2-${INFLUX_CLI_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz.asc /tmp/influxdb2-${INFLUX_CLI_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz \
    && apk del gpg gpg-agent

# Move binaries to /usr/local/bin
RUN tar xvzf /tmp/influxdb2-${INFLUX_DB_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz -C /tmp/ \
    && tar xvzf /tmp/influxdb2-client-${INFLUX_CLI_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz -C /tmp/ \
    && cp /tmp/influxdb2_${TARGETOS}_${TARGETARCH}/influxd /usr/local/bin/ \
    && cp /tmp/influx /usr/local/bin/

# Copy s6 service scripts
RUN mkdir /etc/s6-overlay/s6-rc.d/influxd/ \
    && mkdir /etc/s6-overlay/s6-rc.d/influxd/dependencies.d/ \
    && touch /etc/s6-overlay/s6-rc.d/user/contents.d/influxd \
    && touch /etc/s6-overlay/s6-rc.d/influxd/dependencies.d/base
COPY s6/type /etc/s6-overlay/s6-rc.d/influxd/type
COPY s6/run /etc/s6-overlay/s6-rc.d/influxd/run
COPY s6/finish /etc/s6-overlay/s6-rc.d/influxd/finish

# Set container defaults
EXPOSE 8086
ENV INFLUXD_BOLT_PATH='/var/lib/influxdb/influxd.bolt' \
    INFLUXD_ENGINE_PATH='/var/lib/influxdb/' \
    INFLUXD_SQLITE_PATH='/var/lib/influxdb/influxd.sqlite'
VOLUME /var/lib/influxdb/

# Set entrypoint
ENTRYPOINT ["/init"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
