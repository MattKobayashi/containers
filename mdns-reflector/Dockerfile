FROM alpine:3.20.3 as buildenv

ENV SOURCE_FILE=mdns-reflector.tar.gz \
    SOURCE_URL=https://github.com/vfreex/mdns-reflector/archive/refs/tags/v0.0.1-dev.1.tar.gz \
    SOURCE_SHA1SUM=a78fdcb8c1f850b89fbc548d574c2c8a16cadd52

# Download source file, extract and compile
WORKDIR /mdns-reflector
RUN apk --no-cache upgrade \
    && apk --no-cache add tar build-base cmake \
    && wget -O "$SOURCE_FILE" "$SOURCE_URL" \
    && echo "${SOURCE_SHA1SUM}  ${SOURCE_FILE}" | sha1sum -c - \
    && tar -xz --strip-components=1 --file="$SOURCE_FILE" \
    && mkdir build \
    && cd build \
    && cmake -DCMAKE_BUILD_TYPE=release .. \
    && make install

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

# Copy relevant compiled files to distribution image
RUN adduser --system mdns-reflector \
    && apk --no-cache upgrade
COPY --from=buildenv /usr/local/bin/ /usr/local/bin/

# Switch to non-root user
USER mdns-reflector

# Set entrypoint
ENTRYPOINT ["/init"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
