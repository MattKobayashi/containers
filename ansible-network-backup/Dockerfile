FROM alpine:3

WORKDIR /ansible

ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.24/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=6817299e04457e5d6ec4809c72ee13a43e95ba41

RUN wget "$SUPERCRONIC_URL" \
    && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
    && chmod +x "$SUPERCRONIC" \
    && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
    && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic \
    && addgroup -S ansible && adduser -S ansible -G ansible \
    && apk --no-cache upgrade \
    && apk add --no-cache ansible-core git py3-pip build-base python3-dev libssh-dev \
    && pip3 install ansible-pylibssh \
    && ansible-galaxy collection install community.general \
    && ansible-galaxy collection install cisco.ios cisco.iosxr junipernetworks.junos community.routeros \
    && apk del py3-pip build-base python3-dev libssh-dev

USER ansible

COPY ansible-cron ./crontab/ansible-cron
COPY config_backup.yaml .

ENV TZ=UTC \
	GIT_USER=Ansible

ENTRYPOINT ["supercronic", "./crontab/ansible-cron"]
