FROM python:3.11-alpine

RUN adduser --system irrexplorer \
    && apk --no-cache upgrade \
    && apk --no-cache add tar build-base python3-dev poetry npm yarn

USER irrexplorer

ENV SOURCE_FILE=irrexplorer.tar.gz \
    SOURCE_URL=https://github.com/NLNOG/irrexplorer/archive/c4eb6599c1bd359f1464834bf5e07828aec1769a.tar.gz \
    SOURCE_SHA1SUM=cd031821503510b35346be06f9f38dc736c9ff2a

# Download source file, extract and compile
WORKDIR /irrexplorer
COPY entrypoint.sh .
RUN wget -O "$SOURCE_FILE" "$SOURCE_URL" \
    && echo "${SOURCE_SHA1SUM}  ${SOURCE_FILE}" | sha1sum -c - \
    && tar -xz --strip-components=1 --file="$SOURCE_FILE" \
    && poetry install \
    && poetry run frontend-install \
    && poetry run frontend-build

# Set expose ports and entrypoint
EXPOSE 8000/tcp
ENTRYPOINT ["/irrexplorer/entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
