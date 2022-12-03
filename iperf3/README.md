# docker-iperf3

iPerf3 in an Alpine-based Docker image. Small, lightweight and (most importantly) up-to-date with source.

## Running as a server

To run docker-iperf3 as a server in the foreground:

`docker run -it --rm --network=host ghcr.io/mattkobayashi/docker-iperf3 --server`

Or alternatively, you can run it as a daemon in the background:

`docker run -d --name iperf3-server --network=host ghcr.io/mattkobayashi/docker-iperf3 --server`

## Running as a client

There's a few ways to do this, but the basic gist is:

`docker run -it --rm --network=host ghcr.io/mattkobayashi/docker-iperf3 --client <SERVER_IP> <OPTIONS>`

## Explanatory notes

- iPerf3 has a lot of tunables and options available (especially on the client side). These are all documented [here](https://iperf.fr/iperf-doc.php#3doc).

- The use of `network=host` is recommended so as to avoid the Docker network proxy and ensure the best possible throughput for test conditions. It is possible to port forward with the Docker proxy, however performance may be affected. For example, you can run a server like this:

   `docker run -d --name iperf3-server -p 5201:5201/tcp -p 5201:5201/udp ghcr.io/mattkobayashi/docker-iperf3 --server`
