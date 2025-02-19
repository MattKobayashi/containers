FROM certbot/dns-cloudflare:v3.2.0@sha256:3c3eca6a6476d1fc2cd67de0ebc1e7b9b8c6775fcfaadb7098aad76e9cade5e3

RUN apk --no-cache add supercronic \
    && mkdir /crontab/ \
    && mkdir /opt/certs/

COPY certbot-cron /crontab/
COPY --chmod=0744 entry*.sh .

ENTRYPOINT ["./entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
