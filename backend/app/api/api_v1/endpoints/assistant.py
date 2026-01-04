from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Any, Dict, List

from sqlmodel import Session, select

from app.api.deps import SessionDep, CurrentUser
from app.models import User
from backend.app.models_progress import StudentProgress

router = APIRouter()


class AssistantQuery(BaseModel):
    prompt: str
    context: Dict[str, Any] = {}


@router.post("/query")
def query_assistant(body: AssistantQuery, session: Session = Depends(SessionDep), current_user: User = Depends(CurrentUser)) -> Dict[str, Any]:
    prompt = body.prompt.lower()
    answer = "هذه إجابة تجريبية من مساعد قيتاغورس."
    recommendations: List[Dict[str, Any]] = []
    actions: List[Dict[str, Any]] = []

    # example: check struggling modules
    stmt = select(StudentProgress).where(StudentProgress.user_id == str(current_user.id))
    progress_rows = session.exec(stmt).all()
    weak = [p for p in progress_rows if p.progress_percentage < 60 or p.struggling]
    if weak:
        for p in weak:
            recommendations.append({"module_name": getattr(p, "lesson_id", None) or "عام", "suggestion": "راجع الأساسيات وابدأ بتمارين تطبيقية"})
    if "خطة" in prompt or "تعلم" in prompt:
        recommendations.append({"type": "plan", "text": "اقترح خطة 4 أسابيع: أسبوع أساسيات، أسبوع تطبيق، أسبوع تقييم، أسبوع مراجعة"})
        actions.append({"type": "start_course", "target": "course_basic"})
    return {"answer": answer, "recommendations": recommendations, "actions": actions}
