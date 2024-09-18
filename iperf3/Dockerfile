FROM alpine:3.20.3 as buildenv

ENV SOURCE_FILE=iperf3.tar.gz \
    SOURCE_URL=https://github.com/esnet/iperf/archive/3.13.tar.gz \
    SOURCE_SHA1SUM=57504ea15f392d9d69723933aa8f0ad891f7e786

# Download source file, extract and compile
WORKDIR /iperf3
RUN apk --no-cache upgrade \
    && apk --no-cache add tar build-base \
    && wget -O "$SOURCE_FILE" "$SOURCE_URL" \
    && echo "${SOURCE_SHA1SUM}  ${SOURCE_FILE}" | sha1sum -c - \
    && tar -xz --strip-components=1 --file="$SOURCE_FILE" \
    && ./configure \
    && make \
    && make install

FROM alpine:3.20.3

# Copy relevant compiled files to distribution image
RUN adduser --system iperf3 \
    && ldconfig -n /usr/local/lib \
    && apk --no-cache upgrade
COPY --from=buildenv /usr/local/lib/ /usr/local/lib/
COPY --from=buildenv /usr/local/bin/ /usr/local/bin/
COPY --from=buildenv /usr/local/include/ /usr/local/include/
COPY --from=buildenv /usr/local/share/man/ /usr/local/share/man/

# Switch to non-root user
USER iperf3

# Set expose port and entrypoint
EXPOSE 5201
ENTRYPOINT ["iperf3"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
