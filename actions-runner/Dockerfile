FROM ubuntu:22.04

ARG TARGETPLATFORM
ENV RUNNER_VERSION=2.306.0 \
    RUNNER_HASH_x64=b0a090336f0d0a439dac7505475a1fb822f61bbb36420c7b3b3fe6b1bdc4dbaa \
    RUNNER_HASH_arm64=842a9046af8439aa9bcabfe096aacd998fc3af82b9afe2434ddd77b96f872a83 \
    RUNNER_HASH_arm=01799a8e6c39788a9f848e903de1ed7d0503d695d0ccc57f4c57ca78f35499c6

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
