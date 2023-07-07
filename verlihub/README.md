# verlihub

The `verlihub` DC++ hub server in an Ubuntu-based Docker image.

## Prerequisites

- A MySQL server

## Initial configuration

Run the container with the `--install` flag, e.g. `docker run -it ghcr.io/mattkobayashi/verlihub --install`. This will populate the configuration files. When prompted, choose option `[1]` for the configuration directory.

## Running the container

To run verlihub:

`docker run -d --name verlihub --expose 411:411/tcp ghcr.io/mattkobayashi/verlihub`

As a Compose file:

```
---
services:
   verlihub:
      container_name: ptokax
      image: 'ghcr.io/mattkobayashi/verlihub'
      restart: unless-stopped
      volumes:
         - type: volume
           source: verlihub_data
           target: /home/verlihub/.config/verlihub
      ports:
         - target: 411
           published: 411
           mode: host

volumes:
   verlihub_data:
      name: verlihub_data
```
