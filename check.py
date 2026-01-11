import os

# قائمة المجلدات المراد فحصها
folders = [
    r"D:\BTEC-backend\backend\app\knowledge_base\Business\iq",
    r"D:\BTEC-backend\backend\app\knowledge_base\Business\L2 Grade 10",
    r"D:\BTEC-backend\backend\app\knowledge_base\Business\L3 Grade 11",
    r"D:\BTEC-backend\backend\app\knowledge_base\Business\L3 Grade 12"
]

print("--- جاري التحقق من المسارات ---")
for path in folders:
    if os.path.exists(path):
        print(f"✅ موجود: {path}")
    else:
        print(f"❌ غير موجود: {path}")