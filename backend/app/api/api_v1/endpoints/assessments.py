from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from typing import Literal
from sqlmodel import Session

from app.services.assessments import assess_question, create_assessment
from app.api.deps import SessionDep

router = APIRouter()


class AssessmentRequest(BaseModel):
    question: str
    level: Literal["L2", "L3"]
    major: Literal["Business", "IT"]


@router.post("/", response_model=dict)
def assess(session: SessionDep, body: AssessmentRequest = Body(...)):
    """Assess a short question payload and return a lightweight score + advice.

    The result is persisted to the DB when a session is provided.
    """
    res = assess_question(body.question, body.level, body.major)
    # Persist the result (owner_id left as None for now)
    try:
        create_assessment(session, res["question"], res["level"], res["major"], res.get("difficulty_score"), res.get("advice"))
    except Exception:
        # best-effort persistence: don't fail the API if DB save fails
        pass
    return res
