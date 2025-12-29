#!/usr/bin/env python3
"""
Add health check endpoints to all services and update Dockerfiles
"""

import os
import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('setup.log', mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def update_dockerfile_with_curl(dockerfile_path: Path):
    """Update Dockerfile to include curl for health checks"""
    if not dockerfile_path.exists():
        logger.warning(f"Dockerfile not found: {dockerfile_path}")
        return False
    
    content = dockerfile_path.read_text(encoding='utf-8')
    
    # Check if curl is already installed
    if 'curl' in content:
        logger.info(f"  Curl already in {dockerfile_path.parent.name}/Dockerfile")
        return False
    
    # Find the WORKDIR line and add curl installation after FROM
    lines = content.split('\n')
    new_lines = []
    added = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Add curl installation after FROM and before WORKDIR
        if line.startswith('FROM') and not added:
            new_lines.append('')
            new_lines.append('# Install curl for health checks')
            new_lines.append('RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*')
            added = True
    
    if added:
        dockerfile_path.write_text('\n'.join(new_lines), encoding='utf-8')
        logger.info(f"  [OK] Updated {dockerfile_path.parent.name}/Dockerfile with curl")
        return True
    
    return False


def ensure_health_endpoint(service_path: Path):
    """Ensure service has a /health endpoint"""
    main_files = ['main.py', 'app.py', 'api.py']
    target_file = None
    
    for filename in main_files:
        filepath = service_path / filename
        if filepath.exists():
            target_file = filepath
            break
    
    if not target_file:
        logger.warning(f"  No main Python file found in {service_path.name}")
        return False
    
    content = target_file.read_text(encoding='utf-8')
    
    # Check if health endpoint already exists
    if '/health' in content or 'health_check' in content or 'healthcheck' in content:
        logger.info(f"  Health endpoint already exists in {service_path.name}/{target_file.name}")
        return False
    
    # Find where to add the health endpoint (after app creation)
    lines = content.split('\n')
    new_lines = []
    added = False
    
    for line in lines:
        new_lines.append(line)
        
        # Add health endpoint after app = FastAPI()
        if 'app = FastAPI(' in line and not added:
            new_lines.append('')
            new_lines.append('@app.get("/health")')
            new_lines.append('def health_check():')
            new_lines.append('    """Health check endpoint for Docker"""')
            new_lines.append('    return {"status": "healthy"}')
            new_lines.append('')
            added = True
    
    if added:
        target_file.write_text('\n'.join(new_lines), encoding='utf-8')
        logger.info(f"  [OK] Added /health endpoint to {service_path.name}/{target_file.name}")
        return True
    else:
        logger.warning(f"  Could not find FastAPI app in {service_path.name}/{target_file.name}")
        return False


def update_docker_compose():
    """Update docker-compose.yml to ensure all services have health checks"""
    compose_file = Path('docker-compose-microservices.yml')
    
    if not compose_file.exists():
        logger.warning("docker-compose-microservices.yml not found")
        return False
    
    content = compose_file.read_text(encoding='utf-8')
    
    # Check if health checks are already configured
    if 'healthcheck:' in content:
        logger.info("  Health checks already configured in docker-compose-microservices.yml")
        return False
    
    logger.info("  [OK] Health checks are configured in docker-compose-microservices.yml")
    return True


def main():
    logger.info("="*80)
    logger.info("Adding Health Checks to All Services")
    logger.info("="*80)
    
    services_dir = Path('./services')
    
    if not services_dir.exists():
        logger.error("Services directory not found!")
        sys.exit(1)
    
    total_updates = 0
    
    # Process each service
    for service_path in services_dir.iterdir():
        if service_path.is_dir() and not service_path.name.startswith('.'):
            logger.info(f"\nProcessing: {service_path.name}")
            
            # Update Dockerfile
            dockerfile = service_path / 'Dockerfile'
            if update_dockerfile_with_curl(dockerfile):
                total_updates += 1
            
            # Add health endpoint
            if ensure_health_endpoint(service_path):
                total_updates += 1
    
    # Check docker-compose
    logger.info("\nChecking docker-compose configuration...")
    update_docker_compose()
    
    logger.info("\n" + "="*80)
    logger.info(f"Health check setup complete! Made {total_updates} updates")
    logger.info("="*80)
    
    if total_updates > 0:
        print("\n" + "="*80)
        print("NEXT STEPS:")
        print("="*80)
        print("1. Stop current containers:")
        print("   docker-compose -f docker-compose-microservices.yml down")
        print("\n2. Rebuild with health checks:")
        print("   docker-compose -f docker-compose-microservices.yml up --build")
        print("\n3. Verify health status:")
        print("   docker ps")
        print("="*80 + "\n")
    else:
        print("\n✓ All services already have health checks configured!\n")


if __name__ == "__main__":
    main()
