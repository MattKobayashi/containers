FROM alpine:3.20.3

# Add s6-overlay
WORKDIR /tmp
ENV S6_OVERLAY_VERSION=3.2.0.0
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz.sha256 /tmp
RUN echo "$(cat s6-overlay-noarch.tar.xz.sha256)" | sha256sum -c - \
    && tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz.sha256 /tmp
RUN echo "$(cat s6-overlay-x86_64.tar.xz.sha256)" | sha256sum -c - \
    && tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz
COPY s6-rc.d/ /etc/s6-overlay/s6-rc.d/

# Set work directory
WORKDIR /opt/speedtest/

# Update image and install/extract Ookla Speedtest
RUN apk --no-cache upgrade \
    && wget https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz \
    && tar -xof ookla-speedtest-1.2.0-linux-x86_64.tgz

# Set entrypoint
ENTRYPOINT ["/init"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
