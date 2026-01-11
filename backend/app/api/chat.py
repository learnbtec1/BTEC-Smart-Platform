from fastapi import APIRouter
from ..schemas import ChatIn

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
async def chat_endpoint(payload: ChatIn):
    return {"answer": f"Received: {payload.q}"}
