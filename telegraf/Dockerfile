FROM alpine:3.21.3@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c

# Set working directory
WORKDIR /opt/docker-telegraf

# Install Python and requirements
COPY requirements.txt .
RUN apk --no-cache add python3 py3-requests telegraf smartmontools jq curl lm-sensors wget

# Install Ookla Speedtest CLI utility
WORKDIR /opt/ookla 
RUN wget -O - https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz | tar xz

# Set entrypoint
WORKDIR /opt/docker-telegraf
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/opt/docker-telegraf/entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
