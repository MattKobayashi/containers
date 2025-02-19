FROM alpine:3.21.3@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c AS buildenv

ENV SOURCE_FILE=iperf2.tar.gz \
    SOURCE_URL=https://downloads.sourceforge.net/project/iperf2/iperf-2.1.9.tar.gz \
    SOURCE_SHA1SUM=e7b669c2e8747df95b59956e83ff53d3971d7a5f

# Download source file, extract and compile
WORKDIR /iperf2
RUN apk --no-cache add tar build-base \
    && wget -O "$SOURCE_FILE" "$SOURCE_URL" \
    && echo "${SOURCE_SHA1SUM}  ${SOURCE_FILE}" | sha1sum -c - \
    && tar -xz --strip-components=1 --file="$SOURCE_FILE" \
    && ./configure \
    && make \
    && make install

FROM alpine:3.21.3@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c

# Copy relevant compiled files to distribution image
RUN adduser --system iperf2 \
    && apk --no-cache add libgcc libstdc++
COPY --from=buildenv /usr/local/bin/ /usr/local/bin/
COPY --from=buildenv /usr/local/share/man/ /usr/local/share/man/

# Switch to non-root user
USER iperf2

# Set expose port and entrypoint
EXPOSE 5001
ENTRYPOINT ["iperf"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
