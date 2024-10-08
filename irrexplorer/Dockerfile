FROM python:3.11.10-alpine3.19

RUN adduser --system irrexplorer \
    && apk --no-cache add tar build-base python3-dev poetry npm yarn

USER irrexplorer

ENV SOURCE_FILE=irrexplorer.tar.gz \
    SOURCE_URL=https://github.com/NLNOG/irrexplorer/archive/28f61d29041caf23c03fafcc50ff4e02453e5b69.tar.gz \
    SOURCE_SHA1SUM=d638a350655953ac048e4fdfa8700ff433ae98fd

# Download source file, extract and compile
WORKDIR /irrexplorer
COPY --chmod=700 entrypoint.sh .
RUN wget -O "$SOURCE_FILE" "$SOURCE_URL" \
    && echo "${SOURCE_SHA1SUM}  ${SOURCE_FILE}" | sha1sum -c - \
    && tar -xz --strip-components=1 --file="$SOURCE_FILE" \
    && poetry lock \
    && poetry install \
    && poetry run frontend-install \
    && poetry run frontend-build

# Set expose ports and entrypoint
EXPOSE 8000/tcp
ENTRYPOINT ["/irrexplorer/entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
