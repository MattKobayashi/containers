FROM certbot/dns-cloudflare:v3.3.0@sha256:7a7043ab7b9fdb4c2b1016685d379c4bf28ce13821e12c10f51747c2eb3aacb2

RUN apk --no-cache add supercronic \
    && mkdir /crontab/ \
    && mkdir /opt/certs/

COPY certbot-cron /crontab/
COPY --chmod=0744 entry*.sh .

ENTRYPOINT ["./entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
