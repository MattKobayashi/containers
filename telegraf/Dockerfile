FROM alpine:3.20.3

# Set working directory
WORKDIR /opt/docker-telegraf

# Install Python and requirements
COPY requirements.txt .
RUN apk --no-cache upgrade \
    && apk --no-cache add python3 py3-requests

# Install other dependencies
RUN apk --no-cache upgrade \
    && apk --no-cache add telegraf smartmontools jq curl lm-sensors wget

# Install Ookla Speedtest CLI utility
WORKDIR /opt/ookla 
RUN wget -O - https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz | tar xz

# Set entrypoint
WORKDIR /opt/docker-telegraf
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/opt/docker-telegraf/entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
