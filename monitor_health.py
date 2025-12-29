#!/usr/bin/env python3
"""
Monitor Health - Real-time health monitoring of all microservices
"""

import requests
import time
import sys
from datetime import datetime

def check_health(service_name, url):
    """Check health of a service"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return "✓ HEALTHY", response.elapsed.total_seconds() * 1000
        else:
            return f"✗ UNHEALTHY ({response.status_code})", 0
    except requests.exceptions.ConnectionError:
        return "✗ UNREACHABLE", 0
    except requests.exceptions.Timeout:
        return "✗ TIMEOUT", 0
    except Exception as e:
        return f"✗ ERROR: {str(e)}", 0

def monitor():
    """Monitor all services"""
    services = {
        "Gateway": "http://localhost/health",
        "Example Service": "http://localhost:8000/health"
    }
    
    print("\n" + "="*80)
    print(" MICROSERVICES HEALTH MONITOR")
    print("="*80)
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[{timestamp}]")
            print("-"*80)
            
            all_healthy = True
            
            for service_name, url in services.items():
                status, response_time = check_health(service_name, url)
                
                if "HEALTHY" in status:
                    print(f"{status:20} | {service_name:20} | {response_time:.2f}ms | {url}")
                else:
                    print(f"{status:20} | {service_name:20} | {url}")
                    all_healthy = False
            
            if all_healthy:
                print("\n✓ All services are healthy!")
            else:
                print("\n⚠️  Some services are unhealthy!")
            
            print("\nNext check in 10 seconds...")
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n\n" + "="*80)
        print(" Monitoring stopped")
        print("="*80 + "\n")

if __name__ == "__main__":
    monitor()
