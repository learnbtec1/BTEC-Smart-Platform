from backend.app.services.example import get_example, create_example


def test_get_example():
    res = get_example("42")
    assert res["id"] == "42"
    assert "Example" in res["text"]


def test_create_example():
    payload = {"name": "test", "meta": {"a": 1}}
    res = create_example(payload)
    assert res["id"] == "generated-id"
    assert res["payload"]["name"] == "test"
