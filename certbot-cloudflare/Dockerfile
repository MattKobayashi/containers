FROM certbot/dns-cloudflare:v4.0.0@sha256:d2b69333e562fb548f9f8150d5b2b71728348738c0fe9fa2afe6c29c26906f2c

RUN apk --no-cache add supercronic \
    && mkdir /crontab/ \
    && mkdir /opt/certs/

COPY certbot-cron /crontab/
COPY --chmod=0744 entry*.sh .

ENTRYPOINT ["./entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
