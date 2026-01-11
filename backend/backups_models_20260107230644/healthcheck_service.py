from typing import Dict

def get_health_status() -> Dict[str, str]:
    """Return a minimal health status dictionary.

    Keep logic here so the route stays thin. Expand with DB/queue checks later.
    """
    # Placeholder checks; expand with real integrations as needed
    status = {
        "status": "ok",
        "database": "unknown",
        "dependencies": "ok",
    }
    return status
