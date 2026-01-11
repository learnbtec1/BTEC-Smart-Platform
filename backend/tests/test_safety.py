from app.safety import evaluate_safety


def test_safety_ok() -> None:
    data = {"steps": [{"safety_ok": True}, {"safety_ok": True}]}
    res = evaluate_safety(data)
    assert res["status"] == "OK"


def test_safety_skipped_step() -> None:
    data = {"steps": [{"safety_ok": True}, {"skipped": True}, {"safety_ok": True}]}
    res = evaluate_safety(data)
    assert res["status"] == "Critical Failure"
    assert "skipped" in res["reason"]


def test_safety_explicit_failure() -> None:
    data = {"steps": [{"safety_ok": True}, {"safety_ok": False}]}
    res = evaluate_safety(data)
    assert res["status"] == "Critical Failure"
    assert "safety_failed" in res["reason"]
