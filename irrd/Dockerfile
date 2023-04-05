FROM python:3.9-alpine

RUN apk --no-cache upgrade \
    && apk --no-cache add build-base postgresql15-dev linux-headers \
    && adduser --system irrd

USER irrd

RUN python3 -m pip install irrd

# Set expose ports and entrypoint
EXPOSE 43/tcp
EXPOSE 8000/tcp
ENTRYPOINT /usr/local/bin/irrd --foreground

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
