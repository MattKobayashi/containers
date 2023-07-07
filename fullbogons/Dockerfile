FROM alpine:3

ENV SOURCE_FILE=bird.tar.gz \
    SOURCE_URL=https://gitlab.nic.cz/labs/bird/-/archive/v2.13.1/bird-v2.13.1.tar.gz \
    SOURCE_SHA1SUM=b2da703ea2fc68fec1e07c635a3c3301ccf291e4

# Download source file, extract and compile
WORKDIR /bird
RUN apk --no-cache upgrade \
    && apk --no-cache add tar build-base autoconf flex bison linux-headers ncurses-dev libssh-dev readline-dev \
    && wget -O "$SOURCE_FILE" "$SOURCE_URL" \
    && echo "${SOURCE_SHA1SUM}  ${SOURCE_FILE}" | sha1sum -c - \
    && tar -xz --strip-components=1 --file="$SOURCE_FILE" \
    && autoreconf \
    && ./configure \
    && make \
    && make install

# Post-install cleanup
RUN apk del tar build-base autoconf \
    && rm -rf /bird/*

# Copy external files
COPY requirements.txt .
COPY fullbogons.py .
COPY templates/* templates/
COPY entrypoint.sh .

# Set up image for running BIRD
RUN adduser -D bird \
    && chown -R bird /bird/ \
    && apk --no-cache upgrade \
    && apk add python3 \
    && python3 -m ensurepip \
    && pip3 install -r requirements.txt

# Set expose ports
# BGP: 179/tcp
# RIP: 520/udp
# RIP-ng: 521/udp
EXPOSE 179/tcp 520/udp 521/udp

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
