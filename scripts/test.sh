#!/bin/bash

set -e

# Function to clean up
cleanup() {
    echo "Cleaning up..."
    docker stop some-sqld 2>/dev/null || true
    docker rm some-sqld 2>/dev/null || true
}

# Set up trap to ensure cleanup on exit
trap cleanup EXIT

# Ensure no container is running
cleanup

# Run the Docker container
echo "Starting libsql-server container..."
./scripts/docker.sh

# Run tests
echo "Running tests..."
python3 manage.py test

echo "Test execution completed."