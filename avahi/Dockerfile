FROM alpine:3.21.2
RUN apk --no-cache add avahi augeas

RUN mkdir /opt/avahi
COPY entrypoint.sh /opt/avahi/
RUN chmod +x /opt/avahi/entrypoint.sh

ENTRYPOINT ["/opt/avahi/entrypoint.sh"]

LABEL maintainer="matthew@kobayashi.com.au"
