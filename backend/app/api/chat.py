from fastapi import APIRouter
from pydantic import BaseModel
import time
import random

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat_with_tutor(data: ChatRequest):
    time.sleep(1) # محاكاة التفكير
    user_msg = data.message.lower()
    
    response = "أنا هنا. "
    
    if "pass" in user_msg or "مقبول" in user_msg:
        response = "للحصول على **Pass**، ركز على الوصف الدقيق والشرح الواضح للمفاهيم."
    elif "merit" in user_msg or "جيد" in user_msg:
        response = "للحصول على **Merit**، يجب عليك التحليل والمقارنة بين الأساليب المختلفة."
    elif "distinction" in user_msg or "امتياز" in user_msg:
        response = "للوصول إلى **Distinction**، قدم تقييماً نقدياً وحلولاً مبررة بالأدلة."
    else:
        response = "أهلاً بك! اسألني عن معايير BTEC (Pass, Merit, Distinction)."
        
    return {"response": response}
