FROM alpine:3 as buildenv

ENV SOURCE_FILE=ptokax.tar.gz \
    SOURCE_URL=http://www.ptokax.org/files/0.5.3.0-nix-src.tgz \
    SOURCE_SHA1SUM=119f78a2759db98cfa6e6501138651176dc27613

# Download source file, extract and compile
WORKDIR /ptokax
COPY makefile-alpine .
RUN apk --no-cache upgrade \
    && apk --no-cache add tar build-base zlib-dev tinyxml-dev lua5.4-dev \
    && wget -O "$SOURCE_FILE" "$SOURCE_URL" \
    && echo "${SOURCE_SHA1SUM}  ${SOURCE_FILE}" | sha1sum -c - \
    && tar -xz --strip-components=1 --file="$SOURCE_FILE" \
    && ln -s /usr/lib/lua5.4/liblua.so /usr/lib/ \
    && sed -i -e '/-llua5.1 -ltinyxml/r makefile-alpine' makefile \
    && make alpine

FROM alpine:3

# Copy relevant compiled files to distribution image
COPY --from=buildenv /ptokax/PtokaX /ptokax/
COPY --from=buildenv /ptokax/cfg.example/ /config/
RUN adduser -Su 1000 ptokax \
    && apk --no-cache upgrade \
    && apk --no-cache add libstdc++ lua5.4-libs tinyxml libgcc \
    && chown -R ptokax:nogroup /ptokax/ \
    && chown -R ptokax:nogroup /config/

# Switch to non-root user
USER ptokax

# Set entrypoint
ENTRYPOINT ["/ptokax/PtokaX"]
CMD ["-c", "/config"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
