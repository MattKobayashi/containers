FROM ruby:3.3.5-alpine3.20

ENV SOURCE_FILE=oxidized.tar.gz \
    SOURCE_URL=https://github.com/ytti/oxidized/archive/refs/tags/0.29.1.tar.gz \
    SOURCE_SHA1SUM=024c744081ba4c7d14cbbe1c95ccb46723163d63 \
    VERSION=0.29.1

# Download source file, extract and compile
WORKDIR /tmp/oxidized
RUN apk --no-cache add build-base cmake git libpq-dev mariadb-dev libssh2-dev icu-dev yq \
    && git clone https://github.com/ytti/oxidized.git . \
    && git checkout $VERSION \
    && gem install --no-document aws-sdk slack-ruby-client xmpp4r cisco_spark rugged \
    && gem install --no-document gpgme sequel sqlite3 mysql2 pg \
    && gem install --no-document net-tftp net-http-persistent mechanize \
    && CMAKE_FLAGS='-DUSE_SSH=ON' rake install \
    && gem install --no-document oxidized-web \
    && apk del build-base cmake libpq-dev mariadb-dev libssh2-dev

# Create non-root user account
RUN adduser --system oxidized

# Switch to non-root user
USER oxidized
WORKDIR /home/oxidized

# Copy files
COPY --chown=oxidized --chmod=0700 entrypoint.sh /home/oxidized/
COPY --chown=oxidized config /home/oxidized/.config/oxidized/

# Set expose port and entrypoint
EXPOSE 8888
ENTRYPOINT ["/home/oxidized/entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
