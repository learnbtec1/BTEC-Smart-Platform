from typing import List, Optional
from sqlmodel import Session
from app.models import StudentProgress
from datetime import datetime


def greet_student(name: str) -> str:
    return f"Hello {name}! Welcome back to the BTEC Virtual Tutor. How can I help you learn today?"


def recommend_learning(session: Session, student_id: Optional[str] = None) -> List[str]:
    """Return simple recommendations based on stored progress.

    If student_id is provided, use their progress to tailor recommendations.
    """
    recommendations: List[str] = []
    if student_id is None:
        # generic recommendations
        return [
            "Start with the fundamentals module for your course.",
            "Try a short practice quiz every day (10-15 minutes).",
            "Review feedback from previous tasks and focus on weak areas.",
        ]

    stmt = session.query(StudentProgress).filter(StudentProgress.student_id == student_id)
    progress_rows = stmt.all()
    if not progress_rows:
        return [
            "We don't have progress for you yet — begin with the diagnostic test.",
            "Try the fundamentals module to build a baseline.",
        ]

    # compute average progress across courses
    avg = sum(p.progress for p in progress_rows) / len(progress_rows)

    if avg < 40.0:
        recommendations.append("Focus on core concepts: watch short videos and complete guided exercises.")
        recommendations.append("Schedule daily 15-20 minute practice sessions.")
    elif avg < 75.0:
        recommendations.append("You're progressing well — try mixed practice and timed quizzes.")
        recommendations.append("Work on project-based assignments to apply concepts.")
    else:
        recommendations.append("Great progress! Attempt advanced modules and challenge problems.")
        recommendations.append("Consider mentoring peers to deepen understanding.")

    # course-specific tip example (pick lowest performing course)
    lowest = min(progress_rows, key=lambda r: r.progress)
    if lowest and lowest.progress < 60.0:
        recommendations.append(f"Spend extra practice time on '{lowest.course}' (current {lowest.progress:.0f}%).")

    # If any course is very low, explicitly suggest an intervention plan
    struggles = [p for p in progress_rows if p.progress < 40.0]
    if struggles:
        for s in struggles:
            recommendations.append(
                f"You're struggling with '{s.course}' ({s.progress:.0f}%). Try the guided module and request tutor help."
            )

    return recommendations


def record_progress(session: Session, student_id: str, course: str, progress: float) -> StudentProgress:
    # try to find existing record
    obj = (
        session.query(StudentProgress)
        .filter(StudentProgress.student_id == student_id)
        .filter(StudentProgress.course == course)
        .first()
    )
    if obj:
        obj.progress = progress
        obj.last_updated = datetime.utcnow()
    else:
        obj = StudentProgress(student_id=student_id, course=course, progress=progress)
        session.add(obj)

    session.commit()
    session.refresh(obj)
    return obj


def get_progress(session: Session, student_id: int) -> List[StudentProgress]:
    return session.query(StudentProgress).filter(StudentProgress.student_id == student_id).all()
