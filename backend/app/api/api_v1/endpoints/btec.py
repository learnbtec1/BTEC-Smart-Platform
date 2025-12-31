from fastapi import APIRouter, UploadFile, File, Form
from app.btec_engine.text_evaluator import evaluate_text
from app.btec_engine.audio_evaluator import transcribe_audio
import tempfile
import os

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/assessments/", response_model=schemas.BTECAssessment)
def create_assessment(
    *,
    assessment_in: schemas.BTECAssessmentCreate,
    db: deps.SessionDep,
    current_user: deps.CurrentUser,
):
    """
    Create a new BTEC assessment.
    """
    assessment = crud.create_btec_assessment(
        session=db, assessment_in=assessment_in, owner_id=current_user.id
    )
    return assessment


@router.post("/evaluate/text")
async def evaluate_text_endpoint(
    student_answer: str = Form(...),
    model_answer: str = Form(...),
):
    """
    Evaluate similarity between student answer and model answer.
    """
    result = evaluate_text(student_answer, model_answer)
    return {"status": "ok", "data": result}


@router.post("/evaluate/audio")
async def evaluate_audio_endpoint(file: UploadFile = File(...)):
    """
    Transcribe audio using Whisper and return text.
    """
    # Save uploaded file temporarily
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Transcribe
    text = transcribe_audio(tmp_path)

    # Cleanup
    os.remove(tmp_path)

    return {"status": "ok", "transcript": text}
