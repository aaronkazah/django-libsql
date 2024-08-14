#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/libsql_server.log"

# Generate Ed25519 key pair
openssl genpkey -algorithm Ed25519 -out "${SCRIPT_DIR}/jwt_private_key.pem"

# Extract public key in PEM format
openssl pkey -in "${SCRIPT_DIR}/jwt_private_key.pem" -pubout -out "${SCRIPT_DIR}/jwt_public_key.pem"

# Extract raw public key and encode in URL-safe base64 without padding
JWT_KEY=$(openssl pkey -in "${SCRIPT_DIR}/jwt_private_key.pem" -pubout -outform DER | tail -c 32 | base64 | tr '/+' '_-' | tr -d '=')

echo "JWT public key (URL-safe Base64 format without padding):"
echo $JWT_KEY
echo

# Function to wait for the server to be ready and capture logs
wait_for_server() {
    echo "Waiting for libsql-server to be ready..."
    for i in {1..30}; do
        if docker ps --filter "name=some-sqld" --format '{{.Names}}' | grep -q 'some-sqld'; then
            if curl -s http://localhost:8080 > /dev/null; then
                echo "libsql-server is ready!"
                return 0
            fi
        else
            echo "Container 'some-sqld' is not running. Capturing logs..."
            docker logs some-sqld &> "$LOG_FILE" || echo "No logs available"
            return 1
        fi
        echo "Attempt $i: Server not ready, waiting..."
        sleep 2
    done
    echo "Server did not become ready in time."
    docker logs some-sqld &> "$LOG_FILE" || echo "No logs available"
    return 1
}

# Run the Docker container
echo "Starting libsql-server container..."
docker run --name some-sqld -d -p 8080:8080 \
    -e SQLD_NODE=primary \
    -e SQLD_AUTH_JWT_KEY="$JWT_KEY" \
    --platform linux/amd64 \
    --rm \
    ghcr.io/tursodatabase/libsql-server:latest

# Wait for the server to be ready
if ! wait_for_server; then
    echo "Error: Server did not start properly. Cleaning up..."
    docker stop some-sqld 2>/dev/null || true
    docker rm some-sqld 2>/dev/null || true
    echo "Logs have been saved to $LOG_FILE"
    exit 1
fi

echo "Server is ready and running!"