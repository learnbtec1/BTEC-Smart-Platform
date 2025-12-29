
import yaml
import os

compose_file = "docker-compose-microservices.yml"
services_dir = "services"
log_file = "setup.log"

def log_action(message):
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(message + "\n")
    print(message)

def read_ports_from_compose():
    with open(compose_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    ports_map = {}
    for service, details in data.get("services", {}).items():
        ports = details.get("ports", [])
        if ports:
            # أخذ أول منفذ قبل النقطتين
            port = ports[0].split(":")[-1]
            ports_map[service] = port
    return ports_map

def add_healthcheck(dockerfile_path, port):
    healthcheck_text = f"""
# إضافة فحص الصحة تلقائيًا
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:{port}/health || exit 1
"""
    with open(dockerfile_path, "r+", encoding="utf-8") as file:
        content = file.read()
        if "HEALTHCHECK" not in content:
            file.write("\n" + healthcheck_text)
            log_action(f"✅ تم إضافة فحص الصحة إلى: {dockerfile_path} (المنفذ {port})")
        else:
            log_action(f"⚠️ الملف يحتوي بالفعل على HEALTHCHECK: {dockerfile_path}")

def process_services(ports_map):
    for service, port in ports_map.items():
        dockerfile_path = os.path.join(services_dir, service, "Dockerfile")
        if os.path.exists(dockerfile_path):
            add_healthcheck(dockerfile_path, port)
        else:
            log_action(f"❌ لم يتم العثور على Dockerfile للخدمة: {service}")

if __name__ == "__main__":
    ports_map = read_ports_from_compose()
    process_services(ports_map)
