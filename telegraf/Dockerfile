FROM alpine:3

WORKDIR /opt/docker-telegraf
COPY requirements.txt .
COPY entrypoint.sh .
RUN apk --no-cache upgrade \
    && apk add --update --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/latest-stable/main/ telegraf smartmontools jq curl lm-sensors wget python3 \
    && python3 -m ensurepip \
    && python3 -m pip install --no-cache -r requirements.txt \
    && chmod +x entrypoint.sh

WORKDIR /opt/ookla 
RUN wget -O - https://install.speedtest.net/app/cli/ookla-speedtest-1.1.1-linux-x86_64.tgz | tar xz

ENTRYPOINT ["/opt/docker-telegraf/entrypoint.sh"]
LABEL maintainer="matthew@kobayashi.com.au"
