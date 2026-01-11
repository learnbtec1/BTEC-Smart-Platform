import sys
import os

# التأكد من أن مسار المشروع مضاف
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from sqlmodel import Session as _Session
from app.main import app
from app.core.config import settings
from tests.utils.utils import random_email, random_lower_string
from tests.utils.user import user_authentication_headers
from app import crud
from app.database import engine
from app.models import UserCreate  # استيراد الموديل الصحيح

# تشغيل سيناريو واحد يفشل عادة (تحديث الإيميل لإيميل مستخدم آخر)
def run_debug():
    with TestClient(app) as client:
        # 1. إنشاء مستخدم "آخر" في قاعدة البيانات ليكون هناك تعارض
        username_conflict = random_email()
        pwd_conflict = random_lower_string()
        
        print(f"Creating conflict user: {username_conflict}")
        
        with _Session(engine) as db:
            user_in = UserCreate(email=username_conflict, password=pwd_conflict)
            crud.create_user(session=db, user_create=user_in)
            
        # 2. الحصول على توكن للمستخدم الحالي (Test User)
        # ملاحظة: نستخدم كلمة المرور الصحيحة إذا كانت ثابتة، أو ننشئ مستخدمًا جديدًا
        # هنا سنحاول استخدام الدالة المساعدة
        print(f"Getting token for: {settings.EMAIL_TEST_USER}")
        
        # قد تفشل هذه الخطوة وتعطي 401 إذا كان المستخدم غير موجود في الـ DB
        # وهذا ما نحاول فحصه
        try:
            headers = user_authentication_headers(client=client, email=settings.EMAIL_TEST_USER, password="changethis") 
            # ملاحظة: كلمة السر الافتراضية عادة "changethis" في config.py
            # إذا فشل هذا، فالمشكلة أن المستخدم Test User غير موجود
        except Exception as e:
            print(f"Auth failed immediately: {e}")
            return

        # 3. محاولة تحديث الإيميل للإيميل المتعارض
        r = client.patch(
            f"{settings.API_V1_STR}/users/me", 
            headers=headers, 
            json={"email": username_conflict}
        )
        
        print(f"PATCH /users/me result -> Status: {r.status_code}")
        print(f"Response: {r.json()}")

if __name__ == "__main__":
    run_debug()