import time, requests, sys
from datetime import datetime

SERVICES = [
    ("Gateway", "http://localhost/health"),
    ("Example Service", "http://localhost:8000/health")
]

print("="*80)
print(" MICROSERVICES HEALTH MONITOR - CONTINUOUS MODE")
print("="*80)
print("Press Ctrl+C to stop\n")

try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{timestamp}]")
        print("-"*80)
        
        all_healthy = True
        for name, url in SERVICES:
            try:
                start = time.time()
                r = requests.get(url, timeout=2)
                elapsed = (time.time() - start) * 1000
                if r.status_code == 200:
                    print(f"✓ HEALTHY   | {name:20} | {elapsed:.2f}ms | {url}")
                else:
                    print(f"✗ UNHEALTHY | {name:20} | HTTP {r.status_code} | {url}")
                    all_healthy = False
            except requests.exceptions.ConnectionError:
                print(f"✗ DOWN      | {name:20} | Connection refused | {url}")
                all_healthy = False
            except requests.exceptions.Timeout:
                print(f"✗ TIMEOUT   | {name:20} | Request timeout | {url}")
                all_healthy = False
            except Exception as e:
                print(f"✗ ERROR     | {name:20} | {str(e)[:30]} | {url}")
                all_healthy = False
        
        if all_healthy:
            print("\n✓ All services healthy")
        else:
            print("\n⚠️  Some services are unhealthy")
        
        print("\nNext check in 10 seconds...")
        time.sleep(10)
        
except KeyboardInterrupt:
    print("\n\n" + "="*80)
    print(" Monitoring stopped by user")
    print("="*80 + "\n")
    sys.exit(0)
