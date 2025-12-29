# Advanced Deployment Guide

## Deployment Scripts Overview

This project includes production-ready deployment scripts with automatic rollback capabilities.

### Available Scripts

| Script | Platform | Features |
|--------|----------|----------|
| `deploy_advanced.ps1` | Windows (PowerShell) | Full rollback support |
| `deploy_advanced.sh` | Linux/macOS/WSL (Bash) | Full rollback support |
| `deploy_simple.sh` | Linux/macOS/WSL (Bash) | Simple deployment |

## Prerequisites

1. **Docker and Docker Compose installed**
2. **Container registry credentials** (GitHub Container Registry, Docker Hub, etc.)
3. **Environment file configured** (`.env`)

## Setup

### 1. Create `.env` File

Copy `.env.example` to `.env` and configure:

```bash
# Container Registry
IMAGE_REGISTRY=ghcr.io/YOUR_USERNAME/btec-backend
REGISTRY_USERNAME=YOUR_GITHUB_USERNAME
REGISTRY_PASSWORD=YOUR_GITHUB_TOKEN

# Image version
IMAGE_TAG=latest

# Database (optional)
DATABASE_URL=postgresql://user:password@localhost:5432/btec_db
REDIS_URL=redis://localhost:6379

# Security
JWT_SECRET_KEY=your_jwt_secret_here
SECRET_KEY=your_app_secret_here
```

### 2. Get Container Registry Token

**For GitHub Container Registry:**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `write:packages`, `read:packages`, `delete:packages`
4. Copy token to `.env` as `REGISTRY_PASSWORD`

**For Docker Hub:**
1. Go to Docker Hub → Account Settings → Security
2. Create access token
3. Copy token to `.env` as `REGISTRY_PASSWORD`

## Deployment Methods

### Method 1: Advanced Deployment (Recommended)

**Windows (PowerShell):**
```powershell
# Deploy latest version
.\deploy_advanced.ps1

# Deploy specific version
.\deploy_advanced.ps1 -Tag v1.2.3

# Deploy from feature branch
.\deploy_advanced.ps1 -Tag feature-auth
```

**Linux/macOS/WSL (Bash):**
```bash
# Make script executable (first time only)
chmod +x deploy_advanced.sh

# Deploy latest version
./deploy_advanced.sh

# Deploy specific version
./deploy_advanced.sh v1.2.3

# Deploy from feature branch
./deploy_advanced.sh feature-auth
```

### Method 2: Simple Deployment

```bash
chmod +x deploy_simple.sh
./deploy_simple.sh
```

## How It Works

### Advanced Deployment Flow

```
1. Load environment variables from .env
   ↓
2. Validate required credentials
   ↓
3. Read previous successful tag (for rollback)
   ↓
4. Login to container registry
   ↓
5. Pull latest images with specified tag
   ↓
6. Stop existing containers
   ↓
7. Start new containers
   ↓
8. Wait for services to initialize (20 seconds)
   ↓
9. Run health checks on all services
   ↓
10. IF HEALTHY → Save tag, complete ✓
    IF UNHEALTHY → Rollback to previous tag ✗
```

### Health Check URLs

The script checks these endpoints:
- `http://localhost/health` - API Gateway
- `http://localhost:8000/health` - Example Service

### Rollback Mechanism

If health checks fail:
1. Script identifies last successful tag from `.last_successful_tag`
2. Pulls images with previous tag
3. Restarts containers with previous version
4. Exits with error code 1

If no previous tag exists:
- Deployment fails
- Manual intervention required

## Build and Push Images

Before deploying, build and push your images to the registry:

```bash
# Login to registry
echo $REGISTRY_PASSWORD | docker login $IMAGE_REGISTRY -u $REGISTRY_USERNAME --password-stdin

# Build images
docker-compose -f docker-compose-microservices.yml build

# Tag images
docker tag btec-backend-gateway:latest $IMAGE_REGISTRY/gateway:v1.0.0
docker tag btec-backend-example_service:latest $IMAGE_REGISTRY/example_service:v1.0.0

# Push to registry
docker push $IMAGE_REGISTRY/gateway:v1.0.0
docker push $IMAGE_REGISTRY/example_service:v1.0.0
```

Or use GitHub Actions (see `.github/workflows/deploy.yml`).

## Monitoring Deployment

### During Deployment

Watch the deployment logs:
```bash
# PowerShell
.\deploy_advanced.ps1 -Verbose

# Bash
./deploy_advanced.sh | tee deployment.log
```

### After Deployment

Check service status:
```bash
# Container status
docker-compose -f docker-compose-microservices.yml ps

# Service logs
docker-compose -f docker-compose-microservices.yml logs -f

# Health monitoring
python monitor_health.py
```

## Troubleshooting

### Health Checks Fail

1. Check service logs:
   ```bash
   docker-compose -f docker-compose-microservices.yml logs
   ```

2. Verify health endpoints:
   ```bash
   curl http://localhost/health
   curl http://localhost:8000/health
   ```

3. Check container status:
   ```bash
   docker ps
   ```

### Rollback Doesn't Work

1. Verify `.last_successful_tag` file exists
2. Check if previous tag images are available in registry
3. Manually rollback:
   ```bash
   export IMAGE_TAG=v1.0.0
   docker-compose -f docker-compose-microservices.yml pull
   docker-compose -f docker-compose-microservices.yml up -d
   ```

### Registry Authentication Fails

1. Verify credentials in `.env`:
   ```bash
   echo $IMAGE_REGISTRY
   echo $REGISTRY_USERNAME
   ```

2. Test login manually:
   ```bash
   echo $REGISTRY_PASSWORD | docker login $IMAGE_REGISTRY -u $REGISTRY_USERNAME --password-stdin
   ```

3. Check token permissions (GitHub: needs `write:packages`)

### Images Not Found

1. Verify images exist in registry
2. Check tag names match
3. Ensure images were pushed:
   ```bash
   docker images | grep btec-backend
   ```

## Production Deployment

### Blue-Green Deployment

For zero-downtime deployment, use blue-green strategy:

1. Deploy to staging environment first
2. Run smoke tests
3. Switch traffic to new version
4. Keep old version running as backup

### Canary Deployment

Gradually roll out to subset of users:

1. Deploy new version alongside old
2. Route 10% traffic to new version
3. Monitor metrics
4. Gradually increase traffic
5. Complete rollout or rollback

## CI/CD Integration

### GitHub Actions

The deployment scripts integrate with GitHub Actions:

```yaml
- name: Deploy to Production
  env:
    IMAGE_REGISTRY: ${{ secrets.IMAGE_REGISTRY }}
    REGISTRY_USERNAME: ${{ secrets.REGISTRY_USERNAME }}
    REGISTRY_PASSWORD: ${{ secrets.REGISTRY_PASSWORD }}
  run: |
    ./deploy_advanced.sh ${{ github.sha }}
```

See `.github/workflows/deploy.yml` for complete example.

## Best Practices

1. **Always tag images** - Never use `latest` in production
2. **Test deployments** - Use staging environment first
3. **Monitor health** - Set up continuous health monitoring
4. **Keep rollback ready** - Always maintain previous version
5. **Use secrets** - Never commit credentials to git
6. **Automate deployments** - Use CI/CD pipelines
7. **Log everything** - Keep deployment logs for debugging

## Security Considerations

1. **Secrets Management**
   - Use environment variables
   - Never commit `.env` to git
   - Rotate credentials regularly

2. **Registry Access**
   - Use access tokens, not passwords
   - Limit token permissions
   - Use separate tokens per environment

3. **Network Security**
   - Use HTTPS for health checks in production
   - Implement authentication on endpoints
   - Use private networks where possible

## Advanced Configuration

### Custom Health Check Ports

Edit `deploy_advanced.sh` or `deploy_advanced.ps1`:

```bash
CHECK_URLS=(
  "http://localhost:3000/health"
  "http://localhost:3001/health"
  "http://localhost:3002/health"
)
```

### Custom Wait Time

Adjust sleep duration before health checks:

```bash
# Wait longer for slow-starting services
sleep 60
```

### Additional Validation

Add custom validation steps:

```bash
# Run database migrations
docker-compose exec gateway python manage.py migrate

# Run smoke tests
docker-compose exec gateway pytest tests/smoke/
```

## Support

For issues or questions:
- Check logs: `docker-compose logs`
- Review health status: `python monitor_health.py`
- Check documentation: `README-MICROSERVICES.md`

---

**Deployment Status Tracking**

Track your deployments in `.last_successful_tag` file.
This file is automatically managed by deployment scripts.

```bash
# View last successful deployment
cat .last_successful_tag

# Force set successful tag (use cautiously)
echo "v1.2.3" > .last_successful_tag
```
