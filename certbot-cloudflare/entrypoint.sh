#!/bin/sh

cat > cli.ini << EOF
dns-cloudflare = True
agree-tos = True
no-eff-email = True
keep-until-expiring = True
dns-cloudflare-propagation-seconds = 30
dns-cloudflare-credentials = /run/secrets/CERTBOT_CF_DNS_API_TOKEN
deploy-hook = cp -RL /etc/letsencrypt/live/$DOMAIN/ /opt/certs/ && chmod -R o+r /opt/certs/
domain = $DOMAIN
email = $EMAIL
EOF

exec /usr/bin/supercronic /crontab/certbot-cron
