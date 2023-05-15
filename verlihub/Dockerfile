FROM alpine:3 as build

ENV SOURCE_FILE=verlihub.tar.gz \
    SOURCE_URL=https://github.com/MattKobayashi/verlihub/archive/refs/tags/v1.4.1.0.tar.gz \
    SOURCE_SHA1SUM=c8ae72640889f78aec567115fc96ec725628b4df

# Download source file, extract and compile
WORKDIR /verlihub/
RUN apk --no-cache add bash build-base cmake gettext gettext-dev icu-dev libmaxminddb-dev mariadb-dev openssl-dev pcre-dev \
    && apk --no-cache add libexecinfo-dev --repository=https://dl-cdn.alpinelinux.org/alpine/v3.15/main/ \
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

# Copy bin
COPY --from=build /usr/bin/msgmerge /usr/bin/
COPY --from=build /usr/local/bin/verlihub /usr/local/bin/
COPY --from=build /usr/local/bin/verlihub_config /usr/local/bin/
COPY --from=build /usr/local/bin/vh /usr/local/bin/
COPY --from=build /usr/local/bin/vh_daemon /usr/local/bin/
COPY --from=build /usr/local/bin/vh_gui /usr/local/bin/
COPY --from=build /usr/local/bin/vh_lib /usr/local/bin/
COPY --from=build /usr/local/bin/vh_migration_0.9.8eto1.0 /usr/local/bin/
COPY --from=build /usr/local/bin/vh_regimporter /usr/local/bin/
COPY --from=build /usr/local/bin/vhm /usr/local/bin/

# Copy includes
COPY --from=build /usr/local/include/verlihub/ /usr/local/include/verlihub/

# Copy lib
COPY --from=build /lib/ld-musl-x86_64.so* /lib/
COPY --from=build /lib/libssl.so* /lib/
COPY --from=build /lib/libz.so* /lib/
COPY --from=build /usr/lib/libasprintf.so* /usr/lib/
COPY --from=build /usr/lib/libcrypto.so* /usr/lib/
COPY --from=build /usr/lib/libexecinfo.so* /usr/lib/
COPY --from=build /usr/lib/libgcc_s.so* /usr/lib/
COPY --from=build /usr/lib/libicudata.so* /usr/lib/
COPY --from=build /usr/lib/libicui18n.so* /usr/lib/
COPY --from=build /usr/lib/libicuuc.so* /usr/lib/
COPY --from=build /usr/lib/libintl.so* /usr/lib/
COPY --from=build /usr/lib/libmaxminddb.so* /usr/lib/
COPY --from=build /usr/lib/libpcre.so* /usr/lib/
COPY --from=build /usr/lib/libstdc++.so* /usr/lib/
COPY --from=build /usr/local/lib/libplug_pi.so /usr/local/lib/
COPY --from=build /usr/local/lib/libverlihub.so /usr/local/lib/
COPY --from=build /usr/local/lib/libvhapi.so /usr/local/lib/

# Copy locale
COPY --from=build /usr/local/share/locale/cs_CZ/LC_MESSAGES/verlihub.mo /usr/local/share/locale/cs_CZ/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/hu_HU/LC_MESSAGES/verlihub.mo /usr/local/share/locale/hu_HU/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/pl_PL/LC_MESSAGES/verlihub.mo /usr/local/share/locale/pl_PL/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/ro_RO/LC_MESSAGES/verlihub.mo /usr/local/share/locale/ro_RO/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/sk_SK/LC_MESSAGES/verlihub.mo /usr/local/share/locale/sk_SK/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/bg_BG/LC_MESSAGES/verlihub.mo /usr/local/share/locale/bg_BG/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/ru_RU/LC_MESSAGES/verlihub.mo /usr/local/share/locale/ru_RU/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/de_DE/LC_MESSAGES/verlihub.mo /usr/local/share/locale/de_DE/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/es_ES/LC_MESSAGES/verlihub.mo /usr/local/share/locale/es_ES/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/fr_FR/LC_MESSAGES/verlihub.mo /usr/local/share/locale/fr_FR/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/it_IT/LC_MESSAGES/verlihub.mo /usr/local/share/locale/it_IT/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/nl_NL/LC_MESSAGES/verlihub.mo /usr/local/share/locale/nl_NL/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/sv_SE/LC_MESSAGES/verlihub.mo /usr/local/share/locale/sv_SE/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/tr_TR/LC_MESSAGES/verlihub.mo /usr/local/share/locale/tr_TR/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/lt_LT/LC_MESSAGES/verlihub.mo /usr/local/share/locale/lt_LT/LC_MESSAGES/
COPY --from=build /usr/local/share/locale/zh_CN/LC_MESSAGES/verlihub.mo /usr/local/share/locale/zh_CN/LC_MESSAGES/

# Copy share
COPY --from=build /usr/local/share/verlihub/ /usr/local/share/verlihub/

# Copy entrypoint.sh to image
WORKDIR /verlihub/
COPY entrypoint.sh .

# Change to non-root user
USER verlihub

# Set entrypoint
ENTRYPOINT ["/verlihub/entrypoint.sh"]
CMD ["--install"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
