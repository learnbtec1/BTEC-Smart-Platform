from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
import os
import httpx
from typing import Optional, List
import uuid
from logging import getLogger

# typing for DB session
from sqlmodel import Session

logger = getLogger(__name__)

# Attempt absolute imports (when running as package) then fallback to relative
try:
    from app.schemas import ChatIn  # optional convenience
except Exception:
    try:
        from ..schemas import ChatIn  # relative fallback
    except Exception:
        class ChatIn(BaseModel):
            q: str

# CRUD helpers (create_message, get_messages_by_session)
try:
    from app.crud import create_message, get_messages_by_session
except Exception:
    try:
        from ..crud import create_message, get_messages_by_session
    except Exception:
        create_message = None
        get_messages_by_session = None

# DB dependency
try:
    from app.database import get_db
except Exception:
    try:
        from ..database import get_db
    except Exception:
        get_db = None

# Authentication dependency (optional)
try:
    from app.api.auth import get_current_user
except Exception:
    try:
        from ..api.auth import get_current_user
    except Exception:
        # fallback: noop dependency for testing (returns None)
        def get_current_user():
            return None

router = APIRouter(prefix="/chat", tags=["chat"])

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

SYSTEM_PROMPT = (
    "You are an expert tutor. Answer concisely in Arabic (or the user's language) "
    "with clear explanations and examples when relevant. Keep a helpful and friendly tone."
)

class ChatPayload(BaseModel):
    q: str
    session_id: Optional[str] = None

@router.post("/", status_code=200)
async def chat_endpoint(
    payload: ChatPayload,
    db: "Session" = Depends(get_db) if get_db else None,
    current_user = Depends(get_current_user)
):
    q = (payload.q or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="Empty question")

    session_id = payload.session_id or str(uuid.uuid4())

    # Save user's message (best-effort; failures don't block the response)
    try:
        if create_message and db is not None:
            user_id = getattr(current_user, "id", None) if current_user else None
            create_message(db=db, user_id=user_id, session_id=session_id, role="user", content=q)
    except Exception as e:
        logger.exception("Failed to save user message: %s", e)

    # Build context: system prompt + conversation history (if available)
    messages: List[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
    try:
        if get_messages_by_session and db is not None:
            history = get_messages_by_session(db=db, session_id=session_id, limit=20)
            for h in history:
                # support ORM objects or dict-like
                role = getattr(h, "role", None) or (h.get("role") if isinstance(h, dict) else None)
                content = getattr(h, "content", None) or (h.get("content") if isinstance(h, dict) else None)
                if role and content:
                    messages.append({"role": role, "content": content})
    except Exception as e:
        logger.exception("Failed to load history: %s", e)

    # Call LLM provider (OpenAI by default)
    if LLM_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OpenAI API key not configured on the server."
            )

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        body = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": 800,
            "temperature": 0.2,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.post(url, json=body, headers=headers)
            except httpx.RequestError as e:
                logger.exception("LLM request failed: %s", e)
                raise HTTPException(status_code=502, detail=f"LLM request failed: {e}") from e

        if resp.status_code != 200:
            logger.error("LLM returned non-200: %s %s", resp.status_code, resp.text)
            raise HTTPException(status_code=502, detail={"llm_status": resp.status_code, "body": resp.text})

        data = resp.json()
        try:
            assistant_text = data["choices"][0]["message"]["content"]
        except Exception:
            logger.exception("Unexpected LLM response structure: %s", data)
            raise HTTPException(status_code=502, detail="Unexpected LLM response structure")

        # Save assistant reply
        try:
            if create_message and db is not None:
                user_id = getattr(current_user, "id", None) if current_user else None
                create_message(db=db, user_id=user_id, session_id=session_id, role="assistant", content=assistant_text)
        except Exception as e:
            logger.exception("Failed to save assistant message: %s", e)

        return {"answer": assistant_text, "session_id": session_id, "raw": data}

    else:
        # Local stub fallback
        answer = f"(local stub) Received: {q}"
        try:
            if create_message and db is not None:
                user_id = getattr(current_user, "id", None) if current_user else None
                create_message(db=db, user_id=user_id, session_id=session_id, role="assistant", content=answer)
        except Exception as e:
            logger.exception("Failed to save assistant stub message: %s", e)
        return {"answer": answer, "session_id": session_id}