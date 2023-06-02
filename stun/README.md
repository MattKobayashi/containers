# stun

A STUN server in an Alpine-based Docker image. Small, lightweight and (most importantly) up-to-date with source.

## Running

Simply start the container as a daemon:

`docker run -d --name stun -p 3478:3478/tcp -p 3478:3478/udp ghcr.io/mattkobayashi/stun`

Or use the example `docker-compose.yml` from this repository to run as a Docker Compose project (recommended).
