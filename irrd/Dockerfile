FROM pypy:3-slim

RUN apt-get update \
    && apt-get upgrade \
    && apt-get install build-essential \
    && adduser --system irrd

USER irrd

RUN pip3 install irrd

# Set expose ports and entrypoint
EXPOSE 43/tcp
EXPOSE 8000/tcp
ENTRYPOINT /usr/local/bin/irrd --foreground

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
