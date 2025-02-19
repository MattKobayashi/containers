FROM debian:12.9-slim@sha256:40b107342c492725bc7aacbe93a49945445191ae364184a6d24fedb28172f6f7

# Install xz-utils
RUN apt-get update \
    && apt-get --yes install xz-utils wget

# Set work directory
WORKDIR /opt/speedtest/

# Update image and install/extract Ookla Speedtest
RUN wget https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz \
    && tar -xof ookla-speedtest-1.2.0-linux-x86_64.tgz \
    && apt-get --yes remove xz-utils wget \
    && apt-get --yes autoremove

# Set entrypoint
ENTRYPOINT ["/opt/speedtest/speedtest", "--accept-license", "--progress=no"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
