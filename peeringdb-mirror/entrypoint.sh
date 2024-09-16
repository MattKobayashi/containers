#!/bin/bash

# Cleanup function
cleanup() {
    echo "Container stopped, performing cleanup..."
    poetry run peeringdb server --stop
}

# Trap SIGTERM
trap 'cleanup' SIGTERM

# Execute command(s)
poetry --no-root install ; poetry run peeringdb server --setup ; poetry run peeringdb server --start &

# Wait
wait $!
