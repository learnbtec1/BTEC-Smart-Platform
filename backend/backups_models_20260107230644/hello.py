from typing import Dict


def say_hello(name: str) -> Dict[str, str]:
    """Simple example service used by API and tests."""
    return {"message": f"Hello, {name}!"}
