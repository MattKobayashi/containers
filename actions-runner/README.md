# actions-runner

A GitHub Actions self-hosted runner in an Ubuntu-based Docker image. Small, lightweight and (most importantly) up-to-date with source.

## Configuration

Add a self-hosted runner to a repository on GitHub under Settings > Actions > Runners. Select Linux for the OS and your Docker host's architecture. Copy the repository URL and the token, these will be set as environment variables.

Set the following environment variables when creating your Docker container:

- `REPO=` The full URL of your GitHub repository that the self-hosted runner will be added to.
- `TOKEN=` The self-hosted runner token provided during the self-hosted runner setup. This value can also be passed as a Docker secret.

## Running

Simply start the container as a daemon:

`docker run -d --name actions-runner -e 'ENV_VARS=whatever' ghcr.io/mattkobayashi/actions-runner`

Or use the example `docker-compose.yml` from this repository to run as a Docker Compose project (recommended).
