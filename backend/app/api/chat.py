from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatIn(BaseModel):
    q: str

@router.post("/")
async def chat_endpoint(payload: ChatIn):
    q = payload.q
    answer = f"Received: {q}. This is a placeholder response."
    return {"answer": answer}
