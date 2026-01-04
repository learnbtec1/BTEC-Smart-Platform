import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_assistant_query():
    res = client.post("/api/v1/assistant/query", json={"prompt":"اريد خطة تعلم"})
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data

def test_health_and_files_list():
    res = client.get("/api/v1/files")
    assert res.status_code in (200,401)
