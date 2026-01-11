from fastapi.testclient import TestClient

from app.core.config import settings


def test_plagiarism_detection_high_similarity(client: TestClient, monkeypatch) -> None:
    # Mock the evaluator to return a high similarity score
    monkeypatch.setattr(
        "app.btec_engine.text_evaluator.evaluate_text",
        lambda s, m: {"similarity": 0.95, "levenshtein_ratio": 0.93},
    )

    form = {"student_answer": "same answer", "model_answer": "same answer"}
    r = client.post(f"{settings.API_V1_STR}/btec/evaluate/text", data=form)
    assert r.status_code == 200
    payload = r.json()
    assert payload["data"]["similarity"] >= 0.9


def test_plagiarism_detection_low_similarity(client: TestClient, monkeypatch) -> None:
    # Mock the evaluator used by the endpoint. The endpoint imports the
    # function directly into its module namespace, so patch that symbol.
    monkeypatch.setattr(
        "app.api.api_v1.endpoints.btec.evaluate_text",
        lambda s, m: {"similarity": 0.12, "levenshtein_ratio": 0.10},
    )

    form = {"student_answer": "different", "model_answer": "unrelated"}
    r = client.post(f"{settings.API_V1_STR}/btec/evaluate/text", data=form)
    assert r.status_code == 200
    payload = r.json()
    assert payload["data"]["similarity"] < 0.5
