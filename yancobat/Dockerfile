FROM alpine:3

WORKDIR /ansible

ARG TARGETPLATFORM
ENV SUPERCRONIC_SHA1SUM_amd64=642f4f5a2b67f3400b5ea71ff24f18c0a7d77d49 \
    SUPERCRONIC_SHA1SUM_arm=4f625d77d2f9a790ea4ad679d0d2c318a14ec3be \
    SUPERCRONIC_SHA1SUM_arm64=0b658d66bd54cf10aeccd9bdbd95fc7d9ba84a61 \
    SUPERCRONIC_SHA1SUM_i386=1b5ebdd122b05cd2ff38b585022f1d909b0146ff \
    SUPERCRONIC_VERSION=v0.2.25

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
    && sudo -u ansible pip3 install ansible-pylibssh \
    && sudo -u ansible ansible-galaxy collection install community.general \
    && sudo -u ansible ansible-galaxy collection install cisco.ios cisco.iosxr junipernetworks.junos community.network community.routeros \
    && apk del py3-pip build-base python3-dev libssh-dev sudo

USER ansible

COPY --chown=ansible --chmod=0744 entrypoint.sh /ansible/entrypoint.sh
COPY --chown=ansible ansible-cron /ansible/crontab/ansible-cron
COPY --chown=ansible config-backup.yaml /ansible/config-backup.yaml
COPY --chown=ansible clone-repo.yaml /ansible/clone-repo.yaml
COPY --chown=ansible vars.yaml /ansible/vars.yaml

ENV TZ=UTC \
    GIT_USER=YANCoBaT \
    NOTIFY_TELEGRAM_ENABLED=false \
    NOTIFY_SLACK_ENABLED=false

ENTRYPOINT ["./entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
