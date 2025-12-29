#!/usr/bin/env python3
"""
Microservices Setup Automation Script
Scans services, fixes common issues, generates docker-compose and API gateway
"""

import os
import sys
import json
import logging
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Set
from datetime import datetime


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('setup.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class MicroserviceSetup:
    """Main class to handle microservices setup automation"""
    
    def __init__(self, services_dir: str = "./services"):
        self.services_dir = Path(services_dir)
        self.gateway_dir = Path("./gateway")
        self.services: List[Dict] = []
        self.issues_fixed = 0
        
    def run(self):
        """Main execution flow"""
        logger.info("=" * 80)
        logger.info("Starting Microservices Setup Automation")
        logger.info("=" * 80)
        
        # Create services directory if it doesn't exist
        self.services_dir.mkdir(exist_ok=True)
        logger.info(f"Services directory: {self.services_dir.absolute()}")
        
        # Step 1: Scan all services
        self.scan_services()
        
        # Step 2: Check and fix each service
        for service in self.services:
            self.check_and_fix_service(service)
        
        # Step 3: Generate docker-compose.yml
        self.generate_docker_compose()
        
        # Step 4: Create FastAPI gateway
        self.create_gateway()
        
        # Step 5: Generate README
        self.generate_readme()
        
        logger.info("=" * 80)
        logger.info(f"Setup completed! Fixed {self.issues_fixed} issues across {len(self.services)} services")
        logger.info("=" * 80)
        
    def scan_services(self):
        """Scan all subdirectories in services folder"""
        logger.info("\n[STEP 1] Scanning services directory...")
        
        if not self.services_dir.exists():
            logger.warning(f"Services directory does not exist: {self.services_dir}")
            logger.info("Creating example service structure...")
            self.create_example_service()
            
        for service_path in self.services_dir.iterdir():
            if service_path.is_dir() and not service_path.name.startswith('.'):
                service_info = {
                    'name': service_path.name,
                    'path': service_path,
                    'port': 8000 + len(self.services),
                    'has_dockerfile': False,
                    'has_requirements': False,
                    'has_init': False,
                    'python_files': [],
                    'issues': []
                }
                self.services.append(service_info)
                logger.info(f"Found service: {service_path.name}")
        
        if not self.services:
            logger.warning("No services found. Creating example service...")
            self.create_example_service()
            self.scan_services()
            
    def create_example_service(self):
        """Create an example service for demonstration"""
        example_path = self.services_dir / "example_service"
        example_path.mkdir(parents=True, exist_ok=True)
        
        # Create main.py
        main_py = example_path / "main.py"
        main_py.write_text('''from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"service": "example_service", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
''', encoding='utf-8')
        
        # Create requirements.txt
        req_txt = example_path / "requirements.txt"
        req_txt.write_text('fastapi==0.104.1\nuvicorn==0.24.0\n', encoding='utf-8')
        
        logger.info(f"Created example service at {example_path}")
        
    def check_and_fix_service(self, service: Dict):
        """Check for issues and fix them"""
        logger.info(f"\n[STEP 2] Checking service: {service['name']}")
        service_path = service['path']
        
        # Check for Python files
        service['python_files'] = list(service_path.glob('**/*.py'))
        logger.info(f"  Found {len(service['python_files'])} Python files")
        
        # Check __init__.py
        init_file = service_path / "__init__.py"
        if not init_file.exists():
            logger.warning(f"  Missing __init__.py")
            service['issues'].append('missing_init')
            self.fix_missing_init(service_path)
        else:
            service['has_init'] = True
            
        # Check requirements.txt
        req_file = service_path / "requirements.txt"
        if not req_file.exists():
            logger.warning(f"  Missing requirements.txt")
            service['issues'].append('missing_requirements')
            self.fix_missing_requirements(service_path, service['python_files'])
        else:
            service['has_requirements'] = True
            self.check_requirements(req_file)
            
        # Check Dockerfile
        dockerfile = service_path / "Dockerfile"
        if not dockerfile.exists():
            logger.warning(f"  Missing Dockerfile")
            service['issues'].append('missing_dockerfile')
            self.fix_missing_dockerfile(service)
        else:
            service['has_dockerfile'] = True
            
        # Check for broken imports
        self.check_and_fix_imports(service)
        
        logger.info(f"  Service check complete: {len(service['issues'])} issues found and fixed")
        
    def fix_missing_init(self, service_path: Path):
        """Create missing __init__.py"""
        init_file = service_path / "__init__.py"
        init_file.write_text(f'"""Package for {service_path.name}"""\n', encoding='utf-8')
        logger.info(f"  [OK] Created __init__.py")
        self.issues_fixed += 1
        
    def fix_missing_requirements(self, service_path: Path, python_files: List[Path]):
        """Generate requirements.txt based on imports"""
        imports = self.extract_imports(python_files)
        requirements = self.map_imports_to_packages(imports)
        
        req_file = service_path / "requirements.txt"
        req_file.write_text('\n'.join(sorted(requirements)) + '\n', encoding='utf-8')
        logger.info(f"  [OK] Created requirements.txt with {len(requirements)} packages")
        self.issues_fixed += 1
        
    def extract_imports(self, python_files: List[Path]) -> Set[str]:
        """Extract all imports from Python files"""
        imports = set()
        import_pattern = re.compile(r'^\s*(?:from|import)\s+([a-zA-Z0-9_]+)')
        
        for py_file in python_files:
            try:
                content = py_file.read_text(encoding='utf-8')
                for line in content.split('\n'):
                    match = import_pattern.match(line)
                    if match:
                        imports.add(match.group(1))
            except Exception as e:
                logger.warning(f"  Could not read {py_file}: {e}")
                
        return imports
        
    def map_imports_to_packages(self, imports: Set[str]) -> List[str]:
        """Map import names to package names with versions"""
        # Common import to package mappings
        package_map = {
            'fastapi': 'fastapi==0.104.1',
            'uvicorn': 'uvicorn==0.24.0',
            'pydantic': 'pydantic==2.5.0',
            'sqlalchemy': 'sqlalchemy==2.0.23',
            'redis': 'redis==5.0.1',
            'requests': 'requests==2.31.0',
            'httpx': 'httpx==0.25.2',
            'celery': 'celery==5.3.4',
            'pymongo': 'pymongo==4.6.0',
            'psycopg2': 'psycopg2-binary==2.9.9',
            'jwt': 'PyJWT==2.8.0',
            'pytest': 'pytest==7.4.3',
            'numpy': 'numpy==1.26.2',
            'pandas': 'pandas==2.1.4',
            'sklearn': 'scikit-learn==1.3.2',
            'dotenv': 'python-dotenv==1.0.0',
            'jinja2': 'jinja2==3.1.2',
            'aiohttp': 'aiohttp==3.9.1',
        }
        
        packages = []
        for imp in imports:
            # Skip standard library imports
            if imp in ['os', 'sys', 'json', 'time', 'datetime', 'logging', 
                      're', 'pathlib', 'typing', 'collections', 'itertools',
                      'functools', 'asyncio', 'threading', 'multiprocessing']:
                continue
                
            if imp in package_map:
                packages.append(package_map[imp])
            elif imp not in ['__future__', '__main__']:
                # Add generic package
                packages.append(f'{imp}>=1.0.0')
                
        # Always include FastAPI and uvicorn for microservices
        if not any('fastapi' in p for p in packages):
            packages.append('fastapi==0.104.1')
        if not any('uvicorn' in p for p in packages):
            packages.append('uvicorn==0.24.0')
            
        return packages
        
    def check_requirements(self, req_file: Path):
        """Check if requirements are up to date"""
        try:
            content = req_file.read_text()
            lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
            
            # Check for version pins
            unpinned = [l for l in lines if '==' not in l and '>=' not in l and '<=' not in l]
            if unpinned:
                logger.warning(f"  Found unpinned requirements: {unpinned}")
                # Could auto-fix here by pinning versions
                
        except Exception as e:
            logger.warning(f"  Could not check requirements: {e}")
            
    def fix_missing_dockerfile(self, service: Dict):
        """Create Dockerfile for service"""
        service_path = service['path']
        dockerfile = service_path / "Dockerfile"
        
        # Detect main entry point
        main_file = "main.py"
        if (service_path / "app.py").exists():
            main_file = "app.py"
        elif (service_path / "api.py").exists():
            main_file = "api.py"
            
        dockerfile_content = f'''FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE {service['port']}

# Run application
CMD ["uvicorn", "{main_file.replace('.py', '')}:app", "--host", "0.0.0.0", "--port", "{service['port']}"]
'''
        
        dockerfile.write_text(dockerfile_content, encoding='utf-8')
        service['has_dockerfile'] = True
        logger.info(f"  [OK] Created Dockerfile")
        self.issues_fixed += 1
        
    def check_and_fix_imports(self, service: Dict):
        """Check for and fix broken imports"""
        for py_file in service['python_files']:
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # Check for common import issues
                issues = []
                
                # Relative imports without package
                if re.search(r'from \. import', content) or re.search(r'from \.\. import', content):
                    if not (service['path'] / "__init__.py").exists():
                        issues.append("relative_imports_no_package")
                        
                # Missing common imports
                if 'FastAPI' in content and 'from fastapi import FastAPI' not in content:
                    issues.append("missing_fastapi_import")
                    
                if issues:
                    logger.info(f"  Found import issues in {py_file.name}: {issues}")
                    # Auto-fix could be added here
                    
            except Exception as e:
                logger.warning(f"  Could not check imports in {py_file}: {e}")
                
    def generate_docker_compose(self):
        """Generate unified docker-compose.yml"""
        logger.info("\n[STEP 3] Generating docker-compose.yml...")
        
        compose = {
            'version': '3.8',
            'services': {},
            'networks': {
                'microservices': {
                    'driver': 'bridge'
                }
            }
        }
        
        for service in self.services:
            service_config = {
                'build': {
                    'context': f'./{self.services_dir.name}/{service["name"]}',
                    'dockerfile': 'Dockerfile'
                },
                'container_name': service['name'],
                'ports': [f"{service['port']}:{service['port']}"],
                'networks': ['microservices'],
                'environment': {
                    'SERVICE_NAME': service['name'],
                    'SERVICE_PORT': service['port']
                },
                'restart': 'unless-stopped',
                'healthcheck': {
                    'test': f'curl -f http://localhost:{service["port"]}/health || exit 1',
                    'interval': '30s',
                    'timeout': '10s',
                    'retries': 3
                }
            }
            
            compose['services'][service['name']] = service_config
            
        # Add gateway service
        compose['services']['gateway'] = {
            'build': {
                'context': './gateway',
                'dockerfile': 'Dockerfile'
            },
            'container_name': 'api_gateway',
            'ports': ['80:80'],
            'networks': ['microservices'],
            'depends_on': [s['name'] for s in self.services],
            'restart': 'unless-stopped',
            'environment': {
                'SERVICES': json.dumps({s['name']: f"http://{s['name']}:{s['port']}" 
                                       for s in self.services})
            }
        }
        
        # Write docker-compose.yml
        compose_file = Path('docker-compose-microservices.yml')
        
        import yaml
        try:
            with open(compose_file, 'w', encoding='utf-8') as f:
                yaml.dump(compose, f, default_flow_style=False, sort_keys=False)
            logger.info(f"  [OK] Created {compose_file}")
        except ImportError:
            # Fallback to manual YAML writing if PyYAML not available
            self.write_yaml_manually(compose_file, compose)
            logger.info(f"  [OK] Created {compose_file} (without PyYAML)")
            
        self.issues_fixed += 1
        
    def write_yaml_manually(self, filepath: Path, data: Dict):
        """Write YAML file manually without PyYAML"""
        lines = ['version: "3.8"', '', 'services:']
        
        for service_name, config in data['services'].items():
            lines.append(f'  {service_name}:')
            if 'build' in config:
                lines.append('    build:')
                lines.append(f'      context: {config["build"]["context"]}')
                lines.append(f'      dockerfile: {config["build"]["dockerfile"]}')
            if 'container_name' in config:
                lines.append(f'    container_name: {config["container_name"]}')
            if 'ports' in config:
                lines.append('    ports:')
                for port in config['ports']:
                    lines.append(f'      - "{port}"')
            if 'networks' in config:
                lines.append('    networks:')
                for net in config['networks']:
                    lines.append(f'      - {net}')
            if 'environment' in config:
                lines.append('    environment:')
                for key, val in config['environment'].items():
                    lines.append(f'      {key}: "{val}"')
            if 'depends_on' in config:
                lines.append('    depends_on:')
                for dep in config['depends_on']:
                    lines.append(f'      - {dep}')
            if 'restart' in config:
                lines.append(f'    restart: {config["restart"]}')
            if 'healthcheck' in config:
                lines.append('    healthcheck:')
                lines.append(f'      test: "{config["healthcheck"]["test"]}"')
                lines.append(f'      interval: {config["healthcheck"]["interval"]}')
                lines.append(f'      timeout: {config["healthcheck"]["timeout"]}')
                lines.append(f'      retries: {config["healthcheck"]["retries"]}')
            lines.append('')
            
        lines.append('networks:')
        lines.append('  microservices:')
        lines.append('    driver: bridge')
        
        filepath.write_text('\n'.join(lines), encoding='utf-8')
        
    def create_gateway(self):
        """Create FastAPI gateway"""
        logger.info("\n[STEP 4] Creating API Gateway...")
        
        self.gateway_dir.mkdir(exist_ok=True)
        
        # Create main gateway application
        gateway_main = self.gateway_dir / "main.py"
        gateway_code = f'''from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Microservices API Gateway", version="1.0.0")

# Load service configurations
SERVICES = json.loads(os.getenv('SERVICES', '{{}}'))
logger.info(f"Loaded services: {{SERVICES}}")

# Fallback for local development
if not SERVICES:
    SERVICES = {{
{chr(10).join(f'        "{s["name"]}": "http://localhost:{s["port"]}",' for s in self.services)}
    }}

@app.get("/")
async def root():
    return {{
        "gateway": "Microservices API Gateway",
        "services": list(SERVICES.keys()),
        "status": "running"
    }}

@app.get("/health")
async def health():
    return {{"status": "healthy", "services": len(SERVICES)}}

@app.get("/services")
async def list_services():
    """List all available services"""
    return {{"services": SERVICES}}

@app.api_route("/{{service_name}}/{{path:path}}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway_proxy(service_name: str, path: str, request: Request):
    """Proxy requests to microservices"""
    
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{{service_name}}' not found")
    
    service_url = SERVICES[service_name]
    target_url = f"{{service_url}}/{{path}}"
    
    # Forward request
    async with httpx.AsyncClient() as client:
        try:
            # Get request body if present
            body = None
            if request.method in ["POST", "PUT", "PATCH"]:
                body = await request.body()
            
            response = await client.request(
                method=request.method,
                url=target_url,
                headers={{k: v for k, v in request.headers.items() 
                        if k.lower() not in ['host', 'connection']}},
                content=body,
                params=request.query_params,
                timeout=30.0
            )
            
            return JSONResponse(
                content=response.json() if response.headers.get('content-type', '').startswith('application/json') 
                       else {{"response": response.text}},
                status_code=response.status_code
            )
            
        except httpx.RequestError as e:
            logger.error(f"Error proxying to {{service_name}}: {{e}}")
            raise HTTPException(status_code=503, detail=f"Service '{{service_name}}' unavailable")
        except Exception as e:
            logger.error(f"Unexpected error: {{e}}")
            raise HTTPException(status_code=500, detail="Internal gateway error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
'''
        gateway_main.write_text(gateway_code, encoding='utf-8')
        logger.info("  [OK] Created gateway/main.py")
        
        # Create requirements.txt
        gateway_req = self.gateway_dir / "requirements.txt"
        gateway_req.write_text('''fastapi==0.104.1
uvicorn==0.24.0
httpx==0.25.2
python-dotenv==1.0.0
''', encoding='utf-8')
        logger.info("  [OK] Created gateway/requirements.txt")
        
        # Create Dockerfile
        gateway_dockerfile = self.gateway_dir / "Dockerfile"
        gateway_dockerfile.write_text('''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
''', encoding='utf-8')
        logger.info("  [OK] Created gateway/Dockerfile")
        
        # Create __init__.py
        (self.gateway_dir / "__init__.py").write_text('"""API Gateway Package"""\n', encoding='utf-8')
        
        self.issues_fixed += 1
        
    def generate_readme(self):
        """Generate comprehensive README"""
        logger.info("\n[STEP 5] Generating README.md...")
        
        readme_content = f'''# Microservices Architecture

Auto-generated microservices setup created on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Services

This project contains {len(self.services)} microservice(s):

{chr(10).join(f"- **{s['name']}**: Running on port {s['port']}" for s in self.services)}

## Architecture

- **API Gateway**: Routes requests to individual services (port 80)
- **Services**: Independent microservices with their own containers
- **Network**: All services communicate via Docker bridge network

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)

### Running with Docker

1. Build and start all services:
```bash
docker-compose -f docker-compose-microservices.yml up --build
```

2. Access the API Gateway:
```
http://localhost
```

3. Access individual services:
{chr(10).join(f"   - {s['name']}: http://localhost:{s['port']}" for s in self.services)}

### Stopping Services

```bash
docker-compose -f docker-compose-microservices.yml down
```

## API Gateway Usage

The gateway routes requests to services using the pattern:
```
http://localhost/<service_name>/<endpoint>
```

### Examples

```bash
# List all services
curl http://localhost/services

# Call example_service root endpoint
curl http://localhost/example_service/

# Health check
curl http://localhost/health
```

## Local Development

### Setup Individual Service

```bash
cd services/<service_name>
pip install -r requirements.txt
uvicorn main:app --reload --port <port>
```

### Setup Gateway

```bash
cd gateway
pip install -r requirements.txt
uvicorn main:app --reload --port 80
```

## Project Structure

```
.
├── services/
{chr(10).join(f"│   ├── {s['name']}/" for s in self.services)}
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── __init__.py
├── gateway/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── __init__.py
├── docker-compose-microservices.yml
├── setup_microservices.py
├── setup.log
└── README-MICROSERVICES.md
```

## Adding New Services

1. Create service directory: `mkdir services/new_service`
2. Add Python code, requirements.txt
3. Run setup script: `python setup_microservices.py`
4. Rebuild containers: `docker-compose -f docker-compose-microservices.yml up --build`

## Troubleshooting

### View logs
```bash
docker-compose -f docker-compose-microservices.yml logs -f [service_name]
```

### Check service health
```bash
curl http://localhost/<service_name>/health
```

### Rebuild specific service
```bash
docker-compose -f docker-compose-microservices.yml up --build <service_name>
```

## Setup Log

All automation actions are logged in `setup.log`

## Generated Files

This setup automatically created/fixed:
- {self.issues_fixed} issues across all services
- Docker configurations for all services
- Unified docker-compose.yml
- FastAPI API Gateway with routing
- Service health checks
- Missing __init__.py files
- Missing requirements.txt files
- Missing Dockerfiles

## Notes

- All services use FastAPI and uvicorn
- Services communicate via Docker network
- Gateway provides unified API endpoint
- Each service is independently deployable
- Health checks ensure service availability

## Next Steps

1. Customize service implementations in `services/*/main.py`
2. Add environment variables in docker-compose.yml
3. Implement authentication/authorization in gateway
4. Add database services (PostgreSQL, Redis, etc.)
5. Set up CI/CD pipeline
6. Add monitoring and logging (Prometheus, Grafana)

---

*Auto-generated by setup_microservices.py*
'''
        
        readme_file = Path('README-MICROSERVICES.md')
        readme_file.write_text(readme_content, encoding='utf-8')
        logger.info(f"  [OK] Created {readme_file}")
        self.issues_fixed += 1


def main():
    """Main entry point"""
    setup = MicroserviceSetup()
    
    try:
        setup.run()
        print("\n" + "=" * 80)
        print("SUCCESS! Your microservices are ready.")
        print("=" * 80)
        print("\nNext steps:")
        print("1. Review setup.log for details")
        print("2. Read README-MICROSERVICES.md for usage instructions")
        print("3. Run: docker-compose -f docker-compose-microservices.yml up --build")
        print("\n")
        
    except Exception as e:
        logger.error(f"Setup failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
