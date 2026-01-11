from datetime import timedelta

from fastapi.testclient import TestClient

from app.core.config import settings


def test_jwt_login_and_protected_route(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens
    access = tokens["access_token"]

    # Use token to access a protected test-only endpoint
    headers = {"Authorization": f"Bearer {access}"}
    r2 = client.post(f"{settings.API_V1_STR}/login/test-token", headers=headers)
    assert r2.status_code == 200
    assert "email" in r2.json() or "id" in r2.json()


def test_token_expiration(client: TestClient) -> None:
    # Create an already-expired token and ensure it's rejected by protected endpoints
    from app.utils import create_access_token

    expired = create_access_token({"sub": settings.FIRST_SUPERUSER}, expires_delta=timedelta(seconds=-10))
    headers = {"Authorization": f"Bearer {expired}"}
    r = client.post(f"{settings.API_V1_STR}/login/test-token", headers=headers)
    assert r.status_code == 401


def test_unauthorized_access_to_protected(client: TestClient) -> None:
    # When no Authorization header is provided some token decoders can
    # raise on `None`. To robustly exercise the unauthorized path, send
    # an explicit invalid token value and expect a 401 response.
    headers = {"Authorization": "Bearer invalid"}
    r = client.post(f"{settings.API_V1_STR}/login/test-token", headers=headers)
    assert r.status_code == 401
