FROM alpine:3

# Set supercronic environment variables
ARG TARGETPLATFORM
ENV SUPERCRONIC_SHA1SUM_amd64=cd48d45c4b10f3f0bfdd3a57d054cd05ac96812b \
    SUPERCRONIC_SHA1SUM_arm=75e065bf0909f920b06d5bd797c0e6b31e68b112 \
    SUPERCRONIC_SHA1SUM_arm64=512f6736450c56555e01b363144c3c9d23abed4c \
    SUPERCRONIC_SHA1SUM_i386=3436985298ce241d7d9477eb9eab164b582717a8 \
    SUPERCRONIC_VERSION=v0.2.29

# Install supercronic
WORKDIR /supercronic

RUN if [ "$TARGETPLATFORM" = "linux/amd64" ]; then ARCH=amd64; elif [ "$TARGETPLATFORM" = "linux/arm/v7" ]; then ARCH=arm; elif [ "$TARGETPLATFORM" = "linux/arm64" ]; then ARCH=arm64; elif [ "$TARGETPLATFORM" = "linux/i386" ]; then ARCH=i386; else exit 1; fi \
    && export SUPERCRONIC="supercronic-linux-${ARCH}" \
    && export SUPERCRONIC_URL="https://github.com/aptible/supercronic/releases/download/${SUPERCRONIC_VERSION}/${SUPERCRONIC}" \
    && wget "$SUPERCRONIC_URL" \
    && eval SUPERCRONIC_SHA1SUM='$SUPERCRONIC_SHA1SUM_'$ARCH \
    && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
    && chmod +x "${SUPERCRONIC}" \
    && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
    && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

# Set BIRD environment variables
ENV SOURCE_FILE=bird.tar.gz \
    SOURCE_URL=https://gitlab.nic.cz/labs/bird/-/archive/v2.13.1/bird-v2.13.1.tar.gz \
    SOURCE_SHA1SUM=b2da703ea2fc68fec1e07c635a3c3301ccf291e4

# Install BIRD
WORKDIR /bird
RUN apk --no-cache upgrade \
    && apk --no-cache add tar build-base autoconf flex bison linux-headers ncurses-dev libssh-dev readline-dev \
    && wget -O "$SOURCE_FILE" "$SOURCE_URL" \
    && echo "${SOURCE_SHA1SUM}  ${SOURCE_FILE}" | sha1sum -c - \
    && tar -xz --strip-components=1 --file="$SOURCE_FILE" \
    && autoreconf \
    && ./configure \
    && make \
    && make install

# Post-install cleanup
RUN apk del tar build-base autoconf \
    && rm -rf /bird/*

# Copy external files
COPY requirements.txt .
COPY fullbogons.py .
COPY templates/* templates/
COPY crontab/* crontab/
COPY entrypoint.sh .

# Set up image for running BIRD
RUN adduser -D bird \
    && chown -R bird /bird/ \
    && apk --no-cache upgrade \
    && apk add python3 \
    && python3 -m ensurepip \
    && pip3 install -r requirements.txt

# Set expose ports
# BGP: 179/tcp
# RIP: 520/udp
# RIP-ng: 521/udp
EXPOSE 179/tcp 520/udp 521/udp

# Set default environment variables
ENV BIRD_ROUTER_ID= \
    BIRD_ASN=64666 \
    BIRD_PEERS= \
    BIRD_EXCLUDED_PREFIXES= \
    BIRD_DEBUG=states,filters,interfaces,events

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
