FROM ubuntu:latest as buildenv

ENV SOURCE_FILE=ptokax.tar.gz \
    SOURCE_URL=http://www.ptokax.org/files/0.5.3.0-nix-src.tgz \
    SOURCE_SHA1SUM=119f78a2759db98cfa6e6501138651176dc27613

# Download source file, extract and compile
WORKDIR /ptokax-build/
RUN apt update \
    && apt -y full-upgrade \
    && apt -y install wget make g++ zlib1g-dev libtinyxml-dev liblua5.4-dev \
    && wget -O "$SOURCE_FILE" "$SOURCE_URL" \
    && echo "${SOURCE_SHA1SUM}  ${SOURCE_FILE}" | sha1sum -c - \
    && tar -xz --strip-components=1 --file="$SOURCE_FILE" \
    && make

# Finished compiling, configure image for distribution
WORKDIR /ptokax/
COPY entrypoint.sh .
RUN cp /ptokax-build/PtokaX . \
    && mkdir /config/ \
    && mkdir /config/cfg/ \
    && cp -R /ptokax-build/cfg.example/ /config/cfg/ \
    && rm -R /ptokax-build/ \
    && apt -y remove wget make g++ \
    && apt -y autoremove \
    && adduser --system --uid 1000 ptokax \
    && chown -R ptokax:nogroup /ptokax/ \
    && chown -R ptokax:nogroup /config/ \
    && chmod +x entrypoint.sh

# Switch to non-root user
USER ptokax

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
