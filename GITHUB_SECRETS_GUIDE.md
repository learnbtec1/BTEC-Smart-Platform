# GitHub Actions Secrets Configuration Guide

## Adding Secrets to Your Repository

### Step-by-Step Guide:

1. **Navigate to Repository Settings**
   - Go to your GitHub repository
   - Click on **Settings** tab
   - Select **Secrets and variables** → **Actions**
   - Click **New repository secret**

2. **Common Secrets for Microservices:**

   ```
   Name: DOCKER_USERNAME
   Value: your-dockerhub-username
   
   Name: DOCKER_PASSWORD
   Value: your-dockerhub-password-or-token
   
   Name: DATABASE_URL
   Value: postgresql://user:password@host:port/dbname
   
   Name: REDIS_URL
   Value: redis://password@host:port
   
   Name: JWT_SECRET_KEY
   Value: your-secret-jwt-key-here
   
   Name: API_KEY
   Value: your-api-key-here
   
   Name: GATEWAY_SECRET
   Value: your-gateway-secret-here
   ```

## Required Secrets for This Project

### Docker Hub (for CI/CD)
- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub access token (recommended) or password

### Database Connections
- `DATABASE_URL` - PostgreSQL connection string
- `DB_USER` - Database username
- `DB_PASSWORD` - Database password
- `DB_NAME` - Database name

### Redis Cache
- `REDIS_URL` - Redis connection string
- `REDIS_PASSWORD` - Redis password

### API Security
- `JWT_SECRET_KEY` - Secret key for JWT token generation
- `SECRET_KEY` - Application secret key
- `API_KEY` - External API authentication key

### Cloud Services (if applicable)
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `GCP_CREDENTIALS` - Google Cloud credentials JSON
- `AZURE_CREDENTIALS` - Azure credentials

## Generating Secure Secrets

### Generate Random Secret Key (Python):
```python
import secrets
print(secrets.token_hex(32))
```

### Generate Random Secret Key (PowerShell):
```powershell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

### Generate JWT Secret (OpenSSL):
```bash
openssl rand -hex 32
```

## Using Secrets in GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Microservices

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and Push Docker Images
      env:
        DATABASE_URL: ${{ secrets.DATABASE_URL }}
        JWT_SECRET_KEY: ${{ secrets.JWT_SECRET_KEY }}
        REDIS_URL: ${{ secrets.REDIS_URL }}
      run: |
        docker-compose -f docker-compose-microservices.yml build
        docker-compose -f docker-compose-microservices.yml push
    
    - name: Deploy to Server
      env:
        SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
        SERVER_HOST: ${{ secrets.SERVER_HOST }}
      run: |
        # Add deployment commands here
        echo "Deploying to production..."
```

## Environment Variables in Docker Compose

Update `docker-compose-microservices.yml` to use secrets:

```yaml
services:
  example_service:
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - REDIS_URL=${REDIS_URL}
      - API_KEY=${API_KEY}
```

## Local Development (.env file)

Create `.env` file (DO NOT commit to git):

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DB_USER=admin
DB_PASSWORD=your_local_password

# Redis
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=your_redis_password

# Security
JWT_SECRET_KEY=your_local_jwt_secret
SECRET_KEY=your_local_secret_key
API_KEY=your_local_api_key

# Docker Hub (for local builds)
DOCKER_USERNAME=your_username
DOCKER_PASSWORD=your_password
```

## Security Best Practices

1. **Never commit secrets to git**
   - Add `.env` to `.gitignore`
   - Use environment variables or secret management

2. **Use Docker Hub Access Tokens**
   - Create token at: https://hub.docker.com/settings/security
   - Use token instead of password

3. **Rotate secrets regularly**
   - Change secrets every 90 days
   - Update in GitHub Actions secrets

4. **Use secret scanning**
   - Enable GitHub secret scanning
   - Enable push protection

5. **Limit secret access**
   - Use environment-specific secrets
   - Separate production and development secrets

## Checking .gitignore

Ensure your `.gitignore` includes:

```gitignore
# Environment variables
.env
.env.local
.env.*.local

# Secrets
secrets/
*.key
*.pem

# Logs
*.log
setup.log
health_check.log
```

## Creating GitHub Actions Workflow

Run this script to generate a basic workflow:

```bash
python create_github_workflow.py
```

---

**Important**: After adding secrets:
1. Test in a separate branch first
2. Verify secrets are accessible in workflow runs
3. Check workflow logs for any exposure (GitHub masks secrets automatically)
4. Never log or print secret values

---

*Generated for BTEC-Backend microservices project*
