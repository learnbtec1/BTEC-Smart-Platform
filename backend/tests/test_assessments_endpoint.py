def test_assessments_endpoint_post(client):
    payload = {
        "question": "Describe the value chain of a small retail business.",
        "level": "L2",
        "major": "Business",
    }

    r = client.post("/api/v1/assessments/", json=payload)
    assert r.status_code == 200, f"Unexpected status: {r.status_code} - {r.text}"
    data = r.json()
    assert data["question"] == payload["question"]
    assert data["level"] == payload["level"]
    assert data["major"] == payload["major"]
    assert isinstance(data.get("difficulty_score"), int)
    assert isinstance(data.get("advice"), str)
