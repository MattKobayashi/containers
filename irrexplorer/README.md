# irrexplorer

irrexplorer in an Alpine Linux-based Docker image.

## Running

`docker run -d --name irrexplorer -e 'DATABASE_URL=postgresql://postgresql/irrexplorer' -e 'IRRD_ENDPOINT=https://irrd.example.net/graphql/' ghcr.io/mattkobayashi/irrexplorer`

## Explanatory notes

- Review the prerequisites for irrexplorer [here](https://github.com/NLNOG/irrexplorer#requirements).

- Configuration options for irrexplorer are passed as environment variables. A full list is available [here](https://github.com/NLNOG/irrexplorer#configuration). Optional settings have sensible defaults, and generally don't need to be changed.