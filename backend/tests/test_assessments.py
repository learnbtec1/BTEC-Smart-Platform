from app.services.assessments import assess_question
from app.core.config import settings


def test_assess_question_basic():
    q = "Explain the differences between profit and revenue."
    res = assess_question(q, "L2", "Business")
    assert res["question"] == q
    assert res["level"] == "L2"
    assert res["major"] == "Business"
    assert isinstance(res["difficulty_score"], int)
    assert "Business" in res["advice"] or "business" in res["advice"].lower()
