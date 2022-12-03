# docker-rng-tools

rng-tools in an Alpine-based Docker image. Small, lightweight and designed for use with OSes that don't include rng-tools by default (e.g. BurmillaOS).

## Running

To run docker-rngtools from the command line:

`docker run -d --name docker-rng-tools ghcr.io/mattkobayashi/docker-rng-tools`

## Docker Compose

An example Compose script:

```
services:
  docker-rng-tools:
    container_name: docker-rng-tools
      image: "ghcr.io/mattkobayashi/docker-rng-tools"
      restart: unless-stopped
      cap_add:
        - SYS_ADMIN
```

## Explanatory notes

- The `SYS_ADMIN` capability is required to allow write access to /dev/random so that the rngd process can add to the entropy pool.
