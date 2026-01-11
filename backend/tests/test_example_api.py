from fastapi.testclient import TestClient

from app.core.config import settings


def test_create_and_list_example(client: TestClient, superuser_token_headers: dict[str, str]):
    headers = superuser_token_headers
    # create item
    payload = {"title": "Test Item", "description": "An example"}
    r = client.post(f"{settings.API_V1_STR}/example/", json=payload, headers=headers)
    assert r.status_code == 200
    created = r.json()
    assert created["title"] == "Test Item"

    # list items
    r = client.get(f"{settings.API_V1_STR}/example/", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(item["title"] == "Test Item" for item in data)
