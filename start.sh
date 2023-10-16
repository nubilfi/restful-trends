#!/bin/bash

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script's directory
cd "$DIR"

# Activate the virtual environment if it's not activated
if [ -z "$VIRTUAL_ENV" ]; then
    source .venv/bin/activate
fi

# Check if requirements are already installed
if ! pip show -r requirements.txt >/dev/null 2>&1; then
    # Install requirements if not already installed
    pip install -r requirements.txt
fi

# Start the Gunicorn server
gunicorn -c gunicorn_config.py main:app
