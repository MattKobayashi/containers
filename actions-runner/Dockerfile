FROM ubuntu:latest

ARG TARGETPLATFORM
ENV RUNNER_VERSION=2.304.0 \
	RUNNER_HASH_x64=292e8770bdeafca135c2c06cd5426f9dda49a775568f45fcc25cc2b576afc12f \
	RUNNER_HASH_arm=9b988321757805f0d650574f49808ed7c7b31a691551b205f724e68f5ed9b543 \
	RUNNER_HASH_arm64=34c49bd0e294abce6e4a073627ed60dc2f31eee970c13d389b704697724b31c6

RUN adduser --system --group runner \
	&& apt-get update && apt-get -y install curl ca-certificates curl gnupg \
	&& install -m 0755 -d /etc/apt/keyrings \
	&& curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
	&& chmod a+r /etc/apt/keyrings/docker.gpg \
	&& echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
	&& apt-get update && apt-get -y install docker-ce-cli

USER runner
WORKDIR /actions-runner

RUN if [ "$TARGETPLATFORM" = "linux/amd64" ]; then ARCH=x64; elif [ "$TARGETPLATFORM" = "linux/arm/v7" ]; then ARCH=arm; elif [ "$TARGETPLATFORM" = "linux/arm64" ]; then ARCH=arm64; else exit 1; fi \
	&& curl -o actions-runner-linux-${ARCH}-${RUNNER_VERSION}.tar.gz https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-${ARCH}-${RUNNER_VERSION}.tar.gz \
	&& eval RUNNER_HASH='$RUNNER_HASH_'$ARCH \
	&& echo "${RUNNER_HASH}  actions-runner-linux-${ARCH}-${RUNNER_VERSION}.tar.gz" | sha256sum -c \
	&& tar xzf actions-runner-linux-${ARCH}-${RUNNER_VERSION}.tar.gz \
	&& rm actions-runner-linux-${ARCH}-${RUNNER_VERSION}.tar.gz

USER root
RUN ./bin/installdependencies.sh \
	&& apt-get remove -y curl ca-certificates curl gnupg

COPY --chmod=0744 --chown=runner:runner entrypoint.sh /actions-runner/entrypoint.sh

USER runner
ENTRYPOINT ["./entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"