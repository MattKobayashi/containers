# ptokax

ptokax in an Ubuntu-based Docker image for the PtokaX DC++ hub server.

## Initial configuration

This is a list of environment variables you can pass to the container to configure basic options for PtokaX:

- `HUB`: Name of the hub (required)
- `HUB_ADDR`: Address of the hub (required)
- `MAX_USERS`: Maximum number of hub users (default: 500)
- `ADMIN_NICK`: Nickname of the admin user (default: Admin)

## Running the container

To run ptokax:

`docker run -d --name ptokax -e "HUB=DC++ Hub" -e "HUB_ADDR=A place" --volume /path/to/your/Settings.pxt:/config/cfg/Settings.pxt --expose 1209:1209/tcp --expose 411:411/tcp ghcr.io/mattkobayashi/ptokax`

Optionally, bind a RegisteredUsers.xml file (example file available in the repo):

`docker run -d --name ptokax -e "HUB=DC++ Hub" -e "HUB_ADDR=A place" --volume /path/to/your/Settings.pxt:/config/cfg/Settings.pxt --volume /path/to/your/RegisteredUsers.xml:/config/cfg/RegisteredUsers.xml --expose 1209:1209/tcp --expose 411:411/tcp ghcr.io/mattkobayashi/ptokax`

As a Compose file:

```
---
services:
   ptokax:
      container_name: ptokax
      image: 'ghcr.io/mattkobayashi/ptokax'
      restart: unless-stopped
      environment:
         - 'HUB=DC++ Hub'
         - 'HUB_ADDR=A place'
         - 'MAX_USERS=500' # Optional
         - 'ADMIN_NICK=Admin' # Optional
      volumes:
         - type: bind
           source: /path/to/your/Settings.pxt
           target: /config/cfg/Settings.pxt
         # OPTIONAL: bind a RegisteredUsers.xml file
         - type: bind
           soource: /path/to/your/RegisteredUsers.xml
           target: /config/cfg/RegisteredUsers.xml
      ports:
         - target: 1209
           published: 1209
           mode: host
         - target: 411
           published: 411
           mode: host
```

## Notes

- This was a prick to get working. Hope you enjoy!
