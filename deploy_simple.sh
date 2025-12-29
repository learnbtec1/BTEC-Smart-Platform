#!/bin/bash
# Simple deployment script without rollback

set -e

echo "=== SIMPLE DEPLOY ==="

# Load environment
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Build and start
docker-compose -f docker-compose-microservices.yml build
docker-compose -f docker-compose-microservices.yml up -d

echo "Waiting for services..."
sleep 15

# Health checks
echo "Checking health..."
curl -f http://localhost/health || echo "Gateway health check failed"
curl -f http://localhost:8000/health || echo "Service health check failed"

echo "=== DEPLOY COMPLETE ==="
