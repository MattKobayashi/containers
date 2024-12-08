FROM alpine:3.21.0 AS build

ENV SOURCE_HASH=4479e1ae070651dfc4836a998267c7ac2fba4f011abcfdca3b8ccd7736d4fd26 \
    SOURCE_VERSION=1.2.16 \
    SOURCE_FILE=stuntman.tgz

WORKDIR /stuntman

RUN apk --no-cache add build-base boost-dev openssl-dev wget tar \
    && wget -O $SOURCE_FILE https://www.stunprotocol.org/stunserver-$SOURCE_VERSION.tgz \
    && echo "$SOURCE_HASH  $SOURCE_FILE" | sha256sum -c \
    && tar -xz --strip-components=1 --file="$SOURCE_FILE" \
    && make

FROM alpine:3.21.0

WORKDIR /stuntman

RUN addgroup -S stuntman && adduser -S stuntman -G stuntman \
    && apk --no-cache add libstdc++ libgcc

USER stuntman

COPY --from=build /stuntman/stunclient /stuntman/stunclient
COPY --from=build /stuntman/stunserver /stuntman/stunserver

HEALTHCHECK CMD /stuntman/stunclient localhost

EXPOSE 3478/tcp 3478/udp

ENTRYPOINT ["/stuntman/stunserver"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
