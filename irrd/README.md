# irrd

irrd and IRR Explorer in a PyPy-based container image.

## Configuration

Create an appropriate configuration file and mount it into the container as shown below. An example configuration file can be found [here](https://irrd.readthedocs.io/en/stable/admins/configuration/#example-configuration-file), and a list of all available configuration options can be found [here](https://irrd.readthedocs.io/en/stable/admins/configuration/#configuration-options).

### Required `irrd.yaml` values

- `irrd.database_url`: `"postgresql://irrd:irrd@/irrd"`
- `irrd.redis_url`: `"unix:///run/redis/redis-server.sock"`
- `irrd.piddir`: `/opt/irrd`
- `irrd.user`: `irrd`
- `irrd.group`: `irrd`

## Environment Variables

- `IRRD_HTTP_PORT` (required): The port that IRRd's HTTP service runs on, as configured in `/etc/irrd.yaml`.

## Running

Start the daemon:

`docker run -d --name irrd --env IRRD_HTTP_PORT=8080 --volume /path/to/irrd.yaml:/etc/irrd.yaml --volume irrd_database:/var/lib/postgresql/15/main ghcr.io/mattkobayashi/irrd`

## Explanatory notes

- Review the prerequisites for irrd [here](https://irrd.readthedocs.io/en/stable/admins/deployment/#requirements).

- Omit the `log.logfile_path` setting from your configuration file. This will log the daemon's output to `stdout`, allowing you to view logs with the `docker logs` command.
