FROM ubuntu:22.04

ARG TARGETPLATFORM
ENV RUNNER_VERSION=2.311.0 \
    RUNNER_HASH_x64=29fc8cf2dab4c195bb147384e7e2c94cfd4d4022c793b346a6175435265aa278 \
    RUNNER_HASH_arm64=5d13b77e0aa5306b6c03e234ad1da4d9c6aa7831d26fd7e37a3656e77153611e \
    RUNNER_HASH_arm=806c63e3cdb92fa32fb0cf2409fd468c9929e3bfb4db7f80b9a7655d53bbb9dd

RUN apt-get update && apt-get -y install curl jq git ca-certificates gnupg sudo \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update && apt-get -y install docker-ce-cli \
    && adduser --system --group runner \
    && echo 'runner ALL = NOPASSWD: /usr/bin/apt-get' >> /etc/sudoers

USER runner
WORKDIR /actions-runner

RUN if [ "$TARGETPLATFORM" = "linux/amd64" ]; then ARCH=x64; elif [ "$TARGETPLATFORM" = "linux/arm/v7" ]; then ARCH=arm; elif [ "$TARGETPLATFORM" = "linux/arm64" ]; then ARCH=arm64; else exit 1; fi \
    && curl -O -L https://github.com/actions/runner/releases/download/v$RUNNER_VERSION/actions-runner-linux-$ARCH-$RUNNER_VERSION.tar.gz \
    && eval RUNNER_HASH='$RUNNER_HASH_'$ARCH \
    && echo "$RUNNER_HASH  actions-runner-linux-$ARCH-$RUNNER_VERSION.tar.gz" | sha256sum -c \
    && tar xzf actions-runner-linux-$ARCH-$RUNNER_VERSION.tar.gz \
    && rm actions-runner-linux-$ARCH-$RUNNER_VERSION.tar.gz

USER root
RUN ./bin/installdependencies.sh

COPY --chmod=0744 --chown=runner:runner entrypoint.sh /actions-runner/entrypoint.sh

USER runner
ENTRYPOINT ["./entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
