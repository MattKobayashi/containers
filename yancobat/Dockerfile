FROM alpine:3

WORKDIR /ansible

ARG TARGETPLATFORM
ENV SUPERCRONIC_SHA1SUM_amd64=cd48d45c4b10f3f0bfdd3a57d054cd05ac96812b \
    SUPERCRONIC_SHA1SUM_arm=75e065bf0909f920b06d5bd797c0e6b31e68b112 \
    SUPERCRONIC_SHA1SUM_arm64=512f6736450c56555e01b363144c3c9d23abed4c \
    SUPERCRONIC_SHA1SUM_i386=3436985298ce241d7d9477eb9eab164b582717a8 \
    SUPERCRONIC_VERSION=v0.2.29

RUN if [ "$TARGETPLATFORM" = "linux/amd64" ]; then ARCH=amd64; elif [ "$TARGETPLATFORM" = "linux/arm/v7" ]; then ARCH=arm; elif [ "$TARGETPLATFORM" = "linux/arm64" ]; then ARCH=arm64; elif [ "$TARGETPLATFORM" = "linux/i386" ]; then ARCH=i386; else exit 1; fi \
    && export SUPERCRONIC="supercronic-linux-${ARCH}" \
    && export SUPERCRONIC_URL="https://github.com/aptible/supercronic/releases/download/${SUPERCRONIC_VERSION}/${SUPERCRONIC}" \
    && wget "$SUPERCRONIC_URL" \
    && eval SUPERCRONIC_SHA1SUM='$SUPERCRONIC_SHA1SUM_'$ARCH \
    && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
    && chmod +x "${SUPERCRONIC}" \
    && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
    && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic \
    && addgroup -S ansible && adduser -S ansible -G ansible \
    && mkdir /repo && chown -R ansible /repo \
    && apk --no-cache upgrade \
    && apk add --no-cache ansible-core git yq libssh py3-pip build-base python3-dev libssh-dev sudo \
    && mkdir /ansible/venv && chown -R ansible /ansible/venv \
    && sudo -u ansible python3 -m venv /ansible/venv \
    && sudo -u ansible source venv/bin/activate \
    && pip3 install ansible-pylibssh \
    && ansible-galaxy collection install community.general community.network \
    && ansible-galaxy collection install cisco.ios cisco.iosxr junipernetworks.junos community.routeros vyos.vyos \
    && exit \
    && apk del py3-pip build-base python3-dev libssh-dev sudo

USER ansible

COPY --chown=ansible --chmod=0744 entrypoint.sh /ansible/entrypoint.sh
COPY --chown=ansible ansible-cron /ansible/crontab/ansible-cron
COPY --chown=ansible yancobat-backup.yaml /ansible/yancobat-backup.yaml
COPY --chown=ansible yancobat-setup.yaml /ansible/yancobat-setup.yaml
COPY --chown=ansible vars.yaml /ansible/vars.yaml

ENV TZ=UTC \
    GIT_USER=YANCoBaT \
    NOTIFY_TELEGRAM_ENABLED=false \
    NOTIFY_SLACK_ENABLED=false

ENTRYPOINT ["./entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
