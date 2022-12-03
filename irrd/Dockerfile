FROM python:3.9-alpine

RUN apk --no-cache upgrade \
    && apk add build-base postgresql14-dev linux-headers \
    && adduser --system irrd \
    && python3 -m pip install irrd

# Set expose ports and entrypoint
EXPOSE 43/tcp
EXPOSE 8000/tcp
ENTRYPOINT /usr/local/bin/irrd --foreground

LABEL maintainer="matthew@kobayashi.au"
