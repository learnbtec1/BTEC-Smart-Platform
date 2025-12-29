#!/bin/bash
set -euo pipefail

APP_NAME="btec-backend"
COMPOSE_FILE="docker-compose-microservices.yml"
LAST_TAG_FILE=".last_successful_tag"
NEW_TAG="${1:-latest}"

echo "=== [$APP_NAME] ADVANCED DEPLOY STARTED (tag: $NEW_TAG) ==="

# Load environment variables
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Validate required environment variables
if [ -z "${IMAGE_REGISTRY:-}" ] || [ -z "${REGISTRY_USERNAME:-}" ] || [ -z "${REGISTRY_PASSWORD:-}" ]; then
  echo "ERROR: IMAGE_REGISTRY / REGISTRY_USERNAME / REGISTRY_PASSWORD must be set in .env"
  exit 1
fi

# Get previous successful tag for rollback
if [ -f "$LAST_TAG_FILE" ]; then
  OLD_TAG=$(cat "$LAST_TAG_FILE")
else
  OLD_TAG=""
fi

echo "Previous successful tag: ${OLD_TAG:-<none>}"

# Login to container registry
echo "$REGISTRY_PASSWORD" | docker login "$IMAGE_REGISTRY" -u "$REGISTRY_USERNAME" --password-stdin

# Set image tag
export IMAGE_TAG="$NEW_TAG"

# Pull latest images
echo "Pulling images with tag: $IMAGE_TAG"
docker compose -f "$COMPOSE_FILE" pull

# Stop existing containers
echo "Stopping existing containers..."
docker compose -f "$COMPOSE_FILE" down

# Start new containers
echo "Starting new containers..."
docker compose -f "$COMPOSE_FILE" up -d --remove-orphans

# Wait for services to start
echo "Waiting for services to be ready..."
sleep 20

# Health check URLs
CHECK_URLS=(
  "http://localhost/health"
  "http://localhost:8000/health"
)

# Run health checks
HEALTH_FAIL=0
echo "Running health checks..."
for URL in "${CHECK_URLS[@]}"; do
  if curl -fsS "$URL" > /dev/null; then
    echo "[OK] $URL"
  else
    echo "[FAIL] $URL"
    HEALTH_FAIL=1
  fi
done

# Handle health check failures
if [ "$HEALTH_FAIL" -ne 0 ]; then
  echo "Health checks FAILED - Initiating rollback"

  if [ -n "$OLD_TAG" ]; then
    echo "Rolling back to previous tag: $OLD_TAG"
    export IMAGE_TAG="$OLD_TAG"
    docker compose -f "$COMPOSE_FILE" pull || true
    docker compose -f "$COMPOSE_FILE" up -d --remove-orphans
    
    echo "Rollback complete. Deployment FAILED."
    exit 1
  else
    echo "No previous tag available for rollback"
    echo "Deployment FAILED - manual intervention required"
    exit 1
  fi
fi

# Save successful tag
echo "$NEW_TAG" > "$LAST_TAG_FILE"

# Show running containers
echo ""
echo "Running containers:"
docker compose -f "$COMPOSE_FILE" ps

echo ""
echo "=== DEPLOYMENT COMPLETE ✓ ==="
echo "Successfully deployed tag: $NEW_TAG"
