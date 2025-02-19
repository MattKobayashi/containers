FROM alpine:3.21.3@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c AS buildenv

ENV SOURCE_FILE=mdns-reflector.tar.gz \
    SOURCE_URL=https://github.com/vfreex/mdns-reflector/archive/refs/tags/v0.0.1-dev.1.tar.gz \
    SOURCE_SHA1SUM=a78fdcb8c1f850b89fbc548d574c2c8a16cadd52

# Download source file, extract and compile
WORKDIR /mdns-reflector
RUN apk --no-cache add tar build-base cmake \
    && wget -O "$SOURCE_FILE" "$SOURCE_URL" \
    && echo "${SOURCE_SHA1SUM}  ${SOURCE_FILE}" | sha1sum -c - \
    && tar -xz --strip-components=1 --file="$SOURCE_FILE" \
    && mkdir build \
    && cd build \
    && cmake -DCMAKE_BUILD_TYPE=release .. \
    && make install

FROM alpine:3.21.3@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c

# Copy relevant compiled files to distribution image
RUN adduser --system mdns-reflector
COPY --from=buildenv /usr/local/bin/ /usr/local/bin/

# Switch to non-root user
USER mdns-reflector

# Set entrypoint
ENTRYPOINT ["mdns-reflector"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
