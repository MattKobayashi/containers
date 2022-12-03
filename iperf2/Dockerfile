FROM alpine:3 as buildenv

ENV SOURCE_FILE=iperf2.tar.gz \
    SOURCE_URL=https://sourceforge.net/projects/iperf2/files/iperf-2.1.8.tar.gz/download \
    SOURCE_SHA1SUM=7725efffc6ef46fe5247ee326c39e5fa2eadf1eb

# Grab iperf2 from Sourceforge and compile
WORKDIR /iperf2
RUN apk --no-cache upgrade \
    && apk add --no-cache tar build-base \
    && wget -O "$SOURCE_FILE" "$SOURCE_URL" \
    && echo "${SOURCE_SHA1SUM}}  ${SOURCE_FILE}}" | sha1sum -c - \
    && tar -xz --strip-components=1 --file="$SOURCE_FILE" \
    && ./configure \
    && make \
    && make install

FROM alpine:3

# Copy relevant compiled files to distribution image
RUN adduser --system iperf2 \
    && apk --no-cache upgrade \
    && apk add --no-cache libgcc libstdc++
COPY --from=buildenv /usr/local/bin/ /usr/local/bin/
COPY --from=buildenv /usr/local/share/man/ /usr/local/share/man/

# Switch to 'iperf2' user
USER iperf2

# Set expose port and entrypoint
EXPOSE 5001
ENTRYPOINT ["iperf"]

LABEL maintainer="matthew@kobayashi.au"
