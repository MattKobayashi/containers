FROM alpine:3.21.3@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c
RUN apk --no-cache add avahi augeas

RUN mkdir /opt/avahi
COPY entrypoint.sh /opt/avahi/
RUN chmod +x /opt/avahi/entrypoint.sh

ENTRYPOINT ["/opt/avahi/entrypoint.sh"]

LABEL maintainer="matthew@kobayashi.com.au"
