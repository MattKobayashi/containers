FROM python:3.13.1-alpine3.19@sha256:8287ca207e905649e9f399b5f91a119e5e9051d8cd110d5f8c3b4bd9458ebd1d

RUN adduser --system irrexplorer \
    && apk --no-cache add tar build-base python3-dev poetry npm yarn

USER irrexplorer

ENV SOURCE_FILE=irrexplorer.tar.gz \
    SOURCE_URL=https://github.com/NLNOG/irrexplorer/archive/28f61d29041caf23c03fafcc50ff4e02453e5b69.tar.gz \
    SOURCE_SHA1SUM=d638a350655953ac048e4fdfa8700ff433ae98fd

# Download source file, extract and compile
WORKDIR /irrexplorer
COPY --chmod=700 --chown=irrexplorer entrypoint.sh .
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
