FROM alpine:3.21.3

# Install dependencies and set timezone
RUN apk add --no-cache ca-certificates curl tzdata bash busybox-suid su-exec ffmpeg vlc \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && sed -i 's/geteuid/getppid/' /usr/bin/vlc

# Add xTeve and guide2go
RUN wget https://github.com/xteve-project/xTeVe-Downloads/raw/master/xteve_linux_amd64.zip -O temp.zip; unzip temp.zip -d /usr/bin/; rm temp.zip
COPY *.sh /
COPY sample_*.txt /

# Set executable permissions
RUN chmod +x /entrypoint.sh \
    && chmod +x /cronjob.sh \
    && chmod +x /usr/bin/xteve \
    && mkdir /config

# Expose port
EXPOSE 34400

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>, alturismo <alturismo@gmail.com>"
