FROM alpine:3.21.2

RUN apk --no-cache add supercronic \
    && addgroup -S ansible && adduser -S ansible -G ansible \
    && mkdir /repo && chown -R ansible /repo \
    && apk --no-cache upgrade \
    && apk add --no-cache py3-pip ansible-core git yq libssh build-base python3-dev libssh-dev

USER ansible
WORKDIR /ansible

COPY --chown=ansible --chmod=0744 entrypoint.sh /ansible/entrypoint.sh
COPY --chown=ansible ansible-cron /ansible/crontab/ansible-cron
COPY --chown=ansible yancobat-backup.yaml /ansible/yancobat-backup.yaml
COPY --chown=ansible yancobat-setup.yaml /ansible/yancobat-setup.yaml
COPY --chown=ansible vars.yaml /ansible/vars.yaml
COPY --chown=ansible pyproject.toml /ansible/pyproject.toml

RUN ansible-galaxy collection install community.general community.network \
    && ansible-galaxy collection install cisco.ios cisco.iosxr junipernetworks.junos community.routeros vyos.vyos \
    && pip install --break-system-packages --user ansible-pylibssh

USER root
RUN apk del build-base python3-dev libssh-dev

USER ansible

ENV TZ=UTC \
    GIT_USER=YANCoBaT \
    NOTIFY_PUSHOVER_ENABLED=false \
    NOTIFY_SLACK_ENABLED=false \
    NOTIFY_TELEGRAM_ENABLED=false

ENTRYPOINT ["./entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
