# fullbogons

A BIRD daemon with templated Team Cymru fullbogon import and iBGP session configuration in an Alpine Linux-based Docker image.

## Configuration

Set the following environment variables when creating your Docker container:

- `BIRD_ROUTER_ID=` The router ID you wish to use for the BIRD daemon. This should be your host's IP address.
- `BIRD_ASN=` The AS number you wish to use for the iBGP sessions to peers.
- `BIRD_PEERS=` A list of peers in the format `name,ip` using CIDR notation (e.g. `/24`) and separated by semi-colons (`;`).
- `BIRD_EXCLUDED_PREFIXES=` A list of prefixes you want to exclude from the fullbogon list, in CIDR notation (e.g. `/24`) and separated by semi-colons (`;`).
- `BIRD_DEBUG=` A list of debugging options to configure for BIRD's protocols, as a comma-separated list (e.g. `states,filters,interfaces`). Possible options are listed [here](https://bird.network.cz/?get_doc&v=20&f=bird-3.html#ss3.4), however the defaults should be good enough for the vast majority of cases.

## Running

Start the container as a daemon:

`docker run -d --name fullbogons --privileged --network-mode=host -e 'ENV_VARS=setem' ghcr.io/mattkobayashi/fullbogons`

Or use the example `docker-compose.yml` from this repository to run as a Docker Compose project (recommended).
