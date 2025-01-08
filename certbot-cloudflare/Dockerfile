FROM certbot/dns-cloudflare:v3.1.0

RUN apk --no-cache add supercronic \
    && mkdir /crontab/ \
    && mkdir /opt/certs/

COPY certbot-cron /crontab/
COPY --chmod=0744 entrypoint.sh .

ENTRYPOINT ["./entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
