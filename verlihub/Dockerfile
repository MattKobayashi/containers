FROM alpine:3 as build

ENV SOURCE_FILE=verlihub.tar.gz \
    SOURCE_URL=https://github.com/Verlihub/verlihub/archive/baa5f6ca57742f08bab1ab577e0d58119f7e07f7.tar.gz \
    SOURCE_SHA1SUM=13cd61773642af497c941804f091200fcce0db88

# Download source file, extract and compile
WORKDIR /verlihub/
RUN apk --no-cache add bash build-base cmake gettext gettext-dev icu-dev libmaxminddb-dev mariadb-dev openssl-dev pcre-dev \
    && apk --no-cache add libexecinfo-dev --repository=https://dl-cdn.alpinelinux.org/alpine/v3.16/main/ \
    && wget -O "$SOURCE_FILE" "$SOURCE_URL" \
    && echo "${SOURCE_SHA1SUM}  ${SOURCE_FILE}" | sha1sum -c - \
    && tar -xz --strip-components=1 --file="$SOURCE_FILE" \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install \
    && rm -R /verlihub/*

# Copy compiled files to final image
FROM alpine:3

# Install runtime dependencies
RUN apk --no-cache add bash icu-data-full mariadb-connector-c mysql-client ncurses \
    && adduser -Su 1000 verlihub

# Copy /usr/bin/
COPY --from=build \
    /usr/bin/msgmerge \
    /usr/bin/

# Copy /usr/local/bin/
COPY --from=build \
    /usr/local/bin/verlihub* \
    /usr/local/bin/vh* \
    /usr/local/bin/

# Copy /usr/local/include/
COPY --from=build \
    /usr/local/include/verlihub/ \
    /usr/local/include/verlihub/

# Copy /lib/
COPY --from=build \
    /lib/ld-musl-x86_64.so* \
    /lib/libssl.so* \
    /lib/libz.so* \
    /lib/

# Copy /usr/lib/
COPY --from=build \
    /usr/lib/libasprintf.so* \
    /usr/lib/libcrypto.so* \
    /usr/lib/libexecinfo.so* \
    /usr/lib/libgcc_s.so* \
    /usr/lib/libicudata.so* \
    /usr/lib/libicui18n.so* \
    /usr/lib/libicuuc.so* \
    /usr/lib/libintl.so* \
    /usr/lib/libmaxminddb.so* \
    /usr/lib/libpcre.so* \
    /usr/lib/libstdc++.so* \
    /usr/lib/

COPY --from=build \
    /usr/local/lib/libplug_pi.so \
    /usr/local/lib/libverlihub.so \
    /usr/local/lib/libvhapi.so \
    /usr/local/lib/

# Copy /usr/local/share/locale/
COPY --from=build \
    /usr/local/share/locale/ \
    /usr/local/share/locale/

# Copy share
COPY --from=build \
    /usr/local/share/verlihub/ \
    /usr/local/share/verlihub/

# Copy entrypoint.sh to image
WORKDIR /verlihub/
COPY entrypoint.sh .

# Change to non-root user
USER verlihub

# Set entrypoint
ENTRYPOINT ["/verlihub/entrypoint.sh"]
CMD ["--install"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
