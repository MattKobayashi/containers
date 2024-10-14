FROM debian:12.7-slim AS build

# Install dependencies and compile
RUN apt-get update \
    && apt-get --yes install \
    git \
    build-essential \
    cmake \
    libpcre3-dev \
    libssl-dev \
    libmaxminddb-dev \
    libicu-dev \
    gettext \
    libasprintf-dev \
    mariadb-server \
    libmariadb-dev \
    mariadb-client \
    libmariadb-dev-compat \
    && git clone https://github.com/Verlihub/verlihub.git \
    && cd verlihub/ \
    && git checkout 1.5.0.0 \
    && mkdir -p build \
    && cd build/ \
    && cmake -DWITH_PLUGINS=OFF .. \
    && make

FROM debian:12.7-slim
WORKDIR /opt/verlihub/

# Install s6-overlay installation dependencies
RUN apt-get update \
    && apt-get --yes install \
    xz-utils

# Add s6-overlay
WORKDIR /tmp
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
RUN apt-get --yes install \
    libpcre3-dev \
    libssl3 \
    libmaxminddb-dev \
    libicu-dev \
    libasprintf-dev \
    mariadb-client \
    libmariadb-dev \
    libmariadb-dev-compat

# Copy files from build image
COPY --from=build /verlihub/ /verlihub/

# Run make install
RUN apt-get --yes install build-essential cmake \
    && cd /verlihub/build/ \
    && make install \
    && mkdir -p /opt/verlihub/sql/ \
    && cp /verlihub/share/sql/default_reglist.sql /opt/verlihub/sql/ \
    && rm -r /verlihub/

# Remove build dependencies
RUN apt-get --yes purge \
    build-essential \
    cmake \
    libpcre3-dev \
    libmaxminddb-dev \
    libicu-dev \
    libasprintf-dev \
    libmariadb-dev \
    libmariadb-dev-compat \
    xz-utils \
    && apt-get --yes autoremove \
    && apt-get --yes clean

# Install runtime dependencies
RUN apt-get --yes install \
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

# Copy files to image
COPY --chmod=700 --chown=verlihub:verlihub scripts/setup.py /opt/verlihub/scripts/setup.py

# Set entrypoint
ENTRYPOINT ["/init"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
