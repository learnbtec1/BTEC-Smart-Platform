from typing import Literal, TypedDict
from sqlmodel import Session

from app.schemas import Assessment, AssessmentCreate


class AssessmentResult(TypedDict):
    question: str
    level: str
    major: str
    difficulty_score: int
    advice: str


def assess_question(question: str, level: Literal["L2", "L3"], major: Literal["Business", "IT"]) -> AssessmentResult:
    """Lightweight assessment logic used for tests and example scaffolding.

    Returns a small dict with a computed difficulty score and short advice.
    Keep logic simple so service is easy to unit test and extend.
    """
    base = 50 if level == "L2" else 70
    major_adj = -10 if major == "Business" else 0
    length_adj = min(len(question) // 20, 20)
    difficulty = max(0, min(100, base + major_adj + length_adj))

    advice = (
        "Focus on clear, concrete examples for Business learners."
        if major == "Business"
        else "Include technical steps and expected outputs for IT learners."
    )

    return {
        "question": question,
        "level": level,
        "major": major,
        "difficulty_score": difficulty,
        "advice": advice,
    }


def create_assessment(session: Session, question: str, level: str, major: str, difficulty_score: int | None, advice: str | None, owner_id=None) -> Assessment:
    """Persist the assessment result and return the created model."""
    assessment_in = AssessmentCreate(
        question=question,
        level=level,
        major=major,
        difficulty_score=difficulty_score,
        advice=advice,
    )
    # Use SQLModel's model_dump() to build dict for SQLModel object (dict() is deprecated)
    assessment = Assessment(**assessment_in.model_dump(), owner_id=owner_id)
    session.add(assessment)
    session.commit()
    session.refresh(assessment)
    return assessment
