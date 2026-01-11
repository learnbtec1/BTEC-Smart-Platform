"""Simple integration verifier: Next.js -> FastAPI assessment submission.

This script is intended to be run locally against a running backend
(`http://localhost:8000`). It performs a login to obtain a token and
submits a mock assessment payload to the BTEC assessment endpoint to
verify a successful round-trip.

Usage:
    python integration/verify_assessment_integration.py
"""
import requests
from app.core.config import settings


BASE = "http://localhost:8000"


def main():
    # Login as superuser to obtain token
    login_url = f"{BASE}{settings.API_V1_STR}/login/access-token"
    resp = requests.post(login_url, data={"username": settings.FIRST_SUPERUSER, "password": settings.FIRST_SUPERUSER_PASSWORD})
    if resp.status_code != 200:
        print("Login failed", resp.status_code, resp.text)
        return 1
    token = resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Submit a mock assessment
    url = f"{BASE}{settings.API_V1_STR}/btec/assessments/"
    payload = {"title": "Integration Test", "content": "Sample assessment content"}
    r = requests.post(url, json=payload, headers=headers)
    print("POST", url, "->", r.status_code)
    print(r.text)
    return 0 if r.status_code in (200, 201) else 2


if __name__ == "__main__":
    raise SystemExit(main())
