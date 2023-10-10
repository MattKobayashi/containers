FROM ubuntu:22.04

ARG TARGETPLATFORM
ENV RUNNER_VERSION=2.310.0 \
    RUNNER_HASH_x64=7ed6e2594aa8fc5b5a5e1986483f6683746f85695f4266a525e27b0e8e233ca7 \
    RUNNER_HASH_arm64=4aa4762880f3b17ff63ce585dd26aac783011c36bd034cdc06ca410d941d5274 \
    RUNNER_HASH_arm=1ad707e1e9eb03ae6ca7d04049dd00202325142f3f1122c6d46eb46ba486eb69

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
