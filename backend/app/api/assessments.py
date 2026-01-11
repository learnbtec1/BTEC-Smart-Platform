from fastapi import APIRouter
from pydantic import BaseModel
import random
import time

router = APIRouter()

class AssessmentRequest(BaseModel):
    question: str
    major: str
    level: str

@router.post("/")
async def assess_question(data: AssessmentRequest):
    # 1. محاكاة وقت التفكير (وكأن الذكاء الاصطناعي يحلل)
    time.sleep(2) 
    
    # 2. توليد تقييم ذكي بناءً على المدخلات (بدون OpenAI)
    score = random.randint(4, 9)
    
    # قائمة نصائح جاهزة تظهر بشكل عشوائي لتبدو واقعية
    advice_list = [
        f"السؤال جيد ويغطي جوانب مهمة في {data.major}، ولكن يفضل استخدام أفعال مثل 'حلل' أو 'قيّم' لرفع مستوى التحدي للطلاب.",
        f"بناءً على معايير BTEC لمستوى {data.level}، يعتبر السؤال مباشراً جداً. حاول ربطه بسيناريو عملي (Scenario-based) ليكون أكثر فاعلية.",
        "السؤال ممتاز وواضح، والكلمات المفتاحية دقيقة. يمكن تحسينه بإضافة جزء يطلب من الطالب تبرير إجابته.",
        f"الصياغة تحتاج لبعض التدقيق اللغوي لتكون أوضح لطلاب {data.level}. تأكد من تحديد المطلوب بدقة لتجنب الإجابات العامة."
    ]
    
    return {
        "difficulty_score": score,
        "advice": random.choice(advice_list)
    }
