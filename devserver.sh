#!/bin/sh
source .venv/bin/activate

# Check if a port is provided
if [ -z "$1" ]; then
    PORT=5000  # Default port if none is provided
else
    PORT=$1  # Use the provided port
fi

python -m flask --app main run -p $PORT --debug
