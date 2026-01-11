from app.main import app
from fastapi.testclient import TestClient
from app.core.config import settings

client = TestClient(app)
resp = client.post(f"{settings.API_V1_STR}/login/access-token", data={"username": settings.FIRST_SUPERUSER, "password": settings.FIRST_SUPERUSER_PASSWORD})
print('status', resp.status_code)
print('body', resp.text)
if resp.status_code == 200:
    import jwt
    token = resp.json().get('access_token')
    print('token raw:', token)
    print('decoded:', jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256']))
