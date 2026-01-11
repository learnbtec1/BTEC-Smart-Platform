from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings


def run():
    client = TestClient(app)
    login_data = {"username": settings.FIRST_SUPERUSER, "password": settings.FIRST_SUPERUSER_PASSWORD}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    print("login status:", r.status_code)
    print(r.text)
    if r.status_code == 200:
        token = r.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        rt = client.post(f"{settings.API_V1_STR}/login/test-token", headers=headers)
        print("test-token status:", rt.status_code)
        print(rt.text)


if __name__ == '__main__':
    run()
