# irrd

irrd in an Alpine Linux-based Docker image.

## Configuration

Create an appropriate configuration file and mount it into the container as shown below. An example configuration file can be found [here](https://irrd.readthedocs.io/en/stable/admins/configuration/#example-configuration-file), and a list of all available configuration options can be found [here](https://irrd.readthedocs.io/en/stable/admins/configuration/#configuration-options).

## Running

First, create the database tables:

`docker run -d --name irrd --volume /path/to/irrd.yaml:/etc/irrd.yaml --entrypoint /usr/local/bin/irrd_database_upgrade ghcr.io/mattkobayashi/irrd`

Then start the daemon:

`docker run -d --name irrd --volume /path/to/irrd.yaml:/etc/irrd.yaml ghcr.io/mattkobayashi/irrd`

## Explanatory notes

- Review the prerequisites for irrd [here](https://irrd.readthedocs.io/en/stable/admins/deployment/#requirements).

- This Docker image expects a PostgreSQL version of 15 or above. Earlier versions may work, but this is not guaranteed.

- Omit the `log.logfile_path` setting from your configuration file. This will log the daemon's output to `stdout`, allowing you to view them with the `docker logs` command.
