#!/usr/bin/env python3
"""
Generate secure secrets for GitHub Actions and local development
"""

import secrets
import string
from pathlib import Path

def generate_secret(length=32):
    """Generate a cryptographically secure random secret"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_jwt_secret():
    """Generate JWT secret key"""
    return secrets.token_hex(32)

def generate_env_template():
    """Generate .env template file"""
    template = f"""# Auto-generated environment variables template
# Copy this to .env and fill in your values

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/btec_db
DB_USER=admin
DB_PASSWORD={generate_secret(16)}

# Redis Configuration
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD={generate_secret(16)}

# Security Keys (CHANGE THESE IN PRODUCTION!)
JWT_SECRET_KEY={generate_jwt_secret()}
SECRET_KEY={generate_jwt_secret()}
API_KEY={generate_secret(32)}

# Gateway Configuration
GATEWAY_SECRET={generate_secret(32)}

# Docker Hub (Optional - for CI/CD)
DOCKER_USERNAME=your_dockerhub_username
DOCKER_PASSWORD=your_dockerhub_token

# Service Ports (for local development)
GATEWAY_PORT=80
EXAMPLE_SERVICE_PORT=8000

# Environment
ENVIRONMENT=development
DEBUG=True
"""
    return template

def generate_secrets_list():
    """Generate list of secrets to add to GitHub"""
    secrets_list = {
        'JWT_SECRET_KEY': generate_jwt_secret(),
        'SECRET_KEY': generate_jwt_secret(),
        'API_KEY': generate_secret(32),
        'GATEWAY_SECRET': generate_secret(32),
        'DB_PASSWORD': generate_secret(16),
        'REDIS_PASSWORD': generate_secret(16),
    }
    return secrets_list

def main():
    print("="*80)
    print(" GENERATE SECURE SECRETS FOR GITHUB ACTIONS")
    print("="*80)
    print()
    
    # Generate .env.example
    env_template = generate_env_template()
    env_example_path = Path('.env.example')
    env_example_path.write_text(env_template, encoding='utf-8')
    print(f"✓ Created {env_example_path}")
    
    # Generate secrets for GitHub
    print("\n" + "="*80)
    print(" SECRETS TO ADD TO GITHUB ACTIONS")
    print("="*80)
    print("\nGo to: Settings → Secrets and variables → Actions → New repository secret")
    print("\nAdd these secrets:\n")
    
    secrets_list = generate_secrets_list()
    for name, value in secrets_list.items():
        print(f"Name:  {name}")
        print(f"Value: {value}")
        print()
    
    # Save to file for reference
    secrets_file = Path('GENERATED_SECRETS.txt')
    with open(secrets_file, 'w', encoding='utf-8') as f:
        f.write("GITHUB ACTIONS SECRETS\n")
        f.write("="*80 + "\n\n")
        f.write("⚠️  WARNING: Keep this file secure and delete after adding to GitHub!\n\n")
        for name, value in secrets_list.items():
            f.write(f"{name}={value}\n")
    
    print("="*80)
    print(f"✓ Secrets also saved to: {secrets_file}")
    print("⚠️  WARNING: Delete GENERATED_SECRETS.txt after adding to GitHub!")
    print("="*80)
    
    # Create .gitignore entry
    gitignore_path = Path('.gitignore')
    gitignore_entries = """
# Environment variables and secrets
.env
.env.local
.env.*.local
GENERATED_SECRETS.txt
secrets/
*.key
*.pem

# Logs
*.log
setup.log
health_check.log
"""
    
    if gitignore_path.exists():
        current_content = gitignore_path.read_text(encoding='utf-8')
        if '.env' not in current_content:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write(gitignore_entries)
            print(f"\n✓ Updated {gitignore_path} with secret patterns")
    else:
        gitignore_path.write_text(gitignore_entries, encoding='utf-8')
        print(f"\n✓ Created {gitignore_path}")
    
    print("\n" + "="*80)
    print(" NEXT STEPS:")
    print("="*80)
    print("1. Copy .env.example to .env and customize for local development")
    print("2. Add secrets to GitHub: Settings → Secrets → Actions → New secret")
    print("3. Delete GENERATED_SECRETS.txt after adding to GitHub")
    print("4. Never commit .env or GENERATED_SECRETS.txt to git")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
