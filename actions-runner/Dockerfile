FROM ubuntu:24.04

ARG TARGETPLATFORM
ENV RUNNER_VERSION=2.316.0 \
    RUNNER_HASH_x64=64a47e18119f0c5d70e21b6050472c2af3f582633c9678d40cb5bcb852bcc18f \
    RUNNER_HASH_arm64=03ea42d347d9ad2d875ea03c2321a0e6507c8575edaa6a75fbe8edfefe0e2a74 \
    RUNNER_HASH_arm=5059dda203b6b3b29bd591536b2d68231a425afc0fe022f27fd154ea6f441e23

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
RUN add-apt-repository ppa:dotnet/backports \
    && apt-get install dotnet6

COPY --chmod=0744 --chown=runner:runner entrypoint.sh /actions-runner/entrypoint.sh

USER runner
ENTRYPOINT ["./entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
