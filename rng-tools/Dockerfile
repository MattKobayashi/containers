FROM alpine:3

# Uprade and install packages to image
RUN apk --no-cache upgrade \
    && apk --no-cache add rng-tools

# Set entrypoint
ENTRYPOINT ["rngd"]
CMD ["-f"]

LABEL org.opencontainers.image.authors="MattKobayashi <matthew@kobayashi.au>"
