#!/bin/sh

cat > cli.ini << EOF
# dns-cloudflare = True
standalone = True
agree-tos = True
no-eff-email = True
keep-until-expiring = True
# dns-cloudflare-propagation-seconds = 30
# dns-cloudflare-credentials = /run/secrets/CERTBOT_CF_DNS_API_TOKEN
deploy-hook = cp -RL /etc/letsencrypt/live/$DOMAIN/ /opt/certs/ && chmod -R o+r /opt/certs/
domain = $DOMAIN
email = $EMAIL
EOF

exec certbot certonly --config cli.ini --dry-run --no-verify-ssl --non-interactive --server https://10.30.50.2:14000/dir --verbose
