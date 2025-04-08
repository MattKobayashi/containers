ARG DEBIAN_FRONTEND=noninteractive
FROM debian:12.10-slim@sha256:b1211f6d19afd012477bd34fdcabb6b663d680e0f4b0537da6e6b0fd057a3ec3 AS build

# Install dependencies and compile
RUN apt-get update \
    && apt-get --no-install-recommends --yes install \
    git \
    build-essential \
    ca-certificates \
    cmake \
    libicu-dev \
    libpcre3-dev \
    libssl-dev \
    libmaxminddb-dev \
    gettext \
    libasprintf-dev \
    mariadb-server \
    libmariadb-dev \
    mariadb-client \
    python3 \
    libmariadb-dev-compat
# RUN git clone --depth 1 --branch release-72-1 https://github.com/unicode-org/icu.git \
#     && cd icu/icu4c/source \
#     && CFLAGS="-fPIC" CXXFLAGS="-fPIC" ./runConfigureICU Linux --enable-shared \
#     && make \
#     && make install
RUN git clone --depth 1 --branch 1.5.0.0 https://github.com/Verlihub/verlihub.git \
    && mkdir -p verlihub/build \
    && cd verlihub/build \
    && cmake -DWITH_PLUGINS=OFF .. \
    && make \
    && make install

FROM debian:12.10-slim@sha256:b1211f6d19afd012477bd34fdcabb6b663d680e0f4b0537da6e6b0fd057a3ec3
WORKDIR /opt/verlihub/

# Install s6-overlay installation dependencies
RUN apt-get update \
    && apt-get --no-install-recommends --yes install \
    xz-utils

# Add s6-overlay
WORKDIR /tmp/
ENV S6_OVERLAY_VERSION=3.2.0.2
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz.sha256 /tmp
RUN echo "$(cat s6-overlay-noarch.tar.xz.sha256)" | sha256sum -c - \
    && tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz.sha256 /tmp
RUN echo "$(cat s6-overlay-x86_64.tar.xz.sha256)" | sha256sum -c - \
    && tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz
COPY s6-rc.d/ /etc/s6-overlay/s6-rc.d/

# Install runtime dependencies
RUN apt-get --no-install-recommends --yes install \
    libpcre3 \
    libmaxminddb0 \
    libicu72 \
    libasprintf0v5 \
    libmariadb3 \
    pip \
    && pip3 install --break-system-packages mysql-connector-python \
    && useradd --system --base-dir /opt verlihub \
    && mkdir -p /opt/verlihub/.config/verlihub/ \
    && chown -R verlihub:verlihub /opt/verlihub/

# Copy files from build image
COPY --from=build /usr/local/lib/libvhapi.so /usr/local/lib/libvhapi.so
COPY --from=build /usr/local/lib/libverlihub.so /usr/local/lib/libverlihub.so
COPY --from=build /usr/local/bin/verlihub /usr/local/bin/verlihub
COPY --from=build /usr/local/bin/verlihub_config /usr/local/bin/verlihub_config
COPY --from=build /usr/local/include/verlihub/ /usr/local/include/verlihub/
COPY --from=build /usr/local/share/verlihub/ /usr/local/share/verlihub/
COPY --from=build /usr/local/bin/vh_daemon /usr/local/bin/vh_daemon
COPY --from=build /usr/local/bin/vh_lib /usr/local/bin/vh_lib
COPY --from=build /usr/local/bin/vh_gui /usr/local/bin/vh_gui
COPY --from=build /usr/local/bin/vh /usr/local/bin/vh
COPY --from=build /usr/local/bin/vhm /usr/local/bin/vhm
COPY --from=build /usr/local/bin/vh_regimporter /usr/local/bin/vh_regimporter
COPY --from=build /usr/local/bin/vh_migration_0.9.8eto1.0 /usr/local/bin/vh_migration_0.9.8eto1.0
COPY --from=build /usr/local/share/locale/cs_CZ/LC_MESSAGES/verlihub.mo /usr/local/share/locale/cs_CZ/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/hu_HU/LC_MESSAGES/verlihub.mo /usr/local/share/locale/hu_HU/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/pl_PL/LC_MESSAGES/verlihub.mo /usr/local/share/locale/pl_PL/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/ro_RO/LC_MESSAGES/verlihub.mo /usr/local/share/locale/ro_RO/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/sk_SK/LC_MESSAGES/verlihub.mo /usr/local/share/locale/sk_SK/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/bg_BG/LC_MESSAGES/verlihub.mo /usr/local/share/locale/bg_BG/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/ru_RU/LC_MESSAGES/verlihub.mo /usr/local/share/locale/ru_RU/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/de_DE/LC_MESSAGES/verlihub.mo /usr/local/share/locale/de_DE/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/es_ES/LC_MESSAGES/verlihub.mo /usr/local/share/locale/es_ES/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/fr_FR/LC_MESSAGES/verlihub.mo /usr/local/share/locale/fr_FR/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/it_IT/LC_MESSAGES/verlihub.mo /usr/local/share/locale/it_IT/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/nl_NL/LC_MESSAGES/verlihub.mo /usr/local/share/locale/nl_NL/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/sv_SE/LC_MESSAGES/verlihub.mo /usr/local/share/locale/sv_SE/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/tr_TR/LC_MESSAGES/verlihub.mo /usr/local/share/locale/tr_TR/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/lt_LT/LC_MESSAGES/verlihub.mo /usr/local/share/locale/lt_LT/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/locale/zh_CN/LC_MESSAGES/verlihub.mo /usr/local/share/locale/zh_CN/LC_MESSAGES/verlihub.mo
COPY --from=build /usr/local/share/man/man1/verlihub.1 /usr/local/share/man/man1/verlihub.1
COPY --from=build /usr/local/share/man/man1/vh.1 /usr/local/share/man/man1/vh.1
COPY --from=build /usr/local/share/man/man1/vh_regimporter.1 /usr/local/share/man/man1/vh_regimporter.1
COPY --from=build /usr/local/share/man/man1/vhm.1 /usr/local/share/man/man1/vhm.1

# Run ldconfig
RUN ldconfig

# Copy files to image
COPY --chmod=700 --chown=verlihub:verlihub scripts/setup.py /opt/verlihub/scripts/setup.py

# Set entrypoint
ENTRYPOINT ["/init"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
